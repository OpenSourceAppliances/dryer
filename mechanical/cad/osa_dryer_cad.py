"""osa-dryer parametric mechanical model.

One file holds every number. Run it and it writes:
  step/osa-dryer-assembly.step          the whole machine, bought parts as envelopes
  step/<part>.step                      one file per part we make
  drawings/<part>.dxf                   flat pattern for every laser-cut plate (CUT layer)
  drawings/frame-cut-list.csv           every extrusion length
  drawings/view-*.svg                   views for checking, not for cutting

Coordinate system: X across the cabinet (left negative), Y from front (0) to back, Z up from the floor.
All dimensions mm. Needs cadquery (pip install cadquery). Also runs in FreeCAD's CadQuery workbench.

Status: draft 3, 2026-11-05. Bought parts (motor, blower, timers, rollers) are drawn as envelopes
from catalog numbers that have NOT been measured. docs/verification.md says which measurement unlocks
which DXF. Do not cut a plate whose gate is open.
"""
import csv
import math
import os
import sys

import cadquery as cq
from cadquery import exporters

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
for sub in ("step", "drawings"):
    os.makedirs(os.path.join(OUT, sub), exist_ok=True)

# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------
P = dict(
    # cabinet
    W=690.0, D=750.0,
    ext=40.0,                 # 4040 extrusion
    ext_small=20.0,           # 2020 tray rails
    t_panel=1.5,              # outer panels, steel
    t_bulk=1.5,               # bulkheads, steel
    t_base=1.5,
    bay_top=300.0,            # top face of the bay ceiling rails (mid rails are bay_top-40 .. bay_top)
    # drum (made: a wrapped 304 sheet on two laser-cut rings, see docs/design-rules.md 7b)
    drum_d=620.0, drum_l=550.0, drum_rim_r=None,   # drum_d is the outside diameter of the wrapped sheet
    drum_t=0.8, ring_t=2.0, ring_id=480.0,
    tab_n=30, tab_w=24.0, tab_h=20.0, tab_hole_d=4.5,
    seam_pitch=50.0, seam_inset=15.0, seam_hole_d=4.5, splice_w=60.0, splice_t=1.0,
    baffle_n=3, baffle_leg=40.0, baffle_len=480.0, baffle_hole_d=6.5,
    belt_track_w=40.0, roller_track_w=45.0,       # fastener-free zones on the wall (belt track centred on the pulley, 7a)
    baffle_hole_offsets=(-170.0, -50.0, 50.0, 170.0),   # along the baffle from its centre; clear of the belt track
    roller_inset=0.0,         # roller face flush with the drum end, so the roller runs over the ring (7b)
    drum_clear_bottom=20.0, drum_clear_top=18.5,   # 18.5 so the body comes out at 1000
    drum_front_y=50.0,        # front face of the drum
    door_opening_d=460.0,
    door_ring_od=560.0, door_ring_id=470.0, door_disc_d=540.0, t_door=2.0,
    # rollers (bought dryer drum rollers, two front and two rear; measure the kit)
    roller_d=60.0, roller_angle_deg=30.0, roller_shaft_hole_d=10.5,
    motor_pulley_d=30.0,
    # lint filter slot in the front bulkhead (inside the drum, below the door opening)
    lint_slot_w=260.0, lint_slot_h=40.0, lint_slot_below_axis=270.0,
    # rear air inlet zone
    inlet_w=200.0, inlet_h=130.0, inlet_above_axis=50.0, inlet_hole_d=10.0, inlet_pitch=14.0,   # inside the ring opening (R 240)
    # riser duct
    riser_w=260.0, riser_depth=50.0,
    # console wedge
    console_face=160.0,       # length of the sloped face (holds the 120 mm aperture plus the 20 mm bands)
    console_y0=450.0,         # where the wedge starts on the top
    uci_ap_w=240.0, uci_ap_h=120.0, uci_hole_x=260.0, uci_hole_y=140.0, uci_hole_d=4.5,
    # fasteners
    m6_hole=6.5, m4_hole=4.5, panel_pitch=150.0,
    # bay layout (envelopes)
    motor_axis_z=120.0, motor_len=200.0, motor_d=140.0, motor_y0=190.0,   # motor behind the blower, pulley on its rear shaft
    blower_d=220.0, blower_w=100.0, blower_y0=84.0,                       # blower on the front shaft, inlet facing front
    lint_duct_depth=36.0,                                                 # between the front panel and the front bulkhead
    tray_w=320.0, tray_depth=250.0, tray_y0=420.0, tray_x0=-160.0, t_tray=1.5,
    pm_w=170.0, pm_depth=250.0, pm_h=180.0, pm_x0=-340.0, pm_y0=450.0,
    exhaust_d=102.0, exhaust_x=230.0, exhaust_z=150.0,
    cord_hole_d=22.0,         # hole for the cord strain relief bushing (PG16 / M20 style); confirm against the bushing bought, V-112
)
P["drum_rim_r"] = P["drum_d"] / 2
P["drum_flat_w"] = math.pi * (P["drum_d"] - P["drum_t"])   # sheet length at the mid-surface
P["drum_axis_z"] = P["bay_top"] + P["t_base"] + P["drum_clear_bottom"] + P["drum_d"] / 2
P["H_body"] = P["drum_axis_z"] + P["drum_d"] / 2 + P["drum_clear_top"] + P["ext"]
P["console_rise"] = P["console_face"] * math.sin(math.radians(45))
P["H_total"] = P["H_body"] + P["console_rise"]
P["front_bulk_y"] = P["ext"]                         # plate sits behind the front rails
P["rear_bulk_y"] = P["drum_front_y"] + P["drum_l"] + 10.0   # plate front face
P["rear_cross_y"] = P["rear_bulk_y"] + P["t_bulk"]  # rear cross rails start here
P["inner_w"] = P["W"] - 2 * P["ext"]                # 610 between the posts
P["half_w"] = P["W"] / 2
P["belt_y"] = P["motor_y0"] + P["motor_len"] + 12.0   # pulley centre on the rear shaft
P["belt_track_y"] = P["belt_y"] - P["drum_front_y"]   # belt track on the drum, in flat-pattern Y (from the front edge)
P["r_mid"] = (P["drum_d"] - P["drum_t"]) / 2          # sheet mid-surface radius; flat X maps to angle at this radius
for _off in P["baffle_hole_offsets"]:   # no baffle bolt in the belt track
    assert abs(P["drum_l"] / 2 + _off - P["belt_track_y"]) > P["belt_track_w"] / 2 + P["baffle_hole_d"] / 2, "baffle hole in the belt track"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
parts = []          # (name, solid, color, is_plate, thickness)
cut_list = []       # (item, profile, length_mm, qty, note)
STEEL = cq.Color(0.72, 0.72, 0.75)
ALU = cq.Color(0.85, 0.85, 0.88)
BOUGHT = cq.Color(0.95, 0.75, 0.55)
DRUM = cq.Color(0.80, 0.86, 0.95)
DUCT = cq.Color(0.90, 0.80, 0.70)


def add(name, solid, color=STEEL, plate=False, t=None):
    parts.append((name, solid, color, plate, t))
    return solid


def box(x0, x1, y0, y1, z0, z1):
    """Axis-aligned box from min/max corners."""
    return (cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False)
            .translate((x0, y0, z0)))


def extrusion(name, x0, x1, y0, y1, z0, z1, qty_note=""):
    """A 4040 or 2020 length as a box; records the cut list."""
    lengths = sorted([x1 - x0, y1 - y0, z1 - z0])
    profile = f"{int(lengths[0])}x{int(lengths[1])}" if lengths[0] == lengths[1] else f"{int(lengths[0])}x{int(lengths[1])}"
    cut_list.append((name, profile, round(lengths[2], 1), 1, qty_note))
    return add(name, box(x0, x1, y0, y1, z0, z1), ALU)


def plate_xz(name, x0, x1, z0, z1, y0, t, holes=(), rect_cuts=(), circ_cuts=(), slots=()):
    """A flat plate in the XZ plane (front/rear facing), thickness along +Y from y0.
    holes: (x, z, d). rect_cuts: (xc, zc, w, h). circ_cuts: (x, z, d). slots: (xc, zc, w, h) rounded ends."""
    w, h = x1 - x0, z1 - z0
    wp = cq.Workplane("XZ").center((x0 + x1) / 2, (z0 + z1) / 2).rect(w, h)
    solid = wp.extrude(-t).translate((0, y0, 0))   # XZ workplane normal is -Y, so extrude(-t) goes +Y
    for (x, z, d) in holes:
        solid = solid.cut(cq.Workplane("XZ").center(x, z).circle(d / 2).extrude(-t - 2).translate((0, y0 - 1, 0)))
    for (x, z, d) in circ_cuts:
        solid = solid.cut(cq.Workplane("XZ").center(x, z).circle(d / 2).extrude(-t - 2).translate((0, y0 - 1, 0)))
    for (xc, zc, cw, ch) in rect_cuts:
        solid = solid.cut(cq.Workplane("XZ").center(xc, zc).rect(cw, ch).extrude(-t - 2).translate((0, y0 - 1, 0)))
    for (xc, zc, cw, ch) in slots:
        solid = solid.cut(cq.Workplane("XZ").center(xc, zc).slot2D(cw, ch).extrude(-t - 2).translate((0, y0 - 1, 0)))
    add(name, solid, STEEL, plate=True, t=t)
    # 2D for DXF: same features, in plate-local coordinates (x right, y up)
    sk = cq.Workplane("XY").center((x0 + x1) / 2, (z0 + z1) / 2).rect(w, h).extrude(1)
    for (x, z, d) in list(holes) + list(circ_cuts):
        sk = sk.cut(cq.Workplane("XY").center(x, z).circle(d / 2).extrude(3).translate((0, 0, -1)))
    for (xc, zc, cw, ch) in rect_cuts:
        sk = sk.cut(cq.Workplane("XY").center(xc, zc).rect(cw, ch).extrude(3).translate((0, 0, -1)))
    for (xc, zc, cw, ch) in slots:
        sk = sk.cut(cq.Workplane("XY").center(xc, zc).slot2D(cw, ch).extrude(3).translate((0, 0, -1)))
    export_dxf(name, sk)
    return solid


def plate_xy(name, x0, x1, y0, y1, z0, t, holes=(), rect_cuts=(), circ_cuts=()):
    """A flat plate in the XY plane (horizontal), thickness along +Z from z0."""
    w, d = x1 - x0, y1 - y0
    solid = cq.Workplane("XY").center((x0 + x1) / 2, (y0 + y1) / 2).rect(w, d).extrude(t).translate((0, 0, z0))
    for (x, y, dd) in list(holes) + list(circ_cuts):
        solid = solid.cut(cq.Workplane("XY").center(x, y).circle(dd / 2).extrude(t + 2).translate((0, 0, z0 - 1)))
    for (xc, yc, cw, ch) in rect_cuts:
        solid = solid.cut(cq.Workplane("XY").center(xc, yc).rect(cw, ch).extrude(t + 2).translate((0, 0, z0 - 1)))
    add(name, solid, STEEL, plate=True, t=t)
    sk = cq.Workplane("XY").center((x0 + x1) / 2, (y0 + y1) / 2).rect(w, d).extrude(1)
    for (x, y, dd) in list(holes) + list(circ_cuts):
        sk = sk.cut(cq.Workplane("XY").center(x, y).circle(dd / 2).extrude(3).translate((0, 0, -1)))
    for (xc, yc, cw, ch) in rect_cuts:
        sk = sk.cut(cq.Workplane("XY").center(xc, yc).rect(cw, ch).extrude(3).translate((0, 0, -1)))
    export_dxf(name, sk)
    return solid


def plate_yz(name, y0, y1, z0, z1, x0, t, holes=()):
    """A flat plate in the YZ plane (side panel), thickness along +X from x0. holes: (y, z, d)."""
    d, h = y1 - y0, z1 - z0
    solid = cq.Workplane("YZ").center((y0 + y1) / 2, (z0 + z1) / 2).rect(d, h).extrude(t).translate((x0, 0, 0))
    for (y, z, dd) in holes:
        solid = solid.cut(cq.Workplane("YZ").center(y, z).circle(dd / 2).extrude(t + 2).translate((x0 - 1, 0, 0)))
    add(name, solid, STEEL, plate=True, t=t)
    sk = cq.Workplane("XY").center((y0 + y1) / 2, (z0 + z1) / 2).rect(d, h).extrude(1)
    for (y, z, dd) in holes:
        sk = sk.cut(cq.Workplane("XY").center(y, z).circle(dd / 2).extrude(3).translate((0, 0, -1)))
    export_dxf(name, sk)
    return solid


def export_dxf(name, sketch_solid):
    # re-wrap the solid in a fresh workplane so the DXF comes out in world coordinates, not about the sketch centre
    sec = cq.Workplane("XY").newObject([sketch_solid.val()]).section(0.5)
    path = os.path.join(OUT, "drawings", f"{name}.dxf")
    exporters.export(sec, path)
    try:   # put every entity on a layer called CUT, which is what laser shops ask for; harmless if ezdxf is missing
        import ezdxf
        doc = ezdxf.readfile(path)
        if "CUT" not in doc.layers:
            doc.layers.add("CUT")
        for ent in doc.modelspace():
            ent.dxf.layer = "CUT"
        doc.saveas(path)
    except ImportError:
        pass


def pitch_points(a0, a1, pitch, inset):
    """Hole positions along a run from a0 to a1 with the given pitch, inset from the ends."""
    a, b = a0 + inset, a1 - inset
    n = max(1, int(round((b - a) / pitch)))
    return [a + i * (b - a) / n for i in range(n + 1)]


# ---------------------------------------------------------------------------
# Frame (4040) and tray rails (2020)
# ---------------------------------------------------------------------------
e, hw, D = P["ext"], P["half_w"], P["D"]
Hb = P["H_body"]
bt = P["bay_top"]
ry = P["rear_cross_y"]

# posts
for i, (x0, y0) in enumerate([(-hw, 0), (hw - e, 0), (-hw, D - e), (hw - e, D - e)]):
    extrusion(f"post-{i+1}", x0, x0 + e, y0, y0 + e, 0, Hb, "corner post")

levels = {"bottom": (0, e), "mid": (bt - e, bt), "top": (Hb - e, Hb)}
for lvl, (z0, z1) in levels.items():
    if lvl == "mid":
        extrusion("rail-mid-front-left", -hw + e, -170, 0, e, z0, z1, "front stub, lint duct passes between the stubs")
        extrusion("rail-mid-front-right", 170, hw - e, 0, e, z0, z1, "front stub")
    else:
        extrusion(f"rail-{lvl}-front", -hw + e, hw - e, 0, e, z0, z1, "end rail")
    extrusion(f"rail-{lvl}-rear", -hw + e, hw - e, D - e, D, z0, z1, "end rail")
    extrusion(f"rail-{lvl}-left", -hw, -hw + e, e, D - e, z0, z1, "side rail")
    extrusion(f"rail-{lvl}-right", hw - e, hw, e, D - e, z0, z1, "side rail")
    if lvl in ("mid", "top"):
        extrusion(f"rail-{lvl}-rearcross", -hw + e, hw - e, ry, ry + e, z0, z1, "rear bulkhead cross rail")

# tray rails: 2020 on top of the bottom frame, running front to back, 600 long
es = P["ext_small"]
tx0 = P["tray_x0"]
for i, x in enumerate([tx0 - 10, tx0 + P["tray_w"] - 10]):
    extrusion(f"tray-rail-{i+1}", x, x + es, e + 300, D - e - 10, e, e + es, "2020 tray rail")

# ---------------------------------------------------------------------------
# Bulkheads
# ---------------------------------------------------------------------------
az = P["drum_axis_z"]
tb = P["t_bulk"]
bulk_x0, bulk_x1 = -P["inner_w"] / 2, P["inner_w"] / 2
bulk_z0, bulk_z1 = bt - e + 5, Hb - 5

# mounting holes: along the top edge (into the top front rail / top rear cross rail) and bottom edge (mid rails)
def bulk_holes(front=False):
    hs = []
    for x in pitch_points(bulk_x0, bulk_x1, P["panel_pitch"], 30):
        if not front or abs(x) >= 190:
            hs.append((x, bt - e / 2, P["m6_hole"]))
        hs.append((x, Hb - e / 2, P["m6_hole"]))
    return hs

# roller shaft holes, the same pattern on both bulkheads: on the rim radius plus the roller radius, 30 degrees each side of bottom
rollers = []
rr = P["drum_rim_r"] + P["roller_d"] / 2
for ang in (-P["roller_angle_deg"], P["roller_angle_deg"]):
    rollers.append((rr * math.sin(math.radians(ang)), az - rr * math.cos(math.radians(ang)), P["roller_shaft_hole_d"]))

# front bulkhead: door opening, lint slot, front roller holes
plate_xz("front-bulkhead", bulk_x0, bulk_x1, bulk_z0, bulk_z1, P["front_bulk_y"], tb,
         holes=bulk_holes(front=True) + rollers,
         circ_cuts=[(0, az, P["door_opening_d"])],
         slots=[(0, az - P["lint_slot_below_axis"], P["lint_slot_w"], P["lint_slot_h"])])

# rear bulkhead: inlet hole field, roller shaft holes, mounting holes
inlet = []
nx = int(P["inlet_w"] // P["inlet_pitch"])
nz = int(P["inlet_h"] // P["inlet_pitch"])
for i in range(nx):
    for j in range(nz):
        x = -P["inlet_w"] / 2 + P["inlet_pitch"] / 2 + i * P["inlet_pitch"]
        z = az + P["inlet_above_axis"] + j * P["inlet_pitch"]
        inlet.append((x, z, P["inlet_hole_d"]))
plate_xz("rear-bulkhead", bulk_x0, bulk_x1, bulk_z0, bulk_z1, P["rear_bulk_y"], tb,
         holes=bulk_holes() + rollers + inlet)

# ---------------------------------------------------------------------------
# Bay ceiling plate (drum compartment floor) and base pan
# ---------------------------------------------------------------------------
tp = P["t_panel"]
# The plate starts 0.5 mm behind the front bulkhead. In front of the bulkhead the mid front stubs and the
# lint duct close the bay; a full-width plate there would be cut into loose strips by the bulkhead slot.
P["ceil_y0"] = P["front_bulk_y"] + tb + 0.5
ceil_holes = []
for x in pitch_points(-hw + e, hw - e, P["panel_pitch"], 40):
    ceil_holes.append((x, ry + e / 2, P["m6_hole"]))     # into the mid rear cross rail
    ceil_holes.append((x, D - e / 2, P["m6_hole"]))      # into the mid rear end rail
for y in pitch_points(e, D - e, P["panel_pitch"], 40):
    ceil_holes.append((-hw + e / 2, y, P["m6_hole"]))    # into the mid side rails
    ceil_holes.append((hw - e / 2, y, P["m6_hole"]))
plate_xy("bay-ceiling", -hw + tp, hw - tp, P["ceil_y0"], D, bt, P["t_base"], holes=ceil_holes,
         rect_cuts=[(0, P["belt_y"], 40, 90),                       # belt slot, centred on the pulley
                    (0, P["rear_bulk_y"] + tb / 2, P["inner_w"] + 2, tb + 1),    # rear bulkhead passes through
                    (-hw + e / 2, D - e / 2, e + 1, e + 1), (hw - e / 2, D - e / 2, e + 1, e + 1),   # rear post notches
                    (0, ry + e + 2 + P["riser_depth"] / 2, P["riser_w"] + 4, P["riser_depth"] + 4)])   # riser, 2 mm clearance

base_holes = []
for x in pitch_points(-hw + e, hw - e, P["panel_pitch"], 40):
    base_holes.append((x, e / 2, P["m6_hole"])); base_holes.append((x, D - e / 2, P["m6_hole"]))
for y in pitch_points(e, D - e, P["panel_pitch"], 40):
    base_holes.append((-hw + e / 2, y, P["m6_hole"])); base_holes.append((hw - e / 2, y, P["m6_hole"]))
plate_xy("base-pan", -hw + tp, hw - tp, 0, D, -P["t_base"], P["t_base"], holes=base_holes)   # no cuts; the exhaust leaves through the rear lower panel

# ---------------------------------------------------------------------------
# Outer panels
# ---------------------------------------------------------------------------
def side_holes():
    hs = []
    for z in pitch_points(0, Hb, P["panel_pitch"], 60):
        hs.append((e / 2, z, P["m6_hole"])); hs.append((D - e / 2, z, P["m6_hole"]))
    for y in pitch_points(e, D - e, P["panel_pitch"], 60):
        for lvl, (z0, z1) in levels.items():
            hs.append((y, (z0 + z1) / 2, P["m6_hole"]))
    return hs

plate_yz("side-panel-left", 0, D, 0, Hb, -hw - tp, tp, holes=side_holes())
plate_yz("side-panel-right", 0, D, 0, Hb, hw, tp, holes=side_holes())

def end_holes(z0, z1, extra_levels, stubs_only_at=None):
    """Holes down both posts between z0 and z1, plus a row along each rail centre line in extra_levels.
    stubs_only_at: the Z of a row that lands on the mid front stubs, which only exist beyond X 170."""
    hs = []
    for z in pitch_points(z0, z1, P["panel_pitch"], 60):
        hs.append((-hw + e / 2, z, P["m6_hole"])); hs.append((hw - e / 2, z, P["m6_hole"]))
    for x in pitch_points(-hw + e, hw - e, P["panel_pitch"], 60):
        for zc in extra_levels:
            if stubs_only_at is not None and zc == stubs_only_at and abs(x) < 190:
                continue
            hs.append((x, zc, P["m6_hole"]))
    return hs

# The front and rear panels split at the bottom of the mid rail (260) so the upper panel bolts to the mid rail,
# the top rail and the posts, and the lower panel to the bottom rail and the posts. The lower panel comes off
# to reach the bay. The upper panel carries the door ring opening; the lower panels carry the louvers.
P["panel_split_z"] = bt - e
plate_xz("front-upper-panel", -hw, hw, P["panel_split_z"], Hb, -tp, tp,
         holes=end_holes(P["panel_split_z"], Hb, [bt - e / 2, Hb - e / 2], stubs_only_at=bt - e / 2),
         circ_cuts=[(0, az, P["door_ring_id"] + 10)])
louvers = [(x, z, 60, 5) for x in (-240, -160, -80, 0, 80, 160, 240) for z in range(80, 240, 20)]
plate_xz("front-lower-panel", -hw, hw, 0, P["panel_split_z"] - 1, -tp, tp,
         holes=end_holes(0, P["panel_split_z"] - 1, [e / 2]), slots=louvers)
plate_xz("rear-upper-panel", -hw, hw, P["panel_split_z"], Hb, D, tp, holes=end_holes(P["panel_split_z"], Hb, [bt - e / 2, Hb - e / 2]))
rear_louvers = [(x, z, 60, 5) for x in (-160, -80, 0, 80) for z in range(80, 240, 20)]   # clear of the exhaust port and the cord entry
plate_xz("rear-lower-panel", -hw, hw, 0, P["panel_split_z"] - 1, D, tp,
         holes=end_holes(0, P["panel_split_z"] - 1, [e / 2]),
         circ_cuts=[(P["exhaust_x"], P["exhaust_z"], P["exhaust_d"] + 4),     # exhaust collar, 2 mm clearance
                    (-250, 120, P["cord_hole_d"])],                             # cord strain relief bushing, in front of the power module
         slots=rear_louvers)

# top panel in front of the console, and the console wedge (sloped face with the UCI aperture, cap, two cheeks)
top_holes = []
for x in pitch_points(-hw + e, hw - e, P["panel_pitch"], 60):
    top_holes.append((x, e / 2, P["m6_hole"]))
for y in pitch_points(e, P["console_y0"] - tp, P["panel_pitch"], 60):
    top_holes.append((-hw + e / 2, y, P["m6_hole"])); top_holes.append((hw - e / 2, y, P["m6_hole"]))
plate_xy("top-panel", -hw, hw, 0, P["console_y0"] - tp, Hb, tp, holes=top_holes)   # stops 1.5 short of the face plate's outer corner

cy0, cf, cr = P["console_y0"], P["console_face"], P["console_rise"]
# sloped face: build as a plate in a tilted workplane; aperture and 4 holes
face = (cq.Workplane("XY").rect(P["W"] - 2 * tp, cf).extrude(tp)
        .faces(">Z").workplane().rect(P["uci_ap_w"], P["uci_ap_h"]).cutThruAll()
        .faces(">Z").workplane().pushPoints([(sx * P["uci_hole_x"] / 2, sy * P["uci_hole_y"] / 2) for sx in (-1, 1) for sy in (-1, 1)]).hole(P["uci_hole_d"]))
# +45 about X: the plate rises toward the rear and its outward normal is (0, -0.707, 0.707), front and up.
# (Draft 2 had -45 here, which laid the face the wrong way; found by the section audit, see docs/verification.md V-010.)
face = face.rotate((0, 0, 0), (1, 0, 0), 45).translate((0, cy0 + cr / 2, Hb + cr / 2))
add("console-face", face, STEEL, plate=True, t=tp)
sk = (cq.Workplane("XY").rect(P["W"] - 2 * tp, cf).extrude(1)
      .cut(cq.Workplane("XY").rect(P["uci_ap_w"], P["uci_ap_h"]).extrude(3).translate((0, 0, -1))))
for sx in (-1, 1):
    for sy in (-1, 1):
        sk = sk.cut(cq.Workplane("XY").center(sx * P["uci_hole_x"] / 2, sy * P["uci_hole_y"] / 2).circle(P["uci_hole_d"] / 2).extrude(3).translate((0, 0, -1)))
export_dxf("console-face", sk)
plate_xy("console-cap", -hw, hw, cy0 + cr, D, Hb + cr, tp)
for side, x0 in (("left", -hw), ("right", hw - tp)):
    cheek = (cq.Workplane("YZ").polyline([(cy0, Hb), (cy0 + cr, Hb + cr), (D, Hb + cr), (D, Hb)]).close()
             .extrude(tp).translate((x0, 0, 0)))
    add(f"console-cheek-{side}", cheek, STEEL, plate=True, t=tp)
    sk = cq.Workplane("XY").polyline([(cy0, Hb), (cy0 + cr, Hb + cr), (D, Hb + cr), (D, Hb)]).close().extrude(1)
    export_dxf(f"console-cheek-{side}", sk)

# ---------------------------------------------------------------------------
# Door: ring on the front panel, disc, hinge side marked by holes
# ---------------------------------------------------------------------------
ring = (cq.Workplane("XZ").center(0, az).circle(P["door_ring_od"] / 2).circle(P["door_ring_id"] / 2)
        .extrude(-P["t_door"]).translate((0, -tp - P["t_door"], 0)))
add("door-ring", ring, STEEL, plate=True, t=P["t_door"])
sk = cq.Workplane("XY").circle(P["door_ring_od"] / 2).extrude(1).cut(cq.Workplane("XY").circle(P["door_ring_id"] / 2).extrude(3).translate((0, 0, -1)))
export_dxf("door-ring", sk)
disc = (cq.Workplane("XZ").center(0, az).circle(P["door_disc_d"] / 2).extrude(-P["t_door"])
        .translate((0, -tp - 2 * P["t_door"] - 8, 0)))
add("door-disc", disc, STEEL, plate=True, t=P["t_door"])
export_dxf("door-disc", cq.Workplane("XY").circle(P["door_disc_d"] / 2).extrude(1))

# ---------------------------------------------------------------------------
# Ducts: riser (behind the rear bulkhead, from the bay to the inlet zone) and lint duct (front)
# ---------------------------------------------------------------------------
riser_top = az + P["inlet_above_axis"] + P["inlet_h"] + 10
add("riser-duct", box(-P["riser_w"] / 2, P["riser_w"] / 2, ry + e + 2, ry + e + 2 + P["riser_depth"], bt - 120, riser_top), DUCT)
assert ry + e + 2 + P["riser_depth"] + 2 <= D - e, "riser must clear the rear end rail"
add("lint-duct", box(-168, 168, 2, 2 + P["lint_duct_depth"], 150, az - P["lint_slot_below_axis"] + P["lint_slot_h"] / 2), DUCT)   # 2 mm from each front stub
add("lint-duct-transition", box(-110, 110, 2 + P["lint_duct_depth"], P["blower_y0"], 50, 190), DUCT)

# ---------------------------------------------------------------------------
# Bought parts as envelopes
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# Drum: wrapped sheet, two rings, splice strip, angle baffles (all made), four rollers (bought)
# ---------------------------------------------------------------------------
ro, ri = P["drum_d"] / 2, P["drum_d"] / 2 - P["drum_t"]
y0d, L = P["drum_front_y"], P["drum_l"]
rm = P["r_mid"]


def about_axis(shape, theta_deg):
    """Turn a shape built at angle 0 (pointing +X from the drum axis) to angle theta in the XZ plane
    (theta 90 is the top of the drum), then lift it to the drum axis."""
    return shape.rotate((0, 0, 0), (0, 1, 0), -theta_deg).translate((0, 0, az))


def radial_hole(theta_deg, y, d, r0, r1):
    """A cylinder along the radius at angle theta, from radius r0 to r1, for cutting holes in curved parts."""
    cyl = cq.Workplane("YZ").center(y, 0).circle(d / 2).extrude(r1 - r0).translate((r0, 0, 0))
    return about_axis(cyl, theta_deg)


def flat_x_to_theta(x):
    """Flat-pattern X (0 at the seam) to drum angle in degrees; the seam is at the top (90)."""
    return 90.0 + math.degrees(x / rm)


# seam holes: down both short edges of the flat sheet, 50 mm pitch, clear of the belt track and the roller tracks
seam_ys = []
y = P["roller_track_w"] + 10
while y <= L - P["roller_track_w"] - 10:
    if abs(y - P["belt_track_y"]) > P["belt_track_w"] / 2 + 5:
        seam_ys.append(y)
    y += P["seam_pitch"]
seam_thetas = (flat_x_to_theta(P["seam_inset"]), flat_x_to_theta(P["drum_flat_w"] - P["seam_inset"]))
tab_thetas = [flat_x_to_theta(P["drum_flat_w"] * (i + 0.5) / P["tab_n"]) for i in range(P["tab_n"])]
baffle_thetas = [flat_x_to_theta(P["drum_flat_w"] * (i + 0.5) / P["baffle_n"]) for i in range(P["baffle_n"])]
baffle_ys = [y0d + L / 2 + off for off in P["baffle_hole_offsets"]]
r_tab_hole = ri - P["tab_h"] / 2

# the sheet: a thin cylinder with 30 tabs folded in against each ring face (sharp fold, bend allowance left to V-208)
shell = cq.Workplane("XZ").center(0, az).circle(ro).circle(ri).extrude(-L).translate((0, y0d, 0))
for theta in tab_thetas:
    for (ya, yb) in ((y0d - P["drum_t"], y0d), (y0d + L, y0d + L + P["drum_t"])):
        tab = box(ri - P["tab_h"], ro, ya, yb, -P["tab_w"] / 2, P["tab_w"] / 2)   # root reaches the sheet so the fold is one body
        tab = tab.intersect(cq.Workplane("XZ").circle(ro).extrude(-(yb - ya) - 2).translate((0, ya - 1, 0)))   # root follows the sheet's outside
        tab = tab.cut(cq.Workplane("XZ").center(r_tab_hole, 0).circle(P["tab_hole_d"] / 2).extrude(-4).translate((0, ya - 1, 0)))
        shell = shell.union(about_axis(tab, theta))
for theta in seam_thetas:
    for yy in seam_ys:
        shell = shell.cut(radial_hole(theta, y0d + yy, P["seam_hole_d"], ri - 2, ro + 2))
for theta in baffle_thetas:
    for yy in baffle_ys:
        shell = shell.cut(radial_hole(theta, yy, P["baffle_hole_d"], ri - 2, ro + 2))
add("drum-sheet", shell, DRUM, plate=True, t=P["drum_t"])

# the rings: 2 mm, outside on the sheet's inside, 30 tab holes
for name, yy in (("drum-ring-front", y0d), ("drum-ring-rear", y0d + L - P["ring_t"])):
    ring_s = cq.Workplane("XZ").center(0, az).circle(ri).circle(P["ring_id"] / 2).extrude(-P["ring_t"]).translate((0, yy, 0))
    for theta in tab_thetas:
        ring_s = ring_s.cut(about_axis(cq.Workplane("XZ").center(r_tab_hole, 0).circle(P["tab_hole_d"] / 2).extrude(-P["ring_t"] - 2).translate((0, yy - 1, 0)), theta))
    add(name, ring_s, DRUM, plate=True, t=P["ring_t"])

# the splice strip: inside the sheet under the seam (top of the drum), between the rings, holes on the seam holes
half_ang = math.degrees((P["splice_w"] / 2) / ri)
spl_len = L - 2 * P["ring_t"] - 2
splice = (cq.Workplane("XZ").center(0, az).circle(ri).circle(ri - P["splice_t"]).extrude(-spl_len)
          .translate((0, y0d + P["ring_t"] + 1, 0)))
keep = (cq.Workplane("XY").box(2 * ri * math.sin(math.radians(half_ang)) + 0.01, spl_len + 2, 2 * ri, centered=(True, False, False))
        .translate((0, y0d + P["ring_t"], az)))
splice = splice.intersect(keep)
for theta in seam_thetas:
    for yy in seam_ys:
        splice = splice.cut(radial_hole(theta, y0d + yy, P["seam_hole_d"], ri - 4, ri + 2))
add("drum-splice", splice, DRUM, plate=True, t=P["splice_t"])

# the baffles: catalog 40x40x3 aluminium angle, 480 long, the wall leg bolted through the sheet's baffle holes.
# The flat leg sits 0.7 mm off the curved wall at its centre line so its edges clear the wall (sagitta of a 40 chord on R 309).
d_leg = math.sqrt(ri ** 2 - (P["baffle_leg"] / 2) ** 2) - 0.05
tb_ang = 3.0
for i, theta in enumerate(baffle_thetas):
    yb0, yb1 = y0d + L / 2 - P["baffle_len"] / 2, y0d + L / 2 + P["baffle_len"] / 2
    leg_wall = box(d_leg - tb_ang, d_leg, yb0, yb1, -P["baffle_leg"] / 2, P["baffle_leg"] / 2)
    leg_up = box(d_leg - P["baffle_leg"], d_leg, yb0, yb1, P["baffle_leg"] / 2 - tb_ang, P["baffle_leg"] / 2)
    ang_s = leg_wall.union(leg_up)
    for yy in baffle_ys:
        ang_s = ang_s.cut(cq.Workplane("YZ").center(yy, 0).circle(P["baffle_hole_d"] / 2).extrude(tb_ang + 4).translate((d_leg - tb_ang - 2, 0, 0)))
    add(f"baffle-{i+1} (angle, cut to length)", about_axis(ang_s, theta), BOUGHT)
cut_list.append(("baffle-1..3", "angle 40x40x3 aluminum", P["baffle_len"], 3, "drum baffles, drilled on the drill press"))

# flat patterns for the drum sheet, the rings, and the splice (plate-local coordinates, mm)
def drum_sheet_sketch():
    W, L = P["drum_flat_w"], P["drum_l"]
    sk = cq.Workplane("XY").center(W / 2, L / 2).rect(W, L).extrude(1)
    pitch = W / P["tab_n"]
    for i in range(P["tab_n"]):
        xc = pitch * (i + 0.5)
        for yc, sign in ((L + P["tab_h"] / 2, 1), (-P["tab_h"] / 2, -1)):
            sk = sk.union(cq.Workplane("XY").center(xc, yc).rect(P["tab_w"], P["tab_h"]).extrude(1))
            sk = sk.cut(cq.Workplane("XY").center(xc, yc + sign * 0).circle(P["tab_hole_d"] / 2).extrude(3).translate((0, 0, -1)))
    # seam holes along both short edges (same list as the solid: clear of the belt track and the roller tracks)
    for xc in (P["seam_inset"], W - P["seam_inset"]):
        for yc in seam_ys:
            sk = sk.cut(cq.Workplane("XY").center(xc, yc).circle(P["seam_hole_d"] / 2).extrude(3).translate((0, 0, -1)))
    # baffle holes: three columns, four holes each
    for i in range(P["baffle_n"]):
        xc = W * (i + 0.5) / P["baffle_n"]
        for off in P["baffle_hole_offsets"]:
            sk = sk.cut(cq.Workplane("XY").center(xc, L / 2 + off).circle(P["baffle_hole_d"] / 2).extrude(3).translate((0, 0, -1)))
    return sk
sheet_sk = drum_sheet_sketch()
export_dxf("drum-sheet", sheet_sk)
ring_sk = cq.Workplane("XY").circle(ri).extrude(1).cut(cq.Workplane("XY").circle(P["ring_id"] / 2).extrude(3).translate((0, 0, -1)))
r_hole = r_tab_hole
for i in range(P["tab_n"]):
    a = math.radians(tab_thetas[i])   # same angles as the solid, so the drawing and the model overlay
    ring_sk = ring_sk.cut(cq.Workplane("XY").center(r_hole * math.cos(a), r_hole * math.sin(a)).circle(P["tab_hole_d"] / 2).extrude(3).translate((0, 0, -1)))
export_dxf("drum-ring", ring_sk)
spl_sk = cq.Workplane("XY").center(P["splice_w"] / 2, spl_len / 2).rect(P["splice_w"], spl_len).extrude(1)
for xc in (P["seam_inset"], P["splice_w"] - P["seam_inset"]):
    for yc in seam_ys:
        spl_sk = spl_sk.cut(cq.Workplane("XY").center(xc, yc - P["ring_t"] - 1).circle(P["seam_hole_d"] / 2).extrude(3).translate((0, 0, -1)))
export_dxf("drum-splice", spl_sk)

# belt length for a belt around the drum and the motor pulley (two-pulley approximation, before the idler)
C = az - P["motor_axis_z"]
Dd, dd = P["drum_d"], P["motor_pulley_d"]
belt_len = 2 * C + math.pi * (Dd + dd) / 2 + (Dd - dd) ** 2 / (4 * C)
P["belt_len_est"] = belt_len
cut_list.append(("belt (bought)", "PJ poly-V, 4 or 5 ribs", round(belt_len), 1, "two-pulley estimate before the idler; pick the nearest catalog J length (V-012)"))
mz, my0 = P["motor_axis_z"], P["motor_y0"]
motor = cq.Workplane("XZ").center(0, mz).circle(P["motor_d"] / 2).extrude(-P["motor_len"]).translate((0, my0, 0))
add("motor (bought)", motor, BOUGHT)
add("pulley (bought)", cq.Workplane("XZ").center(0, mz).circle(P["motor_pulley_d"] / 2).extrude(-16).translate((0, my0 + P["motor_len"] + 4, 0)), BOUGHT)
blower = cq.Workplane("XZ").center(0, mz).circle(P["blower_d"] / 2).extrude(-P["blower_w"]).translate((0, P["blower_y0"], 0))
add("blower (bought)", blower, BOUGHT)
add("heat-module-tray", box(P["tray_x0"], P["tray_x0"] + P["tray_w"], P["tray_y0"], P["tray_y0"] + P["tray_depth"], e + es, e + es + P["t_tray"]), STEEL)
add("heat-module (envelope)", box(P["tray_x0"] + 20, P["tray_x0"] + P["tray_w"] - 20, P["tray_y0"] + 20, P["tray_y0"] + P["tray_depth"] - 20, e + es + 2, e + es + 2 + 160), BOUGHT)
add("power-module (envelope)", box(P["pm_x0"], P["pm_x0"] + P["pm_w"], P["pm_y0"], P["pm_y0"] + P["pm_depth"], e, e + P["pm_h"]), BOUGHT)
exh = (cq.Workplane("XZ").center(P["exhaust_x"], P["exhaust_z"]).circle(P["exhaust_d"] / 2).extrude(-(D - P["blower_y0"] - P["blower_w"]))
       .translate((0, P["blower_y0"] + P["blower_w"], 0)))
add("exhaust-duct (bought)", exh, DUCT)
roller_w = 25.0   # catalog roller width, measured at V-106
for i, (x, z, d) in enumerate(rollers):
    r = cq.Workplane("XZ").center(x, z).circle(P["roller_d"] / 2).extrude(-roller_w).translate((0, y0d + L - P["roller_inset"] - roller_w, 0))
    add(f"roller-rear-{i+1} (bought)", r, BOUGHT)
    r = cq.Workplane("XZ").center(x, z).circle(P["roller_d"] / 2).extrude(-roller_w).translate((0, y0d + P["roller_inset"], 0))
    add(f"roller-front-{i+1} (bought)", r, BOUGHT)

# ---------------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------------
assy = cq.Assembly(name="osa-dryer")
for name, solid, color, plate, t in parts:
    assy.add(solid, name=name, color=color)
assy.save(os.path.join(OUT, "step", "osa-dryer-assembly.step"))
for name, solid, color, plate, t in parts:
    if "(" in name:   # bought parts, envelopes, and cut-to-length catalog stock get no STEP of their own
        continue
    exporters.export(solid, os.path.join(OUT, "step", f"{name}.step"))

with open(os.path.join(OUT, "drawings", "frame-cut-list.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["item", "profile", "length_mm", "qty", "note"])
    for row in cut_list:
        w.writerow(row)

import re

def export_view(shape, vname, pdir, turn):
    """Write a check view. The SVG exporter picks its own 'up', so each view is turned afterwards:
    turn = 0, 90 (clockwise), 180, or 270."""
    path = os.path.join(OUT, "drawings", f"view-{vname}.svg")
    w, h = 1400, 1000
    exporters.export(shape, path, opt={"projectionDir": pdir, "width": w, "height": h, "showHidden": False, "marginLeft": 20, "marginTop": 20})
    s = open(path, encoding="utf-8").read()
    m = re.search(r"<svg[^>]*>", s)
    head, body = s[:m.end()], s[m.end():]
    body = body[: body.rfind("</svg>")]
    if turn == 90:
        head = re.sub(r'width="[^"]*"', f'width="{h}"', head, count=1); head = re.sub(r'height="[^"]*"', f'height="{w}"', head, count=1)
        head = re.sub(r'viewBox="[^"]*"', f'viewBox="0 0 {h} {w}"', head, count=1)
        body = f'<g transform="translate({h},0) rotate(90)">{body}</g>'
    elif turn == 180:
        body = f'<g transform="translate({w},{h}) rotate(180)">{body}</g>'
    elif turn == 270:
        head = re.sub(r'width="[^"]*"', f'width="{h}"', head, count=1); head = re.sub(r'height="[^"]*"', f'height="{w}"', head, count=1)
        head = re.sub(r'viewBox="[^"]*"', f'viewBox="0 0 {h} {w}"', head, count=1)
        body = f'<g transform="translate(0,{w}) rotate(-90)">{body}</g>'
    label = f'<text x="20" y="30" font-family="Helvetica, Arial, sans-serif" font-size="18">osa-dryer check view: {vname} (draft 1, not for cutting)</text>'
    open(path, "w", encoding="utf-8").write(head + body + label + "</svg>")

compound = cq.Compound.makeCompound([s.val() if hasattr(s, "val") else s for _, s, _, _, _ in parts])
OUTER = ("side-panel-left", "side-panel-right", "front-upper-panel", "front-lower-panel", "rear-upper-panel",
         "rear-lower-panel", "top-panel", "console-face", "console-cap", "console-cheek-left", "console-cheek-right",
         "door-ring", "door-disc")
inner = cq.Compound.makeCompound([s.val() for n, s, _, _, _ in parts if n not in OUTER])
VIEWS = {
    "iso": (compound, (1, -1, 0.7), 180),
    "front": (compound, (0, -1, 0), 90),
    "side-left": (compound, (-1, 0, 0), 90),
    "top": (compound, (0, 0, 1), 90),
    "iso-inside": (inner, (1, -1, 0.7), 180),
    "side-inside": (inner, (-1, 0, 0), 90),
    "front-inside": (inner, (0, -1, 0), 90),
}
for vname, (shape, pdir, turn) in VIEWS.items():
    export_view(shape, vname, pdir, turn)

print("parts:", len(parts), " plates:", sum(1 for p in parts if p[3]), " extrusions:", len(cut_list))

# ---------------------------------------------------------------------------
# Interference check (verification V-010): python3 osa_dryer_cad.py <out> --check
# ---------------------------------------------------------------------------
if "--check" in sys.argv:
    import itertools
    solids = [(n, s.val()) for n, s, _, _, _ in parts]
    bad = []
    for (na, a), (nb, b) in itertools.combinations(solids, 2):
        try:
            bba, bbb = a.BoundingBox(), b.BoundingBox()
            if (bba.xmax < bbb.xmin or bbb.xmax < bba.xmin or bba.ymax < bbb.ymin or bbb.ymax < bba.ymin
                    or bba.zmax < bbb.zmin or bbb.zmax < bba.zmin):
                continue
            v = a.intersect(b).Volume()
        except Exception as ex:  # a failed boolean is reported, not hidden
            bad.append((na, nb, f"boolean failed: {ex}"))
            continue
        if v > 1.0:   # mm3; touching faces give 0
            bad.append((na, nb, round(v, 1)))
    if bad:
        print("INTERFERENCE:")
        for na, nb, v in bad:
            print(f"  {na}  x  {nb}  : {v}")
    else:
        print("interference check: no overlaps")
print("drum axis Z", P["drum_axis_z"], " H_body", P["H_body"], " H_total", round(P["H_total"], 1), " rear bulkhead Y", P["rear_bulk_y"])
print("drum sheet flat", round(P["drum_flat_w"], 1), "x", P["drum_l"], " belt estimate", round(P["belt_len_est"]))
