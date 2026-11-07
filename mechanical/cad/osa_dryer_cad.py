"""osa-dryer parametric mechanical model.

One file holds every number. Run it and it writes:
  step/osa-dryer-assembly.step          the whole machine, bought parts as envelopes or representations
  step/<part>.step                      one file per part we make
  drawings/<part>.dxf                   flat pattern for every laser-cut plate (CUT layer)
  drawings/frame-cut-list.csv           every extrusion length
  drawings/view-*.svg                   views for checking, not for cutting

Coordinate system: X across the cabinet (left negative), Y from front (0) to back, Z up from the floor.
All dimensions mm. Needs cadquery (pip install cadquery). Also runs in FreeCAD's CadQuery workbench.

Status: draft 9, 2026-11-06. Draft 9 finishes the parts of the reference build: the blower plate the housing hangs on
(a 1.5 mm plate on two angle feet in front of the housing, the spool's foam on its face), the exhaust set (the housing's
102 collar, a catalog 4 in pipe through the rear lower panel's port as the hose spigot, two clamps, the air-proving tap
and tube), the two chassis sensors the UCI-D wires to J2 (the exhaust thermistor on the lint box's back plate, the
moisture bar set on the front bulkhead's drum side), the gas and condensate entries in the rear lower panel with their
blanking plates, and the harness's cable clamps. The no-heat module is the electric module's tray and box with nothing
in them (DECISIONS.md). Draft 8 draws the ducts as parts: 1.5 mm plates screwed into the tapped edges of aluminium
flat bar frames (the lint box between the front stubs with the bulkhead as its back wall, a spool to the blower, the riser's
hood, trunk and nozzle), the throat liner the drawing showed was missing (a rolled strip between the door ring and the
bulkhead; the lint box's top follows it), the lint basket (mesh on laser-cut sector plates through the widened slot, a
D-pull on its lip), the door switch, PS1, the exhaust thermostats, the motor cradles' bolts, two grommets and four clamp
holes for the harnesses. Draft 5 drew what the documents already called for but the model only
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
DRAFT = 9
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
    lint_slot_r0=238.0, lint_slot_r1=267.0, lint_slot_half_deg=36.0,   # 8 outside the 460 opening, 3 inside the 540 bore; 9201 mm2 (draft 8: 267 so the basket passes with 0.9 each side)
    # throat liner (draft 8): a rolled 1.5 mm strip between the door ring and the front bulkhead that closes the gap round
    # the opening; the lint box's top follows it. Inner radius 235.5 (the ring's 235 edge covers its front end)
    liner_ri=235.5, liner_t=1.5, liner_y0=-1.5, liner_len=41.3,   # from the ring's back face to 0.2 short of the bulkhead
    # lint box (draft 8): 1.5 mm plates on a frame of 30 x 8 aluminium flat bar, in front of the bulkhead between the
    # mid front stubs; the bulkhead is its back wall above 265, a plate below; a spool of 40 x 8 bar to the blower mouth
    lb_y0=7.0, bar_w=30.0, bar_t=8.0, lb_x=166.0, lb_z0=62.0, lb_gap=1.5,   # front plate from Y 7 (the ring bolts' tips end at 4.5); 1.5 foam between the bars and the bulkhead
    lb_hang_z=280.0, lb_hang_y=20.0, lb_rear_plate_z1=275.0, lb_bulk_screw_z=(310.0, 345.0, 380.0),   # the lowest head clears the bay ceiling's front edge (Fusion found 300 in it, draft 8)   # M6 into the stubs' inner slots; the lower back plate laps the bulkhead's foot 10; M4 from the drum side into the side bars
    sp_half=78.0, sp_bar_w=40.0, sp_z0=62.0, sp_z1=198.0, sp_foam=4.0,   # spool: four 40 x 8 bars, 156 wide, 62 to 198 tall (its bottom bar behind the box's), foam 6 compressed to 4 on the blower's inlet face (V-107)
    # lint basket (draft 8): mesh wrapped round two laser-cut sector plates, clamped by two more; it slides through the slot
    bk_r0=239.5, bk_r1=265.5, bk_half_deg=35.6, bk_t=3.0, bk_flange=5.0, mesh_t=0.6,   # 3 mm plates, tapped M3
    bk_far_y0=9.0, bk_lip_y0=41.5, bk_pull_r=214.0, bk_pull_c=64.0,   # the far plate 2 behind the front plate; the lip on the bulkhead's drum side; a 64 mm D-pull on the lip's tab, inside the opening
    # riser (draft 8): a trunk of two 50 x 8 bars between 1.5 mm plates up the back, standing on a hood of 25 x 8 bars
    # over the heat module's collar, and a nozzle of 40 x 8 bars from the trunk's front plate to the inlet field
    riser_z0=230.0, hood_y0=448.0, hood_bar_w=25.0, hood_x=175.0, tr_x=130.0, tr_bar_w=50.0, tr_y0=652.5, tr_over=20.0, nz_x=114.0, nz_bar_w=40.0, nz_z=(658.5, 816.5), nz_foam=1.0,
    hood_gasket_od=150.0, hood_gasket_t=3.0,   # foam ring glued under the hood; the collar's rim brushes it
    # door switch (draft 8): plunger through the ring and panel at 45 degrees right of bottom on the ring bolts' radius, the disc presses it
    ds_angle_deg=45.0, ds_r=258.0, ds_plunger_d=8.0, ds_body=(30.0, 25.0, 45.0),
    ps1_xy=(250.0, 70.0), tf_x=(130.0, 180.0, 230.0),   # air-proving switch on an angle bracket on the pan; exhaust thermostats on the blower's outlet box
    ds_grommet_ceil=(290.0, 60.0, 16.0), ds_grommet_bulk=(290.0, 330.0, 16.0),   # the door switch cable and the moisture pair: up through the bay ceiling behind the bulkhead, through the bulkhead to the front gap (draft 8; 16 mm in draft 9 for the second cable)
    clamp_pts=((-250.0, 120.0), (-250.0, 280.0), (-250.0, 440.0), (-250.0, 600.0)),   # M4 cable clamps along the bay's left side for the bay harness (draft 8)
    # draft 9: the blower plate, the exhaust set, the two chassis sensors, the blanked entries
    bp_x=130.0, bp_z1=245.0, bp_foot_x=(45.0, 135.0), bp_screws=((-88.0, 60.0), (88.0, 60.0), (-88.0, 180.0), (88.0, 180.0)),   # 1.5 mm plate in front of the housing on two 20x20x2 angle feet; the housing's screws on a nominal 176 x 120 pattern (V-107)
    exhaust_wall=1.0, exhaust_collar_len=25.0, exhaust_proud=50.0, exhaust_tap_y=300.0, clamp_w=12.0,   # catalog 4 in pipe over the housing's collar, 50 proud of the rear panel as the hose spigot; PS1's tap on its top
    th1_xz=(120.0, 160.0), th1_body=(36.0, 14.0, 30.0), th1_nib=(10.0, 8.5, 16.0), th1_nib_dz=-5.0, th1_bolt_dz=10.0,   # exhaust thermistor on the lint box's back plate, right of the spool, sensing inside the box: body (w, depth, h) centred at (x, z) on the bay side, its nib through a 12 x 18 slot, one M4 x 20 through the plate and the body
    ms_angle_deg=58.0, ms_r=250.0, ms_len=90.0, ms_w=30.0, ms_t=8.0, ms_tab=35.0,   # moisture bar set on the front bulkhead's drum side, right of the lint slot, inside the ring bore (its corners reach radius 268.8); two M4 at +-35 along the bars
    gas_entry=(-230.0, 150.0, 25.0), cond_entry=(-230.0, 66.0, 20.0), blank_w=60.0, blank_h=44.0, blank_dx=21.0,   # the gas and condensate entries in the rear lower panel (x, z, hole), blanked by 60 x 44 plates on two M4; the lower blank 4 above the bottom rail (Fusion found it 2 into the rail at Z 60)
    # rear air inlet zone
    inlet_w=200.0, inlet_h=130.0, inlet_above_axis=50.0, inlet_hole_d=10.0, inlet_pitch=14.0,   # inside the ring opening (R 240)
    # console: a vertical box at the rear of the top on its own 4040 sub-frame (draft 6), holding the full UCI envelope
    console_h=200.0, uci_ap_z_off=83.0,   # console depth: from the top rear cross rail to the back (set below). Aperture centre above the top panel: the module's nuts under the front rail, the faceplate under its bolts
    uci_ap_w=560.0, uci_ap_h=120.0, uci_hole_x=590.0, uci_hole_y=140.0, uci_hole_d=4.5,   # UCI-D draft 6: 560 wide, six holes (the corners plus two on the centre line); 15 to the console posts' inner faces
    # fasteners
    m6_hole=6.5, m4_hole=4.5, panel_pitch=150.0,
    # bay layout (envelopes)
    motor_axis_z=120.0, motor_len=200.0, motor_d=140.0, motor_y0=190.0,   # motor behind the blower, pulley on its rear shaft
    blower_d=220.0, blower_w=100.0, blower_y0=85.5,                       # blower on the front shaft, inlet facing front; its inlet face on the back of the blower plate (draft 9: 84 + 1.5)
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
    fp_w=620.0, fp_h=160.0, fp_r=10.0, fp_t=2.0,   # 620 wide (UCI-D draft 6): 35 to the console's edges, like the 37 above it
    knob_d=40.0, knob_skirt_h=3.0, knob_body_d=30.0, knob_h=20.0,
)


class Ex(float):
    """A number that remembers how it was made from the named parameters, for the Fusion build (mechanical/cad/fusion_build):
    the plates' outlines and hole rows come out as expressions in the user parameters a builder can change in Fusion.
    Lengths only; a product or ratio of two lengths drops back to a plain float."""

    def __new__(cls, v, expr=None):
        o = float.__new__(cls, float(v))
        o.expr = expr if expr is not None else f"{float(v):g} mm"
        return o

    @staticmethod
    def _e(o):
        return o.expr if isinstance(o, Ex) else f"{float(o):g} mm"

    def __add__(self, o):
        return Ex(float(self) + float(o), f"({self.expr} + {Ex._e(o)})")

    def __radd__(self, o):
        return Ex(float(o) + float(self), f"({Ex._e(o)} + {self.expr})")

    def __sub__(self, o):
        return Ex(float(self) - float(o), f"({self.expr} - {Ex._e(o)})")

    def __rsub__(self, o):
        return Ex(float(o) - float(self), f"({Ex._e(o)} - {self.expr})")

    def __mul__(self, o):
        if isinstance(o, Ex):
            return float(self) * float(o)
        return Ex(float(self) * float(o), f"({self.expr} * {float(o):g})")

    __rmul__ = __mul__

    def __truediv__(self, o):
        if isinstance(o, Ex):
            return float(self) / float(o)
        return Ex(float(self) / float(o), f"({self.expr} / {float(o):g})")

    def __neg__(self):
        return Ex(-float(self), f"(-{self.expr})")

    def __pos__(self):
        return self


# the user parameters of the Fusion build: P key -> parameter name. Everything derived from these carries an expression.
USER_PARAMS = [("W", "cab_w"), ("D", "cab_d"), ("ext", "ext"), ("ext_small", "ext_small"), ("bay_top", "bay_top"),
               ("t_panel", "t_panel"), ("t_bulk", "t_bulk"), ("t_base", "t_base"), ("drum_d", "drum_d"), ("drum_l", "drum_l"),
               ("drum_front_y", "drum_front_y"), ("door_opening_d", "door_d"), ("panel_pitch", "panel_pitch"),
               ("console_h", "console_h"), ("uci_ap_w", "uci_w"), ("uci_ap_h", "uci_h"),
               ("drum_clear_bottom", "drum_clear_bottom"), ("drum_clear_top", "drum_clear_top")]
for _k, _n in USER_PARAMS:
    P[_k] = Ex(P[_k], _n)
# derived parameters the Fusion build defines by these formulas, so the expressions downstream stay readable
DERIVED_PARAMS = [("half_w", "half_w", "cab_w / 2"), ("inner_w", "inner_w", "cab_w - 2 * ext"),
                  ("drum_axis_z", "drum_axis_z", "bay_top + t_base + drum_clear_bottom + drum_d / 2"),
                  ("H_body", "cab_h", "drum_axis_z + drum_d / 2 + drum_clear_top + ext"),
                  ("front_bulk_y", "front_bulk_y", "ext"), ("rear_bulk_y", "rear_bulk_y", "drum_front_y + drum_l + 10 mm"),
                  ("rear_cross_y", "rear_cross_y", "rear_bulk_y + t_bulk"), ("console_depth", "console_depth", "cab_d - rear_cross_y")]
P["drum_rim_r"] = P["drum_d"] / 2
P["bp_y0"] = P["blower_y0"] - P["t_panel"]                   # the blower plate's front face: the spool's foam lands on it (draft 9)
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
for _k, _n, _f in DERIVED_PARAMS:   # the value as computed above, named for the Fusion build
    P[_k] = Ex(P[_k], _n)
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
plate_log = []      # every flat plate as drawn, with the expressions its numbers carry (for the Fusion build)


def _ex(v):
    return getattr(v, "expr", None)


def _rec(vals):
    """A tuple of numbers as [floats..., expressions...] for the plate log."""
    return [float(v) for v in vals] + [_ex(v) for v in vals]


def record_plate(name, kind, u0, u1, v0, v1, pos, t, holes, rect_cuts, circ_cuts, slots, sectors, r):
    plate_log.append(dict(name=name, kind=kind, u0=float(u0), u1=float(u1), v0=float(v0), v1=float(v1), pos=float(pos), t=float(t), r=float(r),
                          ex=dict(u0=_ex(u0), u1=_ex(u1), v0=_ex(v0), v1=_ex(v1), pos=_ex(pos), t=_ex(t)),
                          holes=[_rec(h) for h in holes], rect_cuts=[_rec(c) for c in rect_cuts], circ_cuts=[_rec(c) for c in circ_cuts],
                          slots=[_rec(c) for c in slots], sectors=[_rec(c) for c in sectors]))
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
    record_plate(name, "xz", x0, x1, z0, z1, y0, t, holes, rect_cuts, circ_cuts, slots, sectors, r)
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
    record_plate(name, "xy", x0, x1, y0, y1, z0, t, holes, rect_cuts, circ_cuts, (), (), r)
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
    record_plate(name, "yz", y0, y1, z0, z1, x0, t, holes, rect_cuts, (), (), (), r)
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
        ezdxf.options.write_fixed_meta_data_for_testing = True   # fixed timestamps and GUIDs, so an unchanged drawing is an unchanged file (draft 9)
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
    return [a if i == 0 else a + i * (b - a) / n for i in range(n + 1)]


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

# front bulkhead: door opening, lint slot, front roller holes; bolt heads on its back face (the rails are in front of it).
# Draft 8: six 4.5 holes for the M4 that pull the lint box's side bars against it from the drum side (outside the felt)
LB_BAR_X = P["lb_x"] - P["bar_t"] / 2
lb_bulk_pts = [(sx * LB_BAR_X, z) for sx in (-1, 1) for z in P["lb_bulk_screw_z"]]
# draft 9: the moisture bar set on the drum side, right of the lint slot, inside the ring bore: two M4 holes along the bars
# and a 16 hole for its two terminals, which reach the front gap and run with the door switch cable
_ms = math.radians(P["ms_angle_deg"])
MS_U, MS_T = (math.sin(_ms), -math.cos(_ms)), (math.cos(_ms), math.sin(_ms))        # outward along the radius, and along the bars
MS_C = (P["ms_r"] * MS_U[0], az + P["ms_r"] * MS_U[1])
MS_PTS = [(MS_C[0] + k * MS_T[0], MS_C[1] + k * MS_T[1]) for k in (-P["ms_tab"], P["ms_tab"])]
plate_xz("front-bulkhead", bulk_x0, bulk_x1, bulk_z0, bulk_z1, P["front_bulk_y"], tb,
         holes=bulk_holes(front=True) + rollers + glide_holes + [(x, z, P["m4_hole"]) for (x, z) in lb_bulk_pts] + [P["ds_grommet_bulk"]]
         + [(x, z, P["m4_hole"]) for (x, z) in MS_PTS] + [(MS_C[0], MS_C[1], 16.0)],
         circ_cuts=[(0, az, P["door_opening_d"])],
         sectors=[(0, az, P["lint_slot_r0"], P["lint_slot_r1"], P["lint_slot_half_deg"])], bolt_side=+1)
P["lint_slot_area"] = math.radians(2 * P["lint_slot_half_deg"]) / 2 * (P["lint_slot_r1"] ** 2 - P["lint_slot_r0"] ** 2)
assert P["lint_slot_r1"] < P["ring_id"] / 2 and P["lint_slot_r0"] > P["door_opening_d"] / 2, "lint slot must sit between the door opening and the ring bore"
_ms_half = math.degrees(math.atan2(P["ms_len"] / 2, P["ms_r"]))
assert math.hypot(P["ms_r"] - P["ms_w"] / 2, P["ms_len"] / 2) > P["door_opening_d"] / 2 + 3.0 and math.hypot(P["ms_r"] + P["ms_w"] / 2, P["ms_len"] / 2) < P["ring_id"] / 2 - 1.0, "the moisture bar set's corners sit on the bulkhead between the opening and the ring bore"
assert P["ms_angle_deg"] - _ms_half > P["bk_half_deg"] + 2.0 + 6.0, "the moisture bars clear the basket's lip ring"

# rear bulkhead: inlet hole field, roller shaft holes, mounting holes; bolt heads on its front face (the cross rails are behind it)
inlet = []
nx = int(P["inlet_w"] // P["inlet_pitch"])
nz = int(P["inlet_h"] // P["inlet_pitch"])
for i in range(nx):
    for j in range(nz):
        x = -P["inlet_w"] / 2 + P["inlet_pitch"] / 2 + i * P["inlet_pitch"]
        z = az + P["inlet_above_axis"] + j * P["inlet_pitch"]
        inlet.append((x, z, P["inlet_hole_d"]))
# draft 8: ten 4.5 holes round the field for the M4 that hold the riser's nozzle to the bulkhead from the drum side
NZ_BX = P["nz_x"] - P["bar_t"] / 2                                   # the nozzle's side bars' centre line
nz_z0, nz_z1 = P["nz_z"]
nz_bulk_pts = ([(sx * NZ_BX, z) for sx in (-1, 1) for z in (690.0, 785.0)]
               + [(x, z) for x in (-70.0, 0.0, 70.0) for z in (nz_z0 + P["bar_t"] / 2, nz_z1 - P["bar_t"] / 2)])
plate_xz("rear-bulkhead", bulk_x0, bulk_x1, bulk_z0, bulk_z1, P["rear_bulk_y"], tb,
         holes=bulk_holes() + rollers + inlet + glide_holes + [(x, z, P["m4_hole"]) for (x, z) in nz_bulk_pts], bolt_side=-1)
for (x, z) in nz_bulk_pts:
    assert math.hypot(x, z - az) < P["ring_id"] / 2 - 15.0, "the nozzle's screws must sit inside the ring opening, clear of the felt"


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
ceil_holes += [(gx, gy, gd) for (gx, gy, gd) in (P["grommet_cord"], P["grommet_harness"], P["ds_grommet_ceil"])]   # grommets: the cord and the bay harness come up to the power module; the door switch cable goes up at the right front (draft 8)
plate_xy("bay-ceiling", -hw + tp, hw - tp, P["ceil_y0"], D, bt, P["t_base"], holes=ceil_holes,
         rect_cuts=[(round(P["belt_cross_left"], 1), P["belt_y"], P["belt_slot_w"], P["belt_slot_l"]),    # belt slots, one per run
                    (round(P["belt_cross_right"], 1), P["belt_y"], P["belt_slot_w"], P["belt_slot_l"]),
                    (0, P["rear_bulk_y"] + tb / 2, P["inner_w"] + 2, tb + 1),    # rear bulkhead passes through
                    (-hw + e / 2, D - e / 2, e + 1, e + 1), (hw - e / 2, D - e / 2, e + 1, e + 1),   # rear post notches
                    (0, P["tr_y0"] + (P["tr_bar_w"] + 2 * tp) / 2, 2 * P["tr_x"] + 4, P["tr_bar_w"] + 2 * tp + 4),   # riser trunk, 2 mm clearance (draft 8)
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
CRADLE_Y = (P["motor_y0"] + 25.0, P["motor_y0"] + P["motor_len"] - 55.0)   # the motor's two cradle mounts (30 deep, Y from these)
cradle_pts = [(sx * 22.0, yy + 15.0) for yy in CRADLE_Y for sx in (-1, 1)]   # draft 8: two M6 per cradle through the pan
ps1_pts = [(P["ps1_xy"][0] + k, P["ps1_xy"][1]) for k in (-15.0, 15.0)]     # draft 8: the air-proving switch's angle bracket
BP_FOOT_Y = P["bp_y0"] - 20.0 / 2                                             # draft 9: the blower plate's two 20x20x2 angle feet, in front of the plate; bolts on the foot legs' centre line
bp_foot_pts = [(sx * x, BP_FOOT_Y) for sx in (-1, 1) for x in (70.0, 110.0)]
base_holes += [(x, y, P["m6_hole"]) for (x, y) in cradle_pts + ps1_pts + bp_foot_pts]
base_holes += [(x, y, P["m4_hole"]) for (x, y) in P["clamp_pts"]]   # cable clamps for the bay harness (draft 8)
plate_xy("base-pan", -hw + tp, hw - tp, 0, D, -P["t_base"], P["t_base"], holes=base_holes, bolt_side=-1, bolt_skip=tuple(bracket_pts + cradle_pts + ps1_pts + bp_foot_pts))   # the exhaust leaves through the rear lower panel

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
# door switch (draft 8): plunger through the ring and the panel on the ring bolts' radius, 45 degrees right of bottom; the
# body sits behind the panel on two M4 outside the ring, radially outboard of the plunger
_ds = math.radians(P["ds_angle_deg"])
DS_U, DS_T = (math.sin(_ds), -math.cos(_ds)), (math.cos(_ds), math.sin(_ds))      # outward along the radius, and along the tangent
DS_P = (P["ds_r"] * DS_U[0], az + P["ds_r"] * DS_U[1])                              # the plunger
DS_M = [(288.0 * DS_U[0] + k * DS_T[0], az + 288.0 * DS_U[1] + k * DS_T[1]) for k in (-10.0, 10.0)]   # the mounting holes
plate_xz("front-upper-panel", -hw, hw, P["panel_split_z"], Hb, -tp, tp,
         holes=end_holes(P["panel_split_z"], Hb, [bt - e / 2, Hb - e / 2], stubs_only_at=bt - e / 2)
         + [(x, z, P["m4_hole"]) for (x, z) in ring_bolt_pts] + [(x, z, P["m6_hole"]) for (x, z) in hinge_fixed_bolt_pts]
         + [(DS_P[0], DS_P[1], P["ds_plunger_d"] + 0.5)] + [(x, z, P["m4_hole"]) for (x, z) in DS_M],
         circ_cuts=[(0, az, P["door_ring_id"] + 10)], bolt_side=-1, bolt_skip=tuple(hinge_fixed_bolt_pts + DS_M))
louvers = [(x, z, 60, 5) for x in (-240, -160, -80, 0, 80, 160, 240) for z in range(80, 240, 20)]
plate_xz("front-lower-panel", -hw, hw, 0, P["panel_split_z"] - 1, -tp, tp,
         holes=end_holes(0, P["panel_split_z"] - 1, [e / 2]), slots=louvers, bolt_side=-1)
plate_xz("rear-upper-panel", -hw, hw, P["panel_split_z"], Hb, D, tp, holes=end_holes(P["panel_split_z"], Hb, [bt - e / 2, Hb - e / 2]), bolt_side=+1)
rear_louvers = [(x, z, 60, 5) for x in (-160, -80, 0, 80) for z in range(80, 240, 20)]   # clear of the exhaust port and the cord entry
# draft 9: the gas entry (3/8 NPT bulkhead fitting, gas module) and the condensate drain (grommeted hose, heat pump module)
# at the left, blanked on every other build by a 60 x 44 plate on two M4 inside the panel
ENTRIES = (P["gas_entry"], P["cond_entry"])
entry_holes = [(x, z, d) for (x, z, d) in ENTRIES] + [(x + k, z, P["m4_hole"]) for (x, z, d) in ENTRIES for k in (-P["blank_dx"], P["blank_dx"])]
plate_xz("rear-lower-panel", -hw, hw, 0, P["panel_split_z"] - 1, D, tp,
         holes=end_holes(0, P["panel_split_z"] - 1, [e / 2]) + entry_holes,
         circ_cuts=[(P["exhaust_x"], P["exhaust_z"], P["exhaust_d"] + 4)],    # the exhaust duct passes with 2 mm clearance; the cord enters through the base pan
         slots=rear_louvers, bolt_side=+1)
for (x, z, d) in ENTRIES:
    assert x + P["blank_w"] / 2 < -190.0 - 4.0 and x - P["blank_w"] / 2 > -hw + e + 8.0, "the blanking plates sit between the post's bolts and the louvers"
    assert z - P["blank_h"] / 2 > e + 2.0, "the blanking plates stand clear of the bottom rail itself (its bolt heads are lower)"

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
ring = ring.cut(cq.Workplane("XZ").center(*DS_P).circle((P["ds_plunger_d"] + 0.5) / 2).extrude(-P["t_door"] - 2).translate((0, ring_y0 - 1, 0)))   # door switch plunger (draft 8)
add("door-ring", ring, STEEL, plate=True, t=P["t_door"])
sk = cq.Workplane("XY").circle(P["door_ring_od"] / 2).extrude(1).cut(cq.Workplane("XY").circle(P["door_ring_id"] / 2).extrude(3).translate((0, 0, -1)))
for (x, z) in ring_bolt_pts:
    sk = sk.cut(cq.Workplane("XY").center(x, z - az).circle(P["m4_hole"] / 2).extrude(3).translate((0, 0, -1)))
for (x, z) in hinge_fixed_bolt_pts:
    sk = sk.cut(cq.Workplane("XY").center(x, z - az).circle(P["m6_hole"] / 2).extrude(3).translate((0, 0, -1)))
sk = sk.cut(cq.Workplane("XY").center(DS_P[0], DS_P[1] - az).circle((P["ds_plunger_d"] + 0.5) / 2).extrude(3).translate((0, 0, -1)))
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
cradle_hw = []
for i, yy in enumerate(CRADLE_Y):   # two cradle brackets from the motor mount kit (3 mm, drawn as a shell), two M6 each through the base pan (draft 8)
    cradle = box(-35, 35, yy, yy + 30, 0, mz - 20).cut(box(-30, 30, yy + 3, yy + 27, 3, mz - 20 + 1))
    cradle = cradle.cut(cq.Workplane("XZ").center(0, mz).circle(md / 2 + 0.5).extrude(-40).translate((0, yy - 5, 0)))
    for (x, y) in cradle_pts:
        if yy <= y <= yy + 30:
            cradle = cradle.cut(cq.Workplane("XY").center(x, y).circle(P["m6_hole"] / 2).extrude(6).translate((0, 0, -1)))
            cradle_hw.append(place(hex_bolt_m6(), (x, y, -P["t_base"]), (0, 0, -1)))                        # head under the pan
            cradle_hw.append(place(nut(P["m6_nut_af"], P["m6_nut_h"], 6.2), (x, y, 3.0), (0, 0, 1)))        # nut on the bracket's foot
    add(f"motor-mount-{i+1} (bought, cradle bracket)", cradle, BOUGHT)
add("hardware-motor-mounts (bought, 4 x M6 x 12 hex, washers, nuts, through the base pan)", compound(cradle_hw), HARDWARE)
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
OB_Z0, OB_Z1 = P["exhaust_z"] - P["exhaust_d"] / 2 - 5.0, P["exhaust_z"] + P["exhaust_d"] / 2 + 5.0                 # the outlet box round the 102 collar (draft 9: 94 to 206)
blower = blower.union(box(100, P["exhaust_x"] + P["exhaust_d"] / 2 + 10.0, P["blower_y0"] + 26, my0, OB_Z0, OB_Z1))   # tangential outlet box, its discharge collar on its rear face
add("blower (bought)", blower, BOUGHT)
P["exhaust_y0"] = my0   # the housing's discharge collar starts on the outlet box's rear face; the duct set is drawn after the thermostats (draft 9)

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
assert PM_X0 + PM_W + 10.0 <= -P["tr_x"], "the power module plate must clear the riser trunk"
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
def grommet(gd):
    """A rubber grommet for a 1.5 plate, built about the origin along Z with the plate's mid-plane at z 0: a neck in the hole, a flange either side."""
    g_ = cq.Workplane("XY").circle(gd / 2 - 0.1).circle(gd / 2 - 3.5).extrude(tp).translate((0, 0, -tp / 2))
    for z_ in (-tp / 2 - 1.25, tp / 2):
        g_ = g_.union(cq.Workplane("XY").circle(gd / 2 + 3.0).circle(gd / 2 - 3.5).extrude(1.25).translate((0, 0, z_)))
    return g_


grommets = []
for (gx, gy, gd), gz in ((P["grommet_cord"], bt + tp / 2), (P["grommet_harness"], bt + tp / 2), (P["grommet_console"], Hb + tp / 2), (P["ds_grommet_ceil"], bt + tp / 2)):
    grommets.append(place(grommet(gd), (gx, gy, gz), (0, 0, 1)))
gx, gz, gd = P["ds_grommet_bulk"]
grommets.append(place(grommet(gd), (gx, P["front_bulk_y"] + tb / 2, gz), (0, 1, 0)))   # in the front bulkhead, for the door switch cable (draft 8)
add("grommets (bought, 5 x rubber grommets for 1.5 panels: 22 mm hole x 2, 30 mm hole x 1, 16 mm hole x 2)", compound(grommets), RUBBER)

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

# ---------------------------------------------------------------------------
# Ducts (draft 8): every duct is 1.5 mm laser-cut plate screwed with M4 button heads into the tapped edges of aluminium
# flat bar frames (30 x 8 lint box, 40 x 8 spool and nozzle, 25 x 8 hood, 50 x 8 riser trunk); no bends, no rivets.
# Part names start with "lint-box", "spool", "basket", "liner", "hood", "trunk" or "nozzle". Tapped holes are drawn at
# the thread's outside diameter (4.2), as the hinge leaves are.
# ---------------------------------------------------------------------------
BAR_T, BAR_W = P["bar_t"], P["bar_w"]
m4b10 = button_bolt(4.0, P["m4_head_d"], P["m4_head_h"], 10.0, 2.5)
m4b40 = button_bolt(4.0, P["m4_head_d"], P["m4_head_h"], 40.0, 2.5)
m3b6 = button_bolt(3.0, 5.7, 1.65, 6.0, 2.0)
m3n = nut(5.5, 2.4, 3.2)


def tapped(solid, p, n, depth=8.0):
    """A 4.2 hole into a bar from the surface point p along -n (into the bar), depth deep."""
    return solid.cut(place(cq.Workplane("XY").circle(2.1).extrude(depth + 1).translate((0, 0, -depth)), p, n))


def duct_screw(hw, solid, p_head, n, plate_t=1.5, bolt=None):
    """A button head on the plate's outer face at p_head (outward normal n), tapped into the bar behind the plate."""
    hw.append(place(bolt if bolt is not None else m4b8, p_head, n))
    L = 40.0 if bolt is m4b40 else (10.0 if bolt is m4b10 else 8.0)
    p_bar = tuple(c - plate_t * nc for c, nc in zip(p_head, n))
    return tapped(solid, p_bar, n, L - plate_t)


# --- throat liner: a rolled 1.5 mm strip between the door ring's back face and the front bulkhead, closing the gap round
# the opening (draft 8 finding: nothing bounded the throat radially, so the drum would have drawn room air through the
# 40 mm gap behind the panel). Seam at the top under a splice strip with two M3; the ring's 235 edge covers its front.
LR_I, LR_O = P["liner_ri"], P["liner_ri"] + P["liner_t"]
ly0, ly1 = P["liner_y0"], P["liner_y0"] + P["liner_len"]
liner = cq.Workplane("XZ").center(0, az).circle(LR_O).circle(LR_I).extrude(-P["liner_len"]).translate((0, ly0, 0))
liner = liner.cut(box(-1.0, 1.0, ly0 - 1, ly1 + 1, az + LR_I - 1, az + LR_O + 1))                     # 2 mm seam gap at the top
spl_half = math.degrees(20.0 / (LR_I - 0.75))
splice_l = about_drum_axis(sector_xz(0, az, LR_I - 1.5, LR_I, spl_half, P["liner_len"] - 3.0).translate((0, ly0 + 1.5, 0)), 180.0)
liner_hw = []
for th in (87.0, 93.0):   # 3 degrees each side of the seam, on the strip's centre line
    yy = (ly0 + ly1) / 2
    liner = liner.cut(radial_hole(th, yy, 3.4, LR_I - 3, LR_O + 1))
    splice_l = splice_l.cut(radial_hole(th, yy, 3.4, LR_I - 3, LR_O + 1))
    liner_hw.append(place(m3b6, radial_point(th, yy, LR_I - 1.5), radial_dir(th, outward=False)))    # head inside the throat
    liner_hw.append(place(m3n, radial_point(th, yy, LR_O), radial_dir(th, outward=True)))             # nut outside
add("liner", liner, ALU, plate=True, t=P["liner_t"])
add("liner-splice", splice_l, ALU, plate=True, t=P["liner_t"])
add("hardware-liner (bought, 2 x M3 x 6 button head, nuts)", compound(liner_hw), HARDWARE)
P["liner_flat_len"] = 2 * math.pi * (LR_I + P["liner_t"] / 2) - 2.0
lsk = cq.Workplane("XY").center(P["liner_flat_len"] / 2, P["liner_len"] / 2).rect(P["liner_flat_len"], P["liner_len"]).extrude(1)
hole_off = math.radians(3.0) * (LR_I + P["liner_t"] / 2) - 1.0                             # from each end of the strip to its hole
for xx in (hole_off, P["liner_flat_len"] - hole_off):
    lsk = lsk.cut(cq.Workplane("XY").center(xx, P["liner_len"] / 2).circle(1.7).extrude(3).translate((0, 0, -1)))
export_dxf("liner", lsk)
ssk = cq.Workplane("XY").center(20.0, (P["liner_len"] - 3.0) / 2).rect(40.0, P["liner_len"] - 3.0).extrude(1).edges("|Z").fillet(P["small_corner_r"])
for xx in (20.0 - (hole_off + 1.0), 20.0 + (hole_off + 1.0)):   # 3 degrees each side of the seam
    ssk = ssk.cut(cq.Workplane("XY").center(xx, (P["liner_len"] - 3.0) / 2).circle(1.7).extrude(3).translate((0, 0, -1)))
export_dxf("liner-splice", ssk)
cut_list.append(("liner", "1.5 mm 5052 aluminium strip, 41.3 wide", round(P["liner_flat_len"], 1), 1, "or cut to drawings/liner.dxf; roll round a 471 form, seam at the top"))
assert ly1 <= P["front_bulk_y"] - 0.2 + 1e-9 and LR_O < P["door_ring_od"] / 2 and LR_I >= P["door_ring_id"] / 2 + 0.5, "the liner sits inside the ring's edge and ends 0.2 short of the bulkhead"
assert LR_O + 0.5 <= P["lint_slot_r0"], "the liner must pass inside the lint slot"

# --- lint box: between the mid front stubs, 2 mm behind the ring bolts' tips, its back the bulkhead above 265 and a
# plate below; its top follows the liner. Hung on two M6 into the stubs' inner slots through 4 mm spacers and pulled
# against the bulkhead by six M4 from the drum side (outside the felt). 1.5 mm foam between the side bars and the bulkhead.
LB_X, LBZ0, LB_Y0 = P["lb_x"], P["lb_z0"], P["lb_y0"]
LBI = LB_X - BAR_T                                   # the side bars' inner faces (interior half width)
lb_by0, lb_by1 = LB_Y0 + tp, LB_Y0 + tp + BAR_W      # the bars, between the front plate and the back plate / the foam
LB_TOP_R = LR_O + 0.2                                # the plates' top edges and the bars' mitres follow the liner, 0.2 clear
lb_cyl = cq.Workplane("XZ").center(0, az).circle(LB_TOP_R).extrude(-200).translate((0, -50, 0))
lb_hw, lb_bars = [], []
side_z = [80.0, 160.0, 240.0, 330.0, 420.0]          # front plate screws down each side bar
for sx in (-1, 1):
    bar = box(min(sx * LBI, sx * LB_X), max(sx * LBI, sx * LB_X), lb_by0, lb_by1, LBZ0, 470.0)
    bar = bar.cut(lb_cyl)                                                         # top end mitred to the liner (cut at 43 degrees)
    for z in side_z:
        bar = duct_screw(lb_hw, bar, (sx * LB_BAR_X, LB_Y0, z), (0, -1, 0))        # front plate
    for z in (80.0, 160.0, 240.0):
        bar = duct_screw(lb_hw, bar, (sx * LB_BAR_X, lb_by1 + tp, z), (0, 1, 0))  # lower back plate, from behind
    for z in P["lb_bulk_screw_z"]:
        bar = duct_screw(lb_hw, bar, (sx * LB_BAR_X, P["front_bulk_y"] + tb, z), (0, 1, 0), plate_t=tb + P["lb_gap"], bolt=m4b10)   # from the drum side, through the foam
    bar = bar.cut(cq.Workplane("YZ").center(P["lb_hang_y"], P["lb_hang_z"]).circle(4.25).extrude(BAR_T + 2).translate((min(sx * LBI, sx * LB_X) - 1, 0, 0)))
    lb_bars.append(bar)
    # the hang bolt: M8 x 20 button head inside the box, through the bar and a 4 mm spacer into the stub's end bore, tapped M8
    # (the stub's end is a cut face: its slots do not open there, its 6.8 centre bore does). Drawn at the bore, as the feet are.
    hang = button_bolt(6.7, 13.0, 4.0, 20.0, 5.0)
    lb_hw.append(place(hang, (sx * LBI, P["lb_hang_y"], P["lb_hang_z"]), (-sx, 0, 0)))
    lb_hw.append(place(cq.Workplane("XY").circle(8.0).circle(4.25).extrude(170.0 - LB_X), (sx * LB_X, P["lb_hang_y"], P["lb_hang_z"]), (sx, 0, 0)))
bar = box(-LBI, LBI, lb_by0, lb_by1, LBZ0, LBZ0 + BAR_T)                            # bottom bar
for x in (-100.0, 100.0):
    bar = duct_screw(lb_hw, bar, (x, LB_Y0, LBZ0 + BAR_T / 2), (0, -1, 0))
for x in (-120.0, 120.0):
    bar = duct_screw(lb_hw, bar, (x, lb_by1 + tp, LBZ0 + BAR_T / 2), (0, 1, 0))
SP_H, SPZ0, SPZ1, SPW = P["sp_half"], P["sp_z0"], P["sp_z1"], P["sp_bar_w"]
SPI = SP_H - BAR_T                                                                     # the spool's interior half width (70)
SPZI0, SPZI1 = SPZ0 + BAR_T, SPZ1 - BAR_T                                              # its interior, 70 to 190, round the 130 mouth
sp_y0, sp_y1 = lb_by1 + tp, lb_by1 + tp + SPW                                          # the spool's bars, behind the back plate
spool_bottom_pts = [(-40.0, SPZ0 + BAR_T / 2), (0.0, SPZ0 + BAR_T / 2), (40.0, SPZ0 + BAR_T / 2)]
for (x, z) in spool_bottom_pts:   # M4 x 40 from the front plate through the bottom bar and the back plate into the spool's bottom bar
    bar = bar.cut(cq.Workplane("XZ").center(x, z).circle(2.25).extrude(-BAR_W - 2).translate((0, lb_by0 - 1, 0)))
lb_bars.append(bar)
add("lint-box-bars (30 x 8 aluminium flat bar: 2 sides mitred at the top, 1 bottom)", compound(lb_bars), ALU)
cut_list.append(("lint-box side bar", "flat bar 30x8 aluminum", round(462.1 - LBZ0, 1), 2, "lint box sides; top end cut at 43 degrees to meet the liner, tapped M4 on both edges, one 8.5 hole for the hang bolt"))
cut_list.append(("lint-box bottom bar", "flat bar 30x8 aluminum", round(2 * LBI, 1), 1, "lint box bottom, tapped M4 on both edges, three 4.5 through holes"))

# the box's plates: front (top edge on the liner's radius), and the lower back plate below the bulkhead, lapping its foot
lb_front_holes = [(sx * LB_BAR_X, z, P["m4_hole"]) for sx in (-1, 1) for z in side_z] + [(x, LBZ0 + BAR_T / 2, P["m4_hole"]) for x in (-100.0, 100.0)]
lb_front_holes += [(x, z, P["m4_hole"]) for (x, z) in spool_bottom_pts]
plate_xz("lint-box-front", -LB_X, LB_X, LBZ0, 470.0, LB_Y0, tp, holes=lb_front_holes, circ_cuts=[(0, az, 2 * LB_TOP_R)])
sp_side_pts = [(sx * (SP_H - BAR_T / 2), z) for sx in (-1, 1) for z in (80.0, 160.0)]
sp_top_pts = [(x, SPZ1 - BAR_T / 2) for x in (-40.0, 0.0, 40.0)]   # the spool's top bar (190 to 198)
lb_back_holes = [(sx * LB_BAR_X, z, P["m4_hole"]) for sx in (-1, 1) for z in (80.0, 160.0, 240.0)] + [(x, LBZ0 + BAR_T / 2, P["m4_hole"]) for x in (-120.0, 120.0)]
lb_back_holes += [(x, z, P["m4_hole"]) for (x, z) in sp_side_pts + sp_top_pts + spool_bottom_pts]
TH1_X, TH1_Z = P["th1_xz"]                                                               # draft 9: the exhaust thermistor's slot and bolt hole, right of the spool
TH1_NW, TH1_ND, TH1_NH = P["th1_nib"]
lb_back_holes.append((TH1_X, TH1_Z + P["th1_bolt_dz"], P["m4_hole"]))
plate_xz("lint-box-back", -LB_X, LB_X, LBZ0, P["lb_rear_plate_z1"], lb_by1, tp, holes=lb_back_holes,
         rect_cuts=[(0, (SPZI0 + SPZI1) / 2, 2 * SPI, SPZI1 - SPZI0),                   # 140 x 120 into the spool
                    (TH1_X, TH1_Z + P["th1_nib_dz"], TH1_NW + 2.0, TH1_NH + 2.0)])       # 12 x 18 for the thermistor's nib
assert TH1_X - P["th1_body"][0] / 2 > SP_H + 4.0 and TH1_X + P["th1_body"][0] / 2 < LB_BAR_X - BAR_T / 2 - 4.0, "the thermistor's body sits between the spool's bar and the box's side bar"
assert P["lb_rear_plate_z1"] > bulk_z0 and lb_by1 + tp <= P["front_bulk_y"] + 1e-9, "the lower back plate laps the bulkhead's foot and sits in front of it"
# foam between the side bars and the bulkhead above the back plate (3 mm tape, compressed to the 1.5 gap)
foam = []
for sx in (-1, 1):
    f_ = box(min(sx * LBI, sx * LB_X), max(sx * LBI, sx * LB_X), lb_by1, P["front_bulk_y"], P["lb_rear_plate_z1"], 470.0).cut(lb_cyl)
    for z in P["lb_bulk_screw_z"]:
        f_ = hole_y(f_, sx * LB_BAR_X, z)
    foam.append(f_)
add("lint-box-foam (bought, 3 mm closed-cell foam tape 8 wide, 2 x 190, compressed to 1.5)", compound(foam), FELT)

# the spool: four 40 x 8 bars as a 156 square tube from the back plate to the blower's inlet face, 6 mm foam on its rear
# edges compressed to 4 against the housing (its inlet collar's own screws are a V-107 question)
sp_bars = []
for sx in (-1, 1):
    bar = box(min(sx * SPI, sx * SP_H), max(sx * SPI, sx * SP_H), sp_y0, sp_y1, SPZ0, SPZ1)
    for z in (80.0, 160.0):
        bar = duct_screw(lb_hw, bar, (sx * (SP_H - BAR_T / 2), lb_by1, z), (0, -1, 0))   # from inside the box
    sp_bars.append(bar)
bar = box(-SPI, SPI, sp_y0, sp_y1, SPZI1, SPZ1)                                       # top bar
for (x, z) in sp_top_pts:
    bar = duct_screw(lb_hw, bar, (x, lb_by1, z), (0, -1, 0))
sp_bars.append(bar)
bar = box(-SPI, SPI, sp_y0, sp_y1, SPZ0, SPZ0 + BAR_T)                                   # bottom bar: M4 x 40 from the front plate
for (x, z) in spool_bottom_pts:
    bar = duct_screw(lb_hw, bar, (x, LB_Y0, z), (0, -1, 0), plate_t=sp_y0 - LB_Y0, bolt=m4b40)
sp_bars.append(bar)
add("spool-bars (40 x 8 aluminium flat bar: 2 x 136, 2 x 140)", compound(sp_bars), ALU)
cut_list.append(("spool side bar", "flat bar 40x8 aluminum", round(SPZ1 - SPZ0, 1), 2, "spool sides, tapped M4 on the front edge"))
cut_list.append(("spool end bar", "flat bar 40x8 aluminum", round(2 * SPI, 1), 2, "spool top and bottom, tapped M4 on the front edge"))
sp_foam = [box(min(sx * SPI, sx * SP_H), max(sx * SPI, sx * SP_H), sp_y1, P["bp_y0"], SPZ0, SPZ1) for sx in (-1, 1)]
sp_foam += [box(-SPI, SPI, sp_y1, P["bp_y0"], z0_, z0_ + BAR_T) for z0_ in (SPZ0, SPZI1)]
add("spool-foam (bought, 6 mm closed-cell foam tape 8 wide, 600, compressed to 4 on the blower plate)", compound(sp_foam), FELT)
assert abs(P["bp_y0"] - sp_y1 - P["sp_foam"]) < 1e-9, "the spool's foam fills the gap to the blower plate's front face (draft 9)"
assert SPI > 65.0 + 2.0 and SPZI1 > mz + 65.0 + 2.0, "the spool must clear the blower's 130 inlet mouth sideways and above"
assert SPZ0 == LBZ0 and LBZ0 >= e + es + 2.0, "the spool's bottom bar sits behind the box's, both 2 above the tray rails"
P["spool_area"] = 2 * SPI * (SPZI1 - SPZI0)
P["mouth_blocked"] = SPZI0 - (mz - 65.0)                                              # the spool's bottom bar covers this much of the mouth's bottom
add(f"lint-box-hardware (bought, {sum(1 for _ in lb_hw)} pieces: M4 x 8, M4 x 10 and M4 x 40 button heads, 2 x M6 x 20 button heads with 4 mm spacers and T-nuts)", compound(lb_hw), HARDWARE)

# --- lint basket: stainless mesh wrapped round two laser-cut 3 mm sector plates (a lip on the drum side of the bulkhead,
# a closed far end 2 behind the box's front plate) and clamped at each end by a 1.5 mm plate on six M3 into the tapped
# plates. The mesh's edges fold 5 mm inward at the far end and outward at the lip. It slides through the slot with 0.9
# each side; a 64 mm D-pull on the lip's tab, inside the door opening, lifts it out.
BK0, BK1, BKH, BKT = P["bk_r0"], P["bk_r1"], P["bk_half_deg"], P["bk_t"]
MT, FL = P["mesh_t"], P["bk_flange"]
EPS = math.degrees(MT / ((BK0 + BK1) / 2))                                      # the mesh's own thickness, in degrees at the mean radius
fy0 = P["bk_far_y0"]
far_plate = sector_xz(0, az, BK0, BK1, BKH, BKT).translate((0, fy0, 0))
far_flange = sector_xz(0, az, BK0, BK1, BKH, MT).cut(sector_xz(0, az, BK0 + FL, BK1 - FL, BKH - math.degrees(FL / BK0), MT + 2).translate((0, -1, 0))).translate((0, fy0 + BKT, 0))
far_clamp = sector_xz(0, az, BK0, BK1, BKH, tp).translate((0, fy0 + BKT + MT, 0))
wall_y0 = fy0 + BKT + MT + tp                                                    # the mesh walls run from the far clamp to the lip
ly_ = P["bk_lip_y0"]
wall = sector_xz(0, az, BK0 - MT, BK1 + MT, BKH + EPS, ly_ + BKT - wall_y0).cut(sector_xz(0, az, BK0, BK1, BKH, 60.0).translate((0, -1, 0))).translate((0, wall_y0, 0))
LIP0, LIP1, LIPH = 232.0, 268.5, 37.5
lip_plate = sector_xz(0, az, LIP0, LIP1, LIPH, BKT).cut(sector_xz(0, az, BK0 - MT, BK1 + MT, BKH + EPS, BKT + 2).translate((0, -1, 0)))   # the opening is the mesh's outside
lip_plate = lip_plate.union(box(-P["bk_pull_c"] / 2, P["bk_pull_c"] / 2, 0, BKT, az - LIP0 - 2.0, az - P["bk_pull_r"] + 4.0))   # the tab, into the opening
lip_plate = lip_plate.translate((0, ly_, 0))
lip_flange = sector_xz(0, az, BK0 - MT - FL, BK1 + MT + 2.4, LIPH, MT).cut(sector_xz(0, az, BK0 - MT, BK1 + MT, BKH + EPS, MT + 2).translate((0, -1, 0))).translate((0, ly_ + BKT, 0))
lip_clamp = sector_xz(0, az, LIP0, LIP1, LIPH, tp).cut(sector_xz(0, az, BK0 - MT, BK1 + MT, BKH + EPS, tp + 2).translate((0, -1, 0))).translate((0, ly_ + BKT + MT, 0))
bk_hw = []
m3b5 = button_bolt(3.0, 5.7, 1.65, 5.0, 2.0)


def bk_screws(plate, flange, clamp, y_head, pts):
    """M3 x 5 through the clamp and the mesh flange into the tapped plate; heads on the clamp's face at y_head, facing +Y."""
    for (th, r) in pts:
        a = math.radians(th)
        x, z = r * math.sin(a), az - r * math.cos(a)
        plate = plate.cut(cq.Workplane("XZ").center(x, z).circle(1.5).extrude(-BKT - 2).translate((0, y_head - BKT - MT - tp - 1, 0)))
        flange = flange.cut(cq.Workplane("XZ").center(x, z).circle(1.7).extrude(-MT - 2).translate((0, y_head - MT - tp - 1, 0)))
        clamp = clamp.cut(cq.Workplane("XZ").center(x, z).circle(1.7).extrude(-tp - 2).translate((0, y_head - tp - 1, 0)))
        bk_hw.append(place(m3b5, (x, y_head, z), (0, 1, 0)))
    return plate, flange, clamp


far_pts = [(th, BK1 - 3.2) for th in (-28.0, -10.0, 10.0, 28.0)] + [(th, BK0 + 3.3) for th in (-20.0, 20.0)]   # heads (radius 2.85) clear the mesh walls
lip_pts = [(th, BK0 - MT - 2.5) for th in (-24.0, -8.0, 8.0, 24.0)] + [(th, (BK0 + BK1) / 2) for th in (-36.7, 36.7)]   # the inner band and the two end flanges (the outer band is only 2.4 wide)
far_plate, far_flange, far_clamp = bk_screws(far_plate, far_flange, far_clamp, wall_y0, far_pts)
lip_plate, lip_flange, lip_clamp = bk_screws(lip_plate, lip_flange, lip_clamp, ly_ + BKT + MT + tp, lip_pts)
# the D-pull on the tab: two legs and a bar, M4 x 10 from the tab's back into the tapped legs
pz = az - P["bk_pull_r"] - 3.5
pull = None
for x in (-P["bk_pull_c"] / 2, P["bk_pull_c"] / 2):
    leg = cq.Workplane("XZ").center(x, pz).circle(5.0).extrude(25.0).translate((0, ly_, 0))               # XZ extrude(+) goes -Y: from the tab forward
    leg = leg.cut(cq.Workplane("XZ").center(x, pz).circle(2.1).extrude(9.0).translate((0, ly_ + 0.01, 0)))
    lip_plate = lip_plate.cut(cq.Workplane("XZ").center(x, pz).circle(2.25).extrude(-BKT - 2).translate((0, ly_ - 1, 0)))
    bk_hw.append(place(m4b10, (x, ly_ + BKT, pz), (0, 1, 0)))
    pull = leg if pull is None else pull.union(leg)
pull = pull.union(cq.Workplane("YZ").center(ly_ - 20.0, pz).circle(5.0).extrude(P["bk_pull_c"] + 10.0).translate((-P["bk_pull_c"] / 2 - 5.0, 0, 0)).edges("%CIRCLE").fillet(4.0))
add("basket-far-plate", far_plate, STEEL, plate=True, t=BKT)
add("basket-far-clamp", far_clamp, STEEL, plate=True, t=tp)
add("basket-lip-plate", lip_plate, STEEL, plate=True, t=BKT)
add("basket-lip-clamp", lip_clamp, STEEL, plate=True, t=tp)
add("basket-mesh (bought, stainless 18 x 16 mesh strip, 42 wide, 350 long, wrapped and folded 5 at each edge)", far_flange.union(wall).union(lip_flange), HARDWARE)
add("basket-pull (bought, D-pull, 64 mm centres, 25 projection)", pull, HARDWARE)
add(f"hardware-basket (bought, {len(bk_hw) - 2} x M3 x 5 button head into the tapped plates, 2 x M4 x 10 button head into the pull)", compound(bk_hw), HARDWARE)
# flat patterns in world XZ coordinates about the drum axis, as the bulkheads' are
for nm, sk_ in (("basket-far-plate", sector_xy(0, az, BK0, BK1, BKH, 1)), ("basket-far-clamp", sector_xy(0, az, BK0, BK1, BKH, 1)),
                ("basket-lip-clamp", sector_xy(0, az, LIP0, LIP1, LIPH, 1).cut(sector_xy(0, az, BK0 - MT, BK1 + MT, BKH + EPS, 3).translate((0, 0, -1))))):
    pts = far_pts if "far" in nm else lip_pts
    for (th, r) in pts:
        a = math.radians(th)
        sk_ = sk_.cut(cq.Workplane("XY").center(r * math.sin(a), az - r * math.cos(a)).circle(1.5 if nm.endswith("plate") else 1.7).extrude(3).translate((0, 0, -1)))
    export_dxf(nm, sk_)
sk_ = sector_xy(0, az, LIP0, LIP1, LIPH, 1).cut(sector_xy(0, az, BK0 - MT, BK1 + MT, BKH + EPS, 3).translate((0, 0, -1)))
sk_ = sk_.union(cq.Workplane("XY").center(0, az + (-LIP0 - 2.0 - P["bk_pull_r"] + 4.0) / 2).rect(P["bk_pull_c"], LIP0 + 2.0 - P["bk_pull_r"] + 4.0).extrude(1))
for (th, r) in lip_pts:
    a = math.radians(th)
    sk_ = sk_.cut(cq.Workplane("XY").center(r * math.sin(a), az - r * math.cos(a)).circle(1.5).extrude(3).translate((0, 0, -1)))
for x in (-P["bk_pull_c"] / 2, P["bk_pull_c"] / 2):
    sk_ = sk_.cut(cq.Workplane("XY").center(x, pz).circle(2.25).extrude(3).translate((0, 0, -1)))
export_dxf("basket-lip-plate", sk_)
P["basket_wall_area"] = math.radians(2 * BKH) * (BK1 + MT) * (P["front_bulk_y"] - wall_y0)     # the outer wall inside the box, facing down
P["lint_slot_area"] = math.radians(2 * P["lint_slot_half_deg"]) / 2 * (P["lint_slot_r1"] ** 2 - P["lint_slot_r0"] ** 2)
assert BK0 - MT >= P["lint_slot_r0"] + 0.8 and BK1 + MT <= P["lint_slot_r1"] - 0.8, "the basket passes the slot with 0.8 or more each side"
assert LIP1 + 1.0 <= P["ring_id"] / 2 and LIP0 >= P["door_opening_d"] / 2 + 1.0, "the lip rides inside the ring's bore and outside the opening when it is pulled"
assert fy0 >= LB_Y0 + tp + 0.5 and ly_ >= P["front_bulk_y"] + tb - 1e-9, "the basket's far end clears the box's front plate; its lip sits on the bulkhead's drum side"
assert BK0 - MT > LB_TOP_R + 1.0, "the basket's inner wall clears the liner"

# --- riser: a hood over the heat module's collar (25 x 8 bars between two plates, under the mid rear cross rail), a trunk
# of two 50 x 8 bars between two plates standing on the hood's top plate behind the rear bulkhead, and a nozzle of 40 x 8
# bars from the trunk's front plate to the bulkhead's inlet field. The module slides out under the hood (nothing of the
# riser reaches below 230). Hood heads on top sit clear of the cross rail's footprint.
HX, HBW, RZ0 = P["hood_x"], P["hood_bar_w"], P["riser_z0"]
HY0, HY1 = P["hood_y0"], P["tr_y0"] + tp + P["tr_bar_w"] + tp                 # the hood runs back to the trunk's rear face
hz0, hz1 = RZ0 + tp, RZ0 + tp + HBW                                            # the hood's bars (231.5 to 256.5)
HXI = HX - BAR_T                                                               # interior half width (167)
TX, TBW, TY0 = P["tr_x"], P["tr_bar_w"], P["tr_y0"]
TXI = TX - BAR_T                                                               # 122
ty0b, ty1b = TY0 + tp, TY0 + tp + TBW                                          # the trunk's bars (654 to 704)
TZ1 = az + P["inlet_above_axis"] + P["inlet_h"] + P["tr_over"]                 # 831.5: the top bar above the nozzle's top bar (816.5)
rs_hw, hood_bars, trunk_bars, nz_bars = [], [], [], []
hood_side_pts = [(sx * (HX - BAR_T / 2), y) for sx in (-1, 1) for y in (500.0, 580.0, 690.0)]
hood_end_pts = [(x, HY0 + BAR_T / 2) for x in (-120.0, 120.0)] + [(x, HY1 - BAR_T / 2) for x in (-150.0, 150.0)]   # rear ones outside the trunk's plates
for sx in (-1, 1):
    bar = box(min(sx * HXI, sx * HX), max(sx * HXI, sx * HX), HY0, HY1, hz0, hz1)
    for (x, y) in hood_side_pts:
        if (x > 0) == (sx > 0):
            bar = duct_screw(rs_hw, bar, (x, y, RZ0), (0, 0, -1))                # bottom plate, from below
            bar = duct_screw(rs_hw, bar, (x, y, hz1 + tp), (0, 0, 1))            # top plate, from above
    hood_bars.append(bar)
for (y0_, y1_) in ((HY0, HY0 + BAR_T), (HY1 - BAR_T, HY1)):
    bar = box(-HXI, HXI, y0_, y1_, hz0, hz1)
    for (x, y) in hood_end_pts:
        if y0_ <= y <= y1_:
            bar = duct_screw(rs_hw, bar, (x, y, RZ0), (0, 0, -1))
            bar = duct_screw(rs_hw, bar, (x, y, hz1 + tp), (0, 0, 1))
    hood_bars.append(bar)
add("hood-bars (25 x 8 aluminium flat bar: 2 sides, front, rear)", compound(hood_bars), ALU)
cut_list.append(("hood side bar", "flat bar 25x8 aluminum", round(HY1 - HY0, 1), 2, "hood sides, tapped M4 on both edges"))
cut_list.append(("hood end bar", "flat bar 25x8 aluminum", round(2 * HXI, 1), 2, "hood front and rear, tapped M4 on both edges"))
hood_holes = [(x, y, P["m4_hole"]) for (x, y) in hood_side_pts + hood_end_pts]
trunk_foot_pts = [(sx * (TX - BAR_T / 2), y) for sx in (-1, 1) for y in (665.0, 688.0)]   # the trunk's side bars stand on the hood's top plate
plate_xy("hood-bottom", -HX, HX, HY0, HY1, RZ0, tp, holes=hood_holes, circ_cuts=[(0, P["hm_collar_y"], P["hm_collar_d"] + 3.0)])
plate_xy("hood-top", -HX, HX, HY0, HY1, hz1, tp, holes=hood_holes + [(x, y, P["m4_hole"]) for (x, y) in trunk_foot_pts],
         rect_cuts=[(0, (ty0b + ty1b) / 2, 2 * TXI, TBW)])
P["hood_area"] = 2 * HXI * HBW
assert hz1 + tp <= bt - e - 2.0 + 1e-9, "the hood passes 2 under the mid rear cross rail"
for (x, y) in hood_side_pts + hood_end_pts:   # the heads on top must miss the cross rail
    assert not (ry - 4.0 <= y <= ry + e + 4.0), f"hood screw at Y {y} under the mid rear cross rail"
assert HY1 + 2.2 + 2.0 <= D - e, "the hood and the trunk's rear heads must clear the rear end rail"
assert HXI * 2 >= 2 * P["hm_collar_flange_d"] / 2 + 20.0, "the hood covers the collar's flange with margin"
# the hood's gasket: a foam ring glued under the bottom plate round the collar's hole; the module's collar rim brushes it
gk = (cq.Workplane("XY").center(0, P["hm_collar_y"]).circle(P["hood_gasket_od"] / 2).circle(P["hm_collar_d"] / 2).extrude(P["hood_gasket_t"])
      .translate((0, 0, RZ0 - P["hood_gasket_t"])))
add("hood-gasket (bought, 3 mm foam ring 150 x 125, glued under the hood's bottom plate)", gk, FELT)
assert HY0 <= P["hm_collar_y"] - P["hood_gasket_od"] / 2, "the hood must cover the gasket ring"
# the trunk
trunk_side_z = (320.0, 440.0, 560.0, 680.0, 800.0)
NZ0, NZ1 = P["nz_z"]
NX, NBW = P["nz_x"], P["nz_bar_w"]
NXI = NX - BAR_T                                                               # 106
nz_in_z0, nz_in_z1 = NZ0 + BAR_T, NZ1 - BAR_T                                  # 666.5 to 808.5
for sx in (-1, 1):
    bar = box(min(sx * TXI, sx * TX), max(sx * TXI, sx * TX), ty0b, ty1b, hz1 + tp, TZ1)
    for z in trunk_side_z:
        bar = duct_screw(rs_hw, bar, (sx * (TX - BAR_T / 2), TY0, z), (0, -1, 0))        # front plate
        bar = duct_screw(rs_hw, bar, (sx * (TX - BAR_T / 2), ty1b + tp, z), (0, 1, 0))   # rear plate
    for y in (665.0, 688.0):
        bar = duct_screw(rs_hw, bar, (sx * (TX - BAR_T / 2), y, hz1), (0, 0, -1))         # into the bar's foot, from inside the hood
    trunk_bars.append(bar)
bar = box(-TXI, TXI, ty0b, ty1b, TZ1 - BAR_T, TZ1)                                       # top bar
for x in (-80.0, 0.0, 80.0):
    bar = duct_screw(rs_hw, bar, (x, TY0, TZ1 - BAR_T / 2), (0, -1, 0))
    bar = duct_screw(rs_hw, bar, (x, ty1b + tp, TZ1 - BAR_T / 2), (0, 1, 0))
trunk_bars.append(bar)
add("trunk-bars (50 x 8 aluminium flat bar: 2 sides, 1 top)", compound(trunk_bars), ALU)
cut_list.append(("trunk side bar", "flat bar 50x8 aluminum", round(TZ1 - hz1 - tp, 1), 2, "riser trunk sides, tapped M4 on both edges and the foot"))
cut_list.append(("trunk top bar", "flat bar 50x8 aluminum", round(2 * TXI, 1), 1, "riser trunk top, tapped M4 on both edges"))
trunk_holes = [(sx * (TX - BAR_T / 2), z, P["m4_hole"]) for sx in (-1, 1) for z in trunk_side_z] + [(x, TZ1 - BAR_T / 2, P["m4_hole"]) for x in (-80.0, 0.0, 80.0)]
nz_trunk_pts = [(sx * (NX - BAR_T / 2), z) for sx in (-1, 1) for z in (700.0, 775.0)] + [(x, z) for x in (-60.0, 0.0, 60.0) for z in (NZ0 + BAR_T / 2, NZ1 - BAR_T / 2)]
plate_xz("trunk-front", -TX, TX, hz1 + tp, TZ1, TY0, tp, holes=trunk_holes + [(x, z, P["m4_hole"]) for (x, z) in nz_trunk_pts],
         rect_cuts=[(0, (nz_in_z0 + nz_in_z1) / 2, 2 * NXI, nz_in_z1 - nz_in_z0)])
plate_xz("trunk-rear", -TX, TX, hz1 + tp, TZ1, ty1b, tp, holes=trunk_holes)
P["riser_area"] = 2 * TXI * TBW
assert TY0 >= ry + e + 1.0 - 1e-9, "the trunk's front plate stands 1 behind the mid rear cross rail"
assert TZ1 + 2.0 <= Hb - e, "the trunk ends under the top rear cross rail"
# the nozzle: 40 x 8 bars from the bulkhead's back face (1 mm foam) to the trunk's front plate; M4 from the drum side
# through the bulkhead and from inside the trunk through its front plate
nz_y0, nz_y1 = P["rear_bulk_y"] + tb + P["nz_foam"], TY0
assert abs(nz_y1 - nz_y0 - NBW) < 1e-9, "the nozzle's bars span the bulkhead to the trunk exactly"
for sx in (-1, 1):
    bar = box(min(sx * NXI, sx * NX), max(sx * NXI, sx * NX), nz_y0, nz_y1, NZ0, NZ1)
    for (x, z) in nz_trunk_pts:
        if abs(x) > NXI and (x > 0) == (sx > 0):
            bar = duct_screw(rs_hw, bar, (x, TY0 + tp, z), (0, 1, 0))                                    # from inside the trunk
    for (x, z) in nz_bulk_pts:
        if abs(x) > NXI and (x > 0) == (sx > 0):
            bar = duct_screw(rs_hw, bar, (x, P["rear_bulk_y"], z), (0, -1, 0), plate_t=tb + P["nz_foam"], bolt=m4b10)   # from the drum side
    nz_bars.append(bar)
for (z0_, z1_) in ((NZ0, NZ0 + BAR_T), (NZ1 - BAR_T, NZ1)):
    bar = box(-NXI, NXI, nz_y0, nz_y1, z0_, z1_)
    for (x, z) in nz_trunk_pts:
        if z0_ <= z <= z1_:
            bar = duct_screw(rs_hw, bar, (x, TY0 + tp, z), (0, 1, 0))
    for (x, z) in nz_bulk_pts:
        if z0_ <= z <= z1_:
            bar = duct_screw(rs_hw, bar, (x, P["rear_bulk_y"], z), (0, -1, 0), plate_t=tb + P["nz_foam"], bolt=m4b10)
    nz_bars.append(bar)
add("nozzle-bars (40 x 8 aluminium flat bar: 2 sides, top, bottom)", compound(nz_bars), ALU)
cut_list.append(("nozzle side bar", "flat bar 40x8 aluminum", round(NZ1 - NZ0, 1), 2, "inlet nozzle sides, tapped M4 on both edges"))
cut_list.append(("nozzle end bar", "flat bar 40x8 aluminum", round(2 * NXI, 1), 2, "inlet nozzle top and bottom, tapped M4 on both edges"))
nz_foam = [box(min(sx * NXI, sx * NX), max(sx * NXI, sx * NX), P["rear_bulk_y"] + tb, nz_y0, NZ0, NZ1) for sx in (-1, 1)]
nz_foam += [box(-NXI, NXI, P["rear_bulk_y"] + tb, nz_y0, z0_, z0_ + BAR_T) for z0_ in (NZ0, NZ1 - BAR_T)]
nz_foam = [f_ for f_ in nz_foam]
for (x, z) in nz_bulk_pts:
    nz_foam = [hole_y(f_, x, z) for f_ in nz_foam]
add("nozzle-foam (bought, 2 mm closed-cell foam tape 8 wide, 900, compressed to 1 on the bulkhead)", compound(nz_foam), FELT)
P["nozzle_area"] = 2 * NXI * (nz_in_z1 - nz_in_z0)
assert -NXI < -P["inlet_w"] / 2 - 4.0 and nz_in_z0 < az + P["inlet_above_axis"] - P["inlet_hole_d"] / 2 - 4.0 and nz_in_z1 > az + P["inlet_above_axis"] + 8 * P["inlet_pitch"] + P["inlet_hole_d"] / 2 + 4.0, "the nozzle surrounds the hole field with 4 mm to spare"
add(f"riser-hardware (bought, {len(rs_hw)} x M4 x 8 and M4 x 10 button heads)", compound(rs_hw), HARDWARE)

# --- door switch (draft 8): a plunger switch behind the front upper panel, 45 degrees right of bottom on the ring bolts'
# radius; the closed door's disc presses the plunger (drawn pressed, 3 mm travel). Two M4 into its tapped ears outside the
# ring. Envelope: the listed two-contact dryer door switch of uci-spec section 13 is measured at V-115.
bw_, bd_, bh_ = P["ds_body"]
ds_body = box(-bw_ / 2, bw_ / 2, 0, bd_, -bh_ / 2, bh_ / 2).rotate((0, 0, 0), (0, 1, 0), 90.0 + P["ds_angle_deg"]).translate((272.5 * DS_U[0], 0, az + 272.5 * DS_U[1]))
ds_body = ds_body.union(cq.Workplane("XZ").center(*DS_P).circle(P["ds_plunger_d"] / 2).extrude(12.0).translate((0, 1.0, 0)))   # plunger to Y -11, on the disc's back face
for (x, z) in DS_M:
    ds_body = ds_body.cut(cq.Workplane("XZ").center(x, z).circle(2.1).extrude(-9.0).translate((0, -1.0, 0)))
add("door-switch (bought, two-contact plunger switch, envelope)", ds_body, BOUGHT)
add("hardware-door-switch (bought, 2 x M4 x 8 button head into the switch's tapped ears)",
    compound([place(m4b8, (x, -tp, z), (0, -1, 0)) for (x, z) in DS_M]), HARDWARE)
assert P["ds_r"] > P["door_ring_id"] / 2 + 10 and P["ds_r"] < P["door_disc_d"] / 2 - 8 and all(math.hypot(x, z - az) > P["door_ring_od"] / 2 + 5 for (x, z) in DS_M), "plunger under the disc, inside the ring; ears outside the ring"
assert DS_P[0] > LB_X + 10.0, "the switch sits clear of the lint box"

# --- air-proving switch PS1 (draft 8): on a 20x20x2 angle bracket on the base pan at the right front, in front of the
# blower's outlet box; its tube to the blower outlet is a V-205 question. Envelope only.
px_, py_ = P["ps1_xy"]
ps_brk = angle_x(px_ - 30.0, px_ + 30.0, py_ + 10.0, -1, 0.0, +1)                        # vertical leg at Y 78 to 80, foot forward on the pan
for (x, y) in ps1_pts:
    ps_brk = ps_brk.cut(cq.Workplane("XY").center(x, y).circle(P["m6_hole"] / 2).extrude(A_T + 2).translate((0, 0, -1)))
ps_hw = [place(hex_bolt_m6(), (x, y, A_T), (0, 0, 1)) for (x, y) in ps1_pts] + [place(nut(P["m6_nut_af"], P["m6_nut_h"], 6.2), (x, y, -P["t_base"]), (0, 0, -1)) for (x, y) in ps1_pts]
ps_body = box(px_ - 30.0, px_ + 30.0, py_ + 10.0, py_ + 38.0, 0.0, 60.0)
for x in (px_ - 15.0, px_ + 15.0):
    ps_brk = hole_y(ps_brk, x, 12.0)
    ps_body = ps_body.cut(cq.Workplane("XZ").center(x, 12.0).circle(2.1).extrude(-9.0).translate((0, py_ + 10.0 - 1.0, 0)))
    ps_hw.append(place(m4b8, (x, py_ + 10.0 - A_T, 12.0), (0, -1, 0)))
add("ps1-bracket (angle 20x20x2, 60)", ps_brk, ALU)
cut_list.append(("ps1-bracket", "angle 20x20x2 aluminum", 60, 1, "air-proving switch bracket, on the base pan"))
add("ps1-air-proving-switch (bought, envelope)", ps_body, BOUGHT)
add("hardware-ps1 (bought, 2 x M6 x 12 hex, nuts, through the base pan; 2 x M4 x 8 button head into the switch)", compound(ps_hw), HARDWARE)

# --- exhaust thermostats (draft 8): TF2 (thermal fuse), T_HI and T_LO (cycling) on the blower's outlet box, disc type on
# 54 x 14 brackets, each with two screws into the housing (the kit's screws; the housing is measured at V-107)
tf_hw = []
tf_sols = []
oz = OB_Z1                                                                              # the outlet box's top face (206, draft 9)
for x in P["tf_x"]:
    br_ = box(x - 7.0, x + 7.0, 123.0, 177.0, oz, oz + 2.0)
    bd2 = box(x - 11.0, x + 11.0, 139.0, 161.0, oz + 2.0, oz + 15.0)
    t_ = br_.union(bd2)
    for yy in (130.0, 170.0):
        t_ = t_.cut(cq.Workplane("XY").center(x, yy).circle(2.25).extrude(5).translate((0, 0, oz - 1)))
        blower = blower.cut(cq.Workplane("XY").center(x, yy).circle(2.1).extrude(9).translate((0, 0, oz - 8)))
        tf_hw.append(place(m4b8, (x, yy, oz + 2.0), (0, 0, 1)))
    tf_sols.append(t_)
add("exhaust-thermostats (bought, TF2 thermal fuse, T_HI and T_LO cycling thermostats, envelopes on the blower outlet)", compound(tf_sols), BOUGHT)
add("hardware-exhaust-thermostats (bought, 6 x M4 x 8 button head into the housing)", compound(tf_hw), HARDWARE)

# ---------------------------------------------------------------------------
# Draft 9: the blower plate, the exhaust set, the two chassis sensors, the blanked entries, the cable clamps
# ---------------------------------------------------------------------------
# --- the blower plate: a 1.5 mm steel plate standing on the base pan in front of the housing, with the spool's bore cut
# through it, carrying the housing on its own screws (the bought housing's pattern, V-107; drawn on a nominal 180 x 120)
# and standing on two 20x20x2 angle feet bolted through the pan. The spool's foam lands on its front face.
BP_X, BP_Z1, BP_Y0 = P["bp_x"], P["bp_z1"], P["bp_y0"]
bp_screw_pts = [(x, z) for (x, z) in P["bp_screws"]]
bp_leg_pts = [(sx * x, 10.0) for sx in (-1, 1) for x in (70.0, 110.0)]                 # M4 through the plate into the feet's vertical legs
bp_holes = [(x, z, P["m4_hole"]) for (x, z) in bp_screw_pts + bp_leg_pts]
plate_xz("blower-plate", -BP_X, BP_X, 0.0, BP_Z1, BP_Y0, tp, holes=bp_holes,
         rect_cuts=[(0, (SPZI0 + SPZI1) / 2, 2 * SPI, SPZI1 - SPZI0)])                   # the spool's bore, 140 x 120
bp_hw = []
for (x, z) in bp_screw_pts:                                                             # housing screws from the plate's front, into the housing's bosses
    blower = blower.cut(cq.Workplane("XZ").center(x, z).circle(2.1).extrude(-9.0).translate((0, P["blower_y0"] - 1.0, 0)))
    bp_hw.append(place(m4b8, (x, BP_Y0, z), (0, -1, 0)))
    assert math.hypot(x, z - mz) < P["blower_d"] / 2 - 2.0 and abs(x) > SP_H + P["m4_head_d"] / 2 + 2.0, "the housing's screws sit on its face, clear of the spool's foam"
bp_feet = []
for sx in (-1, 1):
    x0_, x1_ = sorted((sx * P["bp_foot_x"][0], sx * P["bp_foot_x"][1]))
    foot = angle_x(x0_, x1_, BP_Y0, -1, 0.0, +1)                                         # vertical leg on the plate's front face, foot forward on the pan
    for (x, z) in bp_leg_pts:
        if x0_ <= x <= x1_:
            foot = hole_y(foot, x, z)
            bp_hw.append(place(m4b8, (x, P["blower_y0"], z), (0, 1, 0)))                 # head on the plate's back, below the housing
            bp_hw.append(place(m4n_, (x, BP_Y0 - A_T, z), (0, -1, 0)))
    for (x, y) in bp_foot_pts:
        if x0_ <= x <= x1_:
            foot = foot.cut(cq.Workplane("XY").center(x, y).circle(P["m6_hole"] / 2).extrude(A_T + 2).translate((0, 0, -1)))
            bp_hw.append(place(hex_bolt_m6(), (x, y, -P["t_base"]), (0, 0, -1)))          # head under the pan
            bp_hw.append(place(nut(P["m6_nut_af"], P["m6_nut_h"], 6.2), (x, y, A_T), (0, 0, 1)))
    bp_feet.append(foot)
add("blower-plate-feet (angle 20x20x2, 2 x 90)", compound(bp_feet), ALU)
cut_list.append(("blower-plate feet", "angle 20x20x2 aluminum", round(P["bp_foot_x"][1] - P["bp_foot_x"][0], 1), 2, "blower plate feet, on the base pan"))
add("hardware-blower-plate (bought, 4 x M4 x 8 button head into the housing, 4 x M4 x 8 and nuts into the feet, 4 x M6 x 12 hex, washers, nuts through the base pan)", compound(bp_hw), HARDWARE)
assert BP_X + 4.0 < 150.0 and BP_Z1 + 10.0 < bt - e and P["bp_foot_x"][1] + 10.0 < 150.0, "the blower plate and its feet clear the tray rails and the bay ceiling's rails"
assert BP_Y0 - A_L > lb_by1 + tp + 2.0 or SPZ0 > A_L + 2.0, "the feet lie under the spool, clear of the lint box's back plate"

# --- the exhaust set: the housing's own 102 discharge collar on the outlet box (the interface flange of design-rules 3.2),
# a catalog 4 in aluminium pipe over it, along the bay floor's right side and through the rear lower panel's 106 port,
# 50 proud as the vent hose spigot; two worm-drive clamps (one on the collar, one bearing on the panel from inside); a
# tap for the air-proving switch on the pipe's top, a barb fitting and the tube down to PS1
EX_X, EX_Z, EX_D = P["exhaust_x"], P["exhaust_z"], P["exhaust_d"]
EX_R, EX_WALL = EX_D / 2, P["exhaust_wall"]
EX_Y0 = P["exhaust_y0"]
blower = blower.union(cq.Workplane("XZ").center(EX_X, EX_Z).circle(EX_R - EX_WALL - 0.5).circle(EX_R - EX_WALL - 1.5)
                      .extrude(-P["exhaust_collar_len"]).translate((0, EX_Y0, 0)))         # the collar: 1 mm wall, 0.5 inside the pipe's bore
parts[[n for n, *_ in parts].index("blower (bought)")] = ("blower (bought)", blower, BOUGHT, False, None)
EX_Y1 = D + tp + P["exhaust_proud"]                                                        # the spigot's end, outside the rear lower panel
EX_LEN = EX_Y1 - (EX_Y0 + 2.0)
exh = cq.Workplane("XZ").center(EX_X, EX_Z).circle(EX_R).circle(EX_R - EX_WALL).extrude(-EX_LEN).translate((0, EX_Y0 + 2.0, 0))
exh = exh.cut(cq.Workplane("XY").center(EX_X, P["exhaust_tap_y"]).circle(3.25).extrude(20).translate((0, 0, EX_Z + EX_R - 10)))   # the tap, 6.5
add("exhaust-duct (bought, 4 in aluminium pipe, 102 x 1, cut to length, one 6.5 hole for the tap)", exh, DUCT)
cut_list.append(("exhaust duct (bought)", "4 in (102) aluminium pipe", round(EX_LEN, 1), 1, "from 2 past the housing's collar to 50 proud of the rear lower panel; one 6.5 hole on top at Y 300 for the tap"))
clamps_ = []
for yc in (EX_Y0 + 8.0, D - P["clamp_w"]):                                                 # over the collar joint; inside the panel, bearing on it
    ring_ = cq.Workplane("XZ").center(EX_X, EX_Z).circle(EX_R + 0.7).circle(EX_R).extrude(-P["clamp_w"]).translate((0, yc, 0))
    ring_ = ring_.union(box(EX_X - 11.0, EX_X + 11.0, yc, yc + P["clamp_w"], EX_Z + EX_R + 0.7, EX_Z + EX_R + 10.7))   # the worm screw housing, on top
    clamps_.append(ring_)
add("exhaust-clamps (bought, 2 x worm-drive hose clamps for 102, envelopes)", compound(clamps_), HARDWARE)
tap_z = EX_Z + EX_R                                                                        # the pipe's top at the tap
barb = hexagon(10.0, 5.0).translate((EX_X, P["exhaust_tap_y"], tap_z))                      # the fitting's hex on the pipe
barb = barb.union(cq.Workplane("XY").center(EX_X, P["exhaust_tap_y"]).circle(2.5).extrude(15.0).translate((0, 0, tap_z + 5.0)))   # the barb, 5 mm, for the tube
barb = barb.union(cq.Workplane("XY").center(EX_X, P["exhaust_tap_y"]).circle(3.0).extrude(9.0).translate((0, 0, tap_z - 9.0)))    # the thread through the hole, its nut inside
barb = barb.union(hexagon(10.0, 4.0).translate((EX_X, P["exhaust_tap_y"], tap_z - 1.5 - 4.0)))                                  # the locknut under the pipe's curved wall (1.5 down at the hex's corners)
add("exhaust-tap-barb (bought, 1/8 NPT or M6 brass barb fitting with a locknut, 5 mm barb, envelope)", barb, HARDWARE)
PS1_PORT = (px_, py_ + 24.0, 60.0)                                                         # the switch's port on top of its body (V-205 sets which port)
tube_pts = [(EX_X, P["exhaust_tap_y"], tap_z + 20.0), (EX_X, P["exhaust_tap_y"], 240.0), (PS1_PORT[0], PS1_PORT[1], 240.0), PS1_PORT]   # from the barb's end (the tube slides over it)
tube_path = cq.Workplane("XY").polyline(tube_pts)
ps1_tube = cq.Workplane("XY").workplane(offset=tube_pts[0][2]).center(tube_pts[0][0], tube_pts[0][1]).circle(3.0).sweep(tube_path, transition="round")
add("ps1-tube (bought, 6 mm silicone tube from the tap to PS1, drawn on its route)", ps1_tube, RUBBER)
assert tube_pts[1][2] > oz + 15.0 + P["m4_head_h"] + 10.0 and tube_pts[1][2] < bt - e - 10.0, "the tube passes over the thermostats, under the bay ceiling's rails"
assert PS1_PORT[1] < P["blower_y0"] + 26 - 3.0, "the tube's drop sits in front of the outlet box"
assert EX_X - EX_R > P["tray_w"] / 2 + 5.0, "the pipe runs beside the heat module's tray"

# --- the exhaust thermistor TH1 (uci-spec 7.1, TEMP_EXH): an appliance-market exhaust thermistor on the bay side of the
# lint box's back plate, right of the spool, its sensing nib through a slot into the box; one M4 x 20 from inside the box
# through the plate and the body, nut on the body. Envelope; the bought part's slot and hole are V-112.
TB_W, TB_D, TB_H = P["th1_body"]
th1_y0 = lb_by1 + tp                                                                      # the back plate's bay-side face
th1 = box(TH1_X - TB_W / 2, TH1_X + TB_W / 2, th1_y0, th1_y0 + TB_D, TH1_Z - TB_H / 2, TH1_Z + TB_H / 2)
th1 = th1.union(box(TH1_X - TH1_NW / 2, TH1_X + TH1_NW / 2, th1_y0 - TH1_ND, th1_y0, TH1_Z + P["th1_nib_dz"] - TH1_NH / 2, TH1_Z + P["th1_nib_dz"] + TH1_NH / 2))
th1 = hole_y(th1, TH1_X, TH1_Z + P["th1_bolt_dz"])
th1 = th1.union(box(TH1_X - 4.0, TH1_X + 4.0, th1_y0 + TB_D, th1_y0 + TB_D + 8.0, TH1_Z - 12.0, TH1_Z + 4.0))   # two 6.3 mm spade terminals, below the bolt's nut
add("th1-exhaust-thermistor (bought, 10 k NTC appliance thermistor, envelope)", th1, BOUGHT)
m4b20 = button_bolt(4.0, P["m4_head_d"], P["m4_head_h"], 20.0, 2.5)
add("hardware-th1 (bought, 1 x M4 x 20 button head from inside the lint box, nut on the body)",
    compound([place(m4b20, (TH1_X, lb_by1, TH1_Z + P["th1_bolt_dz"]), (0, -1, 0)), place(m4n_, (TH1_X, th1_y0 + TB_D, TH1_Z + P["th1_bolt_dz"]), (0, 1, 0))]), HARDWARE)
assert th1_y0 + TB_D + 8.0 < BP_Y0 - 4.0, "the thermistor and its terminals sit in front of the blower plate"
assert th1_y0 - TH1_ND > lb_by0 + 2.0, "the nib stays inside the box"

# --- the moisture bar set (uci-spec 7.2, MOIST): an appliance-market sensor bar set (two stainless strips on an insulating
# base) on the front bulkhead's drum side, right of the lint slot, inside the ring bore, along the tangent at 58 degrees
# right of bottom; two M4 x 16 from the drum side through its tabs, nuts in the front gap; its two terminals through a 16
# hole to the front gap. Envelope; the bought set's footprint and tab holes are V-112.
MS_L, MS_W, MS_T_ = P["ms_len"], P["ms_w"], P["ms_t"]
ms_y0 = P["front_bulk_y"] + tb                                                             # the bulkhead's drum-side face
ms = box(-MS_L / 2, MS_L / 2, 0.0, MS_T_, -MS_W / 2, MS_W / 2)
for k in (-P["ms_tab"], P["ms_tab"]):
    ms = ms.cut(cq.Workplane("XZ").center(k, 0).circle(2.25).extrude(-MS_T_ - 2).translate((0, -1, 0)))
ms = ms.cut(box(-8.0, 8.0, -1.0, 2.0, -9.0, 9.0))                                           # the terminals' recess over the bulkhead's hole
ms = ms.rotate((0, 0, 0), (0, 1, 0), -P["ms_angle_deg"]).translate((MS_C[0], ms_y0, MS_C[1]))
add("moisture-bars (bought, dryer moisture sensor bar set, two stainless strips on an insulating base, envelope)", ms, BOUGHT)
m4b16 = button_bolt(4.0, P["m4_head_d"], P["m4_head_h"], 16.0, 2.5)
ms_hw = [place(m4b16, (x, ms_y0 + MS_T_, z), (0, 1, 0)) for (x, z) in MS_PTS] + [place(m4n_, (x, P["front_bulk_y"], z), (0, -1, 0)) for (x, z) in MS_PTS]
add("hardware-moisture-bars (bought, 2 x M4 x 16 button head from the drum side, nuts in the front gap)", compound(ms_hw), HARDWARE)
for (x, z) in MS_PTS:
    assert math.hypot(x, z - az) > P["liner_ri"] + P["liner_t"] + P["m4_nut_af"] / 2 + 2.0, "the bars' nuts clear the throat liner"
assert ms_y0 + MS_T_ <= y0d + 20.0, "the bar set reaches into the drum's mouth no further than the baffles' ends"   # inside the ring bore it touches the load, which is the point

# --- the two blanked entries in the rear lower panel: 60 x 44 x 1.5 plates inside the panel on two M4 x 8, heads outside
blank_hw = []
for i, (x, z, d) in enumerate(ENTRIES):
    if i == 0:   # the gas entry's blank is the drawn part; the condensate drain's is the same plate, cut twice
        blank0 = plate_xz("entry-blank", x - P["blank_w"] / 2, x + P["blank_w"] / 2, z - P["blank_h"] / 2, z + P["blank_h"] / 2, D - tp, tp,
                          holes=[(x + k, z, P["m4_hole"]) for k in (-P["blank_dx"], P["blank_dx"])])
    else:
        add("entry-blank-2 (the second entry-blank, cut two to drawings/entry-blank.dxf; on the condensate drain)", blank0.translate((x - ENTRIES[0][0], 0, z - ENTRIES[0][1])), STEEL)
    for k in (-P["blank_dx"], P["blank_dx"]):
        blank_hw.append(place(m4b8, (x + k, D + tp, z), (0, 1, 0)))                          # head outside the panel
        blank_hw.append(place(m4n_, (x + k, D - tp, z), (0, -1, 0)))                        # nut on the blank's inside face
add("hardware-entry-blanks (bought, 4 x M4 x 8 button head, nuts)", compound(blank_hw), HARDWARE)

# --- the cable clamps for the bay harness: four nylon P-clips for a 12 mm bundle on the base pan's left side (draft 8
# placed their holes), M4 x 8 through the clip and the pan, nut under the pan. Envelopes.
clip_sols, clip_hw = [], []
for (x, y) in P["clamp_pts"]:
    tab = box(x - 8.0, x + 8.0, y - 5.0, y + 5.0, 0.0, 1.5)
    tab = tab.cut(cq.Workplane("XY").center(x, y).circle(2.25).extrude(4).translate((0, 0, -1)))
    loop = cq.Workplane("XZ").center(x + 15.0, 7.5).circle(7.5).circle(6.0).extrude(-10.0).translate((0, y - 5.0, 0))
    clip_sols.append(tab.union(loop))
    clip_hw.append(place(m4b8, (x, y, 1.5), (0, 0, 1)))
    clip_hw.append(place(m4n_, (x, y, -P["t_base"]), (0, 0, -1)))
add("cable-clamps (bought, 4 x nylon P-clip for a 12 mm bundle, envelopes)", compound(clip_sols), RUBBER)
add("hardware-cable-clamps (bought, 4 x M4 x 8 button head, nuts under the pan)", compound(clip_hw), HARDWARE)

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

import json
with open(os.path.join(OUT, "cad", "plates.json"), "w", encoding="utf-8") as f:   # every flat plate with its expressions, for the Fusion build
    json.dump(dict(draft=DRAFT, user_params=[(k, n, float(P[k])) for k, n in USER_PARAMS],
                   derived_params=[(n, f, float(P[k])) for k, n, f in DERIVED_PARAMS], plates=plate_log), f, indent=0)
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
if "--check" in sys.argv or "--check-new" in sys.argv:
    import itertools
    solids = [(n, s.val() if hasattr(s, "val") else s) for n, s, _, _, _ in parts]
    NEW = ("blower-plate", "hardware-blower-plate", "blower (bought)", "exhaust", "ps1-tube", "th1", "hardware-th1", "moisture", "hardware-moisture", "entry-blank", "hardware-entry", "cable-clamps", "hardware-cable", "lint-box-back", "front-bulkhead", "rear-lower-panel", "base-pan", "spool-foam", "grommets")
    bad = []
    for (na, a), (nb, b) in itertools.combinations(solids, 2):
        if "--check-new" in sys.argv and not (na.startswith(NEW) or nb.startswith(NEW)):
            continue
        try:
            bba, bbb = a.BoundingBox(), b.BoundingBox()
            if (bba.xmax < bbb.xmin or bbb.xmax < bba.xmin or bba.ymax < bbb.ymin or bbb.ymax < bba.ymin
                    or bba.zmax < bbb.zmin or bbb.zmax < bba.zmin):
                continue
            ox0, ox1 = max(bba.xmin, bbb.xmin) - 1, min(bba.xmax, bbb.xmax) + 1
            oy0, oy1 = max(bba.ymin, bbb.ymin) - 1, min(bba.ymax, bbb.ymax) + 1
            oz0, oz1 = max(bba.zmin, bbb.zmin) - 1, min(bba.zmax, bbb.zmax) + 1
            clip = cq.Workplane("XY").box(ox1 - ox0, oy1 - oy0, oz1 - oz0, centered=False).translate((ox0, oy0, oz0)).val()
            a_c, b_c = a.intersect(clip), b.intersect(clip)       # the pieces inside the boxes' overlap: small shapes boolean reliably
            try:
                if a_c.Volume() < 1e-6 or b_c.Volume() < 1e-6:       # one of them has nothing in the overlap region (a compound's pieces are spread out)
                    continue
            except Exception:
                continue
            common = a_c.intersect(b_c)
            v = common.Volume()
        except Exception as ex:  # a failed boolean is reported, not hidden
            bad.append((na, nb, f"boolean failed: {ex}", ""))
            continue
        if v > 1.0:   # mm3; touching faces give 0
            cb = common.BoundingBox()
            bad.append((na, nb, round(v, 1), " at " + " ".join(f"{q:.1f}" for q in (cb.xmin, cb.xmax, cb.ymin, cb.ymax, cb.zmin, cb.zmax))))
            if "--check-new" in sys.argv:   # name the pieces of a compound that overlap, one line each
                for (nx_, x_), (ny_, y_) in ((na, a), (nb, b)), ((nb, b), (na, a)):
                    pieces = x_.Solids() if hasattr(x_, "Solids") else [x_]
                    if len(pieces) > 1:
                        for k, pc in enumerate(pieces):
                            try:
                                cv = pc.intersect(y_).Volume()
                            except Exception:
                                continue
                            if cv > 1.0:
                                pb = pc.BoundingBox()
                                bad.append((f"  piece {k} of {nx_[:40]}", ny_[:40], round(cv, 1), " piece at " + " ".join(f"{q:.1f}" for q in (pb.xmin, pb.xmax, pb.ymin, pb.ymax, pb.zmin, pb.zmax))))
    if bad:
        print("INTERFERENCE:")
        for na, nb, v, where in bad:
            print(f"  {na}  x  {nb}  : {v}{where}")
    else:
        print("interference check: no overlaps")
print("drum axis Z", P["drum_axis_z"], " H_body", P["H_body"], " H_total", round(P["H_total"], 1), " rear bulkhead Y", P["rear_bulk_y"],
      " lint slot area", round(P["lint_slot_area"]), " hood section", round(P["hood_area"]), " trunk", round(P["riser_area"]),
      " nozzle", round(P["nozzle_area"]), " basket outer wall in the box", round(P["basket_wall_area"]), " liner strip", round(P["liner_flat_len"], 1))
print("drum sheet flat", round(P["drum_flat_w"], 1), "x", P["drum_l"], " belt drawn length", round(P["belt_len_est"], 1),
      " belt crosses the ceiling at X", round(P["belt_cross_left"], 2), "and", round(P["belt_cross_right"], 2), " feet", P["foot_height"])
print("drum", round(P["drum_rpm"], 1), "rpm", " heat module top", round(P["hm_zmax"], 1), " collar area", round(P["hm_collar_area"]),
      " inlet area", round(P["hm_inlet_area"]), " felt arcs", round(P["felt_long_len"]), "and", round(P["felt_short_len"]))
