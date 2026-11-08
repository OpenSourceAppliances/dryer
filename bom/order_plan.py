"""order_plan.py: what to order, from whom, and what to send them, for one dryer.

Run from the repo root:  python3 bom/order_plan.py
Writes bom/order-plan.csv (one row per thing to order); with --json PATH also the same rows grouped into order
packages, for the ordering page.

Sources, all in this repo, so the plan follows the design when it changes:
    bom/bom.csv, bom/heat-electric-240.csv    bought parts, specs, two vendors each
    mechanical/drawings/*.dxf                 every laser-cut part (size measured from the file)
    mechanical/cad/plates.json                plate thicknesses
    mechanical/drawings/frame-cut-list.csv    extrusion, bar and angle lengths
    mechanical/cad/hardware.json              every bolt, nut and washer the model places (counts)
    docs/verification.md                      the checks that must close before a part is ordered or cut

Plain-language rules kept here:
    Wave 1  buy now and measure on arrival (the 100-series checks need the real parts in hand)
    Wave 2  cut and buy after the checks that hold them are closed
    Wave 3  the drum sheet, last, after the trial wrap (V-208)
Vendor part numbers marked unverified in the BOM stay marked; the generic spec is the real identity of a part.
Draft 1, 2026-11-07, model draft 9.
"""
import collections
import csv
import json
import math
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def p(*a):
    return os.path.join(ROOT, *a)


# ---------------------------------------------------------------- packages: who you order from
PACKAGES = [
    ("motor-drive", "Motor, blower and drive", "Industrial distributor (Grainger, Zoro) or an appliance parts house",
     "The generic spec on each line. Motor: 120 V, 1/3 hp, NEMA 48, dual 1/2 in shaft. Ask for the nameplate and the "
     "shaft drawing before you pay if the listing does not show them."),
    ("appliance", "Appliance repair parts", "PartSelect, AppliancePartsPros, RepairClinic, or a local appliance parts store",
     "The OEM part number (Whirlpool numbers are listed) or the generic spec. These houses sell by OEM number; aftermarket "
     "brands (Supco, ERP) cross-reference the same number."),
    ("electrical", "Controls and electrical", "Digi-Key or Mouser for the small parts; AutomationDirect, RS or a local "
     "electrical distributor for the DIN rail devices", "The maker's part number. Check the datasheet's size against the "
     "envelope in the model before ordering (V-112)."),
    ("extrusion", "Extrusion and frame hardware", "Misumi (cut to length and end tapping as order options) or McMaster-Carr, "
     "or 8020 / any 8 mm slot 4040 maker", "The cut list: profile, length, quantity, and which ends are tapped M8. "
     "Misumi takes the length and tapping in the part number configurator."),
    ("fasteners", "Fasteners", "McMaster-Carr, Fastenal, Bolt Depot, or Misumi for the T-nuts",
     "Size, length, head, material and quantity. Counts are the model's own, with about 10 percent spare."),
    ("laser-steel-15", "Laser cutting: 1.5 mm steel", "Online laser service (SendCutSend, OSH Cut, Xometry) or a local "
     "laser shop", "The DXF files (CUT layer only), mild steel 0.060 in (16 ga, 1.52 mm), the quantity of each, no bends, "
     "deburred. Powder coat: the colour in the Finish column, or order bare and paint them yourself."),
    ("laser-steel-2", "Laser cutting: 2 mm steel", "Same service as the 1.5 mm steel",
     "door-ring.dxf and door-disc.dxf, mild steel 0.075 in (14 ga, 1.9 mm) or the nearest they stock, one each, graphite "
     "grey powder coat (RAL 7024) or bare."),
    ("laser-stainless", "Laser cutting: stainless", "OSH Cut (lists 304 at 0.036 in up to 119 x 47 in) or SendCutSend "
     "(custom quote over 68 x 44 in)", "The DXF files, 304 stainless, 2B or mill finish, the thickness per line, quantity, "
     "no bends (the drum tabs are folded by hand), deburred. Ask for the M3 holes in the basket plates to be tapped."),
    ("laser-aluminium", "Laser cutting: aluminium", "Same service as the steel",
     "tier0-faceplate.dxf (CUT layer; LABEL layer only if you want the text engraved), liner.dxf and liner-splice.dxf, "
     "5052 aluminium, the thickness per line, no bends."),
    ("stock", "Bar and angle stock", "A local metal supplier (cheapest, cuts to length), Online Metals, or McMaster-Carr",
     "Profile, alloy, length to buy. You cut and drill these yourself from the cut list; or ask the supplier to cut to the "
     "lengths listed."),
    ("hardware-store", "Hardware store and HVAC supply", "Any hardware store, HVAC supply house or McMaster-Carr",
     "The generic spec. Nothing here is made to a drawing."),
]
PKG = {k: (t, w, s) for k, t, w, s in PACKAGES}

# BOM line -> package
PKG_OF = {
    "CH-M1": "motor-drive", "CH-BLOWER": "motor-drive", "CH-PULLEY": "motor-drive", "CH-BELT": "motor-drive",
    "CH-IDLER": "motor-drive", "CH-MOTOR-MOUNT": "appliance",
    "CH-ROLLERS": "appliance", "CH-GLIDES": "appliance", "CH-FELT": "appliance", "HE-R1": "appliance",
    "HE-TF1": "appliance", "HE-T_HL": "appliance", "CPM-TF2": "appliance", "CPM-T_HI": "appliance", "CPM-T_LO": "appliance",
    "CPM-TH1": "appliance", "CPM-MOIST": "appliance", "CPM-S1": "appliance", "CH-DOORSEAL": "appliance",
    "CH-LATCH": "appliance", "CPM-CORD-240": "appliance",
    "CH-EXT-4040": "extrusion", "CH-EXT-2020": "extrusion", "CH-BRKT": "extrusion", "CH-BRKT-2020": "extrusion",
    "CH-TNUT-M8": "extrusion", "CH-FEET": "extrusion",
    "CH-ROLLER-STUDS": "fasteners", "CPM-GND": "fasteners", "T0-NUTS": "fasteners",
    "CH-FLATBAR": "stock", "CH-ANGLE-20": "stock", "CH-DRUM-BAFFLE": "stock", "CH-IDLER-ARM": "stock",
    "CH-EXHAUST": "hardware-store", "CH-EXH-CLAMP": "hardware-store", "CH-TAP": "hardware-store",
    "HE-COLLAR": "hardware-store", "CPM-DIN": "electrical", "HE-DIN": "electrical", "CH-HINGE": "hardware-store", "CH-HANDLE": "hardware-store",
    "CH-GASKET": "hardware-store", "CH-PAINT": "hardware-store", "CPM-CORD-120": "hardware-store",
}
# BOM lines replaced by other rows of the plan (the made parts by their DXFs, the screws by the model's counts)
REPLACED = {
    "CH-PLATES": "laser rows", "CH-DUCTS": "laser rows", "CH-LINER": "laser rows", "CH-BLOWER-PLATE": "laser rows",
    "CH-BLANKS": "laser rows", "CH-DRUM-SHEET": "laser rows", "CH-DRUM-RINGS": "laser rows",
    "CH-DRUM-SPLICE": "laser rows", "CPM-BOX": "laser rows", "HE-TRAY": "laser rows", "HE-BOX": "laser rows",
    "T0-FACE": "laser rows", "CH-LINT": "laser rows and a hardware store row",
    "CH-BOLT-M6": "fastener rows", "CH-TNUT-M6": "fastener rows", "CH-BOLT-M4": "fastener rows",
    "CH-TNUT-M4": "fastener rows", "CH-BOLT-M3": "fastener rows", "CH-BOLT-M8": "fastener rows",
    "CH-DRUM-HW": "fastener rows", "CH-CSK": "fastener rows", "CH-DS-MOUNT": "fastener rows",
    "CH-PS1-BRKT": "stock rows (CH-ANGLE-20)",
    "CH-EXT-4040": "cut list rows", "CH-EXT-2020": "cut list rows", "CH-ANGLE-20": "cut list rows",
    "CH-DRUM-BAFFLE": "cut list rows", "CH-FLATBAR": "cut list rows", "CH-IDLER-ARM": "cut list rows",
}
# wave 2: bought parts that wait on a measurement of another part
WAVE2_BOUGHT = {"CH-PULLEY": "V-105, V-106", "CH-BELT": "V-012, V-105"}

# ---------------------------------------------------------------- laser-cut parts
# name -> (package, design material, design thickness mm, stock to order, qty, finish, gate)
BLUE = "RAL 5023 distant blue"
GREY = "RAL 7024 graphite grey"
INSIDE = "none (inside part): bare, or primer and enamel"
LASER = {
    # 1.5 mm mild steel
    "side-panel-left": (BLUE, ""), "side-panel-right": (BLUE, ""), "front-upper-panel": (BLUE, "V-115"),
    "rear-upper-panel": (BLUE, ""), "top-panel": (BLUE, ""),
    "front-lower-panel": (GREY, ""), "rear-lower-panel": (GREY, "V-107"),
    "console-face": (GREY, ""), "console-cap": (GREY, ""), "console-rear": (GREY, ""),
    "console-cheek-left": (GREY, ""), "console-cheek-right": (GREY, ""),
    "front-bulkhead": (INSIDE, "V-102, V-112"), "rear-bulkhead": (INSIDE, "V-102"),
    "base-pan": (INSIDE, "V-105, V-106, V-107, V-111, V-112, V-113"), "bay-ceiling": (INSIDE, ""),
    "lint-box-front": (INSIDE, ""), "lint-box-back": (INSIDE, "V-112"), "hood-bottom": (INSIDE, ""),
    "hood-top": (INSIDE, ""), "trunk-front": (INSIDE, ""), "trunk-rear": (INSIDE, ""),
    "blower-plate": (INSIDE, "V-107"), "entry-blank": (INSIDE, ""),
    "power-module-plate": (INSIDE, "V-112"), "power-module-cover": (INSIDE, "V-112"),
    "power-module-barrier": (INSIDE, "V-112"),
    "heat-module-tray": (INSIDE, "V-108, V-112"), "heat-module-wall-left": (INSIDE, "V-108"),
    "heat-module-wall-right": (INSIDE, "V-108"), "heat-module-wall-front": (INSIDE, "V-108"),
    "heat-module-wall-rear": (INSIDE, "V-108"), "heat-module-top": (INSIDE, "V-108, V-109"),
    "heat-module-terminal-plate": (INSIDE, "V-112"),
}
OTHER_LASER = {
    # name: (package, material, design t, stock to order, finish, gate)
    "door-ring": ("laser-steel-2", "mild steel", 2.0, "0.075 in (14 ga, 1.90 mm)", GREY, "V-115"),
    "door-disc": ("laser-steel-2", "mild steel", 2.0, "0.075 in (14 ga, 1.90 mm)", GREY, "V-115"),
    "drum-sheet": ("laser-stainless", "304 stainless", 0.8, "0.030 in (0.76 mm) or 0.036 in (0.91 mm), see the open question",
                   "none (2B or mill)", "V-101, V-208"),
    "drum-ring": ("laser-stainless", "304 stainless", 2.0, "0.074 to 0.075 in (14 ga, 1.9 mm)", "none (2B or mill)", ""),
    "drum-splice": ("laser-stainless", "304 stainless", 1.0, "0.036 in (0.91 mm) or 0.048 in (1.22 mm)", "none", "V-208"),
    "basket-far-plate": ("laser-stainless", "304 stainless", 3.0, "0.120 to 0.125 in (3.05 to 3.18 mm), M3 holes tapped",
                         "none", ""),
    "basket-lip-plate": ("laser-stainless", "304 stainless", 3.0, "0.120 to 0.125 in (3.05 to 3.18 mm), M3 holes tapped",
                         "none", ""),
    "basket-far-clamp": ("laser-stainless", "304 stainless", 1.5, "0.060 in (16 ga, 1.52 mm)", "none", ""),
    "basket-lip-clamp": ("laser-stainless", "304 stainless", 1.5, "0.060 in (16 ga, 1.52 mm)", "none", ""),
    "tier0-faceplate": ("laser-aluminium", "5052 aluminium", 2.0, "0.080 in (2.03 mm)", "none, or brushed", "V-110"),
    "liner": ("laser-aluminium", "5052 aluminium", 1.5, "0.063 in (1.60 mm) or 0.060 in", "none", ""),
    "liner-splice": ("laser-aluminium", "5052 aluminium", 1.5, "0.063 in (1.60 mm) or 0.060 in", "none", ""),
}
LASER_QTY = {"drum-ring": 2, "entry-blank": 2}
LASER_WHY = {
    "drum-ring": "cut early: the trial wrap (V-208) needs the real rings",
    "drum-sheet": "one piece 1945 mm long: confirm the service cuts it at this thickness (V-101); wrap a cheap blank first (V-208)",
    "entry-blank": "two from the one file",
    "base-pan": "most holes of any plate are set by bought parts: motor cradles, idler, blower plate feet, PS1 bracket, cord bushing, feet",
    "front-bulkhead": "roller stud holes (V-102) and the moisture bar holes (V-112)",
    "rear-bulkhead": "roller stud holes (V-102)",
    "front-upper-panel": "door switch plunger and ear holes (V-115)",
    "door-ring": "hinge and switch holes (V-115)",
    "door-disc": "hinge leaf, handle and catch holes (V-115)",
    "tier0-faceplate": "timer shaft and knob holes, checked on a timer in hand (V-110)",
    "blower-plate": "housing screw holes drilled from the bought housing (V-107)",
    "rear-lower-panel": "exhaust pipe hole position follows the housing's collar (V-107)",
    "liner": "rolled by hand round a 471 mm plywood disc after cutting",
    "basket-far-plate": "ask for the six M3 holes tapped",
    "basket-lip-plate": "ask for the six M3 holes tapped",
}


def dxf_size(name):
    """Overall size of a DXF's CUT layer in mm, and its number of round holes."""
    try:
        import ezdxf
        from ezdxf import bbox
    except ImportError:
        return None, None, None
    doc = ezdxf.readfile(p("mechanical", "drawings", name + ".dxf"))
    msp = doc.modelspace()
    cut = [e for e in msp if e.dxf.layer == "CUT"]
    b = bbox.extents(cut)
    holes = sum(1 for e in cut if e.dxftype() == "CIRCLE")
    return round(b.size.x, 1), round(b.size.y, 1), holes


def inch(mm):
    return mm / 25.4


# ---------------------------------------------------------------- fasteners from the model
def fastener_rows():
    hw = json.load(open(p("mechanical", "cad", "hardware.json")))["hardware"]
    count = collections.Counter()
    tnut_m6 = washer_m6 = 0
    for name, pieces in hw.items():
        n_hex = sum(1 for pc in pieces if pc and pc[0][0] == "hex_m6")
        if "T-nuts" in name:
            tnut_m6 += n_hex
        if "washers" in name:
            washer_m6 += n_hex
        for pc in pieces:
            if pc:
                count[tuple(pc[0])] += 1
    # what each drawn kind is, in words (the button head's d and length; nuts by size)
    rows = []

    def spare(n):
        return int(math.ceil(n * 1.10 / 5.0) * 5) if n >= 10 else n + 2

    def add(item, spec, n, note=""):
        rows.append(dict(item=item, spec=spec, model=n, qty=spare(n), note=note))

    hex6 = count[("hex_m6", 12.0)]
    add("M6 x 12 hex head bolt", "ISO 4017 / DIN 933, 8.8 zinc", hex6, "panels, console, motor cradles, PS1, blower plate, idler brackets")
    add("M6 flat washer", "ISO 7089, zinc", washer_m6, "under the hex heads on the T-nut joints")
    add("M6 T-nut for the 8 mm slot", "drop-in or slide-in, 4040 8 mm slot (Misumi HNTT8-6 class)", tnut_m6 + 2,
        "every panel and console joint, plus 2 for the lint box hang bolts")
    add("M6 nyloc nut", "ISO 10511, zinc or stainless", count[("nut", 10.0, 5.0, 6.2)], "baffles, hinge, through-the-pan bolts")
    add("M6 x 12 button head", "ISO 7380, stainless A2", count[("button", 6.0, 10.5, 3.3, 12.0, 4.0)], "drum baffles")
    add("M6 x 16 countersunk socket", "ISO 10642, stainless A2", count[("csk", 6.0, 12.0, 16.0)], "fixed hinge half")
    m4 = {L: count[("button", 4.0, 7.6, 2.2, L, 2.5)] for L in (8.0, 10.0, 16.0, 20.0, 40.0)}
    add("M4 x 8 button head", "ISO 7380, stainless A2, 2.5 mm hex key", m4[8.0], "drum tabs and seam, modules, ducts, door, sensors")
    add("M4 x 10 button head", "ISO 7380, stainless A2", m4[10.0], "faceplate, handle, glides, riser, basket pull")
    add("M4 x 16 button head", "ISO 7380, stainless A2", m4[16.0], "moisture bars")
    add("M4 x 20 button head", "ISO 7380, stainless A2", m4[20.0], "exhaust thermistor")
    add("M4 x 40 button head", "ISO 7380, stainless A2", m4[40.0], "lint box")
    add("M4 nyloc nut", "ISO 10511, stainless A2", count[("nut", 7.0, 3.2, 4.2)], "")
    add("M4 T-nut for the 6 mm slot", "2020 6 mm slot (Misumi HNTT5-4 class)", 8, "tray rail brackets 4, heat module tray 4")
    add("M4 T-nut for the 8 mm slot", "4040 8 mm slot", 4, "tray rail brackets' other legs")
    add("M3 x 5 button head", "ISO 7380, stainless A2", count[("button", 3.0, 5.7, 1.65, 5.0, 2.0)], "lint basket clamp plates")
    add("M3 x 6 button head", "ISO 7380, stainless A2", count[("button", 3.0, 5.7, 1.65, 6.0, 2.0)], "liner splice")
    add("M3 nyloc nut", "ISO 10511, stainless A2", count[("nut", 5.5, 2.4, 3.2)], "liner splice")
    n_hang = count[("button", 6.7, 13.0, 4.0, 20.0, 5.0)]
    add("Lint box hang bolt, 20 long, with a 16 x 8.5 x 4 spacer", "button head, stainless; M8 per the BOM (CH-BOLT-M8), "
        "the model's set is named M6 x 20: check before ordering", n_hang, "open question")
    return rows


# ---------------------------------------------------------------- stock lengths from the cut list
def cut_rows():
    rows = list(csv.DictReader(open(p("mechanical", "drawings", "frame-cut-list.csv"))))
    by = collections.defaultdict(list)
    for r in rows:
        try:
            L = float(r["length_mm"])
        except ValueError:
            continue
        by[r["profile"]].append((r["item"], L, int(r["qty"]), r["note"]))
    return by


def main():
    bom = []
    for f in ("bom.csv", "heat-electric-240.csv"):
        for r in csv.DictReader(open(p("bom", f))):
            r["_file"] = f
            bom.append(r)
    out = []

    def row(**k):
        base = dict(wave="", package="", ref="", item="", give="", qty="", source_1="", pn_1="", source_2="",
                    pn_2="", gate="", flags="", note="")
        base.update(k)
        out.append(base)

    # bought lines from the BOM
    for r in bom:
        pid = r["part_id"]
        if pid in REPLACED:
            continue
        pkg = PKG_OF.get(pid) or ("electrical" if r["category"] in ("electrical", "control") else
                                  "fasteners" if r["category"] == "fastener" else "hardware-store")
        gates = sorted(set(re.findall(r"V-\d+", r["generic_spec"] + " " + r["notes"])))
        flags = []
        if "unverified" in r["notes"].lower():
            flags.append("part no. unverified")
        if not r["unit_cost"]:
            flags.append("no price yet")
        if pid == "CPM-CORD-120":
            flags.insert(0, "not for the electric build")
        wave = "2" if pid in WAVE2_BOUGHT else "1"
        gate = WAVE2_BOUGHT.get(pid, ", ".join(g for g in gates if g.startswith("V-1")))
        row(wave=wave, package=pkg, ref=pid, item=r["description"], give=r["generic_spec"], qty=r["quantity"],
            source_1=r["vendor_1"], pn_1=r["vendor_1_part_number"], source_2=r["vendor_2"], pn_2=r["vendor_2_part_number"],
            gate=gate, flags="; ".join(flags),
            note=("measure on arrival: " + ", ".join(g for g in gates if g.startswith("V-1")) if wave == "1" and gates else ""))

    # laser-cut parts, one row per DXF
    T = {pl["name"]: pl["t"] for pl in json.load(open(p("mechanical", "cad", "plates.json")))["plates"]}
    for name in sorted(set(LASER) | set(OTHER_LASER)):
        w, h, holes = dxf_size(name)
        if name in LASER:
            finish, gate = LASER[name]
            pkg, mat, t, stock = "laser-steel-15", "mild steel", T.get(name, 1.5), "0.060 in (16 ga, 1.52 mm)"
        else:
            pkg, mat, t, stock, finish, gate = OTHER_LASER[name]
        qty = LASER_QTY.get(name, 1)
        wave = "3" if name == "drum-sheet" else ("1" if name == "drum-ring" else "2")
        size = f"{w:.0f} x {h:.0f} mm ({inch(w):.1f} x {inch(h):.1f} in), {holes} holes" if w else ""
        row(wave=wave, package=pkg, ref=name + ".dxf", item=name.replace("-", " "),
            give=f"{mat}, design {t:g} mm; order {stock}; finish: {finish}; {size}", qty=str(qty),
            source_1=PKG[pkg][1].split(" (")[0].split(",")[0], gate=gate,
            flags="no price yet", note=LASER_WHY.get(name, ""))

    # lint basket mesh and pull (the rest of CH-LINT)
    row(wave="2", package="hardware-store", ref="CH-LINT", item="Lint basket mesh and pull",
        give="Stainless 18 x 16 insect screen, a strip 42 x 350 mm; a D-pull with 64 mm hole centres, about 25 mm projection, M4",
        qty="1 each", source_1="hardware store", source_2="McMaster-Carr", flags="no price yet")
    row(wave="1", package="hardware-store", ref="V-208", item="Trial drum blank",
        give="0.5 mm aluminium flashing or heavy card, at least 1950 x 600 mm, cut by hand to drum-sheet.dxf printed full size",
        qty="1", source_1="hardware store (roof flashing roll)", source_2="", gate="", flags="",
        note="wrapped round the real rings before the stainless is cut (V-208)")

    # fasteners
    for f in fastener_rows():
        row(wave="1", package="fasteners", ref="model", item=f["item"], give=f["spec"], qty=str(f["qty"]),
            source_1="McMaster-Carr", source_2="Fastenal or Bolt Depot",
            note=f"the model places {f['model']}; {f['note']}".rstrip("; "),
            flags="open question" if "check before" in f["spec"] else "no price yet")

    # extrusion and stock from the cut list
    by = cut_rows()
    ext = {"40x40": ("4040 T-slot, 8 mm slot", "CH-EXT-4040"), "20x20": ("2020 T-slot, 6 mm slot", "CH-EXT-2020")}
    bom_by = {r["part_id"]: r for r in bom}
    tapped = {"post-1", "post-2", "post-3", "post-4", "rail-mid-front-left", "rail-mid-front-right"}
    for prof, (desc, pid) in ext.items():
        lengths = collections.Counter()
        tap = collections.Counter()
        for item, L, q, note in by.get(prof, []):
            lengths[L] += q
            if item in tapped:
                tap[L] += q
        total = sum(L * q for L, q in lengths.items())
        cuts = "; ".join(f"{q} x {L:g}" + (f" ({tap[L]} tapped M8 in one end)" if tap[L] else "")
                         for L, q in sorted(lengths.items(), reverse=True))
        row(wave="1", package="extrusion", ref=pid, item=f"{desc}, cut to length", give=f"Cut list (mm): {cuts}. "
            f"Total {total / 1000:.2f} m; one cut piece per line on a Misumi order, or {math.ceil(total * 1.08 / 2000)} x 2 m "
            f"bars to cut yourself", qty=str(sum(lengths.values())) + " pieces", source_1="Misumi", pn_1=bom_by[pid]["vendor_1_part_number"],
            source_2="McMaster-Carr", pn_2=bom_by[pid]["vendor_2_part_number"],
            gate="V-113", flags="part no. unverified; no price yet", note="the posts' bottom ends take the feet; the front stubs' ends take the lint box hang bolts")

    stock = [("flat bar 30x8 aluminum", "6061/6082 flat bar 30 x 8 (1-1/4 x 5/16 in)"),
             ("flat bar 40x8 aluminum", "6061/6082 flat bar 40 x 8 (1-1/2 x 5/16 in)"),
             ("flat bar 25x8 aluminum", "6061/6082 flat bar 25 x 8 (1 x 5/16 in)"),
             ("flat bar 50x8 aluminum", "6061/6082 flat bar 50 x 8 (2 x 5/16 in)"),
             ("flat bar 25x4 aluminum", "6061 flat bar 25 x 4 (1 x 5/32 in)"),
             ("angle 20x20x2 aluminum", "6063/6061 angle 20 x 20 x 2 (3/4 x 3/4 x 1/16 in)"),
             ("angle 40x40x3 aluminum", "6063/6061 angle 40 x 40 x 3 (1-1/2 x 1-1/2 x 1/8 in)")]
    for prof, spec in stock:
        items = by.get(prof, [])
        if not items:
            continue
        total = sum(L * q for _, L, q, _ in items)
        buy = math.ceil(total * 1.10 / 500.0) * 0.5
        cuts = "; ".join(f"{q} x {L:g} {item}" for item, L, q, _ in items)
        row(wave="1", package="stock", ref=prof, item=spec, give=f"Cut list (mm): {cuts}. Total {total / 1000:.2f} m",
            qty=f"{buy:g} m", source_1="local metal supplier", source_2="McMaster-Carr or Online Metals",
            flags="no price yet", note=("the BOM's 3 m is short; buy the length here" if prof.startswith("angle 20") else ""))

    # write CSV
    cols = ["wave", "package", "ref", "item", "qty", "give", "source_1", "pn_1", "source_2", "pn_2", "gate", "flags", "note"]
    order = {k: i for i, (k, *_) in enumerate(PACKAGES)}
    out.sort(key=lambda r: (order[r["package"]], r["wave"], r["ref"]))
    with open(p("bom", "order-plan.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in out:
            w.writerow({c: r[c] for c in cols})

    packages = []
    for k, title, who, send in PACKAGES:
        rows = [r for r in out if r["package"] == k]
        if rows:
            packages.append(dict(id=k, title=title, who=who, send=send, rows=rows))
    import sys
    if "--json" in sys.argv:
        json.dump(dict(draft=1, model_draft=9, packages=packages), open(sys.argv[sys.argv.index("--json") + 1], "w"), indent=1)
    print(f"{len(out)} rows in {len(packages)} packages; "
          + ", ".join(f"wave {w}: {sum(1 for r in out if r['wave'] == w)}" for w in "123"))


if __name__ == "__main__":
    main()
