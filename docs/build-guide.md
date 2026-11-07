# Build guide

This is an uncertified appliance design published for free by individuals with no organization behind it. It involves mains voltage, heat, moving parts, and in some cases water and refrigerant. Building or operating it can cause fire, electric shock, injury, property damage, or death. There is no warranty of any kind. You are responsible for your own build, for checking it against your local electrical and building codes, and for deciding whether to use it. If you are not confident you can do that, do not build this.

Draft 2, 2026-11-06 (draft 1 2026-11-05). Status: an order of assembly with the verification gates in it. Draft 2 follows model draft 7: full-depth tray rails on brackets, the power module as a plate behind the rear bulkhead, the roller studs and the drum glides, the electric module's bolted box. There has been no real build, so there are no photos yet; the photos come from the first build and go next to the step where something could go wrong.

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
5. Tray rails (2020, 750 long) on the front and rear bottom end rails at X minus 170 to 150 and plus 150 to 170, a 2020 inside corner bracket at each end: one M4 into the rail's outer side slot (T-nut for the 6 mm slot), one down into the end rail's top slot (M4 T-nut for the 8 mm slot). Put four more M4 T-nuts into each tray rail's top slot now, for the heat module tray; they cannot go in later.
6. Feet into the post ends (per V-113). Level the frame on the floor it will live on.
7. Mark every torqued bolt with a paint pen (V-302).

## 2. Bay

Every duct here is 1.5 mm plate on a frame of aluminium flat bar, the plates screwed with M4 button heads into holes tapped in the bars' edges (draft 8). Tapping an 8 mm edge wants the hole square: use the drill press with the bar clamped on its side, and a tap guide. The one rolled part besides the drum sheet is the throat liner (section 5).

1. Base pan under the bottom rails, M6 into the slots. The cord's strain relief bushing into the 22 mm hole at the rear left (X -275, Y 690), locknut under the pan.
2. The two motor cradle brackets on the pan, two M6 x 12 each through the pan's 6.5 holes (heads under the pan, nuts on the brackets' feet; the kit's own pattern governs, V-106), blower housing at the front (V-107), motor in, the 20 mm pulley on the rear shaft, wheel on the front shaft. Direction checked at V-204 already. The thermal fuse and the two cycling thermostats on the blower's outlet box with the kit's screws; PS1 on its 20x20x2 angle bracket at the right front, two M6 through the pan.
3. Idler bracket and spring bracket on the pan, the arm on its pivot, the idler on the arm; the spring waits for the belt.
4. Exhaust duct from the blower outlet along the right side to the rear lower panel port position.
5. The duct frames are made on the bench first (section 4a): the flat bar cut to the lengths in `drawings/frame-cut-list.csv`, every edge hole drilled 3.3 on the drill press, square to the edge, and tapped M4; the lint box's side bars get their 43 degree top cut and the 8.5 hang hole; the trunk's side bars are tapped in their lower end face as well. The spool is screwed to the lint box's back plate from inside the box, its bottom bar by the three M4 x 40 that pass through the box's bottom bar; 6 mm foam tape on its rear edges.

## 3. Rear bulkhead and riser

1. Fit the two rear glides (9.5 thick) to the bulkhead's front face with their nuts sunk in the pads, bolt heads behind (V-103). Lay the two felt arcs (10 mm, the long one round the bottom, the short one over the top) round the glides per V-104. Fit the two rear rollers on their studs: shim under the head, roller, spacer, stud through the 8.5 hole from the drum side, washer and nut behind; the nut clamps the shoulder's step to the plate and the roller stays free (V-102). Bond the plate.
2. Hang the bulkhead on the mid and top rear cross rails, M6 into the slots from the front, rollers down, inlet field up.
3. The riser: the hood's bottom plate, four bars and top plate screwed together (M4 x 8 into the bars' tapped edges, heads under the bottom plate and on top of the top plate, the top heads clear of where the mid rear cross rail sits), the foam ring glued round the collar hole underneath; the trunk's two side bars and top bar between its front and rear plates, then the trunk stood on the hood's top plate over its opening and screwed from inside the hood into the side bars' tapped feet (four M4 x 8). Lift the hood and trunk in from the back under the mid rear cross rail, the trunk up through the bay ceiling's cut, the hood's bottom at 230 over where the collar will be. The nozzle: four bars with 2 mm foam on their front edges, held to the bulkhead's back face round the hole field by ten M4 x 10 from the drum side (through the bulkhead and the foam into the bars' tapped front edges) and to the trunk's front plate by ten M4 x 8 from inside the trunk.
4. Power module plate on the rear faces of the two rear cross rails, four M6 into their rear slots (T-nuts in first), bonded through its ground stud. Its bottom edge drops through the bay ceiling's slot, so the ceiling plate goes in first if it is not already there (section 4), or the plate goes on after it.

## 4. Bay ceiling plate

1. Slide the plate in over the mid rails from the front, slot over the rear bulkhead, notches at the rear posts. Its front edge stops 0.5 mm behind where the front bulkhead will stand.
2. M6 into the mid side rails, the rear cross rail, the rear end rail.
3. The lint box (its front plate, two side bars, bottom bar and lower back plate screwed together on the bench, the spool on its back) up between the front stubs, 4 mm spacers between its side bars and the stubs, and the two M8 x 20 button heads through the bars and spacers into the stubs' tapped end bores (tap them M8 like the posts' bores, 6.8 drill is already there). Its bottom bar stands 2 above the tray rails. 3 mm foam tape on the back edges of the side bars above the back plate, where the bulkhead will press on them.

## 5. Front bulkhead

1. Fit the two front glides (8 thick) to the back face, the two felt arcs, the two front rollers on their studs (heads on the drum side, nuts in front of the plate) (V-103, V-104, V-102). Bond the plate.
2. Hang it on the mid front stubs and the top front rail; its bottom edge stands just in front of the ceiling plate's front edge, and its face lands on the lint box's foam strips and the top of its lower back plate. The front studs' nuts sit beside the lint box's side bars, 6 mm from them.
3. From the drum side, six M4 x 10 through the bulkhead's 4.5 holes at X plus and minus 162 (Z 310, 345, 380) into the side bars' tapped back edges, pulling the box onto its foam. The slot is now the box's inlet.
4. The throat liner: roll the 1.5 mm strip round a 471 plywood disc until it holds the curve (it springs back a little; roll it tighter than the form and check against the ring), fit the splice inside the seam with its two M3 x 6 (heads inside, nuts outside), and set the liner into the lint box's arc with its back edge on the bulkhead. The door ring goes on next (section 7) and traps its front edge.
5. The lint basket (section 7a) goes in last, through the slot from the drum side.

## 5a. Lint basket, on the bench

1. Tap the six M3 holes in each 3 mm sector plate (2.5 drill is in the DXF). Cut the mesh strip 42 x 350 (or wrap a longer piece and trim), fold one long edge 5 mm inward over the far plate's rim, lay the far clamp plate on it and run in the six M3 x 5. Wrap the strip round the far plate's edge, bending it round the two outer corners, and fold the other long edge 5 mm outward over the lip plate's back; lip clamp on, six M3 x 5. The mesh's ends meet on the inner arc; overlap them 10 mm.
2. Two M4 x 10 from the back of the lip's tab into the D-pull.
3. Try it in the slot before the bulkhead goes in: it should slide with a little drag and none of the mesh should catch on the slot's edges (V-018).

## 6. Drum

Built on the bench before the frame is closed, after V-208 has been run with a cheap material.

1. Lay the stainless sheet flat on cardboard, tabs up. Fold every tab inward 90 degrees with a hand seamer, checking each against a square.
2. Stand both rings on edge on the floor, tab-hole side out, 550 mm apart on two scraps of wood. Lift the sheet, one person each end, and lay its middle over the rings so the seam edges hang down on both sides.
3. Starting at the tabs nearest the top, bolt each tab to its ring hole with an M4 button head from the tab side and a nut on the ring face, working down both sides alternately. The sheet pulls round as you go. Do not fully tighten until all 60 are in.
4. Bring the two seam edges together under the drum, slide the splice strip inside, and bolt the seam through the splice with the button heads inside the drum. Then tighten everything.
5. Measure the diameter at mid-length at four angles (V-208 again, on the real sheet) and write the numbers in the build log.
6. Drill the three baffles on the drill press to the sheet's holes and bolt them in, angle inside, nuts outside.
7. Two people. Drum in from the front at an angle, rear end onto the rear rollers, front end onto the front rollers.
8. Turn by hand: free, silent, both felt seals touching the ring faces all round, about 1 mm of end play between the glides (V-304, V-306).
9. Belt around the drum through the two ceiling slots, under the motor pulley, over the idler, spring hooked between its posts. Ten turns by hand, belt centered on the smooth track between the seam bolts (V-305).

## 7. Heat module

1. Build the electric module on the bench (V-203 closed): the box on the tray (bottom angles first, bolted to the tray with the nuts under it; the element rails and side walls; the end walls and corner angles; the element on its rails with its terminals out through the right wall), the collar and thermostats on the lid, the lid on its angles, the terminal plate on its foot behind the box, the DIN rail and its devices, the element leads. Bond the tray at its stud.
2. Slide it in on the tray rails from the back (the rear lower panel is still off; everything on it passes under the riser's hood at 230) until its front edge is at Y 420, and bolt the side angles down into the rails' T-nuts (four M4). The collar's rim is now 3 under the hood, touching the foam ring.
3. Mains leads from X2 and the SELV pair from X4 down through the bay harness grommet to the module's strips. Tray bonding lead to X2:4.

## 8. Panels and console

1. Side panels, then rear upper and lower, then the top panel. Console frame next: the four 200 posts on the top panel with their foot brackets bolted down through the panel into the top rear cross rail's and rear top rail's slots (the T-nuts go into those slots before the top panel goes on), the four top rails and their brackets. Then the console cheeks, face, rear plate and cap. M6 into the slots at every hole. Bond each panel (V-303).
2. Front upper panel with the door ring, door disc on its hinge, latch and strike adjusted so S1 and S2 both operate (V-308).
3. Front lower panel last, after the bay has been looked at one more time for anything left inside.

## 9. Harness and controls

1. Cord through the base pan's bushing from below, straight up the bay and through the ceiling grommet to X1 on the power module's rail A1, strain relieved at the bushing. The bay harness down through the second ceiling grommet. J1 and J2 leads from the power module up through the top panel's grommet into the console, strain relieved (V-310). Cover on the mains rails, four M4.
2. Control module in, four M4 screws, plugs in.
3. Everything in Gate 3 ticked (V-301 to V-311).

## 10. Power

`docs/commissioning.md`, every stage, in order. Then the test run in `docs/verification.md` Gate 5. Then the build log in `builds/`.
