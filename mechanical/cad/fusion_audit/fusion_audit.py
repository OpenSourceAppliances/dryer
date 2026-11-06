"""fusion_audit.py: measure every STEP file of the dryer inside Autodesk Fusion, with Fusion's own kernel.

This is the independent half of the CAD audit (docs/verification.md, V-014). cad_audit.py measures the files
with OpenCascade; this script measures the same files with Autodesk's kernel and writes one CSV that
cad_audit.py --fusion compares body by body and feature by feature.

How to run it, inside Fusion on Windows:
  1. Utilities > Add-Ins > Scripts and Add-Ins (Shift+S), or File > Scripts and Add-Ins.
  2. Scripts tab, the + next to My Scripts, pick the folder mechanical/cad/fusion_audit (it holds this file
     and fusion_audit.manifest), then select fusion_audit and Run.
  Or, in the Text Commands window (File > View > Show Text Commands), switch the toggle to Py and type
     exec(open(r"C:\\...\\mechanical\\cad\\fusion_audit\\fusion_audit.py").read()); main()
  Set the two paths below first if the repo is somewhere else.

It opens every STEP in STEP_DIR in a new unsaved document, measures, writes the CSV and a log, and closes
the documents without saving. Nothing is uploaded; Fusion's local STEP translator is used.
Units: Fusion's API works in cm; everything here is converted to mm.
"""
import csv
import glob
import math
import os
import time
import traceback

import adsk.core
import adsk.fusion

STEP_DIR = r"C:\Users\cory\appliances\osa-dryer\mechanical\step"
OUT_DIR = r"C:\Users\cory\appliances\osa-dryer\mechanical\cad\audit"
OUT_CSV = os.path.join(OUT_DIR, "fusion-measured.csv")
OUT_LOG = os.path.join(OUT_DIR, "fusion-audit.log")

CLEAR_PAIRS = [
    ("drum-sheet", "front-bulkhead"), ("drum-sheet", "rear-bulkhead"), ("drum-sheet", "bay-ceiling"),
    ("drum-sheet", "side-panel-left"), ("drum-sheet", "side-panel-right"), ("drum-sheet", "top-panel"),
    ("drum-sheet", "rail-top-left"), ("drum-sheet", "rail-top-right"), ("drum-sheet", "rail-top-front"),
    ("drum-sheet", "roller-front-1 (bought)"), ("drum-sheet", "roller-front-2 (bought)"),
    ("drum-sheet", "roller-rear-1 (bought)"), ("drum-sheet", "roller-rear-2 (bought)"),
    ("drum-sheet", "drum-ring-front"), ("drum-sheet", "drum-ring-rear"), ("drum-sheet", "drum-splice"),
    ("drum-sheet", "baffle-1 (angle, cut to length)"), ("drum-ring-front", "front-bulkhead"),
    ("drum-ring-rear", "rear-bulkhead"), ("door-ring", "front-upper-panel"), ("door-disc", "door-ring"),
    ("console-face", "console-cheek-left"), ("console-face", "console-cheek-right"), ("console-face", "top-panel"),
    ("console-face", "console-cap"), ("front-bulkhead", "bay-ceiling"), ("rear-bulkhead", "bay-ceiling"),
    ("lint-duct", "rail-mid-front-left"), ("lint-duct", "rail-mid-front-right"), ("lint-duct", "front-bulkhead"),
    ("lint-duct", "front-upper-panel"), ("riser-duct", "rear-bulkhead"), ("riser-duct", "rail-mid-rear"),
    ("riser-duct", "bay-ceiling"), ("heat-module (envelope)", "heat-module-tray"), ("heat-module (envelope)", "bay-ceiling"),
    ("motor (bought)", "base-pan"), ("blower (bought)", "front-bulkhead"), ("blower (bought)", "lint-duct-transition"),
    ("pulley (bought)", "bay-ceiling"), ("exhaust-duct (bought)", "rear-lower-panel"), ("power-module (envelope)", "side-panel-left"),
    ("power-module (envelope)", "bay-ceiling"), ("drum-sheet", "front-upper-panel"),
]

FIELDS = ["record", "file", "body", "other", "is_solid", "volume_mm3", "area_mm2", "faces", "planar_faces", "cylindrical_faces",
          "edges", "vertices", "xmin", "ymin", "zmin", "xmax", "ymax", "zmax", "radius", "ax", "ay", "az", "fx", "fy", "fz",
          "t0", "t1", "length", "n_faces", "value_mm", "note"]


def mm(v):
    return v * 10.0


def log(f, msg):
    f.write(msg + "\n")
    f.flush()


def canon_axis(d):
    v = [d.x, d.y, d.z]
    for c in v:
        if abs(c) > 1e-9:
            if c < 0:
                v = [-x for x in v]
            break
    return v


def measure_body(rows, logf, file_tag, body_name, body):
    bb = body.boundingBox
    n_plane = n_cyl = 0
    groups = []
    for face in body.faces:
        g = face.geometry
        st = g.surfaceType
        if st == adsk.core.SurfaceTypes.PlaneSurfaceType:
            n_plane += 1
        elif st == adsk.core.SurfaceTypes.CylinderSurfaceType:
            n_cyl += 1
            cyl = adsk.core.Cylinder.cast(g)
            r = mm(cyl.radius)
            o = cyl.origin
            loc = [mm(o.x), mm(o.y), mm(o.z)]
            dv = canon_axis(cyl.axis)
            t = sum(l * a for l, a in zip(loc, dv))
            foot = [l - t * a for l, a in zip(loc, dv)]
            fb = face.boundingBox
            corners = [(x, y, z) for x in (mm(fb.minPoint.x), mm(fb.maxPoint.x)) for y in (mm(fb.minPoint.y), mm(fb.maxPoint.y)) for z in (mm(fb.minPoint.z), mm(fb.maxPoint.z))]
            ts = [sum(c * a for c, a in zip(cc, dv)) for cc in corners]
            t0, t1 = min(ts), max(ts)
            placed = False
            for grp in groups:
                if abs(grp["r"] - r) < 1e-4 and all(abs(a - b) < 1e-6 for a, b in zip(grp["dir"], dv)) \
                        and all(abs(a - b) < 1e-3 for a, b in zip(grp["foot"], foot)) \
                        and t0 <= grp["t1"] + 0.01 and t1 >= grp["t0"] - 0.01:
                    grp["t0"] = min(grp["t0"], t0)
                    grp["t1"] = max(grp["t1"], t1)
                    grp["n"] += 1
                    placed = True
                    break
            if not placed:
                groups.append(dict(r=r, dir=dv, foot=foot, t0=t0, t1=t1, n=1))
    rows.append(dict(record="body", file=file_tag, body=body_name, is_solid=int(body.isSolid),
                     volume_mm3=round(body.volume * 1000.0, 4), area_mm2=round(body.area * 100.0, 4),
                     faces=body.faces.count, planar_faces=n_plane, cylindrical_faces=n_cyl,
                     edges=body.edges.count, vertices=body.vertices.count,
                     xmin=round(mm(bb.minPoint.x), 5), ymin=round(mm(bb.minPoint.y), 5), zmin=round(mm(bb.minPoint.z), 5),
                     xmax=round(mm(bb.maxPoint.x), 5), ymax=round(mm(bb.maxPoint.y), 5), zmax=round(mm(bb.maxPoint.z), 5)))
    for grp in groups:
        rows.append(dict(record="cylinder", file=file_tag, body=body_name, radius=round(grp["r"], 5),
                         ax=round(grp["dir"][0], 6), ay=round(grp["dir"][1], 6), az=round(grp["dir"][2], 6),
                         fx=round(grp["foot"][0], 5), fy=round(grp["foot"][1], 5), fz=round(grp["foot"][2], 5),
                         t0=round(grp["t0"], 5), t1=round(grp["t1"], 5), length=round(grp["t1"] - grp["t0"], 5), n_faces=grp["n"]))
    log(logf, f"  {body_name}: solid {body.isSolid}, {body.faces.count} faces ({n_plane} planar, {n_cyl} cylindrical in {len(groups)} cylinders), volume {body.volume * 1000.0:.3f} mm3")


def all_bodies(design):
    """(name, body) for the root bodies and every occurrence's bodies, in the root coordinate system."""
    out = []
    root = design.rootComponent
    for b in root.bRepBodies:
        out.append((b.name, b))
    for occ in root.allOccurrences:
        for b in occ.bRepBodies:
            out.append((occ.component.name, b))
    return out


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    app = adsk.core.Application.get()
    ui = app.userInterface
    rows = []
    with open(OUT_LOG, "w", encoding="utf-8") as logf:
        log(logf, f"fusion_audit start {time.strftime('%Y-%m-%d %H:%M:%S')}  Fusion {app.version}")
        im = app.importManager
        files = sorted(glob.glob(os.path.join(STEP_DIR, "*.step")))
        log(logf, f"{len(files)} STEP files in {STEP_DIR}")
        for path in files:
            tag = os.path.splitext(os.path.basename(path))[0]
            log(logf, f"importing {tag}")
            doc = None
            try:
                opts = im.createSTEPImportOptions(path)
                doc = im.importToNewDocument(opts)
                if doc is None:
                    log(logf, f"  import returned no document")
                    rows.append(dict(record="error", file=tag, note="import returned no document"))
                    continue
                design = adsk.fusion.Design.cast(doc.products.itemByProductType("DesignProductType"))
                bodies = all_bodies(design)
                log(logf, f"  {len(bodies)} bodies")
                for name, body in bodies:
                    measure_body(rows, logf, tag, name, body)
                if tag == "osa-dryer-assembly":
                    by_name = {}
                    for name, body in bodies:
                        by_name.setdefault(name, body)
                    mm_ = app.measureManager
                    for a, b in CLEAR_PAIRS:
                        if a in by_name and b in by_name:
                            res = mm_.measureMinimumDistance(by_name[a], by_name[b])
                            rows.append(dict(record="distance", file=tag, body=a, other=b, value_mm=round(mm(res.value), 5)))
                            log(logf, f"  distance {a} / {b}: {mm(res.value):.4f} mm")
                        else:
                            rows.append(dict(record="distance", file=tag, body=a, other=b, note="body not found"))
                            log(logf, f"  distance {a} / {b}: body not found")
            except Exception:
                log(logf, "  ERROR " + traceback.format_exc())
                rows.append(dict(record="error", file=tag, note=traceback.format_exc().splitlines()[-1]))
            finally:
                if doc is not None:
                    try:
                        doc.close(False)
                    except Exception:
                        log(logf, "  could not close the document: " + traceback.format_exc().splitlines()[-1])
        with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=FIELDS)
            w.writeheader()
            for r in rows:
                w.writerow(r)
        n_bodies = sum(1 for r in rows if r["record"] == "body")
        n_err = sum(1 for r in rows if r["record"] == "error")
        log(logf, f"done: {n_bodies} bodies, {sum(1 for r in rows if r['record'] == 'cylinder')} cylinders, {sum(1 for r in rows if r['record'] == 'distance')} distances, {n_err} errors")
        log(logf, f"wrote {OUT_CSV}")
    try:
        app.log(f"fusion_audit done: {n_bodies} bodies, {n_err} errors, see {OUT_LOG}")
    except Exception:
        pass
    return n_bodies, n_err


def run(context):
    """Entry point when run from Scripts and Add-Ins."""
    try:
        n_bodies, n_err = main()
        adsk.core.Application.get().userInterface.messageBox(f"fusion_audit done: {n_bodies} bodies measured, {n_err} errors.\nCSV: {OUT_CSV}")
    except Exception:
        try:
            adsk.core.Application.get().userInterface.messageBox("fusion_audit failed:\n" + traceback.format_exc())
        except Exception:
            pass

