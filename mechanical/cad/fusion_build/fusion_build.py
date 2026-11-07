"""osa-dryer: the parametric Fusion build (see README.md beside this file).

Run inside Autodesk Fusion. From the Text Commands box (py mode):
    REPO=r"C:\\path\\to\\osa-dryer"; exec(open(REPO + r"\\mechanical\\cad\\fusion_build\\fusion_build.py").read()); print(build_all())
or one stage at a time: new_design(); stage_a(); ...

Draws every part of the dryer natively in a new design: user parameters, sketches with dimensions, extrudes, revolves,
cuts and patterns, one component per part, named as in the STEP the script writes, so fusion_audit.py can compare the
two. Every part is drawn about its own origin and placed by a Move feature whose X, Y and Z distances are expressions
in the user parameters, so the timeline stays readable (one sketch, one extrude, one move for a bar) and a parameter
change moves the part. Numbers come from the P table in osa_dryer_cad.py.

Draft 1, 2026-11-07: stages A (parameters, frame, tray rails) and B (the flat plates from plates.json).
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
    return "stage A: 4 posts, 17 rails, 2 tray rails"


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


def build_all():
    new_design()
    out = [stage_a(), stage_b(), stage_c()]
    return "\n".join(out)
