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

## 2026-11-06  Every bought part is drawn from published figures before the first build

Decision: Until a part is in hand, the model draws it as an envelope or a representation taken from the maker's datasheet where there is one, otherwise from a seller's listing, and the verification plan names the measurement that confirms each figure (V-106, V-108, V-112 and the parts-in-hand gate). A figure that came from a listing rather than a datasheet is marked as such in the model and the BOM. Nothing is cut whose dimensions depend on an unconfirmed figure.
Why: The first build cannot wait on parts to measure, and the charter wants a complete design before anything is bought. Drawing from published figures lets the whole machine be checked for fit and clearance on paper; the gates in `docs/verification.md` keep an unconfirmed number from reaching a laser cutter. The risk accepted is a parameter change after the parts arrive, which the model is built to take.
Charter: follows (document everything; build once with gates).
Affects: `mechanical/cad/osa_dryer_cad.py` (every bought part), `docs/verification.md`, `bom/`.

## 2026-11-06  The common power module is a plate behind the rear bulkhead, serviced from the back

Decision: The common power module leaves the bay. It is a 150 x 720 x 1.5 laser-cut plate bolted to the rear faces of the two rear cross rails, in the dead space left of the riser behind the rear bulkhead, with five short horizontal DIN rails facing the back, a cover over the three mains rails and a barrier under the two SELV rails. It is reached with the rear upper panel off. The cord still enters through the base pan and goes up through a grommet in the bay ceiling; the bay harness goes down through a second grommet and the console harness up through one in the top panel. `electrical/wiring/common-power-module.md` keeps its designators and wire list; its "two rails A and B" become A1 to A3 and B1 to B2.
Why: Draft 6 put the module in a 170 x 250 x 180 box at the rear left of the bay, but the drive on the centre line, the heat module tray, the exhaust on the right and the cord bushing left it no room, and a box in the bay sits in the heat module's draught. The space behind the rear bulkhead left of the riser is 155 wide and 620 tall and holds nothing else; it is dry, cool, and two bolts from the rear panel. The alternatives were to shrink the heat module tray (it cannot: the element sets its length) or to stack the module above the drive, where it would block the belt. What is given up: two panels now carry electrical things (the rear lower panel gives the heat module's terminals, the rear upper panel the power module), which section 7 Access records; and a harness runs 300 mm down the back of the bulkhead to the bay.
Charter: follows (catalog parts, one panel off for service, mains separated from SELV by a barrier).
Affects: `docs/design-rules.md` sections 4 and 7a, `mechanical/cad/osa_dryer_cad.py`, `electrical/wiring/common-power-module.md`, `docs/maintenance.md`.

## 2026-11-06  The electric heat module is a bolted duct box with the catalog element inside; the drum rides on glides and shoulder screws; the pulley is 20

Decision: Draft 7 of the model draws the electric heat module: a 1.5 mm laser-cut duct box (290 x 205 x 110) on the tray, every edge joined with 20x20x2 aluminium angle and M4 button heads with nuts, the catalog open-coil element on its frame on two angle rails inside, a 125 round catalog starting collar on the lid that stands under a hole in the riser's hood with a foam ring between, the thermostats on the lid, and the contactor and terminal strips on a DIN rail on a plate behind the box. The tray rails run the full depth of the cabinet and the tray bolts to them with M4 T-nuts. The drum is located endways by two nylon glides on each bulkhead, with the felt in two arcs round them, and the rollers turn on ISO 7379 shoulder screws (10 x 35, M8) through the bulkheads at 32 degrees each side of bottom. The motor pulley is 20 mm.
Why: Section 5.2 preferred an appliance-market element assembly, but those cans are straight through (air in one end, out the other) and the chassis wants the module's outlet on top under the hood, which would need an elbow and a second box; the element on its own frame is a listed subassembly and the box is plain flat stock. Rivets would be the usual way to join a sheet box, but section 8 rules them out, so it is bolted. The 2020 tray rails take M4 or M5 T-nuts, not the M6 draft 2 named. Drawing the drum support showed that nothing located the drum endways (the felts only seal) and that the rollers had no stud: the glides and the shoulder screws are the catalog answer, and moving the rollers from 30 to 32 degrees keeps the front studs' nuts out of the lint duct. Checking the drive ratio showed the 30 pulley of drafts 3 to 6 gave 83 drum rpm, far above the 45 to 55 target; 20 gives 56. What is given up: the box has 64 M4 bolts where a riveted one would have none to undo; the collar's gasket is a sliding foam ring rather than a bolted flange, so the hood's seal depends on the tray being pushed home.
Charter: follows for the box (flat stock, angle, catalog fasteners), the glides and the studs. Departs from the fastener line in section 8 of the design rules (M6 for the tray, the heater box and the power module box) by using M4 there; the charter's four-size budget is kept.
Affects: `docs/design-rules.md` 3.2, 5.2, 7, 7a, 7b, 8; `mechanical/cad/osa_dryer_cad.py`; `bom/bom.csv`, `bom/heat-electric-240.csv`; `docs/verification.md`.

## 2026-11-06  UCI-D aperture 500 wide

Decision: The UCI-D aperture grows from 240 x 120 to 500 x 120 (`controls/uci-spec.md` draft 5): faceplate 540 x 160 on six M4 screws (the 520 x 140 corner pattern plus one hole at the middle of each long edge), envelope 500 x 120 x 120 behind the panel plane. The Tier 0 faceplate (draft 3) spreads its two knobs, the selector and START across the plate. The console frame does not change.
Why: The aperture is the one chassis dimension that every control module ever built for this dryer inherits, and 240 was sized to the four Tier 0 controls with nothing to spare. A later module would have had to choose between those controls and a display. 500 is what the console as drawn gives with margin (the posts' bracket bolt heads are 295 from the centre line each side, so the envelope clears them by 45), and it holds a 7 inch class display beside a row of buttons, or two Eurocard boards, or a Tier 3 screen. What is given up: a 540 mm plate needs six screws instead of four, and the Tier 0 plate is mostly blank aluminum.
Charter: follows (the control interface is specified once and outlives the boards; a screen is a Tier 3 accessory and this gives it a place without touching the chassis).
Affects: `controls/uci-spec.md` 4.1 to 4.3 and 10, `mechanical/drawings/tier0_drawings.py` and `tier0-faceplate.dxf` / `.svg`, `mechanical/cad/osa_dryer_cad.py`, `mechanical/cad/expected-dimensions.csv`, `docs/design-rules.md` 7a Console, `docs/verification.md` V-015, `controls/tier0-mechanical/README.md`, `bom/bom.csv` T0-FACE and CH-BOLT-M4.

## 2026-11-06  Every M4 is a button head with a hex socket

Decision: All M4 fasteners on the dryer are button head socket screws (ISO 7380, 2.5 mm hex key): the drum's 76 tab and seam bolts, the door ring's eight, the hinge lift-off halves' four, the control faceplate's four, and the DIN rail and clamp screws to come. The M4 row of the fastener budget (design-rules section 8) changes from pan head Phillips to button head, and the service set gains a 2.5 mm hex key (and a 4 mm one for the two countersunk M6 hinge screws).
Why: The draft 5 model had drawn button heads inside the drum (low, round, nothing for a sock to catch on) and Phillips pan heads in the budget, so two head types, two tools and two bolt families for one size. One head type and one key is the smaller service set in practice; a 2.5 mm key is as common as a Phillips driver and does not cam out. Pan heads with washers were the alternative, and they would have been proud inside the drum. What is given up: the charter's exact service-set target (10 and 13 mm sockets, Phillips, multimeter) now reads plus two hex keys; the Phillips driver stays for M3 and for screws that come with bought parts.
Charter: follows the fastener rule (hex head or socket head; button heads are socket heads). Adds to the service-set target, which the charter states as a target, not a rule.
Affects: `docs/design-rules.md` section 8 and 7b Hardware, `bom/bom.csv` fastener lines, `controls/uci-spec.md` 4.2 (faceplate fasteners), `mechanical/cad/osa_dryer_cad.py`.

## 2026-11-06  The console is a 200 mm box on its own 4040 frame, deep enough for the whole UCI-D envelope

Decision: The console becomes a vertical box across the rear of the top, 200 tall, from the top rear cross rail (Y 611.5) to the back, built like the cabinet: four 4040 posts standing on the top panel, four rails at the top, twelve inside corner brackets with M6 hardware, and five flat plates (face, cap, rear, two cheeks) bolted into its slots. The face plate carries the UCI-D aperture 83 above the top panel. The machine is 1203 tall on the frame (1221 on the feet), up from 1113. The 45 degree wedge of drafts 3 to 5 is dropped.
Why: Draft 5 found that the wedge could not hold the UCI-D envelope (240 x 120 x 120 behind the panel plane): the envelope ran into the drum compartment. The choice was between a console shaped around today's Tier 0 parts and one shaped around the envelope that every future module is promised. A box 138.5 deep holds the envelope with 18 to spare and keeps every chassis part out of it, which is what makes a Tier 1, 2 or 3 module a drop-in forty years from now. A small frame rather than bent sheet keeps the fabrication rule (flat plates and extrusion, no brake) and makes the console as stiff as the cabinet, so leaning on it or turning a stiff knob does not flex a plate. Its front posts stand over the cabinet's top rear cross rail and its rear posts over the rear posts, and the foot brackets bolt down through the top panel into those rails' slots, so the load goes into the frame. What is given up: 90 mm of height, eight more extrusion cuts, twelve brackets and 24 bolts, and the sloped face that was easier to read from above.
Charter: follows (extrusion, flat stock, catalog brackets, the control interface isolated from the chassis).
Affects: `docs/design-rules.md` 7a Console, 7 Outside size, `mechanical/cad/osa_dryer_cad.py`, `mechanical/drawings/console-*.dxf`, `frame-cut-list.csv`, `bom/bom.csv` console lines, `docs/verification.md` V-015, V-019, `controls/tier0-mechanical/README.md`.

## 2026-11-06  The heat module leaves by the back; the cord enters through the base pan

Decision: The heat module tray slides out the back of the bay with the rear lower panel off. The riser's bottom rises from 180 to 230 and the riser gains a 300 x 28 hood that reaches forward over the module's top-rear outlet collar (240 x 60 at Y 580 to 640, up to 229), so nothing of the riser reaches below 230 and the module (222 tall, 229 with its collar) passes under it. The cord's strain relief bushing moves from the rear lower panel to the base pan under the power module, and the cord runs under the pan to the back in the 18 mm the feet now give (feet 10 pad plus 8 hex, up from 14).
Why: The draft 5 motion check found the tray's front path blocked by the motor, pulley, blower and belt, which stand on the centre line, and its back path blocked by the riser. Moving the drive off the centre line would have put the pulley off the drum's middle and the belt at an angle; the back exit costs only a hood on the riser and a different panel to take off. The rear lower panel already comes off for the power module and the motor, so the access rule (one panel per job) still holds, and the cord no longer passes through the panel that comes off. What is given up: the module cannot be changed from the front in a tight alcove; the machine has to be pulled out, as it does to vent it anyway.
Charter: follows (any wear part reachable by removing one panel; every subassembly removable as a unit).
Affects: `docs/design-rules.md` 7a Air and Panels, 7 Heat module bay and Access, 7c Feet, `mechanical/cad/osa_dryer_cad.py`, `mechanical/drawings/base-pan.dxf`, `rear-lower-panel.dxf`, `bom/bom.csv` (feet, cord bushing note), `docs/verification.md` V-021, V-022, `mechanical/cad/fusion_motion/fusion_motion.py`.

## 2026-11-06  Lint slot: a curved slot inside the rings' bore; the bore grows to 540

Decision: The drum rings' bore grows from 480 to 540 (ring 270 to 309.2) and the lint slot becomes an annular sector in the front bulkhead between radius 238 and 266 about the drum axis, 36 degrees each side of straight down (8867 mm2). The 460 door opening stays. The felt seals move out to radius 273 to 291 on both bulkheads, riding the ring faces inboard of the tabs, which shrink to 16 tall (holes on 301.2) so the felt has a smooth 18 mm face. The front felt is now drawn.
Why: Draft 5 found that the straight 260 x 40 slot sat in the front felt's band, outside the ring bore and at its ends outside the drum: air leaving the drum would have had to pass between the ring face and the bulkhead. Three options were on the table (V-016): shrink the door opening to 400 and put the slot inside the 480 bore, keep the opening and grow the bore, or put the filter in the door. Keeping the 460 opening was chosen for the user (the opening is what makes a dryer easy to load) and growing the bore costs nothing but a different ring DXF and a slightly larger felt. The filter-in-the-door option was not taken because it puts a serviced part on the moving part and is harder to draw from flat stock. What is given up: 30 mm of ring face width (still 39 mm) and a slot area 12 percent smaller than the straight one (8867 against 10057, still 8 percent over the blower outlet). The lint screen that fits the curved slot is V-018.
Charter: follows (laser-cut rings and bulkhead; the screen will be a catalog mesh in a laser-cut frame).
Affects: `docs/design-rules.md` 7a Bulkheads, 7b Rings, Sheet and Seals, 7 Lint management, `mechanical/cad/osa_dryer_cad.py`, `mechanical/drawings/front-bulkhead.dxf`, `drum-ring.dxf`, `drum-sheet.dxf`, `felt-seal.dxf`, `bom/bom.csv` felt and lint screen lines, `docs/verification.md` V-013, V-016, V-018.

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
