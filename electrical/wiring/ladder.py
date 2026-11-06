"""Draws the osa-dryer ladder diagrams as plain SVG.

Two files:
  ladder-common-power-module.svg   the common power module, mains side and 24 V side
  ladder-heat-modules.svg          the four heat modules at the HEAT_EN terminals

Everything is boxes and lines on purpose: a careful adult with a multimeter should be able
to follow a wire from the cord to the drum without knowing schematic symbols.
"""
import html

FONT = "Helvetica, Arial, sans-serif"


class Drawing:
    def __init__(self, w, h, title):
        self.w, self.h = w, h
        self.items = []
        self.items.append(f'<rect x="0" y="0" width="{w}" height="{h}" fill="#ffffff"/>')
        self.text(24, 34, title, size=20, bold=True)

    # ---- primitives ----
    def line(self, x1, y1, x2, y2, dash=False, width=1.8):
        d = ' stroke-dasharray="6,5"' if dash else ""
        self.items.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#111" stroke-width="{width}"{d}/>'
        )

    def text(self, x, y, s, size=13, anchor="start", bold=False, color="#111", italic=False):
        lines = s.split("\n")
        fw = ' font-weight="bold"' if bold else ""
        fs = ' font-style="italic"' if italic else ""
        out = [f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" text-anchor="{anchor}" fill="{color}"{fw}{fs}>']
        for i, ln in enumerate(lines):
            dy = 0 if i == 0 else size * 1.2
            out.append(f'<tspan x="{x}" dy="{dy}">{html.escape(ln)}</tspan>')
        out.append("</text>")
        self.items.append("".join(out))

    def node(self, x, y):
        self.items.append(f'<circle cx="{x}" cy="{y}" r="3.5" fill="#111"/>')

    def box(self, cx, cy, label, w=None, h=None, fill="#fff"):
        lines = label.split("\n")
        if w is None:
            w = max(len(ln) for ln in lines) * 7.2 + 18
        if h is None:
            h = 16 * len(lines) + 14
        x = cx - w / 2
        y = cy - h / 2
        self.items.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="3" fill="{fill}" stroke="#111" stroke-width="1.6"/>'
        )
        ty = cy - (len(lines) - 1) * 8 + 4.5
        self.text(cx, ty, label, size=12, anchor="middle")
        return x, x + w

    def terminal(self, cx, cy, label, side="right"):
        self.items.append(f'<circle cx="{cx}" cy="{cy}" r="7" fill="#fff" stroke="#111" stroke-width="1.6"/>')
        if side == "right":
            self.text(cx + 11, cy + 4, label, size=12)
        elif side == "left":
            self.text(cx - 11, cy + 4, label, size=12, anchor="end")
        elif side == "below":
            self.text(cx, cy + 20, label, size=12, anchor="middle")
        elif side == "above":
            self.text(cx, cy - 12, label, size=12, anchor="middle")
        elif side == "above-left":
            self.text(cx + 6, cy - 12, label, size=12, anchor="end")

    def rung(self, y, xa, xb, elements, dash_after=None):
        """Lay out boxes evenly between xa and xb on a horizontal rung.
        elements: list of label strings (boxes) or ('node',) or ('term', label)."""
        n = len(elements)
        if n == 0:
            self.line(xa, y, xb, y)
            return []
        widths = []
        for e in elements:
            if isinstance(e, tuple):
                widths.append(14)
            else:
                lines = e.split("\n")
                widths.append(max(len(ln) for ln in lines) * 7.2 + 18)
        total = sum(widths)
        gap = (xb - xa - total) / (n + 1)
        x = xa
        spans = []
        for e, w in zip(elements, widths):
            self.line(x, y, x + gap, y)
            x += gap
            cx = x + w / 2
            if isinstance(e, tuple):
                if e[0] == "node":
                    self.node(cx, y)
                elif e[0] == "term":
                    self.terminal(cx, y, e[1], side=e[2] if len(e) > 2 else "below")
                spans.append((x, x + w))
            else:
                self.box(cx, y, e)
                spans.append((x, x + w))
            x += w
        self.line(x, y, xb, y)
        return spans

    def rail(self, x, y1, y2, label, side="left"):
        self.line(x, y1, x, y2, width=2.6)
        if side == "left":
            self.text(x - 8, y1 - 8, label, size=13, anchor="end", bold=True)
        else:
            self.text(x + 8, y1 - 8, label, size=13, bold=True)

    def note(self, x, y, s, size=12):
        self.text(x, y, s, size=size, italic=True, color="#333")

    def save(self, path):
        svg = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}">'
        ]
        svg += self.items
        svg.append("</svg>")
        open(path, "w", encoding="utf-8").write("\n".join(svg))


# ---------------------------------------------------------------------------
# Drawing 1: common power module
# ---------------------------------------------------------------------------
def common_power_module(path):
    d = Drawing(1500, 1400, "osa-dryer: common power module, ladder diagram (draft 1, 2026-11-05)")
    d.note(24, 58, "Read each rung left to right. A box is a part; the label is the part's name in the wire list. Dashed lines are outside the common power module.")

    # ---------------- MAINS SECTION ----------------
    d.text(24, 100, "MAINS SIDE  (inside the common power module, behind the barrier)", size=15, bold=True)
    L1x, Nx = 140, 1000
    top, bottom = 130, 470
    d.rail(L1x, top, bottom, "L1 (X1:1)", side="left")
    d.rail(Nx, top, bottom, "N (X1:3)", side="right")

    # CB1 drawn in the L1 rail
    d.items.append(f'<rect x="{L1x-40}" y="150" width="80" height="34" fill="#fff" stroke="#111" stroke-width="1.6" rx="3"/>')
    d.text(L1x, 172, "CB1 10 A", size=12, anchor="middle")
    d.note(L1x + 52, 172, "supplementary breaker, protects the 120 V side only (motor and supply)")

    # Rung: motor
    y = 240
    d.rung(y, L1x, Nx, ["S1 door switch\ncontact 1 (mains)", "K_MOTOR\n1-2", "M1 motor 120 V\nwith built-in overload"])
    d.text(Nx - 12, y - 30, "to X3:1 (L), X3:2 (N)", size=11, anchor="end", italic=True, color="#333")

    # Rung: PSU
    y = 330
    spans = d.rung(y, L1x, Nx, ["F1 2 A T", "PSU 24 V DC 2.5 A\nlisted, universal input"])
    psu_x1, psu_x2 = spans[1]
    psu_cx = (psu_x1 + psu_x2) / 2
    d.line(psu_cx - 30, y + 24, psu_cx - 30, 572)
    d.line(psu_cx + 30, y + 24, psu_cx + 30, 572)
    d.text(psu_cx - 36, 485, "+24V", size=12, anchor="end")
    d.text(psu_cx + 36, 485, "0V", size=12)

    # Heat module mains terminals, unswitched
    y = 420
    d.line(L1x, y, 300, y)
    d.terminal(300, y, "X2:1  L1 to heat module", side="right")
    d.line(Nx, y, 1040, y)
    d.terminal(1040, y, "X2:3  N", side="right")
    d.note(L1x + 20, y - 10, "unswitched: the heat module has its own contactor")
    d.text(1150, 160, "L2 (X1:2)", size=13, bold=True)
    d.line(1150, 170, 1150, 440, width=2.6)
    d.line(1150, 420, 1250, 420)
    d.terminal(1250, 420, "X2:2  L2", side="right")
    d.note(1160, 200, "live only with a\n240 V cord")
    d.text(1370, 160, "PE (X1:4)", size=13, bold=True)
    d.line(1370, 170, 1370, 440, width=2.6)
    d.line(1370, 420, 1430, 420)
    d.terminal(1430, 420, "X2:4", side="below")
    d.note(1380, 200, "bonded to the box,\nthe rail, the frame,\n0V (one point)")

    # Barrier line between mains and SELV
    d.line(24, 500, 1476, 500, dash=True, width=1.2)
    d.note(24, 520, "barrier: no mains below this line")

    # ---------------- 24 V SECTION ----------------
    d.text(24, 548, "24 V SIDE  (SELV: everything the control module and the heat module's coil circuit touch)", size=15, bold=True)
    Px, Zx = 140, 1040      # +24V rail, 0V rail
    ILKx = 300               # 24V_ILK rail
    top24, bot24 = 600, 1340
    d.line(psu_cx - 30, 572, Px, 572)
    d.line(Px, 572, Px, top24)
    d.line(psu_cx + 30, 572, Zx, 572)
    d.line(Zx, 572, Zx, top24)
    d.rail(Px, top24, bot24, "+24V", side="left")
    d.rail(Zx, top24, bot24, "0V", side="right")

    # S2 door contact 2 feeding 24V_ILK
    y = 640
    d.line(Px, y, 175, y)
    d.box(225, y, "S2 door switch\ncontact 2")
    d.line(275, y, ILKx, y)
    d.node(ILKx, y)
    d.line(ILKx, y, ILKx, 990, width=2.6)
    d.text(ILKx + 8, y - 12, "24V_ILK", size=13, bold=True)

    # Rung: motor contactor coil
    y = 700
    d.rung(y, ILKx, Zx, ["RLY_MOTOR\n11-14", "K_MOTOR coil\nA1-A2, 24 V DC"])

    # Rung: heat permission chain with HI / LO branches
    y = 790
    spans = d.rung(y, ILKx, 640, ["PS1 air-proving\nswitch", "TF2 exhaust\nthermal fuse"])
    tap_x = spans[0][1] + 10
    d.node(640, y)
    yh, yl = y, y + 70
    d.line(640, yh, 640, yl)
    d.rung(yh, 640, 930, ["RLY_HEAT_LO\n11-12 (n.c.)", "RLY_HEAT\n11-14", "T_HI cycling\nthermostat"])
    d.rung(yl, 640, 930, ["RLY_HEAT_LO\n11-14 (n.o.)", "T_LO cycling\nthermostat"])
    d.line(930, yh, 930, yl)
    d.node(930, yh)
    d.node(930, yl)
    d.line(930, yh, 978, yh)
    d.terminal(985, yh, "X4:1  HEAT_EN", side="below")
    d.line(992, yh, Zx + 120, yh, dash=True)
    d.box(Zx + 190, yh, "heat module:\nits own limits, then\nits contactor coil", fill="#f4f4f4")
    d.line(Zx + 258, yh, Zx + 300, yh, dash=True)
    d.line(Zx + 300, yh, Zx + 300, yh + 45, dash=True)
    d.line(Zx + 300, yh + 45, Zx + 37, yh + 45, dash=True)
    d.terminal(Zx + 30, yh + 45, "X4:2  0V", side="below")
    d.line(Zx + 23, yh + 45, Zx, yh + 45)
    d.note(650, yl + 38, "RLY_HEAT_LO is one changeover contact: common 11 at the node, n.c. 12 feeds the HI branch,\nn.o. 14 feeds the LO branch, so LOW wins if both requests are asserted", size=11)

    # Status rungs
    y = 935
    d.node(tap_x, 790)
    d.line(tap_x, 790, tap_x, y)
    d.line(tap_x, y, 505, y)
    d.box(540, y, "PTC2\n100 mA")
    d.line(575, y, 640, y)
    d.terminal(640, y, "J1.12  STAT_AIRFLOW", side="below")
    d.line(647, y, Zx, y, dash=True)
    d.note(ILKx, y - 32, "tapped after PS1:\n24 V only while air is proven", size=11)

    y = 990
    d.line(ILKx, y, 505, y)
    d.box(540, y, "PTC1\n100 mA")
    d.line(575, y, 640, y)
    d.terminal(640, y, "J1.11  STAT_DOOR", side="below")
    d.line(647, y, 760, y, dash=True)
    d.box(830, y, "control module\nload, 50 mA max", fill="#f4f4f4")
    d.line(900, y, Zx, y, dash=True)

    # Rungs: request coils to J1
    d.note(Px + 10, 1040, "request lines: 24 V through the coil; the control module sinks 8 to 40 mA to 0V to assert")
    ys = [1075, 1135, 1195]
    names = [("RLY_MOTOR coil\nA1-A2, diode inside", "J1.3  REQ_MOTOR"),
             ("RLY_HEAT coil\nA1-A2, diode inside", "J1.4  REQ_HEAT"),
             ("RLY_HEAT_LO coil\nA1-A2, diode inside", "J1.5  REQ_HEAT_LO")]
    for y, (coil, pin) in zip(ys, names):
        d.line(Px, y, 230, y)
        d.box(320, y, coil)
        d.line(410, y, 470, y)
        d.terminal(477, y, pin, side="above")
        d.line(484, y, 620, y, dash=True)
        d.box(700, y, "control module\ncloses to 0V", fill="#f4f4f4")
        d.line(770, y, Zx, y, dash=True)

    # HEAT_ON rung
    y = 1265
    d.line(Px, y, 175, y)
    d.terminal(182, y, "X4:3", side="above")
    d.line(189, y, 240, y, dash=True)
    d.box(300, y, "heat module\nHEAT_ON contact", fill="#f4f4f4")
    d.line(370, y, 420, y, dash=True)
    d.terminal(427, y, "X4:4", side="above")
    d.line(434, y, 505, y)
    d.box(540, y, "PTC3\n100 mA")
    d.line(575, y, 640, y)
    d.terminal(640, y, "J1.13  STAT_HEAT_ON", side="below")
    d.line(647, y, Zx, y, dash=True)

    # J1 power
    y = 1320
    d.line(Px, y, 175, y)
    d.box(225, y, "F2 2 A")
    d.line(275, y, 340, y)
    d.terminal(340, y, "J1.1, J1.2  +24V to the control module", side="right")
    d.line(Zx, y, 900, y)
    d.terminal(900, y, "J1.9, J1.10  0V", side="left")

    d.note(24, 1380, "Not drawn: J2 (passive sensors, no connection to the power module), wire colors, terminal torque. See common-power-module.md for the wire list.")
    d.save(path)


# ---------------------------------------------------------------------------
# Drawing 2: the four heat modules
# ---------------------------------------------------------------------------
def heat_modules(path):
    d = Drawing(1500, 1250, "osa-dryer: heat modules at the X2 terminals (draft 1, 2026-11-05)")
    d.note(24, 58, "Each module gets unswitched mains (X2:1 to X2:4, mains strip) and the 24 V permission HEAT_EN (X4:1, return X4:2, SELV strip), and gives back a HEAT_ON contact (X4:3, X4:4).")

    def panel(y0, title, mains_elems, coil_elems, heat_on, notes, mains_right="N (X2:3)"):
        d.text(24, y0, title, size=15, bold=True)
        Lx, Rx = 160, 1060
        # mains rung
        ym = y0 + 45
        d.terminal(Lx, ym, "X2:1 L1", side="left")
        d.terminal(Rx, ym, mains_right, side="right")
        if mains_elems:
            d.rung(ym, Lx + 7, Rx - 7, mains_elems)
        else:
            d.text((Lx + Rx) / 2, ym + 4, "nothing connected", size=12, anchor="middle", italic=True)
        # coil rung
        yc = y0 + 115
        d.terminal(Lx, yc, "X4:1 HEAT_EN", side="left")
        d.terminal(Rx, yc, "X4:2 0V", side="right")
        if coil_elems:
            d.rung(yc, Lx + 7, Rx - 7, coil_elems)
        else:
            d.text((Lx + Rx) / 2, yc + 4, "nothing connected", size=12, anchor="middle", italic=True)
        # heat on rung
        yo = y0 + 170
        d.terminal(Lx, yo, "X4:3", side="left")
        d.terminal(Rx, yo, "X4:4", side="right")
        if heat_on:
            d.rung(yo, Lx + 7, Rx - 7, [heat_on])
        else:
            d.text((Lx + Rx) / 2, yo + 4, "open: STAT_HEAT_ON stays false", size=12, anchor="middle", italic=True)
        d.note(1185, ym - 6, notes)

    panel(110, "NONE  (blanking duct, nothing electrical)", [], [], None,
          "Every build runs this way first.\nThe bay holds a sheet duct from\nthe louvers to the riser flange.")

    panel(380, "ELECTRIC  (reference build, 240 V, 30 A circuit)",
          ["K_HEAT 1-2", "TF1 thermal fuse\nheater box", "T_HL high-limit\nheater box", "R1 element\n5.0 to 5.6 kW", "K_HEAT 3-4"],
          ["K_HEAT coil\nA1-A2, 24 V DC"],
          "CS1 current switch on an element lead\n(or K_HEAT auxiliary contact 53-54)",
          "Both poles switched. The thermal\nfuse and high-limit carry the\nelement current and sit in the\nmains path, as the charter asks.",
          mains_right="L2 (X2:2)")

    panel(650, "GAS  (120 V, 15 A circuit, plus a gas line and an outdoor vent)",
          ["K_HEAT 1-2", "T_BHL burner\nhigh-limit", "TF1 thermal fuse\nburner housing", "burner assembly: igniter,\nradiant flame sensor, valve coils"],
          ["K_HEAT coil\nA1-A2, 24 V DC"],
          "RLY_VALVE: relay with a 120 V coil wired across\nthe gas valve coil; contact closed = valve open",
          "The burner assembly is a listed\nunit with its own flame safety.\nNothing here decides anything;\nit only permits.")

    panel(920, "HEAT PUMP  (120 V, 15 or 20 A circuit, a drain, no vent; blocked until a sealed unit is confirmed)",
          ["K_COMP 1-2", "sealed unit: compressor with its own\nthermal protector and high-pressure switch"],
          ["TMR1 anti-short-cycle\nlockout, 3 to 5 min", "T_CHL condenser\noutlet high-limit", "FS1 condensate\nsafety switch (n.c.)", "K_COMP coil\nA1-A2, 24 V DC"],
          "CS1 current switch on the compressor lead\n(or K_COMP auxiliary contact 53-54)",
          "Fixed-speed compressor only.\nA full tank or a failed pump\nopens FS1 and stops heat\nwithout a board.")

    d.note(24, 1215, "Terminal numbers 1-2, 3-4 (contactor poles), 11-14 (relay n.o.), 11-12 (relay n.c.), 53-54 (contactor auxiliary), A1-A2 (coil) follow the IEC convention printed on the parts.")
    d.save(path)


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    common_power_module(f"{out}/ladder-common-power-module.svg")
    heat_modules(f"{out}/ladder-heat-modules.svg")
    print("ok")
