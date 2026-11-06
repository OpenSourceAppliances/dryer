"""osa-dryer parametric mechanical model.

One file holds every number. Run it and it writes:
  step/osa-dryer-assembly.step          the whole machine, bought parts as envelopes or representations
  step/<part>.step                      one file per part we make
  drawings/<part>.dxf                   flat pattern for every laser-cut plate (CUT layer)
  drawings/frame-cut-list.csv           every extrusion length
  drawings/view-*.svg                   views for checking, not for cutting

Coordinate system: X across the cabinet (left negative), Y from front (0) to back, Z up from the floor.
All dimensions mm. Needs cadquery (pip install cadquery). Also runs in FreeCAD's CadQuery workbench.

Status: draft 4, 2026-11-06. Draft 4 draws what the documents already called for but the model only
implied: T-slot profiles on the extrusions, laser corner radii, every panel bolt, the leveling feet, the belt
on its real path with the idler, the door hinges, handle, seal and catch, the Tier 0 control module, and
the detail of the motor, pulley and blower. Bought parts (motor, blower, timers, rollers, hinges, feet) are
drawn as representations from catalog numbers that have NOT been measured. docs/verification.md says which
measurement unlocks which DXF. Do not cut a plate whose gate is open.
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
    # --- draft 4: what the documents call for, now drawn ---
    plate_corner_r=6.0,       # laser-cut outside corners of every rectangular plate (no sharp sheet corners to handle)
    small_corner_r=3.0,       # cheeks, the splice strip, the drum tabs
    # T-slot profiles, generic European 8 mm slot 4040 and 6 mm slot 2020; the bought profile's own drawing governs (V-105)
    # slot: the opening, running to depth; the T-nut's band is under_w wide from the lip down to lip + band, its far
    # corners chamfered by cham so the diagonal webs to the profile's corners stay
    tslot_4040=dict(size=40.0, slot=8.2, lip=2.0, band=5.0, under_w=13.0, cham=3.0, depth=12.5, bore=6.8, corner_r=2.0),
    tslot_2020=dict(size=20.0, slot=6.2, lip=1.5, band=3.0, under_w=11.0, cham=2.5, depth=6.0, bore=4.2, corner_r=1.5),
    # panel bolts (design-rules 7c): M6 x 12 hex head with a flat washer, into a drop-in T-nut (the T-nut is not drawn)
    m6_bolt_len=12.0, m6_head_af=10.0, m6_head_h=4.0, m6_washer_d=12.0, m6_washer_t=1.6, m6_nut_af=10.0, m6_nut_h=5.0,
    # drum hardware (7b): M4 button heads and nuts on the tabs and the seam, M6 on the baffles (6.5 holes)
    m4_head_d=7.6, m4_head_h=2.2, m4_nut_af=7.0, m4_nut_h=3.2, m6_button_d=10.5, m6_button_h=3.3,
    # leveling feet (7c Feet): catalog M8 feet into the posts' tapped centre bores, through 8.5 holes in the base pan
    foot_pad_d=50.0, foot_pad_h=8.0, foot_hex_af=19.0, foot_hex_h=6.0, foot_stud_d=8.0, foot_stud_in=35.0, foot_hole_d=8.5,
    # belt and idler (7a Drive): PJ 5-rib belt, catalog flat idler on a sprung arm pressing the slack (left) run inward
    belt_w=12.0, belt_t=3.5, idler_d=40.0, idler_w=12.0, idler_x=-60.0, idler_z=165.0,
    belt_slot_w=40.0, belt_slot_l=90.0,   # one slot in the bay ceiling per belt run, centred where the run crosses the plate
    # door hardware (7a Door): two catalog flag hinges on the left, a D-handle on the right, a seal on the disc, a magnetic catch
    hinge_pin_d=8.0, hinge_knuckle_d=18.0, hinge_leaf_t=6.0, hinge_leaf_h=30.0, hinge_z_off=50.0, hinge_pin_x=-278.5, hinge_pin_y=-14.0,
    hinge_leaf_x_in=-245.0,   # inboard end of both leaves (clear of the seal)
    handle_bar_d=14.0, handle_span=128.0, handle_standoff=30.0, handle_x=220.0,
    seal_ri=237.0, seal_ro=246.0, seal_t=6.0,
    ring_bolt_r=257.5, ring_bolt_n=8,
    latch_x0=256.0, latch_x1=268.0,
    # felt seal (7a Drum and door): 8 mm polyester felt annulus glued to the rear bulkhead; the front one waits on the lint slot decision (V-010 finding)
    felt_ri=250.0, felt_ro=285.0, felt_t=8.0,
    # Tier 0 control module (controls/tier0-mechanical): faceplate numbers from mechanical/drawings/tier0_drawings.py
    fp_w=280.0, fp_h=160.0, fp_r=10.0, fp_t=2.0,
    knob_d=40.0, knob_skirt_h=3.0, knob_body_d=30.0, knob_h=20.0,
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
HARDWARE = cq.Color(0.55, 0.55, 0.58)
RUBBER = cq.Color(0.15, 0.15, 0.15)
FELT = cq.Color(0.55, 0.52, 0.48)
COS30 = math.cos(math.radians(30))


def add(name, solid, color=STEEL, plate=False, t=None):
    parts.append((name, solid, color, plate, t))
    return solid


def box(x0, x1, y0, y1, z0, z1):
    """Axis-aligned box from min/max corners."""
    return (cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False)
            .translate((x0, y0, z0)))


def orient(shape, n):
    """Turn a shape built along +Z so that +Z points along the vector n."""
    nx, ny, nz = n
    L = math.sqrt(nx * nx + ny * ny + nz * nz)
    nx, ny, nz = nx / L, ny / L, nz / L
    if nz > 1 - 1e-9:
        return shape
    if nz < -1 + 1e-9:
        return shape.rotate((0, 0, 0), (1, 0, 0), 180)
    return shape.rotate((0, 0, 0), (-ny, nx, 0.0), math.degrees(math.acos(nz)))   # about Z x n


def place(shape, p, n):
    return orient(shape, n).translate(p)


def hexagon(af, h):
    return cq.Workplane("XY").polygon(6, af / COS30).extrude(h)


def tslot_bar(spec, length):
    """A T-slot extrusion of the given length along +Z from z = 0, centred on the Z axis: four slots and the centre bore."""
    s, h = spec["size"], spec["size"] / 2
    bar = cq.Workplane("XY").rect(s, s).extrude(length).edges("|Z").fillet(spec["corner_r"])
    x_lip, x_far, w2, c = h - spec["lip"] + 0.01, h - spec["lip"] - spec["band"], spec["under_w"] / 2, spec["cham"]
    band = (cq.Workplane("XY").polyline([(x_lip, -w2), (x_far + c, -w2), (x_far, -w2 + c), (x_far, w2 - c), (x_far + c, w2), (x_lip, w2)])
            .close().extrude(length + 2).translate((0, 0, -1)))
    groove = box(h - spec["depth"], h + 1, -spec["slot"] / 2, spec["slot"] / 2, -1, length + 1).union(band)
    for ang in (0, 90, 180, 270):
        bar = bar.cut(groove.rotate((0, 0, 0), (0, 0, 1), ang))
    return bar.cut(cq.Workplane("XY").circle(spec["bore"] / 2).extrude(length + 2).translate((0, 0, -1)))


def extrusion(name, x0, x1, y0, y1, z0, z1, qty_note=""):
    """A 4040 or 2020 length with its T-slot profile; records the cut list."""
    sx, sy, sz = x1 - x0, y1 - y0, z1 - z0
    lengths = sorted([sx, sy, sz])
    profile = f"{int(lengths[0])}x{int(lengths[1])}"
    cut_list.append((name, profile, round(lengths[2], 1), 1, qty_note))
    spec = P["tslot_4040"] if abs(lengths[0] - 40) < 1e-6 else P["tslot_2020"]
    bar = tslot_bar(spec, lengths[2])
    if sx == lengths[2]:
        bar = bar.rotate((0, 0, 0), (0, 1, 0), 90).translate((x0, (y0 + y1) / 2, (z0 + z1) / 2))
    elif sy == lengths[2]:
        bar = bar.rotate((0, 0, 0), (1, 0, 0), -90).translate(((x0 + x1) / 2, y0, (z0 + z1) / 2))
    else:
        bar = bar.translate(((x0 + x1) / 2, (y0 + y1) / 2, z0))
    return add(name, bar, ALU)


# --- bolts, nuts and such. Every one is built along +Z with its bearing face at z = 0 and placed with place(shape, p, n):
#     p is the point on the surface it sits on, n the outward normal of that surface. Heads extend along +n, shanks along -n.
def hex_bolt_m6(length=None):
    L = length or P["m6_bolt_len"]
    wt, hh = P["m6_washer_t"], P["m6_head_h"]
    shank = cq.Workplane("XY").circle(3.0).extrude(L + wt + 1).translate((0, 0, -L)).faces("<Z").chamfer(0.5)
    washer = cq.Workplane("XY").circle(P["m6_washer_d"] / 2).extrude(wt)
    head = hexagon(P["m6_head_af"], hh).translate((0, 0, wt)).edges(">Z").chamfer(0.6)
    return shank.union(washer).union(head)


def button_bolt(d_shank, head_d, head_h, length, socket_af):
    head = cq.Workplane("XY").circle(head_d / 2).extrude(head_h).edges(">Z").fillet(head_h * 0.8)
    head = head.cut(hexagon(socket_af, 2).translate((0, 0, head_h - 1.2)))
    shank = cq.Workplane("XY").circle(d_shank / 2).extrude(length + 0.5).translate((0, 0, -length)).faces("<Z").chamfer(0.4)
    return shank.union(head)


def csk_bolt(d_shank, head_d, length):
    """Countersunk screw: the 90 degree head is flush with the surface it sits in (z <= 0)."""
    depth = (head_d - d_shank) / 2
    head = cq.Workplane("XY").add(cq.Solid.makeCone(d_shank / 2, head_d / 2, depth, cq.Vector(0, 0, -depth), cq.Vector(0, 0, 1)))
    shank = cq.Workplane("XY").circle(d_shank / 2).extrude(length - depth + 0.5).translate((0, 0, -length)).faces("<Z").chamfer(0.4)
    return shank.union(head)


def csk_cut(d_shank, head_d):
    """The countersink for csk_bolt, a little oversize, to cut from the part the head sits in."""
    depth = (head_d - d_shank) / 2
    return cq.Workplane("XY").add(cq.Solid.makeCone(d_shank / 2 + 0.05, head_d / 2 + 0.3, depth + 0.25, cq.Vector(0, 0, -depth), cq.Vector(0, 0, 1)))


def nut(af, h, bore):
    return hexagon(af, h).cut(cq.Workplane("XY").circle(bore / 2).extrude(h + 2).translate((0, 0, -1)))


def compound(solids):
    return cq.Compound.makeCompound([s.val() if hasattr(s, "val") else s for s in solids])


def plate_bolts(name, pts, n, bolt=None, qty_note=""):
    """One compound part holding a bolt at every point in pts (world points on the surface), heads along n."""
    bolt = bolt if bolt is not None else hex_bolt_m6()
    if not pts:
        return None
    sols = [place(bolt, p, n) for p in pts]
    return add(f"hardware-{name} (bought, {len(pts)} x M6 x 12 hex, washers, T-nuts{qty_note})", compound(sols), HARDWARE)


def fillet_corners(solid, axis_sel, r):
    return solid.edges(axis_sel).fillet(r) if r > 0 else solid


def plate_xz(name, x0, x1, z0, z1, y0, t, holes=(), rect_cuts=(), circ_cuts=(), slots=(), r=None, bolt_side=None, bolt_d=None, bolt_skip=()):
    """A flat plate in the XZ plane (front/rear facing), thickness along +Y from y0, corners rounded r.
    holes: (x, z, d). rect_cuts: (xc, zc, w, h). circ_cuts: (x, z, d). slots: (xc, zc, w, h) rounded ends.
    bolt_side: -1 puts a hex bolt head on the y0 face at every hole of diameter bolt_d, +1 on the y0+t face."""
    r = P["plate_corner_r"] if r is None else r
    w, h = x1 - x0, z1 - z0
    wp = cq.Workplane("XZ").center((x0 + x1) / 2, (z0 + z1) / 2).rect(w, h)
    solid = fillet_corners(wp.extrude(-t), "|Y", r).translate((0, y0, 0))   # XZ workplane normal is -Y, so extrude(-t) goes +Y
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
    sk = fillet_corners(cq.Workplane("XY").center((x0 + x1) / 2, (z0 + z1) / 2).rect(w, h).extrude(1), "|Z", r)
    for (x, z, d) in list(holes) + list(circ_cuts):
        sk = sk.cut(cq.Workplane("XY").center(x, z).circle(d / 2).extrude(3).translate((0, 0, -1)))
    for (xc, zc, cw, ch) in rect_cuts:
        sk = sk.cut(cq.Workplane("XY").center(xc, zc).rect(cw, ch).extrude(3).translate((0, 0, -1)))
    for (xc, zc, cw, ch) in slots:
        sk = sk.cut(cq.Workplane("XY").center(xc, zc).slot2D(cw, ch).extrude(3).translate((0, 0, -1)))
    export_dxf(name, sk)
    if bolt_side:
        yb = y0 if bolt_side < 0 else y0 + t
        plate_bolts(name, [(x, yb, z) for (x, z, d) in holes if abs(d - (bolt_d or P["m6_hole"])) < 1e-6 and (x, z) not in bolt_skip], (0, bolt_side, 0))
    return solid


def plate_xy(name, x0, x1, y0, y1, z0, t, holes=(), rect_cuts=(), circ_cuts=(), r=None, bolt_side=None, bolt_skip=()):
    """A flat plate in the XY plane (horizontal), thickness along +Z from z0."""
    r = P["plate_corner_r"] if r is None else r
    w, d = x1 - x0, y1 - y0
    solid = fillet_corners(cq.Workplane("XY").center((x0 + x1) / 2, (y0 + y1) / 2).rect(w, d).extrude(t), "|Z", r).translate((0, 0, z0))
    for (x, y, dd) in list(holes) + list(circ_cuts):
        solid = solid.cut(cq.Workplane("XY").center(x, y).circle(dd / 2).extrude(t + 2).translate((0, 0, z0 - 1)))
    for (xc, yc, cw, ch) in rect_cuts:
        solid = solid.cut(cq.Workplane("XY").center(xc, yc).rect(cw, ch).extrude(t + 2).translate((0, 0, z0 - 1)))
    add(name, solid, STEEL, plate=True, t=t)
    sk = fillet_corners(cq.Workplane("XY").center((x0 + x1) / 2, (y0 + y1) / 2).rect(w, d).extrude(1), "|Z", r)
    for (x, y, dd) in list(holes) + list(circ_cuts):
        sk = sk.cut(cq.Workplane("XY").center(x, y).circle(dd / 2).extrude(3).translate((0, 0, -1)))
    for (xc, yc, cw, ch) in rect_cuts:
        sk = sk.cut(cq.Workplane("XY").center(xc, yc).rect(cw, ch).extrude(3).translate((0, 0, -1)))
    export_dxf(name, sk)
    if bolt_side:
        zb = z0 if bolt_side < 0 else z0 + t
        plate_bolts(name, [(x, y, zb) for (x, y, dd) in holes if abs(dd - P["m6_hole"]) < 1e-6 and (x, y) not in bolt_skip], (0, 0, bolt_side))
    return solid


def plate_yz(name, y0, y1, z0, z1, x0, t, holes=(), r=None, bolt_side=None):
    """A flat plate in the YZ plane (side panel), thickness along +X from x0. holes: (y, z, d)."""
    r = P["plate_corner_r"] if r is None else r
    d, h = y1 - y0, z1 - z0
    solid = fillet_corners(cq.Workplane("YZ").center((y0 + y1) / 2, (z0 + z1) / 2).rect(d, h).extrude(t), "|X", r).translate((x0, 0, 0))
    for (y, z, dd) in holes:
        solid = solid.cut(cq.Workplane("YZ").center(y, z).circle(dd / 2).extrude(t + 2).translate((x0 - 1, 0, 0)))
    add(name, solid, STEEL, plate=True, t=t)
    sk = fillet_corners(cq.Workplane("XY").center((y0 + y1) / 2, (z0 + z1) / 2).rect(d, h).extrude(1), "|Z", r)
    for (y, z, dd) in holes:
        sk = sk.cut(cq.Workplane("XY").center(y, z).circle(dd / 2).extrude(3).translate((0, 0, -1)))
    export_dxf(name, sk)
    if bolt_side:
        xb = x0 if bolt_side < 0 else x0 + t
        plate_bolts(name, [(xb, y, z) for (y, z, dd) in holes if abs(dd - P["m6_hole"]) < 1e-6], (bolt_side, 0, 0))
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
post_xy = [(-hw, 0), (hw - e, 0), (-hw, D - e), (hw - e, D - e)]
for i, (x0, y0) in enumerate(post_xy):
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

# leveling feet: into the posts' tapped centre bores, through the base pan
foot_pts = [(x0 + e / 2, y0 + e / 2) for (x0, y0) in post_xy]
feet = []
for (fx, fy) in foot_pts:
    ph, hh_ = P["foot_pad_h"], P["foot_hex_h"]
    pad = cq.Workplane("XY").circle(P["foot_pad_d"] / 2).extrude(ph).edges("<Z").fillet(2.0)
    hexb = hexagon(P["foot_hex_af"], hh_).translate((0, 0, ph))
    stud = cq.Workplane("XY").circle(P["foot_stud_d"] / 2).extrude(P["t_base"] + 0.5).translate((0, 0, ph + hh_ - 0.5))
    thread = cq.Workplane("XY").circle(P["tslot_4040"]["bore"] / 2 - 0.1).extrude(P["foot_stud_in"] + 0.5).translate((0, 0, ph + hh_ + P["t_base"] - 0.5))
    feet.append(pad.union(hexb).union(stud).union(thread).translate((fx, fy, -(ph + hh_ + P["t_base"]))))
add("feet (bought, 4 x M8 leveling feet, 50 pad)", compound(feet), RUBBER)
P["foot_height"] = P["foot_pad_h"] + P["foot_hex_h"]   # floor to the base pan

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

# front bulkhead: door opening, lint slot, front roller holes; bolt heads on its back face (the rails are in front of it)
plate_xz("front-bulkhead", bulk_x0, bulk_x1, bulk_z0, bulk_z1, P["front_bulk_y"], tb,
         holes=bulk_holes(front=True) + rollers,
         circ_cuts=[(0, az, P["door_opening_d"])],
         slots=[(0, az - P["lint_slot_below_axis"], P["lint_slot_w"], P["lint_slot_h"])], bolt_side=+1)

# rear bulkhead: inlet hole field, roller shaft holes, mounting holes; bolt heads on its front face (the cross rails are behind it)
inlet = []
nx = int(P["inlet_w"] // P["inlet_pitch"])
nz = int(P["inlet_h"] // P["inlet_pitch"])
for i in range(nx):
    for j in range(nz):
        x = -P["inlet_w"] / 2 + P["inlet_pitch"] / 2 + i * P["inlet_pitch"]
        z = az + P["inlet_above_axis"] + j * P["inlet_pitch"]
        inlet.append((x, z, P["inlet_hole_d"]))
plate_xz("rear-bulkhead", bulk_x0, bulk_x1, bulk_z0, bulk_z1, P["rear_bulk_y"], tb,
         holes=bulk_holes() + rollers + inlet, bolt_side=-1)

# felt seal on the rear bulkhead's front face, inboard of the rear tabs, against the rear ring's back face
felt = (cq.Workplane("XZ").center(0, az).circle(P["felt_ro"]).circle(P["felt_ri"]).extrude(-P["felt_t"])
        .translate((0, P["rear_bulk_y"] - P["felt_t"], 0)))
add("felt-seal-rear", felt, FELT, plate=True, t=P["felt_t"])
export_dxf("felt-seal-rear", cq.Workplane("XY").circle(P["felt_ro"]).extrude(1).cut(cq.Workplane("XY").circle(P["felt_ri"]).extrude(3).translate((0, 0, -1))))

# ---------------------------------------------------------------------------
# Belt path (needed for the bay ceiling slots): drum -> motor pulley (right run) -> idler -> drum (left run)
# ---------------------------------------------------------------------------
def tangent(A, B):
    """Common tangent from circle A to circle B along the loop's clockwise traversal (viewed from the front, X right, Z up).
    A, B = (cx, cz, r, s) with s +1 for a pulley inside the loop, -1 for a backside idler outside it. Returns (pA, pB)."""
    ax, azz, ra, sa = A
    bx, bz, rb, sb = B
    cx, cz = bx - ax, bz - azz
    L = math.hypot(cx, cz)
    k = sa * ra - sb * rb
    ca = k / L
    sa_ = math.sqrt(max(0.0, 1 - ca * ca))
    chx, chz = cx / L, cz / L
    nx_, nz_ = ca * chx - sa_ * chz, ca * chz + sa_ * chx
    return (ax + sa * ra * nx_, azz + sa * ra * nz_), (bx + sb * rb * nx_, bz + sb * rb * nz_)


BT, BW = P["belt_t"], P["belt_w"]
belt_circles = [(0.0, az, P["drum_rim_r"] + BT / 2, +1),
                (0.0, P["motor_axis_z"], P["motor_pulley_d"] / 2 + BT / 2, +1),
                (P["idler_x"], P["idler_z"], P["idler_d"] / 2 + BT / 2, -1)]
belt_runs = [tangent(belt_circles[i], belt_circles[(i + 1) % 3]) for i in range(3)]


def arc_mid(c, p_in, p_out):
    cx, cz, r, s = c
    a0 = math.atan2(p_in[1] - cz, p_in[0] - cx)
    a1 = math.atan2(p_out[1] - cz, p_out[0] - cx)
    if s > 0:
        d = (a0 - a1) % (2 * math.pi)
        am = a0 - d / 2
    else:
        d = (a1 - a0) % (2 * math.pi)
        am = a0 + d / 2
    return (cx + r * math.cos(am), cz + r * math.sin(am)), d * r


def cross_at_z(p, q, z):
    t = (z - p[1]) / (q[1] - p[1])
    return p[0] + t * (q[0] - p[0])


# where the two straight runs cross the bay ceiling plate (its mid-thickness), one slot each
ceil_mid_z = bt + P["t_base"] / 2
P["belt_cross_right"] = cross_at_z(belt_runs[0][0], belt_runs[0][1], ceil_mid_z)   # drum -> pulley
P["belt_cross_left"] = cross_at_z(belt_runs[2][0], belt_runs[2][1], ceil_mid_z)    # idler -> drum
belt_len = 0.0
for i in range(3):
    pa, pb = belt_runs[i]
    belt_len += math.hypot(pb[0] - pa[0], pb[1] - pa[1])
    belt_len += arc_mid(belt_circles[(i + 1) % 3], pb, belt_runs[(i + 1) % 3][0])[1]
P["belt_len_est"] = belt_len

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
         rect_cuts=[(round(P["belt_cross_left"], 1), P["belt_y"], P["belt_slot_w"], P["belt_slot_l"]),    # belt slots, one per run
                    (round(P["belt_cross_right"], 1), P["belt_y"], P["belt_slot_w"], P["belt_slot_l"]),
                    (0, P["rear_bulk_y"] + tb / 2, P["inner_w"] + 2, tb + 1),    # rear bulkhead passes through
                    (-hw + e / 2, D - e / 2, e + 1, e + 1), (hw - e / 2, D - e / 2, e + 1, e + 1),   # rear post notches
                    (0, ry + e + 2 + P["riser_depth"] / 2, P["riser_w"] + 4, P["riser_depth"] + 4)],   # riser, 2 mm clearance
         bolt_side=+1)

base_holes = []
for x in pitch_points(-hw + e, hw - e, P["panel_pitch"], 40):
    base_holes.append((x, e / 2, P["m6_hole"])); base_holes.append((x, D - e / 2, P["m6_hole"]))
for y in pitch_points(e, D - e, P["panel_pitch"], 40):
    base_holes.append((-hw + e / 2, y, P["m6_hole"])); base_holes.append((hw - e / 2, y, P["m6_hole"]))
base_holes += [(fx, fy, P["foot_hole_d"]) for (fx, fy) in foot_pts]   # the feet's studs pass through to the posts
ARM_Y0 = P["belt_y"] - P["belt_w"] / 2 - 1.5 - 0.5 - 4.0                       # the idler arm runs in front of the belt plane, 0.5 off the idler's flange, flush with the motor's back
BRACKET_Y = ARM_Y0 - 20.0                                                        # idler and spring bracket bolts, on the pan
bracket_pts = [(-128.0, BRACKET_Y), (-102.0, BRACKET_Y), (55.0, BRACKET_Y), (75.0, BRACKET_Y)]
base_holes += [(bx, by, P["m6_hole"]) for (bx, by) in bracket_pts]
plate_xy("base-pan", -hw + tp, hw - tp, 0, D, -P["t_base"], P["t_base"], holes=base_holes, bolt_side=-1, bolt_skip=tuple(bracket_pts))   # no cuts; the exhaust leaves through the rear lower panel

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

plate_yz("side-panel-left", 0, D, 0, Hb, -hw - tp, tp, holes=side_holes(), bolt_side=-1)
plate_yz("side-panel-right", 0, D, 0, Hb, hw, tp, holes=side_holes(), bolt_side=+1)

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

# door ring bolt pattern (8 x M4 through the ring and the front upper panel) and the two fixed hinge leaves (2 x M6 each)
ring_bolt_pts = []
for k in range(P["ring_bolt_n"]):
    a = math.radians(22.5 + 45.0 * k)
    ring_bolt_pts.append((P["ring_bolt_r"] * math.cos(a), az + P["ring_bolt_r"] * math.sin(a)))
hinge_zs = (az - P["hinge_z_off"], az + P["hinge_z_off"])     # knuckle centres: fixed (ring side) below, swinging (disc side) above
hinge_fixed_bolt_pts = [(-266.0, hinge_zs[0]), (-252.0, hinge_zs[0])]   # 14 apart: the 12 mm countersunk heads and the 10 mm nuts must clear each other
hinge_swing_bolt_pts = [(-259.0, hinge_zs[1]), (-250.0, hinge_zs[1])]
handle_pts = [(P["handle_x"], az - P["handle_span"] / 2), (P["handle_x"], az + P["handle_span"] / 2)]

# The front and rear panels split at the bottom of the mid rail (260) so the upper panel bolts to the mid rail,
# the top rail and the posts, and the lower panel to the bottom rail and the posts. The lower panel comes off
# to reach the bay. The upper panel carries the door ring opening; the lower panels carry the louvers.
P["panel_split_z"] = bt - e
plate_xz("front-upper-panel", -hw, hw, P["panel_split_z"], Hb, -tp, tp,
         holes=end_holes(P["panel_split_z"], Hb, [bt - e / 2, Hb - e / 2], stubs_only_at=bt - e / 2)
         + [(x, z, P["m4_hole"]) for (x, z) in ring_bolt_pts] + [(x, z, P["m6_hole"]) for (x, z) in hinge_fixed_bolt_pts],
         circ_cuts=[(0, az, P["door_ring_id"] + 10)], bolt_side=-1, bolt_skip=tuple(hinge_fixed_bolt_pts))
louvers = [(x, z, 60, 5) for x in (-240, -160, -80, 0, 80, 160, 240) for z in range(80, 240, 20)]
plate_xz("front-lower-panel", -hw, hw, 0, P["panel_split_z"] - 1, -tp, tp,
         holes=end_holes(0, P["panel_split_z"] - 1, [e / 2]), slots=louvers, bolt_side=-1)
plate_xz("rear-upper-panel", -hw, hw, P["panel_split_z"], Hb, D, tp, holes=end_holes(P["panel_split_z"], Hb, [bt - e / 2, Hb - e / 2]), bolt_side=+1)
rear_louvers = [(x, z, 60, 5) for x in (-160, -80, 0, 80) for z in range(80, 240, 20)]   # clear of the exhaust port and the cord entry
plate_xz("rear-lower-panel", -hw, hw, 0, P["panel_split_z"] - 1, D, tp,
         holes=end_holes(0, P["panel_split_z"] - 1, [e / 2]),
         circ_cuts=[(P["exhaust_x"], P["exhaust_z"], P["exhaust_d"] + 4),     # exhaust collar, 2 mm clearance
                    (-250, 120, P["cord_hole_d"])],                             # cord strain relief bushing, in front of the power module
         slots=rear_louvers, bolt_side=+1)

# top panel in front of the console, and the console wedge (sloped face with the UCI aperture, cap, two cheeks)
top_holes = []
for x in pitch_points(-hw + e, hw - e, P["panel_pitch"], 60):
    top_holes.append((x, e / 2, P["m6_hole"]))
for y in pitch_points(e, P["console_y0"] - tp, P["panel_pitch"], 60):
    top_holes.append((-hw + e / 2, y, P["m6_hole"])); top_holes.append((hw - e / 2, y, P["m6_hole"]))
plate_xy("top-panel", -hw, hw, 0, P["console_y0"] - tp, Hb, tp, holes=top_holes, bolt_side=+1)   # stops 1.5 short of the face plate's outer corner

cy0, cf, cr = P["console_y0"], P["console_face"], P["console_rise"]
S45 = math.sin(math.radians(45))
CONSOLE_C = (0.0, cy0 + cr / 2, Hb + cr / 2)       # centre of the console face plate's inner surface
N_FACE = (0.0, -S45, S45)                           # outward normal of the sloped face (front and up)
S_FACE = (0.0, S45, S45)                            # up the slope


def on_face(solid):
    """A solid built in the console face's local frame (x across, y up the slope, z outward from the inner surface) to the world."""
    return solid.rotate((0, 0, 0), (1, 0, 0), 45).translate(CONSOLE_C)


def face_point(u, v, w):
    return (u, CONSOLE_C[1] + v * S_FACE[1] + w * N_FACE[1], CONSOLE_C[2] + v * S_FACE[2] + w * N_FACE[2])


# sloped face: build as a plate in a tilted workplane; aperture and 4 holes
uci_pts = [(sx * P["uci_hole_x"] / 2, sy * P["uci_hole_y"] / 2) for sx in (-1, 1) for sy in (-1, 1)]
face = (fillet_corners(cq.Workplane("XY").rect(P["W"] - 2 * tp, cf).extrude(tp), "|Z", P["plate_corner_r"])
        .faces(">Z").workplane().rect(P["uci_ap_w"], P["uci_ap_h"]).cutThruAll()
        .faces(">Z").workplane().pushPoints(uci_pts).hole(P["uci_hole_d"]))
# +45 about X: the plate rises toward the rear and its outward normal is (0, -0.707, 0.707), front and up.
# (Draft 2 had -45 here, which laid the face the wrong way; found by the section audit, see docs/verification.md V-010.)
face = on_face(face)
add("console-face", face, STEEL, plate=True, t=tp)
sk = (fillet_corners(cq.Workplane("XY").rect(P["W"] - 2 * tp, cf).extrude(1), "|Z", P["plate_corner_r"])
      .cut(cq.Workplane("XY").rect(P["uci_ap_w"], P["uci_ap_h"]).extrude(3).translate((0, 0, -1))))
for (ux, uy) in uci_pts:
    sk = sk.cut(cq.Workplane("XY").center(ux, uy).circle(P["uci_hole_d"] / 2).extrude(3).translate((0, 0, -1)))
export_dxf("console-face", sk)
plate_xy("console-cap", -hw, hw, cy0 + cr, D, Hb + cr, tp)
for side, x0 in (("left", -hw), ("right", hw - tp)):
    cheek = (cq.Workplane("YZ").polyline([(cy0, Hb), (cy0 + cr, Hb + cr), (D, Hb + cr), (D, Hb)]).close()
             .extrude(tp).edges("|X").fillet(P["small_corner_r"]).translate((x0, 0, 0)))
    add(f"console-cheek-{side}", cheek, STEEL, plate=True, t=tp)
    sk = cq.Workplane("XY").polyline([(cy0, Hb), (cy0 + cr, Hb + cr), (D, Hb + cr), (D, Hb)]).close().extrude(1).edges("|Z").fillet(P["small_corner_r"])
    export_dxf(f"console-cheek-{side}", sk)

# ---------------------------------------------------------------------------
# Tier 0 control module on the console face (controls/tier0-mechanical, drawing numbers in tier0_drawings.py)
# ---------------------------------------------------------------------------
FP_T = P["fp_t"]
TIMERS = {"dry-time": -80.0, "heat-time": -20.0}
SEL_X, START_X = 45.0, 90.0
fp_holes = [(x, y, 4.5) for (x, y) in uci_pts]                                  # UCI-D mounting pattern
for x in TIMERS.values():
    fp_holes += [(x, 0, 12.0), (x, 83.3 / 2, 4.0), (x, -83.3 / 2, 4.0)]          # timer shaft and yoke holes
fp_holes += [(SEL_X, 0, 22.3), (START_X, 0, 22.3)]                               # 22 mm devices
fp_holes += [(25.0, -38.0, 4.5), (105.0, -38.0, 4.5), (-112.0, -45.0, 4.5), (-112.0, 45.0, 4.5)]   # DIN rail standoffs, cable ties
fp = fillet_corners(cq.Workplane("XY").rect(P["fp_w"], P["fp_h"]).extrude(FP_T), "|Z", P["fp_r"])
for (x, y, d) in fp_holes:
    fp = fp.cut(cq.Workplane("XY").center(x, y).circle(d / 2).extrude(FP_T + 2).translate((0, 0, -1)))
for text, x, y in (("DRY TIME", -80, 50), ("HEAT TIME", -20, 50), ("HEAT", 45, 27), ("START", 90, 27), ("AIR  LOW  HIGH", 45, -27)):
    fp = fp.faces(">Z").workplane(origin=(0, 0, FP_T)).center(x, y).text(text, 5, -0.3, combine="cut", halign="center", valign="center")
fp_z0 = tp                      # the faceplate sits on the console face's outer surface
add("tier0-faceplate", on_face(fp.translate((0, 0, fp_z0))), ALU, plate=True, t=FP_T)
# no DXF from here: mechanical/drawings/tier0_drawings.py writes tier0-faceplate.dxf (with its label and reference layers)
# from the same numbers, and the audit matches this part's section against that file
# four M4 button heads hold the faceplate to the console face, nuts inside the console
fp_bolts = [place(button_bolt(4.0, P["m4_head_d"], P["m4_head_h"], 10.0, 2.5), face_point(ux, uy, fp_z0 + FP_T), N_FACE) for (ux, uy) in uci_pts]
fp_nuts = [place(nut(P["m4_nut_af"], P["m4_nut_h"], 4.2), face_point(ux, uy, 0.0), tuple(-c for c in N_FACE)) for (ux, uy) in uci_pts]
add("hardware-tier0-faceplate (bought, 4 x M4 x 10 button head, nuts)", compound(fp_bolts + fp_nuts), HARDWARE)

fp_top = fp_z0 + FP_T           # outer surface of the faceplate, in face coordinates


def knob(x, d, skirt_h, body_d, h):
    """A skirted pointer knob, built in face coordinates 1 mm above the faceplate; the shaft reaches into the timer."""
    k = cq.Workplane("XY").center(x, 0).circle(d / 2).extrude(skirt_h)
    k = k.union(cq.Workplane("XY").center(x, 0).circle(body_d / 2).extrude(h - 1.0).edges(">Z").fillet(2.0))
    k = k.union(box(x - 1.5, x + 1.5, body_d / 2 - 1, d / 2 - 0.5, skirt_h, skirt_h + 1.2))   # pointer line on the skirt
    k = k.union(box(x - 1.5, x + 1.5, 0, body_d / 2 - 2, h - 1.0, h + 0.2))                       # pointer line across the top
    k = k.translate((0, 0, fp_top + 1.0))
    shaft = cq.Workplane("XY").center(x, 0).circle(3.0).extrude(fp_top + 1.0 + skirt_h).faces("<Z").chamfer(0.5)   # D-shaft, from the timer
    return k.union(shaft)


for key, x in TIMERS.items():
    add(f"tier0-knob-{key} (bought)", on_face(knob(x, P["knob_d"], P["knob_skirt_h"], P["knob_body_d"], P["knob_h"])), RUBBER)
    # the timer behind the plate: wall-device yoke strap against the faceplate's back, body behind it
    yoke = box(x - 12, x + 12, -53.2, 53.2, -1.5, 0).cut(cq.Workplane("XY").center(x, 0).circle(6.5).extrude(3).translate((0, 0, -2)))
    body = box(x - 20.3, x + 20.3, -35.45, 35.45, -1.5 - 30.2, -1.5)
    add(f"tier0-timer-{key} (bought)", on_face(yoke.union(body).translate((0, 0, fp_z0))), BOUGHT)


def device22(x, cap):
    """A 22 mm panel device: bezel on the plate, operator in front, body and contact block behind."""
    bezel = cq.Workplane("XY").center(x, 0).circle(15.0).circle(11.15).extrude(2.5).translate((0, 0, fp_top))
    body = cq.Workplane("XY").center(x, 0).circle(11.0).extrude(fp_top + 45).translate((0, 0, -45))
    block = box(x - 12.5, x + 12.5, -17.5, 17.5, -45, -15)
    base = bezel.union(body).union(block)
    return base, cap(x)


def selector_cap(x):
    hub = cq.Workplane("XY").center(x, 0).circle(11.0).extrude(4.0)
    lever = cq.Workplane("XY").center(x, 0).slot2D(30.0, 8.0, angle=90).extrude(6.0).translate((0, 0, 4.0))
    return hub.union(lever).translate((0, 0, fp_top + 2.5))


def start_cap(x):
    return cq.Workplane("XY").center(x, 0).circle(11.0).extrude(8.0).edges(">Z").fillet(2.0).translate((0, 0, fp_top + 2.5))


base, cap = device22(SEL_X, selector_cap)
add("tier0-selector-body (bought)", on_face(base), BOUGHT)
add("tier0-selector (bought)", on_face(cap), RUBBER)
base, cap = device22(START_X, start_cap)
add("tier0-start-body (bought)", on_face(base), BOUGHT)
add("tier0-start-button (bought)", on_face(cap), cq.Color(0.1, 0.6, 0.2))
# K1 on 100 mm of DIN rail on two 12 mm standoffs behind the plate; the socket and relay stack away from the plate
rail = box(15, 115, -55.5, -20.5, fp_z0 - 12 - 7.5, fp_z0 - 12)
standoffs = [cq.Workplane("XY").center(x, -38).circle(4.0).extrude(12).translate((0, 0, fp_z0 - 12)) for x in (25, 105)]
relay = box(16, 44, -74, -19, fp_z0 - 12 - 7.5 - 65, fp_z0 - 12 - 7.5)
add("tier0-k1-relay-on-din-rail (bought)", on_face(rail.union(standoffs[0]).union(standoffs[1]).union(relay)), BOUGHT)

# ---------------------------------------------------------------------------
# Door: ring on the front panel, disc, two catalog flag hinges, handle, seal, catch
# ---------------------------------------------------------------------------
ring_y0 = -tp - P["t_door"]                     # ring from -3.5 to -1.5
disc_y0 = -tp - 2 * P["t_door"] - 8             # disc from -13.5 to -11.5
ring = (cq.Workplane("XZ").center(0, az).circle(P["door_ring_od"] / 2).circle(P["door_ring_id"] / 2)
        .extrude(-P["t_door"]).translate((0, ring_y0, 0)))
for (x, z) in ring_bolt_pts:
    ring = ring.cut(cq.Workplane("XZ").center(x, z).circle(P["m4_hole"] / 2).extrude(-P["t_door"] - 2).translate((0, ring_y0 - 1, 0)))
for (x, z) in hinge_fixed_bolt_pts:
    ring = ring.cut(cq.Workplane("XZ").center(x, z).circle(P["m6_hole"] / 2).extrude(-P["t_door"] - 2).translate((0, ring_y0 - 1, 0)))
add("door-ring", ring, STEEL, plate=True, t=P["t_door"])
sk = cq.Workplane("XY").circle(P["door_ring_od"] / 2).extrude(1).cut(cq.Workplane("XY").circle(P["door_ring_id"] / 2).extrude(3).translate((0, 0, -1)))
for (x, z) in ring_bolt_pts:
    sk = sk.cut(cq.Workplane("XY").center(x, z - az).circle(P["m4_hole"] / 2).extrude(3).translate((0, 0, -1)))
for (x, z) in hinge_fixed_bolt_pts:
    sk = sk.cut(cq.Workplane("XY").center(x, z - az).circle(P["m6_hole"] / 2).extrude(3).translate((0, 0, -1)))
export_dxf("door-ring", sk)
ring_hw = [place(button_bolt(4.0, P["m4_head_d"], P["m4_head_h"], 10.0, 2.5), (x, ring_y0, z), (0, -1, 0)) for (x, z) in ring_bolt_pts]
ring_hw += [place(nut(P["m4_nut_af"], P["m4_nut_h"], 4.2), (x, 0.0, z), (0, 1, 0)) for (x, z) in ring_bolt_pts]
add("hardware-door-ring (bought, 8 x M4 x 10 button head, nuts)", compound(ring_hw), HARDWARE)

disc = cq.Workplane("XZ").center(0, az).circle(P["door_disc_d"] / 2).extrude(-P["t_door"]).translate((0, disc_y0, 0))
disc_holes = [(x, z, P["m4_hole"]) for (x, z) in hinge_swing_bolt_pts + handle_pts]
for (x, z, d) in disc_holes:
    disc = disc.cut(cq.Workplane("XZ").center(x, z).circle(d / 2).extrude(-P["t_door"] - 2).translate((0, disc_y0 - 1, 0)))
add("door-disc", disc, STEEL, plate=True, t=P["t_door"])
sk = cq.Workplane("XY").circle(P["door_disc_d"] / 2).extrude(1)
for (x, z, d) in disc_holes:
    sk = sk.cut(cq.Workplane("XY").center(x, z - az).circle(d / 2).extrude(3).translate((0, 0, -1)))
export_dxf("door-disc", sk)

# hinges: the fixed half (leaf on the ring, knuckle, pin) below the axis, the swinging half (leaf on the disc, bored knuckle) above
hx, hy = P["hinge_pin_x"], P["hinge_pin_y"]
kd, lt, lh = P["hinge_knuckle_d"], P["hinge_leaf_t"], P["hinge_leaf_h"]
for i, (zk, kind) in enumerate(((hinge_zs[0], "fixed"), (hinge_zs[1], "swing"))):
    knuckle = cq.Workplane("XY").center(hx, hy).circle(kd / 2).extrude(lh).translate((0, 0, zk - lh / 2))
    if kind == "fixed":
        leaf = box(hx, P["hinge_leaf_x_in"], ring_y0 - lt, ring_y0, zk - lh / 2, zk + lh / 2)         # on the ring's front face
        pin = cq.Workplane("XY").center(hx, hy).circle(P["hinge_pin_d"] / 2).extrude(lh + 2 * P["hinge_z_off"] + 10).translate((0, 0, zk - lh / 2 - 5))
        half = knuckle.union(leaf).union(pin)
        for (x, z) in hinge_fixed_bolt_pts:
            half = half.cut(cq.Workplane("XZ").center(x, z).circle(P["m6_hole"] / 2).extrude(-lt - 2).translate((0, ring_y0 - lt - 1, 0)))
            half = half.cut(place(csk_cut(6.0, 12.0), (x, ring_y0 - lt, z), (0, -1, 0)))
        add(f"door-hinge-{i+1}-fixed (bought, flag hinge, pinned half)", half, HARDWARE)
        bolts = [place(csk_bolt(6.0, 12.0, 16.0), (x, ring_y0 - lt, z), (0, -1, 0)) for (x, z) in hinge_fixed_bolt_pts]
        bolts += [place(nut(P["m6_nut_af"], P["m6_nut_h"], 6.2), (x, 0.0, z), (0, 1, 0)) for (x, z) in hinge_fixed_bolt_pts]
        add(f"hardware-door-hinge-{i+1} (bought, 2 x M6 x 16 countersunk, nuts)", compound(bolts), HARDWARE)
    else:
        leaf = box(hx, P["hinge_leaf_x_in"], disc_y0 + P["t_door"], disc_y0 + P["t_door"] + lt, zk - lh / 2, zk + lh / 2)   # on the disc's back face
        half = knuckle.union(leaf).cut(cq.Workplane("XY").center(hx, hy).circle(P["hinge_pin_d"] / 2 + 0.1).extrude(lh + 2).translate((0, 0, zk - lh / 2 - 1)))
        for (x, z) in hinge_swing_bolt_pts:   # tapped M4 in the leaf, drawn at the thread's outside diameter
            half = half.cut(cq.Workplane("XZ").center(x, z).circle(2.1).extrude(-lt - 2).translate((0, disc_y0 + P["t_door"] - 1, 0)))
        add(f"door-hinge-{i+1}-swing (bought, flag hinge, lift-off half)", half, HARDWARE)
        bolts = [place(button_bolt(4.0, P["m4_head_d"], P["m4_head_h"], 8.0, 2.5), (x, disc_y0, z), (0, -1, 0)) for (x, z) in hinge_swing_bolt_pts]
        add(f"hardware-door-hinge-{i+1} (bought, 2 x M4 x 8 button head into the tapped leaf)", compound(bolts), HARDWARE)

# handle: two standoffs and a bar, M4 from the back of the disc into the standoffs
hd, hs_ = P["handle_bar_d"], P["handle_standoff"]
handle = None
for (x, z) in handle_pts:
    so = cq.Workplane("XZ").center(x, z).circle(hd / 2).extrude(hs_).translate((0, disc_y0, 0))     # XZ extrude(+) goes -Y
    so = so.cut(cq.Workplane("XZ").center(x, z).circle(2.1).extrude(10).translate((0, disc_y0 + 0.01, 0)))   # tapped M4, 10 deep
    handle = so if handle is None else handle.union(so)
bar = (cq.Workplane("XY").center(P["handle_x"], disc_y0 - hs_ - hd / 2 + 0.5).circle(hd / 2)
       .extrude(P["handle_span"] + hd).translate((0, 0, az - P["handle_span"] / 2 - hd / 2)).edges("%CIRCLE").fillet(5.0))
handle = handle.union(bar)
add("door-handle (bought, D handle 128 centres)", handle, HARDWARE)
add("hardware-door-handle (bought, 2 x M4 x 10 button head into the handle)",
    compound([place(button_bolt(4.0, P["m4_head_d"], P["m4_head_h"], 10.0, 2.5), (x, disc_y0 + P["t_door"], z), (0, 1, 0)) for (x, z) in handle_pts]), HARDWARE)
# seal on the disc's back, catch on the ring with its strike on the disc
seal = (cq.Workplane("XZ").center(0, az).circle(P["seal_ro"]).circle(P["seal_ri"]).extrude(-P["seal_t"])
        .translate((0, disc_y0 + P["t_door"], 0)))
add("door-seal (bought, OEM door seal)", seal, RUBBER)
add("door-catch (bought, magnetic catch)", box(P["latch_x0"], P["latch_x1"], ring_y0 - 6.5, ring_y0, az - 6, az + 6), HARDWARE)
add("door-catch-strike (bought)", box(P["latch_x0"], P["latch_x1"], disc_y0 + P["t_door"], disc_y0 + P["t_door"] + 1.0, az - 6, az + 6), HARDWARE)

# ---------------------------------------------------------------------------
# Ducts: riser (behind the rear bulkhead, from the bay to the inlet zone) and lint duct (front)
# ---------------------------------------------------------------------------
riser_top = az + P["inlet_above_axis"] + P["inlet_h"] + 10
add("riser-duct", box(-P["riser_w"] / 2, P["riser_w"] / 2, ry + e + 2, ry + e + 2 + P["riser_depth"], bt - 120, riser_top), DUCT)
assert ry + e + 2 + P["riser_depth"] + 2 <= D - e, "riser must clear the rear end rail"
add("lint-duct", box(-168, 168, 2, 2 + P["lint_duct_depth"], 150, az - P["lint_slot_below_axis"] + P["lint_slot_h"] / 2), DUCT)   # 2 mm from each front stub
add("lint-duct-transition", box(-110, 110, 2 + P["lint_duct_depth"], P["blower_y0"], 50, 190), DUCT)

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


def radial_point(theta_deg, y, r):
    a = math.radians(theta_deg)
    return (r * math.cos(a), y, az + r * math.sin(a))


def radial_dir(theta_deg, outward=True):
    a = math.radians(theta_deg)
    s = 1.0 if outward else -1.0
    return (s * math.cos(a), 0.0, s * math.sin(a))


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
        tab = tab.edges("|Y").edges("<X").fillet(P["small_corner_r"])            # rounded corners at the tab's free (inner) end
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

# tab hardware (7b): button heads inside the drum on the ring's inner face, nuts outside on the tab
tab_hw = []
m4b = button_bolt(4.0, P["m4_head_d"], P["m4_head_h"], 8.0, 2.5)
m4n = nut(P["m4_nut_af"], P["m4_nut_h"], 4.2)
for theta in tab_thetas:
    x, _, z = radial_point(theta, 0, r_tab_hole)
    tab_hw.append(place(m4b, (x, y0d + P["ring_t"], z), (0, 1, 0)))               # front ring: head on the inside face at Y 52
    tab_hw.append(place(m4n, (x, y0d - P["drum_t"], z), (0, -1, 0)))              # nut on the front tab at 49.2
    tab_hw.append(place(m4b, (x, y0d + L - P["ring_t"], z), (0, -1, 0)))          # rear ring: head on the inside face at Y 598
    tab_hw.append(place(m4n, (x, y0d + L + P["drum_t"], z), (0, 1, 0)))           # nut on the rear tab at 600.8
add("hardware-drum-tabs (bought, 60 x M4 x 8 button head, nuts)", compound(tab_hw), HARDWARE)

# the splice strip: inside the sheet under the seam (top of the drum), between the rings, holes on the seam holes
half_ang = math.degrees((P["splice_w"] / 2) / ri)
spl_len = L - 2 * P["ring_t"] - 2
splice = (cq.Workplane("XZ").center(0, az).circle(ri).circle(ri - P["splice_t"]).extrude(-spl_len)
          .translate((0, y0d + P["ring_t"] + 1, 0)))
keep = (cq.Workplane("XY").box(2 * ri * math.sin(math.radians(half_ang)) + 0.01, spl_len + 2, 2 * ri, centered=(True, False, False))
        .translate((0, y0d + P["ring_t"], az)))
splice = splice.intersect(keep).edges("|Z").fillet(P["small_corner_r"])
for theta in seam_thetas:
    for yy in seam_ys:
        splice = splice.cut(radial_hole(theta, y0d + yy, P["seam_hole_d"], ri - 4, ri + 2))
add("drum-splice", splice, DRUM, plate=True, t=P["splice_t"])
seam_hw = []
for theta in seam_thetas:
    for yy in seam_ys:
        seam_hw.append(place(m4b, radial_point(theta, y0d + yy, ri - P["splice_t"] - 0.05), radial_dir(theta, outward=False)))   # head inside on the splice (0.05 off the concave face)
        seam_hw.append(place(m4n, radial_point(theta, y0d + yy, ro), radial_dir(theta, outward=True)))                      # nut outside on the sheet
add("hardware-drum-seam (bought, 16 x M4 x 8 button head, nuts)", compound(seam_hw), HARDWARE)

# the baffles: catalog 40x40x3 aluminium angle, 480 long, the wall leg bolted through the sheet's baffle holes.
# The flat leg sits 0.7 mm off the curved wall at its centre line so its edges clear the wall (sagitta of a 40 chord on R 309).
d_leg = math.sqrt(ri ** 2 - (P["baffle_leg"] / 2) ** 2) - 0.05
tb_ang = 3.0
baffle_hw = []
m6b = button_bolt(6.0, P["m6_button_d"], P["m6_button_h"], 12.0, 4.0)
m6n = nut(P["m6_nut_af"], P["m6_nut_h"], 6.2)
for i, theta in enumerate(baffle_thetas):
    yb0, yb1 = y0d + L / 2 - P["baffle_len"] / 2, y0d + L / 2 + P["baffle_len"] / 2
    leg_wall = box(d_leg - tb_ang, d_leg, yb0, yb1, -P["baffle_leg"] / 2, P["baffle_leg"] / 2)
    leg_up = box(d_leg - P["baffle_leg"], d_leg, yb0, yb1, P["baffle_leg"] / 2 - tb_ang, P["baffle_leg"] / 2)
    ang_s = leg_wall.union(leg_up)
    for yy in baffle_ys:
        ang_s = ang_s.cut(cq.Workplane("YZ").center(yy, 0).circle(P["baffle_hole_d"] / 2).extrude(tb_ang + 4).translate((d_leg - tb_ang - 2, 0, 0)))
    add(f"baffle-{i+1} (angle, cut to length)", about_axis(ang_s, theta), BOUGHT)
    for yy in baffle_ys:   # heads outside the drum, nuts on the angle's inner face
        baffle_hw.append(place(m6b, radial_point(theta, yy, ro), radial_dir(theta, outward=True)))
        baffle_hw.append(place(m6n, radial_point(theta, yy, d_leg - tb_ang), radial_dir(theta, outward=False)))
add("hardware-drum-baffles (bought, 12 x M6 x 12 button head, nuts)", compound(baffle_hw), HARDWARE)
cut_list.append(("baffle-1..3", "angle 40x40x3 aluminum", P["baffle_len"], 3, "drum baffles, drilled on the drill press"))

# flat patterns for the drum sheet, the rings, and the splice (plate-local coordinates, mm)
def drum_sheet_sketch():
    W, L = P["drum_flat_w"], P["drum_l"]
    sk = cq.Workplane("XY").center(W / 2, L / 2).rect(W, L).extrude(1)
    pitch = W / P["tab_n"]
    for i in range(P["tab_n"]):
        xc = pitch * (i + 0.5)
        for yc, free in ((L + P["tab_h"] / 2, ">Y"), (-P["tab_h"] / 2, "<Y")):
            tab = cq.Workplane("XY").center(xc, yc).rect(P["tab_w"], P["tab_h"]).extrude(1).edges("|Z").edges(free).fillet(P["small_corner_r"])
            sk = sk.union(tab)
            sk = sk.cut(cq.Workplane("XY").center(xc, yc).circle(P["tab_hole_d"] / 2).extrude(3).translate((0, 0, -1)))
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
spl_sk = cq.Workplane("XY").center(P["splice_w"] / 2, spl_len / 2).rect(P["splice_w"], spl_len).extrude(1).edges("|Z").fillet(P["small_corner_r"])
for xc in (P["seam_inset"], P["splice_w"] - P["seam_inset"]):
    for yc in seam_ys:
        spl_sk = spl_sk.cut(cq.Workplane("XY").center(xc, yc - P["ring_t"] - 1).circle(P["seam_hole_d"] / 2).extrude(3).translate((0, 0, -1)))
export_dxf("drum-splice", spl_sk)

# ---------------------------------------------------------------------------
# Drive: motor, pulley, blower, belt, idler; heat module tray; power module; exhaust; rollers
# ---------------------------------------------------------------------------
cut_list.append(("belt (bought)", "PJ poly-V, 5 ribs", round(belt_len), 1, "length of the drawn path round the drum, the pulley and the idler; pick the nearest catalog J length (V-012)"))
mz, my0 = P["motor_axis_z"], P["motor_y0"]
ml, md = P["motor_len"], P["motor_d"]
motor = cq.Workplane("XZ").center(0, mz).circle(md / 2).extrude(-(ml - 24)).translate((0, my0 + 12, 0))           # frame
for yy in (my0, my0 + ml - 12):                                                                                    # end bells
    motor = motor.union(cq.Workplane("XZ").center(0, mz).circle(md / 2 - 10).extrude(-12).translate((0, yy, 0)))
motor = motor.union(cq.Workplane("XZ").center(0, mz).circle(7.5).extrude(-(my0 - (P["blower_y0"] + P["blower_w"]))).translate((0, P["blower_y0"] + P["blower_w"], 0)))   # front shaft to the blower
motor = motor.union(cq.Workplane("XZ").center(0, mz).circle(7.5).extrude(-4).translate((0, my0 + ml, 0)))          # rear shaft to the pulley
motor = motor.union(box(-25, 25, my0 + 70, my0 + 130, mz + md / 2 - 5, mz + md / 2 + 20))                          # terminal box
add("motor (bought)", motor, BOUGHT)
for i, yy in enumerate((my0 + 25, my0 + ml - 55)):   # two cradle mounts from the motor mount kit, bolted to the base pan
    cradle = box(-35, 35, yy, yy + 30, 0, mz - 20).cut(cq.Workplane("XZ").center(0, mz).circle(md / 2 + 0.5).extrude(-40).translate((0, yy - 5, 0)))
    add(f"motor-mount-{i+1} (bought, cradle)", cradle, BOUGHT)
pulley = cq.Workplane("XZ").center(0, mz).circle(P["motor_pulley_d"] / 2).extrude(-16).translate((0, P["belt_y"] - 8, 0))
for k in range(4):   # four grooves between the five ribs
    gy = P["belt_y"] - 4.5 + 3.0 * k
    pulley = pulley.cut(cq.Workplane("XZ").center(0, mz).circle(P["motor_pulley_d"] / 2 + 1).circle(P["motor_pulley_d"] / 2 - 1.2).extrude(-1.2).translate((0, gy - 0.6, 0)))
pulley = pulley.union(cq.Workplane("XZ").center(0, mz).circle(10.0).extrude(-6).translate((0, P["belt_y"] + 8, 0)))   # hub with the set screw
add("pulley (bought)", pulley, BOUGHT)
blower = cq.Workplane("XZ").center(0, mz).circle(P["blower_d"] / 2).extrude(-P["blower_w"]).translate((0, P["blower_y0"], 0))
blower = blower.cut(cq.Workplane("XZ").center(0, mz).circle(65.0).extrude(-8).translate((0, P["blower_y0"], 0)))     # inlet mouth, facing the transition
blower = blower.union(box(100, 270, P["blower_y0"] + 26, my0, mz - 10, mz + 70))                                     # tangential outlet turning into the exhaust duct
add("blower (bought)", blower, BOUGHT)
P["exhaust_y0"] = my0
add("heat-module-tray", box(P["tray_x0"], P["tray_x0"] + P["tray_w"], P["tray_y0"], P["tray_y0"] + P["tray_depth"], e + es, e + es + P["t_tray"]), STEEL)
add("heat-module (envelope)", box(P["tray_x0"] + 20, P["tray_x0"] + P["tray_w"] - 20, P["tray_y0"] + 20, P["tray_y0"] + P["tray_depth"] - 20, e + es + 2, e + es + 2 + 160), BOUGHT)
add("power-module (envelope)", box(P["pm_x0"], P["pm_x0"] + P["pm_w"], P["pm_y0"], P["pm_y0"] + P["pm_depth"], e, e + P["pm_h"]), BOUGHT)
exh = (cq.Workplane("XZ").center(P["exhaust_x"], P["exhaust_z"]).circle(P["exhaust_d"] / 2).extrude(-(D - P["exhaust_y0"]))
       .translate((0, P["exhaust_y0"], 0)))
add("exhaust-duct (bought)", exh, DUCT)
# cord: strain relief bushing in the rear lower panel, cord to the power module and 60 mm out the back
bush = hexagon(24.0, 8.0).translate((0, 0, 0)).union(cq.Workplane("XY").circle(10.0).extrude(10).translate((0, 0, 8)).edges(">Z").fillet(3.0))
bush = bush.union(cq.Workplane("XY").circle(10.9).extrude(tp + 10.5).translate((0, 0, -tp - 10)))   # thread through the panel
bush = bush.union(hexagon(26.0, 5.0).translate((0, 0, -tp - 5)))                                     # locknut inside
bush = bush.cut(cq.Workplane("XY").circle(4.6).extrude(40).translate((0, 0, -20)))                   # the cord passes through
add("cord-bushing (bought, PG16 strain relief)", place(bush, (-250, D + tp, 120), (0, 1, 0)), RUBBER)
cord = cq.Workplane("XZ").center(-250, 120).circle(4.5).extrude(-(D + tp + 18 + 60 - (P["pm_y0"] + P["pm_depth"]))).translate((0, P["pm_y0"] + P["pm_depth"], 0))
add("power-cord (bought)", cord, RUBBER)
roller_w = 25.0   # catalog roller width, measured at V-106
for i, (x, z, d) in enumerate(rollers):
    r = cq.Workplane("XZ").center(x, z).circle(P["roller_d"] / 2).extrude(-roller_w).translate((0, y0d + L - P["roller_inset"] - roller_w, 0))
    add(f"roller-rear-{i+1} (bought)", r, BOUGHT)
    r = cq.Workplane("XZ").center(x, z).circle(P["roller_d"] / 2).extrude(-roller_w).translate((0, y0d + P["roller_inset"], 0))
    add(f"roller-front-{i+1} (bought)", r, BOUGHT)

# belt: the drawn path, offset to the belt's thickness, extruded to its width
edges_ = []
for i in range(3):
    pa, pb = belt_runs[i]
    edges_.append(cq.Edge.makeLine(cq.Vector(pa[0], 0, pa[1]), cq.Vector(pb[0], 0, pb[1])))
    c_next = belt_circles[(i + 1) % 3]
    p_out = belt_runs[(i + 1) % 3][0]
    mid, _ = arc_mid(c_next, pb, p_out)
    edges_.append(cq.Edge.makeThreePointArc(cq.Vector(pb[0], 0, pb[1]), cq.Vector(mid[0], 0, mid[1]), cq.Vector(p_out[0], 0, p_out[1])))
belt_wire = cq.Wire.assembleEdges(edges_)
belt_face = cq.Face.makeFromWires(belt_wire.offset2D(BT / 2)[0], [belt_wire.offset2D(-BT / 2)[0]])
belt = cq.Workplane("XY").add(cq.Solid.extrudeLinear(belt_face, cq.Vector(0, BW, 0))).translate((0, P["belt_y"] - BW / 2, 0))
add("belt (bought, PJ 5 rib)", belt, RUBBER)
# idler: flat pulley on an arm that pivots on a bracket on the base pan, pulled toward the belt by a spring on a second bracket
ix, iz = P["idler_x"], P["idler_z"]
idler = cq.Workplane("XZ").center(ix, iz).circle(P["idler_d"] / 2).extrude(-P["idler_w"]).translate((0, P["belt_y"] - P["idler_w"] / 2, 0))
for yy in (P["belt_y"] - P["idler_w"] / 2 - 1.5, P["belt_y"] + P["idler_w"] / 2):   # flanges
    idler = idler.union(cq.Workplane("XZ").center(ix, iz).circle(P["idler_d"] / 2 + 2).extrude(-1.5).translate((0, yy, 0)))
idler = idler.cut(cq.Workplane("XZ").center(ix, iz).circle(4.1).extrude(-30).translate((0, P["belt_y"] - 15, 0)))
add("idler-pulley (bought, flat idler 40 with bearing)", idler, BOUGHT)
piv = (-115.0, 25.0)
anchor = (65.0, 25.0)
arm_len = math.hypot(ix - piv[0], iz - piv[1])
arm_ang = math.degrees(math.atan2(iz - piv[1], ix - piv[0]))
arm_y0 = ARM_Y0                                                   # arm 390..394, 0.5 in front of the idler's front flange
arm = box(-12.5, arm_len + 12.5, arm_y0, arm_y0 + 4.0, -12.5, 12.5).edges("|Y").fillet(6.0)
for xx in (0.0, arm_len):
    arm = arm.cut(cq.Workplane("XZ").center(xx, 0).circle(4.25).extrude(-10).translate((0, arm_y0 - 3, 0)))
arm = arm.cut(cq.Workplane("XZ").center(0.6 * arm_len, 0).circle(2.6).extrude(-10).translate((0, arm_y0 - 3, 0)))   # spring post hole
arm = arm.rotate((0, 0, 0), (0, 1, 0), -arm_ang).translate((piv[0], 0, piv[1]))
add("idler-arm (flat bar 25x4, cut to length)", arm, ALU)
cut_list.append(("idler-arm", "flat bar 25x4 aluminum", round(arm_len + 25, 1), 1, "idler arm, two 8.5 holes and one 5.2 hole on the drill press"))
# axle: head in front of the arm, nut behind the idler's rear flange
ax_y1 = P["belt_y"] + P["idler_w"] / 2 + 1.5 + 5.0
axle = cq.Workplane("XZ").center(ix, iz).circle(4.0).extrude(-(ax_y1 - arm_y0)).translate((0, arm_y0, 0))
axle = axle.union(place(hexagon(13.0, 5.0), (ix, arm_y0, iz), (0, -1, 0))).union(place(hexagon(13.0, 5.0), (ix, ax_y1 - 5.0, iz), (0, 1, 0)))
add("hardware-idler-axle (bought, M8 x 30 bolt, nut)", axle, HARDWARE)
# pivot bracket: angle on the pan, vertical leg against the arm's front face, horizontal leg forward
brk = box(-140, -90, arm_y0 - 3.0, arm_y0, 0, 40).union(box(-140, -90, arm_y0 - 40.0, arm_y0, 0, 3))
brk = brk.cut(cq.Workplane("XZ").center(piv[0], piv[1]).circle(4.25).extrude(-10).translate((0, arm_y0 - 5, 0)))
for (x, y) in bracket_pts[:2]:
    brk = brk.cut(cq.Workplane("XY").center(x, y).circle(P["m6_hole"] / 2).extrude(10).translate((0, 0, -2)))
add("idler-bracket (angle 40x40x3, cut to length)", brk, ALU)
cut_list.append(("idler-bracket, spring-bracket", "angle 40x40x3 aluminum", 50, 2, "idler pivot and spring anchor, bolted through the base pan"))
pivot_bolt = cq.Workplane("XZ").center(piv[0], piv[1]).circle(4.0).extrude(-(arm_y0 + 4.0 + 5.0 + 1.0 - (arm_y0 - 3.0 - 5.0))).translate((0, arm_y0 - 8.0, 0))
pivot_bolt = pivot_bolt.union(place(hexagon(13.0, 5.0), (piv[0], arm_y0 - 3.0, piv[1]), (0, -1, 0))).union(place(hexagon(13.0, 5.0), (piv[0], arm_y0 + 4.0, piv[1]), (0, 1, 0)))
add("hardware-idler-pivot (bought, M8 x 25 bolt, nut)", pivot_bolt, HARDWARE)
sb = box(anchor[0] - 20, anchor[0] + 20, arm_y0 - 3.0, arm_y0, 0, 40).union(box(anchor[0] - 20, anchor[0] + 20, arm_y0 - 40.0, arm_y0, 0, 3))
for (x, y) in bracket_pts[2:]:
    sb = sb.cut(cq.Workplane("XY").center(x, y).circle(P["m6_hole"] / 2).extrude(10).translate((0, 0, -2)))
sb = sb.cut(cq.Workplane("XZ").center(*anchor).circle(2.6).extrude(-10).translate((0, arm_y0 - 5, 0)))   # spring post hole
add("spring-bracket (angle 40x40x3, cut to length)", sb, ALU)
# spring behind the belt plane, in front of the heat module tray, on two posts that reach back from the arm and the bracket
a_mid = (piv[0] + 0.6 * (ix - piv[0]), piv[1] + 0.6 * (iz - piv[1]))
sp_y = P["belt_y"] + BW / 2 + 1.0 + 4.0                           # spring centre line: 1 mm behind the belt's back face
post_y1 = sp_y + 4.5
posts = (cq.Workplane("XZ").center(*a_mid).circle(2.5).extrude(-(post_y1 - arm_y0 + 3.0)).translate((0, arm_y0 - 3.0, 0))
         .union(cq.Workplane("XZ").center(*anchor).circle(2.5).extrude(-(post_y1 - arm_y0 + 6.0)).translate((0, arm_y0 - 6.0, 0))))
add("hardware-idler-spring-posts (bought, 2 x M5 shoulder posts)", posts, HARDWARE)
d_sp = (anchor[0] - a_mid[0], anchor[1] - a_mid[1])
sp_len = math.hypot(*d_sp)
u_sp = (d_sp[0] / sp_len, 0.0, d_sp[1] / sp_len)
hook, post_r = 7.0, 2.6
sp_free = sp_len - 2 * post_r                                                                # from post surface to post surface
spring = cq.Workplane("XY").circle(4.0).extrude(sp_free - 2 * hook).translate((0, 0, hook))   # coil body between the hooks
for t0 in (0.0, sp_free - hook):
    spring = spring.union(cq.Workplane("XY").circle(0.9).extrude(hook).translate((0, 0, t0)))  # hooks, drawn as thin wire
spring = place(spring, (a_mid[0] + u_sp[0] * post_r, sp_y, a_mid[1] + u_sp[2] * post_r), u_sp)
add("idler-spring (bought, extension spring)", spring, HARDWARE)
assert abs(arm_y0 - 20.0 - BRACKET_Y) < 1e-9
brk_bolts = [place(hex_bolt_m6(), (x, y, 3.0), (0, 0, 1)) for (x, y) in bracket_pts]
brk_bolts += [place(nut(P["m6_nut_af"], P["m6_nut_h"], 6.2), (x, y, -P["t_base"]), (0, 0, -1)) for (x, y) in bracket_pts]
add("hardware-idler-brackets (bought, 4 x M6 x 12 hex, nuts, through the base pan)", compound(brk_bolts), HARDWARE)

# ---------------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------------
assy = cq.Assembly(name="osa-dryer")
for name, solid, color, plate, t in parts:
    assy.add(solid, name=name, color=color)
assy.save(os.path.join(OUT, "step", "osa-dryer-assembly.step"))
for name, solid, color, plate, t in parts:
    if "(" in name:   # bought parts, envelopes, hardware and cut-to-length catalog stock get no STEP of their own
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
    label = f'<text x="20" y="30" font-family="Helvetica, Arial, sans-serif" font-size="18">osa-dryer check view: {vname} (draft 4, not for cutting)</text>'
    open(path, "w", encoding="utf-8").write(head + body + label + "</svg>")

if "--no-views" not in sys.argv:
    VIEW_PARTS = [(n, s) for n, s, _, _, _ in parts if not n.startswith("hardware-")]   # bolts make the line drawings unreadable
    compound_all = cq.Compound.makeCompound([s.val() if hasattr(s, "val") else s for _, s in VIEW_PARTS])
    OUTER = ("side-panel-left", "side-panel-right", "front-upper-panel", "front-lower-panel", "rear-upper-panel",
             "rear-lower-panel", "top-panel", "console-face", "console-cap", "console-cheek-left", "console-cheek-right",
             "door-ring", "door-disc")
    inner = cq.Compound.makeCompound([s.val() if hasattr(s, "val") else s for n, s in VIEW_PARTS if n not in OUTER and not n.startswith("door-") and not n.startswith("tier0")])
    VIEWS = {
        "iso": (compound_all, (1, -1, 0.7), 180),
        "front": (compound_all, (0, -1, 0), 90),
        "side-left": (compound_all, (-1, 0, 0), 90),
        "top": (compound_all, (0, 0, 1), 90),
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
    solids = [(n, s.val() if hasattr(s, "val") else s) for n, s, _, _, _ in parts]
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
print("drum sheet flat", round(P["drum_flat_w"], 1), "x", P["drum_l"], " belt drawn length", round(P["belt_len_est"], 1),
      " belt crosses the ceiling at X", round(P["belt_cross_left"], 2), "and", round(P["belt_cross_right"], 2), " feet", P["foot_height"])
