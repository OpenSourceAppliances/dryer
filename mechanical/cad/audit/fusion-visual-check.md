# Fusion visual and Measure-tool check

Date: 2026-11-06. Autodesk Fusion 2706.1.17 (Personal), Windows. Part of V-014 in `docs/verification.md`.

`mechanical/step/osa-dryer-assembly.step` was opened in Fusion through File > Open > Open from my computer (59 bodies, units mm). Parts were shown and hidden through Fusion's own visibility toggles (driven from the Text Commands window, which is only a faster way of clicking the eye icons), the camera was set to Fusion's standard views, and every number below was read from Fusion's Inspect > Measure dialog after clicking the face, edge or body in the viewport. The screenshots in `fusion-screens/` are cropped to the CAD viewport and the Measure dialog; files ending in `b` are close-ups of the dialog taken when another window covered it in the full capture.

## Views

| file | what it shows | what to look for |
|---|---|---|
| 01-assembly-iso.jpg, 08-assembly-iso-front-right.jpg | whole machine, front left and front right | door ring and disc centred on the front; 56 louvers on the front lower panel; the panel split at the mid rail; side panel bolt pattern on the posts and the three rail levels; console wedge with the UCI aperture facing front and up |
| 02-inside-iso-panels-hidden.jpg | left side, top, front panels, console face and door hidden | drum between the bulkheads with the splice on top and the seam and baffle holes; lint duct in front of the bulkhead between the two front stubs; frame |
| 03-inside-left-panels-hidden.jpg | same from the left | drum compartment above the bay ceiling; rollers at the drum ends; riser behind the rear bulkhead; motor, blower, exhaust, power module and heat module envelopes in the bay; console wedge rising toward the rear |
| 04-front.jpg, 05-left.jpg, 06-back.jpg, 07-top.jpg | the four standard views | front: door, louvers, aperture; left: the wedge slopes up toward the rear and the door disc stands proud at the front; back: exhaust port with the duct end inside it, 32 louvers, cord entry; top: cap, sloped face with the aperture, top panel holes |

## Measurements

Every value matches `docs/design-rules.md`, `controls/uci-spec.md` and the OpenCascade audit (`audit-report.md`). Fusion shows two decimals for round numbers and three for the rest.

| # | what was measured (how) | Fusion reading | expected | file |
|---|---|---|---|---|
| 1 | drum outer face (face: radius, diameter) | R 310.00, D 620.00 mm | 620 drum | 10, 10b |
| 2 | drum outer face to right side panel inner face (two faces) | min 35.00 mm, drum axis to panel 345.00 | 35 | 11, 11b |
| 3 | drum body to front bulkhead body (two bodies) | 7.70 mm | 7.7 (tabs at 49.2, bulkhead back face 41.5) | 12, 12b |
| 4 | drum body to rear bulkhead body | 9.20 mm | 9.2 | 13 |
| 5 | drum body to bay ceiling plate body | 20.00 mm | 20 | 14 |
| 6 | drum body to a roller body | 0.00 mm | 0, the roller runs on the sheet | 15, 15b |
| 7 | lint duct body to left front stub body | 2.00 mm | 2 | 16 |
| 8 | door opening edge on the front bulkhead (edge) | D 460.00, centre X 0.00, Y 40.00, Z 631.50 | 460 on the drum axis at the bulkhead | 17 |
| 9 | left roller shaft hole edge | D 10.50, centre X -170.00, Y 40.00, Z 337.051 | 10.5 at (-170, 337.05) | 18 |
| 10 | lint slot bottom straight edge | length 220.00 mm | 260 slot minus the 40 width | 19 |
| 11 | lint slot end arc | R 20.00, centre X -110.00, Z 361.50 | 40 wide, 260 long, 270 below the axis | 20 |
| 12 | front left post outer face to right side panel inner face | 690.00 mm, angle 0 | 690 cabinet | 21, 21b |
| 13 | front left post front edge to rear upper panel inner face | 750.00 mm; the edge is 1000.00 long | 750 deep, 1000 posts | 22 |
| 14 | base pan top face to top panel top face | 1001.50 mm | 1000 body plus the 1.5 panel | 23 |
| 15 | top panel top face to console cap top face | 113.137 mm | 160 sin 45 | 24, 24b |
| 16 | UCI aperture top edge (edge) and the console face (face) | edge 240.00 mm; face area 81056.383 mm2 | 240; 687 x 160 minus 240 x 120 minus four 4.5 holes = 81056.4 | 25 |
| 17 | UCI aperture left and right edges | each 120.00 mm, 240.00 apart | 240 x 120 | 26 |
| 18 | UCI mounting hole edge | D 4.50, centre X -130.00, Y 555.005, Z 1107.127 | 4.5 on the 260 x 140 pattern; (555.005, 1107.127) is 70 up the slope from the face centre plus the 1.5 plate | 27 |
| 19 | exhaust port edge on the rear lower panel | D 106.00, centre X 230.00, Y 751.50, Z 150.00 | 106 at (230, 150) | 28 |
| 20 | cord entry edge | D 22.00, centre X -250.00, Z 120.00 | 22 at (-250, 120) | 29 |
| 21 | base pan top face to the rear bulkhead slot edge on the bay ceiling | 301.50 mm; slot edge 612.00 long | 300 bay plus 1.5 plate; 612 slot | 30 |
| 22 | front ring outer edge and rear ring inner edge | front ring D 618.40; 548.00 apart along the axis | 618.4 rings; 550 drum less the 2 mm rear ring | 31 |
| 23 | rear ring inner edge | D 480.00, centre X 0.00, Y 598.00, Z 631.50 | 480 bore, rear ring at 598 to 600 | 32 |

What this does and does not prove: the files Fusion opens are the files the audit measured, and Fusion's own kernel and Measure tool agree with the documents on every dimension picked here. It does not change the physical questions left to V-208 (roller load on the 0.8 mm sheet, tab fold landing on the ring holes).
