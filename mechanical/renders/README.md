# Product renders

Rendered from the parametric Fusion model (`../fusion/osa-dryer-parametric.f3d`) by `render()` in
`../cad/fusion_motion/fusion_motion.py`, with Fusion's own local renderer: the Soft Light studio environment, a white
background, a ground plane that takes the shadow and a little reflection, 1920 x 1080. Each shot is rendered one and a
half times bigger and its middle kept, which gives the look of a 54 mm lens (the renderer keeps its own 36 mm view
whatever the viewport camera is set to). The paint is the two-tone scheme of `DECISIONS.md` 2026-11-07: RAL 5023
distant blue body, RAL 7024 graphite grey trim.

| File | Shows |
| --- | --- |
| `01-dryer-front-left.png` | the dryer from the front left |
| `02-dryer-rear-right.png` | the dryer from the rear right: the exhaust, the console's back, the cord |
| `03-dryer-front.png` | the dryer from the front: door, skirt, console |
| `04-dryer-service-side.png` | the left side panel and the top off: drum, drive, ducts and modules in place |
| `05-dryer-rear-open.png` | the rear panels and the power module cover off: heat module, power module, blower, exhaust |
| `06-drum-set.png` | the drum: sheet, rings, splice, baffles, rollers and their studs |
| `07-heat-module.png` | the electric heat module on its tray: element, collar, thermostats, DIN rail and devices |
| `08-power-module.png` | the power module without its cover: the five DIN rails and their devices, barrier, standoffs, ground stud |
| `09-tier0-module.png` | the Tier 0 control module: faceplate, timers, knobs, HEAT selector, START, K1 |
| `10-door.png` | the door: ring, disc, hinges, handle, seal, catch and switch |
| `11-drive.png` | the drive: motor on its cradles, pulley, idler, blower on its plate (the belt runs up to the drum, left out) |
| `12-lint-path.png` | the lint path: lint box, basket, riser, liner, hood, trunk and nozzle |
| `13-exhaust-set.png` | the exhaust: blower outlet, thermostats, pipe, clamps, tap, PS1 and its tube |
| `14-frame.png` | the frame: posts, rails, tray rails, console sub-frame, brackets and feet |

To render them again: open the parametric archive in Fusion, load the script in the Text Commands window as its
docstring says, then `dress()` (or `dress(only=...)` for the painted panels) and `render()`; `render(names=("07",))`
makes one shot. The shots are the `SHOTS` table in the script: what is shown, what is hidden, and the camera's
direction. Bought parts are the script's envelopes, so a motor, a timer or a terminal strip is a plain block of about
the right size, not a picture of the real part.
