"""osa-dryer parametric mechanical model.

One file holds every number. Run it and it writes:
  step/osa-dryer-assembly.step          the whole machine, bought parts as envelopes or representations
  step/<part>.step                      one file per part we make
  drawings/<part>.dxf                   flat pattern for every laser-cut plate (CUT layer)
  drawings/frame-cut-list.csv           every extrusion length
  drawings/view-*.svg                   views for checking, not for cutting

Coordinate system: X across the cabinet (left negative), Y from front (0) to back, Z up from the floor.
All dimensions mm. Needs cadquery (pip install cadquery). Also runs in FreeCAD's CadQuery workbench.

Status: draft 7, 2026-11-06. Draft 5 drew what the documents already called for but the model only
implied: T-slot profiles on the extrusions, laser corner radii, every panel bolt, the leveling feet, the belt
on its real path with the idler, the door hinges, handle, seal and catch, the Tier 0 control module, and
the detail of the motor, pulley and blower. Draft 6 settled the three things draft 5 found (DECISIONS.md,
2026-11-06): the drum ring bore grows to 540 and the lint slot becomes a curved slot inside it, the heat
module leaves by the back under a hood into a raised riser, and the console is a vertical box on its own small
4040 frame that holds the whole UCI envelope. Draft 7 draws the two modules and the drum's support: the electric
heat module (a bolted 1.5 mm duct box on the tray with the catalog element, a round collar under the hood, and its
contactor and terminals on a DIN rail behind the box), the common power module as a plate with five DIN rails on
the rear cross rails behind the rear upper panel (DECISIONS.md, 2026-11-06), the tray rails the full depth of the
cabinet, nylon glides that locate the drum endways with the felts in two arcs round them, shoulder-screw roller
studs, the 20 mm motor pulley (56 drum rpm; 30 gave 83), and the grommets the cord and harnesses pass through.
Every M4 is a button head. Bought parts (motor, blower, timers, rollers, hinges, feet, element, DIN devices) are
drawn as envelopes or representations from published figures that have NOT been measured. docs/verification.md
says which measurement unlocks which DXF. Do not cut a plate whose gate is open.
"""
import csv
import math
import os
import re
import sys

import cadquery as cq
from cadquery import exporters

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
DRAFT = 7
HERE = os.path.dirname(os.path.abspath(__file__))
for sub in ("step", "drawings"):
    os.makedirs(os.path.join(OUT, sub), exist_ok=True)
# the Tier 0 faceplate's numbers live with its drawing (mechanical/drawings/tier0_drawings.py); this model draws the
# module from them so the faceplate here and tier0-faceplate.dxf cannot drift apart
sys.path.insert(0, os.path.join(HERE, "..", "drawings"))
import tier0_drawings as T0  # noqa: E402

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
    drum_t=0.8, ring_t=2.0, ring_id=540.0,                     # 540 bore (draft 6): room for the curved lint slot inside it
    tab_n=30, tab_w=24.0, tab_h=16.0, tab_hole_d=4.5,          # 16 tall tabs (draft 6): the felt rides on the ring face inboard of them
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
    roller_d=60.0, roller_angle_deg=32.0, roller_shaft_hole_d=8.5, roller_bore_d=10.5,   # 32 degrees (draft 7): the studs' nuts clear the lint duct; 8.5 hole for the stud's M8 thread
    roller_stud_head_d=16.0, roller_stud_head_h=7.0, roller_stud_shoulder=35.0, roller_stud_thread=13.0, roller_spacer=8.5,   # ISO 7379 shoulder screw 10 x 35, M8 thread, bearing on the bulkhead; spacer 16 x 10.5 x 8.5; 1.0 shim under the head
    roller_inset_rear=-1.5,   # the rear rollers stand 1.5 proud of the drum's rear end so both ends use the same 35 shoulder (front gap 8.5, rear gap 10 - 1.5)
    glide_w=45.0, glide_h=20.0, glide_r=282.0, glide_angle_deg=45.0, glide_t_front=8.0, glide_t_rear=9.5,   # two nylon drum glides per bulkhead at 10 and 2 o'clock, on the felt's radius; 0.5 end float
    motor_pulley_d=20.0,      # 1725 rpm x 20 / 620 = 56 drum rpm (draft 7: 30 gave 83, outside the 45 to 55 target)
    # lint filter slot in the front bulkhead: a curved slot inside the ring bore, below the door opening (draft 6)
    lint_slot_r0=238.0, lint_slot_r1=266.0, lint_slot_half_deg=36.0,   # 8 outside the 460 opening, 4 inside the 540 bore; 8865 mm2
    # rear air inlet zone
    inlet_w=200.0, inlet_h=130.0, inlet_above_axis=50.0, inlet_hole_d=10.0, inlet_pitch=14.0,   # inside the ring opening (R 240)
    # riser duct: vertical part behind the rear cross rails, and a hood under the mid cross rail over the heat module's outlet
    riser_w=260.0, riser_depth=50.0, riser_z0=230.0, hood_w=300.0, hood_y0=448.0, hood_h=28.0,   # the hood reaches forward over the module's collar (draft 7)
    hood_gasket_od=150.0, hood_gasket_t=3.0,   # foam ring glued under the hood; the collar's rim brushes it
    # console: a vertical box at the rear of the top on its own 4040 sub-frame (draft 6), holding the full UCI envelope
    console_h=200.0, uci_ap_z_off=83.0,   # console depth: from the top rear cross rail to the back (set below). Aperture centre above the top panel: the module's nuts under the front rail, the faceplate under its bolts
    uci_ap_w=500.0, uci_ap_h=120.0, uci_hole_x=520.0, uci_hole_y=140.0, uci_hole_d=4.5,   # UCI-D draft 5: 500 wide, six holes (the corners plus two on the centre line)
    # fasteners
    m6_hole=6.5, m4_hole=4.5, panel_pitch=150.0,
    # bay layout (envelopes)
    motor_axis_z=120.0, motor_len=200.0, motor_d=140.0, motor_y0=190.0,   # motor behind the blower, pulley on its rear shaft
    blower_d=220.0, blower_w=100.0, blower_y0=84.0,                       # blower on the front shaft, inlet facing front
    lint_duct_y0=5.0, lint_duct_depth=33.0, lint_duct_top=445.0,         # between the front panel (behind the ring bolts' nuts and tips) and the front bulkhead
    tray_w=340.0, tray_depth=280.0, tray_y0=420.0, tray_x0=-170.0, t_tray=1.5,   # on the two 2020 tray rails (X +-150..170), draft 7; starts 3 behind the idler spring (409..417)
    # electric heat module (draft 7): a laser-cut 1.5 mm duct box on the tray, joined with 20x20x2 aluminium angle and M4 (no
    # brake, no rivets), the catalog element along X inside it on two angle rails, a round catalog collar on top under the
    # riser's hood, the contactor and terminal strips on a DIN rail on a plate behind the box
    hm_box_x=145.0, hm_box_y0=422.0, hm_box_y1=627.0, hm_box_h=110.0, t_duct=1.5,
    hm_elem_l=267.0, hm_elem_w=190.0, hm_elem_h=51.0,          # Whirlpool 279838 class element: 10.5 x 7.5 x 2 in from a seller listing (V-108)
    hm_elem_z0=81.5,                                            # element frame's underside, on the rails' top legs
    hm_collar_d=125.0, hm_collar_y=525.0, hm_collar_top=227.0, hm_collar_flange_d=155.0,   # 125 flanged starting collar, 3 under the hood's gasket
    hm_inlet_y=(450.0, 600.0), hm_inlet_z=(84.0, 144.0),        # opening in the box's left end: 150 x 60, 9000 mm2
    hm_term_cut=(525.0, 107.0, 40.0, 25.0),                     # the element's terminals leave through the right end: (yc, zc, w, h), final position from the element bought (V-108)
    hm_plate_y=634.0, hm_plate_h=100.0,                         # the terminal plate across the tray behind the box, DIN rail on its rear face
    hm_thermostat_x=110.0, hm_thermostat_y=500.0,               # 279816 class high-limit and thermal cut-off on the box top, either side of the collar, brackets along Y
    # common power module (draft 7): a plate on the rear faces of the two rear cross rails, left of the riser, behind the
    # rear upper panel; five DIN rails across it, the mains rails under a cover, a barrier between mains and SELV
    pm_x0=-300.0, pm_w=150.0, pm_z0=270.0, pm_z1=990.0, pm_rails_z=(360.0, 470.0, 580.0, 700.0, 820.0), pm_barrier_z=640.0,
    pm_cover_standoff=75.0, pm_cover_z0=310.0, pm_cover_z1=640.0,   # the cover starts above the bay ceiling's rear bolt heads (307)
    grommet_cord=(-275.0, 690.0, 22.0), grommet_harness=(-200.0, 690.0, 30.0), grommet_console=(-225.0, 690.0, 22.0),   # (x, y, hole) in the bay ceiling (cord, bay harness) and the top panel (console harness)
    cord_top_z=320.0,          # the cord ends under X1 on the power module's first rail
    exhaust_d=102.0, exhaust_x=230.0, exhaust_z=150.0,
    cord_hole_d=22.0, cord_x=-275.0, cord_y=690.0,   # cord strain relief bushing through the base pan at the rear left (draft 6); the cord goes up through the bay ceiling to the power module (draft 7); confirm against the bushing bought, V-112
    motor_shaft_d=12.7,        # 1/2 in dryer motor shaft both ends (V-106)
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
    foot_pad_d=50.0, foot_pad_h=10.0, foot_hex_af=19.0, foot_hex_h=8.0, foot_stud_d=8.0, foot_stud_in=35.0, foot_hole_d=8.5,   # 18 under the pan: room for the cord
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
    # felt seals (7b Seals): 10 mm polyester felt arcs glued to both bulkheads, drawn compressed to the gap the drum leaves
    felt_ri=273.0, felt_ro=291.0, felt_t=8.0, felt_t_rear=10.0,   # on the ring face between the 540 bore and the tab tips (293.2); front gap 8.5, rear gap 10
    # Tier 0 control module (controls/tier0-mechanical): faceplate numbers from mechanical/drawings/tier0_drawings.py
    fp_w=540.0, fp_h=160.0, fp_r=10.0, fp_t=2.0,
    knob_d=40.0, knob_skirt_h=3.0, knob_body_d=30.0, knob_h=20.0,
)
P["drum_rim_r"] = P["drum_d"] / 2
P["drum_flat_w"] = math.pi * (P["drum_d"] - P["drum_t"])   # sheet length at the mid-surface
P["drum_axis_z"] = P["bay_top"] + P["t_base"] + P["drum_clear_bottom"] + P["drum_d"] / 2
P["H_body"] = P["drum_axis_z"] + P["drum_d"] / 2 + P["drum_clear_top"] + P["ext"]
P["H_total"] = P["H_body"] + P["t_panel"] + P["console_h"] + P["t_panel"]   # body, top panel, console box, cap
P["front_bulk_y"] = P["ext"]                         # plate sits behind the front rails
P["rear_bulk_y"] = P["drum_front_y"] + P["drum_l"] + 10.0   # plate front face
P["rear_cross_y"] = P["rear_bulk_y"] + P["t_bulk"]  # rear cross rails start here
P["console_depth"] = P["D"] - P["rear_cross_y"]      # the console's front posts stand over the top rear cross rail (draft 6): 138.5
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


def plate_bolts(name, pts, n, bolt=None, label=None):
    """One compound part holding a bolt at every point in pts (world points on the surface), heads along n."""
    bolt = bolt if bolt is not None else hex_bolt_m6()
    label = label or "M6 x 12 hex, washers, T-nuts"
    if not pts:
        return None
    sols = [place(bolt, p, n) for p in pts]
    return add(f"hardware-{name} (bought, {len(pts)} x {label})", compound(sols), HARDWARE)


def sector_xz(xc, zc, r0, r1, half_deg, depth):
    """An annular sector about (xc, zc) in the XZ plane, centred on straight down, extruded along +Y from Y 0 by depth."""
    ring = cq.Workplane("XZ").center(xc, zc).circle(r1).circle(r0).extrude(-depth)
    L = 2 * r1
    pts = [(xc, zc)] + [(xc + L * math.sin(math.radians(a)), zc - L * math.cos(math.radians(a))) for a in (-half_deg, -half_deg / 2, 0, half_deg / 2, half_deg)]
    wedge = cq.Workplane("XZ").polyline(pts).close().extrude(-depth)
    return ring.intersect(wedge)


def sector_xy(xc, yc, r0, r1, half_deg, depth):
    ring = cq.Workplane("XY").center(xc, yc).circle(r1).circle(r0).extrude(depth)
    L = 2 * r1
    pts = [(xc, yc)] + [(xc + L * math.sin(math.radians(a)), yc - L * math.cos(math.radians(a))) for a in (-half_deg, -half_deg / 2, 0, half_deg / 2, half_deg)]
    wedge = cq.Workplane("XY").polyline(pts).close().extrude(depth)
    return ring.intersect(wedge)


def fillet_corners(solid, axis_sel, r):
    return solid.edges(axis_sel).fillet(r) if r > 0 else solid


def plate_xz(name, x0, x1, z0, z1, y0, t, holes=(), rect_cuts=(), circ_cuts=(), slots=(), sectors=(), r=None, bolt_side=None, bolt_d=None, bolt_skip=(), bolt=None, bolt_label=None):
    """A flat plate in the XZ plane (front/rear facing), thickness along +Y from y0, corners rounded r.
    holes: (x, z, d). rect_cuts: (xc, zc, w, h). circ_cuts: (x, z, d). slots: (xc, zc, w, h) rounded ends.
    sectors: (xc, zc, r0, r1, half_deg) curved slots centred on straight down from (xc, zc).
    bolt_side: -1 puts a bolt head on the y0 face at every hole of diameter bolt_d, +1 on the y0+t face."""
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
    for (xc, zc, r0, r1, half) in sectors:
        solid = solid.cut(sector_xz(xc, zc, r0, r1, half, t + 2).translate((0, y0 - 1, 0)))
    add(name, solid, STEEL, plate=True, t=t)
    # 2D for DXF: same features, in plate-local coordinates (x right, y up)
    sk = fillet_corners(cq.Workplane("XY").center((x0 + x1) / 2, (z0 + z1) / 2).rect(w, h).extrude(1), "|Z", r)
    for (x, z, d) in list(holes) + list(circ_cuts):
        sk = sk.cut(cq.Workplane("XY").center(x, z).circle(d / 2).extrude(3).translate((0, 0, -1)))
    for (xc, zc, cw, ch) in rect_cuts:
        sk = sk.cut(cq.Workplane("XY").center(xc, zc).rect(cw, ch).extrude(3).translate((0, 0, -1)))
    for (xc, zc, cw, ch) in slots:
        sk = sk.cut(cq.Workplane("XY").center(xc, zc).slot2D(cw, ch).extrude(3).translate((0, 0, -1)))
    for (xc, zc, r0, r1, half) in sectors:
        sk = sk.cut(sector_xy(xc, zc, r0, r1, half, 3).translate((0, 0, -1)))
    export_dxf(name, sk)
    if bolt_side:
        yb = y0 if bolt_side < 0 else y0 + t
        plate_bolts(name, [(x, yb, z) for (x, z, d) in holes if abs(d - (bolt_d or P["m6_hole"])) < 1e-6 and (x, z) not in bolt_skip], (0, bolt_side, 0), bolt, bolt_label)
    return solid


def plate_xy(name, x0, x1, y0, y1, z0, t, holes=(), rect_cuts=(), circ_cuts=(), r=None, bolt_side=None, bolt_skip=(), bolt_d=None, bolt=None, bolt_label=None):
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
        plate_bolts(name, [(x, y, zb) for (x, y, dd) in holes if abs(dd - (bolt_d or P["m6_hole"])) < 1e-6 and (x, y) not in bolt_skip], (0, 0, bolt_side), bolt, bolt_label)
    return solid


def plate_yz(name, y0, y1, z0, z1, x0, t, holes=(), rect_cuts=(), r=None, bolt_side=None, bolt_d=None, bolt=None, bolt_label=None):
    """A flat plate in the YZ plane (side panel), thickness along +X from x0. holes: (y, z, d). rect_cuts: (yc, zc, w, h)."""
    r = P["plate_corner_r"] if r is None else r
    d, h = y1 - y0, z1 - z0
    solid = fillet_corners(cq.Workplane("YZ").center((y0 + y1) / 2, (z0 + z1) / 2).rect(d, h).extrude(t), "|X", r).translate((x0, 0, 0))
    for (y, z, dd) in holes:
        solid = solid.cut(cq.Workplane("YZ").center(y, z).circle(dd / 2).extrude(t + 2).translate((x0 - 1, 0, 0)))
    for (yc, zc, cw, ch) in rect_cuts:
        solid = solid.cut(cq.Workplane("YZ").center(yc, zc).rect(cw, ch).extrude(t + 2).translate((x0 - 1, 0, 0)))
    add(name, solid, STEEL, plate=True, t=t)
    sk = fillet_corners(cq.Workplane("XY").center((y0 + y1) / 2, (z0 + z1) / 2).rect(d, h).extrude(1), "|Z", r)
    for (y, z, dd) in holes:
        sk = sk.cut(cq.Workplane("XY").center(y, z).circle(dd / 2).extrude(3).translate((0, 0, -1)))
    for (yc, zc, cw, ch) in rect_cuts:
        sk = sk.cut(cq.Workplane("XY").center(yc, zc).rect(cw, ch).extrude(3).translate((0, 0, -1)))
    export_dxf(name, sk)
    if bolt_side:
        xb = x0 if bolt_side < 0 else x0 + t
        plate_bolts(name, [(xb, y, z) for (y, z, dd) in holes if abs(dd - (bolt_d or P["m6_hole"])) < 1e-6], (bolt_side, 0, 0), bolt, bolt_label)
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

# tray rails (draft 7): two 2020 lengths the full depth of the cabinet, lying on the front and rear bottom end rails
# at X +-150..170, each held at both ends by a 2020 inside corner bracket on the end rail's top slot. The heat
# module tray sits on them and slides out the back over the rear bottom rail.
es = P["ext_small"]
TRAY_RAIL_X = [(-170.0, -150.0), (150.0, 170.0)]
for i, (x0, x1) in enumerate(TRAY_RAIL_X):
    extrusion(f"tray-rail-{i+1}", x0, x1, 0, D, e, e + es, "2020 tray rail, on the bottom end rails")
# the brackets: 20 series inside corner brackets (legs 20, 2.5 thick, 17 wide) on the rail's outer side and the end rail's top
B20L, B20T, B20W = 20.0, 2.5, 17.0
tr_brk, tr_hw = [], []
for (x0, x1) in TRAY_RAIL_X:
    sx = -1 if x0 < 0 else 1
    xf = x0 if sx < 0 else x1            # the tray rail's outer face
    for yc in (e / 2, D - e / 2):        # on the front and rear bottom rails' top slot centre lines
        leg_v = box(min(xf, xf + sx * B20T), max(xf, xf + sx * B20T), yc - B20W / 2, yc + B20W / 2, e, e + B20L)
        leg_h = box(min(xf, xf + sx * B20L), max(xf, xf + sx * B20L), yc - B20W / 2, yc + B20W / 2, e, e + B20T)
        b = leg_v.union(leg_h)
        b = b.cut(cq.Workplane("YZ").center(yc, e + es / 2).circle(2.25).extrude(B20T + 2).translate((min(xf, xf + sx * B20T) - 1, 0, 0)))
        b = b.cut(cq.Workplane("XY").center(xf + sx * (B20L - 8.0), yc).circle(2.25).extrude(B20T + 2).translate((0, 0, e - 1)))
        tr_brk.append(b)
        tr_hw.append(place(button_bolt(4.0, P["m4_head_d"], P["m4_head_h"], 8.0, 2.5), (xf + sx * B20T, yc, e + es / 2), (sx, 0, 0)))   # into the tray rail's side slot (its centre line, 10 up)
        tr_hw.append(place(button_bolt(4.0, P["m4_head_d"], P["m4_head_h"], 8.0, 2.5), (xf + sx * (B20L - 8.0), yc, e + B20T), (0, 0, 1)))   # into the end rail's top slot
add("tray-rail-brackets (bought, 4 x 2020 inside corner brackets)", compound(tr_brk), HARDWARE)
add("hardware-tray-rails (bought, 8 x M4 x 8 button head, T-nuts for the 6 and 8 mm slots)", compound(tr_hw), HARDWARE)

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
ro, ri = P["drum_d"] / 2, P["drum_d"] / 2 - P["drum_t"]
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

# roller stud holes, the same pattern on both bulkheads: on the rim radius plus the roller radius, 32 degrees each side of
# bottom (draft 7: 30 put the studs' nuts into the lint duct's sides)
rollers = []
rr = P["drum_rim_r"] + P["roller_d"] / 2
for ang in (-P["roller_angle_deg"], P["roller_angle_deg"]):
    rollers.append((rr * math.sin(math.radians(ang)), az - rr * math.cos(math.radians(ang)), P["roller_shaft_hole_d"]))
# drum glides (draft 7): two nylon pads per bulkhead at 10 and 2 o'clock on the felt's radius, taking the drum's end
# thrust; the felt is laid in two arcs between them. Two M4 holes each, through the bulkhead.
GLIDE_ANGLES = (-P["glide_angle_deg"], P["glide_angle_deg"])     # from straight up, viewed from the front
glide_pts, glide_holes = [], []
for ang in GLIDE_ANGLES:
    a = math.radians(ang)
    cx_, cz_ = P["glide_r"] * math.sin(a), az + P["glide_r"] * math.cos(a)
    tx_, tz_ = math.cos(a), -math.sin(a)      # tangent, along the pad
    glide_pts.append((cx_, cz_, ang))
    for k in (-12.0, 12.0):
        glide_holes.append((cx_ + k * tx_, cz_ + k * tz_, P["m4_hole"]))

# front bulkhead: door opening, lint slot, front roller holes; bolt heads on its back face (the rails are in front of it)
plate_xz("front-bulkhead", bulk_x0, bulk_x1, bulk_z0, bulk_z1, P["front_bulk_y"], tb,
         holes=bulk_holes(front=True) + rollers + glide_holes,
         circ_cuts=[(0, az, P["door_opening_d"])],
         sectors=[(0, az, P["lint_slot_r0"], P["lint_slot_r1"], P["lint_slot_half_deg"])], bolt_side=+1)
P["lint_slot_area"] = math.radians(2 * P["lint_slot_half_deg"]) / 2 * (P["lint_slot_r1"] ** 2 - P["lint_slot_r0"] ** 2)
assert P["lint_slot_r1"] < P["ring_id"] / 2 and P["lint_slot_r0"] > P["door_opening_d"] / 2, "lint slot must sit between the door opening and the ring bore"

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
         holes=bulk_holes() + rollers + inlet + glide_holes, bolt_side=-1)


def about_drum_axis(shape, theta_deg):
    return shape.rotate((0, 0, az), (0, 1, az), theta_deg)


# felt seals and glides (7b Seals, draft 7): on the rear bulkhead's front face against the rear ring, and on the front
# bulkhead's back face against the front ring; both ride on the ring face between the 540 bore and the tab tips. Each
# felt is two arcs of strip (a long one round the bottom, a short one over the top) with a glide pad in each gap; the
# pads carry the drum's end thrust so the felt only seals. The pads are 8 thick at the front (the felt's thickness) and
# 10 at the rear, where the ring face is 2 further from the bulkhead.
assert P["felt_ro"] < ri - P["tab_h"] and P["felt_ri"] > P["ring_id"] / 2, "felt must sit on the ring face inboard of the tabs"
assert P["glide_r"] - P["glide_h"] / 2 >= P["felt_ri"] - 1 and P["glide_r"] + P["glide_h"] / 2 <= P["felt_ro"] + 1, "glides in the felt band"
pad_half_deg = math.degrees((P["glide_w"] + 2.0) / 2 / P["glide_r"])        # half the gap each pad takes, 1 mm clear each side
long_half = 180.0 - P["glide_angle_deg"] - pad_half_deg                     # the long arc, centred on straight down
short_half = P["glide_angle_deg"] - pad_half_deg                            # the short arc, centred on straight up
P["felt_long_len"] = 2 * math.radians(long_half) * P["glide_r"]
P["felt_short_len"] = 2 * math.radians(short_half) * P["glide_r"]


def felt_arcs(y0, t):
    long_ = sector_xz(0, az, P["felt_ri"], P["felt_ro"], long_half, t).translate((0, y0, 0))
    short_ = about_drum_axis(sector_xz(0, az, P["felt_ri"], P["felt_ro"], short_half, t).translate((0, y0, 0)), 180.0)
    return long_, short_


def glide_pads(y0, t, pocket_far):
    """Two pads from Y y0 to y0 + t, long axis along the tangent; hex pockets 4.5 deep for the M4 nuts open on the ring
    side (the far, +Y face if pocket_far, else the near face), cut with the nut's own placement so the hexagons agree."""
    pads = []
    for (cx_, cz_, ang) in glide_pts:
        pad = box(-P["glide_w"] / 2, P["glide_w"] / 2, 0, t, -P["glide_h"] / 2, P["glide_h"] / 2)
        pad = pad.edges("|Y").fillet(3.0)
        for k in (-12.0, 12.0):
            pad = pad.cut(cq.Workplane("XZ").center(k, 0).circle(2.25).extrude(-t - 2).translate((0, -1, 0)))
        pad = pad.rotate((0, 0, 0), (0, 1, 0), ang).translate((cx_, y0, cz_))
        a = math.radians(ang)
        for k in (-12.0, 12.0):
            px, pz = cx_ + k * math.cos(a), cz_ - k * math.sin(a)
            if pocket_far:
                pad = pad.cut(place(hexagon(7.6, 5.0), (px, y0 + t - 4.5, pz), (0, 1, 0)))
            else:
                pad = pad.cut(place(hexagon(7.6, 5.0), (px, y0 + 4.5, pz), (0, -1, 0)))
        pads.append(pad)
    return pads


fl, fs = felt_arcs(P["rear_bulk_y"] - P["felt_t_rear"], P["felt_t_rear"])
add("felt-seal-rear-long", fl, FELT, plate=True, t=P["felt_t_rear"])
add("felt-seal-rear-short", fs, FELT, plate=True, t=P["felt_t_rear"])
fl, fs = felt_arcs(P["front_bulk_y"] + tb, P["felt_t"])
add("felt-seal-front-long", fl, FELT, plate=True, t=P["felt_t"])
add("felt-seal-front-short", fs, FELT, plate=True, t=P["felt_t"])
export_dxf("felt-seal-long", sector_xy(0, 0, P["felt_ri"], P["felt_ro"], long_half, 1))
export_dxf("felt-seal-short", sector_xy(0, 0, P["felt_ri"], P["felt_ro"], short_half, 1))
cut_list.append(("felt-seal-long", "10 mm polyester felt, 18 wide strip", round(P["felt_long_len"]), 2, "or cut to drawings/felt-seal-long.dxf; one per bulkhead, round the bottom"))
cut_list.append(("felt-seal-short", "10 mm polyester felt, 18 wide strip", round(P["felt_short_len"]), 2, "or cut to drawings/felt-seal-short.dxf; one per bulkhead, over the top"))
GT_F, GT_R = P["glide_t_front"], P["glide_t_rear"]
glide_y_rear = P["rear_bulk_y"] - GT_R
add("drum-glides-front (bought, 2 x nylon drum glide pads, 45 x 20 x 8)", compound(glide_pads(P["front_bulk_y"] + tb, GT_F, True)), BOUGHT)
add("drum-glides-rear (bought, 2 x nylon drum glide pads, 45 x 20 x 9.5)", compound(glide_pads(glide_y_rear, GT_R, False)), BOUGHT)
glide_hw = []
for (gx, gz, d_) in glide_holes:
    glide_hw.append(place(button_bolt(4.0, P["m4_head_d"], P["m4_head_h"], 8.0, 2.5), (gx, P["front_bulk_y"], gz), (0, -1, 0)))      # head in the front gap
    glide_hw.append(place(nut(P["m4_nut_af"], P["m4_nut_h"], 4.2), (gx, P["front_bulk_y"] + tb + GT_F - 4.5, gz), (0, 1, 0)))        # sunk in the pad
    glide_hw.append(place(button_bolt(4.0, P["m4_head_d"], P["m4_head_h"], 10.0, 2.5), (gx, P["rear_bulk_y"] + tb, gz), (0, 1, 0)))   # head in the rear compartment
    glide_hw.append(place(nut(P["m4_nut_af"], P["m4_nut_h"], 4.2), (gx, glide_y_rear + 4.5, gz), (0, -1, 0)))                       # sunk in the pad
add("hardware-drum-glides (bought, 4 x M4 x 8 and 4 x M4 x 10 button head, nuts)", compound(glide_hw), HARDWARE)

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
PM_X0, PM_W, PM_Y = P["pm_x0"], P["pm_w"], ry + e   # the power module plate stands on the cross rails' rear faces (draft 7)
ceil_holes += [(gx, gy, gd) for (gx, gy, gd) in (P["grommet_cord"], P["grommet_harness"])]   # grommets: the cord and the bay harness come up to the power module
plate_xy("bay-ceiling", -hw + tp, hw - tp, P["ceil_y0"], D, bt, P["t_base"], holes=ceil_holes,
         rect_cuts=[(round(P["belt_cross_left"], 1), P["belt_y"], P["belt_slot_w"], P["belt_slot_l"]),    # belt slots, one per run
                    (round(P["belt_cross_right"], 1), P["belt_y"], P["belt_slot_w"], P["belt_slot_l"]),
                    (0, P["rear_bulk_y"] + tb / 2, P["inner_w"] + 2, tb + 1),    # rear bulkhead passes through
                    (-hw + e / 2, D - e / 2, e + 1, e + 1), (hw - e / 2, D - e / 2, e + 1, e + 1),   # rear post notches
                    (0, ry + e + 2 + P["riser_depth"] / 2, P["riser_w"] + 4, P["riser_depth"] + 4),   # riser, 2 mm clearance
                    (PM_X0 + PM_W / 2, PM_Y + tp / 2, PM_W + 2, tp + 2)],   # power module plate passes through (draft 7)
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
base_holes += [(P["cord_x"], P["cord_y"], P["cord_hole_d"])]           # cord strain relief bushing, under the power module (draft 6)
plate_xy("base-pan", -hw + tp, hw - tp, 0, D, -P["t_base"], P["t_base"], holes=base_holes, bolt_side=-1, bolt_skip=tuple(bracket_pts))   # the exhaust leaves through the rear lower panel

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
         circ_cuts=[(P["exhaust_x"], P["exhaust_z"], P["exhaust_d"] + 4)],    # exhaust collar, 2 mm clearance; the cord enters through the base pan
         slots=rear_louvers, bolt_side=+1)

# top panel, full depth; the console box stands on it at the rear
CD, CH = P["console_depth"], P["console_h"]
con_y0 = D - CD                                     # the console face plate's inner surface, the front posts' front faces
assert abs(con_y0 - ry) < 1e-6, "the console's front posts stand over the top rear cross rail"
assert con_y0 + 120.0 <= D, "the UCI-D envelope (120 deep from the panel plane, uci-spec 4.3) must fit in front of the rear plate"
con_z0 = Hb + tp                                    # top of the top panel
con_z1 = con_z0 + CH                                # top of the console frame; the cap sits on it
up_x = [(-hw, -hw + e), (hw - e, hw)]               # the 4040 console posts, inside the cheeks, over the side rails
up_y = [(con_y0, con_y0 + e), (D - e, D)]
cfoot_pts = [(sx * (hw - e - 23.0), yc) for sx in (-1, 1) for yc in (con_y0 + e / 2, D - e / 2)]   # foot bracket bolts through the top panel into the top rear cross rail and the rear top rail, inboard of each post
top_holes = []
for x in pitch_points(-hw + e, hw - e, P["panel_pitch"], 60):
    top_holes.append((x, e / 2, P["m6_hole"]))
    top_holes.append((x, D - e / 2, P["m6_hole"]))
for y in pitch_points(e, D - e, P["panel_pitch"], 60):
    if y < con_y0 - 12:   # not under the console posts; the console's foot bolts clamp the panel there
        top_holes.append((-hw + e / 2, y, P["m6_hole"])); top_holes.append((hw - e / 2, y, P["m6_hole"]))
top_holes += [(fx, fy, P["m6_hole"]) for (fx, fy) in cfoot_pts]
top_holes.append(P["grommet_console"])   # the console harness comes up from the power module through a grommet (draft 7)
plate_xy("top-panel", -hw, hw, 0, D, Hb, tp, holes=top_holes, bolt_side=+1, bolt_skip=tuple(cfoot_pts))   # the console's foot bolts are in its own hardware

# the sub-frame: a small cabinet frame of 4040 like the cabinet's own, four posts the full console height with four
# rails between them at the top, the same M6 hardware and inside corner brackets. The posts stand on the top panel over
# the cabinet's top rear cross rail and rear top rail; their foot brackets bolt through the top panel into those rails'
# top slots with T-nuts, so the console's weight and the push on its knobs go straight into the cabinet frame.
for i, (x0, x1) in enumerate(up_x):
    for j, (y0, y1) in enumerate(up_y):
        extrusion(f"console-post-{2 * i + j + 1}", x0, x1, y0, y1, con_z0, con_z1, "console post")
extrusion("console-rail-front", -hw + e, hw - e, con_y0, con_y0 + e, con_z1 - e, con_z1, "console end rail")
extrusion("console-rail-rear", -hw + e, hw - e, D - e, D, con_z1 - e, con_z1, "console end rail")
extrusion("console-rail-left", -hw, -hw + e, con_y0 + e, D - e, con_z1 - e, con_z1, "console side rail")
extrusion("console-rail-right", hw - e, hw, con_y0 + e, D - e, con_z1 - e, con_z1, "console side rail")
brk_sols, brk_bolts_c = [], []
BRK_L, BRK_T, BRK_W = 35.0, 4.0, 34.0     # catalog 4040 inside corner bracket: legs 35, 4 thick, 34 wide, one hole per leg


def corner_bracket(face, d, c_along, z_corner, up, axis):
    """An inside corner bracket in the corner between a post face and a horizontal surface. `axis` is "x" when the post
    face is an X face at x=face (the bracket extends toward +d from it), "y" when it is a Y face at y=face; c_along is
    the bracket's centre along the face; the horizontal leg lies on the surface at z_corner (up=+1) or under it (-1)."""
    a0, a1 = sorted((face, face + d * BRK_T))
    b0, b1 = sorted((face, face + d * BRK_L))
    za0, za1 = sorted((z_corner, z_corner + up * BRK_L))
    zb0, zb1 = sorted((z_corner, z_corner + up * BRK_T))
    if axis == "x":
        leg_a = box(a0, a1, c_along - BRK_W / 2, c_along + BRK_W / 2, za0, za1)
        leg_b = box(b0, b1, c_along - BRK_W / 2, c_along + BRK_W / 2, zb0, zb1)
        h_a = cq.Workplane("YZ").center(c_along, z_corner + up * (BRK_L - 12.0)).circle(P["m6_hole"] / 2).extrude(BRK_T + 2).translate((a0 - 1, 0, 0))
        h_b = cq.Workplane("XY").center(face + d * (BRK_L - 12.0), c_along).circle(P["m6_hole"] / 2).extrude(BRK_T + 2).translate((0, 0, zb0 - 1))
    else:
        leg_a = box(c_along - BRK_W / 2, c_along + BRK_W / 2, a0, a1, za0, za1)
        leg_b = box(c_along - BRK_W / 2, c_along + BRK_W / 2, b0, b1, zb0, zb1)
        h_a = cq.Workplane("XZ").center(c_along, z_corner + up * (BRK_L - 12.0)).circle(P["m6_hole"] / 2).extrude(-(BRK_T + 2)).translate((0, a0 - 1, 0))
        h_b = cq.Workplane("XY").center(c_along, face + d * (BRK_L - 12.0)).circle(P["m6_hole"] / 2).extrude(BRK_T + 2).translate((0, 0, zb0 - 1))
    return leg_a.union(leg_b).cut(h_a).cut(h_b)


def corner_bracket_v(x_face, dx, y_face, dy, zc):
    """An inside corner bracket between two vertical faces meeting at (x_face, y_face): one leg on the plane x = x_face
    with its thickness toward dx, the other on the plane y = y_face with its thickness toward dy; each leg runs from
    the corner along the other face. zc is the bracket's centre height. Holes for its two M6 bolts."""
    leg_a = box(*sorted((x_face, x_face + dx * BRK_T)), *sorted((y_face, y_face + dy * BRK_L)), zc - BRK_W / 2, zc + BRK_W / 2)
    leg_b = box(*sorted((x_face, x_face + dx * BRK_L)), *sorted((y_face, y_face + dy * BRK_T)), zc - BRK_W / 2, zc + BRK_W / 2)
    h_a = cq.Workplane("YZ").center(y_face + dy * (BRK_L - 12.0), zc).circle(P["m6_hole"] / 2).extrude(BRK_T + 2).translate((min(x_face, x_face + dx * BRK_T) - 1, 0, 0))
    h_b = cq.Workplane("XZ").center(x_face + dx * (BRK_L - 12.0), zc).circle(P["m6_hole"] / 2).extrude(-(BRK_T + 2)).translate((0, min(y_face, y_face + dy * BRK_T) - 1, 0))
    return leg_a.union(leg_b).cut(h_a).cut(h_b)


for sx in (-1, 1):
    xi = sx * (hw - e)                     # the post's inner face; brackets extend inboard (toward -sx)
    for (yy0, yy1) in up_y:
        yc = (yy0 + yy1) / 2
        # foot: against the post's inner face, on the top panel
        brk_sols.append(corner_bracket(xi, -sx, yc, con_z0, +1, "x"))
        brk_bolts_c.append(place(hex_bolt_m6(), (xi - sx * (BRK_L - 12.0), yc, con_z0 + BRK_T), (0, 0, 1)))            # down through the top panel into the cabinet rail's top slot
        brk_bolts_c.append(place(hex_bolt_m6(), (xi - sx * BRK_T, yc, con_z0 + BRK_L - 12.0), (-sx, 0, 0)))              # into the post's inner slot
        # the end rail: against the post's inner face, under the rail
        zt = con_z1 - e
        brk_sols.append(corner_bracket(xi, -sx, yc, zt, -1, "x"))
        brk_bolts_c.append(place(hex_bolt_m6(), (xi - sx * (BRK_L - 12.0), yc, zt - BRK_T), (0, 0, -1)))                # up into the rail's bottom slot
        brk_bolts_c.append(place(hex_bolt_m6(), (xi - sx * BRK_T, yc, zt - BRK_L + 12.0), (-sx, 0, 0)))                 # into the post's inner slot
    # the side rail, short (between the posts): at its front end a bracket against the front post's rear face, under
    # the rail; at its rear end a bracket inside the frame between the rail's inner face and the rear end rail's front
    # face (two brackets under one short rail would overlap)
    yf, xc = con_y0 + e, sx * (hw - e / 2)
    brk_sols.append(corner_bracket(yf, +1, xc, zt, -1, "y"))
    brk_bolts_c.append(place(hex_bolt_m6(), (xc, yf + (BRK_L - 12.0), zt - BRK_T), (0, 0, -1)))                          # up into the side rail's bottom slot
    brk_bolts_c.append(place(hex_bolt_m6(), (xc, yf + BRK_T, zt - BRK_L + 12.0), (0, 1, 0)))                             # into the front post's rear slot
    zc = con_z1 - e / 2
    brk_sols.append(corner_bracket_v(xi, -sx, D - e, -1, zc))
    brk_bolts_c.append(place(hex_bolt_m6(), (xi - sx * BRK_T, D - e - (BRK_L - 12.0), zc), (-sx, 0, 0)))                 # into the side rail's inner slot
    brk_bolts_c.append(place(hex_bolt_m6(), (xi - sx * (BRK_L - 12.0), D - e - BRK_T, zc), (0, -1, 0)))                 # into the rear end rail's front slot
add("console-brackets (bought, 12 x 4040 inside corner brackets)", compound(brk_sols), HARDWARE)
add("hardware-console-brackets (bought, 24 x M6 x 12 hex, washers, T-nuts)", compound(brk_bolts_c), HARDWARE)

# the console plates: face (vertical, carries the UCI-D aperture), cap, two cheeks continuing the side panels, rear
CONSOLE_C = (0.0, con_y0, con_z0 + P["uci_ap_z_off"])   # aperture centre on the face plate's inner surface, on the posts' front faces
N_FACE = (0.0, -1.0, 0.0)                           # outward normal of the face
S_FACE = (0.0, 0.0, 1.0)                            # up the face
AP_Z = CONSOLE_C[2]
uci_pts = [(sx * P["uci_hole_x"] / 2, sy * P["uci_hole_y"] / 2) for sx in (-1, 1) for sy in (-1, 1)] + [(0.0, sy * P["uci_hole_y"] / 2) for sy in (-1, 1)]
post_bolt_z = (con_z0 + 28.5, con_z1 - e - 28.5)     # two bolts per post, clear of the brackets' legs (35)
rail_bolt_x = pitch_points(-hw + e, hw - e, P["panel_pitch"], 60)
face_holes = [(sx * (hw - e / 2), z, P["m6_hole"]) for sx in (-1, 1) for z in post_bolt_z] + [(x, con_z1 - e / 2, P["m6_hole"]) for x in rail_bolt_x]
face_holes += [(ux, AP_Z + uy, P["uci_hole_d"]) for (ux, uy) in uci_pts]
plate_xz("console-face", -hw, hw, con_z0, con_z1, con_y0 - tp, tp, holes=face_holes, rect_cuts=[(0, AP_Z, P["uci_ap_w"], P["uci_ap_h"])], bolt_side=-1)
rear_holes = [(sx * (hw - e / 2), z, P["m6_hole"]) for sx in (-1, 1) for z in post_bolt_z] + [(x, con_z1 - e / 2, P["m6_hole"]) for x in rail_bolt_x]
plate_xz("console-rear", -hw, hw, Hb, con_z1, D, tp, holes=rear_holes, bolt_side=+1)   # from the top panel's rear edge up
cap_holes = [(x, con_y0 + e / 2, P["m6_hole"]) for x in rail_bolt_x] + [(x, D - e / 2, P["m6_hole"]) for x in rail_bolt_x]
cap_holes += [(sx * (hw - e / 2), (con_y0 + e + D - e) / 2, P["m6_hole"]) for sx in (-1, 1)]
plate_xy("console-cap", -hw - tp, hw + tp, con_y0 - tp, D + tp, con_z1, tp, holes=cap_holes, bolt_side=+1)
for side, x0, bs in (("left", -hw - tp, -1), ("right", hw, +1)):
    ch_holes = [(yc, z, P["m6_hole"]) for yc in (con_y0 + e / 2, D - e / 2) for z in post_bolt_z] + [((con_y0 + e + D - e) / 2, con_z1 - e / 2, P["m6_hole"])]
    plate_yz(f"console-cheek-{side}", con_y0 - tp, D + tp, Hb, con_z1, x0, tp, holes=ch_holes, bolt_side=bs)


def on_face(solid):
    """A solid built in the console face's local frame (x across, y up, z outward from the inner surface) to the world."""
    return solid.rotate((0, 0, 0), (1, 0, 0), 90).translate(CONSOLE_C)


def face_point(u, v, w):
    return (u, CONSOLE_C[1] + v * S_FACE[1] + w * N_FACE[1], CONSOLE_C[2] + v * S_FACE[2] + w * N_FACE[2])


# ---------------------------------------------------------------------------
# Tier 0 control module on the console face (controls/tier0-mechanical, drawing numbers in tier0_drawings.py)
# ---------------------------------------------------------------------------
FP_T = P["fp_t"]
assert (T0.FP_W, T0.FP_H, T0.FP_R) == (P["fp_w"], P["fp_h"], P["fp_r"]), "faceplate outline: model and drawing"
assert sorted(T0.MOUNT) == sorted((x, y) for (x, y) in uci_pts), "UCI-D mounting pattern: model and drawing"
TIMERS = {"dry-time": T0.TIMERS["DRY TIME"], "heat-time": T0.TIMERS["HEAT TIME"]}
SEL_X, START_X, DEV_Y = T0.SEL_X, T0.START_X, T0.DEV_Y
fp_holes = [(x, y, d) for (x, y, d, _) in T0.holes()]
fp = fillet_corners(cq.Workplane("XY").rect(P["fp_w"], P["fp_h"]).extrude(FP_T), "|Z", P["fp_r"])
for (x, y, d) in fp_holes:
    fp = fp.cut(cq.Workplane("XY").center(x, y).circle(d / 2).extrude(FP_T + 2).translate((0, 0, -1)))
for text, x, y in T0.LABELS:
    fp = fp.faces(">Z").workplane(origin=(0, 0, FP_T)).center(x, y).text(text, 5, -0.3, combine="cut", halign="center", valign="center")
fp_z0 = tp                      # the faceplate sits on the console face's outer surface
add("tier0-faceplate", on_face(fp.translate((0, 0, fp_z0))), ALU, plate=True, t=FP_T)
# no DXF from here: mechanical/drawings/tier0_drawings.py writes tier0-faceplate.dxf (with its label and reference layers)
# from the same numbers, and the audit matches this part's section against that file
# four M4 button heads hold the faceplate to the console face, nuts inside the console
fp_bolts = [place(button_bolt(4.0, P["m4_head_d"], P["m4_head_h"], 10.0, 2.5), face_point(ux, uy, fp_z0 + FP_T), N_FACE) for (ux, uy) in uci_pts]
fp_nuts = [place(nut(P["m4_nut_af"], P["m4_nut_h"], 4.2), face_point(ux, uy, 0.0), tuple(-c for c in N_FACE)) for (ux, uy) in uci_pts]
add(f"hardware-tier0-faceplate (bought, {len(uci_pts)} x M4 x 10 button head, nuts)", compound(fp_bolts + fp_nuts), HARDWARE)

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
    bezel = cq.Workplane("XY").center(x, DEV_Y).circle(15.0).circle(11.15).extrude(2.5).translate((0, 0, fp_top))
    body = cq.Workplane("XY").center(x, DEV_Y).circle(11.0).extrude(fp_top + 45).translate((0, 0, -45))
    block = box(x - 12.5, x + 12.5, DEV_Y - 17.5, DEV_Y + 17.5, -45, -15)
    base = bezel.union(body).union(block)
    return base, cap(x)


def selector_cap(x):
    hub = cq.Workplane("XY").center(x, DEV_Y).circle(11.0).extrude(4.0)
    lever = cq.Workplane("XY").center(x, DEV_Y).slot2D(30.0, 8.0, angle=90).extrude(6.0).translate((0, 0, 4.0))
    return hub.union(lever).translate((0, 0, fp_top + 2.5))


def start_cap(x):
    return cq.Workplane("XY").center(x, DEV_Y).circle(11.0).extrude(8.0).edges(">Z").fillet(2.0).translate((0, 0, fp_top + 2.5))


base, cap = device22(SEL_X, selector_cap)
add("tier0-selector-body (bought)", on_face(base), BOUGHT)
add("tier0-selector (bought)", on_face(cap), RUBBER)
base, cap = device22(START_X, start_cap)
add("tier0-start-body (bought)", on_face(base), BOUGHT)
add("tier0-start-button (bought)", on_face(cap), cq.Color(0.1, 0.6, 0.2))
# K1 on 100 mm of DIN rail on two 12 mm standoffs behind the plate; the socket and relay stack away from the plate.
# The rail's standoffs sit at T0.RAIL; the socket hangs 36 below their line and 19 above it, inside the aperture's
# projection (uci-spec 4.3), which is why the 22 mm devices sit above the centre line (T0.DEV_Y)
(rx0, ry_), (rx1, _) = T0.RAIL
rail = box(rx0 - 10, rx1 + 10, ry_ - 17.5, ry_ + 17.5, fp_z0 - 12 - 7.5, fp_z0 - 12)
standoffs = [cq.Workplane("XY").center(x, ry_).circle(4.0).extrude(12).translate((0, 0, fp_z0 - 12)) for x in (rx0, rx1)]
relay = box(rx0 - 9, rx0 + 19, ry_ - 36, ry_ + 19, fp_z0 - 12 - 7.5 - 65, fp_z0 - 12 - 7.5)
assert ry_ - 36 >= -P["uci_ap_h"] / 2 and ry_ + 19 <= DEV_Y - 17.5 - 2, "K1 inside the aperture's projection and clear of the 22 mm devices' blocks"
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
ring_hw = [place(button_bolt(4.0, P["m4_head_d"], P["m4_head_h"], 8.0, 2.5), (x, ring_y0, z), (0, -1, 0)) for (x, z) in ring_bolt_pts]
ring_hw += [place(nut(P["m4_nut_af"], P["m4_nut_h"], 4.2), (x, 0.0, z), (0, 1, 0)) for (x, z) in ring_bolt_pts]
add("hardware-door-ring (bought, 8 x M4 x 8 button head, nuts)", compound(ring_hw), HARDWARE)

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
riser_y0 = ry + e + 2
riser = box(-P["riser_w"] / 2, P["riser_w"] / 2, riser_y0, riser_y0 + P["riser_depth"], P["riser_z0"], riser_top)
# the hood: from over the heat module's outlet, under the mid rear cross rail, into the riser (draft 6; the module slides out under it)
hood_z1 = P["riser_z0"] + P["hood_h"]
riser = riser.union(box(-P["hood_w"] / 2, P["hood_w"] / 2, P["hood_y0"], riser_y0 + P["riser_depth"], P["riser_z0"], hood_z1))
add("riser-duct", riser, DUCT)
assert riser_y0 + P["riser_depth"] + 2 <= D - e, "riser must clear the rear end rail"
assert hood_z1 + 2 <= bt - e, "hood must pass under the mid rear cross rail"
P["hood_area"] = P["hood_h"] * P["hood_w"]
# the hood's gasket (draft 7): a foam ring glued under the hood round the collar's hole; the module's collar rim brushes it
gk = (cq.Workplane("XY").center(0, P["hm_collar_y"]).circle(P["hood_gasket_od"] / 2).circle(P["hm_collar_d"] / 2).extrude(P["hood_gasket_t"])
      .translate((0, 0, P["riser_z0"] - P["hood_gasket_t"])))
add("hood-gasket (bought, 3 mm foam ring 150 x 125, glued under the hood)", gk, FELT)
assert P["hood_y0"] <= P["hm_collar_y"] - P["hood_gasket_od"] / 2, "the hood must cover the gasket ring"
add("lint-duct", box(-168, 168, P["lint_duct_y0"], P["lint_duct_y0"] + P["lint_duct_depth"], 150, P["lint_duct_top"]), DUCT)   # 2 mm from each front stub, behind the ring bolts' nuts
add("lint-duct-transition", box(-110, 110, P["lint_duct_y0"] + P["lint_duct_depth"], P["blower_y0"], 50, 190), DUCT)

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
msr = P["motor_shaft_d"] / 2
motor = motor.union(cq.Workplane("XZ").center(0, mz).circle(msr).extrude(-(my0 - (P["blower_y0"] + P["blower_w"]))).translate((0, P["blower_y0"] + P["blower_w"], 0)))   # front shaft to the blower
motor = motor.union(cq.Workplane("XZ").center(0, mz).circle(msr).extrude(-4).translate((0, my0 + ml, 0)))          # rear shaft to the pulley
motor = motor.union(box(-25, 25, my0 + 70, my0 + 130, mz + md / 2 - 5, mz + md / 2 + 20))                          # terminal box
add("motor (bought)", motor, BOUGHT)
for i, yy in enumerate((my0 + 25, my0 + ml - 55)):   # two cradle mounts from the motor mount kit, bolted to the base pan
    cradle = box(-35, 35, yy, yy + 30, 0, mz - 20).cut(cq.Workplane("XZ").center(0, mz).circle(md / 2 + 0.5).extrude(-40).translate((0, yy - 5, 0)))
    add(f"motor-mount-{i+1} (bought, cradle)", cradle, BOUGHT)
pulley = cq.Workplane("XZ").center(0, mz).circle(P["motor_pulley_d"] / 2).extrude(-16).translate((0, P["belt_y"] - 8, 0))
for k in range(4):   # four grooves between the five ribs
    gy = P["belt_y"] - 4.5 + 3.0 * k
    pulley = pulley.cut(cq.Workplane("XZ").center(0, mz).circle(P["motor_pulley_d"] / 2 + 1).circle(P["motor_pulley_d"] / 2 - 1.2).extrude(-1.2).translate((0, gy - 0.6, 0)))
pulley = pulley.union(cq.Workplane("XZ").center(0, mz).circle(P["motor_pulley_d"] / 2 + 1.0).extrude(-6).translate((0, P["belt_y"] + 8, 0)))   # hub with the set screw
add("pulley (bought)", pulley, BOUGHT)
P["drum_rpm"] = 1725.0 * P["motor_pulley_d"] / P["drum_d"]
assert 45.0 <= P["drum_rpm"] <= 57.0, f"drum speed {P['drum_rpm']:.1f} rpm is outside the 45 to 55 target (pulley {P['motor_pulley_d']})"
blower = cq.Workplane("XZ").center(0, mz).circle(P["blower_d"] / 2).extrude(-P["blower_w"]).translate((0, P["blower_y0"], 0))
blower = blower.cut(cq.Workplane("XZ").center(0, mz).circle(65.0).extrude(-8).translate((0, P["blower_y0"], 0)))     # inlet mouth, facing the transition
blower = blower.union(box(100, 270, P["blower_y0"] + 26, my0, mz - 10, mz + 70))                                     # tangential outlet turning into the exhaust duct
add("blower (bought)", blower, BOUGHT)
P["exhaust_y0"] = my0
exh = (cq.Workplane("XZ").center(P["exhaust_x"], P["exhaust_z"]).circle(P["exhaust_d"] / 2).extrude(-(D - P["exhaust_y0"]))
       .translate((0, P["exhaust_y0"], 0)))
add("exhaust-duct (bought)", exh, DUCT)

# ---------------------------------------------------------------------------
# Electric heat module (draft 7): a laser-cut duct box on the tray, joined with 20x20x2 aluminium angle and M4 button
# heads with nuts (no brake, no rivets), the element on two angle rails inside, a round catalog collar on top under the
# riser's hood, the contactor and the terminal strips on a DIN rail on a plate behind the box. Everything here slides
# out the back with the tray. Part names start with "heat-module" so the motion check moves them together.
# ---------------------------------------------------------------------------
m4b8 = button_bolt(4.0, P["m4_head_d"], P["m4_head_h"], 8.0, 2.5)
m4n_ = nut(P["m4_nut_af"], P["m4_nut_h"], 4.2)
A_L, A_T = 20.0, 2.0                                       # 20 x 20 x 2 aluminium angle
tz1 = e + es + P["t_tray"]                                 # tray top face (61.5)
ty0, ty1 = P["tray_y0"], P["tray_y0"] + P["tray_depth"]
bx, by0, by1, td = P["hm_box_x"], P["hm_box_y0"], P["hm_box_y1"], P["t_duct"]
bz1 = tz1 + P["hm_box_h"]                                  # top face of the box's top plate
wz1 = bz1 - td                                             # walls end under the top plate
HM_BY = (470.0, 580.0)                                     # bolt rows along the side walls (Y)
HM_BX = (-100.0, 0.0, 100.0)                               # bolt columns along the end walls (X)
Z_BOT, Z_TOP, Z_CNR = tz1 + 10.0, wz1 - 6.5, (tz1 + A_L + wz1 + A_T - A_L) / 2   # bolt heights on the bottom angles' legs, the top angles' legs, the corner angles
hm_hw, hm_nuts = [], []


def angle_x(x0, x1, y_v, sy, z_v, sz):
    """A 20x20x2 angle along X from x0 to x1: vertical leg from y_v growing toward sy (+1/-1), from z_v growing toward sz;
    horizontal leg at the vertical leg's end z_v, growing from y_v toward sy. Returns the solid (holes cut by the caller)."""
    leg_v = box(x0, x1, min(y_v, y_v + sy * A_T), max(y_v, y_v + sy * A_T), min(z_v, z_v + sz * A_L), max(z_v, z_v + sz * A_L))
    leg_h = box(x0, x1, min(y_v, y_v + sy * A_L), max(y_v, y_v + sy * A_L), min(z_v, z_v + sz * A_T), max(z_v, z_v + sz * A_T))
    return leg_v.union(leg_h)


def angle_y(y0, y1, x_v, sx, z_v, sz):
    leg_v = box(min(x_v, x_v + sx * A_T), max(x_v, x_v + sx * A_T), y0, y1, min(z_v, z_v + sz * A_L), max(z_v, z_v + sz * A_L))
    leg_h = box(min(x_v, x_v + sx * A_L), max(x_v, x_v + sx * A_L), y0, y1, min(z_v, z_v + sz * A_T), max(z_v, z_v + sz * A_T))
    return leg_v.union(leg_h)


def angle_z(z0, z1, x_v, sx, y_v, sy):
    """A vertical corner angle: one leg in the plane x = x_v growing toward sx, the other in y = y_v growing toward sy."""
    leg_x = box(min(x_v, x_v + sx * A_T), max(x_v, x_v + sx * A_T), min(y_v, y_v + sy * A_L), max(y_v, y_v + sy * A_L), z0, z1)
    leg_y = box(min(x_v, x_v + sx * A_L), max(x_v, x_v + sx * A_L), min(y_v, y_v + sy * A_T), max(y_v, y_v + sy * A_T), z0, z1)
    return leg_x.union(leg_y)


def hole_x(solid, y, z):
    return solid.cut(cq.Workplane("YZ").center(y, z).circle(2.25).extrude(2000).translate((-1000, 0, 0)))


def hole_y(solid, x, z):
    return solid.cut(cq.Workplane("XZ").center(x, z).circle(2.25).extrude(-2000).translate((0, -500, 0)))


def hole_z(solid, x, y):
    return solid.cut(cq.Workplane("XY").center(x, y).circle(2.25).extrude(3000).translate((0, 0, -500)))


def joint(p_head, n, p_nut=None, length=8.0):
    """An M4 button head with its head on the surface point p_head (outward normal n) and, if given, a nut with its base on p_nut facing -n."""
    hm_hw.append(place(button_bolt(4.0, P["m4_head_d"], P["m4_head_h"], length, 2.5), p_head, n))
    if p_nut is not None:
        hm_nuts.append(place(m4n_, p_nut, tuple(-c for c in n)))


# the tray: on the two 2020 rails, bonded with an M6 stud at the rear right
tray_holes = [(sx * 160.0, yy, P["m4_hole"]) for sx in (-1, 1) for yy in HM_BY]                  # side angles and tray to the rails' top slots (T-nuts)
tray_holes += [(x, by0 + td + A_L / 2, P["m4_hole"]) for x in HM_BX]                              # front inside angle
tray_holes += [(x, by1 - td - A_L / 2, P["m4_hole"]) for x in HM_BX]                              # rear inside angle
tray_holes += [(x, P["hm_plate_y"] + 1.5 + A_L / 2, P["m4_hole"]) for x in HM_BX]                 # terminal plate angle
tray_holes += [(140.0, 680.0, 6.6)]                                                                # bonding stud
plate_xy("heat-module-tray", P["tray_x0"], P["tray_x0"] + P["tray_w"], ty0, ty1, e + es, P["t_tray"], holes=tray_holes)
assert ty0 >= (P["belt_y"] + BW / 2 + 1.0 + 4.0) + 4.0 + 3.0, "the tray starts at least 3 behind the idler spring (its centre line is set with the idler below)"
assert by0 >= ty0 + 2.0 and by1 + 2.0 <= ty1, "the box sits on the tray"
# the box walls (1.5 mm, same stock as the panels): side walls full length outside the end walls; holes for the angles
side_holes_hm = [(yy, Z_BOT, P["m4_hole"]) for yy in HM_BY] + [(yy, Z_TOP, P["m4_hole"]) for yy in HM_BY] + [(yy, Z_CNR, P["m4_hole"]) for yy in (by0 + A_L / 2, by1 - A_L / 2)]
iy, iz = P["hm_inlet_y"], P["hm_inlet_z"]
plate_yz("heat-module-wall-left", by0, by1, tz1, wz1, -bx, td, holes=side_holes_hm,
         rect_cuts=[((iy[0] + iy[1]) / 2, (iz[0] + iz[1]) / 2, iy[1] - iy[0], iz[1] - iz[0])], r=P["small_corner_r"])
tc = P["hm_term_cut"]
plate_yz("heat-module-wall-right", by0, by1, tz1, wz1, bx - td, td, holes=side_holes_hm, rect_cuts=[tc], r=P["small_corner_r"])
end_holes_hm = [(x, Z_BOT, P["m4_hole"]) for x in HM_BX] + [(x, Z_TOP, P["m4_hole"]) for x in HM_BX] + [(sx * (bx - A_L / 2), Z_CNR, P["m4_hole"]) for sx in (-1, 1)]
plate_xz("heat-module-wall-front", -bx + td, bx - td, tz1, wz1, by0, td, holes=end_holes_hm, r=P["small_corner_r"])
plate_xz("heat-module-wall-rear", -bx + td, bx - td, tz1, wz1, by1 - td, td, holes=end_holes_hm, r=P["small_corner_r"])
# the top plate: lid, held by the top angles' legs; the collar's hole and flange holes; the thermostats' holes
cy, cd_ = P["hm_collar_y"], P["hm_collar_d"]
top_holes_hm = [(sx * (bx - A_L / 2), yy, P["m4_hole"]) for sx in (-1, 1) for yy in HM_BY]
top_holes_hm += [(x, yy, P["m4_hole"]) for x in HM_BX for yy in (by0 + A_L / 2, by1 - A_L / 2)]
top_holes_hm += [(cx_, cy_, P["m4_hole"]) for (cx_, cy_) in ((70.0, cy), (-70.0, cy), (0.0, cy + 70.0), (0.0, cy - 70.0))]
tx_, ty_ = P["hm_thermostat_x"], P["hm_thermostat_y"]
top_holes_hm += [(sx * tx_, ty_ + k, P["m4_hole"]) for sx in (-1, 1) for k in (-20.0, 20.0)]
plate_xy("heat-module-top", -bx, bx, by0, by1, wz1, td, holes=top_holes_hm, circ_cuts=[(0, cy, cd_ + 1.0)], r=P["small_corner_r"])

# the angles. Bottom: outside on the side walls (their legs on the tray, bolted into the tray rails' top slots, which also
# holds the tray), inside on the end walls (legs on the tray, nuts under it). Top: outside, legs on the lid. Corners:
# outside, between the bottom and top angles' legs. Element rails: inside the side walls, top leg under the element.
ang_bottom, ang_top, ang_corner, ang_rails = [], [], [], []
for sx in (-1, 1):
    xo = sx * bx                                                    # the side wall's outer face
    a = angle_y(by0, by1, xo, sx, tz1, +1)                          # outside bottom angle
    for yy in HM_BY:
        a = hole_x(a, yy, Z_BOT); a = hole_z(a, sx * 160.0, yy)
        joint((xo + sx * A_T, yy, Z_BOT), (sx, 0, 0), (xo - sx * (td + A_T), yy, Z_BOT))   # through the wall into the element rail's leg
        joint((sx * 160.0, yy, tz1 + A_T), (0, 0, 1))                                        # into the tray rail's top slot (T-nut)
    ang_bottom.append(a)
    a = angle_y(by0 + A_L, by1 - A_L, xo + sx * A_T, -sx, bz1 + A_T, -1)   # outside top angle from its outer top corner, between the end walls' top angles
    for yy in HM_BY:
        a = hole_x(a, yy, Z_TOP); a = hole_z(a, sx * (bx - A_L / 2), yy)
        joint((xo + sx * A_T, yy, Z_TOP), (sx, 0, 0), (xo - sx * td, yy, Z_TOP))
        joint((sx * (bx - A_L / 2), yy, bz1 + A_T), (0, 0, 1), (sx * (bx - A_L / 2), yy, wz1))
    ang_top.append(a)
    r_ = angle_y(by0 + td + A_T, by1 - td - A_T, xo - sx * td, -sx, tz1 + A_L, -1)   # element rail: vertical leg on the wall's inside, top leg inward, between the inside bottom angles
    for yy in HM_BY:
        r_ = hole_x(r_, yy, Z_BOT)
    ang_rails.append(r_)
    for (yo, sy) in ((by0, -1), (by1, +1)):                         # corner angles
        a = angle_z(tz1 + A_L, bz1 + A_T - A_L, xo + sx * A_T, -sx, yo + sy * A_T, -sy)   # from its outer corner, legs inward along both walls
        a = hole_x(a, yo - sy * A_L / 2, Z_CNR); a = hole_y(a, sx * (bx - A_L / 2), Z_CNR)
        joint((xo + sx * A_T, yo - sy * A_L / 2, Z_CNR), (sx, 0, 0), (xo - sx * td, yo - sy * A_L / 2, Z_CNR))
        joint((sx * (bx - A_L / 2), yo + sy * A_T, Z_CNR), (0, sy, 0), (sx * (bx - A_L / 2), yo - sy * td, Z_CNR))
        ang_corner.append(a)
for (yo, sy) in ((by0, -1), (by1, +1)):
    a = angle_x(-bx + td + A_T, bx - td - A_T, yo - sy * td, -sy, tz1, +1)   # inside bottom angle, between the element rails' legs
    for x in HM_BX:
        a = hole_y(a, x, Z_BOT); a = hole_z(a, x, yo - sy * (td + A_L / 2))
        joint((x, yo, Z_BOT), (0, sy, 0), (x, yo - sy * (td + A_T), Z_BOT))
        joint((x, yo - sy * (td + A_L / 2), tz1 + A_T), (0, 0, 1), (x, yo - sy * (td + A_L / 2), e + es))
    ang_bottom.append(a)
    a = angle_x(-bx, bx, yo + sy * A_T, -sy, bz1 + A_T, -1)         # outside top angle on the end wall, from its outer top corner
    for x in HM_BX:
        a = hole_y(a, x, Z_TOP); a = hole_z(a, x, yo - sy * A_L / 2)
        joint((x, yo + sy * A_T, Z_TOP), (0, sy, 0), (x, yo - sy * td, Z_TOP))
        joint((x, yo - sy * A_L / 2, bz1 + A_T), (0, 0, 1), (x, yo - sy * A_L / 2, wz1))
    ang_top.append(a)
add("heat-module-angles-bottom (20x20x2 aluminium angle, 2 x 205 outside, 2 x 283 inside)", compound(ang_bottom), ALU)
add("heat-module-angles-top (20x20x2 aluminium angle, 2 x 165, 2 x 290)", compound(ang_top), ALU)
add("heat-module-angles-corner (20x20x2 aluminium angle, 4 x 72)", compound(ang_corner), ALU)
add("heat-module-element-rails (20x20x2 aluminium angle, 2 x 198)", compound(ang_rails), ALU)
cut_list.append(("heat-module angles", "angle 20x20x2 aluminum", 205, 2, "box bottom, outside the side walls"))
cut_list.append(("heat-module angles", "angle 20x20x2 aluminum", round(2 * (bx - td - A_T), 1), 2, "box bottom, inside the end walls"))
cut_list.append(("heat-module angles", "angle 20x20x2 aluminum", round(by1 - by0 - 2 * A_L, 1), 2, "lid, side walls"))
cut_list.append(("heat-module angles", "angle 20x20x2 aluminum", round(2 * bx, 1), 2, "lid, end walls"))
cut_list.append(("heat-module angles", "angle 20x20x2 aluminum", round(bz1 + A_T - A_L - (tz1 + A_L), 1), 4, "box corners"))
cut_list.append(("heat-module angles", "angle 20x20x2 aluminum", round(by1 - by0 - 2 * (td + A_T), 1), 2, "element rails, inside the side walls"))
cut_list.append(("heat-module angles", "angle 20x20x2 aluminum", round(2 * bx, 1), 1, "terminal plate foot"))

# the element: a catalog open-coil element on its frame, lying along X on the rails' top legs; terminals out the right end
el, ew, eh, ez0 = P["hm_elem_l"], P["hm_elem_w"], P["hm_elem_h"], P["hm_elem_z0"]
ey0 = (by0 + by1) / 2 - ew / 2
elem = box(-el / 2, el / 2, ey0, ey0 + ew, ez0, ez0 + eh)
elem = elem.union(box(el / 2, bx + 12.0, tc[0] - 10.0, tc[0] + 10.0, tc[1] - 6.0, tc[1] + 6.0))   # the two terminals, through the right wall's opening
add("heat-module-element (bought, 279838 class open-coil element on its frame, envelope)", elem, BOUGHT)
assert ez0 >= tz1 + A_L - A_T - 1e-6 and ez0 + eh <= wz1 - P["m4_nut_h"] - 2, "the element must sit on the rails under the lid's nuts"
assert -el / 2 >= -bx + td + A_T + 2 and ey0 >= by0 + td + A_T and ey0 + ew <= by1 - td - A_T, "the element must fit inside the box"
# the collar: a 125 flanged starting collar on the lid, its rim 3 under the hood's gasket; four M4 through the flange
ch0 = bz1
collar = cq.Workplane("XY").center(0, cy).circle(cd_ / 2).circle(cd_ / 2 - 0.6).extrude(P["hm_collar_top"] - ch0).translate((0, 0, ch0))
collar = collar.union(cq.Workplane("XY").center(0, cy).circle(P["hm_collar_flange_d"] / 2).circle(cd_ / 2 - 0.6).extrude(1.0).translate((0, 0, ch0)))
for (cx_, cy_) in ((70.0, cy), (-70.0, cy), (0.0, cy + 70.0), (0.0, cy - 70.0)):
    collar = collar.cut(cq.Workplane("XY").center(cx_, cy_).circle(2.25).extrude(4).translate((0, 0, ch0 - 1)))
    joint((cx_, cy_, ch0 + 1.0), (0, 0, 1), (cx_, cy_, wz1))
add("heat-module-collar (bought, 125 flanged starting collar, cut to 55.5)", collar, DUCT)
assert P["hm_collar_top"] + 3.0 <= P["riser_z0"], "the collar must stop 3 under the hood"
P["hm_collar_area"] = math.pi * (cd_ / 2) ** 2
P["hm_inlet_area"] = (iy[1] - iy[0]) * (iz[1] - iz[0])
# the thermostats: high-limit and thermal cut-off from the 279816 class kit, on brackets on the lid beside the collar
thermos = []
for sx in (-1, 1):
    brk_t = box(sx * tx_ - 7.0, sx * tx_ + 7.0, ty_ - 27.0, ty_ + 27.0, bz1, bz1 + 2.0)      # mounting bracket, holes 40 apart
    body = box(sx * tx_ - 11.0, sx * tx_ + 11.0, ty_ - 11.0, ty_ + 11.0, bz1 + 2.0, bz1 + 15.0)   # the disc thermostat's body
    t_ = brk_t.union(body)
    for k in (-20.0, 20.0):
        t_ = t_.cut(cq.Workplane("XY").center(sx * tx_, ty_ + k).circle(2.25).extrude(5).translate((0, 0, bz1 - 1)))
        joint((sx * tx_, ty_ + k, bz1 + 2.0), (0, 0, 1), (sx * tx_, ty_ + k, wz1))
    thermos.append(t_)
assert tx_ - 11.0 >= P["hm_collar_flange_d"] / 2 + 3.0 and tx_ + 11.0 <= bx - A_L - 2.0, "thermostats between the collar's flange and the lid's side angles"
add("heat-module-thermostats (bought, 279816 class high-limit and thermal cut-off, envelopes)", compound(thermos), BOUGHT)
# the terminal plate behind the box: 1.5 mm, 100 tall, on an angle foot bolted to the tray; DIN rail on its rear face
py_, ph_ = P["hm_plate_y"], P["hm_plate_h"]
RAIL_ZC = tz1 + ph_ / 2
plate_holes_hm = [(x, Z_BOT, P["m4_hole"]) for x in (-120.0, 0.0, 120.0)] + [(x, RAIL_ZC, P["m4_hole"]) for x in (-120.0, 120.0)]
plate_xz("heat-module-terminal-plate", -bx, bx, tz1, tz1 + ph_, py_, 1.5, holes=plate_holes_hm, r=P["small_corner_r"])
a = angle_x(-bx, bx, py_ + 1.5, +1, tz1, +1)
for x in (-120.0, 0.0, 120.0):
    a = hole_y(a, x, Z_BOT)
    joint((x, py_, Z_BOT), (0, -1, 0), (x, py_ + 1.5 + A_T, Z_BOT))
for x in HM_BX:
    a = hole_z(a, x, py_ + 1.5 + A_L / 2)
    joint((x, py_ + 1.5 + A_L / 2, tz1 + A_T), (0, 0, 1), (x, py_ + 1.5 + A_L / 2, e + es))
add("heat-module-terminal-angle (20x20x2 aluminium angle, 290)", a, ALU)


def din_rail(x0, x1, y_face, zc):
    """A 35 x 7.5 top-hat DIN rail along X with its web on a vertical plate's face at y_face; the devices clip on at y_face + 7.5."""
    web = box(x0, x1, y_face, y_face + 1.0, zc - 12.5, zc + 12.5)
    sides = box(x0, x1, y_face, y_face + 7.5, zc - 13.5, zc - 12.5).union(box(x0, x1, y_face, y_face + 7.5, zc + 12.5, zc + 13.5))
    brims = box(x0, x1, y_face + 6.5, y_face + 7.5, zc - 17.5, zc - 13.5).union(box(x0, x1, y_face + 6.5, y_face + 7.5, zc + 13.5, zc + 17.5))
    return web.union(sides).union(brims)


def din_devices(items, x0, y_face, zc):
    """Device envelopes clipped on a rail from x0 rightward: items are (label, width, height across the rail, depth off the plate)."""
    sols, x = [], x0
    for (label, w, h, d) in items:
        sols.append(box(x, x + w, y_face + 7.5, y_face + 7.5 + d, zc - h / 2, zc + h / 2))
        x += w
    return sols, x


hm_rail_y = py_ + 1.5
hm_rail = din_rail(-140.0, 140.0, hm_rail_y, RAIL_ZC)
for x in (-120.0, 120.0):
    hm_rail = hm_rail.cut(cq.Workplane("XZ").center(x, RAIL_ZC).circle(3.15).extrude(-4).translate((0, hm_rail_y - 1, 0)))
    joint((x, py_, RAIL_ZC), (0, -1, 0), (x, hm_rail_y + 1.0, RAIL_ZC))
add("heat-module-din-rail (bought, 35 x 7.5 top hat, 280)", hm_rail, HARDWARE)
CLAMP = ("end clamp", 9.5, 44.0, 33.0)
HM_DEVICES = [CLAMP, ("X_HM mains: 4 x UK 6 N (L1, L2, N, PE)", 32.8, 47.0, 42.0), ("K_HEAT: LC1D18 class contactor", 45.0, 77.0, 86.0),
              ("partition", 2.0, 47.0, 42.0), ("X_HM SELV: 4 x UK 2.5 N", 24.8, 41.0, 36.0), ("CS1 current switch", 60.0, 40.0, 30.0), CLAMP]
hm_dev, hm_dev_x1 = din_devices(HM_DEVICES, -140.0, hm_rail_y, RAIL_ZC)
add("heat-module-devices (bought, envelopes: 2 end clamps, X_HM mains and SELV strips, partition, K_HEAT, CS1)", compound(hm_dev), BOUGHT)
assert hm_dev_x1 <= 140.0, "the heat module's devices must fit its rail"
assert hm_rail_y + 7.5 + max(d for (_, _, _, d) in HM_DEVICES) + 15.0 <= D, "the heat module's devices must stay 15 clear of the rear panel"
# the module's bonding stud and all its M4 hardware
stud = place(hex_bolt_m6(16.0), (140.0, 680.0, e + es), (0, 0, -1))
stud = stud.union(place(nut(P["m6_nut_af"], P["m6_nut_h"], 6.2), (140.0, 680.0, tz1), (0, 0, 1))).union(place(nut(P["m6_nut_af"], P["m6_nut_h"], 6.2), (140.0, 680.0, tz1 + 5.0 + 2.0), (0, 0, 1)))
add("heat-module-bonding-stud (bought, M6 x 16 hex bolt, 2 nuts, star washers; the PE ring terminal goes between the nuts)", stud, HARDWARE)
add(f"heat-module-hardware (bought, {len(hm_hw)} x M4 x 8 button head, {len(hm_nuts)} nuts, 4 T-nuts for the 6 mm slot)", compound(hm_hw + hm_nuts), HARDWARE)
HM_TOP_LIMIT = P["riser_z0"] - 3.0

# ---------------------------------------------------------------------------
# Common power module (draft 7): a plate on the rear faces of the two rear cross rails, left of the riser, behind the
# rear upper panel; five short DIN rails across it, mains on the lower three under a cover, SELV on the upper two above
# a barrier. Serviced with the rear upper panel off. The cord and the bay harness come up through grommets in the bay
# ceiling; the console harness goes up through a grommet in the top panel.
# ---------------------------------------------------------------------------
pm_hw, pm_nuts = [], []


def pjoint(p_head, n, p_nut=None, length=8.0):
    pm_hw.append(place(button_bolt(4.0, P["m4_head_d"], P["m4_head_h"], length, 2.5), p_head, n))
    if p_nut is not None:
        pm_nuts.append(place(m4n_, p_nut, tuple(-c for c in n)))


pz0, pz1, pxc = P["pm_z0"], P["pm_z1"], PM_X0 + PM_W / 2
pm_face = PM_Y + tp                                                       # the plate's rear face: rails, standoffs and the barrier sit on it
pm_rail_x = (PM_X0 + 5.0, PM_X0 + PM_W - 5.0)
pm_bolt_x = (pm_rail_x[0] + 20.0, pm_rail_x[1] - 20.0)
so_pts = [(PM_X0 + 10.0, P["pm_cover_z0"] + 10.0), (PM_X0 + PM_W - 10.0, P["pm_cover_z0"] + 10.0),
          (PM_X0 + 10.0, P["pm_cover_z1"] - 10.0), (PM_X0 + PM_W - 10.0, P["pm_cover_z1"] - 10.0)]
pm_holes = [(x, zc, P["m6_hole"]) for x in (PM_X0 + 15.0, PM_X0 + PM_W - 15.0) for zc in (bt - e / 2, Hb - e / 2)]   # M6 into the cross rails' rear slots
pm_holes += [(x, zc, P["m4_hole"]) for zc in P["pm_rails_z"] for x in pm_bolt_x]                                     # the five rails
pm_holes += [(x, z, P["m4_hole"]) for (x, z) in so_pts]                                                               # cover standoffs
pm_holes += [(x, P["pm_barrier_z"] + A_L / 2, P["m4_hole"]) for x in (pxc - 45.0, pxc + 45.0)]                        # barrier angle
pm_holes += [(PM_X0 + PM_W - 15.0, pz1 - 40.0, 6.6)]                                                                  # ground stud
plate_xz("power-module-plate", PM_X0, PM_X0 + PM_W, pz0, pz1, PM_Y, tp, holes=pm_holes, bolt_side=+1)
assert PM_X0 + PM_W + 10.0 <= -P["riser_w"] / 2, "the power module plate must clear the riser"
assert pz0 <= bt - e + 10.0 and pz1 >= Hb - e + 10.0, "the plate must reach both cross rails"
rails_pm, devs_pm = [], []
PM_DEVICES = {
    "A1": [CLAMP, ("X1 cord: 4 x UK 6 N (L1, L2, N, PE)", 32.8, 47.0, 42.0), ("CB1: 1P MCB", 17.5, 90.0, 60.0), ("F1: UK 5-HESI fuse terminal", 8.2, 65.0, 50.0), CLAMP],
    "A2": [CLAMP, ("PSU: HDR-60-24", 52.5, 90.0, 54.5), ("K_MOTOR: LC1K0910BD class mini contactor", 45.0, 58.0, 57.0), CLAMP],
    "A3": [CLAMP, ("X2 heat module mains: 4 x UK 6 N", 32.8, 47.0, 42.0), ("X3 motor and S1: 5 x UK 2.5 N", 31.0, 41.0, 36.0), CLAMP],
    "B1": [CLAMP, ("RLY_MOTOR, RLY_HEAT, RLY_HEAT_LO: 3 x 38.51 class", 18.6, 93.0, 70.0), ("PTC1 to PTC3 in fuse terminals", 24.6, 65.0, 50.0), ("F2: UK 5-HESI", 8.2, 65.0, 50.0), ("X4 heat module SELV: 4 x UK 2.5 N", 24.8, 41.0, 36.0), CLAMP],
    "B2": [CLAMP, ("X5 chassis switches: 10 x UK 2.5 N", 62.0, 41.0, 36.0), ("X6 sensors: 6 x UK 2.5 N", 37.2, 41.0, 36.0), CLAMP],
}
pm_dev_depth = 0.0
for rail_name, zc in zip(("A1", "A2", "A3", "B1", "B2"), P["pm_rails_z"]):
    r_ = din_rail(pm_rail_x[0], pm_rail_x[1], pm_face, zc)
    for x in pm_bolt_x:
        r_ = r_.cut(cq.Workplane("XZ").center(x, zc).circle(3.15).extrude(-4).translate((0, pm_face - 1, 0)))
        pjoint((x, PM_Y, zc), (0, -1, 0), (x, pm_face + 1.0, zc))
    rails_pm.append(r_)
    sols, x1_ = din_devices(PM_DEVICES[rail_name], pm_rail_x[0], pm_face, zc)
    assert x1_ <= pm_rail_x[1], f"rail {rail_name} devices overrun the rail"
    pm_dev_depth = max(pm_dev_depth, max(d for (_, _, _, d) in PM_DEVICES[rail_name]))
    add(f"power-module-rail-{rail_name}-devices (bought, envelopes: " + ", ".join(lbl for (lbl, _, _, _) in PM_DEVICES[rail_name] if lbl != "end clamp") + ", 2 end clamps)", compound(sols), BOUGHT)
add("power-module-din-rails (bought, 5 x 35 x 7.5 top hat, 140)", compound(rails_pm), HARDWARE)
assert pm_face + 7.5 + pm_dev_depth + 15.0 <= D, "the power module's devices must stay 15 clear of the rear upper panel"
assert P["pm_rails_z"][2] + 47.0 / 2 + 5.0 <= P["pm_barrier_z"] <= P["pm_rails_z"][3] - 93.0 / 2 - 5.0, "the barrier must sit between the mains and SELV devices"
# the barrier: an angle on the plate at the SELV boundary carrying a 1.5 mm shelf out to the devices' depth
bz_ = P["pm_barrier_z"]
ba = angle_x(PM_X0, PM_X0 + PM_W, pm_face, +1, bz_, +1)
for x in (pxc - 45.0, pxc + 45.0):
    ba = hole_y(ba, x, bz_ + A_L / 2)
    pjoint((x, PM_Y, bz_ + A_L / 2), (0, -1, 0), (x, pm_face + A_T, bz_ + A_L / 2))
    ba = hole_z(ba, x, pm_face + A_L / 2)
    pjoint((x, pm_face + A_L / 2, bz_ + A_T + tp), (0, 0, 1), (x, pm_face + A_L / 2, bz_))
add("power-module-barrier-angle (20x20x2 aluminium angle, 150)", ba, ALU)
cut_list.append(("power-module-barrier-angle", "angle 20x20x2 aluminum", PM_W, 1, "mains to SELV barrier, on the plate"))
plate_xy("power-module-barrier", PM_X0, PM_X0 + PM_W, pm_face + A_T, pm_face + 7.5 + pm_dev_depth, bz_ + A_T, tp,
         holes=[(x, pm_face + A_L / 2, P["m4_hole"]) for x in (pxc - 45.0, pxc + 45.0)], r=P["small_corner_r"])
# the cover over the mains rails: 1.5 mm on four M4 x 75 standoffs
cz0, cz1, so_len = P["pm_cover_z0"], P["pm_cover_z1"], P["pm_cover_standoff"]
cover_y = pm_face + so_len
plate_xz("power-module-cover", PM_X0, PM_X0 + PM_W, cz0, cz1, cover_y, tp, holes=[(x, z, P["m4_hole"]) for (x, z) in so_pts])
standoffs = []
so_bar = hexagon(7.0, so_len).cut(cq.Workplane("XY").circle(2.1).extrude(10).translate((0, 0, -1))).cut(cq.Workplane("XY").circle(2.1).extrude(10).translate((0, 0, so_len - 9)))   # M4 bores, threads not drawn
for (x, z) in so_pts:
    standoffs.append(place(so_bar, (x, pm_face, z), (0, 1, 0)))
    pjoint((x, PM_Y, z), (0, -1, 0))                     # plate to standoff
    pjoint((x, cover_y + tp, z), (0, 1, 0))              # cover to standoff
add("power-module-standoffs (bought, 4 x M4 x 75 hex standoffs, female both ends)", compound(standoffs), HARDWARE)
assert cover_y + tp + 15.0 <= D, "the cover must stay 15 clear of the rear upper panel"
assert cz1 <= bz_, "the cover ends at the barrier"
assert cz0 >= bt + tp + P["m6_washer_t"] + P["m6_head_h"] + 2.0, "the cover must clear the bay ceiling's bolt heads on the rear rail"
gs = (PM_X0 + PM_W - 15.0, pz1 - 40.0)
stud = place(hex_bolt_m6(16.0), (gs[0], PM_Y, gs[1]), (0, -1, 0))
stud = stud.union(place(nut(P["m6_nut_af"], P["m6_nut_h"], 6.2), (gs[0], pm_face, gs[1]), (0, 1, 0))).union(place(nut(P["m6_nut_af"], P["m6_nut_h"], 6.2), (gs[0], pm_face + 7.0, gs[1]), (0, 1, 0)))
add("power-module-ground-stud (bought, M6 x 16 hex bolt, 2 nuts, star washers; the cord's PE ring terminal goes between the nuts)", stud, HARDWARE)
add(f"power-module-hardware (bought, {len(pm_hw)} x M4 x 8 button head, {len(pm_nuts)} nuts)", compound(pm_hw + pm_nuts), HARDWARE)
# the grommets: rubber, straddling the 1.5 mm plate
grommets = []
for (gx, gy, gd), gz in ((P["grommet_cord"], bt + tp / 2), (P["grommet_harness"], bt + tp / 2), (P["grommet_console"], Hb + tp / 2)):
    g_ = cq.Workplane("XY").center(gx, gy).circle(gd / 2 - 0.1).circle(gd / 2 - 3.5).extrude(tp).translate((0, 0, gz - tp / 2))                # the neck, in the hole
    for z_ in (gz - tp / 2 - 1.25, gz + tp / 2):                                                                                            # a flange either side of the plate
        g_ = g_.union(cq.Workplane("XY").center(gx, gy).circle(gd / 2 + 3.0).circle(gd / 2 - 3.5).extrude(1.25).translate((0, 0, z_)))
    grommets.append(g_)
add("grommets (bought, 3 x rubber grommets for 1.5 panels: 22 mm hole x 2, 30 mm hole x 1)", compound(grommets), RUBBER)

# cord: strain relief bushing through the base pan at the rear left (body inside the bay, locknut under the pan), the cord
# up through the bay and the ceiling grommet to X1 on the power module, and down under the pan to the back on the height the feet give
cx, cyy = P["cord_x"], P["cord_y"]
bush = hexagon(24.0, 8.0).union(cq.Workplane("XY").circle(10.0).extrude(10).translate((0, 0, 8)).edges(">Z").fillet(3.0))
bush = bush.union(cq.Workplane("XY").circle(10.9).extrude(P["t_base"] + 5.5).translate((0, 0, -P["t_base"] - 5)))     # thread through the pan, as long as the locknut
bush = bush.union(hexagon(26.0, 5.0).translate((0, 0, -P["t_base"] - 5)))                                            # locknut under the pan
bush = bush.cut(cq.Workplane("XY").circle(4.6).extrude(40).translate((0, 0, -20)))                                    # the cord passes through
add("cord-bushing (bought, PG16 strain relief)", place(bush, (cx, cyy, 0.0), (0, 0, 1)), RUBBER)
cord_z = -P["t_base"] - 10.5         # centre line of the run under the pan: 1 mm under the locknut, 3 above the floor with the feet run in
cord = cq.Workplane("XY").center(cx, cyy).circle(4.5).extrude(P["cord_top_z"] - cord_z).translate((0, 0, cord_z))     # up through the bay and the ceiling grommet to X1
cord = cord.union(cq.Workplane("XZ").center(cx, cord_z).circle(4.5).extrude(-(D + 70 - cyy)).translate((0, cyy, 0)))  # back under the pan, 70 past the panel
cord = cord.union(cq.Workplane("XY").add(cq.Solid.makeSphere(4.5, cq.Vector(cx, cyy, cord_z))))                      # the bend
add("power-cord (bought)", cord, RUBBER)
assert cord_z - 4.5 > -(P["foot_height"] + P["t_base"]), "the cord must clear the floor under the pan"
assert abs(P["grommet_cord"][0] - cx) < 1e-9 and abs(P["grommet_cord"][1] - cyy) < 1e-9, "the cord's grommet sits over its bushing"
assert P["cord_top_z"] < P["pm_rails_z"][0] - 47.0 / 2, "the cord ends under X1"

# rollers: four catalog drum rollers on ISO 7379 shoulder screws through the bulkheads (7b). The shoulder bears on the
# bulkhead and the nut clamps it there; the roller turns on the shoulder between a 1.0 shim under the head and a spacer
# against the bulkhead, with 0.5 end float. Front rollers flush with the drum's front end, rear ones 1.5 proud of its
# rear end, so one 35 shoulder serves both.
roller_w = 25.0   # catalog roller width, measured at V-106
SH, THR, SP = P["roller_stud_shoulder"], P["roller_stud_thread"], P["roller_spacer"]
roller_y = {"front": y0d + P["roller_inset"], "rear": y0d + L - P["roller_inset_rear"] - roller_w}


def shoulder_screw():
    """ISO 7379 10 x 35 M8 along +Z: head above z 0, shoulder z -35..0, thread below; the shim and spacer are separate."""
    head = cq.Workplane("XY").circle(P["roller_stud_head_d"] / 2).extrude(P["roller_stud_head_h"]).edges(">Z").chamfer(0.8)
    head = head.cut(hexagon(5.0, 4.0).translate((0, 0, P["roller_stud_head_h"] - 3.5)))
    shoulder = cq.Workplane("XY").circle(5.0).extrude(SH + 0.5).translate((0, 0, -SH))
    thread = cq.Workplane("XY").circle(4.0).extrude(THR + 0.5).translate((0, 0, -SH - THR)).faces("<Z").chamfer(0.6)
    return head.union(shoulder).union(thread)


stud_hw = []
for i, (x, z, d) in enumerate(rollers):
    for end, sgn, bulk_face in (("front", +1, P["front_bulk_y"] + tb), ("rear", -1, P["rear_bulk_y"])):
        ry0 = roller_y[end]
        r = cq.Workplane("XZ").center(x, z).circle(P["roller_d"] / 2).circle(P["roller_bore_d"] / 2).extrude(-roller_w).translate((0, ry0, 0))
        add(f"roller-{end}-{i+1} (bought)", r, BOUGHT)
        n = (0, sgn, 0)
        head_face = bulk_face + sgn * SH                                   # the shoulder's step bears on the bulkhead's drum-side face
        stud_hw.append(place(shoulder_screw(), (x, head_face, z), n))
        shim_y = ry0 + roller_w if sgn > 0 else ry0 - 1.0                  # 1.0 shim between the roller and the head
        stud_hw.append(cq.Workplane("XZ").center(x, z).circle(8.0).circle(5.25).extrude(-1.0).translate((0, shim_y, 0)))
        spc_y = bulk_face if sgn > 0 else bulk_face - SP                    # spacer 16 x 10.5 x 8.5 between the bulkhead and the roller
        stud_hw.append(cq.Workplane("XZ").center(x, z).circle(8.0).circle(5.25).extrude(-SP).translate((0, spc_y, 0)))
        far = bulk_face - sgn * tb                                          # the bulkhead's far face: washer and nut
        stud_hw.append(place(cq.Workplane("XY").circle(8.0).circle(4.2).extrude(1.6), (x, far, z), (0, -sgn, 0)))
        stud_hw.append(place(nut(13.0, 6.5, 8.2), (x, far - sgn * 1.6, z), (0, -sgn, 0)))
        assert abs((spc_y + SP if sgn > 0 else spc_y) - (ry0 if sgn > 0 else ry0 + roller_w)) < 1e-6, "the spacer must reach the roller"
        assert abs(abs(head_face - (shim_y + 1.0 if sgn > 0 else shim_y)) - 0.5) < 1e-6, "the roller's end float must be 0.5"
add("hardware-roller-studs (bought, 4 x ISO 7379 shoulder screws 10 x 35 M8, 1.0 shims, spacers 16 x 10.5 x 8.5, M8 washers and nuts)", compound(stud_hw), HARDWARE)

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
# the whole heat module must pass under the hood (230) and the mid rear end rail (260) when the tray slides out the back
hm_zmax = max((s_.val() if hasattr(s_, "val") else s_).BoundingBox().zmax for n, s_, _, _, _ in parts if n.startswith("heat-module"))
assert hm_zmax <= HM_TOP_LIMIT + 1e-6, f"heat module reaches {hm_zmax}, over the hood's {P['riser_z0']} less 3"
P["hm_zmax"] = hm_zmax
assy = cq.Assembly(name="osa-dryer")
for name, solid, color, plate, t in parts:
    assy.add(solid, name=name, color=color)


def fix_step_header(path):
    """The STEP writer stamps the file with the time of day, so an unchanged part came out as a changed file on every
    run. Pin the stamp so the repository's diffs show geometry changes only (the model's draft is the version)."""
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        head = f.read(400)
    m = re.search(r"'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}'", head)
    if not m:
        return
    with open(path, "r+b") as f:
        data = f.read()
        stamp = m.group(0).encode()
        fixed = f"'draft-{DRAFT}'".encode().ljust(len(stamp), b" ")   # same length, so nothing else in the file moves
        f.seek(0)
        f.write(data.replace(stamp, fixed, 1))


assy.save(os.path.join(OUT, "step", "osa-dryer-assembly.step"))
fix_step_header(os.path.join(OUT, "step", "osa-dryer-assembly.step"))
for name, solid, color, plate, t in parts:
    if "(" in name:   # bought parts, envelopes, hardware and cut-to-length catalog stock get no STEP of their own
        continue
    exporters.export(solid, os.path.join(OUT, "step", f"{name}.step"))
    fix_step_header(os.path.join(OUT, "step", f"{name}.step"))

with open(os.path.join(OUT, "drawings", "frame-cut-list.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["item", "profile", "length_mm", "qty", "note"])
    for row in cut_list:
        w.writerow(row)


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
    H = w if turn in (90, 270) else h
    label = f'<text x="20" y="{H - 12}" font-family="Helvetica, Arial, sans-serif" font-size="18">osa-dryer check view: {vname} (draft {DRAFT}, not for cutting)</text>'   # along the bottom edge, clear of the drawing
    open(path, "w", encoding="utf-8").write(head + body + label + "</svg>")

if "--no-views" not in sys.argv:
    VIEW_PARTS = [(n, s) for n, s, _, _, _ in parts if not n.startswith("hardware-")]   # bolts make the line drawings unreadable
    compound_all = cq.Compound.makeCompound([s.val() if hasattr(s, "val") else s for _, s in VIEW_PARTS])
    OUTER = ("side-panel-left", "side-panel-right", "front-upper-panel", "front-lower-panel", "rear-upper-panel",
             "rear-lower-panel", "top-panel", "console-face", "console-cap", "console-cheek-left", "console-cheek-right",
             "console-rear", "door-ring", "door-disc")
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
if "--bbox" in sys.argv:   # every part's bounding box, for a quick look at where things are (into the audit folder)
    os.makedirs(os.path.join(OUT, "cad", "audit"), exist_ok=True)
    with open(os.path.join(OUT, "cad", "audit", "part-bboxes.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["part", "xmin", "xmax", "ymin", "ymax", "zmin", "zmax"])
        for n, s_, _, _, _ in parts:
            bb = (s_.val() if hasattr(s_, "val") else s_).BoundingBox()
            w.writerow([n] + [round(q, 2) for q in (bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax)])
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
            common = a.intersect(b)
            v = common.Volume()
        except Exception as ex:  # a failed boolean is reported, not hidden
            bad.append((na, nb, f"boolean failed: {ex}", ""))
            continue
        if v > 1.0:   # mm3; touching faces give 0
            cb = common.BoundingBox()
            bad.append((na, nb, round(v, 1), " at " + " ".join(f"{q:.1f}" for q in (cb.xmin, cb.xmax, cb.ymin, cb.ymax, cb.zmin, cb.zmax))))
    if bad:
        print("INTERFERENCE:")
        for na, nb, v, where in bad:
            print(f"  {na}  x  {nb}  : {v}{where}")
    else:
        print("interference check: no overlaps")
print("drum axis Z", P["drum_axis_z"], " H_body", P["H_body"], " H_total", round(P["H_total"], 1), " rear bulkhead Y", P["rear_bulk_y"],
      " lint slot area", round(P["lint_slot_area"]), " hood section", round(P["hood_area"]))
print("drum sheet flat", round(P["drum_flat_w"], 1), "x", P["drum_l"], " belt drawn length", round(P["belt_len_est"], 1),
      " belt crosses the ceiling at X", round(P["belt_cross_left"], 2), "and", round(P["belt_cross_right"], 2), " feet", P["foot_height"])
print("drum", round(P["drum_rpm"], 1), "rpm", " heat module top", round(P["hm_zmax"], 1), " collar area", round(P["hm_collar_area"]),
      " inlet area", round(P["hm_inlet_area"]), " felt arcs", round(P["felt_long_len"]), "and", round(P["felt_short_len"]))
