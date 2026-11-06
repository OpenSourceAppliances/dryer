# Build guide

This is an uncertified appliance design published for free by individuals with no organization behind it. It involves mains voltage, heat, moving parts, and in some cases water and refrigerant. Building or operating it can cause fire, electric shock, injury, property damage, or death. There is no warranty of any kind. You are responsible for your own build, for checking it against your local electrical and building codes, and for deciding whether to use it. If you are not confident you can do that, do not build this.

Draft 1, 2026-11-05. Status: an order of assembly with the verification gates in it. There has been no real build, so there are no photos yet; the photos come from the first build and go next to the step where something could go wrong.

Every step names the checks from `docs/verification.md` that must be closed before it and the ones it closes. Do not skip a check because a step went well.

## 0. Before anything is bought or cut

- Gate 0 closed: V-001 to V-020.
- Buy the bought parts first: drum and its kits, motor, blower set, timers, power module parts, connectors, extrusion and hardware.
- Gate 1 closed: V-101 to V-115. Put every measurement into `mechanical/cad/osa_dryer_cad.py`, run it, read the diff of `mechanical/drawings/`, then send the DXFs to the cutter and cut the extrusion.
- Gate 2 closed: V-201 to V-207, on the bench, before the frame exists.

## 1. Frame

1. Cut or have cut the 29 extrusion pieces per `mechanical/drawings/frame-cut-list.csv` (21 for the cabinet, 8 for the console frame, which waits until step 8). Deburr the ends. Tap the bottom end of each post M8 for the feet.
2. Bottom level: two side rails and two end rails between the four posts, corner brackets, M8 into T-nuts, square before tightening. Diagonals equal within 2 mm (V-301).
3. Mid level at 260 to 300: side rails, rear end rail, the two front stubs, the rear cross rail at Y 611.5. Check the stubs leave the 340 mm gap centered.
4. Top level at 960 to 1000: side rails, end rails, rear cross rail.
5. Tray rails (2020) on the bottom rails at X minus 170 and plus 150, front end at Y 340.
6. Feet into the post ends (per V-113). Level the frame on the floor it will live on.
7. Mark every torqued bolt with a paint pen (V-302).

## 2. Bay

1. Base pan under the bottom rails, M6 into the slots. The cord's strain relief bushing into the 22 mm hole under the power module's place, locknut under the pan.
2. Motor mount plate and blower housing at the front (per the drawings that follow V-106 and V-107), motor in, pulley on the rear shaft, wheel on the front shaft. Direction checked at V-204 already.
3. Power module box at the rear left, bonded to the frame (ring terminal, star washer, bare metal).
4. Exhaust duct from the blower outlet along the right side to the rear lower panel port position.
5. Lint duct transition box in front of the blower inlet.

## 3. Rear bulkhead and riser

1. Fit the rollers to the rear bulkhead per the kit (V-102). Felt seal per V-104. Bond the plate.
2. Hang the bulkhead on the mid and top rear cross rails, M6 into the slots, rollers down, inlet field up.
3. Riser duct from the bay up behind the bulkhead to the inlet field, gasketed, bolted.

## 4. Bay ceiling plate

1. Slide the plate in over the mid rails from the front, slot over the rear bulkhead, notches at the rear posts. Its front edge stops 0.5 mm behind where the front bulkhead will stand.
2. M6 into the mid side rails, the rear cross rail, the rear end rail.
3. Lint duct up between the front stubs (2 mm to each), bolted to the stubs and to the transition box below.

## 5. Front bulkhead

1. Fit the glides per the kit (V-103), the felt seal (V-104), the lint slot hardware. Bond the plate.
2. Hang it on the mid front stubs and the top front rail; its bottom edge stands just in front of the ceiling plate's front edge.
3. Lint duct bolted to its face over the slot.

## 6. Drum

Built on the bench before the frame is closed, after V-208 has been run with a cheap material.

1. Lay the stainless sheet flat on cardboard, tabs up. Fold every tab inward 90 degrees with a hand seamer, checking each against a square.
2. Stand both rings on edge on the floor, tab-hole side out, 550 mm apart on two scraps of wood. Lift the sheet, one person each end, and lay its middle over the rings so the seam edges hang down on both sides.
3. Starting at the tabs nearest the top, bolt each tab to its ring hole with an M4 button head from the tab side and a nut on the ring face, working down both sides alternately. The sheet pulls round as you go. Do not fully tighten until all 60 are in.
4. Bring the two seam edges together under the drum, slide the splice strip inside, and bolt the seam through the splice with the button heads inside the drum. Then tighten everything.
5. Measure the diameter at mid-length at four angles (V-208 again, on the real sheet) and write the numbers in the build log.
6. Drill the three baffles on the drill press to the sheet's holes and bolt them in, angle inside, nuts outside.
7. Two people. Drum in from the front at an angle, rear end onto the rear rollers, front end onto the front rollers.
8. Turn by hand: free, silent, both felt seals touching the ring faces all round (V-304, V-306).
9. Belt around the drum through the two ceiling slots, under the motor pulley, idler fitted. Ten turns by hand, belt centered on the smooth track between the seam bolts (V-305).

## 7. Heat module

1. Build the electric tray on the bench (V-203 closed), slide it in on the tray rails from the back (the rear lower panel is still off; the module passes under the riser's hood), bolt it to the rails.
2. Riser flange adapter gasketed and bolted. Mains leads to X2, coil leads to X4. Tray bonded to X2:4.

## 8. Panels and console

1. Side panels, then rear upper and lower, then the top panel. Console frame next: the four 200 posts on the top panel with their foot brackets bolted down through the panel into the top rear cross rail's and rear top rail's slots (the T-nuts go into those slots before the top panel goes on), the four top rails and their brackets. Then the console cheeks, face, rear plate and cap. M6 into the slots at every hole. Bond each panel (V-303).
2. Front upper panel with the door ring, door disc on its hinge, latch and strike adjusted so S1 and S2 both operate (V-308).
3. Front lower panel last, after the bay has been looked at one more time for anything left inside.

## 9. Harness and controls

1. Cord through the base pan's bushing from below into the power module, strain relieved. J1 and J2 leads from the power module up to the console through their grommet, strain relieved (V-310).
2. Control module in, four M4 screws, plugs in.
3. Everything in Gate 3 ticked (V-301 to V-311).

## 10. Power

`docs/commissioning.md`, every stage, in order. Then the test run in `docs/verification.md` Gate 5. Then the build log in `builds/`.
