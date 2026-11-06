#!/usr/bin/env python3
"""cad_audit.py: measure everything the model wrote and compare it with what the documents say.

    python3 cad_audit.py <outdir> [--fusion <fusion-measured.csv>]

<outdir> is the folder osa_dryer_cad.py wrote (it holds step/ and drawings/). The audit reads only the
files on disk, never the live model, so it checks what a builder downloads. It uses the OpenCascade
kernel through OCP (the same kernel FreeCAD uses) and ezdxf for the drawings, and writes into
mechanical/cad/audit/ (next to this script):

  measured-parts.csv       one row per STEP part: solids, validity, closed shells, bounding box, volume,
                           surface area, face and edge counts, thickness and normal for flat parts
  measured-cylinders.csv   every cylindrical surface in every part: diameter, axis, position, length
                           (holes, drums, rollers, ducts)
  measured-planes.csv      every planar face: normal, area, centroid
  measured-loops.csv       every closed loop in the mid-plane section of every flat part, and every
                           closed loop in every DXF: type, centre, size
  measured-clearances.csv  minimum distance between chosen pairs of parts in the assembly
  audit-report.md          every expected value from the documents against the measured value,
                           PASS or FAIL, then the generic checks, then the inventory

The expected values come from expected-dimensions.csv, which is written from docs/design-rules.md,
controls/uci-spec.md and drawings/frame-cut-list.csv, not from the CAD script. If a value is only in
the script, it is not in that file; it is still measured and listed.

With --fusion, a CSV written by fusion_audit.py (the same measurements taken inside Autodesk Fusion
with its own kernel) is compared body by body and feature by feature.

Exit code 1 on any FAIL. Draft 4, 2026-11-06: rounded-rectangle outlines (laser corner radii), the T-slot
profiles' bores and corner radii, engraving excluded from the diameter list, the pan's bracket holes.
"""
import csv
import glob
import itertools
import math
import os
import sys

from OCP.Bnd import Bnd_Box
from OCP.BRep import BRep_Tool
from OCP.BRepAdaptor import BRepAdaptor_Curve, BRepAdaptor_Surface
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common, BRepAlgoAPI_Section
from OCP.BRepBndLib import BRepBndLib
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.BRepExtrema import BRepExtrema_DistShapeShape
from OCP.BRepGProp import BRepGProp
from OCP.GeomAbs import GeomAbs_Circle, GeomAbs_Cylinder, GeomAbs_Line, GeomAbs_Plane
from OCP.gp import gp_Dir, gp_Pln, gp_Pnt
from OCP.GProp import GProp_GProps
from OCP.IFSelect import IFSelect_RetDone
from OCP.STEPCAFControl import STEPCAFControl_Reader
from OCP.STEPControl import STEPControl_Reader
from OCP.TCollection import TCollection_ExtendedString
from OCP.TDataStd import TDataStd_Name
from OCP.TDF import TDF_LabelSequence
from OCP.TDocStd import TDocStd_Document
from OCP.TopAbs import TopAbs_EDGE, TopAbs_FACE, TopAbs_SHELL, TopAbs_SOLID, TopAbs_VERTEX
from OCP.TopExp import TopExp_Explorer
from OCP.TopoDS import TopoDS
from OCP.XCAFDoc import XCAFDoc_DocumentTool

try:
    import ezdxf
except ImportError:  # the DXF half of the audit needs it
    ezdxf = None

TOL_POS = 0.01      # mm, positions and sizes
TOL_ANG = 1e-4      # direction cosines
TOL_VOL = 1e-4      # relative, volumes

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
FUSION_CSV = None
if "--fusion" in sys.argv:
    FUSION_CSV = sys.argv[sys.argv.index("--fusion") + 1]
HERE = os.path.dirname(os.path.abspath(__file__))
AUD = os.path.join(HERE, "audit")      # next to this script, whatever <outdir> is
os.makedirs(AUD, exist_ok=True)

results = []     # (id, part, check, expected, measured, status, source)
generic = []     # (part, check, measured, status)
notes = []


def r3(v):
    return round(float(v) + 0.0, 3)


def pt(p):
    return (p.X(), p.Y(), p.Z())


# ---------------------------------------------------------------------------
# STEP reading
# ---------------------------------------------------------------------------
def read_step(path):
    rd = STEPControl_Reader()
    if rd.ReadFile(path) != IFSelect_RetDone:
        raise RuntimeError(f"cannot read {path}")
    rd.TransferRoots()
    return rd.OneShape()


def read_step_named(path):
    """The assembly: every top-level product with its name, through XCAF."""
    doc = TDocStd_Document(TCollection_ExtendedString("audit"))
    rd = STEPCAFControl_Reader()
    rd.SetNameMode(True)
    if rd.ReadFile(path) != IFSelect_RetDone:
        raise RuntimeError(f"cannot read {path}")
    rd.Transfer(doc)
    st = XCAFDoc_DocumentTool.ShapeTool_s(doc.Main())
    free = TDF_LabelSequence()
    st.GetFreeShapes(free)
    out = []

    def label_name(lab):
        nm = TDataStd_Name()
        if lab.FindAttribute(TDataStd_Name.GetID_s(), nm):
            return nm.Get().ToExtString()
        return ""

    def walk(lab, loc_shape_parent):
        comps = TDF_LabelSequence()
        if st.GetComponents_s(lab, comps) and comps.Length() > 0:
            for i in range(1, comps.Length() + 1):
                c = comps.Value(i)
                ref = c
                if st.IsReference_s(c):
                    from OCP.TDF import TDF_Label
                    ref = TDF_Label()
                    st.GetReferredShape_s(c, ref)
                shape = st.GetShape_s(c)          # placed in the parent
                name = label_name(ref) or label_name(c)
                sub = TDF_LabelSequence()
                if st.GetComponents_s(ref, sub) and sub.Length() > 0:
                    walk(ref, shape)
                else:
                    out.append((name, shape))
        else:
            out.append((label_name(lab), st.GetShape_s(lab)))

    for i in range(1, free.Length() + 1):
        walk(free.Value(i), None)
    return out


def explore(shape, kind):
    ex = TopExp_Explorer(shape, kind)
    seen = set()
    while ex.More():
        s = ex.Current()
        h = s.HashCode(1 << 30) if hasattr(s, "HashCode") else id(s)
        key = (h, s.IsSame)
        ex.Next()
        yield s


def solids_of(shape):
    out = []
    ex = TopExp_Explorer(shape, TopAbs_SOLID)
    while ex.More():
        out.append(TopoDS.Solid_s(ex.Current()))
        ex.Next()
    return out


def faces_of(shape):
    out = []
    ex = TopExp_Explorer(shape, TopAbs_FACE)
    while ex.More():
        out.append(TopoDS.Face_s(ex.Current()))
        ex.Next()
    return out


def edges_of(shape):
    out = []
    ex = TopExp_Explorer(shape, TopAbs_EDGE)
    while ex.More():
        out.append(TopoDS.Edge_s(ex.Current()))
        ex.Next()
    return out


def count(shape, kind):
    n = 0
    ex = TopExp_Explorer(shape, kind)
    while ex.More():
        n += 1
        ex.Next()
    return n


def bbox(shape):
    b = Bnd_Box()
    BRepBndLib.AddOptimal_s(shape, b, False, False)
    return b.Get()   # xmin, ymin, zmin, xmax, ymax, zmax


def volume(shape):
    g = GProp_GProps()
    BRepGProp.VolumeProperties_s(shape, g, 1e-6)
    return g.Mass()


def area(shape):
    g = GProp_GProps()
    BRepGProp.SurfaceProperties_s(shape, g)
    return g.Mass()


def centroid(shape):
    g = GProp_GProps()
    BRepGProp.SurfaceProperties_s(shape, g)
    return pt(g.CentreOfMass())


def is_closed(solid):
    ex = TopExp_Explorer(solid, TopAbs_SHELL)
    while ex.More():
        if not BRep_Tool.IsClosed_s(ex.Current()):
            return False
        ex.Next()
    return True


def face_planes(shape):
    """Every planar face: (normal, area, centroid)."""
    out = []
    for f in faces_of(shape):
        ad = BRepAdaptor_Surface(f)
        if ad.GetType() == GeomAbs_Plane:
            n = ad.Plane().Axis().Direction()
            nn = (n.X(), n.Y(), n.Z())
            if f.Orientation().name == "REVERSED" if hasattr(f.Orientation(), "name") else False:
                nn = (-nn[0], -nn[1], -nn[2])
            out.append((nn, area(f), centroid(f)))
    return out


def face_cylinders(shape):
    """Every cylindrical face grouped into cylinders: (radius, axis dir, axis point, length along axis, n faces)."""
    groups = []
    for f in faces_of(shape):
        ad = BRepAdaptor_Surface(f)
        if ad.GetType() != GeomAbs_Cylinder:
            continue
        cyl = ad.Cylinder()
        r = cyl.Radius()
        ax = cyl.Axis()
        d = ax.Direction()
        dv = (d.X(), d.Y(), d.Z())
        loc = pt(ax.Location())
        # canonical axis: positive leading component
        for comp in dv:
            if abs(comp) > TOL_ANG:
                if comp < 0:
                    dv = (-dv[0], -dv[1], -dv[2])
                break
        # axis point: the projection of the origin's foot, i.e. loc minus its component along dv
        t = sum(l * a for l, a in zip(loc, dv))
        foot = tuple(l - t * a for l, a in zip(loc, dv))
        # extent of this face along the axis
        b = bbox(f)
        corners = [(x, y, z) for x in (b[0], b[3]) for y in (b[1], b[4]) for z in (b[2], b[5])]
        ts = [sum(c * a for c, a in zip(cc, dv)) for cc in corners]
        t0, t1 = min(ts), max(ts)
        placed = False
        for g in groups:
            if abs(g["r"] - r) < 1e-4 and all(abs(a - b2) < 1e-6 for a, b2 in zip(g["dir"], dv)) \
                    and all(abs(a - b2) < 1e-4 for a, b2 in zip(g["foot"], foot)) \
                    and t0 <= g["t1"] + 0.01 and t1 >= g["t0"] - 0.01:
                g["t0"] = min(g["t0"], t0)
                g["t1"] = max(g["t1"], t1)
                g["faces"] += 1
                g["area"] += area(f)
                placed = True
                break
        if not placed:
            groups.append(dict(r=r, dir=dv, foot=foot, t0=t0, t1=t1, faces=1, area=area(f)))
    for g in groups:
        g["length"] = g["t1"] - g["t0"]
        g["mid"] = tuple(fo + (g["t0"] + g["t1"]) / 2 * a for fo, a in zip(g["foot"], g["dir"]))
    return groups


# ---------------------------------------------------------------------------
# 2D loops: from a STEP section and from a DXF, classified the same way
# ---------------------------------------------------------------------------
class Seg:
    """A line (kind L) or an arc (kind A) in 2D. An arc's geometry is the counter-clockwise sweep from a0 to a1 (radians),
    whichever way the loop traverses it; p0 and p1 are its ends in traversal order."""

    def __init__(self, kind, p0, p1, c=None, r=None, a0=None, a1=None):
        self.kind, self.p0, self.p1, self.c, self.r, self.a0, self.a1 = kind, p0, p1, c, r, a0, a1

    def sweep(self):
        if self.kind != "A":
            return 0.0
        s = self.a1 - self.a0
        while s < -1e-9:
            s += 2 * math.pi
        return s

    def reversed(self):
        if self.kind == "L":
            return Seg("L", self.p1, self.p0)
        return Seg("A", self.p1, self.p0, self.c, self.r, self.a0, self.a1)   # the same arc, walked the other way


def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def chain_loops(segs, tol=1e-3):
    """Join segments end to end into closed loops. Returns (loops, open_count)."""
    loops = []
    remaining = list(segs)
    open_count = 0
    while remaining:
        cur = [remaining.pop()]
        closed = False
        while True:
            end = cur[-1].p1
            start = cur[0].p0
            if len(cur) > 0 and dist(end, start) < tol:
                closed = True
                break
            found = None
            for i, s in enumerate(remaining):
                if dist(s.p0, end) < tol:
                    found = (i, s)
                    break
                if dist(s.p1, end) < tol:
                    found = (i, s.reversed())
                    break
            if found is None:
                break
            remaining.pop(found[0])
            cur.append(found[1])
        if closed:
            loops.append(cur)
        else:
            open_count += 1
    return loops, open_count


def loop_bbox(loop):
    """Bounding box of a loop, including the extreme points of its arcs."""
    xs, ys = [], []
    for s in loop:
        xs += [s.p0[0], s.p1[0]]
        ys += [s.p0[1], s.p1[1]]
        if s.kind == "A":
            a0, sw = s.a0, s.sweep()
            for k in range(-4, 9):   # every quarter-turn direction the arc passes through
                a = k * math.pi / 2
                d = (a - a0) % (2 * math.pi)
                if d <= sw + 1e-9:
                    xs.append(s.c[0] + s.r * math.cos(a))
                    ys.append(s.c[1] + s.r * math.sin(a))
    return min(xs), min(ys), max(xs), max(ys)


def classify(loop):
    """-> dict(type, cx, cy, w, h, extra). Types: circle, rect, rrect (rounded rectangle), rpoly (polygon with rounded
    corners), slot, polygon, other. Sizes include the arcs' extreme points."""
    kinds = [s.kind for s in loop]
    # merge consecutive arcs on the same circle
    merged = []
    for s in loop:
        if merged and s.kind == "A" and merged[-1].kind == "A" and dist(s.c, merged[-1].c) < 1e-3 and abs(s.r - merged[-1].r) < 1e-3:
            m = merged[-1]
            # the two CCW pieces join at one angle; the merged arc runs CCW from the piece that starts first
            if abs(((m.a1 - s.a0) + math.pi) % (2 * math.pi) - math.pi) < 1e-6:
                merged[-1] = Seg("A", m.p0, s.p1, m.c, m.r, m.a0, m.a0 + m.sweep() + s.sweep())
            else:
                merged[-1] = Seg("A", m.p0, s.p1, m.c, m.r, s.a0, s.a0 + s.sweep() + m.sweep())
        else:
            merged.append(s)
    loop = merged
    if len(loop) == 1 and loop[0].kind == "A":
        s = loop[0]
        return dict(type="circle", cx=s.c[0], cy=s.c[1], w=2 * s.r, h=2 * s.r, n=1)
    if len(loop) == 2 and all(s.kind == "A" for s in loop) and dist(loop[0].c, loop[1].c) < 1e-3:
        s = loop[0]
        return dict(type="circle", cx=s.c[0], cy=s.c[1], w=2 * s.r, h=2 * s.r, n=1)
    if all(s.kind == "L" for s in loop):
        pts = [s.p0 for s in loop]
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        if len(loop) == 4:
            axis_aligned = all(abs(s.p0[0] - s.p1[0]) < 1e-3 or abs(s.p0[1] - s.p1[1]) < 1e-3 for s in loop)
            if axis_aligned:
                return dict(type="rect", cx=(min(xs) + max(xs)) / 2, cy=(min(ys) + max(ys)) / 2,
                            w=max(xs) - min(xs), h=max(ys) - min(ys), n=4)
        return dict(type="polygon", cx=(min(xs) + max(xs)) / 2, cy=(min(ys) + max(ys)) / 2,
                    w=max(xs) - min(xs), h=max(ys) - min(ys), n=len(loop),
                    verts=[(round(x, 3), round(y, 3)) for x, y in pts])
    arcs = [s for s in loop if s.kind == "A"]
    lines = [s for s in loop if s.kind == "L"]
    def quarter(a):
        return abs(a.sweep() - math.pi / 2) < 1e-3
    if len(arcs) == 4 and len(lines) == 4 and all(abs(a.r - arcs[0].r) < 1e-3 for a in arcs) and all(quarter(a) for a in arcs):
        r = arcs[0].r
        cxs, cys = [a.c[0] for a in arcs], [a.c[1] for a in arcs]
        ln = max(lines, key=lambda l: dist(l.p0, l.p1))
        ang = math.degrees(math.atan2(ln.p1[1] - ln.p0[1], ln.p1[0] - ln.p0[0])) % 180.0
        if ang < 1e-3 or abs(ang - 90) < 1e-3 or abs(ang - 180) < 1e-3:
            w, h = max(cxs) - min(cxs) + 2 * r, max(cys) - min(cys) + 2 * r
        else:   # turned: measure along and across the long line
            ux, uy = (ln.p1[0] - ln.p0[0]) / dist(ln.p0, ln.p1), (ln.p1[1] - ln.p0[1]) / dist(ln.p0, ln.p1)
            us = [c[0] * ux + c[1] * uy for c in zip(cxs, cys)]
            vs = [-c[0] * uy + c[1] * ux for c in zip(cxs, cys)]
            w, h = max(us) - min(us) + 2 * r, max(vs) - min(vs) + 2 * r
        return dict(type="rrect", cx=(min(cxs) + max(cxs)) / 2, cy=(min(cys) + max(cys)) / 2, w=w, h=h, n=8, r=r, angle=round(ang, 3))
    if len(arcs) == 2 and len(lines) == 2 and abs(arcs[0].r - arcs[1].r) < 1e-3 \
            and all(abs(a.sweep() - math.pi) < 1e-3 for a in arcs):
        c0, c1 = arcs[0].c, arcs[1].c
        r = arcs[0].r
        length = dist(c0, c1) + 2 * r
        horizontal = abs(c0[1] - c1[1]) < 1e-3
        w, h = (length, 2 * r) if horizontal else (2 * r, length)
        return dict(type="slot", cx=(c0[0] + c1[0]) / 2, cy=(c0[1] + c1[1]) / 2, w=w, h=h, n=4)
    if len(arcs) == 2 and len(lines) == 2 and dist(arcs[0].c, arcs[1].c) < 1e-3 and abs(arcs[0].r - arcs[1].r) > 1e-3 \
            and all(abs(a.sweep() - arcs[0].sweep()) < 1e-6 for a in arcs):
        # an annular sector (the curved lint slot): two concentric arcs of the same sweep joined by two radial lines.
        # Box and centre are the loop's own (for the inside-the-outline and overlap tests); the arc centre and radii
        # are kept for the rows that name them
        x0, y0, x1, y1 = loop_bbox(loop)
        r0, r1 = sorted(a.r for a in arcs)
        span = arcs[0].sweep()
        return dict(type="sector", cx=(x0 + x1) / 2, cy=(y0 + y1) / 2, w=x1 - x0, h=y1 - y0, n=4,
                    ccx=arcs[0].c[0], ccy=arcs[0].c[1], r0=r0, r1=r1, span_deg=math.degrees(span), area=span / 2 * (r1 ** 2 - r0 ** 2))
    if arcs and lines and all(abs(a.r - arcs[0].r) < 1e-3 for a in arcs) and all(a.sweep() <= math.pi + 1e-3 for a in arcs):
        # a polygon with every corner rounded to one radius (the notched ceiling plate, the cheeks): size from the box
        x0, y0, x1, y1 = loop_bbox(loop)
        return dict(type="rpoly", cx=(x0 + x1) / 2, cy=(y0 + y1) / 2, w=x1 - x0, h=y1 - y0, n=len(lines), r=arcs[0].r)
    x0, y0, x1, y1 = loop_bbox(loop)
    return dict(type="other", cx=(x0 + x1) / 2, cy=(y0 + y1) / 2, w=x1 - x0, h=y1 - y0, n=len(loop), kinds="".join(kinds))


def section_loops(shape, origin, normal, u_dir, v_dir):
    """Cut the shape with a plane and return 2D loops in (u, v) coordinates on that plane."""
    pln = gp_Pln(gp_Pnt(*origin), gp_Dir(*normal))
    sec = BRepAlgoAPI_Section(shape, pln, False)
    sec.ComputePCurveOn1(False)
    sec.Approximation(False)
    sec.Build()
    if not sec.IsDone():
        return [], -1

    def to2d(p):
        d = (p[0] - origin[0], p[1] - origin[1], p[2] - origin[2])
        return (sum(a * b for a, b in zip(d, u_dir)), sum(a * b for a, b in zip(d, v_dir)))

    # is (u, v, normal) right-handed? If not, counter-clockwise in 3D about the normal is clockwise in (u, v)
    w = (u_dir[1] * v_dir[2] - u_dir[2] * v_dir[1], u_dir[2] * v_dir[0] - u_dir[0] * v_dir[2], u_dir[0] * v_dir[1] - u_dir[1] * v_dir[0])
    handed = 1.0 if (w[0] * normal[0] + w[1] * normal[1] + w[2] * normal[2]) > 0 else -1.0

    segs = []
    for e in edges_of(sec.Shape()):
        ad = BRepAdaptor_Curve(e)
        t0, t1 = ad.FirstParameter(), ad.LastParameter()
        p0, p1 = to2d(pt(ad.Value(t0))), to2d(pt(ad.Value(t1)))
        if ad.GetType() == GeomAbs_Line:
            segs.append(Seg("L", p0, p1))
        elif ad.GetType() == GeomAbs_Circle:
            circ = ad.Circle()
            c = to2d(pt(circ.Location()))
            r = circ.Radius()
            # orientation of the circle in the plane: its axis along +normal or -normal
            ax = circ.Axis().Direction()
            sgn = (1.0 if (ax.X() * normal[0] + ax.Y() * normal[1] + ax.Z() * normal[2]) > 0 else -1.0) * handed
            a0 = math.atan2(p0[1] - c[1], p0[0] - c[0])
            a1 = math.atan2(p1[1] - c[1], p1[0] - c[0])
            if abs((t1 - t0) - 2 * math.pi) < 1e-6:
                segs.append(Seg("A", p0, p0, c, r, a0, a0 + 2 * math.pi))
            else:
                if sgn < 0:
                    a0, a1 = a1, a0
                    p0, p1 = p1, p0
                segs.append(Seg("A", p0, p1, c, r, a0, a1))
        else:
            # sample the curve into short lines
            n = 24
            prev = p0
            for i in range(1, n + 1):
                q = to2d(pt(ad.Value(t0 + (t1 - t0) * i / n)))
                segs.append(Seg("L", prev, q))
                prev = q
    loops, open_count = chain_loops(segs)
    return [classify(l) for l in loops], open_count


def dxf_loops(path):
    if ezdxf is None:
        return None, 0, {}
    doc = ezdxf.readfile(path)
    msp = doc.modelspace()
    segs = []
    circles = []
    kinds = {}
    cut_only = "CUT" in doc.layers      # a drawing with a CUT layer may carry labels and references on other layers
    for e in msp:
        k = e.dxftype()
        if cut_only and e.dxf.layer != "CUT":
            kinds[k + " (not CUT)"] = kinds.get(k + " (not CUT)", 0) + 1
            continue
        kinds[k] = kinds.get(k, 0) + 1
        if k == "LINE":
            segs.append(Seg("L", (e.dxf.start.x, e.dxf.start.y), (e.dxf.end.x, e.dxf.end.y)))
        elif k == "ARC":
            c = (e.dxf.center.x, e.dxf.center.y)
            r = e.dxf.radius
            a0, a1 = math.radians(e.dxf.start_angle), math.radians(e.dxf.end_angle)
            p0 = (c[0] + r * math.cos(a0), c[1] + r * math.sin(a0))
            p1 = (c[0] + r * math.cos(a1), c[1] + r * math.sin(a1))
            segs.append(Seg("A", p0, p1, c, r, a0, a1))
        elif k == "CIRCLE":
            c = (e.dxf.center.x, e.dxf.center.y)
            circles.append(dict(type="circle", cx=c[0], cy=c[1], w=2 * e.dxf.radius, h=2 * e.dxf.radius, n=1))
        elif k == "LWPOLYLINE":
            pts = [(p[0], p[1], p[2]) for p in e.get_points("xyb")]
            pairs = list(zip(pts, pts[1:] + ([pts[0]] if e.closed else [])))
            for a, b in pairs:
                if abs(a[2]) < 1e-12:
                    segs.append(Seg("L", (a[0], a[1]), (b[0], b[1])))
                else:   # a bulge segment is an arc; ezdxf gives centre, angles and radius
                    from ezdxf.math import bulge_to_arc
                    c, sa, ea, r = bulge_to_arc((a[0], a[1]), (b[0], b[1]), a[2])
                    p0 = (c[0] + r * math.cos(sa), c[1] + r * math.sin(sa))
                    p1 = (c[0] + r * math.cos(ea), c[1] + r * math.sin(ea))
                    segs.append(Seg("A", p0, p1, (c[0], c[1]), r, sa, ea))
        else:
            notes.append(f"{os.path.basename(path)}: entity {k} not handled by the audit")
    loops, open_count = chain_loops(segs)
    return [classify(l) for l in loops] + circles, open_count, kinds


def loop_key(lp):
    return (lp["type"], round(lp["cx"], 2), round(lp["cy"], 2), round(lp["w"], 2), round(lp["h"], 2))


def match_loops(a, b, tol=TOL_POS):
    """Pair loops of list a with loops of list b by type, centre and size. Returns (pairs, only_a, only_b)."""
    b_left = list(b)
    pairs, only_a = [], []
    for la in a:
        hit = None
        for i, lb in enumerate(b_left):
            if la["type"] == lb["type"] and abs(la["cx"] - lb["cx"]) < tol and abs(la["cy"] - lb["cy"]) < tol \
                    and abs(la["w"] - lb["w"]) < tol and abs(la["h"] - lb["h"]) < tol:
                hit = i
                break
        if hit is None:
            only_a.append(la)
        else:
            pairs.append((la, b_left.pop(hit)))
    return pairs, only_a, b_left


def loops_overlap(l1, l2):
    """Do two inner loops (circle/rect/slot/polygon, treated by bounding shapes) overlap? Conservative."""
    if l1["type"] == "circle" and l2["type"] == "circle":
        return dist((l1["cx"], l1["cy"]), (l2["cx"], l2["cy"])) < (l1["w"] + l2["w"]) / 2 - 1e-6
    # a sector against a circle about the sector's own centre (the curved lint slot round the door opening): the
    # circle has to cross the sector's ring of radii to overlap it
    for sec, circ in ((l1, l2), (l2, l1)):
        if sec["type"] == "sector" and circ["type"] == "circle" and dist((sec["ccx"], sec["ccy"]), (circ["cx"], circ["cy"])) < 1e-3:
            return sec["r0"] - 1e-6 < circ["w"] / 2 < sec["r1"] + 1e-6
    # rectangle test on bounding boxes for everything else (slots and rects are axis-aligned)
    ax0, ax1 = l1["cx"] - l1["w"] / 2, l1["cx"] + l1["w"] / 2
    ay0, ay1 = l1["cy"] - l1["h"] / 2, l1["cy"] + l1["h"] / 2
    bx0, bx1 = l2["cx"] - l2["w"] / 2, l2["cx"] + l2["w"] / 2
    by0, by1 = l2["cy"] - l2["h"] / 2, l2["cy"] + l2["h"] / 2
    if ax1 <= bx0 + 1e-6 or bx1 <= ax0 + 1e-6 or ay1 <= by0 + 1e-6 or by1 <= ay0 + 1e-6:
        return False
    # a circle against a box: check the box's nearest point
    for c, box in ((l1, l2), (l2, l1)):
        if c["type"] == "circle" and box["type"] != "circle":
            nx = min(max(c["cx"], box["cx"] - box["w"] / 2), box["cx"] + box["w"] / 2)
            ny = min(max(c["cy"], box["cy"] - box["h"] / 2), box["cy"] + box["h"] / 2)
            return dist((nx, ny), (c["cx"], c["cy"])) < c["w"] / 2 - 1e-6
    return True


# ---------------------------------------------------------------------------
# Measure every STEP part
# ---------------------------------------------------------------------------
parts = {}          # name -> dict of measurements
part_shapes = {}
step_files = sorted(glob.glob(os.path.join(OUT, "step", "*.step")))
assembly_path = os.path.join(OUT, "step", "osa-dryer-assembly.step")

PLANE_AXES = {   # for flat parts: (u, v) in-plane directions by the plate normal axis
    "x": ((0, 1, 0), (0, 0, 1)),
    "y": ((1, 0, 0), (0, 0, 1)),
    "z": ((1, 0, 0), (0, 1, 0)),
}

for path in step_files:
    name = os.path.splitext(os.path.basename(path))[0]
    if name == "osa-dryer-assembly":
        continue
    shape = read_step(path)
    part_shapes[name] = shape
    sol = solids_of(shape)
    m = dict(name=name, solids=len(sol))
    m["valid"] = int(BRepCheck_Analyzer(shape).IsValid())
    m["closed"] = int(all(is_closed(s) for s in sol))
    b = bbox(shape)
    m.update(xmin=b[0], ymin=b[1], zmin=b[2], xmax=b[3], ymax=b[4], zmax=b[5])
    m.update(sx=b[3] - b[0], sy=b[4] - b[1], sz=b[5] - b[2])
    m["volume"] = volume(shape)
    m["area"] = area(shape)
    m["faces"] = count(shape, TopAbs_FACE)
    m["edges"] = count(shape, TopAbs_EDGE)
    m["vertices"] = count(shape, TopAbs_VERTEX)
    planes = face_planes(shape)
    cyls = face_cylinders(shape)
    m["planes"] = planes
    m["cylinders"] = cyls
    m["n_planes"] = len(planes)
    m["n_cyl_faces"] = sum(g["faces"] for g in cyls)
    m["n_other_faces"] = m["faces"] - m["n_planes"] - m["n_cyl_faces"]
    # flat part? the largest plane and the largest opposite plane close together
    big = sorted(planes, key=lambda p: -p[1])
    m["flat"] = 0
    m["thickness"] = None
    m["normal"] = None
    if big:
        n0, a0, c0 = big[0]
        def facing(p):   # parallel, and straight across from the first face (a plate's two faces share their centre line)
            if abs(abs(sum(a * b2 for a, b2 in zip(p[0], n0))) - 1) > 1e-6:
                return False
            d = tuple(a - b2 for a, b2 in zip(p[2], c0))
            t_ = sum(a * b2 for a, b2 in zip(d, n0))
            lateral = math.sqrt(sum((a - t_ * b2) ** 2 for a, b2 in zip(d, n0)))
            return lateral < 0.5
        opp = [p for p in big[1:] if facing(p)]
        if opp:
            n1, a1, c1 = opp[0]
            t = abs(sum((a - b2) * c for a, b2, c in zip(c0, c1, n0)))
            if t <= 8.5 and a0 > 0.5 * a1 and a1 > 0.5 * a0 and abs(m["volume"] - a0 * t) < 0.5 * m["volume"]:   # and nothing much outside the two faces
                m["flat"] = 1
                m["thickness"] = t
                m["normal"] = n0
                mid = tuple((a + b2) / 2 for a, b2 in zip(c0, c1))
                m["mid_point"] = mid
    m["loops"] = None
    if m["flat"]:
        n = m["normal"]
        axis = None
        for ax_name, vec in (("x", (1, 0, 0)), ("y", (0, 1, 0)), ("z", (0, 0, 1))):
            if abs(abs(sum(a * b2 for a, b2 in zip(n, vec))) - 1) < 1e-6:
                axis = ax_name
        if axis:
            u, v = PLANE_AXES[axis]
            m["plane_axis"] = axis
        else:
            # tilted plate (the console face): u along X, v up the slope
            u = (1, 0, 0)
            v = (0, 0, 0)
            # v = normal x u, made to point up (+Z)
            v = (n[1] * 0 - n[2] * 0, n[2] * 1 - n[0] * 0, n[0] * 0 - n[1] * 1)
            v = (0.0, -n[2], n[1])
            if v[2] < 0:
                v = (0.0, -v[1], -v[2])
            m["plane_axis"] = "tilted"
        origin = m["mid_point"]
        # keep the origin at the world zero of the in-plane axes so 2D coordinates equal world coordinates
        if axis:
            o = [0.0, 0.0, 0.0]
            k = {"x": 0, "y": 1, "z": 2}[axis]
            o[k] = origin[k]
            origin = tuple(o)
        m["section_origin"] = origin
        m["section_u"], m["section_v"] = u, v
        loops, open_count = section_loops(shape, origin, n, u, v)
        if not axis and loops:   # tilted plate: (0, 0) is the outline's centre, not the faces' centroid (engraving moves that)
            outer = max(loops, key=lambda l: l["w"] * l["h"])
            ox, oy = outer["cx"], outer["cy"]
            for l in loops:
                l["cx"] -= ox
                l["cy"] -= oy
        m["loops"] = loops
        m["open_section_edges"] = open_count
    parts[name] = m
    print(f"measured {name}: solids {m['solids']} faces {m['faces']} vol {m['volume']:.1f}")

# ---------------------------------------------------------------------------
# The assembly
# ---------------------------------------------------------------------------
assembly = {}
assy_named = read_step_named(assembly_path)
for nm, shp in assy_named:
    sol = solids_of(shp)
    assembly[nm] = dict(name=nm, shape=shp, solids=len(sol), volume=volume(shp), bbox=bbox(shp))
print(f"assembly: {len(assembly)} named solids")

# ---------------------------------------------------------------------------
# DXF drawings
# ---------------------------------------------------------------------------
dxfs = {}
for path in sorted(glob.glob(os.path.join(OUT, "drawings", "*.dxf"))):
    name = os.path.splitext(os.path.basename(path))[0]
    loops, open_count, kinds = dxf_loops(path)
    dxfs[name] = dict(name=name, loops=loops, open=open_count, kinds=kinds)

cut_list = {}
with open(os.path.join(OUT, "drawings", "frame-cut-list.csv"), newline="") as f:
    for row in csv.DictReader(f):
        cut_list[row["item"]] = row

# ---------------------------------------------------------------------------
# Clearances in the assembly
# ---------------------------------------------------------------------------
def min_dist(a, b):
    d = BRepExtrema_DistShapeShape(a, b)
    d.Perform()
    return d.Value() if d.IsDone() else None


clearances = {}
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
    ("belt (bought, PJ 5 rib)", "drum-sheet"), ("belt (bought, PJ 5 rib)", "pulley (bought)"), ("belt (bought, PJ 5 rib)", "idler-pulley (bought, flat idler 40 with bearing)"),
    ("belt (bought, PJ 5 rib)", "bay-ceiling"), ("belt (bought, PJ 5 rib)", "motor (bought)"), ("belt (bought, PJ 5 rib)", "heat-module-tray"),
    ("door-hinge-1-fixed (bought, flag hinge, pinned half)", "door-disc"), ("door-hinge-2-swing (bought, flag hinge, lift-off half)", "door-ring"),
    ("door-seal (bought, OEM door seal)", "door-ring"), ("felt-seal-rear", "drum-ring-rear"), ("felt-seal-front", "drum-ring-front"),
    ("felt-seal-front", "drum-sheet"), ("felt-seal-rear", "drum-sheet"), ("tier0-faceplate", "console-face"),
    ("riser-duct", "heat-module (envelope)"), ("riser-duct", "rail-mid-rearcross"), ("riser-duct", "heat-module-tray"),
    ("lint-duct", "hardware-door-ring (bought, 8 x M4 x 8 button head, nuts)"), ("console-post-1", "top-panel"),
    ("console-post-1", "console-cheek-left"), ("console-rail-front", "console-cap"), ("console-rear", "rear-upper-panel"),
    ("console-cheek-left", "side-panel-left"), ("tier0-k1-relay-on-din-rail (bought)", "console-rail-front"),
    ("tier0-k1-relay-on-din-rail (bought)", "top-panel"), ("power-cord (bought)", "cord-bushing (bought, PG16 strain relief)"),
    ("power-cord (bought)", "feet (bought, 4 x M8 leveling feet, 50 pad)"), ("power-cord (bought)", "base-pan"),
    ("feet (bought, 4 x M8 leveling feet, 50 pad)", "base-pan"), ("hardware-drum-tabs (bought, 60 x M4 x 8 button head, nuts)", "front-bulkhead"),
    ("idler-pulley (bought, flat idler 40 with bearing)", "motor (bought)"), ("hardware-idler-axle (bought, M8 x 30 bolt, nut)", "motor (bought)"),
]
for a, b in CLEAR_PAIRS:
    if a in assembly and b in assembly:
        clearances[(a, b)] = min_dist(assembly[a]["shape"], assembly[b]["shape"])
    else:
        clearances[(a, b)] = None
        notes.append(f"clearance pair missing in the assembly: {a} / {b}")

# ---------------------------------------------------------------------------
# Generic checks (every part, no table needed)
# ---------------------------------------------------------------------------
def gen(part, check, measured, ok):
    generic.append((part, check, measured, "PASS" if ok else "FAIL"))


for name, m in parts.items():
    gen(name, "one solid", m["solids"], m["solids"] == 1)
    gen(name, "valid B-rep (BRepCheck)", m["valid"], m["valid"] == 1)
    gen(name, "closed shells", m["closed"], m["closed"] == 1)
    gen(name, "volume positive", round(m["volume"], 1), m["volume"] > 0)
    gen(name, "in the assembly with the same volume and place", name in assembly,
        name in assembly and abs(assembly[name]["volume"] - m["volume"]) <= TOL_VOL * m["volume"]
        and all(abs(a - b2) < TOL_POS for a, b2 in zip(assembly[name]["bbox"], (m["xmin"], m["ymin"], m["zmin"], m["xmax"], m["ymax"], m["zmax"]))))
    if m["flat"]:
        gen(name, "section edges all closed", m["open_section_edges"], m["open_section_edges"] == 0)
        loops = m["loops"]
        others = [l for l in loops if l["type"] == "other"]
        gen(name, "every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon", f"{len(loops)} loops, {len(others)} unclassified", not others)
        # one outer loop: the one with the largest box; every other loop inside it; no two inner loops overlap
        if loops:
            outer = max(loops, key=lambda l: l["w"] * l["h"])
            inner = [l for l in loops if l is not outer]
            inside = all(l["cx"] - l["w"] / 2 >= outer["cx"] - outer["w"] / 2 - 1e-6 and l["cx"] + l["w"] / 2 <= outer["cx"] + outer["w"] / 2 + 1e-6
                         and l["cy"] - l["h"] / 2 >= outer["cy"] - outer["h"] / 2 - 1e-6 and l["cy"] + l["h"] / 2 <= outer["cy"] + outer["h"] / 2 + 1e-6 for l in inner)
            gen(name, "every cut lies inside the outline", len(inner), inside)
            overl = [(loop_key(a), loop_key(b2)) for a, b2 in itertools.combinations(inner, 2) if loops_overlap(a, b2)]
            gen(name, "no two cuts overlap", f"{len(overl)} overlapping pairs" + (f": {overl[:3]}" if overl else ""), not overl)
            m["outer"] = outer
            m["inner"] = inner
    # DXF against the STEP section, loop by loop
    if name in dxfs and m["flat"]:
        d = dxfs[name]
        gen(name + ".dxf", "DXF entities join into closed loops", f"{d['open']} open chains", d["open"] == 0)
        dl = d["loops"]
        sl = m["loops"]
        # align by outer loop centre (round parts and the console face are drawn about the origin)
        if dl and sl:
            douter = max(dl, key=lambda l: l["w"] * l["h"])
            souter = max(sl, key=lambda l: l["w"] * l["h"])
            dx, dy = souter["cx"] - douter["cx"], souter["cy"] - douter["cy"]
            dl2 = [dict(l, cx=l["cx"] + dx, cy=l["cy"] + dy) for l in dl]
            pairs, only_s, only_d = match_loops(sl, dl2)
            gen(name + ".dxf", "every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm)",
                f"{len(pairs)} matched, {len(only_s)} only in STEP, {len(only_d)} only in DXF" + (f"; STEP-only {[loop_key(l) for l in only_s[:3]]}; DXF-only {[loop_key(l) for l in only_d[:3]]}" if only_s or only_d else ""),
                not only_s and not only_d)
            gen(name + ".dxf", "DXF drawn in world coordinates or about the origin", f"offset ({dx:.2f}, {dy:.2f})",
                (abs(dx) < TOL_POS and abs(dy) < TOL_POS) or (abs(douter["cx"]) < TOL_POS and abs(douter["cy"]) < TOL_POS))
    elif name in dxfs and name not in ("drum-sheet", "drum-splice"):
        gen(name + ".dxf", "DXF exists for a flat part", "part not flat", False)

# frame rails: every M6 hole in a panel or plate must sit on a rail centre line, within the rail's length
rails = {n: m for n, m in parts.items() if n.startswith("rail-") or n.startswith("post-") or n.startswith("tray-rail")
         or n.startswith("console-post") or n.startswith("console-rail")}


def hole_on_rail(cx, cy, cz, axis):
    """A hole with axis along `axis` at (cx, cy, cz): is its centre line on some rail's centre line?"""
    hits = []
    for rn, rm in rails.items():
        c = ((rm["xmin"] + rm["xmax"]) / 2, (rm["ymin"] + rm["ymax"]) / 2, (rm["zmin"] + rm["zmax"]) / 2)
        lo = (rm["xmin"], rm["ymin"], rm["zmin"])
        hi = (rm["xmax"], rm["ymax"], rm["zmax"])
        p = (cx, cy, cz)
        ok = True
        for k in range(3):
            if axis[k] > 0.5:    # along the hole axis the rail just has to be there
                if not (lo[k] - 1e-6 <= p[k] <= hi[k] + 1e-6) and not (abs(p[k] - lo[k]) < 60 or abs(p[k] - hi[k]) < 60):
                    ok = False
                continue
            size = hi[k] - lo[k]
            if size <= 40.5:      # across the rail: on its centre line
                if abs(p[k] - c[k]) > TOL_POS:
                    ok = False
            else:                 # along the rail: within its length
                if not (lo[k] - 1e-6 <= p[k] <= hi[k] + 1e-6):
                    ok = False
        if ok:
            hits.append(rn)
    return hits


PANELS = ("side-panel-left", "side-panel-right", "front-upper-panel", "front-lower-panel", "rear-upper-panel",
          "rear-lower-panel", "top-panel", "base-pan", "bay-ceiling", "front-bulkhead", "rear-bulkhead",
          "console-face", "console-rear", "console-cap", "console-cheek-left", "console-cheek-right")
# M6 holes that are bolted through with a nut instead of into a rail: the idler and spring brackets on the base pan
# (design-rules 7a Drive) and the two fixed hinge leaves on the front upper panel (7a Door). Listed, not inferred.
# The console's four foot bolts through the top panel land on the top rear cross rail and the rear top rail, so the
# rail check covers them.
THROUGH_BOLTED = {"base-pan": [(-128.0, 370.0), (-102.0, 370.0), (55.0, 370.0), (75.0, 370.0)],
                  "front-upper-panel": [(-266.0, 581.5), (-252.0, 581.5)]}
for name in PANELS:
    m = parts[name]
    n = m["normal"]
    axis = tuple(abs(a) for a in n)
    holes = [g for g in m["cylinders"] if abs(g["r"] - 3.25) < 1e-3 and all(abs(abs(a) - b2) < 1e-6 for a, b2 in zip(g["dir"], axis))]
    off, through = [], []
    for g in holes:
        if hole_on_rail(*g["mid"], axis):
            continue
        uv = (g["mid"][0], g["mid"][1]) if axis[2] > 0.5 else (g["mid"][0], g["mid"][2])
        if any(abs(uv[0] - a) < TOL_POS and abs(uv[1] - b2) < TOL_POS for a, b2 in THROUGH_BOLTED.get(name, [])):
            through.append(uv)
        else:
            off.append(tuple(round(x, 1) for x in g["mid"]))
    gen(name, "every M6 hole sits on a frame rail centre line (or is a listed through-bolted hole)",
        f"{len(holes)} M6 holes, {len(through)} through-bolted, {len(off)} off a rail" + (f": {off[:4]}" if off else ""), not off)

# the console (draft 6) is a 4040 frame like the cabinet's, so its plates are in PANELS above and its members in rails;
# its M4 holes are the UCI-D module pattern on the face only
m = parts["console-face"]
m4 = [g for g in m["cylinders"] if abs(g["r"] - 2.25) < 1e-3]
gen("console-face", "the only M4 holes are the four UCI-D module holes (uci-spec 4.1)", f"{len(m4)} M4 holes", len(m4) == 4)

# V-011: every round feature has a named diameter
ALLOWED_D = {4.5: "M4 clearance", 5.0: "louver slot ends (60 x 5)", 6.5: "M6 clearance", 8.5: "M8 clearance (feet studs)", 10.0: "inlet holes", 10.5: "roller shafts",
             40.0: "lint slot ends (260 x 40)",
             22.0: "cord strain relief bushing", 106.0: "exhaust port (102 duct + 2 each side)", 460.0: "door opening",
             470.0: "door ring bore", 480.0: "front panel ring opening", 540.0: "door disc / drum ring bore", 560.0: "door ring",
             616.4: "splice inside", 618.4: "drum ring / sheet inside", 620.0: "drum outside",
             12.0: "plate corner radius 6 / timer shaft holes", 6.0: "corner radius 3 (cheeks, tabs, splice, idler arm ends)", 20.0: "faceplate corner radius 10",
             4.0: "4040 corner radius 2 / timer yoke holes", 3.0: "2020 corner radius 1.5", 6.8: "4040 centre bore (tapped M8 for the feet)", 4.2: "2020 centre bore",
             22.3: "22 mm panel devices", 546.0: "felt seal inside (radius 273)", 582.0: "felt seal outside (radius 291)",
             476.0: "lint slot inner arc (radius 238)", 532.0: "lint slot outer arc (radius 266)"}
bad_d = []
for n, m in parts.items():
    for g in m["cylinders"]:
        if g["length"] < 0.5:   # engraved lettering on the faceplate is 0.3 deep; its curves are not features
            continue
        d = round(2 * g["r"], 3)
        if not any(abs(d - k) < 0.011 for k in ALLOWED_D):
            bad_d.append((n, d))
for n, d in dxfs.items():
    for l in d["loops"]:
        if l["type"] == "circle" and not any(abs(l["w"] - k) < 0.011 for k in ALLOWED_D):
            bad_d.append((n + ".dxf", round(l["w"], 3)))
gen("all parts", "V-011: every round feature deeper than 0.5 mm has a diameter on the named list (" + ", ".join(f"{k:g} {v}" for k, v in sorted(ALLOWED_D.items())) + ")",
    f"{len(bad_d)} off the list" + (f": {bad_d[:5]}" if bad_d else ""), not bad_d)

# V-013: air path areas from the measured features, against the blower outlet (102 round)
try:
    a_outlet = math.pi * 51 ** 2
    # the riser's vertical part, cut level at Z 400 (above the hood, below the ceiling), and its hood over the heat
    # module's outlet, cut at Y 630 (the hood runs from Y 560 to the riser); each section is one rectangle (draft 6)
    def section_area(name, origin, normal, u, v):
        lps, _ = section_loops(part_shapes[name], origin, normal, u, v)
        outer = max(lps, key=lambda l: l["w"] * l["h"])
        assert outer["type"] == "rect", (name, outer)
        inner = [l for l in lps if l is not outer]
        return outer["w"] * outer["h"] - sum(l["w"] * l["h"] for l in inner), outer
    a_riser, riser_sec = section_area("riser-duct", (0, 0, 400), (0, 0, 1), (1, 0, 0), (0, 1, 0))
    a_hood, hood_sec = section_area("riser-duct", (0, 630, 0), (0, 1, 0), (1, 0, 0), (0, 0, 1))
    lint = parts["lint-duct"]
    a_lint = lint["sx"] * lint["sy"]
    slot = [l for l in parts["front-bulkhead"]["loops"] if l["type"] == "sector"][0]
    a_slot = slot["area"]
    inlet = [g for g in parts["rear-bulkhead"]["cylinders"] if abs(2 * g["r"] - 10) < 0.011]
    a_inlet = sum(math.pi * g["r"] ** 2 for g in inlet)
    port = [l for l in parts["rear-lower-panel"]["loops"] if l["type"] == "circle" and abs(l["w"] - 106) < 0.011][0]
    a_exh = a_outlet   # the duct itself, 102 round
    areas = dict(riser=a_riser, riser_hood=a_hood, lint_duct=a_lint, lint_slot=a_slot, inlet_field=a_inlet, exhaust_duct=a_exh)
    gen("air path", "V-013: every opening in the air path is at least the blower outlet (102 round, %.0f mm2)" % a_outlet,
        ", ".join(f"{k} {v:.0f}" for k, v in areas.items()), all(v >= a_outlet - 0.5 for v in areas.values()))
except Exception as ex:
    gen("air path", "V-013 air path areas", f"could not compute: {ex}", False)

# interference on the re-imported assembly (the script checks the live model; this checks the file)
inter = []
names = list(assembly)
for a, b in itertools.combinations(names, 2):
    ba, bb = assembly[a]["bbox"], assembly[b]["bbox"]
    if ba[3] < bb[0] or bb[3] < ba[0] or ba[4] < bb[1] or bb[4] < ba[1] or ba[5] < bb[2] or bb[5] < ba[2]:
        continue
    try:
        com = BRepAlgoAPI_Common(assembly[a]["shape"], assembly[b]["shape"])
        v = volume(com.Shape()) if com.IsDone() else -1
    except Exception as ex:
        v = -1
    if v > 1.0 or v < 0:
        inter.append((a, b, round(v, 2)))
gen("assembly", "no two solids overlap by more than 1 mm3 (file re-import)", f"{len(names)} solids, {len(inter)} overlaps" + (f": {inter[:5]}" if inter else ""), not inter)
expected_names = set(parts)
gen("assembly", "every part file is a named solid in the assembly", f"{len(expected_names - set(assembly))} missing", not (expected_names - set(assembly)))

# ---------------------------------------------------------------------------
# Expected values from the documents
# ---------------------------------------------------------------------------
def find_part(name):
    if name in parts:
        return parts[name]
    if name in assembly:
        a = assembly[name]
        b = a["bbox"]
        return dict(name=name, solids=a["solids"], xmin=b[0], ymin=b[1], zmin=b[2], xmax=b[3], ymax=b[4], zmax=b[5],
                    sx=b[3] - b[0], sy=b[4] - b[1], sz=b[5] - b[2], volume=a["volume"], flat=0, loops=None,
                    cylinders=face_cylinders(a["shape"]), planes=face_planes(a["shape"]))
    return None


def evaluate(row):
    part, check, args = row["part"], row["check"], [a.strip() for a in row["args"].split(";") if a.strip()]
    exp = row["expected"]
    tol = float(row["tol"]) if row["tol"] else TOL_POS
    m = find_part(part) if part not in ("assembly", "cut-list", "clearance", "dxf") else None
    if part not in ("assembly", "cut-list", "clearance", "dxf") and m is None:
        return None, "FAIL (part not found)"
    try:
        if check == "solids":
            val = m["solids"]; ok = val == int(exp)
        elif check == "size":
            val = m["s" + args[0]]; ok = abs(val - float(exp)) <= tol
        elif check in ("min", "max"):
            val = m[args[0] + check]; ok = abs(val - float(exp)) <= tol
        elif check == "thickness":
            val = m["thickness"]; ok = val is not None and abs(val - float(exp)) <= tol
        elif check == "normal":
            n = m["normal"]; e = tuple(float(x) for x in exp.split(","))
            val = tuple(round(x, 4) for x in n) if n else None
            ok = n is not None and (all(abs(a - b2) < 1e-3 for a, b2 in zip(n, e)) or all(abs(a + b2) < 1e-3 for a, b2 in zip(n, e)))
        elif check == "holes":
            d = float(args[0]); axis = args[1] if len(args) > 1 else None
            def axis_ok(g):
                if axis is None:
                    return True
                if axis == "radial":
                    return abs(g["dir"][1]) < 1e-6   # perpendicular to the drum axis (Y)
                vec = {"x": (1, 0, 0), "y": (0, 1, 0), "z": (0, 0, 1)}[axis]
                return abs(abs(sum(a * b2 for a, b2 in zip(g["dir"], vec))) - 1) < 1e-6
            val = sum(1 for g in m["cylinders"] if abs(2 * g["r"] - d) <= tol and axis_ok(g))
            ok = val == int(exp)
        elif check == "hole_at":
            d, u, v = float(args[0]), float(args[1]), float(args[2])
            # plate-local coordinates: look in the section loops first, else in the cylinders
            found = None
            if m.get("loops"):
                for l in m["loops"]:
                    if l["type"] == "circle" and abs(l["w"] - d) <= tol and abs(l["cx"] - u) <= tol and abs(l["cy"] - v) <= tol:
                        found = l
            val = f"({found['cx']:.3f}, {found['cy']:.3f}) d {found['w']:.3f}" if found else "no such hole"
            ok = found is not None and exp == "1"
        elif check == "cyl":
            r = float(args[0]); axis = args[1]
            vec = {"x": (1, 0, 0), "y": (0, 1, 0), "z": (0, 0, 1)}[axis]
            hits = [g for g in m["cylinders"] if abs(g["r"] - r) <= tol and abs(abs(sum(a * b2 for a, b2 in zip(g["dir"], vec))) - 1) < 1e-6]
            if len(args) > 2:   # axis position in the two other coordinates, "a,b" in world order
                pa, pb = (float(x) for x in args[2].split(","))
                k = [i for i in range(3) if vec[i] == 0]
                hits = [g for g in hits if abs(g["mid"][k[0]] - pa) <= tol and abs(g["mid"][k[1]] - pb) <= tol]
            val = len(hits)
            ok = val == int(exp)
        elif check == "cyl_length":
            r = float(args[0]); axis = args[1]
            vec = {"x": (1, 0, 0), "y": (0, 1, 0), "z": (0, 0, 1)}[axis]
            hits = [g for g in m["cylinders"] if abs(g["r"] - r) <= tol and abs(abs(sum(a * b2 for a, b2 in zip(g["dir"], vec))) - 1) < 1e-6]
            val = round(hits[0]["length"], 3) if hits else None
            ok = val is not None and abs(val - float(exp)) <= tol
        elif check == "loop":
            typ = args[0]; cu, cv, w, h = (float(x) for x in args[1:5])
            hits = [l for l in (m["loops"] or []) if l["type"] == typ and abs(l["cx"] - cu) <= tol and abs(l["cy"] - cv) <= tol and abs(l["w"] - w) <= tol and abs(l["h"] - h) <= tol]
            val = len(hits); ok = val == int(exp)
        elif check == "loops":
            typ = args[0]
            val = sum(1 for l in (m["loops"] or []) if l["type"] == typ); ok = val == int(exp)
        elif check == "outline":
            o = m.get("outer"); w, h = float(args[0]), float(args[1])
            val = f"{o['type']} {o['w']:.3f} x {o['h']:.3f}" if o else None
            ok = o is not None and abs(o["w"] - w) <= tol and abs(o["h"] - h) <= tol and exp == "1"
        elif check == "clearance":
            key = (args[0], args[1])
            val = clearances.get(key)
            if val is None and key not in clearances:
                val = min_dist(assembly[args[0]]["shape"], assembly[args[1]]["shape"]) if args[0] in assembly and args[1] in assembly else None
            val = round(val, 3) if val is not None else None
            ok = val is not None and abs(val - float(exp)) <= tol
        elif check == "cut":
            row_ = cut_list.get(args[0])
            val = float(row_["length_mm"]) if row_ else None
            ok = val is not None and abs(val - float(exp)) <= tol
        elif check == "cut_qty":
            row_ = cut_list.get(args[0])
            val = int(row_["qty"]) if row_ else None
            ok = val == int(exp)
        elif check == "assembly_solids":
            val = len(assembly); ok = val == int(exp)
        elif check == "assembly_size":
            k = {"x": (0, 3), "y": (1, 4), "z": (2, 5)}[args[0]]
            lo = min(a["bbox"][k[0]] for a in assembly.values()); hi = max(a["bbox"][k[1]] for a in assembly.values())
            val = round(hi - lo, 3); ok = abs(val - float(exp)) <= tol
        elif check == "assembly_max":
            k = {"x": 3, "y": 4, "z": 5}[args[0]]
            val = round(max(a["bbox"][k] for a in assembly.values()), 3); ok = abs(val - float(exp)) <= tol
        elif check == "assembly_min":
            k = {"x": 0, "y": 1, "z": 2}[args[0]]
            val = round(min(a["bbox"][k] for a in assembly.values()), 3); ok = abs(val - float(exp)) <= tol
        elif check == "dxf_loops":
            d = dxfs.get(args[0]); typ = args[1]
            val = sum(1 for l in d["loops"] if l["type"] == typ) if d else None; ok = val == int(exp)
        elif check == "dxf_circles_d":
            d = dxfs.get(args[0]); dia = float(args[1])
            val = sum(1 for l in d["loops"] if l["type"] == "circle" and abs(l["w"] - dia) <= tol) if d else None; ok = val == int(exp)
        elif check == "dxf_outline":
            d = dxfs.get(args[0]); w, h = float(args[1]), float(args[2])
            o = max(d["loops"], key=lambda l: l["w"] * l["h"]) if d and d["loops"] else None
            val = f"{o['type']} {o['w']:.3f} x {o['h']:.3f}" if o else None
            ok = o is not None and abs(o["w"] - w) <= tol and abs(o["h"] - h) <= tol
        elif check == "dxf_circle_at":
            d = dxfs.get(args[0]); dia, cx, cy = (float(x) for x in args[1:4])
            val = sum(1 for l in d["loops"] if l["type"] == "circle" and abs(l["w"] - dia) <= tol and abs(l["cx"] - cx) <= tol and abs(l["cy"] - cy) <= tol) if d else None
            ok = val == int(exp)
        elif check == "dxf_polygon_vertices":
            d = dxfs.get(args[0])
            polys = [l for l in d["loops"] if l["type"] == "polygon"] if d else []
            val = polys[0]["n"] if polys else None; ok = val == int(exp)
        else:
            return None, f"FAIL (unknown check {check})"
    except Exception as ex:
        return None, f"FAIL (error: {ex})"
    return val, "PASS" if ok else "FAIL"


with open(os.path.join(HERE, "expected-dimensions.csv"), newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        if not row["id"] or row["id"].startswith("#"):
            continue
        val, status = evaluate(row)
        results.append((row["id"], row["part"], f"{row['check']} {row['args']}".strip(), row["expected"], val, status, row["source"]))

# ---------------------------------------------------------------------------
# Drum sheet and splice: unwrap the holes of the curved solids onto the flat pattern and compare with the DXF
# ---------------------------------------------------------------------------
DRUM_HOLE_DS = (4.5, 6.5)     # the drum parts' hole sizes (7b); their 3 mm corner radii are cylinders too, but not holes


def is_hole_d(d):
    return any(abs(d - k) < TOL_POS for k in DRUM_HOLE_DS)


def unwrap_drum(m, r_mid, axis_z, ri, y_front, L, seam_deg=90.0):
    """Holes in the sheet (radial cylinders) and tab holes (cylinders along Y) -> flat (x, y) with x from the seam
    and y from the sheet's front edge. A tab is folded in at the sheet's inner surface (radius ri), so a tab hole's
    flat y is its radial distance inside that surface, before the front edge or beyond the rear edge."""
    out = []
    for g in m["cylinders"]:
        if g["r"] > 100 or not is_hole_d(2 * g["r"]):   # the drum surfaces themselves, and the tabs' corner radii
            continue
        if abs(abs(g["dir"][1]) - 1) < 1e-6:          # tab hole, axis along Y
            x, z = g["mid"][0], g["mid"][2] - axis_z
            theta = math.degrees(math.atan2(z, x))
            arc = math.radians((theta - seam_deg) % 360) * r_mid
            inward = ri - math.hypot(x, z)
            y_flat = y_front - inward if g["mid"][1] < y_front + L / 2 else y_front + L + inward
            out.append(("tab", arc, y_flat, 2 * g["r"]))
        elif abs(g["dir"][1]) < 1e-6:                  # radial hole
            x, z = g["mid"][0], g["mid"][2] - axis_z
            theta = math.degrees(math.atan2(z, x))
            arc = math.radians((theta - seam_deg) % 360) * r_mid
            out.append(("wall", arc, g["mid"][1], 2 * g["r"]))
    return out


DRUM_AXIS_Z = None
if "drum-sheet" in parts:
    m = parts["drum-sheet"]
    big = [g for g in m["cylinders"] if g["r"] > 100]
    if big:
        DRUM_AXIS_Z = big[0]["foot"][2]
        ro = max(g["r"] for g in big); ri = min(g["r"] for g in big)
        r_mid = (ro + ri) / 2
        y_front = m["ymin"] + (ro - ri)       # the sheet's front edge is one sheet thickness behind the tab faces
        L_sheet = (m["ymax"] - (ro - ri)) - y_front
        flat = unwrap_drum(m, r_mid, DRUM_AXIS_Z, ri, y_front, L_sheet)
        W = 2 * math.pi * r_mid
        # DXF circles: tab holes at y = -10 and L+10, wall holes inside
        d = dxfs.get("drum-sheet")
        if d:
            dcirc = [l for l in d["loops"] if l["type"] == "circle"]
            # the STEP's hole x is measured from the seam; x and W - x are the same seam, so compare modulo W
            matched, unmatched = 0, []
            left = list(dcirc)
            flat = [(k, x, y - y_front, d) for k, x, y, d in flat]
            if dcirc and flat:   # align on the mean of each set: the two patterns should be the same pattern
                mx = sum(c["cx"] for c in dcirc) / len(dcirc) - sum(f[1] for f in flat) / len(flat)
                my = sum(c["cy"] for c in dcirc) / len(dcirc) - sum(f[2] for f in flat) / len(flat)
                notes.append(f"drum-sheet.dxf offset from the unwrapped solid: ({mx:.3f}, {my:.3f})")
                flat = [(k, x + mx, y + my, d) for k, x, y, d in flat]
            for kind, x, yy, dia in flat:
                hit = None
                for i, c in enumerate(left):
                    dx = min(abs(c["cx"] - x), abs(c["cx"] - x + W), abs(c["cx"] - x - W))
                    if dx < 0.05 and abs(c["cy"] - yy) < 0.05 and abs(c["w"] - dia) < TOL_POS:
                        hit = i
                        break
                if hit is None:
                    unmatched.append((kind, round(x, 2), round(yy, 2), dia))
                else:
                    matched += 1
                    left.pop(hit)
            gen("drum-sheet.dxf", "every hole in the rolled solid unwraps onto a hole in the flat pattern (0.05 mm)",
                f"{matched} matched, {len(unmatched)} solid-only, {len(left)} DXF-only" + (f"; {unmatched[:3]} {[loop_key(l) for l in left[:3]]}" if unmatched or left else ""),
                not unmatched and not left)
            outline = max(d["loops"], key=lambda l: l["w"] * l["h"])
            gen("drum-sheet.dxf", "flat pattern outline is the sheet's unrolled mid-surface length by its length plus the tabs",
                f"{outline['type']} {outline['w']:.3f} x {outline['h']:.3f}, {outline['n']} edges; unrolled {W:.3f}",
                abs(outline["w"] - W) < TOL_POS)
            m["unrolled_w"] = W
if "drum-splice" in parts and "drum-splice" in dxfs:
    m = parts["drum-splice"]
    big = [g for g in m["cylinders"] if g["r"] > 100]
    ro = max(g["r"] for g in big)
    # the splice edge angle: from its bounding box in X at the outer radius
    half_chord = m["sx"] / 2
    edge_deg = 90 - math.degrees(math.asin(half_chord / ro))
    d = dxfs["drum-splice"]
    dcirc = [l for l in d["loops"] if l["type"] == "circle"]
    holes = [g for g in m["cylinders"] if g["r"] < 100 and is_hole_d(2 * g["r"])]
    matched, unmatched = 0, []
    left = list(dcirc)
    flat = []
    for g in holes:
        x, z = g["mid"][0], g["mid"][2] - DRUM_AXIS_Z
        theta = math.degrees(math.atan2(z, x))
        flat.append((math.radians(theta - edge_deg) * ro, g["mid"][1] - m["ymin"], 2 * g["r"]))
    if dcirc and flat:
        mx = sum(c["cx"] for c in dcirc) / len(dcirc) - sum(f[0] for f in flat) / len(flat)
        my = sum(c["cy"] for c in dcirc) / len(dcirc) - sum(f[1] for f in flat) / len(flat)
        notes.append(f"drum-splice.dxf offset from the unwrapped solid: ({mx:.3f}, {my:.3f})")
        flat = [(x + mx, y + my, d) for x, y, d in flat]
    for arc, yy, dia in flat:
        hit = None
        for i, c in enumerate(left):
            if abs(c["cx"] - arc) < 0.05 and abs(c["cy"] - yy) < 0.05 and abs(c["w"] - dia) < TOL_POS:
                hit = i
                break
        if hit is None:
            unmatched.append((round(arc, 2), round(yy, 2)))
        else:
            matched += 1
            left.pop(hit)
    gen("drum-splice.dxf", "every hole in the curved splice unwraps onto a hole in the flat strip (0.05 mm)",
        f"{matched} matched, {len(unmatched)} solid-only, {len(left)} DXF-only", not unmatched and not left)
    outline = max(d["loops"], key=lambda l: l["w"] * l["h"])
    gen("drum-splice.dxf", "flat strip outline equals the curved strip's arc length by its length",
        f"{outline['w']:.3f} x {outline['h']:.3f}; arc {2 * math.radians(90 - edge_deg) * ro:.3f} x {m['sy']:.3f}",
        abs(outline["w"] - 2 * math.radians(90 - edge_deg) * ro) < 0.05 and abs(outline["h"] - m["sy"]) < TOL_POS)

# ---------------------------------------------------------------------------
# Fusion comparison
# ---------------------------------------------------------------------------
fusion_rows = []
if FUSION_CSV:
    with open(FUSION_CSV, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    bodies = [r for r in rows if r["record"] == "body"]
    fcyl = [r for r in rows if r["record"] == "cylinder"]
    fdist = [r for r in rows if r["record"] == "distance"]
    # a hardware set is one named compound of many solids here and many bodies under one component in Fusion:
    # add the bodies of an assembly component up before comparing (volumes add, boxes merge)
    merged, order = {}, []
    for r in bodies:
        key = (r["file"], r["body"])
        if r["file"] == "osa-dryer-assembly":
            if key not in merged:
                merged[key] = dict(r)
                merged[key]["n_bodies"] = 1
                order.append(key)
            else:
                m_ = merged[key]
                m_["volume_mm3"] = str(float(m_["volume_mm3"]) + float(r["volume_mm3"]))
                for k in ("xmin", "ymin", "zmin"):
                    m_[k] = str(min(float(m_[k]), float(r[k])))
                for k in ("xmax", "ymax", "zmax"):
                    m_[k] = str(max(float(m_[k]), float(r[k])))
                m_["is_solid"] = m_["is_solid"] if r["is_solid"] in ("1", "True", "true") else r["is_solid"]
                m_["n_bodies"] += 1
        else:
            merged[key] = dict(r)
            order.append(key)
    bodies = [merged[k] for k in order]
    seen = set()
    for r in bodies:
        src, nm = r["file"], r["body"]
        key = (src, nm)
        if src == "osa-dryer-assembly":
            ref = assembly.get(nm)
            if ref is None:
                fusion_rows.append((src, nm, "named body present in the OCP read", "missing", "FAIL"))
                continue
            vol = ref["volume"]; bb = ref["bbox"]
            nf = None
        else:
            ref = parts.get(src)
            if ref is None:
                fusion_rows.append((src, nm, "part file known to the audit", "missing", "FAIL"))
                continue
            vol = ref["volume"]; bb = (ref["xmin"], ref["ymin"], ref["zmin"], ref["xmax"], ref["ymax"], ref["zmax"])
            nf = ref["faces"]
        fv = float(r["volume_mm3"])
        nb = r.get("n_bodies", 1)
        fusion_rows.append((src, nm, "volume (mm3)" + (f" ({nb} bodies added)" if nb > 1 else ""), f"OCP {vol:.3f} / Fusion {fv:.3f}", "PASS" if abs(fv - vol) <= 1e-4 * max(vol, 1) + 0.05 else "FAIL"))
        fb = tuple(float(r[k]) for k in ("xmin", "ymin", "zmin", "xmax", "ymax", "zmax"))
        dev = max(abs(a - b2) for a, b2 in zip(fb, bb))
        fusion_rows.append((src, nm, "bounding box (mm)", f"max deviation {dev:.4f}", "PASS" if dev <= 0.02 else "FAIL"))
        if nf is not None:
            ff = int(r["faces"])
            fusion_rows.append((src, nm, "face count", f"OCP {nf} / Fusion {ff}", "PASS" if ff == nf else "CHECK"))
        fusion_rows.append((src, nm, "solid body", r["is_solid"], "PASS" if r["is_solid"] in ("1", "True", "true") else "FAIL"))
        seen.add(key)
    # cylinders: every OCP cylinder group in a part file must appear in Fusion with the same diameter and axis point
    by_file = {}
    for r in fcyl:
        by_file.setdefault(r["file"], []).append(r)
    for src, ref in parts.items():
        fl = by_file.get(src, [])
        if not fl and not ref["cylinders"]:
            continue
        left = list(fl)
        missing = []
        for g in ref["cylinders"]:
            hit = None
            for i, r in enumerate(left):
                if abs(float(r["radius"]) - g["r"]) < 1e-3 and all(abs(abs(float(r[k])) - abs(a)) < 1e-4 for k, a in zip(("ax", "ay", "az"), g["dir"])):
                    foot = tuple(float(r[k]) for k in ("fx", "fy", "fz"))
                    if all(abs(a - b2) < 0.02 for a, b2 in zip(foot, g["foot"])):
                        hit = i
                        break
            if hit is None:
                missing.append((round(2 * g["r"], 3), tuple(round(x, 2) for x in g["foot"])))
            else:
                left.pop(hit)
        fusion_rows.append((src, "", "every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis",
                            f"{len(ref['cylinders']) - len(missing)} matched, {len(missing)} missing in Fusion, {len(left)} extra in Fusion" + (f"; missing {missing[:3]}" if missing else ""),
                            "PASS" if not missing and not left else "FAIL"))
    for r in fdist:
        key = (r["body"], r["other"])
        ref = clearances.get(key)
        if ref is None and r["body"] in assembly and r["other"] in assembly:
            ref = min_dist(assembly[r["body"]]["shape"], assembly[r["other"]]["shape"])
        if ref is None:
            fusion_rows.append(("osa-dryer-assembly", f"{key[0]} / {key[1]}", "clearance", f"Fusion {float(r['value_mm']):.3f}, OCP pair not measured", "CHECK"))
        else:
            fv = float(r["value_mm"])
            fusion_rows.append(("osa-dryer-assembly", f"{key[0]} / {key[1]}", "minimum distance (mm)", f"OCP {ref:.3f} / Fusion {fv:.3f}", "PASS" if abs(fv - ref) <= 0.02 else "FAIL"))
    missing_in_fusion = [n for n in parts if (n, n) not in seen and not any(k[0] == n for k in seen)]
    if missing_in_fusion:
        fusion_rows.append(("", "", "part files measured in Fusion", f"{len(missing_in_fusion)} not in the Fusion CSV: {missing_in_fusion[:5]}", "FAIL"))

# ---------------------------------------------------------------------------
# Write the records
# ---------------------------------------------------------------------------
with open(os.path.join(AUD, "measured-parts.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["part", "solids", "valid", "closed", "xmin", "ymin", "zmin", "xmax", "ymax", "zmax", "size_x", "size_y", "size_z",
                "volume_mm3", "area_mm2", "faces", "planar_faces", "cylindrical_faces", "other_faces", "edges", "vertices", "flat", "thickness", "normal", "section_loops"])
    for n, m in parts.items():
        w.writerow([n, m["solids"], m["valid"], m["closed"]] + [r3(m[k]) for k in ("xmin", "ymin", "zmin", "xmax", "ymax", "zmax", "sx", "sy", "sz")]
                   + [r3(m["volume"]), r3(m["area"]), m["faces"], m["n_planes"], m["n_cyl_faces"], m["n_other_faces"], m["edges"], m["vertices"], m["flat"],
                      r3(m["thickness"]) if m["thickness"] is not None else "", " ".join(f"{x:.4f}" for x in m["normal"]) if m["normal"] else "",
                      len(m["loops"]) if m["loops"] is not None else ""])
    for n, a in assembly.items():
        if n not in parts:
            b = a["bbox"]
            w.writerow([f"[assembly] {n}", a["solids"], "", ""] + [r3(x) for x in b] + [r3(b[3] - b[0]), r3(b[4] - b[1]), r3(b[5] - b[2]), r3(a["volume"])] + [""] * 11)

with open(os.path.join(AUD, "measured-cylinders.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["part", "diameter", "radius", "axis_x", "axis_y", "axis_z", "foot_x", "foot_y", "foot_z", "mid_x", "mid_y", "mid_z", "length", "faces", "area_mm2"])
    for n, m in parts.items():
        for g in sorted(m["cylinders"], key=lambda g: (g["r"], g["mid"])):
            w.writerow([n, r3(2 * g["r"]), r3(g["r"])] + [round(x, 6) for x in g["dir"]] + [r3(x) for x in g["foot"]] + [r3(x) for x in g["mid"]] + [r3(g["length"]), g["faces"], r3(g["area"])])

with open(os.path.join(AUD, "measured-planes.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["part", "normal_x", "normal_y", "normal_z", "area_mm2", "centroid_x", "centroid_y", "centroid_z"])
    for n, m in parts.items():
        for nn, ar, c in sorted(m["planes"], key=lambda p: -p[1]):
            w.writerow([n] + [round(x, 6) for x in nn] + [r3(ar)] + [r3(x) for x in c])

with open(os.path.join(AUD, "measured-loops.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["source", "part", "loop_type", "centre_u", "centre_v", "width", "height", "edges", "vertices"])
    for n, m in parts.items():
        if m["loops"] is None:
            continue
        for l in sorted(m["loops"], key=lambda l: (-l["w"] * l["h"], l["cx"], l["cy"])):
            w.writerow(["step-section", n, l["type"], r3(l["cx"]), r3(l["cy"]), r3(l["w"]), r3(l["h"]), l["n"], l.get("verts", "")])
    for n, d in dxfs.items():
        for l in sorted(d["loops"], key=lambda l: (-l["w"] * l["h"], l["cx"], l["cy"])):
            w.writerow(["dxf", n, l["type"], r3(l["cx"]), r3(l["cy"]), r3(l["w"]), r3(l["h"]), l["n"], l.get("verts", "")])

with open(os.path.join(AUD, "measured-clearances.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["part_a", "part_b", "minimum_distance_mm"])
    for (a, b), v in clearances.items():
        w.writerow([a, b, r3(v) if v is not None else ""])

# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------
n_fail = sum(1 for r in results if r[5].startswith("FAIL")) + sum(1 for g in generic if g[3] == "FAIL") + sum(1 for r in fusion_rows if r[4] == "FAIL")
lines = []
lines.append("# CAD audit report")
lines.append("")
lines.append("Produced by `mechanical/cad/cad_audit.py` from the STEP and DXF files on disk. Every number below was measured from the files, not read from the script.")
lines.append("")
lines.append(f"Parts measured: {len(parts)} STEP files, {len(assembly)} named solids in the assembly, {len(dxfs)} DXF drawings.")
lines.append(f"Document checks: {len(results)}, generic checks: {len(generic)}, Fusion comparisons: {len(fusion_rows)}. **Failures: {n_fail}.**")
lines.append("")
lines.append("## 1. Values stated in the documents, against the files")
lines.append("")
lines.append("| id | part | check | expected | measured | result | source |")
lines.append("|---|---|---|---|---|---|---|")
for r in results:
    lines.append("| " + " | ".join(str(x) if x is not None else "" for x in r) + " |")
lines.append("")
lines.append("## 2. Generic checks on every part")
lines.append("")
lines.append("| part | check | measured | result |")
lines.append("|---|---|---|---|")
for g in generic:
    lines.append("| " + " | ".join(str(x) for x in g) + " |")
lines.append("")
if FUSION_CSV:
    lines.append("## 3. The same files measured inside Autodesk Fusion")
    lines.append("")
    lines.append(f"Fusion record: `{os.path.basename(FUSION_CSV)}`, written by `fusion_audit.py` running inside Fusion. CHECK means the two kernels count faces differently (Fusion may split or merge periodic faces); it is not a geometry difference.")
    lines.append("")
    lines.append("| file | body | comparison | values | result |")
    lines.append("|---|---|---|---|---|")
    for r in fusion_rows:
        lines.append("| " + " | ".join(str(x) for x in r) + " |")
    lines.append("")
lines.append("## 4. Clearances measured in the assembly (mm)")
lines.append("")
lines.append("| part a | part b | minimum distance |")
lines.append("|---|---|---|")
for (a, b), v in clearances.items():
    lines.append(f"| {a} | {b} | {v:.3f} |" if v is not None else f"| {a} | {b} | not measured |")
lines.append("")
lines.append("## 5. Inventory")
lines.append("")
lines.append("Every part: bounding box, volume, faces. The full feature lists are in `measured-cylinders.csv` (every hole and round surface), `measured-planes.csv` (every flat face) and `measured-loops.csv` (every closed loop of every flat part's section and of every DXF).")
lines.append("")
lines.append("| part | solids | X min..max | Y min..max | Z min..max | size | volume mm3 | faces (planar / cylindrical / other) | thickness | section loops |")
lines.append("|---|---|---|---|---|---|---|---|---|---|")
for n, m in parts.items():
    lines.append(f"| {n} | {m['solids']} | {m['xmin']:.2f}..{m['xmax']:.2f} | {m['ymin']:.2f}..{m['ymax']:.2f} | {m['zmin']:.2f}..{m['zmax']:.2f} | {m['sx']:.2f} x {m['sy']:.2f} x {m['sz']:.2f} | {m['volume']:.1f} | {m['faces']} ({m['n_planes']} / {m['n_cyl_faces']} / {m['n_other_faces']}) | {m['thickness']:.3f} |" if m["thickness"] is not None else
                 f"| {n} | {m['solids']} | {m['xmin']:.2f}..{m['xmax']:.2f} | {m['ymin']:.2f}..{m['ymax']:.2f} | {m['zmin']:.2f}..{m['zmax']:.2f} | {m['sx']:.2f} x {m['sy']:.2f} x {m['sz']:.2f} | {m['volume']:.1f} | {m['faces']} ({m['n_planes']} / {m['n_cyl_faces']} / {m['n_other_faces']}) | |")
    lines[-1] += f" {len(m['loops'])} |" if m["loops"] is not None else " |"
lines.append("")
lines.append("Bought parts and envelopes in the assembly (no part file):")
lines.append("")
lines.append("| solid | X min..max | Y min..max | Z min..max | volume mm3 |")
lines.append("|---|---|---|---|---|")
for n, a in assembly.items():
    if n not in parts:
        b = a["bbox"]
        lines.append(f"| {n} | {b[0]:.2f}..{b[3]:.2f} | {b[1]:.2f}..{b[4]:.2f} | {b[2]:.2f}..{b[5]:.2f} | {a['volume']:.1f} |")
lines.append("")
lines.append("DXF drawings:")
lines.append("")
lines.append("| drawing | entities | closed loops | open chains | loops by type |")
lines.append("|---|---|---|---|---|")
for n, d in dxfs.items():
    by = {}
    for l in d["loops"]:
        by[l["type"]] = by.get(l["type"], 0) + 1
    lines.append(f"| {n} | {', '.join(f'{k} {v}' for k, v in sorted(d['kinds'].items()))} | {len(d['loops'])} | {d['open']} | {', '.join(f'{k} {v}' for k, v in sorted(by.items()))} |")
lines.append("")
if notes:
    lines.append("## Notes")
    lines.append("")
    for n in notes:
        lines.append(f"- {n}")
    lines.append("")
open(os.path.join(AUD, "audit-report.md"), "w", encoding="utf-8").write("\n".join(lines))
print(f"document checks {len(results)}, generic checks {len(generic)}, fusion comparisons {len(fusion_rows)}, FAILURES {n_fail}")
for r in results:
    if r[5].startswith("FAIL"):
        print("  FAIL", r)
for g in generic:
    if g[3] == "FAIL":
        print("  FAIL", g)
for r in fusion_rows:
    if r[4] == "FAIL":
        print("  FAIL", r)
sys.exit(1 if n_fail else 0)
