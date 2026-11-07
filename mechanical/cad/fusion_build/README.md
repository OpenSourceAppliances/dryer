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
fixed when the build runs; their spacing follows the parameters.

## Stages

Each stage is run, checked and pushed before the next.

| Stage | What | Status |
| --- | --- | --- |
| A | Parameters; the frame (four posts, the rails of three levels, the tray rails) with the T-slot profile | done 2026-11-07: 23 bars, every one at the script's volume and place; a change of `cab_w` or `cab_h` moves and stretches them |
| B | The plates: panels, bulkheads, bay ceiling, base pan, console plates, module and duct plates, with every hole, slot and cut | done 2026-11-07: the 34 plates the script draws with `plate_xz/xy/yz`, from `../plates.json`; each one is an outline sketch (dimensioned where the numbers carry expressions), its thickness extruded, its holes and slots as patterned cuts (627 holes in 133 cuts, 88 slots in 2), then a Move by its position; 55 of 55 bodies at the script's volume and place |
| C | The drum: sheet with its tabs, rings, splice, baffles; rollers, studs, glides, felts | pending |
| D | The ducts: lint box, spool, riser hood, trunk, nozzle, liner, basket; blower plate; exhaust set | pending |
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
