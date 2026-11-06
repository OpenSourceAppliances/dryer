# Fusion motion and interference check (V-021)

Date: 2026-11-06. Autodesk Fusion 2706.1.17 (Personal), Windows. Model draft 5 (`mechanical/cad/osa_dryer_cad.py`), assembly STEP imported through Fusion's own STEP translator; joints, appearances and the interference analysis from `mechanical/cad/fusion_motion/fusion_motion.py`, run in the Text Commands window.

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
| tray | heat module tray and module envelope (rigid group) | tray rail 1 | the tray's front end face | 250 mm out the front and back |

The blower housing has no joint: its wheel, which is what turns, is not drawn. Every other component is grounded. The belt is drawn on its path and does not deform.

Appearances from Fusion's own library on every component (stainless drum, enamel panels, anodized extrusions, galvanized plates and ducts, rubber rollers, belt and feet, felt, black knobs, green START, satin steel hardware), so the model reads as the materials the BOM names.

## Interference analysis

Fusion's Interference command (coincident faces excluded, overlaps under 1 mm3 ignored) at three points of the demonstration: at rest, a quarter of the way (door 50 degrees, tray 125 mm out) and half way (door 100 degrees, tray 250 mm out).

At rest: clean, no overlap of 1 mm3 or more between any two of the 110 components (the draft 4 run had found the hinge knuckles of the barebones pin in the ring, and the first draft 5 run the two countersunk hinge screws' heads and nuts in each other, 10 mm apart; they are 14 apart now).

While moving, the only overlaps are the heat module tray's path. Pulled out, the tray and the module meet, in order, the idler arm, the idler spring and the belt (from 125 mm out), then the motor, the pulley and the blower (up to 2.9e6 mm3 at 250 mm out). The drive sits on the centre line of the bay, exactly where the tray has to go. The riser's bottom (Z 180) is lower than the module's top (222), so the module cannot leave by the back either. This is a design finding, not a modelling error; `docs/verification.md` V-021 and V-022 carry it and the options (the module leaves by the back with the riser's bottom raised to 230 and a top-rear outlet on the module, or the drive moves off the centre line). It needs a `DECISIONS.md` entry before the tray drawing is called done.

## Screenshots

`fusion-screens/40-draft5-iso-dressed.jpg` the machine as imported, with its appearances; `41-draft5-inside-left-top-front-off.jpg` the left side, top, front panels, console and door hidden: the T-slot frame, the drum on its rollers with the belt around it, the splice and baffle bolts, the bay; `42-draft5-pose-door-open.jpg` the quarter pose, door open; `43-draft5-left-side-off-drive-and-belt.jpg` the left view with the left side off: riser, drum, belt down to the pulley, motor, blower, feet, cord; `44-draft5-console-tier0-module.jpg` the Tier 0 module on the console face. All cropped to the CAD viewport.

## Record

The joint list and the signs the script worked out (so that a positive value in `pose()` always opens the door outward, presses START in and pulls the tray forward) were printed by `reconnect()`: door, knob dry-time, knob heat-time and selector reversed, the rest positive.

Result: 22 overlaps over the three poses, none at rest, all 22 in the heat module tray's path at the two moved poses; the list with volumes is `fusion-motion-interference.txt`. The archive with the joints and appearances is `mechanical/fusion/osa-dryer-assembly-motion.f3d` (Fusion's own format, 9.8 MB; open it in Fusion and drag any joint).
