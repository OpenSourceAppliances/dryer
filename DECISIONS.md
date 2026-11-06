# Decisions

Design decision log for osa-dryer, newest first. Every departure from the charter is recorded here with the reason. Entries are never deleted; a reversed decision gets a new entry that points back at the old one.

Format for each entry:

```
## YYYY-MM-DD  Short title

Decision: what was decided, in one or two sentences.
Why: the reasoning, the tradeoff, and what was given up.
Charter: "follows" or "departs from <section>" and why the departure is justified.
Affects: which files or subsystems this changes.
```

---

## 2026-11-05  The repository is named dryer

Decision: The GitHub repository is `OpenSourceAppliances/dryer`, and the charter's layout is amended so repositories are named plainly under the organization.
Why: The organization name already carries the project name. Keep it simple.
Charter: amends the layout naming; the project copy of the charter needs the same line.
Affects: `README.md`, `osa-charter/CHARTER.md`.

## 2026-11-05  Drum: made by the builder from a wrapped sheet on laser-cut rings (reverses the OEM drum decision of the same day)

Decision: The drum is one laser-cut 0.8 mm 304 sheet with fold-in tabs, wrapped around two laser-cut 2 mm 304 rings and bolted to them, a butt seam over a 1 mm splice strip, three catalog aluminum angle baffles, and four catalog dryer rollers on two bulkheads. Flat patterns are in `mechanical/drawings/drum-sheet.dxf`, `drum-ring.dxf`, `drum-splice.dxf`. The entry below this one, which chose a bought OEM drum, is reversed.
Why: No bought drum is documented. OEM listings publish no dimensions, so a design around one is a design around a measurement nobody can make before buying. The sheet-and-rings drum is documented by its own DXF, every piece is flat stock, extrusion, or catalog, and a damaged wall is one sheet to replace. The one real objection to a builder-made drum, that a faceted drum runs the belt over vertices, does not apply: a wrapped sheet is round because the rings are round, and 0.8 mm 304 at a 310 mm radius stays elastic, so no rolling is needed.
What is given up: certainty about roundness at mid-length until V-208 is run with a cheap material; about 90 M4 bolts; two people for the wrap.
Charter: follows the fabrication rule exactly (laser-cut flat stock, extrusion, and off-the-shelf parts) where the OEM drum only followed its letter. The 55 gallon stainless shipping drum, cut to length, is the documented no-fabrication alternative at about 150 L.
Affects: `docs/design-rules.md` 7a and 7b, `mechanical/cad/osa_dryer_cad.py`, `bom/bom.csv` CH-DRUM lines, `docs/verification.md` V-101 to V-105, V-016, V-017, V-208, `docs/build-guide.md` step 6.

## 2026-11-05  The mechanical source of truth is a parametric script; STEP and DXF are its exports

Decision: `mechanical/cad/osa_dryer_cad.py` (CadQuery, open source, Python) holds every mechanical number and writes every STEP file, every DXF flat pattern, the extrusion cut list, the check views, and runs an interference check. The STEP files are committed so the repo is useful without the script. FreeCAD opens the STEP files and runs the script through its CadQuery workbench.
Why: Design fully, then measure the bought parts, then cut. A drawing-by-drawing model cannot absorb a measured drum diameter without redrawing eight parts; a parametric one regenerates them and the diff shows what changed. The interference check found two real errors in the first pass that a stack of drawings would have carried to the cutter.
Charter: refines "FreeCAD and KiCad as native formats": the native mechanical format is open parametric code that FreeCAD runs, plus STEP. If a contributor prefers a FreeCAD document, the script is the thing to port, not the STEP files.
Affects: `mechanical/`, the charter's layout and native-format rule (amended in `osa-charter/CHARTER.md`).

## 2026-11-05  Drum: a bought OEM drum for the first build, a laser-cut stave drum as a later alternative

Decision: The first dryer uses a drum sold as a repair part for a current 27 in dryer family, with that family's rear rollers, front glides, felt seals, belt, idler, and lint screen. Its measured diameter and length are parameters of the model (V-101). The laser-cut stave drum (twelve flat 304 staves bolted to laser-cut end rings) is documented as the charter-pure alternative to be developed after the first build proves everything else.
Why: The drum is the one part a hobbyist cannot make from flat stock without a compromise: a faceted drum runs the belt over vertices, a rolled cylinder needs a shop, a stock stainless drum is the wrong size. The OEM drum and its wear parts have been catalog items for decades, which is what the charter asks of a part that wears. The first test run should not be the drum's test.
What is given up: an imperial, single-family drum in a metric machine; the bulkheads are drawn around it. The parametric model limits the damage to a parameter change if the family changes.
Charter: departs from "laser-cut flat stock, extrusion, or an off-the-shelf part" only in spirit; the drum is an off-the-shelf part, so it follows the letter. Logged because the stave drum was the intent.
Affects: `docs/design-rules.md` 7a, `mechanical/cad/osa_dryer_cad.py` drum parameters, `bom/bom.csv` drum family lines, `docs/verification.md` V-101 to V-105.

## 2026-11-05  Drive: dual-shaft NEMA 48 motor, catalog blower set, PJ pulley, OEM belt and idler

Decision: One dual-shaft NEMA 48 frame 1/3 hp 1725 rpm motor with a built-in thermal protector drives the blower wheel (front shaft, catalog wheel and housing with the inlet facing front) and the drum (rear shaft, PJ poly-V pulley, the drum family's belt and idler).
Why: The charter wants a standard frame motor. A single-shaft motor would need a second shaft and belt for the blower; a dual-shaft motor is a catalog item from several makers and keeps one belt. The blower set is a catalog item too. The appliance-market dryer motor was rejected because its mount, shaft thread, and pulley are proprietary.
What is given up: the appliance motor's built-in centrifugal heater switch, which the air-proving switch replaces (already decided).
Charter: follows.
Affects: `docs/design-rules.md` 7a, `bom/bom.csv` CH lines, `docs/verification.md` V-106, V-107, V-204.

## 2026-11-05  Frame and panel architecture

Decision: Four 4040 corner posts with three levels of 4040 rails, two 2020 tray rails, two 1.5 mm steel bulkheads hung between the mid and top rails, a bay ceiling plate on the mid rails, flat 1.5 mm panels bolted to the slots with M6 T-nuts at 150 mm pitch, a 45 degree wedge console of flat plates, a 2 mm ring-and-disc door. The mid front rail is two stubs so the lint duct can pass between them in front of the front bulkhead.
Why: Every piece is a square cut of extrusion or a flat laser-cut plate with round holes, which is the charter's fabrication limit. The bulkheads carry the drum loads into the rails, not into the panels, so a panel can come off without the drum moving. The lint duct in front of the bulkhead is the only way to make a flat-stock lint path that does not sit inside the drum, which the interference check proved.
Charter: follows.
Affects: `mechanical/`, `docs/design-rules.md` 7a, `bom/bom.csv`.

## 2026-11-05  Design fully, build once, with gates: docs/verification.md joins the layout

Decision: The dryer is designed completely on paper, then built once for a test run. Every reasoned number has a check in `docs/verification.md` with a gate (design review, parts in hand, bench, assembly, commissioning, test run), a method, a pass condition, and what it unlocks. Nothing is cut while its gate is open. The charter's layout gains `docs/verification.md`.
Why: The project's working mode. The alternative, buy a part and see, spreads surprises through the build; a gated plan puts them all at the gate where they are cheapest.
Charter: amends the layout (in `osa-charter/CHARTER.md`); the project copy of the charter needs the same line.
Affects: `docs/verification.md`, `docs/build-guide.md`, `osa-charter/CHARTER.md`.

## 2026-11-05  UCI-D aperture grows to 240 x 120 (draft 3)

Decision: The control panel aperture is 240 x 120, the faceplate 280 x 160, the hole pattern 260 x 140, and the module envelope 240 x 120 x 120 behind the panel plane.
Why: The Tier 0 timers are wall-box devices on a standard yoke about 106 mm long, which cannot pass a 100 mm opening. The maker's sheet gives the body as 70.9 x 40.6 x 30.2 mm; the yoke length and knob diameter are not on it and still need a part in hand. Changing the aperture now costs nothing; changing it after a chassis is cut costs a panel.
What is given up: 20 mm of console height.
Charter: follows (the UCI's own versioning rule says every change is logged here).
Affects: `controls/uci-spec.md` section 4, `mechanical/drawings/tier0-faceplate.dxf`, `mechanical/drawings/layout-concept.svg`.

## 2026-11-05  A 10 A supplementary breaker protects the 120 V side of the common power module

Decision: CB1, a 1-pole 10 A C-curve DIN supplementary breaker, sits in L1 ahead of the motor circuit and the 24 V supply. The heat module's mains path is not behind it.
Why: On the electric build the branch breaker is 30 A and the 120 V side is wired in 14 and 18 AWG. Residential dryers rely on their listing to cover that; this dryer has no listing, so the protection is brought down to the wire. On 120 V builds CB1 is redundant and harmless. The element path stays on the branch breaker because 30 A is what it needs.
What is given up: one more part, one more thing to trip. A C curve is specified so a motor start does not trip it; commissioning checks that.
Charter: follows (conservative, listed part).
Affects: `electrical/wiring/common-power-module.md`, `bom/bom.csv` CPM-CB1.

## 2026-11-05  The door interlock is two switches on one actuator

Decision: S1, a listed appliance door switch, opens the motor's 120 V line directly. S2, a listed snap-action switch on the same door actuator, gates the 24 V bus that every coil circuit and STAT_DOOR hang from. Opening the door opens both.
Why: The charter asks for a hardwired interlock in the mains path. One appliance door switch gives one contact rated for the motor, and that contact goes where the charter says. The 24 V side needs its own contact so that the chassis coil chain and the control module's STAT_DOOR follow the door without a relay in between. Two switches on one actuator is cheaper and simpler than one two-pole switch rated for both jobs, and the parts market has both in quantity.
What is given up: two switches to align in CAD instead of one.
Charter: follows, literally.
Affects: `electrical/wiring/common-power-module.md`, `controls/uci-spec.md` section 9, `docs/design-rules.md` 3.1, `bom/bom.csv` CPM-S1 and CPM-S2.

## 2026-11-05  Heat pump module is a sealed, pre-charged unit with a fixed-speed compressor

Decision: The heat pump heat module uses a refrigeration circuit bought as one sealed, charged part and never opened. Its compressor is fixed-speed and driven by a contactor from HEAT_EN through a listed anti-short-cycle timer. Inverter-driven compressors are excluded.
Why: The charter's fridge decision already says refrigerant loops are not hobbyist work; brazing and charging are out, and in the US handling refrigerant needs certification. An inverter compressor would put the OEM's board, with its firmware and single source, into the heat path, which breaks the Tier 0 rule. A contactor-driven fixed-speed compressor looks like an element from the chassis's point of view, so the same HEAT_EN chain serves it.
What is given up: the efficiency of a modulating compressor, and for now any dual-source promise. The only sealed units known to exist as parts are OEM dryer assemblies (Whirlpool W11551760, GE WE03X36780), single-source and unverified for compressor type. The module is specified in principle and blocked on sourcing, and the docs say so.
Charter: follows (sealed off-the-shelf unit, as for the fridge; Tier 0 works; interlocks independent of any board).
Affects: `docs/design-rules.md` 5.4, `controls/uci-spec.md` sections 8 and 9, `bom/heat-heatpump.csv`.

## 2026-11-05  Heat source is a swappable module: none, electric, gas, or heat pump

Decision: The cabinet base is a heat module bay with a fixed interface: a terminal strip (unswitched mains, a 24 V HEAT_EN permission, a dry HEAT_ON contact) and three mechanical features (tray rails, riser flange, blower outlet flange). The builder picks one of four heat modules; the module and the cord are the only things that change. Electric stays the reference build. Every build is first run with no heat module during commissioning. The heat module's own switching device and its own listed limits live on the module's tray, so the common power module ends at HEAT_EN.
Why: The requirement that a builder can choose gas or electric, run a heat pump, or run with no heat at all. The UCI-D already only asks for heat, so the controls do not change. One chassis, one build guide, one set of drawings serves every heat choice, and the no-heat first run proves the machine before anything hot goes in.
What is given up: the bay costs cabinet height and a riser duct that a dedicated electric dryer would not need, and the common power module carries the heat-enable chain even in a no-heat build (the BOM marks those lines as omittable).
Charter: follows (the same chassis, the same interfaces, different modules). Refines the 2026-11-05 relay-stage decision: the heater contactor is now on the heat module tray, still on the chassis side, still not on the control module.
Affects: `docs/design-rules.md` sections 1 to 5 and 7, `controls/uci-spec.md` sections 3, 6, 8, 9, `bom/`.

## 2026-11-05  Dryer design rules get their own file

Decision: Dryer-specific targets and rules live in `docs/design-rules.md`. The charter's repository layout gains the line `docs/design-rules.md  appliance-specific targets and rules that the CAD and schematic must meet`.
Why: The README is an overview and DECISIONS.md is a log. Neither is the place to state that the element is 5.6 kW or that the interlock chain runs at 24 V. Every appliance will need this file.
Charter: amends the layout. The amendment is in `osa-charter/CHARTER.md`. The copy of the charter in the project knowledge needs the same line.
Affects: `osa-charter/CHARTER.md`, `docs/design-rules.md`.

## 2026-11-05  Tier 0 keeps time with two spring-wound interval timers

Decision: The Tier 0 control module is two spring-wound interval timers (DRY TIME and HEAT TIME), an AIR / LOW / HIGH selector, a START button, and one hold relay. No timer motor, no electronics.
Why: A spring-wound timer needs no power, so the UCI can stay 24 V only. Several makers have sold them for fans, saunas, and lights for most of a century. Setting HEAT TIME shorter than DRY TIME gives a cool-down with no mechanism at all. The appliance cam timer was rejected because its motor needs mains and each timer is tied to one dryer model. A catalog electronic timer relay was rejected for the reference build because it has an IC inside, though it remains an acceptable Tier 0 alternative for a builder who wants one.
What is given up: a spring timer keeps running while the dryer is stopped (door open, power out), so an interruption costs that much dry time. Documented in the Tier 0 notes.
Charter: follows (Tier 0 is mechanical, no microcontroller, no firmware).
Affects: `controls/uci-spec.md` section 10, `controls/tier0-mechanical/`.

## 2026-11-05  Reference build is US 240 V split-phase electric

Decision: The first dryer is a vented electric dryer on a US 240 V, 30 A circuit with a NEMA 14-30 cord, a 5.0 to 5.6 kW element, and a 120 V motor. 230 V single-phase and gas are variants that swap the power module and heater on the same chassis and the same UCI-D.
Why: The deepest parts market in the world for a basic electric dryer, and it is where the first builder lives. The UCI-D does not care what makes the heat, so a variant costs a power module design, not a control redesign.
Charter: follows.
Affects: `docs/design-rules.md`, everything electrical.

## 2026-11-05  Control rail is 24 V DC

Decision: The chassis supplies one 24 V DC rail to the control module. Modules make their own 5 V or 3.3 V.
Why: 24 V DC is the industrial control standard. Interface relays, DIN power supplies, sensors, and terminal blocks at 24 V are catalog parts from many makers and will be for decades, and it has the noise margin to run through a dryer cabinet next to a contactor. 12 V was rejected for thinner industrial support. A second 5 V rail was rejected as one more part to fail, to save a buck module on the board.
Charter: follows (separate low voltage rail, isolated by a listed supply).
Affects: `controls/uci-spec.md` section 6.

## 2026-11-05  Mains relay stage lives on a fixed power module; the UCI is low voltage only

Decision: The contactor, relays, 24 V supply, and the whole interlock chain live on a power module that is part of the chassis. The control module, at every tier, only ever touches 24 V DC. Request lines are 24 V sinks: the module closes a contact or a transistor to 0V and a relay on the power module does the rest.
Why: The charter says nothing on a control board carries mains except a relay or SSR output stage. Read literally, every tier board would carry 240 V and the UCI connector would carry over 20 A of heater current. Moving that stage onto the chassis means the most disposable part never carries mains, a hobbyist can design a Tier 1 board with no creepage or clearance questions, the Tier 0 module can be bare timers, and there is no mains voltage anywhere in the console. This is how furnaces have separated the 24 V thermostat from the control board for seventy years, and that interface has outlived every board.
Charter: clarifies the electrical rule "nothing on a control board carries mains except a relay or SSR output stage, and that stage is physically separated" by making the separation a different box. The intent (the board only requests, listed parts do the switching, interlocks independent of the board) is kept in full. Recorded as a clarification, not a departure. When the charter is next revised, the wording should say the output stage may live on the chassis.
Affects: `controls/uci-spec.md` throughout, `electrical/`, `docs/design-rules.md` section 3.

## 2026-11-05  Repo created

Decision: osa-dryer created in the standard charter layout.
Why: Dryer first, per the charter decision log. It is the simplest appliance and exercises every rule including heat safety.
Charter: follows.
Affects: everything.
