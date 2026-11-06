# Verification plan

Draft 1, 2026-11-05. Status: the plan is complete for the electric reference build; every check is open until someone signs it.

The dryer is designed fully on paper, then built once and run once. This document is how that works without a surprise at the end: every number that came from reasoning instead of measurement has a check, every check has a gate, and nothing is cut, bought twice, or powered until the gate before it is closed. The checks are the design's honesty made into a list.

## How to use it

- Each check has an ID. Gate 0 is paper only. Gate 1 is parts in hand. Gate 2 is sub-assemblies on the bench. Gate 3 is the assembled machine without power. Gate 4 is `docs/commissioning.md`. Gate 5 is the test run.
- "Unlocks" says what may happen once the check passes. A DXF whose check is open is not sent to the cutter.
- "Regenerate" means: put the measured number into `mechanical/cad/osa_dryer_cad.py`, run it, and look at the diff of the DXFs and the cut list before ordering anything.
- Sign a check by writing the date, the measured value, and your initials in the Result column, and keep a photo in `builds/<your build>/`.
- A check that fails is not reworded. It gets a `DECISIONS.md` entry and a design change, then it is run again.

## Gate 0: design review, paper only

| ID | Check | Method | Pass when | Unlocks | Result |
| --- | --- | --- | --- | --- | --- |
| V-001 | Every document against the charter | Read `README.md`, `docs/design-rules.md`, `controls/uci-spec.md`, `electrical/wiring/common-power-module.md`, `controls/tier0-mechanical/README.md` against the ten core principles and the electrical rules | No rule broken without a `DECISIONS.md` entry | Gate 1 purchasing | |
| V-002 | One pin table everywhere | Compare J1 and J2 pin numbers and names across the UCI spec, the wiring doc, both ladder SVGs, the Tier 0 wiring SVG, and the commissioning checklist | Identical | Gate 1 purchasing | done 2026-11-05 by the author; repeat after any edit |
| V-003 | Interlock truth table | Walk `ladder-common-power-module.svg` for each of: door open, no airflow, TF2 open, T_HI open, T_LO open, module removed, J1 pins 3, 4, 5 shorted together, J1 pin 11 shorted to pin 9, heat module absent | In every row the heat module cannot be energized unless door closed and airflow proven and limits closed and a request present; the motor cannot run with the door open | V-201 | |
| V-004 | Contactor and relay ratings | Datasheets of HE-K_HEAT, CPM-K_MOTOR, CPM-RLY: AC-1 at 240 V for the element current, AC-3 or hp at 120 V for the motor FLA and LRA, DC coil suppression present or a diode added on the ladder | Every rating has margin over the load; suppression accounted for | Purchasing those lines | |
| V-005 | 24 V budget | Module 1.0 A + K_MOTOR coil + K_HEAT coil + three interface relay coils + three PTC lines against the PSU rating; PSU inrush against F1 | Total under 2.5 A with margin; F1 holds the inrush per the PSU sheet | Purchasing CPM-PSU, CPM-F1 | |
| V-006 | CB1 against the motor start | Motor LRA from its sheet against the C-curve trip band of CB1 | LRA inside the no-trip region for the start duration | Purchasing CPM-CB1 | |
| V-007 | Wire gauges | Each wire-list gauge against its current and against the breaker ahead of it (30 A branch for the element path, CB1 for the 120 V side) | No wire smaller than its protection allows | Buying wire | |
| V-008 | Heater-box limits against element current | Datasheets of HE-TF1 and HE-T_HL | Rated at or above the element current at 240 V; otherwise move the under-rated one to the coil circuit and log it | Purchasing HE lines | |
| V-009 | Thermostat settings against the fault rule | L-ratings of CPM-T_HI and CPM-T_LO against the 40 °C threshold in UCI 8.4 and the 60 to 70 °C exhaust target | Closing temperatures above 40 °C; opening temperatures inside the target | Purchasing thermostats | |
| V-010 | CAD interference and dimensional audit | Run `osa_dryer_cad.py --check` (pairwise overlap of every solid), then `cad_audit.py` on the written files: every STEP re-read and measured (solids, validity, closed shells, bounding box, volume, every cylindrical surface and every planar face), every flat part sectioned and every loop classified, every DXF read and matched loop by loop to its STEP section, the rolled drum parts unwrapped onto their flat patterns, every M6 hole checked to sit on a rail centre line, the assembly re-imported and re-checked for overlap, and 269 values stated in the documents compared with the files | No overlap; no audit failure; the report in `mechanical/cad/audit/audit-report.md` | Cutting anything | interference option run 2026-11-05: no overlaps after the bay rework (first run found 13). Audit written and run 2026-11-05: 269 document checks and 378 generic checks pass. The audit found what the interference check could not: the console face plate sloped the wrong way (minus 45 instead of plus 45 about X), the bay ceiling plate in three pieces, a cord hole through an M6 hole, two louver columns through the exhaust port, M6 holes on the front lower panel where no rail is (the lint duct gap), the drum belt track 77 mm from the pulley, and the rollers overhanging the drum end. All fixed in the model and the documents. |
| V-011 | Hole sizes against the fastener budget | `cad_audit.py` lists every circle diameter in every DXF and in every STEP and allows only the named set | Only 4.5 (M4), 6.5 (M6), 8.5 (M8) plus part-specific holes that are named (10 inlet, 10.5 roller shafts, 22 cord bushing, 106 exhaust port, the door and ring openings, 22.3 devices and 12 timer shafts on the Tier 0 faceplate) | Cutting | run 2026-11-05 in the audit: every diameter is on the list |
| V-012 | Belt length | The model prints the two-pulley estimate (2214 mm for a 620 drum and a 30 mm pulley at 511.5 mm centers). Pick the nearest catalog J-section poly-V length and place the idler so its take-up covers the difference | A catalog belt fits inside the idler's take-up range | V-105, motor position | |
| V-013 | Air path areas | Blower outlet area against the riser (260 x 50), the lint duct (336 x 36), the lint slot (260 x 40), the rear inlet hole field (126 x 10 mm), the exhaust (102 round); `cad_audit.py` computes them from the measured features | Nothing in the path smaller than the blower outlet; inlet field at least equal | Cutting bulkheads and ducts | run 2026-11-05 in the audit with 10 mm inlet holes: riser 13000, lint duct 12096, lint slot 10057, inlet field 9896, exhaust 8171 mm2, all at or above the 102 mm outlet (8171) |
| V-014 | Independent kernel re-measure | Open every STEP in Autodesk Fusion and run `mechanical/cad/fusion_audit/fusion_audit.py` there: it measures every body (volume, bounding box, faces, every cylindrical surface) and the chosen clearances with Fusion's own kernel and writes `audit/fusion-measured.csv`; then `cad_audit.py --fusion` compares the two records body by body and feature by feature | Every volume within 0.01 percent, every bounding box and every cylinder axis within 0.02 mm, every clearance within 0.02 mm; face counts may differ (the kernels split periodic faces differently) and are reported, not failed | Cutting anything | run 2026-11-05 in Fusion 2706.1.17: 105 bodies (46 part files and the 59-solid assembly), 1352 cylinders, 44 clearances; 423 comparisons pass. Every bounding box identical to 0.0000 mm, every volume within 2 ppm, every hole and round surface matched with no extras, every clearance identical. One CHECK: Fusion counts 450 faces on the drum sheet where OpenCascade counts 480, because it merges the tab root faces into the shell; same volume, same features. Visual and Measure-tool check 2026-11-06: the assembly opened in Fusion through File > Open, looked over from the six views inside and out, and 23 dimensions read from Fusion's Measure dialog by clicking faces, edges and bodies (drum 620, door opening 460 on the axis, cabinet 690 x 750 x 1001.5, UCI aperture 240 x 120 with 4.5 holes on 260 x 140, clearances 35 / 20 / 7.7 / 9.2 / 0 / 2, console 113.137, port 106, cord 22, rings 618.4 and 548 apart); all as documented. Record and screenshots: `mechanical/cad/audit/fusion-visual-check.md`. |
| V-014 | Heat module fits the bay | Element assembly outline against the tray envelope (320 deep x 160 tall above the tray, 200 clear height in the bay) | Fits with 20 mm of air around it | HE-TRAY drawing | |
| V-015 | Console aperture against the Tier 0 parts | Timer yoke, knob, 22 mm devices, K1 rail against the 240 x 120 x 120 envelope | Everything inside | T0-FACE cutting | needs V-110 |
| V-016 | Door against the drum | Door opening 460 inside the ring opening 480; felt annulus 250 to 285 lands on the ring face between the tabs (outside 289) and the opening; door disc 540; hinge load | Everything inside its zone with margin | Front bulkhead and door DXFs | |
| V-017 | Drum support geometry | Roller positions (310 + roller radius, plus or minus 30 degrees) on both bulkheads against the chosen roller's diameter and shaft | Rollers touch the sheet over the rings, the roller tracks on the sheet carry no fasteners, nothing else touches the drum | Rear and front bulkhead DXFs | needs V-102 |
| V-018 | Lint screen fits the slot | Choose a lint screen family; slot 260 x 40 against it | The screen's frame seats in the slot and pulls out through the door opening | Front bulkhead DXF | |
| V-019 | Height and reach | Total height 1113 against the laundry space; door opening bottom at 401 above the floor; console face reachable | Fits the space; a person can reach the drum bottom | Nothing; information | |
| V-020 | Scope of the first test run | Electric reference build only, Tier 0 only, no gas, no heat pump | Stated in `builds/` before buying | Gate 1 | |

## Gate 1: parts in hand, nothing cut yet

Measure, write the numbers into the CAD parameters, regenerate, read the diff, then order the laser cutting.

| ID | Check | Method | Pass when | Unlocks | Result |
| --- | --- | --- | --- | --- | --- |
| V-101 | Drum sheet stock | Confirm the cutting service cuts 0.8 mm 304 at 1945 x 590 in one piece, and what the kerf and tab accuracy are | A single blank; tab fold lines marked by the cutter or by hand from the DXF | Ordering the drum sheet | |
| V-102 | Rollers | Measure roller OD, shaft diameter, how the shaft mounts (stud, clip, bolt) on the chosen roller | `roller_d`, `roller_shaft_hole_d`, mounting method drawn | Both bulkhead DXFs | |
| V-103 | Drum rings | Measure the cut rings: outside diameter against the sheet's inside (618.4), flatness, hole circle | Rings round within 0.5 mm; holes match the tabs | V-208 | |
| V-104 | Felt strip | Width, thickness, adhesive, temperature rating | Annulus 250 to 285 covered with the strip laid in a ring; compressed thickness sets the bulkhead gap | Bulkhead felt | |
| V-105 | Belt and idler | Belt length and rib count bought; idler diameter and spring rate | V-012 recomputed with real numbers; motor pulley position fixed | Motor mount plate | |
| V-106 | Motor | NEMA frame base pattern, shaft diameter and length both ends, FLA and LRA, thermal protector type | Mount plate holes drawn; V-004, V-006 confirmed with the nameplate | Motor mount, K_MOTOR, CB1 | |
| V-107 | Blower set | Housing outlet size and orientation, inlet diameter, wheel bore and rotation direction | Lint duct and exhaust adapters drawn; wheel bore matches the motor shaft | Lint duct, exhaust adapter | |
| V-108 | Element assembly | Box outline, terminal positions, mounting flanges | Tray drawing completed; V-014 confirmed | HE-TRAY DXF | |
| V-109 | Thermal fuses and thermostats | Tab size, mounting hole spacing, body size | Brackets drawn on the blower housing and the element box | Brackets | |
| V-110 | Timers | Yoke length, shaft diameter, knob diameter, body depth | `tier0_drawings.py` parameters updated; V-015 confirmed | T0-FACE DXF | |
| V-111 | Air-proving switch | Port size, mounting, pressure range | Tube routing and tap drawn | V-205 | |
| V-112 | Power module parts | Total DIN rail length of everything on rail A and rail B, PSU footprint, terminal block widths | Power module box drawn around them | Power module box DXF | |
| V-113 | Extrusion and hardware | Slot width, T-nut fit, whether the extrusion's bore takes an M8 tap for the feet | Feet method confirmed | Frame cutting | |
| V-114 | Connectors intermate | Mini-Fit Jr. and XH parts from the two makers plug together and latch | Yes | Harness making | |
| V-115 | Door hardware | Hinge and latch dimensions | Front panel holes drawn | Front upper panel DXF | |

## Gate 2: bench tests, before the frame exists

| ID | Check | Method | Pass when | Unlocks | Result |
| --- | --- | --- | --- | --- | --- |
| V-201 | Power module on the bench | Wire it complete in its box. Lamps as loads: a 120 V lamp on X3 for the motor, a 240 V lamp (or a second 120 V lamp L1 to N) on a test tray for the heat module. Door switches, PS1, TF2, T_HI, T_LO on flying leads. Run commissioning stages 1 and 2 with the test plug, with PS1 operated by hand (blow into its tube) | Every line of stages 1 and 2 ticks | Fitting the power module to the frame | |
| V-202 | Tier 0 module on the bench | Plug into the bench power module; run commissioning stage 3 | Every line ticks | Fitting the module | |
| V-203 | Electric heat module on the bench | Element resistance, TF1 and T_HL continuity, K_HEAT coil resistance, tray bonding. The element is never energized outside the chassis | All as expected | Fitting the tray | |
| V-204 | Motor and blower | Motor on its mount plate on the bench with the blower, run from the bench power module through K_MOTOR: direction, current against FLA, vibration, noise, the thermal protector does not trip in 20 min | Current within nameplate; no trip | Fitting the drive | |
| V-205 | Air-proving setpoint | Blower, 1 m of duct, PS1 on its tap, a manometer. Find the pressure with a clean inlet and with the inlet half blocked. Set PS1 to close at a clean inlet and open before half blocked | A setpoint exists with margin both ways; record it in `bom.csv` CPM-PS1 and on the PS1 label | Fitting PS1 | |
| V-206 | Faceplate fit | The cut faceplate with both timers, the selector, the button, and K1 fitted | Everything fits and clears the aperture band | Module assembly | |
| V-207 | Bulkhead and drum dry fit | Rear bulkhead with rollers on two sawhorses, drum on the rollers, front bulkhead held against it: turn the drum by hand | Drum turns on the rollers, ring faces land on the felt, nothing else touches | Frame assembly | |
| V-208 | Drum wrap, cheap material first | Wrap a 0.5 mm aluminum flashing or heavy card blank cut to the sheet DXF around the real rings and bolt the tabs. Measure the diameter at mid-length at four angles. Hang a 5 kg weight on a strap over the belt track (352 from the front edge) to mimic belt pull and measure again. Press a roller against the sheet at the ring with 50 N and look for a dent. Then wrap the stainless | Mid-length out-of-round under 3 mm free and under 5 mm loaded; tabs land on the ring holes without forcing (the model assumes a sharp fold; if the real fold moves the hole, change `tab_h` or the hole offset in the model); no dent at the roller; two people can close the seam | Cutting the stainless sheet, V-207 | |

## Gate 3: assembled, unplugged

Done step by step inside `docs/build-guide.md`; listed here so none is skipped.

| ID | Check | Pass when |
| --- | --- | --- |
| V-301 | Frame square and level | Diagonals equal within 2 mm on every face; feet set |
| V-302 | Every T-nut bolt torqued | Marked with a paint pen after torque |
| V-303 | Bonding | Commissioning stage 1 bonding list, every item short to PE |
| V-304 | Drum turns by hand | Free, no rubbing, both directions, with the belt off |
| V-305 | Belt tracks | Belt centered on the drum and the pulley through ten turns by hand |
| V-306 | Seals | Felt seals in contact all round; a sheet of paper is gripped at four points |
| V-307 | Ducts sealed | Riser, lint duct, exhaust joined with gaskets and clamps, no gap you can see light through |
| V-308 | Door | Latches, opens past 90 degrees, operates S1 and S2 (continuity) |
| V-309 | Lint screen | Seats, comes out without tools |
| V-310 | Harness | Wire list ticked at both ends; J1 and J2 reach the module with slack and are strain relieved |
| V-311 | Nothing loose | Rock the cabinet, shake the panels, open and close the door ten times |

## Gate 4: commissioning

`docs/commissioning.md`, all stages, in order, with the numbers written on the sheet in the lid.

## Gate 5: the test run

| ID | Check | Method | Pass when |
| --- | --- | --- | --- |
| V-501 | Air-only run | 20 min, empty drum, panels on. Exhaust airflow measured at the duct (anemometer or a bag timing), motor current, noise notes | Airflow at or above 2.5 m3/min; current within nameplate |
| V-502 | First heated run, empty | 10 min HIGH, then 5 min cool-down. Exhaust temperature every minute, element current, number of T_HI cycles | Exhaust reaches the target and T_HI cycles; no limit trips; no smell after the first minutes |
| V-503 | Wet towels | 4 kg of cotton towels from a spin-dried washer, HIGH, HEAT TIME 50, DRY TIME 60. Temperatures, current, moisture at the end by feel and weight | Dry at the end; no limit trip; no lint outside the filter |
| V-504 | Door interrupt | Open the door mid-cycle, close it, press START | Stops at once, restarts only on START |
| V-505 | Power interrupt | Pull the plug mid-cycle for 10 s | Stays stopped until START |
| V-506 | Restricted vent | Cover half the exhaust outlet for one heated cycle | T_HI cycles faster; the high-limit does not trip; if it does, the thermostat settings are wrong, not the limit |
| V-507 | After the run | Panels off: lint where it should not be, any discoloration, every terminal cool, belt tracking, drum rims | Nothing found, or found and logged |
| V-508 | Build log | `builds/2026-MM-<builder>/` with every number, every photo, every deviation, and the measured values written into `bom.csv` and the CAD parameters | Complete |

## What this plan does not cover

- Gas and heat pump modules: their own rows are added when those modules move past paper. The electric reference build is the only one in scope for the first test run.
- Long-term wear: that is the failure-mode guide's job, fed by the build log.
- Code compliance: the builder's, not the plan's. The plan makes the machine conservative; it does not make it legal anywhere.
