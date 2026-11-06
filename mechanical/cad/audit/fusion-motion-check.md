# Fusion motion and interference check (V-021)

Date: 2026-11-06, run on model draft 7 (the earlier draft 6 run of the same day, and the draft 5 run, are kept below the lines). Autodesk Fusion 2706.1.17 (Personal), Windows. Model draft 7 (`mechanical/cad/osa_dryer_cad.py`, 167 components), assembly STEP imported through Fusion's own STEP translator (`importManager.importToNewDocument`); joints, appearances and the interference analysis from `mechanical/cad/fusion_motion/fusion_motion.py` draft 4, run in the Text Commands window.

## What was built in Fusion

14 as-built joints (nothing moves when a joint is made; each one is defined on a face the STEP carries) and four rigid groups:

| joint | moving | fixed to | on | motion in the demonstration |
|---|---|---|---|---|
| drum | drum sheet, both rings, splice, three baffles, tab, seam and baffle bolts (rigid group) | front bulkhead | the sheet's 310 outside face | one turn |
| pulley | pulley | motor | the pulley's 15 rib face | 620/30 turns per drum turn |
| idler | idler pulley | idler arm | the idler's 20 face | 620/40 turns, the other way |
| idler arm | arm and its axle bolt (rigid group) | idler bracket | the arm's pivot hole | not animated (spring-loaded) |
| roller-front-1, -2, roller-rear-1, -2 | each roller | its bulkhead | the roller's 30 face | 310/30 turns, rolling on the sheet |
| door | disc, both lift-off hinge halves, handle, seal, strike and their screws (rigid group) | the pinned hinge halves | the 8 mm pin | opens to 100 degrees and closes |
| knob dry-time, knob heat-time | each knob | faceplate | the knob's 40 skirt | 300 and 200 degrees |
| selector | selector operator | selector body | its 22 hub | AIR, LOW, HIGH at 0, 45, 90 degrees |
| start button | button cap | button body | its 22 face | pressed 3 mm |
| tray | the whole heat module: tray, box walls and lid, angles, element rails, element, collar, thermostats, terminal plate and its angle, DIN rail and devices, bonding stud and the 124 M4 pieces (rigid group of every "heat-module" component, draft 7) | tray rail 1 | the tray's front end face | 250 mm out the back and in again (the module leaves by the back) |

The blower housing has no joint: its wheel, which is what turns, is not drawn. Every other component is grounded. The belt is drawn on its path and does not deform.

Appearances from Fusion's own library on every component (stainless drum, enamel panels, anodized extrusions for the cabinet and the console frame, galvanized plates and ducts, rubber rollers, belt and feet, felt, black knobs, green START, satin steel hardware and brackets), so the model reads as the materials the BOM names.

## Interference analysis

Fusion's Interference command (coincident faces excluded, overlaps under 1 mm3 ignored) at three points of the demonstration: at rest, a quarter of the way (door 50 degrees, tray 125 mm out) and half way (door 100 degrees, tray 250 mm out). At the two moved poses the rear lower panel and its bolts are left out of the analysis, because that panel is off whenever the tray is pulled (design-rules 7 Access).

Result (draft 7): no overlap of 1 mm3 or more between any two of the 167 components at any of the three poses. The whole heat module, with its 125 collar standing 3 under the hood's foam ring, passes under the riser's hood (230) and the mid rear end rail (260) and out through the rear opening without touching the riser, the exhaust duct, the tray rails' brackets or the bottom rear rail; the door, drum (now on its glides), rollers (on their shoulder screws), belt, idler, knobs, selector and START are clean as before. The pulley now turns 620/20 times per drum turn.

## Screenshots

Draft 7: `fusion-screens/51-draft7-iso-dressed.jpg` the machine as imported, with its appearances; `52-draft7-pose-tray-out-the-back.jpg` the half-way pose from the right rear with the rear lower panel hidden: the whole electric heat module 250 mm out the back on its tray (the box with its angles and bolts, the collar's flange on the lid, K_HEAT and the strips on the terminal plate), the exhaust duct's end beside it; `53-draft7-back-panels-off-modules.jpg` both rear panels hidden, at rest: the riser in the middle, the power module plate to its left (the viewer's right) with its cover over the mains rails and the relays and terminal strips above, the heat module in the bay under the hood; `54-draft7-rear-compartment-power-module.jpg` the same compartment straight on: the cover on its four standoffs, rails B1 and B2 above it, the glide bolts and a roller stud's nut on the rear bulkhead's back; `55-draft7-rear-bulkhead-felt-arcs-glides-rollers.jpg` the drum, front bulkhead and front parts hidden, looking at the rear bulkhead from the front: the two felt arcs, the two glide pads in the gaps at 10 and 2 o'clock with their sunk nuts, the inlet field, the two rollers on their shoulder screws; `56-draft7-heat-module-on-its-rails.jpg` everything but the heat module and its rails hidden, from the front left: the inlet opening in the left wall, the bottom, corner and lid angles with their M4, the collar, the thermostats; `57-draft7-heat-module-from-the-back.jpg` the same from the rear right: the terminal plate's DIN rail with X_HM, K_HEAT and CS1, the element's terminals through the right wall. All cropped to the CAD viewport.

Draft 6: `fusion-screens/45-draft6-iso-dressed.jpg` the machine as imported, with its appearances: the 200 tall console box on the top at the rear; `46-draft6-pose-tray-out-the-back.jpg` the half-way pose from the right rear with the rear lower panel hidden: the heat module 250 mm out the back on its tray, the exhaust duct's end beside it; `47-draft6-inside-right-top-front-off.jpg` the right side, top and front panels, the door, the console's face, cap and right cheek and the control module hidden: the cabinet and console frames, the drum with its belt track, the front bulkhead with the curved lint slot under the opening, the lint duct, the bay; `48-draft6-console-tier0-module.jpg` the Tier 0 module on the console face, faceplate draft 2 (22 mm devices above the centre line); `49-draft6-front-bulkhead-curved-lint-slot.jpg` the front panels, door and lint duct hidden: the 460 opening with the curved slot below it inside the rings' 540 bore, the drum behind; `50-draft6-bay-from-the-back-left.jpg` the rear panels, left side panel and power module envelope hidden: the rear bulkhead and riser, the heat module under the riser's hood, the motor, blower and exhaust, the cord under the pan. All cropped to the CAD viewport.

## Record

The joint list and the signs the script worked out (so that a positive value in `pose()` always opens the door outward, presses START in and pulls the tray out the back) were printed by `reconnect()`: door, knob dry-time, knob heat-time and selector reversed, the rest positive.

Result: 0 overlaps over the three poses (`fusion-motion-interference.txt`, draft 7). The archive with the joints and appearances is `mechanical/fusion/osa-dryer-assembly-motion.f3d` (Fusion's own format, 14.7 MB for draft 7; open it in Fusion and drag any joint).

The independent re-measure of every STEP with Fusion's kernel (V-014) was rerun on draft 7 the same day: 943 bodies (69 part files and the 167-component assembly, whose hardware sets Fusion lists body by body and the comparison adds up), 3943 cylinders, 52 clearances; 895 comparisons pass, every volume within 0.01 percent and every box, cylinder axis and clearance within 0.02 mm; the one CHECK is the drum sheet's face count as before (OCP 600, Fusion 570). Earlier, on draft 6 and again after the aperture change: 637 bodies, 711 comparisons, the same single CHECK (`audit-report.md` section 3).

---

## Draft 5 run, 2026-11-06 (superseded)

At rest: clean, no overlap of 1 mm3 or more between any two of the 110 components (the draft 4 run had found the hinge knuckles of the barebones pin in the ring, and the first draft 5 run the two countersunk hinge screws' heads and nuts in each other, 10 mm apart; they are 14 apart now).

While moving, the only overlaps were the heat module tray's path. Pulled out toward the front, the tray and the module met, in order, the idler arm, the idler spring and the belt (from 125 mm out), then the motor, the pulley and the blower (up to 2.9e6 mm3 at 250 mm out). The drive sits on the centre line of the bay, exactly where the tray had to go. The riser's bottom (Z 180) was lower than the module's top (222), so the module could not leave by the back either. 22 overlaps over the three poses, all in the tray's path. Screenshots `fusion-screens/40` to `44`.
