# The parametric Fusion build

`fusion_build.py` is run inside Autodesk Fusion (Utilities > Scripts, or pasted into the Text Commands box as in
`../fusion_motion/`). It makes a new design and draws every part of the dryer natively: user parameters, construction
planes placed by expressions, sketches with dimensions, extrudes, revolves, cuts and patterns, one component per part,
with the same component names as the STEP the script writes. Builders change a parameter (Modify > Change Parameters) or
a sketch dimension in Fusion's own interface and the model follows. It is the editable version of the design
(`DECISIONS.md` 2026-11-06); `../osa_dryer_cad.py` stays the generator of the STEP, DXF and cut list, and the two are
checked against each other.

## How it is checked

`../fusion_audit/fusion_audit.py` run on the built document measures every body (volume, bounding box, every
cylindrical face) and `../cad_audit.py --fusion` compares those with the OCC measurements of the script's files, body by
body, at 0.01 percent on volume and 0.02 mm on positions. A stage is done when its parts pass that comparison. The
only intended differences are recorded below.

## Numbers

The build reads the parameter table `P` out of `../osa_dryer_cad.py` (the text from `P = dict(` to the Helpers
header) so there is one list of numbers, and the plates from `../plates.json`, which the script writes on every run: every
flat plate with its outline, holes, cuts and slots, each number paired with the expression it was computed from (the
script's `Ex` numbers remember their arithmetic in the user parameters, so a hole row at the panel pitch comes out as
`(-half_w + ext/2) + i * ((cab_h - 60 mm) - ...) / n`). The user parameters it creates in Fusion are the ones a builder might change
(cabinet width, depth and height, drum diameter and length, door opening, bay height, plate thicknesses, panel bolt
pitch, console height, aperture); everything else is drawn from `P` as dimensions a builder can still edit in the sketch.
Draft 1 (2026-11-07): the user parameters drive the frame's lengths and positions and the plates' outlines, hole rows
and big cuts; features that do not follow from them are drawn at their numbers, undimensioned (a builder adds a
dimension in the sketch to drive one). Slots and sectors are drawn, not dimensioned. The number of holes in a row is
fixed when the build runs; their spacing follows the parameters. The parts after the plates are drawn from the same
`P` and from two more files the script writes: `../numbers.json`, the derived numbers of the script's own globals
(the door's bolt points, the hinge heights, the heat module's angle rows, the belt path, the idler's geometry, the
Tier 0 drawing's numbers, and so on, 145 of them), and `../hardware.json`, every bolt, nut, washer and spacer the
script places, by part: what it is, its bearing point and its normal. The ducts' bar frames, the modules' angles and
the envelopes of bought parts are drawn in place at those numbers; the drum and door parts about the drum axis are
drawn about the component's Y axis and moved up by `drum_axis_z`, the Tier 0 module by its aperture centre.

## Stages

Each stage is run, checked and pushed before the next.

| Stage | What | Status |
| --- | --- | --- |
| A | Parameters; the frame (four posts, the rails of three levels, the tray rails) with the T-slot profile | done 2026-11-07: 21 bars (4 posts, 15 rails, 2 tray rails), every one at the script's volume and place; a change of `cab_w` or `cab_h` moves and stretches them |
| B | The plates: panels, bulkheads, bay ceiling, base pan, console plates, module and duct plates, with every hole, slot and cut | done 2026-11-07: the 34 plates the script draws with `plate_xz/xy/yz`, from `../plates.json`; each one is an outline sketch (dimensioned where the numbers carry expressions), its thickness extruded, its holes and slots as patterned cuts (627 holes in 133 cuts, 88 slots in 2), then a Move by its position; 55 of 55 bodies at the script's volume and place |
| C | The drum: sheet with its tabs, rings, splice, baffles; rollers, studs, glides, felts | done 2026-11-07: 17 components, 19 bodies; the sheet is a tube (diameters `drum_d` and `drum_d - 1.6 mm`, length `drum_l`) with one tab joined at each end and patterned 30 times round the axis, its seam and baffle holes cut inward from tangent planes; the rings, splice, baffles, felts and glides are drawn about the drum axis at the origin and moved by `drum_front_y` and `drum_axis_z`, the rollers by expressions in `drum_d`; 74 of 74 bodies of stages A to C at the script's volume and place |
| D | The ducts: lint box, spool, riser hood, trunk, nozzle, liner, basket; blower plate; exhaust set | done 2026-11-07: the console sub-frame (8 bars), the liner and its splice, the lint box and spool bars and foams, the basket's plates, clamps, mesh and pull, the hood, trunk and nozzle bars, the hood gasket and nozzle foam, the blower plate's feet, the exhaust pipe, clamps, tap barb and the PS1 tube: 30 components, 56 bodies; every bar is the script's box with its tapped holes (4.2, the screw's length less the plate it passes through) cut from the bar's face; 130 of 130 bodies of stages A to D at the script's volume and place (`../audit/fusion-screens/73-parametric-stages-a-to-d-ducts-from-the-front-right.jpg`) |
| E | The modules: electric heat module, power module, Tier 0 module; the door; the drive (motor, blower, pulley, belt, idler); sensors, blanks, clamps | pending |
| F | Hardware: every bolt, nut, washer, stud as patterned bodies | pending |
| G | Joints and appearances (from `../fusion_motion/`), the archive `../../fusion/osa-dryer-parametric.f3d`, the comparison record | pending |

## Conventions

- Model coordinates are the script's: X across (left negative), Y from the front (0) to the back, Z up from the floor;
  the API works in cm, every number here is written in mm and converted.
- A plate is one sketch (its outline with every cut) on a construction plane offset by an expression, extruded by its
  thickness; a bar is a profile sketch extruded by its length; a bolt is a revolved profile with its socket cut, then
  patterned.
- Component names are the STEP's names, so `fusion_audit.py` can compare them: `measure_active()` in
  `../fusion_audit/fusion_audit.py` writes `../audit/fusion-build-measured.csv` for the built document, and
  `python3 cad_audit.py . --fusion cad/audit/fusion-build-measured.csv --fusion-partial` compares the parts built so far.
- Fusion orders an arc's own start and end counterclockwise whatever order it was drawn in, so every chained curve
  continues from whichever of the arc's end points lies where the drawing left off (`arc3`).
- Volumes are measured with Fusion's high calculation accuracy (`getPhysicalProperties`), not `body.volume`: that
  property is the medium-accuracy figure, and on the drum splice (a 1 mm strip on a 309 mm radius) it reads 0.015
  percent low, more than the comparison's 0.01 percent, while the geometry was right (end faces, arcs and fillets all
  at their exact areas). The STEP measurement record `../audit/fusion-measured.csv` was made before this change at the
  medium accuracy; it is remade at stage G.
- Holes in the drum parts are circles on a plane tangent to the drum at the hole's angle, cut inward. Fusion's
  plane-at-angle always contains its axis and turns the YZ plane's normal the other way round +Y, so `tangent_plane`
  tries the sign combinations and keeps the plane that holds the point it must touch.
