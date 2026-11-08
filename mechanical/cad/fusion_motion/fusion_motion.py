"""fusion_motion.py: give the dryer assembly its moving parts inside Autodesk Fusion, and its materials.

Run it on the imported assembly (mechanical/step/osa-dryer-assembly.step opened in Fusion, the active
design). It adds Fusion joints so the parts that move in the real machine move in the model, applies
appearances from Fusion's own library so every part reads as the material it is, can play the motion in
the viewport, run Fusion's interference analysis at several points of the motion, and export a Fusion
archive with the joints and appearances in it.

How to run it, in the Text Commands window (File > View > Show Text Commands, toggle Py), with the repo
folder in place of <repo>:
    REPO=r"<repo>"; exec(open(REPO + r"\\mechanical\\cad\\fusion_motion\\fusion_motion.py").read()); build()
then
    dress()                applies library appearances (stainless drum, enamel panels, anodized extrusions, rubber, felt...)
    animate(10)            plays ten seconds of motion: drum tumbling, pulley and idler spinning,
                           rollers rolling, door opening and closing, knobs turning, selector stepping,
                           START pressed, heat module tray sliding out and back
    check_poses()          runs Fusion's interference analysis at rest, half way and fully moved
    export_archive()       writes mechanical/fusion/osa-dryer-assembly-motion.f3d
    hide("side-panel-left", "top-panel", "door-"), show_all(), view("left")   for looking inside
Or from Scripts and Add-Ins: add the folder, run it; that does build(), dress(), animate(10), export_archive().

What moves and how (all as-built joints, so nothing is displaced when the joint is made):
    drum             revolute about the drum axis: sheet, rings, splice, baffles and their bolts in a rigid group
    pulley           revolute about the motor axis, against the motor (the blower housing is fixed; its wheel is not drawn)
    idler pulley     revolute on its axle, against the idler arm; the arm itself pivots on its bracket (not animated, spring-loaded)
    rollers (4)      revolute about their own axes, against their bulkhead
    door             revolute about the hinge pin (the fixed hinge halves carry it): disc, swinging hinge halves,
                     handle, seal, strike and their screws in a rigid group
    timer knobs (2)  revolute about the shaft axis, normal to the console face, against the faceplate
    HEAT selector    revolute, three positions AIR / LOW / HIGH at 0, 45 and 90 degrees
    START button     slider along its axis, 3 mm press
    heat module tray slider along Y, tray and module envelope together, 250 mm pull-out toward the back
    lint basket      slider along Y, the basket's plates, mesh and pull together, 40 mm back out of the slot into the drum
Everything else is grounded. The belt is drawn on its path and does not deform.
Draft 7, 2026-11-07: the two-tone paint is distant blue (RAL 5023) and graphite grey (RAL 7024), two appearances the
script makes in the design from the library's glossy enamel (PAINT); render() makes the product renders of
mechanical/renders/ with Fusion's own renderer.
Draft 6, 2026-11-06 (draft 1 made its own barebones faceplate, knobs and hinge pin; draft 2 jointed the model's own;
draft 3 follows model draft 6: vertical console face, the tray slides out the back, the rear lower panel is left out
of the moved poses; draft 4 follows model draft 7: the whole heat module, every "heat-module" part, rides the tray;
20 pulley; appearances for the new parts; draft 5 follows model draft 8: the lint basket slides, appearances for the
liner, the bar-frame ducts and their foam; draft 6 follows model draft 9: appearances for the blower plate and feet,
the exhaust pipe, clamps, barb and tube, the two sensors, the blanks and the cable clamps).
Units in the API are cm; the numbers below are written in mm and converted.
"""
import math
import os
import time
import traceback

import adsk.core
import adsk.fusion

try:
    REPO = globals().get("REPO") or os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
except NameError:
    raise RuntimeError("set REPO to the repo folder before exec()")

CM = 0.1   # mm -> cm

# geometry the STEP carries (mm), same numbers as osa_dryer_cad.py and docs/design-rules.md
N = (0.0, -1.0, 0.0)                          # console face normal: the face is vertical, looking forward (draft 6)
Y_AXIS = (0.0, 1.0, 0.0)
Z_AXIS = (0.0, 0.0, 1.0)

# component names in the STEP (prefixes; the long names carry the bought-part notes)
DRUM_GROUP = ("drum-sheet", "drum-ring-front", "drum-ring-rear", "drum-splice",
              "baffle-1 (angle", "baffle-2 (angle", "baffle-3 (angle",
              "hardware-drum-tabs", "hardware-drum-seam", "hardware-drum-baffles")
DOOR_GROUP = ("door-disc", "door-handle", "door-seal", "door-catch-strike", "door-hinge-2-swing",
              "hardware-door-hinge-2", "hardware-door-handle")
TRAY_GROUP = ("heat-module",)    # every part whose name starts with this slides out with the tray (draft 7: tray, box, element, collar, terminal plate, devices, hardware)
BASKET_GROUP = ("basket-", "hardware-basket")   # the lint basket slides out of the slot into the drum (draft 8), 40 mm in the demonstration
ARM_GROUP = ("idler-arm", "hardware-idler-axle")
SINGLE_MOVERS = ("pulley (bought", "roller-front-1", "roller-front-2", "roller-rear-1", "roller-rear-2",
                 "idler-pulley", "tier0-knob-dry-time", "tier0-knob-heat-time", "tier0-selector (bought", "tier0-start-button")

J = {}          # joints by name
SIGN = {}       # +1 or -1 per joint, so a positive value in pose() always moves the documented way


def P(x, y, z):
    return adsk.core.Point3D.create(x * CM, y * CM, z * CM)


def get_design():
    app = adsk.core.Application.get()
    d = adsk.fusion.Design.cast(app.activeProduct)
    if d is None:
        raise RuntimeError("open the assembly design first")
    return app, d


def occ_by_name(root, prefix):
    """The occurrence whose component name is `prefix` or starts with it (the STEP names carry long notes)."""
    hit = None
    for o in root.allOccurrences:
        n = o.component.name
        if n == prefix:
            return o
        if n.startswith(prefix) and hit is None:
            hit = o
    if hit is None:
        raise RuntimeError(f"component not found: {prefix}")
    return hit


def cyl_faces(occ, radius_mm, axis=None):
    out = []
    for body in occ.bRepBodies:
        for f in body.faces:
            g = f.geometry
            if g.surfaceType != adsk.core.SurfaceTypes.CylinderSurfaceType:
                continue
            c = adsk.core.Cylinder.cast(g)
            if abs(c.radius - radius_mm * CM) > 0.001:
                continue
            if axis is not None:
                a = c.axis
                if abs(abs(a.x * axis[0] + a.y * axis[1] + a.z * axis[2]) - 1) > 1e-4:
                    continue
            out.append(f)
    if not out:
        raise RuntimeError(f"no cylindrical face of radius {radius_mm} on {occ.component.name}")
    return out


def cyl_face(occ, radius_mm, axis=None, largest=False, near=None):
    """A cylindrical face of the occurrence with this radius (tolerance 0.001 cm), optionally with its axis
    along a world direction; the largest one, or the one nearest a world point (mm)."""
    faces = cyl_faces(occ, radius_mm, axis)
    if near is not None:
        p = P(*near)
        return min(faces, key=lambda f: f.centroid.distanceTo(p))
    if largest:
        return max(faces, key=lambda f: f.area)
    return faces[0]


def revolute(root, occ_moving, occ_fixed, face, name, positive_dir=None):
    """As-built revolute joint on a cylindrical face. positive_dir: world direction the joint's axis should point
    so that a positive rotation turns the documented way; SIGN[name] records the sign to use."""
    geo = adsk.fusion.JointGeometry.createByNonPlanarFace(face, adsk.fusion.JointKeyPointTypes.MiddleKeyPoint)
    inp = root.asBuiltJoints.createInput(occ_moving, occ_fixed, geo)
    inp.setAsRevoluteJointMotion(adsk.fusion.JointDirections.ZAxisJointDirection)
    j = root.asBuiltJoints.add(inp)
    j.name = name
    J[name] = j
    SIGN[name] = 1.0
    if positive_dir is not None:
        try:
            a = j.jointMotion.rotationAxisVector
            if a.x * positive_dir[0] + a.y * positive_dir[1] + a.z * positive_dir[2] < 0:
                SIGN[name] = -1.0
        except Exception:
            pass
    return j


def slider(root, occ_moving, occ_fixed, geo, name, positive_dir):
    inp = root.asBuiltJoints.createInput(occ_moving, occ_fixed, geo)
    inp.setAsSliderJointMotion(adsk.fusion.JointDirections.ZAxisJointDirection)
    j = root.asBuiltJoints.add(inp)
    j.name = name
    J[name] = j
    SIGN[name] = 1.0
    try:
        a = j.jointMotion.slideDirectionVector
        if a.x * positive_dir[0] + a.y * positive_dir[1] + a.z * positive_dir[2] < 0:
            SIGN[name] = -1.0
    except Exception:
        pass
    return j


def rigid_group(root, names, label, by_prefix=False):
    """One rigid group of the named occurrences; with by_prefix, every occurrence whose name starts with any of the names."""
    coll = adsk.core.ObjectCollection.create()
    if by_prefix:
        for o in root.allOccurrences:
            if any(o.component.name.startswith(n) for n in names):
                coll.add(o)
    else:
        for n in names:
            coll.add(occ_by_name(root, n))
    rg = root.rigidGroups.add(coll, True)
    rg.name = label
    return rg


def clean(root):
    """Remove what an earlier run of this script made, so build() can run again on the same design."""
    for j in list(root.asBuiltJoints):
        j.deleteMe()
    for j in list(root.joints):
        j.deleteMe()
    for g in list(root.rigidGroups):
        g.deleteMe()
    for o in list(root.occurrences):
        if o.component.name.endswith("(barebones)"):   # draft 1 of this script made these
            o.deleteMe()
    J.clear()
    SIGN.clear()


def build():
    app, design = get_design()
    root = design.rootComponent
    log = []
    clean(root)

    # --- ground everything that stays put
    movers = DRUM_GROUP + DOOR_GROUP + TRAY_GROUP + BASKET_GROUP + ARM_GROUP + SINGLE_MOVERS
    for o in root.allOccurrences:
        if not any(o.component.name.startswith(m) for m in movers) and not o.isGrounded:
            o.isGrounded = True

    # --- the drum: one rigid group, one revolute joint on the drum axis
    rigid_group(root, DRUM_GROUP, "drum (sheet, rings, splice, baffles, bolts)")
    drum = occ_by_name(root, "drum-sheet")
    revolute(root, drum, occ_by_name(root, "front-bulkhead"), cyl_face(drum, 310.0, Y_AXIS, largest=True), "drum")
    log.append("drum")

    # --- motor shaft: the pulley spins on the motor. The blower housing stays put (its wheel, which turns, is not drawn)
    motor = occ_by_name(root, "motor (bought")
    pulley = occ_by_name(root, "pulley (bought")
    revolute(root, pulley, motor, cyl_face(pulley, 10.0, Y_AXIS, largest=True), "pulley")   # 20 pulley (draft 7)
    log.append("pulley")

    # --- idler: the arm pivots on its bracket (not animated), the pulley spins on the arm
    arm = occ_by_name(root, "idler-arm")
    rigid_group(root, ARM_GROUP, "idler arm with its axle")
    revolute(root, arm, occ_by_name(root, "idler-bracket"), cyl_face(arm, 4.25, Y_AXIS, near=(-115.0, 392.0, 25.0)), "idler arm")
    idler = occ_by_name(root, "idler-pulley")
    revolute(root, idler, arm, cyl_face(idler, 20.0, Y_AXIS, largest=True), "idler")
    log.append("idler")

    # --- rollers
    fb, rb = occ_by_name(root, "front-bulkhead"), occ_by_name(root, "rear-bulkhead")
    for n, bulk in (("roller-front-1", fb), ("roller-front-2", fb), ("roller-rear-1", rb), ("roller-rear-2", rb)):
        r = occ_by_name(root, n)
        revolute(root, r, bulk, cyl_face(r, 30.0, Y_AXIS, largest=True), n)
    log.append("rollers")

    # --- door: the disc and everything on it swing on the pin of the fixed hinge halves
    rigid_group(root, DOOR_GROUP, "door (disc, hinge halves, handle, seal, strike, screws)")
    door = occ_by_name(root, "door-disc")
    fixed = occ_by_name(root, "door-hinge-1-fixed")
    # positive rotation should swing the handle side (+X) toward -Y (open): that is a rotation about -Z
    revolute(root, door, fixed, cyl_face(fixed, 4.0, Z_AXIS, largest=True), "door", positive_dir=(0.0, 0.0, -1.0))
    log.append("door")

    # --- Tier 0 module: knobs on the faceplate, selector and button on their own bodies
    fp = occ_by_name(root, "tier0-faceplate")
    for key in ("dry-time", "heat-time"):
        k = occ_by_name(root, f"tier0-knob-{key}")
        revolute(root, k, fp, cyl_face(k, 20.0, N, largest=True), f"knob {key}", positive_dir=N)
    sel = occ_by_name(root, "tier0-selector (bought")
    revolute(root, sel, occ_by_name(root, "tier0-selector-body"), cyl_face(sel, 11.0, N, largest=True), "selector", positive_dir=N)
    btn = occ_by_name(root, "tier0-start-button")
    geo = adsk.fusion.JointGeometry.createByNonPlanarFace(cyl_face(btn, 11.0, N, largest=True), adsk.fusion.JointKeyPointTypes.MiddleKeyPoint)
    slider(root, btn, occ_by_name(root, "tier0-start-body"), geo, "start button", positive_dir=(-N[0], -N[1], -N[2]))   # positive = pressed in
    log.append("Tier 0 knobs, selector, START")

    # --- heat module tray: slides out the back with the whole module on it (250 mm)
    rigid_group(root, TRAY_GROUP, "heat module on its tray", by_prefix=True)
    tray = occ_by_name(root, "heat-module-tray")
    rail = occ_by_name(root, "tray-rail-1")
    faces = [f for f in tray.bRepBodies.item(0).faces if f.geometry.surfaceType == adsk.core.SurfaceTypes.PlaneSurfaceType]
    face = min(faces, key=lambda f: f.centroid.y)       # the end face at the front of the tray: its normal is the slide axis
    geo = adsk.fusion.JointGeometry.createByPlanarFace(face, None, adsk.fusion.JointKeyPointTypes.CenterKeyPoint)
    slider(root, tray, rail, geo, "tray", positive_dir=(0.0, 1.0, 0.0))    # positive = pulled out toward the back (draft 6: the module leaves by the back)
    log.append("tray slide")

    # --- lint basket: slides back out of the slot into the drum (draft 8); 40 mm clears the slot, then it lifts out through the door
    rigid_group(root, BASKET_GROUP, "lint basket (plates, mesh, pull, screws)", by_prefix=True)
    far = occ_by_name(root, "basket-far-plate")
    faces = [f for f in far.bRepBodies.item(0).faces if f.geometry.surfaceType == adsk.core.SurfaceTypes.PlaneSurfaceType]
    face = min(faces, key=lambda f: f.centroid.y)       # the far plate's front face: its normal is the slide axis
    geo = adsk.fusion.JointGeometry.createByPlanarFace(face, None, adsk.fusion.JointKeyPointTypes.CenterKeyPoint)
    slider(root, far, occ_by_name(root, "front-bulkhead"), geo, "basket", positive_dir=(0.0, 1.0, 0.0))   # positive = pulled back into the drum
    log.append("basket slide")

    app.activeViewport.refresh()
    msg = "fusion_motion build: " + ", ".join(log) + f"; {len(J)} joints"
    try:
        app.log(msg)
    except Exception:
        pass
    return msg


POSITIVE_DIRS = {"door": (0.0, 0.0, -1.0), "knob dry-time": N, "knob heat-time": N, "selector": N,
                 "start button": (-N[0], -N[1], -N[2]), "tray": (0.0, 1.0, 0.0), "basket": (0.0, 1.0, 0.0)}


def reconnect():
    """Pick up the joints an earlier build() left in the design (after this file is run again), with their signs."""
    app, design = get_design()
    J.clear()
    SIGN.clear()
    for j in design.rootComponent.asBuiltJoints:
        J[j.name] = j
        SIGN[j.name] = 1.0
        want = POSITIVE_DIRS.get(j.name)
        if want is None:
            continue
        try:
            a = j.jointMotion.rotationAxisVector if j.jointMotion.jointType == adsk.fusion.JointTypes.RevoluteJointType else j.jointMotion.slideDirectionVector
            if a.x * want[0] + a.y * want[1] + a.z * want[2] < 0:
                SIGN[j.name] = -1.0
        except Exception:
            pass
    return f"reconnected {len(J)} joints"


def _set_rot(name, radians):
    j = J.get(name)
    if j is not None:
        j.jointMotion.rotationValue = SIGN.get(name, 1.0) * radians


def _set_slide(name, cm):
    j = J.get(name)
    if j is not None:
        j.jointMotion.slideValue = SIGN.get(name, 1.0) * cm


def pose(t):
    """Joint values at a fraction t (0..1) of the demonstration."""
    drum = 2 * math.pi * t                                    # one drum turn over the demonstration
    _set_rot("drum", drum)
    _set_rot("pulley", drum * 620.0 / 20.0)                   # belt ratio, drum to the 20 pulley (draft 7)
    _set_rot("idler", -drum * 620.0 / 40.0)                   # backside idler turns the other way
    for n in ("roller-front-1", "roller-front-2", "roller-rear-1", "roller-rear-2"):
        _set_rot(n, -drum * 310.0 / 30.0)                     # rollers roll on the sheet
    _set_rot("door", math.radians(100) * (0.5 - 0.5 * math.cos(2 * math.pi * t)))   # opens to 100 degrees, closes
    _set_rot("knob dry-time", math.radians(300) * t)
    _set_rot("knob heat-time", math.radians(200) * t)
    _set_rot("selector", math.radians(45) * ((1 if t > 0.33 else 0) + (1 if t > 0.66 else 0)))   # AIR, LOW, HIGH
    _set_slide("start button", 0.3 if 0.08 < t < 0.18 else 0.0)                               # 3 mm press
    _set_slide("tray", 25.0 * (0.5 - 0.5 * math.cos(2 * math.pi * t)))                        # out and back
    _set_slide("basket", 40.0 * (0.5 - 0.5 * math.cos(2 * math.pi * t)))                      # out of the slot into the drum and back (draft 8)


def animate(seconds=10.0, fps=12):
    app, design = get_design()
    vp = app.activeViewport
    frames = max(1, int(seconds * fps))
    t0 = time.time()
    for i in range(frames + 1):
        pose(i / frames)
        adsk.doEvents()
        vp.refresh()
        target = t0 + seconds * i / frames      # keep real time
        while time.time() < target:
            adsk.doEvents()
    pose(0.0)
    vp.refresh()
    return f"animated {frames} frames"


def _owner_name(ent):
    """The component name an interference entity belongs to."""
    try:
        if ent.assemblyContext is not None:
            return ent.assemblyContext.component.name
    except Exception:
        pass
    try:
        return ent.parentComponent.name
    except Exception:
        return getattr(ent, "name", str(ent))


SERVICE_PANEL = ("rear-lower-panel", "hardware-rear-lower-panel")   # off before the heat module comes out (7 Access)


def check_poses(ts=(0.0, 0.25, 0.5), min_mm3=1.0):
    """Fusion's own interference analysis at several points of the motion. Returns a list of
    (t, part a, part b, overlap volume in mm3) and prints a summary. The rest pose (t = 0) should be clean;
    anything that appears while something moves is a collision in the design. At the moved poses the rear lower
    panel and its bolts are left out, as they are off when the heat module is pulled."""
    app, design = get_design()
    root = design.rootComponent
    found = []
    for t in ts:
        pose(t)
        adsk.doEvents()
        coll = adsk.core.ObjectCollection.create()
        for o in root.allOccurrences:
            if t > 0 and any(o.component.name.startswith(sp) for sp in SERVICE_PANEL):
                continue
            if o.isLightBulbOn:
                coll.add(o)
        inp = design.createInterferenceInput(coll)
        inp.areCoincidentFacesIncluded = False
        res = design.analyzeInterference(inp)
        n = 0
        for i in range(res.count):
            r_ = res.item(i)
            try:
                vol = r_.interferenceBody.volume * 1000.0
            except Exception:
                vol = -1.0
            if vol < 0 or vol >= min_mm3:
                found.append((t, _owner_name(r_.entityOne), _owner_name(r_.entityTwo), round(vol, 1)))
                n += 1
        try:
            app.log(f"pose t={t}: {n} interferences")
        except Exception:
            pass
    pose(0.0)
    app.activeViewport.refresh()
    for f in found:
        print(f"t={f[0]:.2f}  {f[1]}  x  {f[2]}  {f[3]} mm3")
    print(f"{len(found)} interferences over {len(ts)} poses")
    return found


# The two-tone paint (draft 7 of this script, DECISIONS.md 2026-11-07): the library's glossy enamel copied into the
# design and given a RAL colour (sRGB), one appearance for the body panels and one for the trim. Change a colour here
# and run dress() again; the appearances keep their names, so Fusion's own appearance editor can change them too.
PAINT_BASE = "Paint - Enamel Glossy (White)"
PAINT = {
    "OSA body paint (RAL 5023 distant blue)": (66, 105, 140),
    "OSA trim paint (RAL 7024 graphite grey)": (69, 73, 78),
}

# Appearances from the Fusion Appearance Library (exact library names) or PAINT, by component name or name prefix
APPEARANCES = [
    # two-tone paint: distant blue body (side, upper front and rear, and top panels), graphite console, door and skirt
    ("OSA body paint (RAL 5023 distant blue)", ("side-panel-left", "side-panel-right", "front-upper-panel", "rear-upper-panel", "top-panel")),
    ("OSA trim paint (RAL 7024 graphite grey)", ("door-ring", "door-disc", "front-lower-panel", "rear-lower-panel", "console-face", "console-cap",
                                                "console-cheek-left", "console-cheek-right", "console-rear")),
    ("Aluminum - Anodized Rough (Grey)", ("post-", "rail-", "tray-rail-", "console-post", "console-rail", "heat-module-angles-",
                                          "heat-module-element-rails", "heat-module-terminal-angle", "power-module-barrier-angle")),
    ("Steel - Galvanized (Small)", ("front-bulkhead", "rear-bulkhead", "bay-ceiling", "base-pan", "heat-module-tray", "heat-module-wall-",
                                    "heat-module-top", "heat-module-terminal-plate", "heat-module-collar", "power-module-plate",
                                    "power-module-barrier", "power-module-cover", "lint-box-front", "lint-box-back", "hood-bottom", "hood-top",
                                    "trunk-front", "trunk-rear", "basket-far-", "basket-lip-", "blower (bought", "motor-mount-", "blower-plate", "entry-blank")),
    ("Stainless Steel - Brushed Linear Long", ("drum-sheet", "drum-ring-front", "drum-ring-rear", "drum-splice")),
    ("Aluminum - Satin", ("baffle-", "exhaust-duct", "idler-arm", "idler-bracket", "spring-bracket", "lint-box-bars", "spool-bars", "hood-bars",
                          "trunk-bars", "nozzle-bars", "liner", "ps1-bracket", "blower-plate-feet")),
    ("Rubber - Hard", ("roller-", "belt (bought", "feet (bought", "cord-bushing", "power-cord", "grommets (bought")),
    ("Rubber - Soft", ("door-seal", "hood-gasket", "lint-box-foam", "spool-foam", "nozzle-foam", "ps1-tube")),
    ("Fabric (Grey)", ("felt-seal-",)),
    ("Plastic - Matte (White)", ("drum-glides-",)),
    ("Paint - Metallic (Dark Grey)", ("motor (bought",)),
    ("Steel - Satin", ("pulley (bought", "heat-module-element", "heat-module-din-rail", "heat-module-bonding-stud", "heat-module-hardware",
                       "power-module-din-rails", "power-module-standoffs", "power-module-ground-stud", "power-module-hardware",
                       "idler-pulley", "idler-spring", "hardware-", "console-brackets", "tray-rail-brackets", "lint-box-hardware", "riser-hardware",
                       "basket-mesh", "basket-pull")),
    ("Plastic - Matte (Black)", ("heat-module-devices", "heat-module-thermostats", "power-module-rail-", "door-switch", "ps1-air-proving",
                                 "exhaust-thermostats", "th1-exhaust-thermistor", "cable-clamps")),
    ("Plastic - Matte (White)", ("moisture-bars",)),
    ("Brass - Polished", ("exhaust-tap-barb",)),
    ("Steel - Satin", ("exhaust-clamps",)),
    ("Stainless Steel - Satin", ("door-hinge-", "door-handle", "door-catch")),
    ("Aluminum - Brushed Linear", ("tier0-faceplate",)),
    ("Plastic - Matte (Black)", ("tier0-knob-", "tier0-selector", "tier0-start-body", "tier0-k1-relay")),
    ("Plastic - Matte (White)", ("tier0-timer-",)),
    ("Plastic - Matte (Green)", ("tier0-start-button",)),
]


def _appearance_for(name):
    for appr, keys in APPEARANCES:
        if name in keys:
            return appr
    for appr, keys in APPEARANCES:
        if any(name.startswith(k) for k in keys):
            return appr
    return None


def paint_appearance(design, lib, name, rgb):
    """The design's own copy of the library's glossy enamel, named and coloured; made once, recoloured on every call."""
    appr = None
    try:
        appr = design.appearances.itemByName(name)
    except Exception:
        appr = None
    if appr is None:
        appr = design.appearances.addByCopy(lib.appearances.itemByName(PAINT_BASE), name)
    colour = appr.appearanceProperties.itemById("opaque_albedo")    # the paint layer's colour; surface_albedo is the clear coat
    colour.value = adsk.core.Color.create(rgb[0], rgb[1], rgb[2], 255)
    return appr


def dress(only=None):
    """Give every component a real appearance from Fusion's library, so the model reads as the materials it is;
    with only (name prefixes), just those components (the whole model takes minutes in the parametric document)."""
    app, design = get_design()
    root = design.rootComponent
    lib = app.materialLibraries.itemByName("Fusion Appearance Library")
    done, missing = 0, []
    cache = {}
    for occ in root.allOccurrences:
        if only is not None and not any(occ.component.name.startswith(p) for p in only):
            continue
        appr_name = _appearance_for(occ.component.name)
        if appr_name is None:
            missing.append(occ.component.name)
            continue
        if appr_name not in cache:
            try:
                if appr_name in PAINT:
                    cache[appr_name] = paint_appearance(design, lib, appr_name, PAINT[appr_name])
                else:
                    cache[appr_name] = lib.appearances.itemByName(appr_name)
            except Exception:   # a name the library does not have raises rather than returning None
                cache[appr_name] = None
        appr = cache[appr_name]
        if appr is None:
            missing.append(f"{occ.component.name} ({appr_name} not in library)")
            continue
        occ.appearance = appr
        for b in occ.bRepBodies:        # the STEP gives bodies their own colours, which would win over the occurrence's
            try:
                b.appearance = appr
            except Exception:
                pass
        done += 1
    app.activeViewport.refresh()
    return f"dressed {done} components" + (f"; no appearance for: {missing}" if missing else "")


def hide(*prefixes):
    """Hide every component whose name starts with one of the prefixes (for looking inside). show_all() undoes it."""
    app, design = get_design()
    n = 0
    for o in design.rootComponent.allOccurrences:
        if any(o.component.name.startswith(p) for p in prefixes):
            o.isLightBulbOn = False
            n += 1
    app.activeViewport.refresh()
    return f"hidden {n}"


def show_all():
    app, design = get_design()
    for o in design.rootComponent.allOccurrences:
        o.isLightBulbOn = True
    app.activeViewport.refresh()


def view(name="iso"):
    """Standard camera: iso, front, left, top, back, right, iso-back."""
    app, design = get_design()
    vo = adsk.core.ViewOrientations
    pick = {"iso": vo.IsoTopLeftViewOrientation, "iso-back": vo.IsoTopRightViewOrientation, "front": vo.FrontViewOrientation,
            "left": vo.LeftViewOrientation, "right": vo.RightViewOrientation, "top": vo.TopViewOrientation, "back": vo.BackViewOrientation}[name]
    vp = app.activeViewport
    cam = vp.camera
    cam.viewOrientation = pick
    cam.isFitView = True
    vp.camera = cam
    vp.refresh()


# Product renders (draft 7): file name, what the shot shows, the components shown (name prefixes; None is everything),
# the components hidden, and where the camera stands as a direction from the centre of what is shown (X across, left
# negative; Y front to back; Z up), the distance following from its size. Rendered by render() with Fusion's own
# renderer into mechanical/renders/.
SHOTS = [
    ("01-dryer-front-left", "the dryer from the front left", None, (), (-0.85, -1.0, 0.42)),
    ("02-dryer-rear-right", "the dryer from the rear right: the exhaust, the console's back, the cord", None, (), (0.85, 1.0, 0.42)),
    ("03-dryer-front", "the dryer from the front: door, skirt, console", None, (), (-0.12, -1.0, 0.16)),
    ("04-dryer-service-side", "the left side panel and the top off: drum, drive, ducts and modules in place", None,
     ("side-panel-left", "hardware-side-panel-left", "top-panel", "hardware-top-panel"), (-1.0, -0.6, 0.42)),
    ("05-dryer-rear-open", "the rear panels and the power module cover off: heat module, power module, blower, exhaust", None,
     ("rear-upper-panel", "rear-lower-panel", "hardware-rear-upper-panel", "hardware-rear-lower-panel", "console-rear",
      "hardware-console-rear", "power-module-cover"), (0.9, 1.0, 0.4)),
    ("06-drum-set", "the drum: sheet, rings, splice, baffles, rollers and their studs",
     ("drum-", "baffle-", "roller-", "hardware-drum-", "hardware-roller-studs"), (), (-0.9, -1.0, 0.5)),
    ("07-heat-module", "the electric heat module on its tray: element, collar, thermostats, DIN rail and devices",
     ("heat-module-",), (), (-0.9, 1.0, 0.6)),
    ("08-power-module", "the power module without its cover: the five DIN rails and their devices, barrier, standoffs, ground stud",
     ("power-module-", "hardware-power-module-plate"), ("power-module-cover",), (-0.55, 1.0, 0.3)),
    ("09-tier0-module", "the Tier 0 control module: faceplate, timers, knobs, HEAT selector, START, K1",
     ("tier0-", "hardware-tier0-faceplate"), (), (-0.35, -1.0, 0.25)),
    ("10-door", "the door: ring, disc, hinges, handle, seal, catch and switch", ("door-", "hardware-door-"), (), (-0.8, -1.0, 0.35)),
    ("11-drive", "the drive: motor on its cradles, pulley, idler, blower on its plate (the belt runs up to the drum, left out)",
     ("motor", "pulley", "blower", "idler-", "hardware-idler-", "spring-bracket", "hardware-motor-mounts", "hardware-blower-plate",
      "exhaust-thermostats", "hardware-exhaust-thermostats"), (), (-1.0, 0.5, 0.5)),
    ("12-lint-path", "the lint path: lint box, basket, riser, liner, hood, trunk and nozzle",
     ("lint-box-", "basket-", "hardware-basket", "spool-", "riser-hardware", "liner", "hardware-liner", "hood-", "trunk-", "nozzle-",
      "th1-", "hardware-th1", "moisture-bars", "hardware-moisture-bars"), (), (-0.9, -1.0, 0.5)),
    ("13-exhaust-set", "the exhaust: blower outlet, thermostats, pipe, clamps, tap, PS1 and its tube",
     ("blower (bought", "exhaust-", "hardware-exhaust-", "ps1-", "hardware-ps1", "th1-", "hardware-th1"), (), (1.0, 0.7, 0.5)),
    ("14-frame", "the frame: posts, rails, tray rails, console sub-frame, brackets and feet",
     ("post-", "rail-", "tray-rail", "console-post", "console-rail", "console-brackets", "hardware-console-brackets", "feet"), (), (-0.85, -1.0, 0.42)),
]
RENDER_ENVIRONMENT = "Soft Light"       # the lighting; the background is a plain white
RENDER_LENS = 0.40                       # the viewport camera's perspective angle, radians (the renderer does not use it)
RENDER_TAN_H = 0.5                       # the local renderer's own lens: half the horizontal view angle as a tangent, a 36 mm
#                                          lens on a 36 mm frame, whatever the viewport camera's angle (measured 2026-11-07:
#                                          renders at angles 0.3, 0.4 and 0.8 all came out with the same view angle)
RENDER_CROP = 1.5                        # render this much bigger and keep the middle: the look of a 54 mm lens
RENDER_EXPOSURE = None                   # camera exposure value, None keeps the environment's own (9.5 with Soft Light;
#                                          setting 12 made the scene dark, so leave it unless the environment changes)
RENDER_LIGHT_ANGLE = 0.0                 # rotation of the environment's light about the model, radians


def _visible_box(design):
    lo, hi = [1e9] * 3, [-1e9] * 3
    for o in design.rootComponent.allOccurrences:
        if not o.isLightBulbOn:
            continue
        bb = o.boundingBox
        if bb is None:
            continue
        p, q = bb.minPoint, bb.maxPoint
        lo = [min(lo[0], p.x), min(lo[1], p.y), min(lo[2], p.z)]
        hi = [max(hi[0], q.x), max(hi[1], q.y), max(hi[2], q.z)]
    return lo, hi


def aim(direction, margin=1.06, aspect=16 / 9, crop=1.0):
    """Point the viewport camera at what is visible, from the direction given, just far enough back that every
    corner of its box fits the frame that is kept: the renderer's own lens (RENDER_TAN_H across the whole render,
    the height following from the aspect ratio), divided by the crop that keeps the middle of the render."""
    app, design = get_design()
    lo, hi = _visible_box(design)
    centre = [(a + b) / 2 for a, b in zip(lo, hi)]
    radius = max(math.dist(lo, hi) / 2, 1.0)
    n = math.sqrt(sum(c * c for c in direction))
    d = [c / n for c in direction]
    f = [-c for c in d]                                            # from the eye to the target
    r = [f[1] * 1.0 - f[2] * 0.0, f[2] * 0.0 - f[0] * 1.0, f[0] * 0.0 - f[1] * 0.0]     # f x up(0,0,1)
    rn = math.sqrt(sum(c * c for c in r)) or 1.0
    r = [c / rn for c in r]
    u = [r[1] * f[2] - r[2] * f[1], r[2] * f[0] - r[0] * f[2], r[0] * f[1] - r[1] * f[0]]   # r x f
    th = RENDER_TAN_H / crop
    tv = th / aspect
    dist = 0.0
    for cx in (lo[0], hi[0]):
        for cy in (lo[1], hi[1]):
            for cz in (lo[2], hi[2]):
                c = [cx - centre[0], cy - centre[1], cz - centre[2]]
                depth = sum(a * b for a, b in zip(c, f))
                x = abs(sum(a * b for a, b in zip(c, r)))
                y = abs(sum(a * b for a, b in zip(c, u)))
                dist = max(dist, x / th - depth, y / tv - depth)
    dist = max(dist * margin, radius * 1.01)
    vp = app.activeViewport
    cam = vp.camera
    cam.cameraType = adsk.core.CameraTypes.PerspectiveCameraType
    cam.perspectiveAngle = RENDER_LENS
    cam.isSmoothTransition = False
    cam.isFitView = False
    cam.target = adsk.core.Point3D.create(*centre)
    cam.eye = adsk.core.Point3D.create(centre[0] + d[0] * dist, centre[1] + d[1] * dist, centre[2] + d[2] * dist)
    cam.upVector = adsk.core.Vector3D.create(0, 0, 1)
    vp.camera = cam
    vp.refresh()
    return centre, radius, dist


def scene():
    """The render scene: a studio light, a white background, a ground that takes shadows and a little reflection.
    The Render workspace is activated first; the scene settings are set from there. Setting SceneSettings.cameraType
    closed Fusion outright (twice, 2026-11-07), so the camera's type is left to the viewport camera (aim)."""
    app, design = get_design()
    rm = design.renderManager
    rm.activateRenderWorkspace()
    ss = rm.sceneSettings
    env = rm.renderEnvironments.itemByName(RENDER_ENVIRONMENT)
    if env is not None:
        ss.backgroundEnvironment = env
    ss.backgroundSolidColor = adsk.core.Color.create(255, 255, 255, 255)
    ss.isGroundDisplayed = True
    ss.isGroundFlattened = False
    ss.isGroundReflections = True
    ss.groundRoughness = 0.6
    ss.groundOffset = 0.0
    ss.isDepthOfFieldEnabled = False
    if RENDER_EXPOSURE is not None:
        ss.cameraExposure = RENDER_EXPOSURE
    ss.lightAngle = RENDER_LIGHT_ANGLE
    return ss


def png_crop(src, dst, crop):
    """Keep the middle 1/crop of a PNG's width and height (8-bit, not interlaced, as Fusion writes them), without
    an image library: the IDAT stream is inflated, the rows unfiltered, the middle cut out and deflated again."""
    import struct
    import zlib
    data = open(src, "rb").read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(src + " is not a PNG")
    pos, chunks, idat = 8, [], []
    while pos < len(data):
        n, kind = struct.unpack(">I4s", data[pos:pos + 8])
        body = data[pos + 8:pos + 8 + n]
        pos += 12 + n
        if kind == b"IDAT":
            idat.append(body)
        elif kind == b"IEND":
            break
        else:
            chunks.append((kind, body))
    ihdr = chunks[0][1]
    w, h, depth, ctype, _, _, interlace = struct.unpack(">IIBBBBB", ihdr)
    if depth != 8 or interlace != 0:
        raise ValueError(src + ": only 8-bit non-interlaced PNGs")
    bpp = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}[ctype]
    stride = w * bpp
    raw = zlib.decompress(b"".join(idat))
    cw, ch = int(round(w / crop)), int(round(h / crop))
    left, top = (w - cw) // 2, (h - ch) // 2
    rows, prev, p = [], bytearray(stride), 0
    for y in range(top + ch):
        ft = raw[p]
        cur = bytearray(raw[p + 1:p + 1 + stride])
        p += 1 + stride
        if ft == 1:
            for i in range(bpp, stride):
                cur[i] = (cur[i] + cur[i - bpp]) & 255
        elif ft == 2:
            cur = bytearray((a + b) & 255 for a, b in zip(cur, prev))
        elif ft == 3:
            for i in range(stride):
                cur[i] = (cur[i] + (((cur[i - bpp] if i >= bpp else 0) + prev[i]) >> 1)) & 255
        elif ft == 4:
            for i in range(stride):
                a = cur[i - bpp] if i >= bpp else 0
                b = prev[i]
                c = prev[i - bpp] if i >= bpp else 0
                q = a + b - c
                pa, pb, pc = abs(q - a), abs(q - b), abs(q - c)
                cur[i] = (cur[i] + (a if pa <= pb and pa <= pc else b if pb <= pc else c)) & 255
        if y >= top:
            rows.append(bytes(cur[left * bpp:(left + cw) * bpp]))
        prev = cur
    out = [b"\x89PNG\r\n\x1a\n"]

    def chunk(kind, body):
        out.append(struct.pack(">I", len(body)) + kind + body + struct.pack(">I", zlib.crc32(kind + body) & 0xFFFFFFFF))

    chunk(b"IHDR", struct.pack(">IIBBBBB", cw, ch, 8, ctype, 0, 0, 0))
    for kind, body in chunks[1:]:
        chunk(kind, body)
    chunk(b"IDAT", zlib.compress(b"".join(b"\x00" + r for r in rows), 6))
    chunk(b"IEND", b"")
    open(dst, "wb").write(b"".join(out))
    return cw, ch


def render(names=None, quality=75, width=1920, height=1080, crop=None, folder=None, timeout=3600):
    """Render the SHOTS (or those whose file name starts with one of names) with Fusion's local renderer, one after
    another, waiting for each; quality 75 is Fusion's 'Final'. Each shot is rendered crop times bigger than width by
    height and its middle kept (RENDER_CROP, a longer lens than the renderer's own). Returns one line per shot."""
    app, design = get_design()
    if crop is None:
        crop = RENDER_CROP
    if folder is None:
        folder = os.path.join(REPO, "mechanical", "renders")
    os.makedirs(folder, exist_ok=True)
    root = design.rootComponent
    root.isJointsFolderLightBulbOn = False
    root.isConstructionFolderLightBulbOn = False
    root.isSketchFolderLightBulbOn = False
    root.isOriginFolderLightBulbOn = False
    scene()
    big_w, big_h = int(round(width * crop)), int(round(height * crop))
    if big_w > 4000 or big_h > 4000:
        raise ValueError("the renderer takes at most 4000 pixels a side: %d x %d" % (big_w, big_h))
    lines = []
    for stem, what, shown, hidden, direction in SHOTS:
        if names is not None and not any(stem.startswith(n) for n in names):
            continue
        show_all()
        if shown is not None:
            for o in root.allOccurrences:
                if not any(o.component.name.startswith(p) for p in shown):
                    o.isLightBulbOn = False
        if hidden:
            hide(*hidden)
        for _ in range(2):                                  # set twice and let the viewport settle: the renderer read a
            aim(direction, aspect=width / height, crop=crop)  # stale target when the camera was set once and the render
            app.activeViewport.refresh()                    # started at once (shots off centre, 2026-11-07)
            adsk.doEvents()
            time.sleep(1.5)
            adsk.doEvents()
        rendering = design.renderManager.rendering          # a fresh object each time; its settings do not persist
        rendering.aspectRatio = adsk.fusion.RenderAspectRatios.CustomRenderAspectRatio
        rendering.resolutionWidth = big_w
        rendering.resolutionHeight = big_h
        rendering.renderQuality = quality
        rendering.isBackgroundTransparent = False
        path = os.path.join(folder, stem + ".png")
        big = os.path.join(folder, stem + "-full.png") if crop != 1.0 else path
        for f in (path, big):
            if os.path.exists(f):
                os.remove(f)
        t0 = time.time()
        fut = rendering.startLocalRender(big)
        state = fut.renderState
        while state in (adsk.fusion.LocalRenderStates.QueuedLocalRenderState, adsk.fusion.LocalRenderStates.ProcessingLocalRenderState):
            adsk.doEvents()
            time.sleep(2.0)
            state = fut.renderState
            if time.time() - t0 > timeout:
                break
        ok = state == adsk.fusion.LocalRenderStates.FinishedLocalRenderState and os.path.exists(big)
        t_render = time.time() - t0
        if ok and crop != 1.0:
            png_crop(big, path, crop)
            os.remove(big)
        line = f"{stem}: {'done' if ok else 'FAILED (state %s)' % state} in {t_render:.0f} s render, {time.time() - t0 - t_render:.0f} s crop, {what}"
        lines.append(line)
        print(line)
        app.log(line)
    show_all()
    return "\n".join(lines)


def export_archive(path=None):
    app, design = get_design()
    if path is None:
        folder = os.path.join(REPO, "mechanical", "fusion")
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, "osa-dryer-assembly-motion.f3d")
    opts = design.exportManager.createFusionArchiveExportOptions(path)
    design.exportManager.execute(opts)
    return os.path.relpath(path, REPO)


def run(context):
    """Entry point from Scripts and Add-Ins."""
    try:
        msg = build()
        msg += "; " + dress()
        animate(10)
        out = export_archive()
        adsk.core.Application.get().userInterface.messageBox(msg + "\nexported " + out)
    except Exception:
        try:
            adsk.core.Application.get().userInterface.messageBox("fusion_motion failed:\n" + traceback.format_exc())
        except Exception:
            pass


try:   # run again on a design that already has the joints: pick them up
    if not J and adsk.core.Application.get().activeProduct is not None:
        _d = adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)
        if _d is not None and _d.rootComponent.asBuiltJoints.count:
            reconnect()
except Exception:
    pass
