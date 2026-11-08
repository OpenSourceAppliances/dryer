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

## 2026-11-07  The two-tone paint is distant blue and graphite grey

Decision: The Fusion model's paint scheme (2026-11-06, white and charcoal) changes to a blue and grey pair: the body panels (sides, upper front and rear, top) in RAL 5023 distant blue, the trim (console, door ring and disc, the lower front and rear panels) in RAL 7024 graphite grey. `fusion_motion.py` makes the two appearances in the design from the library's glossy enamel (`PAINT`), so a builder changes a colour by editing one line or the appearance in Fusion's own editor. The product renders in `mechanical/renders/` show this scheme.
Why: A real colour pair that a builder could order as powder coat, named by RAL number so it can be matched; it keeps the earlier rule that the dark trim marks what comes off for service. Still a presentation choice, not a specification: the build guide leaves colours to the builder.
Charter: follows.
Affects: `mechanical/cad/fusion_motion/fusion_motion.py` (draft 7), `mechanical/fusion/osa-dryer-parametric.f3d`, `mechanical/renders/`.

---

## 2026-11-07  In the parametric Fusion build the hardware is fixed bodies, not features

Decision: `mechanical/cad/fusion_build/fusion_build.py` draws every made part and every bought envelope as sketches, dimensions and features, and draws the bolts, nuts, washers and spacers (861 pieces in 45 hardware sets; the roller studs' 20 pieces are drawn with the drive as features, the other 841 as below) as fixed bodies built with Fusion's temporary-geometry tools from `hardware.json`, one base feature per hardware set, at the script's positions.
Why: a bolt as features is a revolve, a hex cut, two chamfers and a placement, five to eight timeline entries each, and Fusion's time per feature grows with the document (stage D's 150 features took 8 minutes; the plates' 133 patterned cuts took 3); 861 bolts that way would take hours and bury the editable parts under thousands of hardware entries in the timeline. A builder edits plates, bars and the drum, not bought stock, and the hardware follows the holes: when a parameter moves the holes, running stage F again redraws the hardware on them from the script's list. What is given up: the hardware does not move with a parameter change by itself.
Charter: follows (the editable form is the parts a builder makes; the hardware is catalog stock).
Affects: `mechanical/cad/fusion_build/`, `mechanical/cad/hardware.json`, `mechanical/cad/osa_dryer_cad.py` (the stock tags and the log in `place()`).

## 2026-11-06  The parts are finished in the script; the editable Fusion build is made at the end

Decision: The design is drawn to completion in `mechanical/cad/osa_dryer_cad.py` (draft 9 finishes the reference build's parts), with Fusion used as it is now: joints, motion, interference, a second kernel's measurements and the archive of record. When the parts are finished, the whole design is rebuilt once inside Fusion by a script of its own, from sketches, dimensions and user parameters, and that archive goes on GitHub as the version a builder edits in Fusion's own interface. Until then the imported archive is the editable form: bodies that can be pushed and pulled, not parameters.
Why: Finishing in the script keeps every change checked by two kernels on every run (the audit and the Fusion comparison caught the open door throat and a 13.5 mm3 screw clash that neither drawing by hand would have). A parametric Fusion build made now would have to be remade after every design change; made once at the end it is made once. A builder who wants to change a drum diameter or a cabinet width needs parameters, so the end-state build is not optional.
Charter: departs from "FreeCAD as the native format" as already recorded (2026-11-06, Fusion holds the design of record); the end-state build keeps the script, STEP and DXF as the open form beside it.
Affects: `README.md`, `mechanical/fusion/`, the task list for the Fusion build.

## 2026-11-06  The no-heat module is the electric module's box with nothing in it

Decision: The "none" heat choice (design-rules 5.1, part of every build and the first stage of every commissioning) uses the electric module's tray and duct box exactly as drawn (`heat-module-tray.dxf`, the four walls, the lid, the angles, the collar, the bonding stud), with no element, no element rails, no thermostats, no terminal plate and no devices. The element's terminal opening in the right end wall stays open. `bom/heat-none.csv` lists what to cut and what to leave out.
Why: Every build is run first with no heat module, so every builder makes this box anyway; a second, simpler blanking duct would be a second set of drawings to keep in step for no airflow gain (the box is an empty plenum from the louvers' side to the collar). An electric builder adds the element and the electrics to the same box later without taking the tray out of the rails' drawings. The open terminal hole and the thermostat holes in the lid draw bay air, which is room air through the louvers, into a duct that heats nothing; they are inside the louvered bay, so no lint path is opened.
Charter: follows (reference build first, parts shared across variants).
Affects: `docs/design-rules.md` 5.1, `bom/heat-none.csv`, `docs/build-guide.md`.

## 2026-11-06  Draft 9: the blower plate, the exhaust set, the chassis sensors, the blanked entries

Decision: The blower housing hangs on a 1.5 mm steel plate standing across the bay in front of it (260 x 245, on two 90 mm 20x20x2 angle feet bolted through the base pan with M6), with the spool's 140 x 120 bore cut through it and the spool's foam on its front face; the housing's own screws go into the plate on the bought housing's pattern (drawn on a nominal 176 x 120, V-107). The blower's discharge is the 102 round collar of design-rules 3.2 on its outlet box; a catalog 4 in aluminium pipe slides over it, runs along the bay floor's right side at X 230, Z 150, through the rear lower panel's 106 port and 50 proud of it as the vent hose spigot, held by a worm-drive clamp on the collar and a second clamp inside the panel that bears on it. The air-proving switch's tap is a 6.5 hole and a barb fitting on the pipe's top at Y 300, with a 6 mm tube over the thermostats to PS1 (its setpoint stays V-205). The two chassis sensors the UCI-D wires to J2 are placed: the exhaust thermistor on the bay side of the lint box's back plate, right of the spool, sensing through a 12 x 18 slot into the box; the moisture bar set on the front bulkhead's drum side at 58 degrees right of bottom on radius 250, its terminals through a 16 hole into the front gap, its pair sharing the door switch cable's two grommets, which grow from 12 to 16. The gas entry (25, for a 3/8 NPT bulkhead fitting) and the condensate drain (20, for a hose grommet) are cut in the rear lower panel at X -230, Z 150 and 66, and blanked on every other build by a 60 x 44 plate on two M4. The four cable clamp holes get their P-clips. 213 parts.
Why: These were the open items of design-rules section 11 (the blower mount and the duct details) and the two sensors the controls spec needs from the chassis. A plate the housing hangs on makes the spool-to-housing joint our own (a flat face with a known opening), so only the screw pattern waits on the bought housing; a sail switch or a tap on the housing itself would have waited on it too. A pipe through the panel as its own spigot is what every dryer does and needs no flanged collar that would have to join the pipe inside. The sensors go where the air is (the box) and where the clothes are (inside the ring bore, clear of the basket's lip and the felt). The entries are cut now because a panel is cut once; a blank is cheaper than a second panel drawing per variant.
Charter: follows (catalog parts, flat stock and angle, four fastener sizes; M4 x 16 and x 20 join the M4 line).
Affects: `mechanical/cad/osa_dryer_cad.py`, `mechanical/cad/cad_audit.py`, `mechanical/cad/expected-dimensions.csv` (Q rows), `docs/design-rules.md` (draft 9), `docs/verification.md` (draft 6), `electrical/wiring/common-power-module.md`, `bom/bom.csv`, `docs/build-guide.md`, `docs/maintenance.md`.

## 2026-11-06  No door window; a glazed door is a later upgrade

Decision: The door is a plain 2 mm steel disc. A window is not part of the design; a glazed door can come later as an upgrade with its own ring and seal, on the same hinges and catch.
Why: A window adds a glass panel, its retaining ring and a second seal for no drying benefit, and the disc is the simplest door a builder can make. Keeping the hinge and catch pattern lets a glazed disc replace it later without touching the panel.
Charter: follows (simplest reference build; upgrades stay compatible).
Affects: `docs/design-rules.md` 7a Door, 7 Door.

## 2026-11-06  Two-tone paint in the Fusion model; the interference check clips to the overlap

Decision: The Fusion appearances show the dryer as a builder would paint it: a warm white body (side, upper front and rear, and top panels) with a charcoal console, door and skirt (the lower front and rear panels). The paint is a presentation choice in `fusion_motion.py`, not a specification; the build guide leaves the colours to the builder. Separately, the script's own interference check now clips each pair of parts to their bounding-box overlap before intersecting them, because OCC's boolean of a small bolt against a large plate with many holes returned no overlap where Fusion found 13.5 mm3 (the lint box's lowest drum-side M4 heads in the bay ceiling's front edge, draft 8); the clipped pieces agree with Fusion and the screws moved from Z 300 to 310.
Why: A real colour scheme makes the Fusion views read as a machine rather than a diagram, and the two tones mark what comes off for service (the dark panels). The check change is a correctness fix: a silent zero from a failed boolean is worse than a slow check.
Charter: follows.
Affects: `mechanical/cad/fusion_motion/fusion_motion.py`, `mechanical/cad/osa_dryer_cad.py` (`--check`), `mechanical/cad/cad_audit.py`, `docs/verification.md` V-010, V-021.

## 2026-11-06  UCI-D aperture 560 wide, faceplate 620

Decision: The UCI-D aperture grows from 500 x 120 to 560 x 120 (`controls/uci-spec.md` draft 6), the faceplate to 620 x 160, the hole pattern to 590 x 140 with the two centre-line holes kept, and the module envelope to 560 x 120 x 120. The Tier 0 layout on the plate does not move.
Why: The Fusion view of the console showed 75 mm of bare face beside a plate with 37 mm above it. The console's posts are the limit: their inner faces are at plus and minus 305 and their bolt heads at 319, so a 620 plate (ending at 310) with its holes at 295 and the aperture at 280 is the most the face can carry while the nuts stay off the posts and the aperture keeps 15 mm of panel to them. More plate is room for the later tiers' displays. What is given up: the faceplate is 80 mm wider for the same Tier 0 controls, a slightly larger laser-cut part, and every number that quoted 500, 520 or 540 changes (spec, drawing, model, audit).
Charter: follows (the UCI is the one interface that every tier shares; widening it before a build costs nothing).
Affects: `controls/uci-spec.md` 4.1 to 4.3 and 10, `mechanical/drawings/tier0_drawings.py` (draft 4), `mechanical/cad/osa_dryer_cad.py`, `docs/design-rules.md` 7a Console, `controls/tier0-mechanical/README.md`, `bom/bom.csv` T0-FACE, the audit's K and H rows.

## 2026-11-06  Ducts are plates on flat bar frames; a throat liner closes the door opening

Decision: Every duct is made of 1.5 mm laser-cut plates screwed with M4 button heads into the tapped edges of aluminium flat bar frames: no bends, no rivets. The lint box (30 x 8 bars) hangs between the mid front stubs on two M8 button heads into the stubs' tapped end bores, with the front bulkhead as its back wall above 265 and a plate below; a spool of 40 x 8 bars carries the air from the box to the blower's inlet face against 6 mm foam. The riser is a hood of 25 x 8 bars over the heat module's collar, a trunk of two 50 x 8 bars standing on the hood's top plate, and a nozzle of 40 x 8 bars from the trunk's front plate to the rear bulkhead's hole field, held by M4 from the drum side through the bulkhead. A throat liner, a 1.5 mm aluminium strip rolled by hand to radius 235.5 and spliced at the top with two M3, stands between the door ring's back face and the front bulkhead; the lint box's plates and side bars end on an arc 0.2 outside it, so the liner is the box's top.
Why: Drawing the lint duct as a real part showed two things the envelopes had hidden. First, nothing bounded the throat between the ring and the bulkhead: the 40 mm gap behind the panel was open all round the opening, so the blower would have drawn most of its air from the room through that gap instead of through the heater and the drum. Second, the duct's top wall has to lie in the 8 mm annulus between the opening (radius 230) and the slot (238), which only a curved wall fits. The liner solves both at once and is the one rolled part, bent round a wooden form like the drum sheet. Flat bar frames give a square, stiff duct that a hobbyist can make with a hacksaw, a file, a drill press and a tap: the plates are laser cut, every joint is a screw into a tapped edge, and a damaged plate or bar is replaced alone. What is given up: a 2 mm foam joint or a tapped edge in 8 mm bar is a leak point that sheet-metal seams would not have; the spool's bottom bar covers the lowest 15 mm of the blower's 130 mouth (6 percent of its area, still over the 102 exhaust); a liner seam at the top and 0.2 mm of float; and more screws (40 in the lint box, 70 in the riser). Alternatives passed over: a rolled 1.5 mm top wall for the duct alone (a second rolled part, and still no throat), a polygon of short mitred bars (six pieces with angled ends), a 3D-printed duct (not in the charter's fabrication list, and the exhaust air is warm).
Charter: follows (laser-cut flat stock, extrusion, drill press, hand tools; the rolled liner is a hand operation round a form, the same as the drum sheet, and is flagged in the build guide).
Affects: `mechanical/cad/osa_dryer_cad.py` (the duct section), `docs/design-rules.md` 7a Air, 7a Door, 7a Bulkheads, 7 Lint management, 7 Access, `docs/verification.md` V-013, V-018, V-107, V-115, `bom/bom.csv` (CH-DUCTS, CH-LINER, CH-LINT), `docs/build-guide.md`.

## 2026-11-06  The lint filter is a mesh basket through the slot, lifted out through the door

Decision: The lint filter is a basket: stainless mesh wrapped round two laser-cut 3 mm sector plates (a lip on the drum side of the bulkhead with an opening the size of the basket, and a closed far end 2 mm behind the lint box's front plate), its edges folded 5 mm and clamped by two 1.5 mm plates on six M3 x 5 into the tapped plates at each end. It passes through the bulkhead slot, widened to radius 238 to 267, with 0.9 mm each side. A tab on the lip reaches into the door opening and carries a catalog 64 mm D-pull; the person opens the door, pulls the basket 40 mm back into the drum, and lifts it out. The lip rides inside the rings' 540 bore (its outer radius is 268.5) and outside the opening (232).
Why: The slot is curved, so a flat screen cannot slide in it; a basket is the shape that fits a curved slot and still comes out through the door, which the design rules require (no tools, from the front). Mesh clamped between plates needs no welding or rivets. The outer wall of the basket faces down into the lint box and alone offers 9060 mm2 inside the box, above the 8171 mm2 exhaust; the inner wall and the ends add more. What is given up: the basket's 0.9 mm slot clearance is a bypass that the OEM plastic screens also have, and the pull sits at the bottom of the throat where a sock can rest against it. The M3 heads stand 1.65 proud on the lip's clamp inside the drum's open end, 2 mm in front of the ring.
Charter: follows (catalog mesh and pull, laser-cut plates, hand tools; the folds in the mesh are made by hand).
Affects: `mechanical/cad/osa_dryer_cad.py` (basket, the slot's outer radius), `docs/design-rules.md` 7a Bulkheads, 7 Lint management, `docs/verification.md` V-018, `docs/maintenance.md`, `bom/bom.csv` (CH-LINT).

## 2026-11-06  Door switch, air-proving switch and exhaust thermostats are placed

Decision: The door switch is a plunger switch behind the front upper panel on the ring bolts' radius, 45 degrees right of bottom, its plunger through the ring and the panel so the closed disc presses it; two M4 into its ears outside the ring. The air-proving switch PS1 stands on a 20x20x2 angle bracket on the base pan at the right front, in front of the blower's outlet box. The thermal fuse TF2 and the cycling thermostats T_HI and T_LO sit on the blower's outlet box with the kit's screws. The motor's two cradle brackets take two M6 each through the base pan, with nuts on their feet. All four are envelopes until the parts are measured (V-107, V-115, V-205).
Why: The wiring document names these parts and the design rules put the door switch in the motor line; the model now gives each a place that nothing else wants, so the harness route can be written. The switch's plunger position was chosen clear of the lint box (which fills the bottom of the throat), the ring bolts, and the hinges on the left. What is given up: the switch's ears sit outside the ring on the painted panel, two visible heads beside the door; PS1's pressure tube is not drawn.
Charter: follows (hardware interlock in the motor line first; listed parts from two makers, uci-spec section 13).
Affects: `mechanical/cad/osa_dryer_cad.py`, `docs/design-rules.md` 7a Door, 7a Drive, 7a Panels, `electrical/wiring/common-power-module.md` (harness route), `bom/bom.csv`.

## 2026-11-06  Fusion holds the design of record; no KiCad schematic

Decision: The mechanical design of record is the Autodesk Fusion archive `mechanical/fusion/osa-dryer-assembly-motion.f3d`: the model as imported from the script's STEP output, with its joints and appearances, checked for interference and re-measured by Fusion's own kernel. The CadQuery script stays the place every number lives and the way the files are regenerated; the STEP files and DXF flat patterns are the neutral exports anyone can open, FreeCAD included. No KiCad schematic is drawn: the electrical design is `electrical/wiring/common-power-module.md` with its terminal map and wire list, and the ladder drawings `ladder.py` writes. The empty `electrical/schematic/` folder goes.
Why: Fusion is what the designer runs the checks in and what a builder will open, and its free personal license is enough for one dryer. Keeping the open exports beside it means nobody needs Fusion to cut a plate or read a dimension. A KiCad schematic of a two-relay, one-contactor machine would repeat the ladder drawings in a second format with nothing added; the wiring document already carries every terminal number and wire. What is given up: a native FreeCAD document and a KiCad project, which the charter named as the formats; a contributor who wants either can make them from the script and the wiring document.
Charter: departs from "FreeCAD and KiCad as native formats" for this appliance, on the grounds above. The charter copy in the project knowledge needs a line saying an appliance may name its design-of-record tool in `DECISIONS.md` as long as open exports (parametric source, STEP, DXF, plain-text wiring) are kept beside it.
Affects: `README.md`, `docs/design-rules.md`, `docs/verification.md` (V-002), `electrical/wiring/common-power-module.md`, `controls/uci-spec.md` section 9, the charter.

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
