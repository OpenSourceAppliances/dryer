"""osa-dryer drawings generated from numbers in the specs.

  tier0-faceplate.dxf / .svg   Tier 0 control module faceplate (UCI-D faceplate spec, draft 3 numbers; faceplate draft 2)
                               the CAD model (mechanical/cad/osa_dryer_cad.py) imports this file for the same numbers
  tier0-wiring.svg             Tier 0 point-to-point wiring
  layout-concept.svg           cabinet concept: side and front elevations with the bay and the air path

All dimensions in millimeters. Needs ezdxf (pip install ezdxf). Run:  python3 tier0_drawings.py <output dir>
"""
import math
import os
import sys
import ezdxf

# the SVG helper lives with the electrical drawings; run this from anywhere in the repo
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'electrical', 'wiring'))
from ladder import Drawing  # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else "."

# ---------------------------------------------------------------------------
# Faceplate geometry (one source of truth for DXF and SVG)
# ---------------------------------------------------------------------------
FP_W, FP_H, FP_R = 540.0, 160.0, 10.0          # faceplate outline (UCI-D draft 5: 500 wide aperture)
MOUNT = [(-260, -70), (260, -70), (-260, 70), (260, 70), (0, -70), (0, 70)]   # 520 x 140 pattern plus two on the centre line, dia 4.5
MOUNT_D = 4.5
AP_W, AP_H = 500.0, 120.0                      # aperture, drawn as a reference only

TIMERS = {"DRY TIME": -150.0, "HEAT TIME": -60.0}  # x of the shaft centre, y = 0
SHAFT_D = 12.0                                 # check against the part: toggle-plate slot is 10.2 x 23.9
YOKE_SPAN = 83.3                               # NEMA device box-mount hole spacing, 3.281 in
YOKE_HOLE_D = 4.0                              # clearance for the 6-32 screws supplied with the timer
SEL_X, START_X, DEV_Y = 60.0, 130.0, 20.0      # 22 mm devices, 20 above the centre line so K1 fits below them
DEV22_D = 22.3
RAIL = [(50.0, -24.0), (130.0, -24.0)]         # M4 standoffs for a 100 mm DIN rail segment (K1 socket hangs 36 below this line, to the aperture's edge)
RAIL_D = 4.5
TIE = [(-230.0, -45.0), (-230.0, 45.0)]        # cable tie anchor holes for the J1 lead
TIE_D = 4.5
LABELS = [("DRY TIME", -150, 50), ("HEAT TIME", -60, 50), ("HEAT", 60, 47), ("START", 130, 47),
          ("AIR  LOW  HIGH", 60, 0)]


def rounded_rect_points(w, h, r):
    """LWPOLYLINE points with bulge for a rounded rectangle centred on the origin."""
    b = math.tan(math.radians(90) / 4)   # bulge for a 90 degree arc
    hw, hh = w / 2, h / 2
    return [
        (-hw + r, -hh, 0), (hw - r, -hh, b),
        (hw, -hh + r, 0), (hw, hh - r, b),
        (hw - r, hh, 0), (-hw + r, hh, b),
        (-hw, hh - r, 0), (-hw, -hh + r, b),
    ]


def holes():
    """(x, y, diameter, name) for every round hole."""
    hs = []
    for x, y in MOUNT:
        hs.append((x, y, MOUNT_D, "mount M4"))
    for name, x in TIMERS.items():
        hs.append((x, 0, SHAFT_D, f"{name} shaft"))
        hs.append((x, YOKE_SPAN / 2, YOKE_HOLE_D, f"{name} yoke"))
        hs.append((x, -YOKE_SPAN / 2, YOKE_HOLE_D, f"{name} yoke"))
    hs.append((SEL_X, DEV_Y, DEV22_D, "HEAT selector, 22 mm"))
    hs.append((START_X, DEV_Y, DEV22_D, "START, 22 mm"))
    for x, y in RAIL:
        hs.append((x, y, RAIL_D, "DIN rail standoff M4"))
    for x, y in TIE:
        hs.append((x, y, TIE_D, "cable tie"))
    return hs


def faceplate_dxf(path):
    doc = ezdxf.new("R2010", setup=True)
    doc.header["$INSUNITS"] = 4  # millimeters
    doc.layers.add("CUT", color=7)
    doc.layers.add("LABEL", color=1)
    doc.layers.add("REF", color=8)
    msp = doc.modelspace()
    msp.add_lwpolyline(rounded_rect_points(FP_W, FP_H, FP_R), format="xyb", close=True, dxfattribs={"layer": "CUT"})
    for x, y, d, _ in holes():
        msp.add_circle((x, y), d / 2, dxfattribs={"layer": "CUT"})
    for text, x, y in LABELS:
        msp.add_text(text, height=5, dxfattribs={"layer": "LABEL"}).set_placement((x, y), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)
    # reference only: the chassis aperture, so the cutter and the builder see the clear zone
    msp.add_lwpolyline([(-AP_W/2, -AP_H/2), (AP_W/2, -AP_H/2), (AP_W/2, AP_H/2), (-AP_W/2, AP_H/2)], close=True, dxfattribs={"layer": "REF"})
    msp.add_text("osa-dryer Tier 0 faceplate, draft 3, 2026-11-06 (UCI-D draft 5, 500 wide aperture). 2 mm aluminum. CUT layer only. LABEL layer is optional engraving. REF is not cut.",
                 height=3, dxfattribs={"layer": "REF"}).set_placement((-FP_W/2, -FP_H/2 - 8))
    doc.saveas(path)


def faceplate_svg(path):
    S = 3.0  # px per mm
    W, H = int(FP_W * S + 700), int(FP_H * S + 340)
    d = Drawing(W, H, "osa-dryer: Tier 0 faceplate (draft 3, 2026-11-06, UCI-D draft 5), 2 mm aluminum, all dimensions mm")
    ox, oy = 150 + FP_W * S / 2, 110 + FP_H * S / 2   # origin of the part at the drawing centre (y down)

    def P(x, y):
        return ox + x * S, oy - y * S

    # outline
    hw, hh, r = FP_W / 2, FP_H / 2, FP_R
    x0, y0 = P(-hw, hh)
    d.items.append(f'<rect x="{x0}" y="{y0}" width="{FP_W*S}" height="{FP_H*S}" rx="{r*S}" fill="#f7f7f7" stroke="#111" stroke-width="2"/>')
    # aperture reference
    ax, ay = P(-AP_W/2, AP_H/2)
    d.items.append(f'<rect x="{ax}" y="{ay}" width="{AP_W*S}" height="{AP_H*S}" fill="none" stroke="#888" stroke-width="1" stroke-dasharray="8,6"/>')
    d.text(ax + 6, ay + 16, "chassis aperture 500 x 120 (reference, not cut)", size=11, color="#555", italic=True)
    # timer bodies and yokes (reference, dashed)
    for name, x in TIMERS.items():
        bx, by = P(x - 20.3, 35.5)
        d.items.append(f'<rect x="{bx}" y="{by}" width="{40.6*S}" height="{70.9*S}" fill="none" stroke="#888" stroke-width="1" stroke-dasharray="4,4"/>')
        yx, yy = P(x - 12, 53.2)
        d.items.append(f'<rect x="{yx}" y="{yy}" width="{24*S}" height="{106.4*S}" fill="none" stroke="#bbb" stroke-width="1" stroke-dasharray="2,4"/>')
    # K1 socket on its rail (reference, dashed): 28 wide, from 36 below the rail line to 19 above it
    (rx0, ry), (rx1, _) = RAIL
    kx, ky = P(rx0 - 9, ry + 19)
    d.items.append(f'<rect x="{kx}" y="{ky}" width="{28*S}" height="{55*S}" fill="none" stroke="#888" stroke-width="1" stroke-dasharray="4,4"/>')
    rlx, rly = P(rx0 - 10, ry + 17.5)
    d.items.append(f'<rect x="{rlx}" y="{rly}" width="{(rx1 - rx0 + 20)*S}" height="{35*S}" fill="none" stroke="#bbb" stroke-width="1" stroke-dasharray="2,4"/>')
    # holes
    for x, y, dia, name in holes():
        cx, cy = P(x, y)
        d.items.append(f'<circle cx="{cx}" cy="{cy}" r="{dia/2*S}" fill="#fff" stroke="#111" stroke-width="1.6"/>')
        d.line(cx - 6, cy, cx + 6, cy, width=0.8)
        d.line(cx, cy - 6, cx, cy + 6, width=0.8)
    # labels (engraving or printed strip)
    for text, x, y in LABELS:
        cx, cy = P(x, y)
        d.text(cx, cy + 4, text, size=12, anchor="middle", bold=True)
    # dimensions
    def dim_h(y_mm, x1_mm, x2_mm, label, off=0):
        x1, y = P(x1_mm, y_mm); x2, _ = P(x2_mm, y_mm)
        y += off
        d.line(x1, y, x2, y, width=1)
        d.line(x1, y - 5, x1, y + 5, width=1); d.line(x2, y - 5, x2, y + 5, width=1)
        d.text((x1 + x2) / 2, y - 5, label, size=11, anchor="middle")
    def dim_v(x_mm, y1_mm, y2_mm, label, off=0):
        x, y1 = P(x_mm, y1_mm); _, y2 = P(x_mm, y2_mm)
        x += off
        d.line(x, y1, x, y2, width=1)
        d.line(x - 5, y1, x + 5, y1, width=1); d.line(x - 5, y2, x + 5, y2, width=1)
        d.items.append(f'<text x="{x+6}" y="{(y1+y2)/2+4}" font-family="Helvetica, Arial, sans-serif" font-size="11" fill="#111">{label}</text>')
    dim_h(-hh - 14, -hw, hw, f"{FP_W:g}")
    dim_h(-hh - 34, -260, 260, "520 (M4 mounting holes, 4.5 dia; two more on the centre line)")
    dim_v(hw + 14, -hh, hh, f"{FP_H:g}")
    dim_v(hw + 44, -70, 70, "140 (mounting holes)")
    dim_h(hh + 14, -hw, -150, "120")
    dim_h(hh + 14, -150, -60, "90")
    dim_h(hh + 14, -60, 60, "120")
    dim_h(hh + 14, 60, 130, "70")
    dim_v(-hw - 14, -YOKE_SPAN/2, YOKE_SPAN/2, "83.3")
    dim_v(hw + 110, 0, DEV_Y, "20 (22 mm devices)")
    dim_v(hw + 110, RAIL[0][1], 0, "24 (K1 rail)")
    d.text(ox - hw * S - 20, oy + 70, "timer yoke holes, 6-32", size=10, anchor="end", italic=True)

    # notes
    ny = oy + FP_H * S / 2 + 130
    notes = [
        "Holes: 6 x 4.5 mount; timers: 12 shaft (check against the part) and 2 x 4.0 yoke holes at 83.3; 2 x 22.3 for the 22 mm selector and button;",
        "2 x 4.5 for the K1 DIN rail standoffs; 2 x 4.5 cable tie anchors. Dashed boxes: timer body 40.6 x 70.9 and yoke 106.4 long, both behind the plate.",
        "The 22 mm devices sit 20 above the centre line and the K1 rail 24 below it, so the K1 socket (36 below the rail line) stays inside the aperture.",
        "Everything mounted on the back stays inside the 500 x 120 aperture; the 20 mm band outside it sits against the chassis panel.",
        "Labels: engrave if the cutter offers it, otherwise a printed strip. Knob diameter is not on the timer's sheet: check it before cutting.",
    ]
    for i, n in enumerate(notes):
        d.text(150, ny + i * 16, n, size=11, italic=True, color="#333")
    d.save(path)


# ---------------------------------------------------------------------------
# Tier 0 wiring, point to point
# ---------------------------------------------------------------------------
def tier0_wiring(path):
    d = Drawing(1300, 760, "osa-dryer: Tier 0 control module wiring (draft 1, 2026-11-05)")
    d.note(24, 58, "Five wires to J1 and one relay. Everything is a switch. Socket terminal numbers for K1 depend on the socket; write them on this drawing when the socket is in hand.")

    # J1 plug on the left
    d.text(60, 110, "J1 plug (Mini-Fit Jr. 16, male terminals)", size=13, bold=True)
    pins = {3: ("REQ_MOTOR", 200), 4: ("REQ_HEAT", 260), 5: ("REQ_HEAT_LO", 320), 9: ("0V", 560), 11: ("STAT_DOOR", 140)}
    d.items.append('<rect x="40" y="120" width="140" height="470" rx="6" fill="#f4f4f4" stroke="#111" stroke-width="1.6"/>')
    for p, (name, y) in pins.items():
        d.terminal(180, y, f"pin {p}  {name}", side="left")

    # STAT_DOOR -> START || K1-A -> DRY TIME -> K1 coil -> 0V
    y = 140
    d.line(187, y, 330, y)
    d.node(330, y)
    d.line(330, y, 330, y + 50)
    d.box(420, y, "START\npush button, n.o.")
    d.box(420, y + 50, "K1 contact A\n(hold)")
    d.line(330, y + 50, 350, y + 50)
    d.line(490, y + 50, 510, y + 50)
    d.line(510, y + 50, 510, y)
    d.node(510, y)
    d.line(490, y, 510, y)
    d.line(510, y, 560, y)
    d.box(640, y, "DRY TIME timer\ncontact, closed while timing")
    d.line(725, y, 780, y)
    d.box(840, y, "K1 coil\n(+ side)")
    d.line(900, y, 960, y)
    d.line(960, y, 960, 560)
    d.text(970, 350, "K1 coil (- side) to 0V", size=11, italic=True)

    # 0V rail from pin 9 along the bottom
    d.line(187, 560, 960, 560)
    d.node(960, 560)

    # K1 contact B: common to 0V, n.o. to the request node
    d.box(300, 460, "K1 contact B\ncommon")
    d.line(300, 483, 300, 560)
    d.node(300, 560)
    d.line(300, 437, 300, 400)
    d.node(300, 400)
    d.text(362, 447, "request node: at 0V while K1 is in", size=11, italic=True)

    # REQ_MOTOR straight to the node
    d.line(187, 200, 230, 200)
    d.line(230, 200, 230, 252)
    d.items.append('<path d="M230,252 A8,8 0 0 1 230,268" fill="none" stroke="#111" stroke-width="1.8"/>')
    d.line(230, 268, 230, 312)
    d.items.append('<path d="M230,312 A8,8 0 0 1 230,328" fill="none" stroke="#111" stroke-width="1.8"/>')
    d.line(230, 328, 230, 400)
    d.line(230, 400, 300, 400)
    d.node(230, 200)
    d.note(240, 236, "hops: wires cross, not joined", size=10)

    # HEAT TIME timer and selector
    d.line(300, 400, 420, 400)
    d.box(500, 400, "HEAT TIME timer\ncontact")
    d.line(580, 400, 640, 400)
    d.box(720, 400, "HEAT selector\ncommon")
    d.line(720, 377, 720, 300)
    d.box(720, 300, "HIGH")
    d.box(820, 400, "LOW")
    d.box(720, 500, "AIR")
    d.line(800, 400, 780, 400)
    d.text(752, 504, "AIR: no connection", size=11, italic=True)
    # HIGH -> pin 4, LOW -> pin 5
    d.line(690, 300, 640, 300)
    d.line(640, 300, 640, 260)
    d.line(640, 260, 187, 260)
    d.line(850, 400, 900, 400)
    d.line(900, 400, 900, 320)
    d.line(900, 320, 187, 320)
    d.node(187, 260); d.node(187, 320)

    # notes
    notes = [
        "Door open or power lost: pin 11 goes to 0 V, K1 drops, both contacts open, nothing is requested. START must be pressed again.",
        "DRY TIME at zero: its contact is open, K1 cannot pull in. HEAT TIME at zero: no heat request, the motor still runs.",
        "K1: 24 V DC plug-in relay with suppression diode, 2 changeover contacts; only the n.o. side of each is used. Coil under 50 mA.",
        "Wire: 0.5 mm2 (20 AWG). Timer and selector terminals take 6.3 mm quick-disconnects or ring terminals; the button's contact block takes screws.",
        "Pins 1, 2 (+24V) are not used. J2 is not plugged in.",
    ]
    for i, n in enumerate(notes):
        d.text(24, 640 + i * 18, n, size=11, italic=True, color="#333")
    d.save(path)


# ---------------------------------------------------------------------------
# Cabinet concept layout: side and front elevations
# ---------------------------------------------------------------------------
def layout_concept(path):
    S = 0.5  # px per mm
    d = Drawing(1500, 850, "osa-dryer: cabinet concept layout (draft 1, 2026-11-05), dimensions mm, not CAD")
    d.note(24, 58, "Targets from docs/design-rules.md section 7, drawn to scale so the bay, the drum, and the air path can be argued about before CAD. Nothing here is a drawing to cut from.")

    # ---- side elevation (left is the front of the dryer) ----
    ox, oy = 120, 740    # floor line origin (x right, y up)
    def P(x, y): return ox + x * S, oy - y * S
    DEPTH, BODY_H, CONSOLE_H, BAY_H = 750, 1000, 100, 300
    DRUM_D, DRUM_L = 650, 550
    d.text(ox, 100, "SIDE ELEVATION (front of the dryer at the left)", size=14, bold=True)
    # floor
    d.line(ox - 20, oy, ox + DEPTH * S + 20, oy, width=2.2)
    # body
    x, y = P(0, BODY_H)
    d.items.append(f'<rect x="{x}" y="{y}" width="{DEPTH*S}" height="{BODY_H*S}" fill="#fafafa" stroke="#111" stroke-width="2"/>')
    # console on top, rear 300 mm
    x, y = P(DEPTH - 300, BODY_H + CONSOLE_H)
    d.items.append(f'<rect x="{x}" y="{y}" width="{300*S}" height="{CONSOLE_H*S}" fill="#fafafa" stroke="#111" stroke-width="2"/>')
    d.text(x + 8, y + 30, "console", size=11)
    # bay
    x, y = P(0, BAY_H)
    d.items.append(f'<rect x="{x}" y="{y}" width="{DEPTH*S}" height="{BAY_H*S}" fill="#eef3f8" stroke="#111" stroke-width="1.2" stroke-dasharray="6,4"/>')
    d.text(x + 300, y + 18, "bay, 300 high", size=10)
    # drum (circle in side view is a rectangle: drum length along depth)
    drum_front, drum_cy = 90, BAY_H + 25 + DRUM_D / 2
    x, y = P(drum_front, drum_cy + DRUM_D / 2)
    d.items.append(f'<rect x="{x}" y="{y}" width="{DRUM_L*S}" height="{DRUM_D*S}" fill="#fff" stroke="#111" stroke-width="1.6"/>')
    d.text(x + 10, y + 40, f"drum, {DRUM_D} dia x {DRUM_L} long", size=11)
    # door
    x, y = P(-25, drum_cy + 240)
    d.items.append(f'<rect x="{x}" y="{y}" width="{25*S}" height="{480*S}" fill="#ddd" stroke="#111" stroke-width="1.2"/>')
    d.text(x + 2, y + 480 * S + 14, "door", size=11)
    # heat module and blower blocks
    x, y = P(DEPTH - 330, 40 + 180)
    d.items.append(f'<rect x="{x}" y="{y}" width="{260*S}" height="{180*S}" fill="#fde9d9" stroke="#111" stroke-width="1.2"/>')
    d.text(x + 6, y + 20, "heat module tray", size=11)
    x, y = P(60, 40 + 180)
    d.items.append(f'<rect x="{x}" y="{y}" width="{180*S}" height="{180*S}" fill="#e3f0e1" stroke="#111" stroke-width="1.2"/>')
    d.text(x + 6, y + 20, "blower", size=11)
    x, y = P(DEPTH - 330 - 40, 40 + 230)
    # riser duct up the back from the heat module to the rear bulkhead
    rx, ry = P(DEPTH - 95, BAY_H + 25 + DRUM_D - 60)
    d.items.append(f'<rect x="{rx}" y="{ry}" width="{60*S}" height="{(BAY_H + 25 + DRUM_D - 60 - 220)*S}" fill="#fde9d9" stroke="#111" stroke-width="1.2"/>')
    d.text(rx - 2, ry - 6, "riser", size=11)
    # lint filter duct from the drum front down to the blower
    lx, ly = P(60, BAY_H + 25 + 120)
    d.items.append(f'<rect x="{lx}" y="{ly}" width="{50*S}" height="{(25 + 120 + 80)*S}" fill="#e3f0e1" stroke="#111" stroke-width="1.2"/>')
    d.text(lx - 2, ly - 6, "lint filter duct", size=11)
    # exhaust / return
    ex, ey = P(240, 40 + 100)
    d.items.append(f'<line x1="{ex}" y1="{ey}" x2="{P(DEPTH-330,0)[0]}" y2="{ey}" stroke="#111" stroke-width="1.2" stroke-dasharray="6,4"/>')
    d.text(ox, oy + 42, "Dashed line in the bay: vented builds run an exhaust duct from the blower to the rear port; the heat pump build returns it into the heat module instead.", size=10, italic=True, color="#333")
    # air path arrows (text)
    d.text(ox + 20, oy - (BODY_H + CONSOLE_H) * S - 44, "air path, vented: louvers > heat module > riser > rear bulkhead > drum > lint filter > blower > exhaust", size=11, italic=True, color="#333")
    d.text(ox + 20, oy - (BODY_H + CONSOLE_H) * S - 28, "air path, heat pump: blower > return duct > heat module (evaporator, condenser) > riser > drum > lint filter > blower", size=11, italic=True, color="#333")
    # dimension lines
    def dim_h(y_mm, x1_mm, x2_mm, label):
        x1, y = P(x1_mm, y_mm); x2, _ = P(x2_mm, y_mm)
        d.line(x1, y, x2, y, width=1); d.line(x1, y-5, x1, y+5, width=1); d.line(x2, y-5, x2, y+5, width=1)
        d.text((x1+x2)/2, y - 5, label, size=11, anchor="middle")
    def dim_v(x_mm, y1_mm, y2_mm, label):
        x, y1 = P(x_mm, y1_mm); _, y2 = P(x_mm, y2_mm)
        d.line(x, y1, x, y2, width=1); d.line(x-5, y1, x+5, y1, width=1); d.line(x-5, y2, x+5, y2, width=1)
        d.items.append(f'<text x="{x+6}" y="{(y1+y2)/2+4}" font-family="Helvetica, Arial, sans-serif" font-size="11" fill="#111">{label}</text>')
    dim_h(-40, 0, DEPTH, "750")
    dim_v(DEPTH + 40, 0, BODY_H + CONSOLE_H, "1100")
    dim_v(DEPTH + 70, 0, BAY_H, "300 bay")
    dim_v(-75, BAY_H + 25, BAY_H + 25 + DRUM_D, "650")

    # ---- front elevation ----
    fx0 = 980
    def F(x, y): return fx0 + x * S, oy - y * S
    WIDTH = 690
    d.text(fx0, 100, "FRONT ELEVATION", size=14, bold=True)
    d.line(fx0 - 20, oy, fx0 + WIDTH * S + 20, oy, width=2.2)
    x, y = F(0, BODY_H)
    d.items.append(f'<rect x="{x}" y="{y}" width="{WIDTH*S}" height="{BODY_H*S}" fill="#fafafa" stroke="#111" stroke-width="2"/>')
    x, y = F(0, BODY_H + CONSOLE_H)
    d.items.append(f'<rect x="{x}" y="{y}" width="{WIDTH*S}" height="{CONSOLE_H*S}" fill="#fafafa" stroke="#111" stroke-width="2"/>')
    # UCI aperture in the console
    ax, ay = F(WIDTH/2 - 250, BODY_H + CONSOLE_H/2 + 60 - 10)
    d.items.append(f'<rect x="{ax}" y="{ay}" width="{500*S}" height="{120*S}" fill="#fff" stroke="#111" stroke-width="1.2"/>')
    d.text(ax + 4, ay + 14, "UCI-D aperture 500 x 120", size=10)
    # door opening
    cx, cy = F(WIDTH/2, BAY_H + 25 + DRUM_D/2)
    d.items.append(f'<circle cx="{cx}" cy="{cy}" r="{230*S}" fill="#eef" stroke="#111" stroke-width="1.6"/>')
    d.items.append(f'<circle cx="{cx}" cy="{cy}" r="{DRUM_D/2*S}" fill="none" stroke="#888" stroke-width="1" stroke-dasharray="4,4"/>')
    d.text(cx, cy + 4, "door opening 460 dia", size=11, anchor="middle")
    d.text(cx, cy + 20, "drum 650 dia behind", size=10, anchor="middle", color="#555")
    # lower front panel (bay access)
    x, y = F(0, BAY_H)
    d.items.append(f'<rect x="{x}" y="{y}" width="{WIDTH*S}" height="{BAY_H*S}" fill="#eef3f8" stroke="#111" stroke-width="1.2" stroke-dasharray="6,4"/>')
    d.text(x + 8, y + 18, "lower front panel: off to slide the heat module tray out", size=11)
    # feet
    for fxm in (60, WIDTH - 60):
        x, y = F(fxm - 15, 0)
        d.items.append(f'<rect x="{x}" y="{y-10}" width="{30*S}" height="10" fill="#333"/>')
    def fdim_h(y_mm, x1_mm, x2_mm, label):
        x1, y = F(x1_mm, y_mm); x2, _ = F(x2_mm, y_mm)
        d.line(x1, y, x2, y, width=1); d.line(x1, y-5, x1, y+5, width=1); d.line(x2, y-5, x2, y+5, width=1)
        d.text((x1+x2)/2, y - 5, label, size=11, anchor="middle")
    fdim_h(-40, 0, WIDTH, "690")

    d.note(24, 828, "Open questions this drawing does not settle: the drum itself, the motor and blower arrangement, drum support, whether the console is part of the cabinet. See docs/design-rules.md section 11.")
    d.save(path)


if __name__ == "__main__":
    faceplate_dxf(f"{OUT}/tier0-faceplate.dxf")
    faceplate_svg(f"{OUT}/tier0-faceplate.svg")
    tier0_wiring(f"{OUT}/tier0-wiring.svg")
    layout_concept(f"{OUT}/layout-concept.svg")
    print("ok")
