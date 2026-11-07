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
Draft 5, 2026-11-06 (draft 1 made its own barebones faceplate, knobs and hinge pin; draft 2 jointed the model's own;
draft 3 follows model draft 6: vertical console face, the tray slides out the back, the rear lower panel is left out
of the moved poses; draft 4 follows model draft 7: the whole heat module, every "heat-module" part, rides the tray;
20 pulley; appearances for the new parts; draft 5 follows model draft 8: the lint basket slides, appearances for the
liner, the bar-frame ducts and their foam).
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


# Appearances from the Fusion Appearance Library (exact library names), by component name or name prefix
APPEARANCES = [
    ("Paint - Enamel Glossy (White)", ("side-panel-left", "side-panel-right", "front-upper-panel", "front-lower-panel",
                                       "rear-upper-panel", "rear-lower-panel", "top-panel", "console-face", "console-cap",
                                       "console-cheek-left", "console-cheek-right", "console-rear", "door-disc")),
    ("Paint - Enamel Glossy (Dark Grey)", ("door-ring",)),
    ("Aluminum - Anodized Rough (Grey)", ("post-", "rail-", "tray-rail-", "console-post", "console-rail", "heat-module-angles-",
                                          "heat-module-element-rails", "heat-module-terminal-angle", "power-module-barrier-angle")),
    ("Steel - Galvanized (Small)", ("front-bulkhead", "rear-bulkhead", "bay-ceiling", "base-pan", "heat-module-tray", "heat-module-wall-",
                                    "heat-module-top", "heat-module-terminal-plate", "heat-module-collar", "power-module-plate",
                                    "power-module-barrier", "power-module-cover", "lint-box-front", "lint-box-back", "hood-bottom", "hood-top",
                                    "trunk-front", "trunk-rear", "basket-far-", "basket-lip-", "blower (bought", "motor-mount-")),
    ("Stainless Steel - Brushed Linear Long", ("drum-sheet", "drum-ring-front", "drum-ring-rear", "drum-splice")),
    ("Aluminum - Satin", ("baffle-", "exhaust-duct", "idler-arm", "idler-bracket", "spring-bracket", "lint-box-bars", "spool-bars", "hood-bars",
                          "trunk-bars", "nozzle-bars", "liner", "ps1-bracket")),
    ("Rubber - Hard", ("roller-", "belt (bought", "feet (bought", "cord-bushing", "power-cord", "grommets (bought")),
    ("Rubber - Soft", ("door-seal", "hood-gasket", "lint-box-foam", "spool-foam", "nozzle-foam")),
    ("Fabric (Grey)", ("felt-seal-",)),
    ("Plastic - Matte (White)", ("drum-glides-",)),
    ("Paint - Metallic (Dark Grey)", ("motor (bought",)),
    ("Steel - Satin", ("pulley (bought", "heat-module-element", "heat-module-din-rail", "heat-module-bonding-stud", "heat-module-hardware",
                       "power-module-din-rails", "power-module-standoffs", "power-module-ground-stud", "power-module-hardware",
                       "idler-pulley", "idler-spring", "hardware-", "console-brackets", "tray-rail-brackets")),
    ("Plastic - Matte (Black)", ("heat-module-devices", "heat-module-thermostats", "power-module-rail-")),
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


def dress():
    """Give every component a real appearance from Fusion's library, so the model reads as the materials it is."""
    app, design = get_design()
    root = design.rootComponent
    lib = app.materialLibraries.itemByName("Fusion Appearance Library")
    done, missing = 0, []
    cache = {}
    for occ in root.allOccurrences:
        appr_name = _appearance_for(occ.component.name)
        if appr_name is None:
            missing.append(occ.component.name)
            continue
        if appr_name not in cache:
            cache[appr_name] = lib.appearances.itemByName(appr_name)
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
