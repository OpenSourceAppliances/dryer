"""osa-dryer: the parametric Fusion build (see README.md beside this file).

Run inside Autodesk Fusion. From the Text Commands box (py mode):
    REPO=r"C:\\path\\to\\osa-dryer"; exec(open(REPO + r"\\mechanical\\cad\\fusion_build\\fusion_build.py").read()); print(build_all())
or one stage at a time: new_design(); stage_a(); ...

Draws every part of the dryer natively in a new design: user parameters, sketches with dimensions, extrudes, revolves,
cuts and patterns, one component per part, named as in the STEP the script writes, so fusion_audit.py can compare the
two. Every part is drawn about its own origin and placed by a Move feature whose X, Y and Z distances are expressions
in the user parameters, so the timeline stays readable (one sketch, one extrude, one move for a bar) and a parameter
change moves the part. Numbers come from the P table in osa_dryer_cad.py.

Draft 1, 2026-11-07: stages A (parameters, frame, tray rails), B (the flat plates from plates.json), C (the drum set),
D (the ducts, blower plate feet and exhaust set), E (the door, the Tier 0 module, the drive, the two modules, sensors,
blanks, clamps, feet and brackets, from numbers.json), F (the hardware from hardware.json, as fixed bodies) and G (the
joints, rigid groups and appearances of ../fusion_motion/fusion_motion.py, its interference check at three poses, the
archive mechanical/fusion/osa-dryer-parametric.f3d). All 213 parts built and checked against the script's files
(README.md, ../audit/fusion-build-report.md).
"""
import math
import os
import re
import traceback

import adsk.core
import adsk.fusion

try:
    REPO = globals().get("REPO") or os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
except NameError:
    raise RuntimeError("set REPO to the repo folder before exec()")

CM = 0.1   # mm -> cm (the API's length unit)

# ---------------------------------------------------------------------------
# The numbers: the P table from the script, with the same derived values
# ---------------------------------------------------------------------------
def load_params():
    src = open(os.path.join(REPO, "mechanical", "cad", "osa_dryer_cad.py"), encoding="utf-8").read()
    i = src.index("P = dict(")
    j = src.index("# Helpers", i)
    j = src.rfind("# ----", 0, j)
    block = src[i:j]
    ns = {"math": math}
    exec(block, ns)
    return ns["P"]


P = load_params()
e, hw, D = P["ext"], P["half_w"], P["D"]
Hb, bt, ry, es = P["H_body"], P["bay_top"], P["rear_cross_y"], P["ext_small"]

import json

# the plates and the parameter lists the script wrote (mechanical/cad/plates.json): the user parameters a builder changes,
# the derived parameters with their formulas, and every flat plate with the expressions its numbers carry
PLATES = json.load(open(os.path.join(REPO, "mechanical", "cad", "plates.json"), encoding="utf-8"))
PARAM_COMMENTS = {"cab_w": "cabinet width over the posts", "cab_d": "cabinet depth over the posts", "ext": "4040 extrusion",
                  "ext_small": "2020 tray rails", "bay_top": "top face of the mid rails (the bay ceiling)", "t_panel": "outer panels and plates",
                  "t_bulk": "bulkheads", "t_base": "base pan", "drum_d": "drum outside diameter", "drum_l": "drum length",
                  "drum_front_y": "the drum's front face", "door_d": "door opening in the front bulkhead", "panel_pitch": "panel bolt pitch",
                  "console_h": "console box height", "uci_w": "UCI-D aperture width", "uci_h": "UCI-D aperture height",
                  "drum_clear_bottom": "drum to the bay ceiling", "drum_clear_top": "drum to the top rails"}

_app = None
_design = None
_root = None


def app_design():
    global _app, _design, _root
    _app = adsk.core.Application.get()
    _design = adsk.fusion.Design.cast(_app.activeProduct)
    _root = _design.rootComponent
    return _app, _design, _root


def new_design():
    """A new, empty parametric design in mm with the user parameters."""
    app = adsk.core.Application.get()
    app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
    app, design, root = app_design()
    design.designType = adsk.fusion.DesignTypes.ParametricDesignType
    design.fusionUnitsManager.distanceDisplayUnits = adsk.fusion.DistanceUnits.MillimeterDistanceUnits
    for key, name, val in PLATES["user_params"]:
        uparam(name, f"{val:g} mm", PARAM_COMMENTS.get(name, key))
    for name, formula, val in PLATES["derived_params"]:
        uparam(name, formula, f"derived: {val:g} as drawn")
    return "new design with %d user and %d derived parameters" % (len(PLATES["user_params"]), len(PLATES["derived_params"]))


def uparam(name, expr, comment=""):
    ups = _design.userParameters
    p = ups.itemByName(name)
    if p is not None:
        p.expression = expr
        return p
    return ups.add(name, adsk.core.ValueInput.createByString(expr), "mm", comment)


def V(expr):
    """A ValueInput from an expression string (mm or parameters) or a number in mm."""
    if isinstance(expr, str):
        return adsk.core.ValueInput.createByString(expr)
    return adsk.core.ValueInput.createByReal(expr * CM)


def E(x):
    """A number in mm as an expression string."""
    return f"{x} mm"


def pt(x, y, z=0.0):
    return adsk.core.Point3D.create(x * CM, y * CM, z * CM)


# ---------------------------------------------------------------------------
# Components, planes, sketches, features
# ---------------------------------------------------------------------------
def new_comp(name):
    occ = _root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    occ.component.name = name
    return occ.component


def base_plane(comp, axis):
    """The component's origin plane normal to the model axis: 'z' is XY, 'y' is XZ, 'x' is YZ."""
    return {"z": comp.xYConstructionPlane, "y": comp.xZConstructionPlane, "x": comp.yZConstructionPlane}[axis]


def plane_normal_sign(comp, axis):
    """+1 if the base plane's normal points along +axis, else -1 (Fusion's XZ plane faces -Y)."""
    n = base_plane(comp, axis).geometry.normal
    v = {"x": n.x, "y": n.y, "z": n.z}[axis]
    return 1.0 if v > 0 else -1.0


def sketch_on(comp, axis):
    """A sketch on the component's origin plane normal to the axis."""
    return comp.sketches.add(base_plane(comp, axis))


def sk_pt(sk, x, y, z):
    """A model point in the sketch's own coordinates."""
    return sk.modelToSketchSpace(pt(x, y, z))


def circle(sk, cx, cy, cz, d):
    return sk.sketchCurves.sketchCircles.addByCenterRadius(sk_pt(sk, cx, cy, cz), d / 2 * CM)


def biggest_profile(sk):
    best, area = None, -1
    for i in range(sk.profiles.count):
        p = sk.profiles.item(i)
        a = p.areaProperties().area
        if a > area:
            best, area = p, a
    return best


def _strokes(curve3d, tol_cm=0.005):
    ev = curve3d.evaluator
    ok, p0, p1 = ev.getParameterExtents()
    ok, pts = ev.getStrokes(p0, p1, tol_cm)
    return [(p.x, p.y) for p in pts]


def _loop_poly(loop):
    """The loop's curves sampled into one closed polygon in sketch coordinates, each curve turned to continue the chain."""
    runs = [_strokes(loop.profileCurves.item(i).geometry) for i in range(loop.profileCurves.count)]
    runs = [r for r in runs if r]
    if not runs:
        return []
    poly = list(runs[0])
    for i, s in enumerate(runs[1:]):
        d0 = (s[0][0] - poly[-1][0]) ** 2 + (s[0][1] - poly[-1][1]) ** 2
        d1 = (s[-1][0] - poly[-1][0]) ** 2 + (s[-1][1] - poly[-1][1]) ** 2
        if i == 0 and min(d0, d1) > 1e-6:     # the first curve was sampled against the loop's direction
            poly.reverse()
            d0 = (s[0][0] - poly[-1][0]) ** 2 + (s[0][1] - poly[-1][1]) ** 2
            d1 = (s[-1][0] - poly[-1][0]) ** 2 + (s[-1][1] - poly[-1][1]) ** 2
        poly.extend(s[::-1] if d1 < d0 else s)
    return poly


def _inside(poly, x, y):
    inside = False
    n = len(poly)
    for i in range(n):
        x0, y0 = poly[i]
        x1, y1 = poly[(i + 1) % n]
        if (y0 > y) != (y1 > y):
            xi = x0 + (y - y0) * (x1 - x0) / (y1 - y0)
            if xi > x:
                inside = not inside
    return inside


def profile_containing(sk, point3d):
    """The profile that holds the sketch-space point: inside its outer loop and outside every inner loop, by a sampled
    point-in-polygon test on the loops' curves (a bounding box test cannot tell a band from the region inside it)."""
    x, y = point3d.x, point3d.y
    for i in range(sk.profiles.count):
        p = sk.profiles.item(i)
        outer_ok, inner_hit = False, False
        for j in range(p.profileLoops.count):
            loop = p.profileLoops.item(j)
            ins = _inside(_loop_poly(loop), x, y)
            if loop.isOuter:
                outer_ok = ins
            elif ins:
                inner_hit = True
        if outer_ok and not inner_hit:
            return p
    return None


def profile_at(sk, point3d):
    """The profile holding the sketch point (a plate's region, where a cut circle that reaches outside the outline makes
    a bigger region of its own; a tube's wall, not its bore); falls back to the largest profile whose box holds it."""
    try:
        p = profile_containing(sk, point3d)
        if p is not None:
            return p
    except Exception:
        pass
    best, area = None, -1
    for i in range(sk.profiles.count):
        p = sk.profiles.item(i)
        bb = p.boundingBox
        if not bb.contains(point3d):
            continue
        a = p.areaProperties().area
        if a > area:
            best, area = p, a
    return best if best is not None else biggest_profile(sk)


def all_profiles(sk):
    coll = adsk.core.ObjectCollection.create()
    for i in range(sk.profiles.count):
        coll.add(sk.profiles.item(i))
    return coll


OPS = {"new": adsk.fusion.FeatureOperations.NewBodyFeatureOperation,
       "join": adsk.fusion.FeatureOperations.JoinFeatureOperation,
       "cut": adsk.fusion.FeatureOperations.CutFeatureOperation}


def extrude(comp, profiles, dist, op="new", along=1.0, bodies=None):
    """Extrude profiles by dist (mm or expression) along the sketch plane's normal; along=-1 goes the other way."""
    exts = comp.features.extrudeFeatures
    inp = exts.createInput(profiles, OPS[op])
    if isinstance(dist, str):
        d = dist if along > 0 else f"-({dist})"
    else:
        d = dist * along
    inp.setDistanceExtent(False, V(d))
    if bodies:
        inp.participantBodies = list(bodies)
    return exts.add(inp)


def move(comp, bodies, dx, dy, dz):
    """Translate bodies by expressions (mm or parameters) in the model's axes: the parametric placement of a part."""
    mf = comp.features.moveFeatures
    coll = adsk.core.ObjectCollection.create()
    for b in bodies:
        coll.add(b)
    inp = mf.createInput2(coll)
    inp.defineAsTranslateXYZ(V(dx), V(dy), V(dz), True)
    return mf.add(inp)


def comp_bodies(comp):
    return [comp.bRepBodies.item(i) for i in range(comp.bRepBodies.count)]


def rotate(comp, bodies, axis_entity, angle_expr):
    """Turn bodies about a construction axis by an expression in degrees (a Move feature)."""
    mf = comp.features.moveFeatures
    coll = adsk.core.ObjectCollection.create()
    for b in bodies:
        coll.add(b)
    inp = mf.createInput2(coll)
    inp.defineAsRotate(axis_entity, V(angle_expr) if isinstance(angle_expr, str) else adsk.core.ValueInput.createByString(f"{angle_expr} deg"))
    return mf.add(inp)


def offset_plane(comp, axis, expr):
    """A construction plane parallel to the base plane normal to the axis, at the model coordinate expr (mm or expression)."""
    s = plane_normal_sign(comp, axis)
    if isinstance(expr, str):
        e_ = expr if s > 0 else f"-({expr})"
    else:
        e_ = expr * s
    planes = comp.constructionPlanes
    inp = planes.createInput()
    inp.setByOffset(base_plane(comp, axis), V(e_))
    pl = planes.add(inp)
    pl.isLightBulbOn = False
    return pl


def angled_plane(comp, axis_entity, angle_expr, base):
    """A construction plane turned about a construction axis from a base plane, by an expression in degrees."""
    planes = comp.constructionPlanes
    inp = planes.createInput()
    inp.setByAngle(axis_entity, V(angle_expr) if isinstance(angle_expr, str) else adsk.core.ValueInput.createByString(f"{angle_expr} deg"), base)
    pl = planes.add(inp)
    pl.isLightBulbOn = False
    return pl


def circ_pattern(comp, features, axis_entity, n, total_angle="360 deg"):
    """A circular pattern of features about a construction axis: n instances over the total angle."""
    cp = comp.features.circularPatternFeatures
    coll = adsk.core.ObjectCollection.create()
    for f_ in features:
        coll.add(f_)
    inp = cp.createInput(coll, axis_entity)
    inp.quantity = V_count(n)
    inp.totalAngle = V(total_angle)
    inp.isSymmetric = False
    try:
        inp.patternComputeOption = adsk.fusion.PatternComputeOptions.AdjustPatternCompute
    except Exception:
        pass
    return cp.add(inp)


def fillet_parallel_edges(comp, body, direction, radius, where=None):
    """Fillet every straight edge of the body parallel to the model direction ('x', 'y' or 'z'), optionally only those
    whose midpoint passes where(x, y, z) in mm."""
    idx = {"x": 0, "y": 1, "z": 2}[direction]
    coll = adsk.core.ObjectCollection.create()
    for i in range(body.edges.count):
        ed = body.edges.item(i)
        g = ed.geometry
        if g.curveType != adsk.core.Curve3DTypes.Line3DCurveType:
            continue
        v = g.startPoint.vectorTo(g.endPoint)
        v.normalize()
        comps_ = (abs(v.x), abs(v.y), abs(v.z))
        if comps_[idx] < 0.999:
            continue
        if where is not None:
            m = g.startPoint.copy()
            m.translateBy(adsk.core.Vector3D.create((g.endPoint.x - g.startPoint.x) / 2, (g.endPoint.y - g.startPoint.y) / 2, (g.endPoint.z - g.startPoint.z) / 2))
            if not where(m.x / CM, m.y / CM, m.z / CM):
                continue
        coll.add(ed)
    if coll.count == 0:
        return None
    ff = comp.features.filletFeatures
    inp = ff.createInput()
    inp.edgeSetInputs.addConstantRadiusEdgeSet(coll, V(radius), True)
    return ff.add(inp)


def polygon(sk, model_pts):
    """A closed chain of lines through model points (x, y, z)."""
    lines = sk.sketchCurves.sketchLines
    sps = [sk_pt(sk, *p) for p in model_pts]
    out = []
    first = lines.addByTwoPoints(sps[0], sps[1])
    out.append(first)
    prev = first
    for i in range(2, len(sps)):
        ln = lines.addByTwoPoints(prev.endSketchPoint, sps[i])
        out.append(ln)
        prev = ln
    out.append(lines.addByTwoPoints(prev.endSketchPoint, first.startSketchPoint))
    return out


def rot_xz(x, z, theta_deg):
    """Turn a point in the XZ plane about the origin by theta (0 along +X, 90 along +Z)."""
    a = math.radians(theta_deg)
    return (x * math.cos(a) - z * math.sin(a), x * math.sin(a) + z * math.cos(a))


# ---------------------------------------------------------------------------
# Standard shapes
# ---------------------------------------------------------------------------
def tslot_profile(spec):
    """The T-slot outline as segments ('L', p0, p1) and ('A', p0, mid, p1) in the profile plane (u, v) mm, counterclockwise,
    the same section osa_dryer_cad.tslot_bar() cuts: a square with four grooves and corner fillets, about the origin."""
    h = spec["size"] / 2
    r = spec["corner_r"]
    x_lip, x_far = h - spec["lip"] + 0.01, h - spec["lip"] - spec["band"]
    w2, c, s2 = spec["under_w"] / 2, spec["cham"], spec["slot"] / 2
    x_int = x_far + c - w2 + s2          # where the band's chamfer meets the slot's wall
    x_bot = h - spec["depth"]
    side = [(h, -s2), (x_lip, -s2), (x_lip, -w2), (x_far + c, -w2), (x_int, -s2), (x_bot, -s2),
            (x_bot, s2), (x_int, s2), (x_far + c, w2), (x_lip, w2), (x_lip, s2), (h, s2)]

    def rot(p, k):
        a = math.radians(90 * k)
        return (p[0] * math.cos(a) - p[1] * math.sin(a), p[0] * math.sin(a) + p[1] * math.cos(a))

    segs = []
    for k in range(4):
        pts = [rot((h, -h + r), k)] + [rot(p, k) for p in side] + [rot((h, h - r), k)]
        for i in range(len(pts) - 1):
            segs.append(("L", pts[i], pts[i + 1]))
        cen = rot((h - r, h - r), k)
        p0, p1 = rot((h, h - r), k), rot((h - r, h), k)
        mid = (cen[0] + r * math.cos(math.radians(45 + 90 * k)), cen[1] + r * math.sin(math.radians(45 + 90 * k)))
        segs.append(("A", p0, mid, p1))
    return segs


def draw_segments(sk, segs, to_model):
    """Draw (u, v) segments; to_model maps (u, v) to a model point (x, y, z)."""
    lines, arcs = sk.sketchCurves.sketchLines, sk.sketchCurves.sketchArcs
    for seg in segs:
        if seg[0] == "L":
            lines.addByTwoPoints(sk_pt(sk, *to_model(*seg[1])), sk_pt(sk, *to_model(*seg[2])))
        else:
            arcs.addByThreePoints(sk_pt(sk, *to_model(*seg[1])), sk_pt(sk, *to_model(*seg[2])), sk_pt(sk, *to_model(*seg[3])))


def bar(name, axis, length_expr, dx, dy, dz, size=40.0):
    """A T-slot bar of the given size: profile about the origin on the plane normal to the axis, extruded along +axis by
    length_expr, then moved so its start sits at (dx, dy, dz) (expressions); its section is centred on that point."""
    spec = P["tslot_4040"] if abs(size - 40) < 1e-6 else P["tslot_2020"]
    comp = new_comp(name)
    sk = sketch_on(comp, axis)
    to_model = {"x": lambda u, v: (0.0, u, v), "y": lambda u, v: (u, 0.0, v), "z": lambda u, v: (u, v, 0.0)}[axis]
    draw_segments(sk, tslot_profile(spec), to_model)
    circle(sk, 0.0, 0.0, 0.0, spec["bore"])
    prof = biggest_profile(sk)
    extrude(comp, prof, length_expr, "new", along=plane_normal_sign(comp, axis))
    move(comp, comp_bodies(comp), dx, dy, dz)
    return comp


# ---------------------------------------------------------------------------
# Stage A: parameters, frame, tray rails
# ---------------------------------------------------------------------------
def stage_a():
    app, design, root = app_design()
    # posts: along Z from the floor, their sections centred ext/2 in from the corners
    for i, (dx, dy) in enumerate([("-cab_w/2 + ext/2", "ext/2"), ("cab_w/2 - ext/2", "ext/2"),
                                  ("-cab_w/2 + ext/2", "cab_d - ext/2"), ("cab_w/2 - ext/2", "cab_d - ext/2")]):
        bar(f"post-{i+1}", "z", "cab_h", dx, dy, "0 mm")
    levels = {"bottom": "ext/2", "mid": "bay_top - ext/2", "top": "cab_h - ext/2"}
    for lvl, zc in levels.items():
        if lvl == "mid":   # two front stubs with the lint box between them
            bar("rail-mid-front-left", "x", "cab_w/2 - ext - 170 mm", "-cab_w/2 + ext", "ext/2", zc)
            bar("rail-mid-front-right", "x", "cab_w/2 - ext - 170 mm", "170 mm", "ext/2", zc)
        else:
            bar(f"rail-{lvl}-front", "x", "cab_w - 2*ext", "-cab_w/2 + ext", "ext/2", zc)
        bar(f"rail-{lvl}-rear", "x", "cab_w - 2*ext", "-cab_w/2 + ext", "cab_d - ext/2", zc)
        bar(f"rail-{lvl}-left", "y", "cab_d - 2*ext", "-cab_w/2 + ext/2", "ext", zc)
        bar(f"rail-{lvl}-right", "y", "cab_d - 2*ext", "cab_w/2 - ext/2", "ext", zc)
        if lvl in ("mid", "top"):
            bar(f"rail-{lvl}-rearcross", "x", "cab_w - 2*ext", "-cab_w/2 + ext", "rear_cross_y + ext/2", zc)
    # the two 2020 tray rails, the full depth, on the bottom end rails
    bar("tray-rail-1", "y", "cab_d", "-160 mm", "0 mm", "ext + ext_small/2", size=20.0)
    bar("tray-rail-2", "y", "cab_d", "160 mm", "0 mm", "ext + ext_small/2", size=20.0)
    return "stage A: 4 posts, 15 rails, 2 tray rails"


# ---------------------------------------------------------------------------
# Stage B: every flat plate the script draws, from plates.json
# ---------------------------------------------------------------------------
KIND_AXIS = {"xz": "y", "xy": "z", "yz": "x"}    # the plane's normal axis by plate kind


def uv_to_model(kind):
    return {"xz": lambda u, v: (u, 0.0, v), "xy": lambda u, v: (u, v, 0.0), "yz": lambda u, v: (0.0, u, v)}[kind]


def sketch_axes(sk, kind):
    """Which sketch orientation (Horizontal/Vertical) runs along the plate's u axis, and the sign of each."""
    tm = uv_to_model(kind)
    o = sk.modelToSketchSpace(pt(*tm(0.0, 0.0)))
    pu = sk.modelToSketchSpace(pt(*tm(1.0, 0.0)))
    pv = sk.modelToSketchSpace(pt(*tm(0.0, 1.0)))
    H, Vt = adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, adsk.fusion.DimensionOrientations.VerticalDimensionOrientation
    u_is_x = abs(pu.x - o.x) > abs(pu.y - o.y)
    return (H if u_is_x else Vt), (Vt if u_is_x else H)


def ex_or(num, expr):
    """An expression for a dimension: the recorded expression, or the number in mm."""
    return expr if expr else f"{num:g} mm"


def neg(expr):
    return f"-({expr})"


def dim_point_from_origin(sk, point, u, v, ue, ve, orient_u, orient_v, textpt):
    """Distance dimensions from the sketch origin to a point along u and along v, only where the coordinate carries an
    expression (a number that no parameter drives stays as drawn and needs no dimension) and is not zero (a dimension
    cannot be zero; the point then simply stays)."""
    dims = sk.sketchDimensions
    if ue and abs(u) > 1e-9:
        d = dims.addDistanceDimension(sk.originPoint, point, orient_u, textpt)
        d.parameter.expression = neg(ue) if u < 0 else ue
    if ve and abs(v) > 1e-9:
        d = dims.addDistanceDimension(sk.originPoint, point, orient_v, textpt)
        d.parameter.expression = neg(ve) if v < 0 else ve


def arc3(sk, start_sp, mid_pt, end_pt):
    """A three-point arc from an existing sketch point through mid_pt to end_pt (a Point3D or a SketchPoint). Fusion
    orders an arc's own start and end counterclockwise, so the returned second value is whichever of the arc's two end
    sketch points lies at end_pt, for the next curve to continue from."""
    arc = sk.sketchCurves.sketchArcs.addByThreePoints(start_sp, mid_pt, end_pt)
    tgt = end_pt.geometry if hasattr(end_pt, "geometry") else end_pt
    a, b = arc.startSketchPoint, arc.endSketchPoint
    da = a.geometry.distanceTo(tgt)
    db = b.geometry.distanceTo(tgt)
    return arc, (a if da < db else b)


def rounded_rect(sk, tm, u0, v0, u1, v1, r):
    """A rectangle with rounded corners as a closed chain of lines and arcs; returns (lines, arcs) with the lines in
    the order bottom, right, top, left (bottom runs from (u0, v0) toward +u)."""
    lines = sk.sketchCurves.sketchLines
    P_ = lambda u, v: sk_pt(sk, *tm(u, v))
    if r <= 1e-9:
        l1 = lines.addByTwoPoints(P_(u0, v0), P_(u1, v0))
        l2 = lines.addByTwoPoints(l1.endSketchPoint, P_(u1, v1))
        l3 = lines.addByTwoPoints(l2.endSketchPoint, P_(u0, v1))
        l4 = lines.addByTwoPoints(l3.endSketchPoint, l1.startSketchPoint)
        return [l1, l2, l3, l4], []
    c = math.cos(math.radians(45)) * r
    l1 = lines.addByTwoPoints(P_(u0 + r, v0), P_(u1 - r, v0))
    a1, p1 = arc3(sk, l1.endSketchPoint, P_(u1 - r + c, v0 + r - c), P_(u1, v0 + r))
    l2 = lines.addByTwoPoints(p1, P_(u1, v1 - r))
    a2, p2 = arc3(sk, l2.endSketchPoint, P_(u1 - r + c, v1 - r + c), P_(u1 - r, v1))
    l3 = lines.addByTwoPoints(p2, P_(u0 + r, v1))
    a3, p3 = arc3(sk, l3.endSketchPoint, P_(u0 + r - c, v1 - r + c), P_(u0, v1 - r))
    l4 = lines.addByTwoPoints(p3, P_(u0, v0 + r))
    a4, _ = arc3(sk, l4.endSketchPoint, P_(u0 + r - c, v0 + r - c), l1.startSketchPoint)
    return [l1, l2, l3, l4], [a1, a2, a3, a4]


def sharp_rect(sk, tm, u0, v0, u1, v1):
    return rounded_rect(sk, tm, u0, v0, u1, v1, 0.0)[0]


def stadium(sk, tm, uc, vc, w, h):
    """A slot: a rectangle w x h with semicircular ends (w along u)."""
    lines = sk.sketchCurves.sketchLines
    P_ = lambda u, v: sk_pt(sk, *tm(u, v))
    rr = h / 2
    half = w / 2 - rr
    l1 = lines.addByTwoPoints(P_(uc - half, vc - rr), P_(uc + half, vc - rr))
    a1, p1 = arc3(sk, l1.endSketchPoint, P_(uc + half + rr, vc), P_(uc + half, vc + rr))
    l2 = lines.addByTwoPoints(p1, P_(uc - half, vc + rr))
    arc3(sk, l2.endSketchPoint, P_(uc - half - rr, vc), l1.startSketchPoint)


def sector(sk, tm, uc, vc, r0, r1, half_deg):
    """An annular sector about (uc, vc) centred on straight down (-v), from -half to +half degrees."""
    lines = sk.sketchCurves.sketchLines
    P_ = lambda u, v: sk_pt(sk, *tm(u, v))
    pol = lambda r, a: (uc + r * math.sin(math.radians(a)), vc - r * math.cos(math.radians(a)))
    l1 = lines.addByTwoPoints(P_(*pol(r0, -half_deg)), P_(*pol(r1, -half_deg)))
    a1, p1 = arc3(sk, l1.endSketchPoint, P_(*pol(r1, 0.0)), P_(*pol(r1, half_deg)))
    l2 = lines.addByTwoPoints(p1, P_(*pol(r0, half_deg)))
    arc3(sk, l2.endSketchPoint, P_(*pol(r0, 0.0)), l1.startSketchPoint)


def group_rows(items, key_fn, pos_fn):
    """Group repeated features into rows of equal spacing along u, then rows into grids along v, then leftover singles
    into columns along v. items: list of records; key_fn(rec) -> the feature's shape key; pos_fn(rec) -> (u, v, ue, ve).
    Returns a list of groups: dict(key, first=rec, n1, d1 (mm along u), e1 (expr), n2, d2 (along v), e2)."""
    from collections import defaultdict
    groups = []
    by_key = defaultdict(list)
    for rec in items:
        by_key[key_fn(rec)].append(rec)
    for key, recs in by_key.items():
        rows = []   # (v, [recs sorted by u])
        by_v = defaultdict(list)
        for rec in recs:
            u, v, ue, ve = pos_fn(rec)
            by_v[round(v, 6)].append(rec)
        for v, rr in by_v.items():
            rr.sort(key=lambda r: pos_fn(r)[0])
            run = [rr[0]]
            for rec in rr[1:]:
                du = pos_fn(rec)[0] - pos_fn(run[-1])[0]
                if len(run) == 1 or abs(du - (pos_fn(run[1])[0] - pos_fn(run[0])[0])) < 1e-6:
                    run.append(rec)
                else:
                    rows.append(run)
                    run = [rec]
            rows.append(run)
        # grids: rows with the same u0, n and spacing, equally spaced in v
        rows.sort(key=lambda run: (round(pos_fn(run[0])[0], 6), len(run), round(pos_fn(run[-1])[0] - pos_fn(run[0])[0], 6), pos_fn(run[0])[1]))
        used = [False] * len(rows)
        i = 0
        while i < len(rows):
            if used[i]:
                i += 1
                continue
            base = rows[i]
            sig = (round(pos_fn(base[0])[0], 6), len(base), round(pos_fn(base[-1])[0] - pos_fn(base[0])[0], 6))
            stack = [base]
            for j in range(i + 1, len(rows)):
                if used[j]:
                    continue
                r2 = rows[j]
                if (round(pos_fn(r2[0])[0], 6), len(r2), round(pos_fn(r2[-1])[0] - pos_fn(r2[0])[0], 6)) != sig:
                    continue
                dv = pos_fn(r2[0])[1] - pos_fn(stack[-1][0])[1]
                if len(stack) == 1 or abs(dv - (pos_fn(stack[1][0])[1] - pos_fn(stack[0][0])[1])) < 1e-6:
                    stack.append(r2)
                    used[j] = True
            used[i] = True
            first = stack[0][0]
            n1 = len(stack[0])
            d1 = (pos_fn(stack[0][1])[0] - pos_fn(first)[0]) if n1 > 1 else 0.0
            e1 = None
            if n1 > 1 and pos_fn(stack[0][1])[2] and pos_fn(first)[2]:
                e1 = f"({pos_fn(stack[0][1])[2]}) - ({pos_fn(first)[2]})"
            n2 = len(stack)
            d2 = (pos_fn(stack[1][0])[1] - pos_fn(first)[1]) if n2 > 1 else 0.0
            e2 = None
            if n2 > 1 and pos_fn(stack[1][0])[3] and pos_fn(first)[3]:
                e2 = f"({pos_fn(stack[1][0])[3]}) - ({pos_fn(first)[3]})"
            groups.append(dict(key=key, first=first, n1=n1, d1=d1, e1=e1, n2=n2, d2=d2, e2=e2))
            i += 1
    # leftover singles (n1 == n2 == 1) into columns along v
    singles = [g for g in groups if g["n1"] == 1 and g["n2"] == 1]
    groups = [g for g in groups if not (g["n1"] == 1 and g["n2"] == 1)]
    by_ku = defaultdict(list)
    for g in singles:
        u, v, ue, ve = pos_fn(g["first"])
        by_ku[(g["key"], round(u, 6))].append(g)
    for (key, u), gs in by_ku.items():
        gs.sort(key=lambda g: pos_fn(g["first"])[1])
        run = [gs[0]]
        for g in gs[1:]:
            dv = pos_fn(g["first"])[1] - pos_fn(run[-1]["first"])[1]
            if len(run) == 1 or abs(dv - (pos_fn(run[1]["first"])[1] - pos_fn(run[0]["first"])[1])) < 1e-6:
                run.append(g)
            else:
                groups.append(_column(run, pos_fn))
                run = [g]
        groups.append(_column(run, pos_fn))
    return groups


def _column(run, pos_fn):
    first = run[0]["first"]
    n2 = len(run)
    d2 = (pos_fn(run[1]["first"])[1] - pos_fn(first)[1]) if n2 > 1 else 0.0
    e2 = None
    if n2 > 1 and pos_fn(run[1]["first"])[3] and pos_fn(first)[3]:
        e2 = f"({pos_fn(run[1]['first'])[3]}) - ({pos_fn(first)[3]})"
    return dict(key=run[0]["key"], first=first, n1=1, d1=0.0, e1=None, n2=n2, d2=d2, e2=e2)


def axis_entity(comp, kind, which):
    """The construction axis along the plate's u ('u') or v ('v') direction."""
    m = {"xz": ("x", "z"), "xy": ("x", "y"), "yz": ("y", "z")}[kind]
    a = m[0] if which == "u" else m[1]
    return {"x": comp.xConstructionAxis, "y": comp.yConstructionAxis, "z": comp.zConstructionAxis}[a]


def pattern(comp, feature, axis1, n1, d1, axis2=None, n2=1, d2=None):
    """A rectangular pattern of a feature: n1 along axis1 at spacing d1 (mm or expression), and n2 along axis2."""
    rp = comp.features.rectangularPatternFeatures
    coll = adsk.core.ObjectCollection.create()
    coll.add(feature)
    inp = rp.createInput(coll, axis1, V(n1), V(d1), adsk.fusion.PatternDistanceType.SpacingPatternDistanceType)
    if axis2 is not None and n2 > 1:
        inp.setDirectionTwo(axis2, V(n2), V(d2))
    return rp.add(inp)


def V_count(n):
    return adsk.core.ValueInput.createByString(str(int(n)))


def cut_group(comp, body, kind, axis, tm, ou, ov, g, draw_one, along):
    """One cut feature for a group of repeated holes or slots, patterned along u and v."""
    sk = sketch_on(comp, axis)
    u, v, ue, ve = g["pos"]
    draw_one(sk, tm, u, v, g)
    dims = sk.sketchDimensions
    if g.get("dim_point") is not None and (ue or ve):
        dim_point_from_origin(sk, g["dim_point"](sk), u, v, ue, ve, ou, ov, sk_pt(sk, *tm(u + 10, v + 10)))
    cut = extrude(comp, all_profiles(sk), g["t"], "cut", along=along, bodies=[body])
    if g["n1"] > 1 or g["n2"] > 1:
        a1 = axis_entity(comp, kind, "u") if g["n1"] > 1 else axis_entity(comp, kind, "v")
        n1, d1 = (g["n1"], ex_or(g["d1"], g["e1"])) if g["n1"] > 1 else (g["n2"], ex_or(g["d2"], g["e2"]))
        rp = comp.features.rectangularPatternFeatures
        coll = adsk.core.ObjectCollection.create()
        coll.add(cut)
        inp = rp.createInput(coll, a1, V_count(n1), V(d1), adsk.fusion.PatternDistanceType.SpacingPatternDistanceType)
        if g["n1"] > 1 and g["n2"] > 1:
            inp.setDirectionTwo(axis_entity(comp, kind, "v"), V_count(g["n2"]), V(ex_or(g["d2"], g["e2"])))
        try:
            inp.patternComputeOption = adsk.fusion.PatternComputeOptions.AdjustPatternCompute
        except Exception:
            pass
        rp.add(inp)


def build_plate(pl):
    """One flat plate from its record: outline and big cuts in one sketch, extruded by the thickness; holes and slots as
    patterned cuts; then moved to its position. Dimensions where the numbers carry expressions."""
    kind, axis = pl["kind"], KIND_AXIS[pl["kind"]]
    tm = uv_to_model(kind)
    comp = new_comp(pl["name"])
    along = plane_normal_sign(comp, axis)
    sk = sketch_on(comp, axis)
    sk.isComputeDeferred = True
    ou, ov = sketch_axes(sk, kind)
    dims, cons = sk.sketchDimensions, sk.geometricConstraints
    u0, u1, v0, v1, r = pl["u0"], pl["u1"], pl["v0"], pl["v1"], pl["r"]
    ex = pl["ex"]
    lines, arcs = rounded_rect(sk, tm, u0, v0, u1, v1, r)
    horiz = (ou == adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation)
    for i, ln in enumerate(lines):
        try:
            if (i in (0, 2)) == horiz:
                cons.addHorizontal(ln)
            else:
                cons.addVertical(ln)
        except Exception:
            pass
    tp = sk_pt(sk, *tm((u0 + u1) / 2, (v0 + v1) / 2))
    d = dims.addDistanceDimension(lines[3].startSketchPoint, lines[1].startSketchPoint, ou, tp)   # width
    d.parameter.expression = f"({ex_or(u1, ex['u1'])}) - ({ex_or(u0, ex['u0'])})"
    d = dims.addDistanceDimension(lines[0].startSketchPoint, lines[2].startSketchPoint, ov, tp)   # height
    d.parameter.expression = f"({ex_or(v1, ex['v1'])}) - ({ex_or(v0, ex['v0'])})"
    if abs(u0) > 1e-9:
        d = dims.addDistanceDimension(sk.originPoint, lines[3].startSketchPoint, ou, tp)
        d.parameter.expression = ex_or(abs(u0), neg(ex["u0"]) if (ex["u0"] and u0 < 0) else ex["u0"])
    else:
        cons.addCoincident(sk.originPoint, lines[3])
    if abs(v0) > 1e-9:
        d = dims.addDistanceDimension(sk.originPoint, lines[0].startSketchPoint, ov, tp)
        d.parameter.expression = ex_or(abs(v0), neg(ex["v0"]) if (ex["v0"] and v0 < 0) else ex["v0"])
    else:
        cons.addCoincident(sk.originPoint, lines[0])
    if arcs:
        try:
            dm = dims.addRadialDimension(arcs[0], tp)
            dm.parameter.expression = f"{r:g} mm"
            for a in arcs[1:]:
                cons.addEqual(arcs[0], a)
        except Exception:
            pass
    # the big round cuts (the door opening) and the rectangular cuts live in the outline sketch
    for (u, v, dd, ue, ve, de) in pl["circ_cuts"]:
        c = circle(sk, *tm(u, v), dd)
        dm = dims.addDiameterDimension(c, sk_pt(sk, *tm(u + dd / 2, v + dd / 2)))
        dm.parameter.expression = ex_or(dd, de)
        dim_point_from_origin(sk, c.centerSketchPoint, u, v, ue, ve, ou, ov, sk_pt(sk, *tm(u + dd, v + dd)))
    for (uc, vc, w, h, uce, vce, we, he) in pl["rect_cuts"]:
        ls = sharp_rect(sk, tm, uc - w / 2, vc - h / 2, uc + w / 2, vc + h / 2)
        tpc = sk_pt(sk, *tm(uc, vc))
        dm = dims.addDistanceDimension(ls[3].startSketchPoint, ls[1].startSketchPoint, ou, tpc)
        dm.parameter.expression = ex_or(w, we)
        dm = dims.addDistanceDimension(ls[0].startSketchPoint, ls[2].startSketchPoint, ov, tpc)
        dm.parameter.expression = ex_or(h, he)
        ule = f"({uce}) - ({ex_or(w, we)}) / 2" if uce else None
        vle = f"({vce}) - ({ex_or(h, he)}) / 2" if vce else None
        dim_point_from_origin(sk, ls[0].startSketchPoint, uc - w / 2, vc - h / 2, ule, vle, ou, ov, tpc)
    for (uc, vc, r0, r1, half, *_rest) in pl["sectors"]:
        sector(sk, tm, uc, vc, r0, r1, half)
    sk.isComputeDeferred = False
    prof = profile_at(sk, sk_pt(sk, *tm(u0 + 5.0, v0 + 5.0)))   # the plate's own region, just inside its lower left corner
    t_expr = ex_or(pl["t"], ex["t"])
    plate_feat = extrude(comp, prof, t_expr, "new", along=along)
    body = plate_feat.bodies.item(0)
    # holes: grouped into rows, grids and columns, one cut each, patterned
    hole_groups = group_rows([tuple(h) for h in pl["holes"]], key_fn=lambda h: ("circle", round(h[2], 6)), pos_fn=lambda h: (h[0], h[1], h[3], h[4]))
    for g in hole_groups:
        h = g["first"]
        g["pos"] = (h[0], h[1], h[3], h[4])
        g["t"] = t_expr
        dd = h[2]
        holder = {}

        def draw_circle(sk, tm, u, v, g, dd=dd, holder=holder):
            holder["c"] = circle(sk, *tm(u, v), dd)

        g["dim_point"] = lambda sk, holder=holder: holder["c"].centerSketchPoint
        cut_group(comp, body, kind, axis, tm, ou, ov, g, draw_circle, along)
    slot_groups = group_rows([tuple(c) for c in pl["slots"]], key_fn=lambda c: ("slot", round(c[2], 6), round(c[3], 6)), pos_fn=lambda c: (c[0], c[1], c[4], c[5]))
    for g in slot_groups:
        c0 = g["first"]
        g["pos"] = (c0[0], c0[1], c0[4], c0[5])
        g["t"] = t_expr
        w, h = c0[2], c0[3]

        def draw_slot(sk, tm, u, v, g, w=w, h=h):
            stadium(sk, tm, u, v, w, h)

        g["dim_point"] = None
        cut_group(comp, body, kind, axis, tm, ou, ov, g, draw_slot, along)
    pos = ex_or(pl["pos"], ex["pos"])
    shift = {"y": ("0 mm", pos, "0 mm"), "z": ("0 mm", "0 mm", pos), "x": (pos, "0 mm", "0 mm")}[axis]
    move(comp, comp_bodies(comp), *shift)
    return comp


def stage_b(names=None):
    app, design, root = app_design()
    done, failed = [], []
    for pl in PLATES["plates"]:
        if names and pl["name"] not in names:
            continue
        try:
            build_plate(pl)
            done.append(pl["name"])
        except Exception:
            failed.append((pl["name"], traceback.format_exc().splitlines()[-1]))
    return f"stage B: {len(done)} plates" + (f"; failed {failed}" if failed else "")


# ---------------------------------------------------------------------------
# Stage C: the drum (sheet with its tabs, rings, splice, baffles), rollers, glides, felts
# Every drum part is drawn about the component's origin with the drum axis along +Y, then moved to the drum's place
# (0, drum_front_y, drum_axis_z), so circular patterns and angled planes use the component's Y axis.
# ---------------------------------------------------------------------------
def drum_numbers():
    ro, ri = P["drum_d"] / 2, P["drum_d"] / 2 - P["drum_t"]
    L = P["drum_l"]
    rm = (P["drum_d"] - P["drum_t"]) / 2
    flat_w = math.pi * (P["drum_d"] - P["drum_t"])
    theta = lambda x: 90.0 + math.degrees(x / rm)
    seam_ys = []
    y = P["roller_track_w"] + 10
    belt_track_y = P["motor_y0"] + P["motor_len"] + 12.0 - P["drum_front_y"]
    while y <= L - P["roller_track_w"] - 10:
        if abs(y - belt_track_y) > P["belt_track_w"] / 2 + 5:
            seam_ys.append(y)
        y += P["seam_pitch"]
    return dict(ro=ro, ri=ri, L=L, rm=rm, flat_w=flat_w, seam_ys=seam_ys,
                seam_thetas=(theta(P["seam_inset"]), theta(flat_w - P["seam_inset"])),
                tab_thetas=[theta(flat_w * (i + 0.5) / P["tab_n"]) for i in range(P["tab_n"])],
                baffle_thetas=[theta(flat_w * (i + 0.5) / P["baffle_n"]) for i in range(P["baffle_n"])],
                baffle_ys=[L / 2 + off for off in P["baffle_hole_offsets"]],
                r_tab_hole=ri - P["tab_h"] / 2)


DRUM_SHIFT = ("0 mm", "drum_front_y", "drum_axis_z")   # the drum's place


def tangent_plane(comp, theta_deg, r_out):
    """A plane tangent to the drum (axis along the component's Y) at angle theta (0 along +X, 90 along +Z) and radius
    r_out. Fusion's plane-at-angle always contains its axis, so: a radial plane through the Y axis whose normal points
    along theta (the YZ plane, normal +X, turned by -theta about +Y), then that plane offset by r_out. The angle and offset signs are
    found by testing which combination contains the point the plane must touch."""
    want = rot_xz(r_out, 0.0, theta_deg)
    planes = comp.constructionPlanes
    for sa in (1.0, -1.0):
        inp = planes.createInput()
        inp.setByAngle(comp.yConstructionAxis, adsk.core.ValueInput.createByString(f"{-sa * theta_deg} deg"), comp.yZConstructionPlane)   # the YZ plane's normal (+X) turned to theta: Fusion turns it the other way round +Y
        pa = planes.add(inp)
        pa.isLightBulbOn = False
        for so in (1.0, -1.0):
            inp2 = planes.createInput()
            inp2.setByOffset(pa, V(so * r_out))
            pl = planes.add(inp2)
            pl.isLightBulbOn = False
            g = pl.geometry
            o, n = g.origin, g.normal
            d = n.x * (want[0] * CM - o.x) + n.y * (0.0 - o.y) + n.z * (want[1] * CM - o.z)
            if abs(d) < 1e-3:
                return pl
            pl.deleteMe()
        pa.deleteMe()
    raise RuntimeError("tangent plane at %.3f degrees misses its point" % theta_deg)


def radial_holes(comp, body, theta_deg, ys, d, r_out, depth):
    """Holes along the drum's radius at angle theta (0 along +X), at the Y positions, from radius r_out inward by depth:
    circles on the tangent plane at that angle, cut inward."""
    pl = tangent_plane(comp, theta_deg, r_out)
    sk = comp.sketches.add(pl)
    p = rot_xz(r_out, 0.0, theta_deg)
    for yy in ys:
        sk.sketchCurves.sketchCircles.addByCenterRadius(sk.modelToSketchSpace(pt(p[0], yy, p[1])), d / 2 * CM)
    n = pl.geometry.normal
    u = rot_xz(1.0, 0.0, theta_deg)
    inward = -1.0 if (n.x * u[0] + n.z * u[1]) > 0 else 1.0
    return extrude(comp, all_profiles(sk), depth, "cut", along=inward)   # no participant bodies: a circular pattern of such a cut finds no target


def tab_profile(sk, dn, theta_deg, yv):
    """One tab's outline at angle theta on a sketch at Y yv: a box from ri - tab_h to the outer surface, tab_w wide, the
    free end's corners rounded, with its hole; returns the profile to extrude."""
    ro, ri = dn["ro"], dn["ri"]
    tw, th, r3 = P["tab_w"], P["tab_h"], P["small_corner_r"]
    x_in = ri - th
    x_out = lambda z: math.sqrt(ro * ro - z * z)
    R = lambda x, z: rot_xz(x, z, theta_deg)
    P_ = lambda x, z: sk_pt(sk, R(x, z)[0], yv, R(x, z)[1])
    lines = sk.sketchCurves.sketchLines
    c = math.cos(math.radians(45)) * r3
    l_in = lines.addByTwoPoints(P_(x_in, -tw / 2 + r3), P_(x_in, tw / 2 - r3))
    a1, p1 = arc3(sk, l_in.endSketchPoint, P_(x_in + r3 - c, tw / 2 - r3 + c), P_(x_in + r3, tw / 2))
    l_top = lines.addByTwoPoints(p1, P_(x_out(tw / 2), tw / 2))
    a_out, p2 = arc3(sk, l_top.endSketchPoint, P_(ro, 0.0), P_(x_out(-tw / 2), -tw / 2))
    l_bot = lines.addByTwoPoints(p2, P_(x_in + r3, -tw / 2))
    arc3(sk, l_bot.endSketchPoint, P_(x_in + r3 - c, -tw / 2 + r3 - c), l_in.startSketchPoint)
    sk.sketchCurves.sketchCircles.addByCenterRadius(P_(dn["r_tab_hole"], 0.0), P["tab_hole_d"] / 2 * CM)
    return profile_at(sk, P_(x_in + 2.0, 0.0))


def build_drum_sheet(dn):
    comp = new_comp("drum-sheet")
    ro, ri, L = dn["ro"], dn["ri"], dn["L"]
    sk = sketch_on(comp, "y")
    c1 = sk.sketchCurves.sketchCircles.addByCenterRadius(sk_pt(sk, 0, 0, 0), ro * CM)
    c2 = sk.sketchCurves.sketchCircles.addByCenterRadius(sk_pt(sk, 0, 0, 0), ri * CM)
    sk.sketchDimensions.addDiameterDimension(c1, sk_pt(sk, ro, 0, ro)).parameter.expression = "drum_d"
    sk.sketchDimensions.addDiameterDimension(c2, sk_pt(sk, ri, 0, -ri)).parameter.expression = "drum_d - 1.6 mm"
    along = plane_normal_sign(comp, "y")
    shell = extrude(comp, profile_at(sk, sk_pt(sk, ro - 0.4, 0, 0)), "drum_l", "new", along=along)
    body = shell.bodies.item(0)
    theta0 = dn["tab_thetas"][0]
    # the first tab at the script's first angle on each end, joined to the sheet and patterned round
    skf = sketch_on(comp, "y")
    tab_f = extrude(comp, tab_profile(skf, dn, theta0, 0.0), P["drum_t"], "join", along=-along, bodies=[body])
    circ_pattern(comp, [tab_f], comp.yConstructionAxis, P["tab_n"], "360 deg")
    skr = comp.sketches.add(offset_plane(comp, "y", "drum_l"))
    tab_r = extrude(comp, tab_profile(skr, dn, theta0, L), P["drum_t"], "join", along=along, bodies=[body])
    circ_pattern(comp, [tab_r], comp.yConstructionAxis, P["tab_n"], "360 deg")
    # seam holes down both seam edges, and the baffle holes, through the wall
    for th in dn["seam_thetas"]:
        radial_holes(comp, body, th, dn["seam_ys"], P["seam_hole_d"], ro + 2, P["drum_t"] + 4)
    for th in dn["baffle_thetas"]:
        radial_holes(comp, body, th, dn["baffle_ys"], P["baffle_hole_d"], ro + 2, P["drum_t"] + 4)
    move(comp, [body], *DRUM_SHIFT)
    return comp


def build_rings(dn):
    ro, ri, L = dn["ro"], dn["ri"], dn["L"]
    for name, y_expr in (("drum-ring-front", "drum_front_y"), ("drum-ring-rear", f"drum_front_y + drum_l - {P['ring_t']} mm")):
        comp = new_comp(name)
        sk = sketch_on(comp, "y")
        c1 = sk.sketchCurves.sketchCircles.addByCenterRadius(sk_pt(sk, 0, 0, 0), ri * CM)
        c2 = sk.sketchCurves.sketchCircles.addByCenterRadius(sk_pt(sk, 0, 0, 0), P["ring_id"] / 2 * CM)
        sk.sketchDimensions.addDiameterDimension(c1, sk_pt(sk, ri, 0, ri)).parameter.expression = "drum_d - 1.6 mm"
        sk.sketchDimensions.addDiameterDimension(c2, sk_pt(sk, 0, 0, -P["ring_id"] / 2)).parameter.expression = f"{P['ring_id']} mm"
        along = plane_normal_sign(comp, "y")
        ring = extrude(comp, profile_at(sk, sk_pt(sk, ri - 5, 0, 0)), P["ring_t"], "new", along=along)
        body = ring.bodies.item(0)
        skh = sketch_on(comp, "y")
        p = rot_xz(dn["r_tab_hole"], 0.0, dn["tab_thetas"][0])
        skh.sketchCurves.sketchCircles.addByCenterRadius(sk_pt(skh, p[0], 0, p[1]), P["tab_hole_d"] / 2 * CM)
        hole = extrude(comp, all_profiles(skh), P["ring_t"], "cut", along=along)
        circ_pattern(comp, [hole], comp.yConstructionAxis, P["tab_n"], "360 deg")
        move(comp, [body], "0 mm", y_expr, "drum_axis_z")


def build_splice(dn):
    ro, ri, L = dn["ro"], dn["ri"], dn["L"]
    comp = new_comp("drum-splice")
    half_ang = math.degrees((P["splice_w"] / 2) / ri)
    spl_len = L - 2 * P["ring_t"] - 2
    y_start = P["ring_t"] + 1
    w = ri * math.sin(math.radians(half_ang)) + 0.005          # the keep box's half width
    r_in = ri - P["splice_t"]
    zo = lambda x, r: math.sqrt(r * r - x * x)
    sk = comp.sketches.add(offset_plane(comp, "y", y_start))
    P_ = lambda x, z: sk_pt(sk, x, y_start, z)
    lines = sk.sketchCurves.sketchLines
    l1 = lines.addByTwoPoints(P_(-w, zo(w, r_in)), P_(-w, zo(w, ri)))
    a1, p1 = arc3(sk, l1.endSketchPoint, P_(0.0, ri), P_(w, zo(w, ri)))
    l2 = lines.addByTwoPoints(p1, P_(w, zo(w, r_in)))
    arc3(sk, l2.endSketchPoint, P_(0.0, r_in), l1.startSketchPoint)
    along = plane_normal_sign(comp, "y")
    spl = extrude(comp, all_profiles(sk), spl_len, "new", along=along)
    body = spl.bodies.item(0)
    fillet_parallel_edges(comp, body, "z", P["small_corner_r"])
    for th in dn["seam_thetas"]:
        radial_holes(comp, body, th, dn["seam_ys"], P["seam_hole_d"], ri + 2, P["splice_t"] + 6)
    move(comp, [body], *DRUM_SHIFT)
    return comp


def build_baffles(dn):
    ro, ri, L = dn["ro"], dn["ri"], dn["L"]
    leg, t_ang = P["baffle_leg"], 3.0
    d_leg = math.sqrt(ri ** 2 - (leg / 2) ** 2) - 0.05
    yb0 = L / 2 - P["baffle_len"] / 2
    for i, theta in enumerate(dn["baffle_thetas"]):
        comp = new_comp(f"baffle-{i+1} (angle, cut to length)")
        prof_pts = [(d_leg - t_ang, -leg / 2), (d_leg, -leg / 2), (d_leg, leg / 2), (d_leg - leg, leg / 2),
                    (d_leg - leg, leg / 2 - t_ang), (d_leg - t_ang, leg / 2 - t_ang)]
        pts = [rot_xz(x, z, theta) for (x, z) in prof_pts]
        sk = comp.sketches.add(offset_plane(comp, "y", yb0))
        polygon(sk, [(x, yb0, z) for (x, z) in pts])
        along = plane_normal_sign(comp, "y")
        ang = extrude(comp, all_profiles(sk), P["baffle_len"], "new", along=along)
        body = ang.bodies.item(0)
        radial_holes(comp, body, theta, dn["baffle_ys"], P["baffle_hole_d"], d_leg + 2, t_ang + 4)
        move(comp, [body], *DRUM_SHIFT)


def build_rollers(dn):
    rr = P["drum_d"] / 2 + P["roller_d"] / 2
    roller_w = 25.0
    L = dn["L"]
    ry = {"front": P["roller_inset"], "rear": L - P["roller_inset_rear"] - roller_w}   # from the drum's front face
    for i, ang in enumerate((-P["roller_angle_deg"], P["roller_angle_deg"])):
        for end in ("front", "rear"):
            comp = new_comp(f"roller-{end}-{i+1} (bought)")
            sk = sketch_on(comp, "y")
            c1 = sk.sketchCurves.sketchCircles.addByCenterRadius(sk_pt(sk, 0, 0, 0), P["roller_d"] / 2 * CM)
            sk.sketchCurves.sketchCircles.addByCenterRadius(sk_pt(sk, 0, 0, 0), P["roller_bore_d"] / 2 * CM)
            along = plane_normal_sign(comp, "y")
            rl = extrude(comp, profile_at(sk, sk_pt(sk, P["roller_d"] / 2 - 2, 0, 0)), roller_w, "new", along=along)
            sa, ca = math.sin(math.radians(ang)), math.cos(math.radians(ang))
            y_e = f"drum_front_y + {P['roller_inset']} mm" if end == "front" else f"drum_front_y + drum_l - {roller_w + P['roller_inset_rear']} mm"
            move(comp, [rl.bodies.item(0)], f"(drum_d / 2 + {P['roller_d'] / 2} mm) * {sa:.6f}", y_e,
                 f"drum_axis_z - (drum_d / 2 + {P['roller_d'] / 2} mm) * {ca:.6f}")


def build_felts():
    """Two arcs per bulkhead, on the ring faces; the glide pads sit in the gaps (7b Seals)."""
    pad_half = math.degrees((P["glide_w"] + 2.0) / 2 / P["glide_r"])
    long_half = 180.0 - P["glide_angle_deg"] - pad_half
    short_half = P["glide_angle_deg"] - pad_half
    for end, y_expr, t in (("rear", f"rear_bulk_y - {P['felt_t_rear']} mm", P["felt_t_rear"]), ("front", "front_bulk_y + t_bulk", P["felt_t"])):
        for arc_name, half, up in ((f"felt-seal-{end}-long", long_half, False), (f"felt-seal-{end}-short", short_half, True)):
            comp = new_comp(arc_name)
            sk = sketch_on(comp, "y")
            sgn = -1.0 if up else 1.0     # the long arc hangs below the axis, the short one stands above it
            tm = lambda u, v: (u, 0.0, -v if up else v)
            sector(sk, tm, 0.0, 0.0, P["felt_ri"], P["felt_ro"], half)
            along = plane_normal_sign(comp, "y")
            f_ = extrude(comp, all_profiles(sk), t, "new", along=along)
            move(comp, [f_.bodies.item(0)], "0 mm", y_expr, "drum_axis_z")


def build_glides():
    """Two nylon pads per bulkhead at 10 and 2 o'clock on the felt's radius, with two M4 holes and sunk nut pockets."""
    for end, y_expr, t, pocket_far in (("front", "front_bulk_y + t_bulk", P["glide_t_front"], True), ("rear", f"rear_bulk_y - {P['glide_t_rear']} mm", P["glide_t_rear"], False)):
        comp = new_comp(f"drum-glides-{end} (bought, 2 x nylon drum glide pads, 45 x 20 x {t:g})")
        along = plane_normal_sign(comp, "y")
        for ang in (-P["glide_angle_deg"], P["glide_angle_deg"]):
            a = math.radians(ang)
            cx_, cz_ = P["glide_r"] * math.sin(a), P["glide_r"] * math.cos(a)
            sk = sketch_on(comp, "y")
            # the pad's rounded rectangle, long axis along the tangent, drawn in place about the drum axis at the origin
            tm = lambda u, v: (cx_ + u * math.cos(a) - v * math.sin(a), 0.0, cz_ - u * math.sin(a) - v * math.cos(a))
            rounded_rect(sk, tm, -P["glide_w"] / 2, -P["glide_h"] / 2, P["glide_w"] / 2, P["glide_h"] / 2, 3.0)
            for k in (-12.0, 12.0):
                sk.sketchCurves.sketchCircles.addByCenterRadius(sk_pt(sk, *tm(k, 0.0)), 2.25 * CM)
            pad = extrude(comp, profile_at(sk, sk_pt(sk, *tm(0.0, 0.0))), t, "new", along=along)
            body = pad.bodies.item(0)
            # nut pockets 4.5 deep, open on the ring side
            y_pl = (t - 4.5) if pocket_far else 4.5
            pl = offset_plane(comp, "y", y_pl)
            skp = comp.sketches.add(pl)
            for k in (-12.0, 12.0):
                cxk, _, czk = tm(k, 0.0)
                hexpts = [(cxk + 7.6 / 2 / math.cos(math.radians(30)) * math.cos(math.radians(60 * j)), y_pl, czk + 7.6 / 2 / math.cos(math.radians(30)) * math.sin(math.radians(60 * j))) for j in range(6)]
                polygon(skp, hexpts)
            extrude(comp, all_profiles(skp), 4.5, "cut", along=along * (1.0 if pocket_far else -1.0), bodies=[body])   # two pads in one component: keep the cut to its pad
        move(comp, comp_bodies(comp), "0 mm", y_expr, "drum_axis_z")


def stage_c():
    app, design, root = app_design()
    dn = drum_numbers()
    done = []
    for fn in (lambda: build_drum_sheet(dn), lambda: build_rings(dn), lambda: build_splice(dn), lambda: build_baffles(dn),
               lambda: build_rollers(dn), build_felts, build_glides):
        try:
            fn()
            done.append(fn.__name__ if hasattr(fn, "__name__") and fn.__name__ != "<lambda>" else "drum part")
        except Exception:
            done.append("FAILED: " + traceback.format_exc().splitlines()[-1])
    return "stage C: " + "; ".join(done)


# ---------------------------------------------------------------------------
# Stage D helpers: boxes, tubes, prisms and holes (the flat-bar duct frames, foam strips, angle feet, envelopes)
# ---------------------------------------------------------------------------
def rect_on(comp, axis, at, a0, b0, a1, b1, at_e=None):
    """A sketch on the plane normal to axis at the model coordinate `at` (expression at_e where given) holding the
    rectangle (a0, b0)-(a1, b1) in the plane's other two model axes, in model order: (y, z), (x, z) or (x, y)."""
    pl = offset_plane(comp, axis, at if at_e is None else at_e)
    sk = comp.sketches.add(pl)
    tm = {"x": lambda u, v: (at, u, v), "y": lambda u, v: (u, at, v), "z": lambda u, v: (u, v, at)}[axis]
    sharp_rect(sk, tm, a0, b0, a1, b1)
    return sk


def box_body(comp, x0, x1, y0, y1, z0, z1, op="new", body=None, z0e=None, he=None):
    """An axis-aligned box: a rectangle on the XY plane at z0 (an expression where given) extruded to z1. With op 'join'
    or 'cut' it works on body; returns the box's body for a new one."""
    sk = rect_on(comp, "z", z0, x0, y0, x1, y1, at_e=z0e)
    f = extrude(comp, all_profiles(sk), (z1 - z0) if he is None else he, op, along=plane_normal_sign(comp, "z"),
                bodies=participants(comp, op, body))
    return f.bodies.item(0) if op == "new" else body


def participants(comp, op, body):
    """The bodies a feature works on: a join merges with every body of the component it meets (a piece that only
    touches another is left as a body of its own, so the component's bodies are moved together); a cut keeps to the
    body it was given."""
    if op == "join":
        return comp_bodies(comp) or None
    return [body] if body is not None else None


def rect_cut(comp, body, axis, at, a0, b0, a1, b1, depth, into, at_e=None):
    """A rectangular pocket or through cut from the plane normal to axis at `at`, `depth` deep along `into` (+1 toward
    +axis, -1 toward -axis), limited to body."""
    sk = rect_on(comp, axis, at, a0, b0, a1, b1, at_e=at_e)
    return extrude(comp, all_profiles(sk), depth, "cut", along=into * plane_normal_sign(comp, axis), bodies=[body])


def holes(comp, body, axis, at, pts, d, depth, into, at_e=None):
    """Round holes of diameter d: circles on the plane normal to axis at the model coordinate `at` (expression at_e
    where given), cut `depth` deep along `into` (+1 toward +axis, -1 toward -axis) into body. pts: (a, b) pairs in the
    plane's other two model axes, in model order. One sketch and one cut for the whole list."""
    if not pts:
        return None
    pl = offset_plane(comp, axis, at if at_e is None else at_e)
    sk = comp.sketches.add(pl)
    for (a, b) in pts:
        p = {"x": (at, a, b), "y": (a, at, b), "z": (a, b, at)}[axis]
        circle(sk, *p, d)
    return extrude(comp, all_profiles(sk), depth, "cut", along=into * plane_normal_sign(comp, axis), bodies=[body])


def tapped(comp, body, axis, at, pts, depth, into, d=4.2, at_e=None):
    """The script's tapped holes: 4.2 (the thread's outside diameter) from the bar's face, `depth` deep."""
    return holes(comp, body, axis, at, pts, d, depth, into, at_e=at_e)


def tube_body(comp, axis, c, d_out, d_in, a0, length, op="new", body=None, a0e=None, le=None):
    """A cylinder (d_in 0) or tube along axis from the model coordinate a0 (expression a0e), `length` toward +axis
    (negative lengths go the other way), centred at c (the other two coordinates in model order)."""
    pl = offset_plane(comp, axis, a0 if a0e is None else a0e)
    sk = comp.sketches.add(pl)
    at = lambda u, v: {"x": (a0, u, v), "y": (u, a0, v), "z": (u, v, a0)}[axis]
    circle(sk, *at(c[0], c[1]), d_out)
    if d_in > 0:
        circle(sk, *at(c[0], c[1]), d_in)
    prof = profile_at(sk, sk_pt(sk, *at(c[0] + (d_out + d_in) / 4.0, c[1])))
    f = extrude(comp, prof, length if le is None else le, op, along=plane_normal_sign(comp, axis),
                bodies=participants(comp, op, body))
    return f.bodies.item(0) if op == "new" else body


def prism(comp, axis, a0, length, pts, op="new", body=None, a0e=None, le=None):
    """A polygon in the plane normal to axis at a0 (points in the plane's other two model axes, in model order),
    extruded `length` toward +axis."""
    pl = offset_plane(comp, axis, a0 if a0e is None else a0e)
    sk = comp.sketches.add(pl)
    tm = {"x": lambda u, v: (a0, u, v), "y": lambda u, v: (u, a0, v), "z": lambda u, v: (u, v, a0)}[axis]
    polygon(sk, [tm(u, v) for (u, v) in pts])
    f = extrude(comp, all_profiles(sk), length if le is None else le, op, along=plane_normal_sign(comp, axis),
                bodies=participants(comp, op, body))
    return f.bodies.item(0) if op == "new" else body


def sector_body(comp, y0, r0, r1, half_deg, depth, up=False, inner=None, op="new", body=None):
    """An annular sector about the component's Y axis (the drum axis before the part is moved), centred straight down
    (or up), from y0 by depth toward +Y; with inner=(r0, r1, half) a second sector is drawn inside it and the band
    between the two is what is extruded (the script's sector.cut(sector))."""
    pl = offset_plane(comp, "y", y0)
    sk = comp.sketches.add(pl)
    tm = (lambda u, v: (u, y0, -v)) if up else (lambda u, v: (u, y0, v))
    sector(sk, tm, 0.0, 0.0, r0, r1, half_deg)
    if inner is not None:
        sector(sk, tm, 0.0, 0.0, inner[0], inner[1], inner[2])
        r_pick = (r0 + inner[0]) / 2.0 if inner[0] - r0 > 1e-6 else (r1 + inner[1]) / 2.0
    else:
        r_pick = (r0 + r1) / 2.0
    prof = profile_at(sk, sk_pt(sk, *tm(0.0, -r_pick)))
    f = extrude(comp, prof, depth, op, along=plane_normal_sign(comp, "y"), bodies=[body] if body is not None else None)
    return f.bodies.item(0) if op == "new" else body


def fillet_circle_edges(comp, body, radius_mm, r):
    """Fillet every circular edge of the body with the given radius (a cylinder's end edges)."""
    coll = adsk.core.ObjectCollection.create()
    for i in range(body.edges.count):
        ed = body.edges.item(i)
        g = ed.geometry
        if g.curveType == adsk.core.Curve3DTypes.Circle3DCurveType and abs(g.radius / CM - radius_mm) < 1e-4:
            coll.add(ed)
    if coll.count == 0:
        return None
    ff = comp.features.filletFeatures
    inp = ff.createInput()
    inp.edgeSetInputs.addConstantRadiusEdgeSet(coll, V(r), True)
    return ff.add(inp)


def pol_xz(th_deg, r):
    """The script's basket points: (theta, r) about the drum axis, theta from straight down toward +X."""
    a = math.radians(th_deg)
    return (r * math.sin(a), -r * math.cos(a))


# ---------------------------------------------------------------------------
# Stage D: the ducts (lint box, spool, basket, liner, hood, trunk, nozzle), the blower plate's feet, the exhaust set.
# The duct frames are the script's boxes with the same tapped holes (4.2, from the bar's face, the screw's length less
# the plate it passes through); they are drawn in place at the script's numbers, as the console sub-frame's rails are.
# Parts about the drum axis (liner, basket) are drawn about the component's Y axis and moved up by drum_axis_z.
# ---------------------------------------------------------------------------
def console_frame():
    """The console sub-frame: four 4040 posts on the top panel over the rear cross rail and the rear top rail, four rails
    between them at the top (the script's console-post-N and console-rail-*)."""
    z0 = "cab_h + t_panel"
    zr = "cab_h + t_panel + console_h - ext/2"
    k = 1
    for dx in ("-cab_w/2 + ext/2", "cab_w/2 - ext/2"):
        for dy in ("rear_cross_y + ext/2", "cab_d - ext/2"):
            bar(f"console-post-{k}", "z", "console_h", dx, dy, z0)
            k += 1
    bar("console-rail-front", "x", "cab_w - 2*ext", "-cab_w/2 + ext", "rear_cross_y + ext/2", zr)
    bar("console-rail-rear", "x", "cab_w - 2*ext", "-cab_w/2 + ext", "cab_d - ext/2", zr)
    bar("console-rail-left", "y", "cab_d - rear_cross_y - 2*ext", "-cab_w/2 + ext/2", "rear_cross_y + ext", zr)
    bar("console-rail-right", "y", "cab_d - rear_cross_y - 2*ext", "cab_w/2 - ext/2", "rear_cross_y + ext", zr)


def duct_numbers():
    tp, tb = P["t_panel"], P["t_bulk"]
    n = dict(tp=tp, tb=tb, BAR_T=P["bar_t"], BAR_W=P["bar_w"])
    n["LR_I"], n["LR_O"] = P["liner_ri"], P["liner_ri"] + P["liner_t"]
    n["LB_X"], n["LBZ0"], n["LB_Y0"] = P["lb_x"], P["lb_z0"], P["lb_y0"]
    n["LBI"] = n["LB_X"] - n["BAR_T"]
    n["LB_BAR_X"] = P["lb_x"] - P["bar_t"] / 2
    n["lb_by0"], n["lb_by1"] = n["LB_Y0"] + tp, n["LB_Y0"] + tp + n["BAR_W"]
    n["LB_TOP_R"] = n["LR_O"] + 0.2
    n["side_z"] = [80.0, 160.0, 240.0, 330.0, 420.0]
    n["SP_H"], n["SPZ0"], n["SPZ1"], n["SPW"] = P["sp_half"], P["sp_z0"], P["sp_z1"], P["sp_bar_w"]
    n["SPI"] = n["SP_H"] - n["BAR_T"]
    n["SPZI0"], n["SPZI1"] = n["SPZ0"] + n["BAR_T"], n["SPZ1"] - n["BAR_T"]
    n["sp_y0"], n["sp_y1"] = n["lb_by1"] + tp, n["lb_by1"] + tp + n["SPW"]
    n["spool_bottom_pts"] = [(-40.0, n["SPZ0"] + n["BAR_T"] / 2), (0.0, n["SPZ0"] + n["BAR_T"] / 2), (40.0, n["SPZ0"] + n["BAR_T"] / 2)]
    n["sp_top_pts"] = [(x, n["SPZ1"] - n["BAR_T"] / 2) for x in (-40.0, 0.0, 40.0)]
    # basket
    n["BK0"], n["BK1"], n["BKH"], n["BKT"] = P["bk_r0"], P["bk_r1"], P["bk_half_deg"], P["bk_t"]
    n["MT"], n["FL"] = P["mesh_t"], P["bk_flange"]
    n["EPS"] = math.degrees(n["MT"] / ((n["BK0"] + n["BK1"]) / 2))
    n["fy0"], n["ly_"] = P["bk_far_y0"], P["bk_lip_y0"]
    n["wall_y0"] = n["fy0"] + n["BKT"] + n["MT"] + tp
    n["LIP0"], n["LIP1"], n["LIPH"] = 232.0, 268.5, 37.5
    n["far_pts"] = [(th, n["BK1"] - 3.2) for th in (-28.0, -10.0, 10.0, 28.0)] + [(th, n["BK0"] + 3.3) for th in (-20.0, 20.0)]
    n["lip_pts"] = [(th, n["BK0"] - n["MT"] - 2.5) for th in (-24.0, -8.0, 8.0, 24.0)] + [(th, (n["BK0"] + n["BK1"]) / 2) for th in (-36.7, 36.7)]
    n["pz"] = -P["bk_pull_r"] - 3.5
    # riser
    n["HX"], n["HBW"], n["RZ0"] = P["hood_x"], P["hood_bar_w"], P["riser_z0"]
    n["HY0"], n["HY1"] = P["hood_y0"], P["tr_y0"] + tp + P["tr_bar_w"] + tp
    n["hz0"], n["hz1"] = n["RZ0"] + tp, n["RZ0"] + tp + n["HBW"]
    n["HXI"] = n["HX"] - n["BAR_T"]
    n["TX"], n["TBW"], n["TY0"] = P["tr_x"], P["tr_bar_w"], P["tr_y0"]
    n["TXI"] = n["TX"] - n["BAR_T"]
    n["ty0b"], n["ty1b"] = n["TY0"] + tp, n["TY0"] + tp + n["TBW"]
    n["TZ1"] = P["drum_axis_z"] + P["inlet_above_axis"] + P["inlet_h"] + P["tr_over"]
    n["hood_side_pts"] = [(sx * (n["HX"] - n["BAR_T"] / 2), y) for sx in (-1, 1) for y in (500.0, 580.0, 690.0)]
    n["hood_end_pts"] = [(x, n["HY0"] + n["BAR_T"] / 2) for x in (-120.0, 120.0)] + [(x, n["HY1"] - n["BAR_T"] / 2) for x in (-150.0, 150.0)]
    n["trunk_side_z"] = (320.0, 440.0, 560.0, 680.0, 800.0)
    n["NZ0"], n["NZ1"] = P["nz_z"]
    n["NX"], n["NBW"] = P["nz_x"], P["nz_bar_w"]
    n["NXI"] = n["NX"] - n["BAR_T"]
    n["NZ_BX"] = P["nz_x"] - P["bar_t"] / 2
    n["nz_trunk_pts"] = [(sx * (n["NX"] - n["BAR_T"] / 2), z) for sx in (-1, 1) for z in (700.0, 775.0)] + [(x, z) for x in (-60.0, 0.0, 60.0) for z in (n["NZ0"] + n["BAR_T"] / 2, n["NZ1"] - n["BAR_T"] / 2)]
    n["nz_bulk_pts"] = ([(sx * n["NZ_BX"], z) for sx in (-1, 1) for z in (690.0, 785.0)]
                        + [(x, z) for x in (-70.0, 0.0, 70.0) for z in (n["NZ0"] + P["bar_t"] / 2, n["NZ1"] - P["bar_t"] / 2)])
    n["nz_y0"], n["nz_y1"] = P["rear_bulk_y"] + tb + P["nz_foam"], n["TY0"]
    # blower plate feet and the exhaust set
    n["A_L"], n["A_T"] = 20.0, 2.0
    n["BP_Y0"] = P["bp_y0"]
    n["BP_FOOT_Y"] = P["bp_y0"] - 20.0 / 2
    n["bp_leg_pts"] = [(sx * x, 10.0) for sx in (-1, 1) for x in (70.0, 110.0)]
    n["bp_foot_pts"] = [(sx * x, n["BP_FOOT_Y"]) for sx in (-1, 1) for x in (70.0, 110.0)]
    n["EX_X"], n["EX_Z"], n["EX_D"] = P["exhaust_x"], P["exhaust_z"], P["exhaust_d"]
    n["EX_R"], n["EX_WALL"] = n["EX_D"] / 2, P["exhaust_wall"]
    n["EX_Y0"] = P["motor_y0"]                      # the script sets P["exhaust_y0"] = my0 after the motor is drawn
    n["EX_Y1"] = P["D"] + tp + P["exhaust_proud"]
    n["EX_LEN"] = n["EX_Y1"] - (n["EX_Y0"] + 2.0)
    n["tap_z"] = n["EX_Z"] + n["EX_R"]
    px_, py_ = P["ps1_xy"]
    n["PS1_PORT"] = (px_, py_ + 24.0, 60.0)
    n["tube_pts"] = [(n["EX_X"], P["exhaust_tap_y"], n["tap_z"] + 20.0), (n["EX_X"], P["exhaust_tap_y"], 240.0), (px_, py_ + 24.0, 240.0), n["PS1_PORT"]]
    return n


def build_liner(n):
    LR_I, LR_O, L_ = n["LR_I"], n["LR_O"], P["liner_len"]
    comp = new_comp("liner")
    body = tube_body(comp, "y", (0.0, 0.0), 2 * LR_O, 2 * LR_I, 0.0, L_)
    rect_cut(comp, body, "y", -1.0, -1.0, LR_I - 1.0, 1.0, LR_O + 1.0, L_ + 2.0, +1)       # 2 mm seam gap at the top
    for th in (87.0, 93.0):
        radial_holes(comp, body, th, [L_ / 2], 3.4, LR_O + 1.0, LR_O - LR_I + 4.0)
    move(comp, [body], "0 mm", f"{P['liner_y0']} mm", "drum_axis_z")
    # the splice strip under the seam, inside the liner
    comp = new_comp("liner-splice")
    spl_half = math.degrees(20.0 / (LR_I - 0.75))
    body = sector_body(comp, 1.5, LR_I - 1.5, LR_I, spl_half, L_ - 3.0, up=True)
    for th in (87.0, 93.0):
        radial_holes(comp, body, th, [L_ / 2], 3.4, LR_O + 1.0, LR_O - LR_I + 4.0)
    move(comp, [body], "0 mm", f"{P['liner_y0']} mm", "drum_axis_z")


def mitre_to_liner(comp, body, n, y0, y1):
    """The lint box's side bars and foam end on the liner's radius: cut with a cylinder about the drum axis."""
    pl = offset_plane(comp, "y", y0 - 1.0)
    sk = comp.sketches.add(pl)
    c = circle(sk, 0.0, y0 - 1.0, P["drum_axis_z"], 2 * n["LB_TOP_R"])
    ou, ov = sketch_axes(sk, "xz")
    dim_point_from_origin(sk, c.centerSketchPoint, 0.0, P["drum_axis_z"], None, "drum_axis_z", ou, ov, sk_pt(sk, 10.0, y0 - 1.0, P["drum_axis_z"] + 10.0))
    return extrude(comp, all_profiles(sk), (y1 - y0) + 2.0, "cut", along=plane_normal_sign(comp, "y"), bodies=[body])


def build_lint_box(n):
    tp, tb, BAR_T, BAR_W = n["tp"], n["tb"], n["BAR_T"], n["BAR_W"]
    LB_X, LBI, LBZ0, LB_Y0, LB_BAR_X = n["LB_X"], n["LBI"], n["LBZ0"], n["LB_Y0"], n["LB_BAR_X"]
    lb_by0, lb_by1 = n["lb_by0"], n["lb_by1"]
    comp = new_comp("lint-box-bars (30 x 8 aluminium flat bar: 2 sides mitred at the top, 1 bottom)")
    for sx in (-1, 1):
        x0_, x1_ = min(sx * LBI, sx * LB_X), max(sx * LBI, sx * LB_X)
        bar_ = box_body(comp, x0_, x1_, lb_by0, lb_by1, LBZ0, 470.0)
        mitre_to_liner(comp, bar_, n, lb_by0, lb_by1)
        tapped(comp, bar_, "y", lb_by0, [(sx * LB_BAR_X, z) for z in n["side_z"]], 8.0 - tp, +1)                   # front plate
        tapped(comp, bar_, "y", lb_by1, [(sx * LB_BAR_X, z) for z in (80.0, 160.0, 240.0)], 8.0 - tp, -1)         # lower back plate
        tapped(comp, bar_, "y", lb_by1, [(sx * LB_BAR_X, z) for z in P["lb_bulk_screw_z"]], 10.0 - (tb + P["lb_gap"]), -1)   # from the drum side, through the foam
        holes(comp, bar_, "x", x0_, [(P["lb_hang_y"], P["lb_hang_z"])], 8.5, BAR_T + 1.0, +1)                     # the hang bolt
    bar_ = box_body(comp, -LBI, LBI, lb_by0, lb_by1, LBZ0, LBZ0 + BAR_T)                                          # bottom bar
    tapped(comp, bar_, "y", lb_by0, [(x, LBZ0 + BAR_T / 2) for x in (-100.0, 100.0)], 8.0 - tp, +1)
    tapped(comp, bar_, "y", lb_by1, [(x, LBZ0 + BAR_T / 2) for x in (-120.0, 120.0)], 8.0 - tp, -1)
    holes(comp, bar_, "y", lb_by0, n["spool_bottom_pts"], 4.5, BAR_W + 1.0, +1)                                   # M4 x 40 through to the spool
    # foam between the side bars and the bulkhead above the back plate
    comp = new_comp("lint-box-foam (bought, 3 mm closed-cell foam tape 8 wide, 2 x 190, compressed to 1.5)")
    for sx in (-1, 1):
        x0_, x1_ = min(sx * LBI, sx * LB_X), max(sx * LBI, sx * LB_X)
        f_ = box_body(comp, x0_, x1_, lb_by1, P["front_bulk_y"], P["lb_rear_plate_z1"], 470.0)
        mitre_to_liner(comp, f_, n, lb_by1, P["front_bulk_y"])
        holes(comp, f_, "y", lb_by1, [(sx * LB_BAR_X, z) for z in P["lb_bulk_screw_z"]], 4.5, P["front_bulk_y"] - lb_by1 + 1.0, +1)
    # the spool: four 40 x 8 bars behind the back plate, and its foam to the blower plate
    SPI, SP_H, SPZ0, SPZ1, SPZI1 = n["SPI"], n["SP_H"], n["SPZ0"], n["SPZ1"], n["SPZI1"]
    sp_y0, sp_y1 = n["sp_y0"], n["sp_y1"]
    comp = new_comp("spool-bars (40 x 8 aluminium flat bar: 2 x 136, 2 x 140)")
    for sx in (-1, 1):
        bar_ = box_body(comp, min(sx * SPI, sx * SP_H), max(sx * SPI, sx * SP_H), sp_y0, sp_y1, SPZ0, SPZ1)
        tapped(comp, bar_, "y", sp_y0, [(sx * (SP_H - BAR_T / 2), z) for z in (80.0, 160.0)], 8.0 - tp, +1)     # from inside the box
    bar_ = box_body(comp, -SPI, SPI, sp_y0, sp_y1, SPZI1, SPZ1)                                                   # top bar
    tapped(comp, bar_, "y", sp_y0, n["sp_top_pts"], 8.0 - tp, +1)
    bar_ = box_body(comp, -SPI, SPI, sp_y0, sp_y1, SPZ0, SPZ0 + BAR_T)                                            # bottom bar: M4 x 40 from the front plate
    tapped(comp, bar_, "y", sp_y0, n["spool_bottom_pts"], 40.0 - (sp_y0 - LB_Y0), +1)
    comp = new_comp("spool-foam (bought, 6 mm closed-cell foam tape 8 wide, 600, compressed to 4 on the blower plate)")
    for sx in (-1, 1):
        box_body(comp, min(sx * SPI, sx * SP_H), max(sx * SPI, sx * SP_H), sp_y1, P["bp_y0"], SPZ0, SPZ1)
    for z0_ in (SPZ0, SPZI1):
        box_body(comp, -SPI, SPI, sp_y1, P["bp_y0"], z0_, z0_ + BAR_T)


def build_basket(n):
    tp = n["tp"]
    BK0, BK1, BKH, BKT, MT, FL, EPS = n["BK0"], n["BK1"], n["BKH"], n["BKT"], n["MT"], n["FL"], n["EPS"]
    fy0, ly_, wall_y0 = n["fy0"], n["ly_"], n["wall_y0"]
    LIP0, LIP1, LIPH = n["LIP0"], n["LIP1"], n["LIPH"]
    far_xz = [pol_xz(th, r) for (th, r) in n["far_pts"]]
    lip_xz = [pol_xz(th, r) for (th, r) in n["lip_pts"]]
    up = ("0 mm", "0 mm", "drum_axis_z")
    comp = new_comp("basket-far-plate")
    b = sector_body(comp, fy0, BK0, BK1, BKH, BKT)
    holes(comp, b, "y", fy0, far_xz, 3.0, BKT + 1.0, +1)
    move(comp, comp_bodies(comp), *up)
    comp = new_comp("basket-far-clamp")
    b = sector_body(comp, fy0 + BKT + MT, BK0, BK1, BKH, tp)
    holes(comp, b, "y", fy0 + BKT + MT, far_xz, 3.4, tp + 1.0, +1)
    move(comp, comp_bodies(comp), *up)
    comp = new_comp("basket-lip-plate")
    b = sector_body(comp, ly_, LIP0, LIP1, LIPH, BKT, inner=(BK0 - MT, BK1 + MT, BKH + EPS))
    box_body(comp, -P["bk_pull_c"] / 2, P["bk_pull_c"] / 2, ly_, ly_ + BKT, -LIP0 - 2.0, -P["bk_pull_r"] + 4.0, op="join", body=b)   # the tab
    holes(comp, b, "y", ly_, lip_xz, 3.0, BKT + 1.0, +1)
    holes(comp, b, "y", ly_, [(x, n["pz"]) for x in (-P["bk_pull_c"] / 2, P["bk_pull_c"] / 2)], 4.5, BKT + 1.0, +1)
    move(comp, comp_bodies(comp), *up)
    comp = new_comp("basket-lip-clamp")
    b = sector_body(comp, ly_ + BKT + MT, LIP0, LIP1, LIPH, tp, inner=(BK0 - MT, BK1 + MT, BKH + EPS))
    holes(comp, b, "y", ly_ + BKT + MT, lip_xz, 3.4, tp + 1.0, +1)
    move(comp, comp_bodies(comp), *up)
    comp = new_comp("basket-mesh (bought, stainless 18 x 16 mesh strip, 42 wide, 350 long, wrapped and folded 5 at each edge)")
    b1 = sector_body(comp, fy0 + BKT, BK0, BK1, BKH, MT, inner=(BK0 + FL, BK1 - FL, BKH - math.degrees(FL / BK0)))          # far flange
    holes(comp, b1, "y", fy0 + BKT, far_xz, 3.4, MT + 1.0, +1)
    b2 = sector_body(comp, wall_y0, BK0 - MT, BK1 + MT, BKH + EPS, ly_ + BKT - wall_y0, inner=(BK0, BK1, BKH))              # the walls
    b3 = sector_body(comp, ly_ + BKT, BK0 - MT - FL, BK1 + MT + 2.4, LIPH, MT, inner=(BK0 - MT, BK1 + MT, BKH + EPS))        # lip flange
    holes(comp, b3, "y", ly_ + BKT, lip_xz, 3.4, MT + 1.0, +1)
    move(comp, [b1, b2, b3], *up)
    comp = new_comp("basket-pull (bought, D-pull, 64 mm centres, 25 projection)")
    c = P["bk_pull_c"]
    pz = n["pz"]
    b = tube_body(comp, "x", (ly_ - 20.0, pz), 10.0, 0.0, -c / 2 - 5.0, c + 10.0)                                           # the bar
    fillet_circle_edges(comp, b, 5.0, 4.0)
    for x in (-c / 2, c / 2):
        tube_body(comp, "y", (x, pz), 10.0, 0.0, ly_, -25.0, op="join", body=b)                                            # the legs, from the tab forward
    tapped(comp, b, "y", ly_, [(x, pz) for x in (-c / 2, c / 2)], 8.99, -1)                                                 # the script's hole starts 0.01 off the leg's end
    move(comp, comp_bodies(comp), *up)


def build_riser(n):
    tp, tb, BAR_T = n["tp"], n["tb"], n["BAR_T"]
    HX, HXI, HY0, HY1, hz0, hz1, RZ0 = n["HX"], n["HXI"], n["HY0"], n["HY1"], n["hz0"], n["hz1"], n["RZ0"]
    comp = new_comp("hood-bars (25 x 8 aluminium flat bar: 2 sides, front, rear)")
    for sx in (-1, 1):
        bar_ = box_body(comp, min(sx * HXI, sx * HX), max(sx * HXI, sx * HX), HY0, HY1, hz0, hz1)
        pts = [(x, y) for (x, y) in n["hood_side_pts"] if (x > 0) == (sx > 0)]
        tapped(comp, bar_, "z", hz0, pts, 8.0 - tp, +1)              # bottom plate, from below
        tapped(comp, bar_, "z", hz1, pts, 8.0 - tp, -1)              # top plate, from above
    for (y0_, y1_) in ((HY0, HY0 + BAR_T), (HY1 - BAR_T, HY1)):
        bar_ = box_body(comp, -HXI, HXI, y0_, y1_, hz0, hz1)
        pts = [(x, y) for (x, y) in n["hood_end_pts"] if y0_ <= y <= y1_]
        tapped(comp, bar_, "z", hz0, pts, 8.0 - tp, +1)
        tapped(comp, bar_, "z", hz1, pts, 8.0 - tp, -1)
    comp = new_comp("hood-gasket (bought, 3 mm foam ring 150 x 125, glued under the hood's bottom plate)")
    tube_body(comp, "z", (0.0, P["hm_collar_y"]), P["hood_gasket_od"], P["hm_collar_d"], RZ0 - P["hood_gasket_t"], P["hood_gasket_t"])
    # the trunk
    TX, TXI, TY0, ty0b, ty1b, TZ1 = n["TX"], n["TXI"], n["TY0"], n["ty0b"], n["ty1b"], n["TZ1"]
    comp = new_comp("trunk-bars (50 x 8 aluminium flat bar: 2 sides, 1 top)")
    for sx in (-1, 1):
        bar_ = box_body(comp, min(sx * TXI, sx * TX), max(sx * TXI, sx * TX), ty0b, ty1b, hz1 + tp, TZ1)
        xc = sx * (TX - BAR_T / 2)
        tapped(comp, bar_, "y", ty0b, [(xc, z) for z in n["trunk_side_z"]], 8.0 - tp, +1)      # front plate
        tapped(comp, bar_, "y", ty1b, [(xc, z) for z in n["trunk_side_z"]], 8.0 - tp, -1)      # rear plate
        tapped(comp, bar_, "z", hz1 + tp, [(xc, y) for y in (665.0, 688.0)], 8.0 - tp, +1)     # into the bar's foot, from inside the hood
    bar_ = box_body(comp, -TXI, TXI, ty0b, ty1b, TZ1 - BAR_T, TZ1)                               # top bar
    tapped(comp, bar_, "y", ty0b, [(x, TZ1 - BAR_T / 2) for x in (-80.0, 0.0, 80.0)], 8.0 - tp, +1)
    tapped(comp, bar_, "y", ty1b, [(x, TZ1 - BAR_T / 2) for x in (-80.0, 0.0, 80.0)], 8.0 - tp, -1)
    # the nozzle: from the bulkhead's back face (1 mm foam) to the trunk's front plate
    NX, NXI, NZ0, NZ1, nz_y0, nz_y1 = n["NX"], n["NXI"], n["NZ0"], n["NZ1"], n["nz_y0"], n["nz_y1"]
    d_bulk = 10.0 - (tb + P["nz_foam"])
    comp = new_comp("nozzle-bars (40 x 8 aluminium flat bar: 2 sides, top, bottom)")
    for sx in (-1, 1):
        bar_ = box_body(comp, min(sx * NXI, sx * NX), max(sx * NXI, sx * NX), nz_y0, nz_y1, NZ0, NZ1)
        tapped(comp, bar_, "y", nz_y1, [(x, z) for (x, z) in n["nz_trunk_pts"] if abs(x) > NXI and (x > 0) == (sx > 0)], 8.0 - tp, -1)   # from inside the trunk
        tapped(comp, bar_, "y", nz_y0, [(x, z) for (x, z) in n["nz_bulk_pts"] if abs(x) > NXI and (x > 0) == (sx > 0)], d_bulk, +1)      # from the drum side
    for (z0_, z1_) in ((NZ0, NZ0 + BAR_T), (NZ1 - BAR_T, NZ1)):
        bar_ = box_body(comp, -NXI, NXI, nz_y0, nz_y1, z0_, z1_)
        tapped(comp, bar_, "y", nz_y1, [(x, z) for (x, z) in n["nz_trunk_pts"] if z0_ <= z <= z1_], 8.0 - tp, -1)
        tapped(comp, bar_, "y", nz_y0, [(x, z) for (x, z) in n["nz_bulk_pts"] if z0_ <= z <= z1_], d_bulk, +1)
    comp = new_comp("nozzle-foam (bought, 2 mm closed-cell foam tape 8 wide, 900, compressed to 1 on the bulkhead)")
    yb = P["rear_bulk_y"] + tb
    for sx in (-1, 1):
        x0_, x1_ = min(sx * NXI, sx * NX), max(sx * NXI, sx * NX)
        f_ = box_body(comp, x0_, x1_, yb, nz_y0, NZ0, NZ1)
        holes(comp, f_, "y", yb, [(x, z) for (x, z) in n["nz_bulk_pts"] if x0_ <= x <= x1_], 4.5, nz_y0 - yb + 1.0, +1)
    for z0_ in (NZ0, NZ1 - BAR_T):
        f_ = box_body(comp, -NXI, NXI, yb, nz_y0, z0_, z0_ + BAR_T)
        holes(comp, f_, "y", yb, [(x, z) for (x, z) in n["nz_bulk_pts"] if z0_ <= z <= z0_ + BAR_T and abs(x) <= NXI], 4.5, nz_y0 - yb + 1.0, +1)


def build_exhaust(n):
    A_L, A_T, BP_Y0 = n["A_L"], n["A_T"], n["BP_Y0"]
    comp = new_comp("blower-plate-feet (angle 20x20x2, 2 x 90)")
    for sx in (-1, 1):
        x0_, x1_ = sorted((sx * P["bp_foot_x"][0], sx * P["bp_foot_x"][1]))
        # vertical leg on the plate's front face (Y BP_Y0 - 2 to BP_Y0, Z 0 to 20), foot forward on the pan (Y BP_Y0 - 20 to BP_Y0, Z 0 to 2)
        foot = prism(comp, "x", x0_, x1_ - x0_, [(BP_Y0 - A_L, 0.0), (BP_Y0, 0.0), (BP_Y0, A_L), (BP_Y0 - A_T, A_L), (BP_Y0 - A_T, A_T), (BP_Y0 - A_L, A_T)])
        holes(comp, foot, "y", BP_Y0, [(x, z) for (x, z) in n["bp_leg_pts"] if x0_ <= x <= x1_], 4.5, A_T + 1.0, -1)          # M4 through the leg
        holes(comp, foot, "z", 0.0, [(x, y) for (x, y) in n["bp_foot_pts"] if x0_ <= x <= x1_], P["m6_hole"], A_T + 1.0, +1)   # M6 through the foot
    EX_X, EX_Z, EX_D, EX_R, EX_WALL = n["EX_X"], n["EX_Z"], n["EX_D"], n["EX_R"], n["EX_WALL"]
    comp = new_comp("exhaust-duct (bought, 4 in aluminium pipe, 102 x 1, cut to length, one 6.5 hole for the tap)")
    duct = tube_body(comp, "y", (EX_X, EX_Z), EX_D, EX_D - 2 * EX_WALL, n["EX_Y0"] + 2.0, n["EX_LEN"])
    holes(comp, duct, "z", EX_Z + EX_R + 10.0, [(EX_X, P["exhaust_tap_y"])], 6.5, 20.0, -1)                                   # the tap, through the top wall
    comp = new_comp("exhaust-clamps (bought, 2 x worm-drive hose clamps for 102, envelopes)")
    for yc in (n["EX_Y0"] + 8.0, P["D"] - P["clamp_w"]):
        tube_body(comp, "y", (EX_X, EX_Z), 2 * (EX_R + 0.7), 2 * EX_R, yc, P["clamp_w"])
        box_body(comp, EX_X - 11.0, EX_X + 11.0, yc, yc + P["clamp_w"], EX_Z + EX_R + 0.7, EX_Z + EX_R + 10.7)                # the worm screw housing (a body of its own, as in the STEP)
    comp = new_comp("exhaust-tap-barb (bought, 1/8 NPT or M6 brass barb fitting with a locknut, 5 mm barb, envelope)")
    tap_z, ty = n["tap_z"], P["exhaust_tap_y"]
    hexp = lambda af: [(EX_X + af / 2 / math.cos(math.radians(30)) * math.cos(math.radians(60 * j)), ty + af / 2 / math.cos(math.radians(30)) * math.sin(math.radians(60 * j))) for j in range(6)]
    b = prism(comp, "z", tap_z, 5.0, hexp(10.0))                                                                              # the fitting's hex on the pipe
    tube_body(comp, "z", (EX_X, ty), 5.0, 0.0, tap_z + 5.0, 15.0, op="join", body=b)                                         # the barb
    tube_body(comp, "z", (EX_X, ty), 6.0, 0.0, tap_z - 9.0, 9.0, op="join", body=b)                                          # the thread through the hole
    prism(comp, "z", tap_z - 1.5 - 4.0, 4.0, hexp(10.0), op="join", body=b)                                                   # the locknut under the pipe's wall
    comp = new_comp("ps1-tube (bought, 6 mm silicone tube from the tap to PS1, drawn on its route)")
    pts = n["tube_pts"]
    # three straight runs meeting at the bends, a ball at each bend (the script's swept tube with round transitions)
    b = tube_body(comp, "z", (pts[0][0], pts[0][1]), 6.0, 0.0, pts[0][2], pts[1][2] - pts[0][2])
    d = (pts[2][0] - pts[1][0], pts[2][1] - pts[1][1])
    L2 = math.hypot(*d)
    pl = tangent_plane_xy(comp, pts[1], d)
    sk = comp.sketches.add(pl)
    sk.sketchCurves.sketchCircles.addByCenterRadius(sk.modelToSketchSpace(pt(*pts[1])), 3.0 * CM)
    nrm = pl.geometry.normal
    s = 1.0 if (nrm.x * d[0] + nrm.y * d[1]) > 0 else -1.0
    extrude(comp, all_profiles(sk), L2, "join", along=s, bodies=[b])
    tube_body(comp, "z", (pts[3][0], pts[3][1]), 6.0, 0.0, pts[3][2], pts[2][2] - pts[3][2], op="join", body=b)
    for p in (pts[1], pts[2]):
        ball(comp, p, 3.0, body=b)


def tangent_plane_xy(comp, p, d):
    """A plane through the model point p normal to the horizontal direction d (dx, dy): the XZ plane turned about the
    Z axis to face d, then offset to p (signs found by testing which plane holds p, as tangent_plane does)."""
    ang = math.degrees(math.atan2(d[1], d[0]))
    planes = comp.constructionPlanes
    for sa in (1.0, -1.0):
        for base_ang in (ang, ang + 90.0, ang - 90.0):
            inp = planes.createInput()
            inp.setByAngle(comp.zConstructionAxis, adsk.core.ValueInput.createByString(f"{sa * base_ang} deg"), comp.xZConstructionPlane)
            pa = planes.add(inp)
            pa.isLightBulbOn = False
            g = pa.geometry
            nrm = g.normal
            # the turned plane must be normal to d (within the plane's own tolerance) before it is offset
            if abs(nrm.x * d[1] - nrm.y * d[0]) > 1e-6 * math.hypot(*d) or abs(nrm.z) > 1e-9:
                pa.deleteMe()
                continue
            dist = (nrm.x * (p[0] * CM - g.origin.x) + nrm.y * (p[1] * CM - g.origin.y) + nrm.z * (p[2] * CM - g.origin.z)) / CM
            for so in (1.0, -1.0):
                inp2 = planes.createInput()
                inp2.setByOffset(pa, V(so * dist))
                pl = planes.add(inp2)
                pl.isLightBulbOn = False
                g2 = pl.geometry
                dd = g2.normal.x * (p[0] * CM - g2.origin.x) + g2.normal.y * (p[1] * CM - g2.origin.y) + g2.normal.z * (p[2] * CM - g2.origin.z)
                if abs(dd) < 1e-4:
                    return pl
                pl.deleteMe()
            pa.deleteMe()
    raise RuntimeError("no plane through %s normal to %s" % (p, d))


def ball(comp, p, r, body=None):
    """A sphere of radius r at the model point p: a half disc on an XZ plane through p revolved about a vertical axis
    through p (a sketch line), joined to body."""
    pl = offset_plane(comp, "y", p[1])
    sk = comp.sketches.add(pl)
    lines, arcs = sk.sketchCurves.sketchLines, sk.sketchCurves.sketchArcs
    top, bot = sk_pt(sk, p[0], p[1], p[2] + r), sk_pt(sk, p[0], p[1], p[2] - r)
    axis_line = lines.addByTwoPoints(top, bot)
    arcs.addByThreePoints(axis_line.startSketchPoint, sk_pt(sk, p[0] + r, p[1], p[2]), axis_line.endSketchPoint)
    rev = comp.features.revolveFeatures
    inp = rev.createInput(all_profiles(sk), axis_line, OPS["join"] if body is not None else OPS["new"])
    inp.setAngleExtent(False, adsk.core.ValueInput.createByString("360 deg"))
    if body is not None:
        inp.participantBodies = [body]
    return rev.add(inp)


def stage_d():
    app, design, root = app_design()
    n = duct_numbers()
    done = []
    for fn in (console_frame, lambda: build_liner(n), lambda: build_lint_box(n), lambda: build_basket(n), lambda: build_riser(n), lambda: build_exhaust(n)):
        try:
            fn()
            done.append(fn.__name__ if hasattr(fn, "__name__") and fn.__name__ != "<lambda>" else "duct part")
        except Exception:
            done.append("FAILED: " + traceback.format_exc().splitlines()[-1])
    return "stage D: " + "; ".join(done)


# ---------------------------------------------------------------------------
# Stage E helpers: angles, through holes, hexagons, chamfers and fillets by rule, rotated placements
# ---------------------------------------------------------------------------
def numbers():
    """The derived numbers the script writes to mechanical/cad/numbers.json (its globals the remaining parts are drawn from)."""
    global NUMBERS
    try:
        return NUMBERS
    except NameError:
        pass
    NUMBERS = json.load(open(os.path.join(REPO, "mechanical", "cad", "numbers.json"), encoding="utf-8"))["numbers"]
    return NUMBERS


def angle_x_body(comp, x0, x1, y_v, sy, z_v, sz, A_L=20.0, A_T=2.0, op="new", body=None):
    """The script's angle_x: a 20x20x2 angle along X, vertical leg from y_v toward sy and up from z_v toward sz, the
    other leg at z_v growing from y_v toward sy."""
    pts = [(y_v, z_v), (y_v + sy * A_L, z_v), (y_v + sy * A_L, z_v + sz * A_T), (y_v + sy * A_T, z_v + sz * A_T),
           (y_v + sy * A_T, z_v + sz * A_L), (y_v, z_v + sz * A_L)]
    return prism(comp, "x", x0, x1 - x0, pts, op=op, body=body)


def angle_y_body(comp, y0, y1, x_v, sx, z_v, sz, A_L=20.0, A_T=2.0, op="new", body=None):
    pts = [(x_v, z_v), (x_v + sx * A_L, z_v), (x_v + sx * A_L, z_v + sz * A_T), (x_v + sx * A_T, z_v + sz * A_T),
           (x_v + sx * A_T, z_v + sz * A_L), (x_v, z_v + sz * A_L)]
    return prism(comp, "y", y0, y1 - y0, pts, op=op, body=body)


def angle_z_body(comp, z0, z1, x_v, sx, y_v, sy, A_L=20.0, A_T=2.0, op="new", body=None):
    pts = [(x_v, y_v), (x_v + sx * A_L, y_v), (x_v + sx * A_L, y_v + sy * A_T), (x_v + sx * A_T, y_v + sy * A_T),
           (x_v + sx * A_T, y_v + sy * A_L), (x_v, y_v + sy * A_L)]
    return prism(comp, "z", z0, z1 - z0, pts, op=op, body=body)


def thru(comp, body, axis, pts, d, lo, hi):
    """Holes of diameter d right through along the axis, from 1 before lo to 1 past hi (the script's hole_x/y/z)."""
    return holes(comp, body, axis, lo - 1.0, pts, d, (hi - lo) + 2.0, +1)


def hex_pts(cu, cv, af):
    """A hexagon of the across-flats size about (cu, cv), first corner along +u (CadQuery's polygon)."""
    R = af / 2 / math.cos(math.radians(30))
    return [(cu + R * math.cos(math.radians(60 * j)), cv + R * math.sin(math.radians(60 * j))) for j in range(6)]


def edges_where(body, pred):
    coll = adsk.core.ObjectCollection.create()
    for i in range(body.edges.count):
        ed = body.edges.item(i)
        if pred(ed):
            coll.add(ed)
    return coll


def circle_edge_pred(radius_mm=None, axis=None, at=None, tol=1e-3):
    """A predicate for circular edges: of the radius, with the axis along a model direction, in the plane at that coordinate."""
    def pred(ed):
        g = ed.geometry
        if g.curveType != adsk.core.Curve3DTypes.Circle3DCurveType:
            return False
        if radius_mm is not None and abs(g.radius / CM - radius_mm) > tol:
            return False
        if axis is not None:
            n = g.normal
            comp_ = {"x": n.x, "y": n.y, "z": n.z}[axis]
            if abs(abs(comp_) - 1.0) > 1e-6:
                return False
            c = {"x": g.center.x, "y": g.center.y, "z": g.center.z}[axis] / CM
            if at is not None and abs(c - at) > tol:
                return False
        return True
    return pred


def fillet_where(comp, body, pred, r):
    coll = edges_where(body, pred)
    if coll.count == 0:
        return None
    ff = comp.features.filletFeatures
    inp = ff.createInput()
    inp.edgeSetInputs.addConstantRadiusEdgeSet(coll, V(r), True)
    return ff.add(inp)


def chamfer_where(comp, body, pred, d):
    coll = edges_where(body, pred)
    if coll.count == 0:
        return None
    cf = comp.features.chamferFeatures
    inp = cf.createInput2()
    inp.chamferEdgeSets.addEqualDistanceChamferEdgeSet(coll, V(d), True)
    return cf.add(inp)


def cyl_along(comp, theta_deg, r, t0, t1, op="new", body=None):
    """A cylinder of radius r along the direction at theta in the XZ plane (0 along +X, 90 along +Z) through the
    component's origin, from t0 to t1 along it: a circle on the plane normal to that direction at t0, extruded."""
    pl = tangent_plane(comp, theta_deg, t0)
    sk = comp.sketches.add(pl)
    p = rot_xz(t0, 0.0, theta_deg)
    sk.sketchCurves.sketchCircles.addByCenterRadius(sk.modelToSketchSpace(pt(p[0], 0.0, p[1])), r * CM)
    n = pl.geometry.normal
    u = rot_xz(1.0, 0.0, theta_deg)
    along = 1.0 if (n.x * u[0] + n.z * u[1]) > 0 else -1.0
    f = extrude(comp, all_profiles(sk), t1 - t0, op, along=along, bodies=participants(comp, op, body))
    return f.bodies.item(0) if op == "new" else body


def rot_y_pt(x, z, theta_deg):
    """The script's rotate((0,0,0),(0,1,0),theta): x' = x cos + z sin, z' = -x sin + z cos."""
    a = math.radians(theta_deg)
    return (x * math.cos(a) + z * math.sin(a), -x * math.sin(a) + z * math.cos(a))


def hex_bolt_m6(comp, p, n, length, op="new", body=None):
    """The script's M6 hex bolt with its washer, built along the normal n (a model axis direction) with the bearing
    face at p: shank d6 from -L to washer_t + 1 (tip chamfer 0.5), washer, hex head (top chamfer 0.6)."""
    wt, hh, af, wd = P["m6_washer_t"], P["m6_head_h"], P["m6_head_af"], P["m6_washer_d"]
    axis, s = axis_of(n)
    c = other_coords(p, axis)
    a0 = p[{"x": 0, "y": 1, "z": 2}[axis]]
    b = tube_body(comp, axis, c, 6.0, 0.0, a0 - s * length, s * (length + wt + 1.0), op=op, body=body)
    body = b if body is None else body
    chamfer_where(comp, body, circle_edge_pred(3.0, axis, a0 - s * length), 0.5)
    tube_body(comp, axis, c, wd, 0.0, a0, s * wt, op="join", body=body)
    prism(comp, axis, a0 + s * wt, s * hh, hex_pts(c[0], c[1], af), op="join", body=body)
    chamfer_where(comp, body, lambda ed: ed.geometry.curveType == adsk.core.Curve3DTypes.Line3DCurveType and abs(edge_coord(ed, axis) - (a0 + s * (wt + hh))) < 1e-3 and edge_in_plane(ed, axis), 0.6)
    return body


def axis_of(n):
    """('x'|'y'|'z', +1|-1) for a normal along a model axis."""
    for k, v in zip("xyz", n):
        if abs(v) > 0.5:
            return k, (1.0 if v > 0 else -1.0)
    raise ValueError("not along an axis: %s" % (n,))


def other_coords(p, axis):
    return {"x": (p[1], p[2]), "y": (p[0], p[2]), "z": (p[0], p[1])}[axis]


def edge_coord(ed, axis):
    g = ed.geometry
    m = g.startPoint.copy()
    m.translateBy(adsk.core.Vector3D.create((g.endPoint.x - g.startPoint.x) / 2, (g.endPoint.y - g.startPoint.y) / 2, (g.endPoint.z - g.startPoint.z) / 2))
    return {"x": m.x, "y": m.y, "z": m.z}[axis] / CM


def edge_in_plane(ed, axis):
    """True for a straight edge lying in a plane normal to the axis."""
    g = ed.geometry
    v = g.startPoint.vectorTo(g.endPoint)
    return abs({"x": v.x, "y": v.y, "z": v.z}[axis]) < 1e-6


def nut_body(comp, p, n, af, h, bore, op="new", body=None):
    """The script's nut: a hexagon af x h with its base on p facing n, bored."""
    axis, s = axis_of(n)
    c = other_coords(p, axis)
    a0 = p[{"x": 0, "y": 1, "z": 2}[axis]]
    b = prism(comp, axis, a0, s * h, hex_pts(c[0], c[1], af), op=op, body=body)
    body = b if body is None else body
    holes(comp, body, axis, a0 - s * 1.0, [c], bore, h + 2.0, s)
    return body


def button_bolt_body(comp, p, n, d, head_d, head_h, length, socket_af, op="new", body=None):
    """The script's button head bolt: head on p along n (its top edge filleted 0.8 head_h, hex socket 2 deep less 0.8),
    shank d from -length to 0.5 with a 0.4 tip chamfer."""
    axis, s = axis_of(n)
    c = other_coords(p, axis)
    a0 = p[{"x": 0, "y": 1, "z": 2}[axis]]
    b = tube_body(comp, axis, c, head_d, 0.0, a0, s * head_h, op=op, body=body)
    body = b if body is None else body
    fillet_where(comp, body, circle_edge_pred(head_d / 2, axis, a0 + s * head_h), head_h * 0.8)
    prism(comp, axis, a0 + s * (head_h - 1.2), s * 2.0, hex_pts(c[0], c[1], socket_af), op="cut", body=body)
    tube_body(comp, axis, c, d, 0.0, a0 - s * length, s * (length + 0.5), op="join", body=body)
    chamfer_where(comp, body, circle_edge_pred(d / 2, axis, a0 - s * length), 0.4)
    return body


# ---------------------------------------------------------------------------
# Stage E: the door, the Tier 0 module, the drive, the electric heat module, the power module, sensors, blanks, clamps,
# feet and brackets. Drawn in place at the script's numbers (mechanical/cad/numbers.json); parts about the drum axis are
# drawn about the component's Y axis and moved up by drum_axis_z, the console's module by its aperture centre.
# ---------------------------------------------------------------------------
def build_door(N):
    az = N["az"]
    ring_y0, disc_y0, t = N["ring_y0"], N["disc_y0"], P["t_door"]
    up = ("0 mm", "0 mm", "drum_axis_z")
    rel = lambda pts: [(x, z - az) for (x, z) in pts]
    comp = new_comp("door-ring")
    b = tube_body(comp, "y", (0.0, 0.0), P["door_ring_od"], P["door_ring_id"], ring_y0, t)
    holes(comp, b, "y", ring_y0, rel(N["ring_bolt_pts"]), P["m4_hole"], t + 1.0, +1)
    holes(comp, b, "y", ring_y0, rel(N["hinge_fixed_bolt_pts"]), P["m6_hole"], t + 1.0, +1)
    holes(comp, b, "y", ring_y0, rel([N["DS_P"]]), P["ds_plunger_d"] + 0.5, t + 1.0, +1)
    move(comp, comp_bodies(comp), *up)
    comp = new_comp("door-disc")
    b = tube_body(comp, "y", (0.0, 0.0), P["door_disc_d"], 0.0, disc_y0, t)
    holes(comp, b, "y", disc_y0, rel(N["hinge_swing_bolt_pts"] + N["handle_pts"]), P["m4_hole"], t + 1.0, +1)
    move(comp, comp_bodies(comp), *up)
    # hinges: the fixed half (leaf on the ring, knuckle, pin) below the axis, the swinging half above
    hx, hy = P["hinge_pin_x"], P["hinge_pin_y"]
    kd, lt, lh = P["hinge_knuckle_d"], P["hinge_leaf_t"], P["hinge_leaf_h"]
    for i, (zk_abs, kind) in enumerate(zip(N["hinge_zs"], ("fixed", "swing"))):
        zk = zk_abs - az
        if kind == "fixed":
            comp = new_comp(f"door-hinge-{i+1}-fixed (bought, flag hinge, pinned half)")
            b = tube_body(comp, "z", (hx, hy), kd, 0.0, zk - lh / 2, lh)                                           # knuckle
            box_body(comp, hx, P["hinge_leaf_x_in"], ring_y0 - lt, ring_y0, zk - lh / 2, zk + lh / 2, op="join", body=b)   # leaf on the ring's front face
            tube_body(comp, "z", (hx, hy), P["hinge_pin_d"], 0.0, zk - lh / 2 - 5.0, lh + 2 * P["hinge_z_off"] + 10.0, op="join", body=b)   # pin
            pts = rel(N["hinge_fixed_bolt_pts"])
            holes(comp, b, "y", ring_y0 - lt, pts, P["m6_hole"], lt + 1.0, +1)
            # the countersinks: the script's cone (6.1 at 3 deep to 12.6 a quarter outside the leaf's front face), which
            # also nicks the knuckle where it stands proud of that face
            for (x, z) in pts:
                cone_cut_y(comp, b, x, z, ring_y0 - lt + 3.0, 3.05, ring_y0 - lt - 0.25, 6.3)
        else:
            comp = new_comp(f"door-hinge-{i+1}-swing (bought, flag hinge, lift-off half)")
            b = tube_body(comp, "z", (hx, hy), kd, 0.0, zk - lh / 2, lh)
            box_body(comp, hx, P["hinge_leaf_x_in"], disc_y0 + t, disc_y0 + t + lt, zk - lh / 2, zk + lh / 2, op="join", body=b)   # leaf on the disc's back face
            holes(comp, b, "z", zk - lh / 2 - 1.0, [(hx, hy)], P["hinge_pin_d"] + 0.2, lh + 2.0, +1)                 # bored for the pin
            holes(comp, b, "y", disc_y0 + t, rel(N["hinge_swing_bolt_pts"]), 4.2, lt + 1.0, +1)                      # tapped M4
        move(comp, comp_bodies(comp), *up)
    # handle: two standoffs and a bar, M4 from the back of the disc into the standoffs
    hd, hs_ = P["handle_bar_d"], P["handle_standoff"]
    comp = new_comp("door-handle (bought, D handle 128 centres)")
    bar_x, bar_y = P["handle_x"], disc_y0 - hs_ - hd / 2 + 0.5
    b = tube_body(comp, "z", (bar_x, bar_y), hd, 0.0, -P["handle_span"] / 2 - hd / 2, P["handle_span"] + hd)      # the bar, its ends rounded
    fillet_where(comp, b, circle_edge_pred(hd / 2, "z"), 5.0)
    b = comp.bRepBodies.item(0)
    for (x, z) in rel(N["handle_pts"]):
        tube_body(comp, "y", (x, z), hd, 0.0, disc_y0, -hs_, op="join", body=b)                                   # the standoffs, 0.5 into the bar
    b = comp.bRepBodies.item(0)
    tapped(comp, b, "y", disc_y0, rel(N["handle_pts"]), 9.99, -1)                                                 # the script's hole starts 0.01 off the face
    move(comp, comp_bodies(comp), *up)
    comp = new_comp("door-seal (bought, OEM door seal)")
    b = tube_body(comp, "y", (0.0, 0.0), 2 * P["seal_ro"], 2 * P["seal_ri"], disc_y0 + t, P["seal_t"])
    move(comp, comp_bodies(comp), *up)
    comp = new_comp("door-catch (bought, magnetic catch)")
    b = box_body(comp, P["latch_x0"], P["latch_x1"], ring_y0 - 6.5, ring_y0, -6.0, 6.0)
    move(comp, comp_bodies(comp), *up)
    comp = new_comp("door-catch-strike (bought)")
    b = box_body(comp, P["latch_x0"], P["latch_x1"], disc_y0 + t, disc_y0 + t + 1.0, -6.0, 6.0)
    move(comp, comp_bodies(comp), *up)
    # the door switch behind the front upper panel, 45 degrees right of bottom; two M4 into its tapped ears
    bw_, bd_, bh_ = P["ds_body"]
    U, T = N["DS_U"], N["DS_T"]
    cx_, cz_ = 272.5 * U[0], 272.5 * U[1]                                   # the body's centre, about the drum axis
    comp = new_comp("door-switch (bought, two-contact plunger switch, envelope)")
    corners = [(cx_ + su * bw_ / 2 * T[0] + sv * bh_ / 2 * U[0], cz_ + su * bw_ / 2 * T[1] + sv * bh_ / 2 * U[1]) for (su, sv) in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    b = prism(comp, "y", 0.0, bd_, corners)
    dsp = (N["DS_P"][0], N["DS_P"][1] - az)
    tube_body(comp, "y", dsp, P["ds_plunger_d"], 0.0, 1.0, -12.0, op="join", body=b)                             # plunger to Y -11
    tapped(comp, b, "y", 0.0, rel(N["DS_M"]), 8.0, +1)
    move(comp, comp_bodies(comp), *up)


def cone_cut_y(comp, body, x, z, y_in, r_in, y_out, r_out):
    """A cone frustum about the line (x, *, z) along Y, radius r_in at y_in and r_out at y_out, cut from body: a
    trapezoid on the plane z = z revolved about its axis line."""
    pl = offset_plane(comp, "z", z)
    sk = comp.sketches.add(pl)
    lines = sk.sketchCurves.sketchLines
    axis = lines.addByTwoPoints(sk_pt(sk, x, y_in, z), sk_pt(sk, x, y_out, z))
    l1 = lines.addByTwoPoints(axis.endSketchPoint, sk_pt(sk, x + r_out, y_out, z))
    l2 = lines.addByTwoPoints(l1.endSketchPoint, sk_pt(sk, x + r_in, y_in, z))
    lines.addByTwoPoints(l2.endSketchPoint, axis.startSketchPoint)
    rev = comp.features.revolveFeatures
    inp = rev.createInput(all_profiles(sk), axis, OPS["cut"])
    inp.setAngleExtent(False, adsk.core.ValueInput.createByString("360 deg"))
    inp.participantBodies = [body]
    return rev.add(inp)


def combine_join(comp, target, tools):
    """Join tool bodies into the target (a Combine feature)."""
    cf = comp.features.combineFeatures
    coll = adsk.core.ObjectCollection.create()
    for t in tools:
        coll.add(t)
    inp = cf.createInput(target, coll)
    inp.operation = adsk.fusion.FeatureOperations.JoinFeatureOperation
    inp.isKeepToolBodies = False
    return cf.add(inp)


def build_tier0(N):
    """The Tier 0 module on the console face. The script draws it in face coordinates (u across, v up, w outward from the
    face plate's inner surface); here u, v, w are the component's x, z, -y, and the parts are moved to the aperture
    centre (0, rear_cross_y, cab_h + t_panel + the aperture's offset)."""
    T0 = N["T0"]
    fp_z0, fp_top, FP_T = N["fp_z0"], N["fp_top"], P["fp_t"]
    shift = ("0 mm", "rear_cross_y", f"cab_h + t_panel + {P['uci_ap_z_off']} mm")
    W = lambda w: -w          # face depth to the component's y
    comp = new_comp("tier0-faceplate")
    sk = comp.sketches.add(offset_plane(comp, "y", W(fp_z0)))
    rounded_rect(sk, lambda u, v: (u, W(fp_z0), v), -P["fp_w"] / 2, -P["fp_h"] / 2, P["fp_w"] / 2, P["fp_h"] / 2, P["fp_r"])
    along = plane_normal_sign(comp, "y")
    b = extrude(comp, all_profiles(sk), -FP_T, "new", along=along).bodies.item(0)                               # toward -y: outward
    by_d = {}
    for (x, y, d, _) in T0["holes"]:
        by_d.setdefault(round(d, 6), []).append((x, y))
    for dd, pts in by_d.items():
        holes(comp, b, "y", W(fp_z0), pts, dd, FP_T + 1.0, -1)
    engrave_labels(comp, b, T0["LABELS"], W(fp_top))
    move(comp, comp_bodies(comp), *shift)
    # knobs and timers
    for key, x in N["TIMERS"].items():
        comp = new_comp(f"tier0-knob-{key} (bought)")
        d, sk_h, bd, h = P["knob_d"], P["knob_skirt_h"], P["knob_body_d"], P["knob_h"]
        w0 = fp_top + 1.0
        b = tube_body(comp, "y", (x, 0.0), d, 0.0, W(w0), -sk_h)                                                   # skirt
        tube_body(comp, "y", (x, 0.0), bd, 0.0, W(w0), -(h - 1.0), op="join", body=b)                             # body
        fillet_where(comp, b, circle_edge_pred(bd / 2, "y", W(w0 + h - 1.0)), 2.0)
        box_body(comp, x - 1.5, x + 1.5, W(w0 + sk_h + 1.2), W(w0 + sk_h), bd / 2 - 1.0, d / 2 - 0.5, op="join", body=b)      # pointer on the skirt
        box_body(comp, x - 1.5, x + 1.5, W(w0 + h + 0.2), W(w0 + h - 1.0), 0.0, bd / 2 - 2.0, op="join", body=b)           # pointer across the top
        tube_body(comp, "y", (x, 0.0), 6.0, 0.0, 0.0, -(w0 + sk_h), op="join", body=b)                            # D shaft from the timer
        chamfer_where(comp, b, circle_edge_pred(3.0, "y", 0.0), 0.5)
        move(comp, comp_bodies(comp), *shift)
        comp = new_comp(f"tier0-timer-{key} (bought)")
        b = box_body(comp, x - 12.0, x + 12.0, W(fp_z0), W(fp_z0 - 1.5), -53.2, 53.2)                             # yoke strap against the plate's back
        holes(comp, b, "y", W(fp_z0 - 1.5), [(x, 0.0)], 13.0, 1.5 + 1.0, -1)
        box_body(comp, x - 20.3, x + 20.3, W(fp_z0 - 1.5), W(fp_z0 - 1.5 - 30.2), -35.45, 35.45, op="join", body=b)   # body behind it
        move(comp, comp_bodies(comp), *shift)
    # the two 22 mm devices: bezel, body and contact block; selector lever and start button
    DEV_Y = N["DEV_Y"]
    for x, nm_body, nm_cap, kind in ((N["SEL_X"], "tier0-selector-body (bought)", "tier0-selector (bought)", "sel"),
                                     (N["START_X"], "tier0-start-body (bought)", "tier0-start-button (bought)", "start")):
        comp = new_comp(nm_body)
        b = tube_body(comp, "y", (x, DEV_Y), 30.0, 22.3, W(fp_top), -2.5)                                           # bezel
        tube_body(comp, "y", (x, DEV_Y), 22.0, 0.0, W(-45.0), -(fp_top + 45.0), op="join", body=b)                 # body, -45 to fp_top
        box_body(comp, x - 12.5, x + 12.5, W(-15.0), W(-45.0), DEV_Y - 17.5, DEV_Y + 17.5, op="join", body=b)       # contact block
        move(comp, comp_bodies(comp), *shift)
        comp = new_comp(nm_cap)
        w0 = fp_top + 2.5
        if kind == "sel":
            b = tube_body(comp, "y", (x, DEV_Y), 22.0, 0.0, W(w0), -4.0)                                            # hub
            sk = comp.sketches.add(offset_plane(comp, "y", W(w0 + 4.0)))
            stadium(sk, lambda u, v: (v, W(w0 + 4.0), u), DEV_Y, x, 30.0, 8.0)                                     # lever, 30 along v (up)
            extrude(comp, all_profiles(sk), -6.0, "join", along=plane_normal_sign(comp, "y"), bodies=[b])
        else:
            b = tube_body(comp, "y", (x, DEV_Y), 22.0, 0.0, W(w0), -8.0)
            fillet_where(comp, b, circle_edge_pred(11.0, "y", W(w0 + 8.0)), 2.0)
        move(comp, comp_bodies(comp), *shift)
    # K1 on 100 mm of DIN rail on two standoffs behind the plate
    (rx0, ry_), (rx1, _) = T0["RAIL"]
    comp = new_comp("tier0-k1-relay-on-din-rail (bought)")
    b = box_body(comp, rx0 - 10.0, rx1 + 10.0, W(fp_z0 - 12.0), W(fp_z0 - 12.0 - 7.5), ry_ - 17.5, ry_ + 17.5)      # rail
    for x in (rx0, rx1):
        tube_body(comp, "y", (x, ry_), 8.0, 0.0, W(fp_z0 - 12.0), -12.0, op="join", body=b)                        # standoffs to the plate
    box_body(comp, rx0 - 9.0, rx0 + 19.0, W(fp_z0 - 19.5), W(fp_z0 - 19.5 - 65.0), ry_ - 36.0, ry_ + 19.0, op="join", body=b)   # socket and relay
    move(comp, comp_bodies(comp), *shift)


def engrave_labels(comp, body, labels, y_face):
    """The faceplate's labels: 5 mm text cut 0.3 into the outer face (the script's text(); Fusion's own font, so the
    engraved volume is not compared)."""
    pl = offset_plane(comp, "y", y_face)
    sk = comp.sketches.add(pl)
    texts = sk.sketchTexts
    for text, x, y in labels:
        p0 = sk_pt(sk, x - 60.0, y_face, y - 2.5)
        p1 = sk_pt(sk, x + 60.0, y_face, y + 2.5)
        try:
            inp = texts.createInput2(text, 5.0 * CM)
            inp.setAsMultiLine(p0, p1, adsk.core.HorizontalAlignments.CenterHorizontalAlignment, adsk.core.VerticalAlignments.MiddleVerticalAlignment, 0.0)
            texts.add(inp)
        except Exception:
            pass
    try:
        prof = adsk.core.ObjectCollection.create()
        for i in range(texts.count):
            prof.add(texts.item(i))
        exts = comp.features.extrudeFeatures
        inp = exts.createInput(prof, OPS["cut"])
        inp.setDistanceExtent(False, V(0.3 * plane_normal_sign(comp, "y")))
        inp.participantBodies = [body]
        exts.add(inp)
    except Exception:
        pass


def build_drive(N):
    mz, my0, ml, md, msr = N["mz"], N["my0"], N["ml"], N["md"], N["msr"]
    comp = new_comp("motor (bought)")
    b = tube_body(comp, "y", (0.0, mz), md, 0.0, my0 + 12.0, ml - 24.0)                                              # frame
    for yy in (my0, my0 + ml - 12.0):
        tube_body(comp, "y", (0.0, mz), md - 20.0, 0.0, yy, 12.0, op="join", body=b)                               # end bells
    y_sh = P["blower_y0"] + P["blower_w"]
    tube_body(comp, "y", (0.0, mz), 2 * msr, 0.0, y_sh, my0 - y_sh, op="join", body=b)                             # front shaft to the blower
    tube_body(comp, "y", (0.0, mz), 2 * msr, 0.0, my0 + ml, 4.0, op="join", body=b)                                # rear shaft to the pulley
    box_body(comp, -25.0, 25.0, my0 + 70.0, my0 + 130.0, mz + md / 2 - 5.0, mz + md / 2 + 20.0, op="join", body=b)  # terminal box
    for i, yy in enumerate(N["CRADLE_Y"]):
        comp = new_comp(f"motor-mount-{i+1} (bought, cradle bracket)")
        b = box_body(comp, -35.0, 35.0, yy, yy + 30.0, 0.0, mz - 20.0)
        rect_cut(comp, b, "z", mz - 20.0, -30.0, yy + 3.0, 30.0, yy + 27.0, mz - 23.0, -1)                        # a 3 mm shell
        holes(comp, b, "y", yy - 5.0, [(0.0, mz)], md + 1.0, 40.0, +1)                                            # the motor's seat
        holes(comp, b, "z", 0.0, [(x, y) for (x, y) in N["cradle_pts"] if yy <= y <= yy + 30.0], P["m6_hole"], 3.0 + 1.0, +1)
    pd, by = P["motor_pulley_d"], P["belt_y"]
    comp = new_comp("pulley (bought)")
    b = tube_body(comp, "y", (0.0, mz), pd, 0.0, by - 8.0, 16.0)
    for k in range(4):
        gy = by - 4.5 + 3.0 * k
        ring_cut(comp, b, "y", gy - 0.6, (0.0, mz), pd + 2.0, pd - 2.4, 1.2, +1)                                   # grooves
    tube_body(comp, "y", (0.0, mz), pd + 2.0, 0.0, by + 8.0, 6.0, op="join", body=b)                               # hub
    # the blower housing: a drum with its inlet mouth, the tangential outlet box, its 102 discharge collar
    comp = new_comp("blower (bought)")
    b = tube_body(comp, "y", (0.0, mz), P["blower_d"], 0.0, P["blower_y0"], P["blower_w"])
    holes(comp, b, "y", P["blower_y0"], [(0.0, mz)], 130.0, 8.0, +1)                                               # inlet mouth
    EX_X, EX_Z, EX_R = P["exhaust_x"], P["exhaust_z"], P["exhaust_d"] / 2
    box_body(comp, 100.0, EX_X + EX_R + 10.0, P["blower_y0"] + 26.0, my0, N["OB_Z0"], N["OB_Z1"], op="join", body=b)
    tube_body(comp, "y", (EX_X, EX_Z), 2 * (EX_R - P["exhaust_wall"] - 0.5), 2 * (EX_R - P["exhaust_wall"] - 1.5), my0, P["exhaust_collar_len"], op="join", body=b)
    oz = N["oz"]
    tapped(comp, b, "z", oz, [(x, yy) for x in P["tf_x"] for yy in (130.0, 170.0)], 8.0, -1)                      # the thermostats' screws
    tapped(comp, b, "y", P["blower_y0"], [tuple(p) for p in P["bp_screws"]], 8.0, +1)                              # the blower plate's screws


def build_belt(N):
    """The belt: the drawn path offset to the belt's thickness, extruded to its width."""
    by = P["belt_y"]
    BT, BW = N["BT"], N["BW"]
    comp = new_comp("belt (bought, PJ 5 rib)")
    y0 = by - BW / 2
    sk = comp.sketches.add(offset_plane(comp, "y", y0))
    curves = adsk.core.ObjectCollection.create()
    first = None
    prev_end = None
    for seg in N["belt_path"]:
        if seg[0] == "L":
            _, pa, pb = seg
            ln = sk.sketchCurves.sketchLines.addByTwoPoints(prev_end if prev_end is not None else sk_pt(sk, pa[0], y0, pa[1]), sk_pt(sk, pb[0], y0, pb[1]))
            curves.add(ln)
            prev_end = ln.endSketchPoint
            first = first or ln
        else:
            _, p0, mid, p1 = seg
            arc, prev_end = arc3(sk, prev_end, sk_pt(sk, mid[0], y0, mid[1]), sk_pt(sk, p1[0], y0, p1[1]))
            curves.add(arc)
    try:
        sk.geometricConstraints.addCoincident(prev_end, first.startSketchPoint)
    except Exception:
        pass
    pa = N["belt_path"][0][1]
    inside = sk_pt(sk, 0.0, y0, N["az"])                                                                          # a point inside the loop (the drum axis)
    sk.offset(curves, inside, BT / 2 * CM)
    sk.offset(curves, inside, -BT / 2 * CM)
    for i in range(curves.count):
        curves.item(i).isConstruction = True                                                                      # only the band is a profile
    prof = profile_at(sk, sk_pt(sk, pa[0], y0, pa[1]))                                                             # the band holds the path
    extrude(comp, prof, BW, "new", along=plane_normal_sign(comp, "y"))


def build_idler(N):
    """The idler pulley, arm, axle, brackets, pivot, spring posts and spring."""
    by = P["belt_y"]
    ix, iz, iw, idd = N["ix"], N["iz"], P["idler_w"], P["idler_d"]
    comp = new_comp("idler-pulley (bought, flat idler 40 with bearing)")
    b = tube_body(comp, "y", (ix, iz), idd, 0.0, by - iw / 2, iw)
    for yy in (by - iw / 2 - 1.5, by + iw / 2):
        tube_body(comp, "y", (ix, iz), idd + 4.0, 0.0, yy, 1.5, op="join", body=b)                                 # flanges
    holes(comp, b, "y", by - 15.0, [(ix, iz)], 8.2, 30.0, +1)
    piv, anchor, arm_len, arm_ang, arm_y0 = N["piv"], N["anchor"], N["arm_len"], N["arm_ang"], N["arm_y0"]
    comp = new_comp("idler-arm (flat bar 25x4, cut to length)")
    sk = comp.sketches.add(offset_plane(comp, "y", arm_y0))
    tm = lambda u, v: (piv[0] + u * math.cos(math.radians(arm_ang)) - v * math.sin(math.radians(arm_ang)), arm_y0, piv[1] + u * math.sin(math.radians(arm_ang)) + v * math.cos(math.radians(arm_ang)))
    rounded_rect(sk, tm, -12.5, -12.5, arm_len + 12.5, 12.5, 6.0)
    b = extrude(comp, all_profiles(sk), 4.0, "new", along=plane_normal_sign(comp, "y")).bodies.item(0)
    pts8 = [tm(0.0, 0.0), tm(arm_len, 0.0)]
    holes(comp, b, "y", arm_y0, [(p[0], p[2]) for p in pts8], 8.5, 4.0 + 1.0, +1)
    pm = tm(0.6 * arm_len, 0.0)
    holes(comp, b, "y", arm_y0, [(pm[0], pm[2])], 5.2, 4.0 + 1.0, +1)                                             # spring post hole
    ax_y1 = N["ax_y1"]
    comp = new_comp("hardware-idler-axle (bought, M8 x 30 bolt, nut)")
    b = tube_body(comp, "y", (ix, iz), 8.0, 0.0, arm_y0, ax_y1 - arm_y0)
    prism(comp, "y", arm_y0, -5.0, hex_pts(ix, iz, 13.0), op="join", body=b)
    prism(comp, "y", ax_y1 - 5.0, 5.0, hex_pts(ix, iz, 13.0), op="join", body=b)
    comp = new_comp("idler-bracket (angle 40x40x3, cut to length)")
    b = angle_x_body(comp, -140.0, -90.0, arm_y0, -1, 0.0, +1, A_L=40.0, A_T=3.0)
    thru(comp, b, "y", [tuple(piv)], 8.5, arm_y0 - 3.0, arm_y0)
    holes(comp, b, "z", 0.0, [tuple(p) for p in N["bracket_pts"][:2]], P["m6_hole"], 3.0 + 1.0, +1)
    comp = new_comp("hardware-idler-pivot (bought, M8 x 25 bolt, nut)")
    b = tube_body(comp, "y", (piv[0], piv[1]), 8.0, 0.0, arm_y0 - 8.0, 18.0)
    prism(comp, "y", arm_y0 - 3.0, -5.0, hex_pts(piv[0], piv[1], 13.0), op="join", body=b)
    prism(comp, "y", arm_y0 + 4.0, 5.0, hex_pts(piv[0], piv[1], 13.0), op="join", body=b)
    comp = new_comp("spring-bracket (angle 40x40x3, cut to length)")
    b = angle_x_body(comp, anchor[0] - 20.0, anchor[0] + 20.0, arm_y0, -1, 0.0, +1, A_L=40.0, A_T=3.0)
    holes(comp, b, "z", 0.0, [tuple(p) for p in N["bracket_pts"][2:]], P["m6_hole"], 3.0 + 1.0, +1)
    thru(comp, b, "y", [tuple(anchor)], 5.2, arm_y0 - 3.0, arm_y0)
    a_mid, post_y1 = N["a_mid"], N["post_y1"]
    comp = new_comp("hardware-idler-spring-posts (bought, 2 x M5 shoulder posts)")
    tube_body(comp, "y", (a_mid[0], a_mid[1]), 5.0, 0.0, arm_y0 - 3.0, post_y1 - arm_y0 + 3.0)
    tube_body(comp, "y", (anchor[0], anchor[1]), 5.0, 0.0, arm_y0 - 6.0, post_y1 - arm_y0 + 6.0)
    # the spring along u_sp from the arm's post to the anchor's: drawn about the origin on planes normal to that
    # direction (a Move cannot turn a body about the component's own axis), then moved to its start
    u_sp, sp_free, hook, post_r, sp_y = N["u_sp"], N["sp_free"], N["hook"], N["post_r"], N["sp_y"]
    theta = math.degrees(math.atan2(u_sp[2], u_sp[0]))
    comp = new_comp("idler-spring (bought, extension spring)")
    b = cyl_along(comp, theta, 4.0, hook, sp_free - hook)                                                           # coil body between the hooks
    for t0 in (0.0, sp_free - hook):
        cyl_along(comp, theta, 0.9, t0, t0 + hook, op="join", body=b)                                               # the hooks, as thin wire
    start = (a_mid[0] + u_sp[0] * post_r, sp_y, a_mid[1] + u_sp[2] * post_r)
    move(comp, comp_bodies(comp), start[0], start[1], start[2])


def build_studs(N):
    """The roller studs: shoulder screw, shim, spacer, washer and nut at each of the four rollers."""
    SH, THR, SP, rw = N["SH"], N["THR"], N["SP"], N["roller_w"]
    comp = new_comp("hardware-roller-studs (bought, 4 x ISO 7379 shoulder screws 10 x 35 M8, 1.0 shims, spacers 16 x 10.5 x 8.5, M8 washers and nuts)")
    for (x, z, d) in N["rollers"]:
        for end, sgn, bulk_face in (("front", 1.0, P["front_bulk_y"] + P["t_bulk"]), ("rear", -1.0, P["rear_bulk_y"])):
            ry0 = N["roller_y"][end]
            head_face = bulk_face + sgn * SH
            hd, hh = P["roller_stud_head_d"], P["roller_stud_head_h"]
            s = tube_body(comp, "y", (x, z), hd, 0.0, head_face, sgn * hh)                                         # head
            chamfer_where(comp, s, circle_edge_pred(hd / 2, "y", head_face + sgn * hh), 0.8)
            prism(comp, "y", head_face + sgn * (hh - 3.5), sgn * 4.0, hex_pts(x, z, 5.0), op="cut", body=s)        # socket
            tube_body(comp, "y", (x, z), 10.0, 0.0, head_face - sgn * SH, sgn * (SH + 0.5), op="join", body=s)     # shoulder
            tube_body(comp, "y", (x, z), 8.0, 0.0, head_face - sgn * (SH + THR), sgn * (THR + 0.5), op="join", body=s)   # thread
            chamfer_where(comp, s, circle_edge_pred(4.0, "y", head_face - sgn * (SH + THR)), 0.6)
            shim_y = ry0 + rw if sgn > 0 else ry0 - 1.0
            tube_body(comp, "y", (x, z), 16.0, 10.5, shim_y, 1.0)                                                  # shim
            spc_y = bulk_face if sgn > 0 else bulk_face - SP
            tube_body(comp, "y", (x, z), 16.0, 10.5, spc_y, SP)                                                    # spacer
            far = bulk_face - sgn * P["t_bulk"]
            tube_body(comp, "y", (x, z), 16.0, 8.4, far, -sgn * 1.6)                                               # washer
            nut_body(comp, (x, far - sgn * 1.6, z), (0.0, -sgn, 0.0), 13.0, 6.5, 8.2)


def ring_cut(comp, body, axis, at, c, d_out, d_in, depth, into):
    """An annular cut (a groove) from the plane normal to axis at `at`."""
    pl = offset_plane(comp, axis, at)
    sk = comp.sketches.add(pl)
    p = {"x": (at, c[0], c[1]), "y": (c[0], at, c[1]), "z": (c[0], c[1], at)}[axis]
    circle(sk, *p, d_out)
    circle(sk, *p, d_in)
    q = {"x": (at, c[0] + (d_out + d_in) / 4.0, c[1]), "y": (c[0] + (d_out + d_in) / 4.0, at, c[1]), "z": (c[0] + (d_out + d_in) / 4.0, c[1], at)}[axis]
    prof = profile_at(sk, sk_pt(sk, *q))
    return extrude(comp, prof, depth, "cut", along=into * plane_normal_sign(comp, axis), bodies=[body])


def build_heat_module(N):
    """The electric heat module's angles, element, collar, thermostats, terminal angle, DIN rail and devices."""
    A_L, A_T = N["A_L"], N["A_T"]
    tz1, bx, by0, by1, td, bz1, wz1 = N["tz1"], N["bx"], N["by0"], N["by1"], N["td"], N["bz1"], N["wz1"]
    HM_BY, HM_BX, Z_BOT, Z_TOP, Z_CNR = N["HM_BY"], N["HM_BX"], N["Z_BOT"], N["Z_TOP"], N["Z_CNR"]
    e, es = N["e"], N["es"]
    comp_b = new_comp("heat-module-angles-bottom (20x20x2 aluminium angle, 2 x 205 outside, 2 x 283 inside)")
    comp_t = new_comp("heat-module-angles-top (20x20x2 aluminium angle, 2 x 165, 2 x 290)")
    comp_c = new_comp("heat-module-angles-corner (20x20x2 aluminium angle, 4 x 72)")
    comp_r = new_comp("heat-module-element-rails (20x20x2 aluminium angle, 2 x 198)")
    for sx in (-1, 1):
        xo = sx * bx                                                                  # the side wall's outer face
        a = angle_y_body(comp_b, by0, by1, xo, sx, tz1, +1)                           # outside bottom angle
        xr = sorted((xo, xo + sx * A_L))
        thru(comp_b, a, "x", [(yy, Z_BOT) for yy in HM_BY], 4.5, xr[0], xr[1])
        thru(comp_b, a, "z", [(sx * 160.0, yy) for yy in HM_BY], 4.5, tz1, tz1 + A_L)
        a = angle_y_body(comp_t, by0 + A_L, by1 - A_L, xo + sx * A_T, -sx, bz1 + A_T, -1)   # outside top angle, from its outer top corner
        xr = sorted((xo + sx * A_T, xo + sx * A_T - sx * A_L))
        thru(comp_t, a, "x", [(yy, Z_TOP) for yy in HM_BY], 4.5, xr[0], xr[1])
        thru(comp_t, a, "z", [(sx * (bx - A_L / 2), yy) for yy in HM_BY], 4.5, bz1 + A_T - A_L, bz1 + A_T)
        r_ = angle_y_body(comp_r, by0 + td + A_T, by1 - td - A_T, xo - sx * td, -sx, tz1 + A_L, -1)   # element rail inside the wall
        xr = sorted((xo - sx * td, xo - sx * td - sx * A_L))
        thru(comp_r, r_, "x", [(yy, Z_BOT) for yy in HM_BY], 4.5, xr[0], xr[1])
        for (yo, sy) in ((by0, -1), (by1, +1)):                                      # corner angles
            a = angle_z_body(comp_c, tz1 + A_L, bz1 + A_T - A_L, xo + sx * A_T, -sx, yo + sy * A_T, -sy)
            xr = sorted((xo + sx * A_T, xo + sx * A_T - sx * A_L))
            yr = sorted((yo + sy * A_T, yo + sy * A_T - sy * A_L))
            thru(comp_c, a, "x", [(yo - sy * A_L / 2, Z_CNR)], 4.5, xr[0], xr[1])
            thru(comp_c, a, "y", [(sx * (bx - A_L / 2), Z_CNR)], 4.5, yr[0], yr[1])
    for (yo, sy) in ((by0, -1), (by1, +1)):
        a = angle_x_body(comp_b, -bx + td + A_T, bx - td - A_T, yo - sy * td, -sy, tz1, +1)   # inside bottom angle
        yr = sorted((yo - sy * td, yo - sy * td - sy * A_L))
        thru(comp_b, a, "y", [(x, Z_BOT) for x in HM_BX], 4.5, yr[0], yr[1])
        thru(comp_b, a, "z", [(x, yo - sy * (td + A_L / 2)) for x in HM_BX], 4.5, tz1, tz1 + A_L)
        a = angle_x_body(comp_t, -bx, bx, yo + sy * A_T, -sy, bz1 + A_T, -1)                   # outside top angle on the end wall
        yr = sorted((yo + sy * A_T, yo + sy * A_T - sy * A_L))
        thru(comp_t, a, "y", [(x, Z_TOP) for x in HM_BX], 4.5, yr[0], yr[1])
        thru(comp_t, a, "z", [(x, yo - sy * A_L / 2) for x in HM_BX], 4.5, bz1 + A_T - A_L, bz1 + A_T)
    # the element and its terminals, the collar on the lid, the two thermostats
    el, ew, eh, ez0 = P["hm_elem_l"], P["hm_elem_w"], P["hm_elem_h"], P["hm_elem_z0"]
    ey0, tc = N["ey0"], N["tc"]
    comp = new_comp("heat-module-element (bought, 279838 class open-coil element on its frame, envelope)")
    b = box_body(comp, -el / 2, el / 2, ey0, ey0 + ew, ez0, ez0 + eh)
    box_body(comp, el / 2, bx + 12.0, tc[0] - 10.0, tc[0] + 10.0, tc[1] - 6.0, tc[1] + 6.0, op="join", body=b)
    cy, cd_, ch0 = N["cy"], N["cd_"], N["ch0"]
    comp = new_comp("heat-module-collar (bought, 125 flanged starting collar, cut to 55.5)")
    b = tube_body(comp, "z", (0.0, cy), cd_, cd_ - 1.2, ch0, P["hm_collar_top"] - ch0)
    tube_body(comp, "z", (0.0, cy), P["hm_collar_flange_d"], cd_ - 1.2, ch0, 1.0, op="join", body=b)
    holes(comp, b, "z", ch0 - 1.0, [(70.0, cy), (-70.0, cy), (0.0, cy + 70.0), (0.0, cy - 70.0)], 4.5, 4.0, +1)
    tx_, ty_ = N["tx_"], N["ty_"]
    comp = new_comp("heat-module-thermostats (bought, 279816 class high-limit and thermal cut-off, envelopes)")
    for sx in (-1, 1):
        t_ = box_body(comp, sx * tx_ - 7.0, sx * tx_ + 7.0, ty_ - 27.0, ty_ + 27.0, bz1, bz1 + 2.0)                      # bracket
        box_body(comp, sx * tx_ - 11.0, sx * tx_ + 11.0, ty_ - 11.0, ty_ + 11.0, bz1 + 2.0, bz1 + 15.0, op="join", body=t_)   # disc body
        holes(comp, t_, "z", bz1 - 1.0, [(sx * tx_, ty_ + k) for k in (-20.0, 20.0)], 4.5, 5.0, +1)
    # the terminal plate's angle foot, the DIN rail on the plate's rear face, the devices
    py_, ph_ = P["hm_plate_y"], P["hm_plate_h"]
    comp = new_comp("heat-module-terminal-angle (20x20x2 aluminium angle, 290)")
    a = angle_x_body(comp, -bx, bx, py_ + 1.5, +1, tz1, +1)
    thru(comp, a, "y", [(x, Z_BOT) for x in (-120.0, 0.0, 120.0)], 4.5, py_ + 1.5, py_ + 1.5 + A_L)
    thru(comp, a, "z", [(x, py_ + 1.5 + A_L / 2) for x in HM_BX], 4.5, tz1, tz1 + A_L)
    RAIL_ZC, hm_rail_y = N["RAIL_ZC"], N["hm_rail_y"]
    comp = new_comp("heat-module-din-rail (bought, 35 x 7.5 top hat, 280)")
    b = din_rail_body(comp, -140.0, 140.0, hm_rail_y, RAIL_ZC)
    holes(comp, b, "y", hm_rail_y - 1.0, [(x, RAIL_ZC) for x in (-120.0, 120.0)], 6.3, 4.0, +1)
    comp = new_comp("heat-module-devices (bought, envelopes: 2 end clamps, X_HM mains and SELV strips, partition, K_HEAT, CS1)")
    din_devices_bodies(comp, N["HM_DEVICES"], -140.0, hm_rail_y, RAIL_ZC)
    comp = new_comp("heat-module-bonding-stud (bought, M6 x 16 hex bolt, 2 nuts, star washers; the PE ring terminal goes between the nuts)")
    hex_bolt_m6(comp, (140.0, 680.0, e + es), (0.0, 0.0, -1.0), 16.0)
    nut_body(comp, (140.0, 680.0, tz1), (0.0, 0.0, 1.0), P["m6_nut_af"], P["m6_nut_h"], 6.2)
    nut_body(comp, (140.0, 680.0, tz1 + 5.0 + 2.0), (0.0, 0.0, 1.0), P["m6_nut_af"], P["m6_nut_h"], 6.2)


def din_rail_body(comp, x0, x1, y_face, zc):
    """The script's 35 x 7.5 top-hat rail along X with its web on a plate's face at y_face: web, two sides, two brims."""
    b = box_body(comp, x0, x1, y_face, y_face + 1.0, zc - 12.5, zc + 12.5)
    for (z0_, z1_) in ((zc - 13.5, zc - 12.5), (zc + 12.5, zc + 13.5)):
        box_body(comp, x0, x1, y_face, y_face + 7.5, z0_, z1_, op="join", body=b)
    for (z0_, z1_) in ((zc - 17.5, zc - 13.5), (zc + 13.5, zc + 17.5)):
        box_body(comp, x0, x1, y_face + 6.5, y_face + 7.5, z0_, z1_, op="join", body=b)
    return b


def din_devices_bodies(comp, items, x0, y_face, zc):
    """Device envelopes clipped on a rail from x0 rightward: (label, width, height across the rail, depth off the plate)."""
    x = x0
    for (label, w, h, d) in items:
        box_body(comp, x, x + w, y_face + 7.5, y_face + 7.5 + d, zc - h / 2, zc + h / 2)
        x += w


def build_power_module(N):
    """The common power module's rails, devices, barrier angle, standoffs and ground stud; the grommets, cord bushing and cord."""
    A_L, A_T, tp = N["A_L"], N["A_T"], N["tp"]
    PM_X0, PM_W, PM_Y, pm_face = N["PM_X0"], N["PM_W"], N["PM_Y"], N["pm_face"]
    pm_rail_x, pm_bolt_x, so_pts, pxc = N["pm_rail_x"], N["pm_bolt_x"], N["so_pts"], N["pxc"]
    comp_r = new_comp("power-module-din-rails (bought, 5 x 35 x 7.5 top hat, 140)")
    for rail_name, zc in zip(("A1", "A2", "A3", "B1", "B2"), P["pm_rails_z"]):
        b = din_rail_body(comp_r, pm_rail_x[0], pm_rail_x[1], pm_face, zc)
        holes(comp_r, b, "y", pm_face - 1.0, [(x, zc) for x in pm_bolt_x], 6.3, 4.0, +1)
        devs = N["PM_DEVICES"][rail_name]
        comp = new_comp(f"power-module-rail-{rail_name}-devices (bought, envelopes: " + ", ".join(lbl for (lbl, _, _, _) in devs if lbl != "end clamp") + ", 2 end clamps)")
        din_devices_bodies(comp, devs, pm_rail_x[0], pm_face, zc)
    bz_ = N["bz_"]
    comp = new_comp("power-module-barrier-angle (20x20x2 aluminium angle, 150)")
    ba = angle_x_body(comp, PM_X0, PM_X0 + PM_W, pm_face, +1, bz_, +1)
    thru(comp, ba, "y", [(x, bz_ + A_L / 2) for x in (pxc - 45.0, pxc + 45.0)], 4.5, pm_face, pm_face + A_L)
    thru(comp, ba, "z", [(x, pm_face + A_L / 2) for x in (pxc - 45.0, pxc + 45.0)], 4.5, bz_, bz_ + A_L)
    so_len = N["so_len"]
    comp = new_comp("power-module-standoffs (bought, 4 x M4 x 75 hex standoffs, female both ends)")
    for (x, z) in so_pts:
        s = prism(comp, "y", pm_face, so_len, hex_pts(x, z, 7.0))
        holes(comp, s, "y", pm_face - 1.0, [(x, z)], 4.2, 10.0, +1)                      # M4 bores 9 deep, both ends
        holes(comp, s, "y", pm_face + so_len + 1.0, [(x, z)], 4.2, 10.0, -1)
    gs = N["gs"]
    comp = new_comp("power-module-ground-stud (bought, M6 x 16 hex bolt, 2 nuts, star washers; the cord's PE ring terminal goes between the nuts)")
    hex_bolt_m6(comp, (gs[0], PM_Y, gs[1]), (0.0, -1.0, 0.0), 16.0)
    nut_body(comp, (gs[0], pm_face, gs[1]), (0.0, 1.0, 0.0), P["m6_nut_af"], P["m6_nut_h"], 6.2)
    nut_body(comp, (gs[0], pm_face + 7.0, gs[1]), (0.0, 1.0, 0.0), P["m6_nut_af"], P["m6_nut_h"], 6.2)
    # grommets: rubber, straddling the 1.5 mm plate: a neck in the hole, a flange either side
    comp = new_comp("grommets (bought, 5 x rubber grommets for 1.5 panels: 22 mm hole x 2, 30 mm hole x 1, 16 mm hole x 2)")
    bt, Hb = N["bt"], N["Hb"]
    for (gx, gy, gd), gz in ((P["grommet_cord"], bt + tp / 2), (P["grommet_harness"], bt + tp / 2), (P["grommet_console"], Hb + tp / 2), (P["ds_grommet_ceil"], bt + tp / 2)):
        grommet_body(comp, "z", (gx, gy), gz, gd, tp)
    gx, gz, gd = P["ds_grommet_bulk"]
    grommet_body(comp, "y", (gx, gz), P["front_bulk_y"] + N["tb"] / 2, gd, tp)
    # the cord's strain relief bushing through the base pan, and the cord
    cx, cyy, tbase = N["cx"], N["cyy"], P["t_base"]
    comp = new_comp("cord-bushing (bought, PG16 strain relief)")
    b = prism(comp, "z", 0.0, 8.0, hex_pts(cx, cyy, 24.0))
    dome = tube_body(comp, "z", (cx, cyy), 20.0, 0.0, 8.0, 10.0)
    fillet_where(comp, dome, circle_edge_pred(10.0, "z", 18.0), 3.0)
    combine_join(comp, b, [dome])
    tube_body(comp, "z", (cx, cyy), 21.8, 0.0, -tbase - 5.0, tbase + 5.5, op="join", body=b)                        # thread through the pan
    prism(comp, "z", -tbase - 5.0, 5.0, hex_pts(cx, cyy, 26.0), op="join", body=b)                                  # locknut under the pan
    holes(comp, b, "z", -20.0, [(cx, cyy)], 9.2, 40.0, +1)                                                          # the cord passes through
    cord_z = N["cord_z"]
    comp = new_comp("power-cord (bought)")
    b = tube_body(comp, "z", (cx, cyy), 9.0, 0.0, cord_z, P["cord_top_z"] - cord_z)                                 # up to X1
    tube_body(comp, "y", (cx, cord_z), 9.0, 0.0, cyy, N["D"] + 70.0 - cyy, op="join", body=b)                       # back under the pan
    ball(comp, (cx, cyy, cord_z), 4.5, body=b)


def grommet_body(comp, axis, c, a_mid, gd, tp):
    """A grommet about the axis with the plate's mid-plane at a_mid: neck (gd - 0.2 over gd - 7) through the plate, a
    1.25 flange (gd + 6 over gd - 7) either side."""
    b = tube_body(comp, axis, c, gd - 0.2, gd - 7.0, a_mid - tp / 2, tp)
    for a0 in (a_mid - tp / 2 - 1.25, a_mid + tp / 2):
        tube_body(comp, axis, c, gd + 6.0, gd - 7.0, a0, 1.25, op="join", body=b)
    return b


def build_sensors(N):
    """PS1 and its bracket, the exhaust thermostats, TH1, the moisture bars, the second entry blank, the cable clamps."""
    A_L, A_T, tp = N["A_L"], N["A_T"], N["tp"]
    px_, py_ = N["px_"], N["py_"]
    comp = new_comp("ps1-bracket (angle 20x20x2, 60)")
    b = angle_x_body(comp, px_ - 30.0, px_ + 30.0, py_ + 10.0, -1, 0.0, +1)
    holes(comp, b, "z", -1.0, [tuple(p) for p in N["ps1_pts"]], P["m6_hole"], A_T + 2.0, +1)
    thru(comp, b, "y", [(px_ - 15.0, 12.0), (px_ + 15.0, 12.0)], 4.5, py_ + 10.0 - A_T, py_ + 10.0)
    comp = new_comp("ps1-air-proving-switch (bought, envelope)")
    b = box_body(comp, px_ - 30.0, px_ + 30.0, py_ + 10.0, py_ + 38.0, 0.0, 60.0)
    tapped(comp, b, "y", py_ + 10.0, [(px_ - 15.0, 12.0), (px_ + 15.0, 12.0)], 8.0, +1)
    oz = N["oz"]
    comp = new_comp("exhaust-thermostats (bought, TF2 thermal fuse, T_HI and T_LO cycling thermostats, envelopes on the blower outlet)")
    for x in P["tf_x"]:
        t_ = box_body(comp, x - 7.0, x + 7.0, 123.0, 177.0, oz, oz + 2.0)
        box_body(comp, x - 11.0, x + 11.0, 139.0, 161.0, oz + 2.0, oz + 15.0, op="join", body=t_)
        holes(comp, t_, "z", oz - 1.0, [(x, yy) for yy in (130.0, 170.0)], 4.5, 5.0, +1)
    TB_W, TB_D, TB_H = P["th1_body"]
    TH1_NW, TH1_ND, TH1_NH = P["th1_nib"]
    TH1_X, TH1_Z, th1_y0 = N["TH1_X"], N["TH1_Z"], N["th1_y0"]
    comp = new_comp("th1-exhaust-thermistor (bought, 10 k NTC appliance thermistor, envelope)")
    b = box_body(comp, TH1_X - TB_W / 2, TH1_X + TB_W / 2, th1_y0, th1_y0 + TB_D, TH1_Z - TB_H / 2, TH1_Z + TB_H / 2)
    box_body(comp, TH1_X - TH1_NW / 2, TH1_X + TH1_NW / 2, th1_y0 - TH1_ND, th1_y0, TH1_Z + P["th1_nib_dz"] - TH1_NH / 2, TH1_Z + P["th1_nib_dz"] + TH1_NH / 2, op="join", body=b)
    thru(comp, b, "y", [(TH1_X, TH1_Z + P["th1_bolt_dz"])], 4.5, th1_y0 - TH1_ND, th1_y0 + TB_D)
    box_body(comp, TH1_X - 4.0, TH1_X + 4.0, th1_y0 + TB_D, th1_y0 + TB_D + 8.0, TH1_Z - 12.0, TH1_Z + 4.0, op="join", body=b)   # spade terminals
    # the moisture bar set on the front bulkhead's drum side, along the tangent at 58 degrees right of bottom
    MS_L, MS_W, MS_T_ = P["ms_len"], P["ms_w"], P["ms_t"]
    ms_y0, MS_C, ang = N["ms_y0"], N["MS_C"], -P["ms_angle_deg"]
    R = lambda x, z: (MS_C[0] + rot_y_pt(x, z, ang)[0], MS_C[1] + rot_y_pt(x, z, ang)[1])
    comp = new_comp("moisture-bars (bought, dryer moisture sensor bar set, two stainless strips on an insulating base, envelope)")
    b = prism(comp, "y", ms_y0, MS_T_, [R(-MS_L / 2, -MS_W / 2), R(MS_L / 2, -MS_W / 2), R(MS_L / 2, MS_W / 2), R(-MS_L / 2, MS_W / 2)])
    holes(comp, b, "y", ms_y0 - 1.0, [tuple(p) for p in N["MS_PTS"]], 4.5, MS_T_ + 2.0, +1)
    prism(comp, "y", ms_y0 - 1.0, 3.0, [R(-8.0, -9.0), R(8.0, -9.0), R(8.0, 9.0), R(-8.0, 9.0)], op="cut", body=b)    # the terminals' recess
    # the second entry blank: the entry-blank plate again, on the condensate drain
    pl0 = [pl for pl in PLATES["plates"] if pl["name"] == "entry-blank"][0]
    (x1_, z1_, _), (x2_, z2_, _) = N["ENTRIES"]
    dx, dz = x2_ - x1_, z2_ - z1_
    pl2 = json.loads(json.dumps(pl0))
    pl2["name"] = "entry-blank-2 (the second entry-blank, cut two to drawings/entry-blank.dxf; on the condensate drain)"
    pl2["u0"], pl2["u1"], pl2["v0"], pl2["v1"] = pl0["u0"] + dx, pl0["u1"] + dx, pl0["v0"] + dz, pl0["v1"] + dz
    for k in ("u0", "u1", "v0", "v1"):
        pl2["ex"][k] = None
    pl2["holes"] = [[h[0] + dx, h[1] + dz, h[2], None, None] for h in pl0["holes"]]
    build_plate(pl2)
    # the cable clamps: a tab with its hole and a loop for the 12 mm bundle
    comp = new_comp("cable-clamps (bought, 4 x nylon P-clip for a 12 mm bundle, envelopes)")
    for (x, y) in P["clamp_pts"]:
        tab = box_body(comp, x - 8.0, x + 8.0, y - 5.0, y + 5.0, 0.0, 1.5)
        holes(comp, tab, "z", -1.0, [(x, y)], 4.5, 4.0, +1)
        tube_body(comp, "y", (x + 15.0, 7.5), 15.0, 12.0, y - 5.0, 10.0)


def build_feet_brackets(N):
    """The leveling feet, the tray rails' corner brackets and the console sub-frame's corner brackets."""
    e, D, tbase = N["e"], N["D"], P["t_base"]
    ph, hh_ = P["foot_pad_h"], P["foot_hex_h"]
    comp = new_comp("feet (bought, 4 x M8 leveling feet, 50 pad)")
    for (fx, fy) in N["foot_pts"]:
        z0 = -(ph + hh_ + tbase)
        f_ = tube_body(comp, "z", (fx, fy), P["foot_pad_d"], 0.0, z0, ph)                                        # pad
        fillet_where(comp, f_, circle_edge_pred(P["foot_pad_d"] / 2, "z", z0), 2.0)
        prism(comp, "z", z0 + ph, hh_, hex_pts(fx, fy, P["foot_hex_af"]), op="join", body=f_)                      # hex
        tube_body(comp, "z", (fx, fy), P["foot_stud_d"], 0.0, z0 + ph + hh_ - 0.5, tbase + 0.5, op="join", body=f_)   # stud through the pan
        tube_body(comp, "z", (fx, fy), P["tslot_4040"]["bore"] - 0.2, 0.0, z0 + ph + hh_ + tbase - 0.5, P["foot_stud_in"] + 0.5, op="join", body=f_)   # into the post's bore
    B20L, B20T, B20W, es = N["B20L"], N["B20T"], N["B20W"], N["es"]
    comp = new_comp("tray-rail-brackets (bought, 4 x 2020 inside corner brackets)")
    for (x0, x1) in N["TRAY_RAIL_X"]:
        sx = -1 if x0 < 0 else 1
        xf = x0 if sx < 0 else x1
        for yc in (e / 2, D - e / 2):
            b = box_body(comp, min(xf, xf + sx * B20T), max(xf, xf + sx * B20T), yc - B20W / 2, yc + B20W / 2, e, e + B20L)
            box_body(comp, min(xf, xf + sx * B20L), max(xf, xf + sx * B20L), yc - B20W / 2, yc + B20W / 2, e, e + B20T, op="join", body=b)
            thru(comp, b, "x", [(yc, e + es / 2)], 4.5, min(xf, xf + sx * B20T), max(xf, xf + sx * B20T))
            thru(comp, b, "z", [(xf + sx * (B20L - 8.0), yc)], 4.5, e, e + B20T)
    BRK_L, BRK_T, BRK_W, hw = N["BRK_L"], N["BRK_T"], N["BRK_W"], N["hw"]
    con_y0, con_z0, con_z1 = N["con_y0"], N["con_z0"], N["con_z1"]
    comp = new_comp("console-brackets (bought, 12 x 4040 inside corner brackets)")

    def corner_bracket(face, d, c_along, z_corner, up, axis):
        a0, a1 = sorted((face, face + d * BRK_T))
        b0, b1 = sorted((face, face + d * BRK_L))
        za0, za1 = sorted((z_corner, z_corner + up * BRK_L))
        zb0, zb1 = sorted((z_corner, z_corner + up * BRK_T))
        if axis == "x":
            b = box_body(comp, a0, a1, c_along - BRK_W / 2, c_along + BRK_W / 2, za0, za1)
            box_body(comp, b0, b1, c_along - BRK_W / 2, c_along + BRK_W / 2, zb0, zb1, op="join", body=b)
            thru(comp, b, "x", [(c_along, z_corner + up * (BRK_L - 12.0))], P["m6_hole"], a0, a1)
            thru(comp, b, "z", [(face + d * (BRK_L - 12.0), c_along)], P["m6_hole"], zb0, zb1)
        else:
            b = box_body(comp, c_along - BRK_W / 2, c_along + BRK_W / 2, a0, a1, za0, za1)
            box_body(comp, c_along - BRK_W / 2, c_along + BRK_W / 2, b0, b1, zb0, zb1, op="join", body=b)
            thru(comp, b, "y", [(c_along, z_corner + up * (BRK_L - 12.0))], P["m6_hole"], a0, a1)
            thru(comp, b, "z", [(c_along, face + d * (BRK_L - 12.0))], P["m6_hole"], zb0, zb1)
        return b

    def corner_bracket_v(x_face, dx, y_face, dy, zc):
        xa = sorted((x_face, x_face + dx * BRK_T))
        ya = sorted((y_face, y_face + dy * BRK_L))
        xb = sorted((x_face, x_face + dx * BRK_L))
        yb = sorted((y_face, y_face + dy * BRK_T))
        b = box_body(comp, xa[0], xa[1], ya[0], ya[1], zc - BRK_W / 2, zc + BRK_W / 2)
        box_body(comp, xb[0], xb[1], yb[0], yb[1], zc - BRK_W / 2, zc + BRK_W / 2, op="join", body=b)
        thru(comp, b, "x", [(y_face + dy * (BRK_L - 12.0), zc)], P["m6_hole"], xa[0], xa[1])
        thru(comp, b, "y", [(x_face + dx * (BRK_L - 12.0), zc)], P["m6_hole"], yb[0], yb[1])
        return b

    for sx in (-1, 1):
        xi = sx * (hw - e)
        for (yy0, yy1) in N["up_y"]:
            yc = (yy0 + yy1) / 2
            corner_bracket(xi, -sx, yc, con_z0, +1, "x")
            zt = con_z1 - e
            corner_bracket(xi, -sx, yc, zt, -1, "x")
        yf, xc = con_y0 + e, sx * (hw - e / 2)
        corner_bracket(yf, +1, xc, zt, -1, "y")
        corner_bracket_v(xi, -sx, D - e, -1, con_z1 - e / 2)


def drop(*prefixes):
    """Delete every top-level component whose name starts with one of the prefixes (to rebuild a group)."""
    n = 0
    for o in list(_root.occurrences):
        if any(o.component.name.startswith(p_) for p_ in prefixes):
            o.deleteMe()
            n += 1
    return n


def stage_e():
    app, design, root = app_design()
    N = numbers()
    done = []
    for nm, fn in (("door", build_door), ("tier0", build_tier0), ("drive", build_drive), ("belt", build_belt), ("idler", build_idler),
                   ("roller studs", build_studs), ("heat module", build_heat_module), ("power module", build_power_module),
                   ("sensors", build_sensors), ("feet and brackets", build_feet_brackets)):
        try:
            fn(N)
            done.append(nm)
        except Exception:
            done.append(nm + " FAILED: " + traceback.format_exc().splitlines()[-1])
    return "stage E: " + "; ".join(done)



# ---------------------------------------------------------------------------
# Stage F: the hardware. Every bolt, nut, washer and spacer the script places (mechanical/cad/hardware.json: what it
# is, its bearing point, its normal) is built as a fixed body with Fusion's temporary BRep tools (cylinders, cones, a
# torus for a button head's round, hexagonal prisms as three slabs intersected, six cuts for a hex head's chamfer) and
# added to its part's component in one base feature: bought stock at the script's positions, not driven by the
# parameters (a parameter change moves the holes; running this stage again redraws the hardware on them).
# ---------------------------------------------------------------------------
_tmp = None


def tmp():
    global _tmp
    if _tmp is None:
        _tmp = adsk.fusion.TemporaryBRepManager.get()
    return _tmp


def t_pt(x, y, z):
    return adsk.core.Point3D.create(x * CM, y * CM, z * CM)


def t_vec(x, y, z):
    return adsk.core.Vector3D.create(x, y, z)


def t_cyl(r, z0, z1, r1=None):
    """A cylinder about +Z from z0 to z1, or a cone frustum with radius r at z0 and r1 at z1."""
    return tmp().createCylinderOrCone(t_pt(0, 0, z0), r * CM, t_pt(0, 0, z1), (r if r1 is None else r1) * CM)


def t_box(cx, cy, cz, lx, ly, lz, angle_deg=0.0):
    """A box centred at (cx, cy, cz), lx along X turned by the angle about Z, ly across, lz up."""
    a = math.radians(angle_deg)
    obb = adsk.core.OrientedBoundingBox3D.create(t_pt(cx, cy, cz), t_vec(math.cos(a), math.sin(a), 0.0), t_vec(-math.sin(a), math.cos(a), 0.0), lx * CM, ly * CM, lz * CM)
    return tmp().createBox(obb)


def t_union(a, b):
    tmp().booleanOperation(a, b, adsk.fusion.BooleanTypes.UnionBooleanType)
    return a


def t_cut(a, b):
    tmp().booleanOperation(a, b, adsk.fusion.BooleanTypes.DifferenceBooleanType)
    return a


def t_hex(af, z0, z1):
    """A hexagonal prism about +Z, across the flats af, corners on the X axis (CadQuery's polygon): three slabs."""
    R = af / math.cos(math.radians(30))
    b = t_box(0.0, 0.0, (z0 + z1) / 2, 2 * R, af, z1 - z0, 0.0)
    for ang in (60.0, 120.0):
        tmp().booleanOperation(b, t_box(0.0, 0.0, (z0 + z1) / 2, 2 * R, af, z1 - z0, ang), adsk.fusion.BooleanTypes.IntersectionBooleanType)
    return b


def t_chamfer_hex_top(body, af, z_top, d):
    """Chamfer the six top edges of a hexagonal prism about +Z by d (equal distances): a 45 degree cut along each flat."""
    R = af / math.cos(math.radians(30))
    for k in range(6):
        phi = math.radians(30.0 + 60.0 * k)                      # the flat's outward normal
        rx, ry = math.cos(phi), math.sin(phi)
        nx, ny, nz = rx / math.sqrt(2), ry / math.sqrt(2), 1 / math.sqrt(2)   # the chamfer plane's normal, outward
        H = 4.0 * d
        c = (af / 2 * rx + nx * (H / 2 - d / math.sqrt(2)), af / 2 * ry + ny * (H / 2 - d / math.sqrt(2)), z_top + nz * (H / 2 - d / math.sqrt(2)))
        obb = adsk.core.OrientedBoundingBox3D.create(t_pt(*c), t_vec(-ry, rx, 0.0), t_vec(rx / math.sqrt(2), ry / math.sqrt(2), -1 / math.sqrt(2)), 2 * R * CM, 4.0 * d * CM, H * CM)
        t_cut(body, tmp().createBox(obb))
    return body


def t_button(d, head_d, head_h, length, socket_af):
    """The script's button head bolt along +Z, bearing face at z 0: the head's top edge rounded by 0.8 head_h (a torus
    and two cylinders), the hex socket, the shank with its 0.4 tip chamfer."""
    rh, f = head_d / 2, head_h * 0.8
    b = t_cyl(rh - f, 0.0, head_h)
    t_union(b, t_cyl(rh, 0.0, head_h - f))
    tor = tmp().createTorus(t_pt(0, 0, 0), t_vec(0, 0, 1), (rh - f) * CM, f * CM)
    m = adsk.core.Matrix3D.create()      # createTorus leaves its centre point unused (the torus comes out about the origin), so move it
    m.translation = adsk.core.Vector3D.create(0.0, 0.0, (head_h - f) * CM)
    tmp().transform(tor, m)
    tmp().booleanOperation(tor, t_cyl(rh + 1.0, head_h - f, head_h), adsk.fusion.BooleanTypes.IntersectionBooleanType)   # only the round's own band of the torus
    t_union(b, tor)
    t_cut(b, t_hex(socket_af, head_h - 1.2, head_h + 0.8))
    t_union(b, t_cyl(d / 2, -length + 0.4, 0.5))
    t_union(b, t_cyl(d / 2 - 0.4, -length, -length + 0.4, d / 2))
    return b


def t_hex_m6(L):
    wt, hh, af, wd = P["m6_washer_t"], P["m6_head_h"], P["m6_head_af"], P["m6_washer_d"]
    b = t_cyl(3.0, -L + 0.5, wt + 1.0)
    t_union(b, t_cyl(2.5, -L, -L + 0.5, 3.0))
    t_union(b, t_cyl(wd / 2, 0.0, wt))
    head = t_chamfer_hex_top(t_hex(af, wt, wt + hh), af, wt + hh, 0.6)
    t_union(b, head)
    return b


def t_csk(d, head_d, length):
    depth = (head_d - d) / 2
    b = t_cyl(d / 2, -length + 0.4, -depth + 0.5)
    t_union(b, t_cyl(d / 2 - 0.4, -length, -length + 0.4, d / 2))
    t_union(b, t_cyl(d / 2, -depth, 0.0, head_d / 2))
    return b


def t_nut(af, h, bore):
    b = t_hex(af, 0.0, h)
    t_cut(b, t_cyl(bore / 2, -1.0, h + 1.0))
    return b


def t_ring(od, idd, L):
    b = t_cyl(od / 2, 0.0, L)
    t_cut(b, t_cyl(idd / 2, -1.0, L + 1.0))
    return b


def t_place(body, p, n):
    """The script's place(): turn +Z to n (identity, 180 about X for -Z, else about (-ny, nx, 0) by acos nz), move to p."""
    m = adsk.core.Matrix3D.create()
    nx, ny, nz = n
    L = math.sqrt(nx * nx + ny * ny + nz * nz)
    nx, ny, nz = nx / L, ny / L, nz / L
    if nz < -1 + 1e-9:
        m.setToRotation(math.pi, t_vec(1, 0, 0), t_pt(0, 0, 0))
    elif nz < 1 - 1e-9:
        m.setToRotation(math.acos(nz), t_vec(-ny, nx, 0.0), t_pt(0, 0, 0))
    m.translation = adsk.core.Vector3D.create(p[0] * CM, p[1] * CM, p[2] * CM)
    tmp().transform(body, m)
    return body


def t_piece(kind):
    k = kind[0]
    if k == "button":
        return t_button(*kind[1:])
    if k == "hex_m6":
        return t_hex_m6(kind[1])
    if k == "csk":
        return t_csk(*kind[1:])
    if k == "nut":
        return t_nut(*kind[1:])
    if k == "ring":
        return t_ring(*kind[1:])
    raise ValueError("unknown stock %r" % (kind,))


def add_fixed_bodies(comp, bodies):
    """Add temporary bodies to a component as one base feature."""
    bf = comp.features.baseFeatures.add()
    bf.startEdit()
    for b in bodies:
        comp.bRepBodies.add(b, bf)
    bf.finishEdit()
    return bf


HW_BUILT_ELSEWHERE = ("hardware-roller-studs",)   # drawn with the drive in stage E


def stage_f(redo=False, only=None):
    """Build every hardware set; with redo, drop the built sets first; with only (name prefixes), just those sets."""
    app, design, root = app_design()
    HW = json.load(open(os.path.join(REPO, "mechanical", "cad", "hardware.json"), encoding="utf-8"))["hardware"]
    done, skipped, n_pieces = [], [], 0
    for name, pieces in HW.items():
        if any(name.startswith(h) for h in HW_BUILT_ELSEWHERE):
            continue
        if only is not None and not any(name.startswith(o) for o in only):
            continue
        if redo:
            drop(name)
        if any(pc is None for pc in pieces):
            skipped.append(name)
        bodies = []
        for pc in pieces:
            if pc is None:
                continue
            kind, p, n = pc
            bodies.append(t_place(t_piece(tuple(kind)), p, n))
        if not bodies:
            continue
        comp = new_comp(name)
        add_fixed_bodies(comp, bodies)
        done.append(name)
        n_pieces += len(bodies)
    return "stage F: %d hardware parts, %d pieces" % (len(done), n_pieces) + ("; pieces not stock in %s" % skipped if skipped else "")


# ---------------------------------------------------------------------------
# Stage G: joints, rigid groups and appearances from ../fusion_motion/fusion_motion.py (run in its own namespace: it
# names its point helper P), Fusion's interference analysis at the three poses, and the archive of record.
# ---------------------------------------------------------------------------
def stage_g(archive="osa-dryer-parametric.f3d", poses=True):
    app, design, root = app_design()
    ns = {"REPO": REPO, "__name__": "fusion_motion"}
    exec(open(os.path.join(REPO, "mechanical", "cad", "fusion_motion", "fusion_motion.py"), encoding="utf-8").read(), ns)
    out = [ns["build"](), ns["dress"]()]
    if poses:
        found = ns["check_poses"]()
        out.append("%d interferences over 3 poses" % len(found) + (": %s" % found[:5] if found else ""))
    path = os.path.join(REPO, "mechanical", "fusion", archive)
    out.append("archive " + ns["export_archive"](path))
    return "stage G: " + "; ".join(out)


def build_all():
    new_design()
    out = [stage_a(), stage_b(), stage_c(), stage_d(), stage_e(), stage_f(), stage_g()]
    return "\n".join(out)
