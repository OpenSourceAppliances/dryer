# CAD audit report

Produced by `mechanical/cad/cad_audit.py` from the STEP and DXF files on disk. Every number below was measured from the files, not read from the script.

Parts measured: 46 STEP files, 59 named solids in the assembly, 20 DXF drawings.
Document checks: 269, generic checks: 380, Fusion comparisons: 0. **Failures: 0.**

## 1. Values stated in the documents, against the files

| id | part | check | expected | measured | result | source |
|---|---|---|---|---|---|---|
| A-001 | assembly | assembly_solids | 59 | 59 | PASS | 7a: 46 made parts + 13 bought parts and envelopes |
| A-002 | assembly | assembly_size x | 693 | 693.0 | PASS | 7: 690 wide cabinet + two 1.5 side panels |
| A-003 | assembly | assembly_min x | -346.5 | -346.5 | PASS | 7: half width 345 + 1.5 panel |
| A-004 | assembly | assembly_max x | 346.5 | 346.5 | PASS | 7: half width 345 + 1.5 panel |
| A-005 | assembly | assembly_min y | -13.5 | -13.5 | PASS | 7a Door: disc 2 thick, 8 off the ring, ring 2 thick, panel 1.5 |
| A-006 | assembly | assembly_max y | 751.5 | 751.5 | PASS | 7: 750 deep + 1.5 rear panel |
| A-007 | assembly | assembly_min z | -1.5 | -1.5 | PASS | 7a Panels: base pan 1.5 under the frame |
| A-008 | assembly | assembly_max z | 1114.637 | 1114.637 | PASS | 7a Console: 1000 + 160 sin 45 = 1113.137, plus the 1.5 cap |
| F-001 | post-1 | size z | 1000 | 1000.0 | PASS | 7a Frame |
| F-002 | post-1 | size x | 40 | 40.0 | PASS | 7a Frame 4040 |
| F-003 | post-1 | size y | 40 | 40.0 | PASS | 7a Frame 4040 |
| F-004 | post-1 | min x | -345 | -345.0 | PASS | 7: 690 wide, posts at the corners |
| F-005 | post-1 | min y | 0 | 0.0 | PASS | 7a Frame |
| F-006 | post-2 | size z | 1000 | 1000.0 | PASS | 7a Frame |
| F-007 | post-2 | max x | 345 | 345.0 | PASS | 7: 690 wide |
| F-008 | post-2 | min y | 0 | 0.0 | PASS | 7a Frame |
| F-009 | post-3 | size z | 1000 | 1000.0 | PASS | 7a Frame |
| F-010 | post-3 | min x | -345 | -345.0 | PASS | 7: 690 wide |
| F-011 | post-3 | max y | 750 | 750.0 | PASS | 7: 750 deep |
| F-012 | post-4 | size z | 1000 | 1000.0 | PASS | 7a Frame |
| F-013 | post-4 | max x | 345 | 345.0 | PASS | 7: 690 wide |
| F-014 | post-4 | max y | 750 | 750.0 | PASS | 7: 750 deep |
| F-015 | rail-bottom-front | size x | 610 | 610.0 | PASS | 7a Frame end rail 610 |
| F-016 | rail-bottom-front | min z | 0 | 0.0 | PASS | 7a Frame bottom level 0..40 |
| F-017 | rail-bottom-front | max z | 40 | 40.0 | PASS | 7a Frame bottom level 0..40 |
| F-018 | rail-bottom-front | min y | 0 | 0.0 | PASS | 7a Frame |
| F-019 | rail-bottom-rear | size x | 610 | 610.0 | PASS | 7a Frame |
| F-020 | rail-bottom-rear | max y | 750 | 750.0 | PASS | 7a Frame |
| F-021 | rail-bottom-left | size y | 670 | 670.0 | PASS | 7a Frame side rail 670 |
| F-022 | rail-bottom-left | min x | -345 | -345.0 | PASS | 7a Frame |
| F-023 | rail-bottom-right | size y | 670 | 670.0 | PASS | 7a Frame |
| F-024 | rail-bottom-right | max x | 345 | 345.0 | PASS | 7a Frame |
| F-025 | rail-mid-front-left | size x | 135 | 135.0 | PASS | 7a Frame front stub 135 |
| F-026 | rail-mid-front-left | min z | 260 | 260.0 | PASS | 7a Frame mid level 260..300 |
| F-027 | rail-mid-front-left | max z | 300 | 300.0 | PASS | 7a Frame mid level 260..300 |
| F-028 | rail-mid-front-left | max x | -170 | -170.0 | PASS | 7a Frame: gap for the lint duct, stubs end 170 from centre |
| F-029 | rail-mid-front-right | size x | 135 | 135.0 | PASS | 7a Frame |
| F-030 | rail-mid-front-right | min x | 170 | 170.0 | PASS | 7a Frame |
| F-031 | rail-mid-rear | size x | 610 | 610.0 | PASS | 7a Frame |
| F-032 | rail-mid-rear | min z | 260 | 260.0 | PASS | 7a Frame |
| F-033 | rail-mid-left | size y | 670 | 670.0 | PASS | 7a Frame |
| F-034 | rail-mid-right | size y | 670 | 670.0 | PASS | 7a Frame |
| F-035 | rail-mid-rearcross | size x | 610 | 610.0 | PASS | 7a Frame rear cross rail 610 |
| F-036 | rail-mid-rearcross | min y | 611.5 | 611.5 | PASS | 7a: at the rear bulkhead (bulkhead at Y 610, 1.5 thick) |
| F-037 | rail-mid-rearcross | min z | 260 | 260.0 | PASS | 7a Frame |
| F-038 | rail-top-front | size x | 610 | 610.0 | PASS | 7a Frame |
| F-039 | rail-top-front | min z | 960 | 960.0 | PASS | 7a Frame top level 960..1000 |
| F-040 | rail-top-front | max z | 1000 | 1000.0 | PASS | 7a Frame top level 960..1000 |
| F-041 | rail-top-rear | size x | 610 | 610.0 | PASS | 7a Frame |
| F-042 | rail-top-left | size y | 670 | 670.0 | PASS | 7a Frame |
| F-043 | rail-top-right | size y | 670 | 670.0 | PASS | 7a Frame |
| F-044 | rail-top-rearcross | size x | 610 | 610.0 | PASS | 7a Frame |
| F-045 | rail-top-rearcross | min y | 611.5 | 611.5 | PASS | 7a Frame |
| F-046 | rail-top-rearcross | min z | 960 | 960.0 | PASS | 7a Frame |
| F-047 | tray-rail-1 | size y | 360 | 360.0 | PASS | 7a Frame 2020 tray rail 360 |
| F-048 | tray-rail-1 | size x | 20 | 20.0 | PASS | 7a Frame 2020 |
| F-049 | tray-rail-1 | size z | 20 | 20.0 | PASS | 7a Frame 2020 |
| F-050 | tray-rail-1 | min z | 40 | 40.0 | PASS | 7a Frame: on the bottom rails |
| F-051 | tray-rail-2 | size y | 360 | 360.0 | PASS | 7a Frame |
| F-052 | tray-rail-2 | min z | 40 | 40.0 | PASS | 7a Frame |
| F-053 | cut-list | cut post-1 | 1000 | 1000.0 | PASS | frame-cut-list.csv |
| F-054 | cut-list | cut rail-bottom-left | 670 | 670.0 | PASS | frame-cut-list.csv |
| F-055 | cut-list | cut rail-bottom-front | 610 | 610.0 | PASS | frame-cut-list.csv |
| F-056 | cut-list | cut rail-mid-front-left | 135 | 135.0 | PASS | frame-cut-list.csv |
| F-057 | cut-list | cut rail-mid-rearcross | 610 | 610.0 | PASS | frame-cut-list.csv |
| F-058 | cut-list | cut tray-rail-1 | 360 | 360.0 | PASS | frame-cut-list.csv |
| F-059 | cut-list | cut baffle-1..3 | 480 | 480.0 | PASS | 7b Baffles 480 long |
| F-060 | cut-list | cut_qty baffle-1..3 | 3 | 3 | PASS | 7b three baffles |
| F-061 | cut-list | cut belt (bought) | 2214 | 2214.0 | PASS | 7a Drive: about 2214 by the two-pulley estimate |
| B-001 | front-bulkhead | size x | 610 | 610.0 | PASS | 7a Bulkheads 610 wide |
| B-002 | front-bulkhead | thickness | 1.5 | 1.5 | PASS | 7a Bulkheads 1.5 steel |
| B-003 | front-bulkhead | normal | 0,1,0 | (-0.0, -1.0, -0.0) | PASS | 7a: front-facing plate |
| B-004 | front-bulkhead | min y | 40 | 40.0 | PASS | 7a: sits behind the front rails (0..40) |
| B-005 | front-bulkhead | min z | 265 | 265.0 | PASS | 7a: from the mid rails (260..300) to the top rails, 5 in from each rail edge |
| B-006 | front-bulkhead | max z | 995 | 995.0 | PASS | 7a: to the top rails (960..1000) |
| B-007 | front-bulkhead | loop circle;0;631.5;460;460 | 1 | 1 | PASS | 7a: door opening 460 on the drum axis; axis Z = 300 + 1.5 + 20 + 310 |
| B-008 | front-bulkhead | loop slot;0;361.5;260;40 | 1 | 1 | PASS | 7a: lint slot 260 x 40 below the opening, 270 below the axis |
| B-009 | front-bulkhead | hole_at 10.5;-170;337.05 | 1 | (-170.000, 337.051) d 10.500 | PASS | 7a: roller shaft holes 30 degrees each side of bottom on radius 310 + 30 = 340 |
| B-010 | front-bulkhead | hole_at 10.5;170;337.05 | 1 | (170.000, 337.051) d 10.500 | PASS | 7a roller shaft holes |
| B-011 | front-bulkhead | holes 10.5;y | 2 | 2 | PASS | 7a two rollers per bulkhead |
| B-012 | front-bulkhead | outline 610;730 | 1 | rect 610.000 x 730.000 | PASS | 7a Bulkheads |
| B-013 | rear-bulkhead | size x | 610 | 610.0 | PASS | 7a Bulkheads |
| B-014 | rear-bulkhead | thickness | 1.5 | 1.5 | PASS | 7a Bulkheads |
| B-015 | rear-bulkhead | min y | 610 | 610.0 | PASS | 7a: in front of the rear cross rails; drum front 50 + length 550 + 10 |
| B-016 | rear-bulkhead | hole_at 10.5;-170;337.05 | 1 | (-170.000, 337.051) d 10.500 | PASS | 7a roller shaft holes |
| B-017 | rear-bulkhead | hole_at 10.5;170;337.05 | 1 | (170.000, 337.051) d 10.500 | PASS | 7a roller shaft holes |
| B-018 | rear-bulkhead | holes 10;y | 126 | 126 | PASS | 7a: inlet field 200 x 130 above the axis, 10 mm holes on a 14 pitch: 14 x 9 |
| B-019 | rear-bulkhead | hole_at 10;-93;681.5 | 1 | (-93.000, 681.500) d 10.000 | PASS | 7a inlet field: first hole 7 in from the field edge, field starts 50 above the axis |
| B-020 | rear-bulkhead | hole_at 10;89;793.5 | 1 | (89.000, 793.500) d 10.000 | PASS | 7a inlet field: last hole |
| B-021 | rear-bulkhead | loops circle | 138 | 138 | PASS | 7a: 126 inlet + 2 roller + 10 M6 |
| B-022 | rear-bulkhead | outline 610;730 | 1 | rect 610.000 x 730.000 | PASS | 7a Bulkheads |
| C-001 | bay-ceiling | thickness | 1.5 | 1.5 | PASS | 7a Bay ceiling 1.5 plate |
| C-002 | bay-ceiling | min z | 300 | 300.0 | PASS | 7a: on the mid rails (top at 300) |
| C-003 | bay-ceiling | min y | 42 | 42.0 | PASS | 7a: starts 0.5 behind the front bulkhead (40 + 1.5) |
| C-004 | bay-ceiling | max y | 750 | 750.0 | PASS | 7a |
| C-005 | bay-ceiling | size x | 687 | 687.0 | PASS | 7a: between the side panels, 690 - 2 x 1.5 |
| C-006 | bay-ceiling | loop rect;0;402;40;90 | 1 | 1 | PASS | 7a: belt slot at the pulley, Y 402 |
| C-007 | bay-ceiling | loop rect;0;610.75;612;2.5 | 1 | 1 | PASS | 7a: rear bulkhead passes through (610..611.5, 1 mm clearance) |
| C-008 | bay-ceiling | loop rect;0;678.5;264;54 | 1 | 1 | PASS | 7a: riser 260 x 50 behind the rear cross rail with 2 mm clearance |
| C-009 | bay-ceiling | holes 6.5;z | 20 | 20 | PASS | 7a Panels: M6 at 150 pitch; 5 on the rear cross rail, 5 on the rear rail, 5 on each side rail |
| C-010 | bay-ceiling | loops polygon | 1 | 1 | PASS | 7a: outline notched at the two rear posts |
| C-011 | base-pan | thickness | 1.5 | 1.5 | PASS | 7a Panels 1.5 steel |
| C-012 | base-pan | max z | 0 | 0.0 | PASS | 7a: under the frame |
| C-013 | base-pan | size x | 687 | 687.0 | PASS | 7a between the side panels |
| C-014 | base-pan | size y | 750 | 750.0 | PASS | 7a |
| C-015 | base-pan | holes 6.5;z | 20 | 20 | PASS | 7a Panels M6 at 150 pitch |
| C-016 | base-pan | loops circle | 20 | 20 | PASS | 7a: no cut-outs in the base pan |
| C-017 | base-pan | outline 687;750 | 1 | rect 687.000 x 750.000 | PASS | 7a |
| P-001 | side-panel-left | thickness | 1.5 | 1.5 | PASS | 7a Panels |
| P-002 | side-panel-left | max x | -345 | -345.0 | PASS | 7: 690 wide |
| P-003 | side-panel-left | size y | 750 | 750.0 | PASS | 7: 750 deep |
| P-004 | side-panel-left | size z | 1000 | 1000.0 | PASS | 7a Frame posts 1000 |
| P-005 | side-panel-left | holes 6.5;x | 29 | 29 | PASS | 7a: 7 per post x 2, 5 per rail x 3 levels |
| P-006 | side-panel-left | outline 750;1000 | 1 | rect 750.000 x 1000.000 | PASS | 7a |
| P-007 | side-panel-right | min x | 345 | 345.0 | PASS | 7: 690 wide |
| P-008 | side-panel-right | holes 6.5;x | 29 | 29 | PASS | 7a |
| P-009 | side-panel-right | outline 750;1000 | 1 | rect 750.000 x 1000.000 | PASS | 7a |
| P-010 | front-upper-panel | thickness | 1.5 | 1.5 | PASS | 7a Panels |
| P-011 | front-upper-panel | max y | 0 | 0.0 | PASS | 7a: on the front of the frame |
| P-012 | front-upper-panel | size x | 690 | 690.0 | PASS | 7: 690 wide |
| P-013 | front-upper-panel | min z | 260 | 260.0 | PASS | 7a: the front panels split at the bottom of the mid rail (260) so the upper one bolts to that rail |
| P-014 | front-upper-panel | max z | 1000 | 1000.0 | PASS | 7a |
| P-015 | front-upper-panel | loop circle;0;631.5;480;480 | 1 | 1 | PASS | 7a Door: ring opening, 470 ring bore + 10 |
| P-016 | front-upper-panel | holes 6.5;y | 16 | 16 | PASS | 7a: 5 per post x 2, 2 on the mid stubs, 4 on the top rail |
| P-017 | front-lower-panel | max z | 259 | 259.0 | PASS | 7a: the bay panel, 1 mm under the upper panel |
| P-018 | front-lower-panel | loops slot | 56 | 56 | PASS | 7a Panels: louvers, 7 columns x 8 rows of 60 x 5 |
| P-019 | front-lower-panel | loop slot;-240;80;60;5 | 1 | 1 | PASS | 7a louver |
| P-020 | front-lower-panel | loop slot;240;220;60;5 | 1 | 1 | PASS | 7a louver, last |
| P-021 | front-lower-panel | holes 6.5;y | 8 | 8 | PASS | 7a: 2 per post x 2, 4 on the bottom rail |
| P-022 | rear-upper-panel | min y | 750 | 750.0 | PASS | 7a: on the back of the frame |
| P-023 | rear-upper-panel | holes 6.5;y | 18 | 18 | PASS | 7a: 5 per post x 2, 4 on the mid rail, 4 on the top rail |
| P-024 | rear-upper-panel | size x | 690 | 690.0 | PASS | 7 |
| P-025 | rear-lower-panel | min y | 750 | 750.0 | PASS | 7a |
| P-026 | rear-lower-panel | loop circle;230;150;106;106 | 1 | 1 | PASS | 7a Air: 102 exhaust at X 230, port 2 mm larger each side |
| P-027 | rear-lower-panel | loop circle;-250;120;22;22 | 1 | 1 | PASS | 7a Panels: cord entry, strain relief bushing hole 22 |
| P-028 | rear-lower-panel | loops slot | 32 | 32 | PASS | 7a: louvers, 4 columns x 8 rows, clear of the exhaust port and the cord entry |
| P-029 | rear-lower-panel | holes 6.5;y | 8 | 8 | PASS | 7a: 2 per post x 2, 4 on the bottom rail |
| P-030 | top-panel | min z | 1000 | 1000.0 | PASS | 7a: on the top rails |
| P-031 | top-panel | thickness | 1.5 | 1.5 | PASS | 7a Panels |
| P-032 | top-panel | max y | 448.5 | 448.5 | PASS | 7a Console: wedge starts at Y 450; panel stops 1.5 short of the face plate |
| P-033 | top-panel | size x | 690 | 690.0 | PASS | 7 |
| P-034 | top-panel | holes 6.5;z | 10 | 10 | PASS | 7a: 4 on the front rail, 3 on each side rail |
| K-001 | console-face | thickness | 1.5 | 1.500000000155886 | PASS | 7a all flat plates 1.5 |
| K-002 | console-face | normal | 0,-0.70710678,0.70710678 | (0.0, -0.7071, 0.7071) | PASS | 7a: 45 degrees, facing front and up |
| K-003 | console-face | outline 687;160 | 1 | rect 687.000 x 160.000 | PASS | 7a: 160 sloped face, between the side panels |
| K-004 | console-face | loop rect;0;0;240;120 | 1 | 1 | PASS | uci-spec 4.1 aperture 240 x 120 |
| K-005 | console-face | hole_at 4.5;-130;-70 | 1 | (-130.000, -70.000) d 4.500 | PASS | uci-spec 4.1 holes on 260 x 140 |
| K-006 | console-face | hole_at 4.5;130;-70 | 1 | (130.000, -70.000) d 4.500 | PASS | uci-spec 4.1 |
| K-007 | console-face | hole_at 4.5;-130;70 | 1 | (-130.000, 70.000) d 4.500 | PASS | uci-spec 4.1 |
| K-008 | console-face | hole_at 4.5;130;70 | 1 | (130.000, 70.000) d 4.500 | PASS | uci-spec 4.1 |
| K-009 | console-face | holes 4.5 | 4 | 4 | PASS | uci-spec 4.1 four holes |
| K-010 | console-face | min y | 448.939 | 448.93933982811 | PASS | 7a: wedge starts at Y 450 on the plate's inner face; the outer corner is 1.5 sin 45 further forward |
| K-011 | console-face | min z | 1000 | 1000.0 | PASS | 7a: on the top of the body |
| K-012 | console-face | max z | 1114.198 | 1114.197745162 | PASS | 7a: 1000 + 113.137 + the 1.5 plate's corner (1.5 x cos 45) |
| K-013 | console-cap | min z | 1113.137 | 1113.13708499 | PASS | 7a: 160 x sin 45 above the top |
| K-014 | console-cap | min y | 563.137 | 563.13708498984 | PASS | 7a: 450 + 160 x cos 45 |
| K-015 | console-cap | max y | 750 | 750.0 | PASS | 7 |
| K-016 | console-cap | outline 690;186.863 | 1 | rect 690.000 x 186.863 | PASS | 7a: cap from the top of the slope to the back |
| K-017 | console-cheek-left | thickness | 1.5 | 1.4999999999999432 | PASS | 7a |
| K-018 | console-cheek-left | normal | 1,0,0 | (-1.0, -0.0, -0.0) | PASS | 7a: side plate |
| K-019 | console-cheek-left | loops polygon | 1 | 1 | PASS | 7a: one triangle (a 4-sided plate here: the slope plus the rear and top) |
| K-020 | console-cheek-left | outline 300;113.137 | 1 | polygon 300.000 x 113.137 | PASS | 7a: from Y 450 to 750, 113.137 high |
| K-021 | console-cheek-right | outline 300;113.137 | 1 | polygon 300.000 x 113.137 | PASS | 7a |
| K-022 | console-cheek-right | min x | 343.5 | 343.5 | PASS | 7a: inside the side panel line |
| D-001 | door-ring | thickness | 2 | 2.0 | PASS | 7a Door 2 mm |
| D-002 | door-ring | loop circle;0;631.5;560;560 | 1 | 1 | PASS | 7a Door ring 560 outside on the drum axis |
| D-003 | door-ring | loop circle;0;631.5;470;470 | 1 | 1 | PASS | 7a Door ring 470 inside |
| D-004 | door-ring | max y | -1.5 | -1.5 | PASS | 7a: on the front panel |
| D-005 | door-disc | thickness | 2 | 2.0 | PASS | 7a Door 2 mm |
| D-006 | door-disc | loop circle;0;631.5;540;540 | 1 | 1 | PASS | 7a Door disc 540 |
| D-007 | door-disc | loops circle | 1 | 1 | PASS | 7a: a plain disc on the first build, no window |
| R-001 | drum-sheet | cyl 310;y;0,631.5 | 1 | 1 | PASS | 7b: 620 outside diameter on the drum axis (0, 631.5) |
| R-002 | drum-sheet | cyl 309.2;y;0,631.5 | 1 | 1 | PASS | 7b: 0.8 wall |
| R-003 | drum-sheet | cyl_length 310;y | 551.6 | 551.6 | PASS | 7b: 550 long, plus the 0.8 tab root at each end that follows the sheet surface |
| R-004 | drum-sheet | min y | 49.2 | 49.1999999 | PASS | 7b: front face at Y 50, tabs folded in front of the front ring |
| R-005 | drum-sheet | max y | 600.8 | 600.8000000999999 | PASS | 7b: tabs behind the rear ring |
| R-006 | drum-sheet | size x | 620 | 620.0000002000002 | PASS | 7b: 620 diameter; tab roots follow the sheet |
| R-007 | drum-sheet | holes 4.5;y | 60 | 60 | PASS | 7b: 30 tabs per edge with a 4.5 hole each |
| R-008 | drum-sheet | holes 4.5;radial | 16 | 16 | PASS | 7b: seam holes at 50 pitch, 8 per edge, belt and roller tracks clear |
| R-009 | drum-sheet | holes 6.5;radial | 12 | 12 | PASS | 7b: three columns of four baffle holes |
| R-010 | drum-sheet | solids | 1 | 1 | PASS | 7b: one sheet, tabs are part of it |
| R-011 | drum-ring-front | cyl 309.2;y;0,631.5 | 1 | 1 | PASS | 7b: ring 618.4 outside, the sheet's inside |
| R-012 | drum-ring-front | cyl 240;y;0,631.5 | 1 | 1 | PASS | 7b: ring 480 inside |
| R-013 | drum-ring-front | thickness | 2 | 2.0 | PASS | 7b: 2 mm rings |
| R-014 | drum-ring-front | min y | 50 | 50.0 | PASS | 7b: front ring at the sheet's front edge |
| R-015 | drum-ring-front | holes 4.5;y | 30 | 30 | PASS | 7b: 30 tab holes |
| R-016 | drum-ring-front | loop circle;0;631.5;618.4;618.4 | 1 | 1 | PASS | 7b ring outside |
| R-017 | drum-ring-front | loop circle;0;631.5;480;480 | 1 | 1 | PASS | 7b ring inside |
| R-018 | drum-ring-rear | max y | 600 | 600.0 | PASS | 7b: rear ring at the sheet's rear edge |
| R-019 | drum-ring-rear | holes 4.5;y | 30 | 30 | PASS | 7b |
| R-020 | drum-ring-rear | cyl 240;y;0,631.5 | 1 | 1 | PASS | 7b |
| R-021 | drum-splice | size y | 544 | 544.0000001999999 | PASS | 7b Splice 60 x 544 |
| R-022 | drum-splice | min y | 53 | 52.9999999 | PASS | 7b: between the rings, 1 mm off each |
| R-023 | drum-splice | holes 4.5;radial | 16 | 16 | PASS | 7b: holes matching the seam holes |
| R-024 | drum-splice | cyl 309.2;y;0,631.5 | 1 | 1 | PASS | 7b: inside the sheet |
| R-025 | drum-splice | cyl 308.2;y;0,631.5 | 1 | 1 | PASS | 7b: 1 mm strip |
| R-026 | dxf | dxf_outline drum-sheet;1945.274;590 |  | polygon 1945.274 x 590.000 | PASS | 7b: 1945.3 x 550 plus 20 mm tabs on both long edges |
| R-027 | dxf | dxf_circles_d drum-sheet;4.5 | 76 | 76 | PASS | 7b: 60 tab holes + 16 seam holes |
| R-028 | dxf | dxf_circles_d drum-sheet;6.5 | 12 | 12 | PASS | 7b: baffle holes |
| R-029 | dxf | dxf_circle_at drum-sheet;4.5;15;55 | 1 | 1 | PASS | 7b: seam hole 15 in from the edge, first one 55 from the front (roller track 45 + 10) |
| R-030 | dxf | dxf_circle_at drum-sheet;4.5;1930.274;455 | 1 | 1 | PASS | 7b: seam hole on the other edge, last one before the rear roller track |
| R-031 | dxf | dxf_circle_at drum-sheet;6.5;324.212;105 | 1 | 1 | PASS | 7b: first baffle hole; column at a sixth of the width, 170 before the middle |
| R-032 | dxf | dxf_circle_at drum-sheet;4.5;32.421;-10 | 1 | 1 | PASS | 7b: first tab hole, tab centred half a pitch from the seam, hole 10 out on the tab |
| R-033 | dxf | dxf_outline drum-ring;618.4;618.4 |  | circle 618.400 x 618.400 | PASS | 7b Rings 618.4 outside |
| R-034 | dxf | dxf_circles_d drum-ring;480 | 1 | 1 | PASS | 7b Rings 480 inside |
| R-035 | dxf | dxf_circles_d drum-ring;4.5 | 30 | 30 | PASS | 7b: 30 holes |
| R-036 | dxf | dxf_circle_at drum-ring;4.5;-31.276;297.561 | 1 | 1 | PASS | 7b: tab hole on radius 299.2 at 6 degrees from the top (first tab centre) |
| R-037 | dxf | dxf_outline drum-splice;60;544 |  | rect 60.000 x 544.000 | PASS | 7b Splice 60 x 544 |
| R-038 | dxf | dxf_circles_d drum-splice;4.5 | 16 | 16 | PASS | 7b |
| R-039 | dxf | dxf_circle_at drum-splice;4.5;15;52 | 1 | 1 | PASS | 7b: splice hole under the first seam hole (55 - 2 ring - 1) |
| M-001 | motor (bought) | size y | 200 | 200.0 | PASS | bom: NEMA 48 frame envelope 200 long (V-106) |
| M-002 | motor (bought) | min y | 190 | 190.0 | PASS | 7a: motor behind the blower |
| M-003 | motor (bought) | cyl 70;y;0,120 | 1 | 1 | PASS | 7a Drive: axis at 120 high, 140 envelope |
| M-004 | pulley (bought) | cyl 15;y;0,120 | 1 | 1 | PASS | 7a Drive: PJ pulley, 30 pitch diameter estimate (V-012) |
| M-005 | pulley (bought) | min y | 394 | 394.0 | PASS | 7a Drive: pulley centred at Y 402, 16 wide |
| M-006 | blower (bought) | cyl 110;y;0,120 | 1 | 1 | PASS | 7a Blower envelope 220 on the motor axis |
| M-007 | blower (bought) | min y | 84 | 84.0 | PASS | 7a Blower on the front shaft |
| M-008 | exhaust-duct (bought) | cyl 51;y;230,150 | 1 | 1 | PASS | 7a Air: 102 exhaust along the bay floor at X 230, 150 high |
| M-009 | exhaust-duct (bought) | max y | 750 | 750.0 | PASS | 7a Air: to the rear lower panel |
| M-010 | heat-module-tray | min y | 420 | 420.0 | PASS | 7a Air: tray Y 420 to 670 |
| M-011 | heat-module-tray | max y | 670 | 670.0 | PASS | 7a Air |
| M-012 | heat-module-tray | size x | 320 | 320.0 | PASS | 7a: tray 320 wide, centred |
| M-013 | heat-module-tray | min z | 60 | 60.0 | PASS | 7a: on the 2020 tray rails (40 + 20) |
| M-014 | riser-duct | size x | 260 | 260.0 | PASS | 7a Air riser 260 x 50 |
| M-015 | riser-duct | size y | 50 | 50.0 | PASS | 7a Air riser 260 x 50 |
| M-016 | riser-duct | min y | 653.5 | 653.5 | PASS | 7a: behind the mid rear cross rail (ends 651.5) with 2 mm |
| M-017 | lint-duct | size x | 336 | 336.0 | PASS | 7a Air: lint duct 336 x 36 between the front stubs with 2 mm each side |
| M-018 | lint-duct | size y | 36 | 36.0 | PASS | 7a Air |
| M-019 | lint-duct | min y | 2 | 2.0 | PASS | 7a: 2 off the front panel |
| M-020 | lint-duct | max y | 38 | 38.0 | PASS | 7a: 2 off the front bulkhead |
| M-021 | power-module (envelope) | size x | 170 | 170.0 | PASS | 7a Power module 170 x 250 x 180 |
| M-022 | power-module (envelope) | size y | 250 | 250.0 | PASS | 7a |
| M-023 | power-module (envelope) | size z | 180 | 180.0 | PASS | 7a |
| M-024 | power-module (envelope) | min x | -340 | -340.0 | PASS | 7a: rear left of the bay |
| M-025 | roller-front-1 (bought) | cyl 30;y;-170,337.05 | 1 | 1 | PASS | 7b Rollers: 60 diameter at 30 degrees below the axis on radius 340 |
| M-026 | roller-front-1 (bought) | min y | 50 | 50.0 | PASS | 7b: running over the ring, flush with the drum end |
| M-027 | roller-front-1 (bought) | size y | 25 | 25.0 | PASS | bom: catalog roller 25 wide (V-106) |
| M-028 | roller-rear-2 (bought) | cyl 30;y;170,337.05 | 1 | 1 | PASS | 7b Rollers |
| M-029 | roller-rear-2 (bought) | max y | 600 | 600.0 | PASS | 7b: over the rear ring |
| M-030 | baffle-1 (angle, cut to length) | size y | 480 | 480.0 | PASS | 7b Baffles 480 long |
| M-031 | baffle-2 (angle, cut to length) | size y | 480 | 480.0 | PASS | 7b |
| M-032 | baffle-3 (angle, cut to length) | size y | 480 | 480.0 | PASS | 7b |
| M-033 | baffle-1 (angle, cut to length) | holes 6.5;radial | 4 | 4 | PASS | 7b: four bolts per baffle |
| X-001 | clearance | clearance drum-sheet;bay-ceiling | 20 | 20.0 | PASS | 7a: 20 mm under the drum (bay top 300 + 1.5 plate) |
| X-002 | clearance | clearance drum-sheet;rail-top-front | 21.03 | 21.03 | PASS | 7a: drum top 941.5 is 18.5 under the top rails (960); nearest rail corner is the top front rail at Y 40, so sqrt(10^2 + 18.5^2) |
| X-003 | clearance | clearance drum-sheet;side-panel-left | 35 | 35.0 | PASS | 7: 35 to each side panel |
| X-004 | clearance | clearance drum-sheet;side-panel-right | 35 | 35.0 | PASS | 7 |
| X-005 | clearance | clearance drum-sheet;front-bulkhead | 7.7 | 7.7 | PASS | 7b: front tabs at 49.2, bulkhead back face at 41.5 |
| X-006 | clearance | clearance drum-sheet;rear-bulkhead | 9.2 | 9.2 | PASS | 7b: rear tabs to 600.8, bulkhead at 610 |
| X-007 | clearance | clearance drum-ring-front;front-bulkhead | 8.5 | 8.5 | PASS | 7b: ring face at 50 |
| X-008 | clearance | clearance drum-ring-rear;rear-bulkhead | 10 | 10.0 | PASS | 7b: ring face at 600 |
| X-009 | clearance | clearance drum-sheet;roller-front-1 (bought) | 0 | 0.0 | PASS | 7b: rollers run on the sheet |
| X-010 | clearance | clearance drum-sheet;roller-rear-2 (bought) | 0 | 0.0 | PASS | 7b |
| X-011 | clearance | clearance drum-sheet;drum-ring-front | 0 | 0.0 | PASS | 7b: ring inside the sheet |
| X-012 | clearance | clearance drum-sheet;drum-splice | 0 | 0.0 | PASS | 7b: splice against the sheet |
| X-013 | clearance | clearance door-disc;door-ring | 8 | 8.0 | PASS | 7a Door: disc 8 off the ring (seal and hinge not modelled) |
| X-014 | clearance | clearance console-face;console-cheek-left | 0 | 0.0 | PASS | 7a: face plate on the cheek's sloped edge |
| X-015 | clearance | clearance console-face;console-cap | 0 | 0.0 | PASS | 7a: cap meets the face plate |
| X-016 | clearance | clearance lint-duct;rail-mid-front-left | 2 | 2.0 | PASS | 7a: 2 to each stub |
| X-017 | clearance | clearance lint-duct;rail-mid-front-right | 2 | 2.0 | PASS | 7a |
| X-018 | clearance | clearance lint-duct;front-bulkhead | 2 | 2.0 | PASS | 7a |
| X-019 | clearance | clearance riser-duct;bay-ceiling | 2 | 2.0 | PASS | 7a: 2 mm all round in the ceiling cut |
| X-020 | clearance | clearance riser-duct;rail-mid-rear | 6.5 | 6.5 | PASS | 7a: riser ends at 703.5, rear rail starts at 710 |
| X-021 | clearance | clearance heat-module (envelope);heat-module-tray | 0.5 | 0.5 | PASS | 7a: module sits on the tray |
| X-022 | clearance | clearance motor (bought);base-pan | 50 | 50.0 | PASS | 7a: motor axis 120 high |
| X-023 | clearance | clearance blower (bought);lint-duct-transition | 0 | 0.0 | PASS | 7a: transition box feeds the blower |
| X-024 | clearance | clearance exhaust-duct (bought);rear-lower-panel | 2 | 2.0 | PASS | 7a: duct through the port with 2 mm |
| X-025 | clearance | clearance power-module (envelope);side-panel-left | 5 | 5.0 | PASS | 7a: rear left of the bay |
| X-026 | clearance | clearance drum-sheet;top-panel | 58.5 | 58.5 | PASS | 7a: drum top 941.5, top panel at 1000 |

## 2. Generic checks on every part

| part | check | measured | result |
|---|---|---|---|
| base-pan | one solid | 1 | PASS |
| base-pan | valid B-rep (BRepCheck) | 1 | PASS |
| base-pan | closed shells | 1 | PASS |
| base-pan | volume positive | 771879.5 | PASS |
| base-pan | in the assembly with the same volume and place | True | PASS |
| base-pan | section edges all closed | 0 | PASS |
| base-pan | every section loop is a circle, rectangle, slot or polygon | 21 loops, 0 unclassified | PASS |
| base-pan | every cut lies inside the outline | 20 | PASS |
| base-pan | no two cuts overlap | 0 overlapping pairs | PASS |
| base-pan.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| base-pan.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 21 matched, 0 only in STEP, 0 only in DXF | PASS |
| base-pan.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
| bay-ceiling | one solid | 1 | PASS |
| bay-ceiling | valid B-rep (BRepCheck) | 1 | PASS |
| bay-ceiling | closed shells | 1 | PASS |
| bay-ceiling | volume positive | 694781.0 | PASS |
| bay-ceiling | in the assembly with the same volume and place | True | PASS |
| bay-ceiling | section edges all closed | 0 | PASS |
| bay-ceiling | every section loop is a circle, rectangle, slot or polygon | 24 loops, 0 unclassified | PASS |
| bay-ceiling | every cut lies inside the outline | 23 | PASS |
| bay-ceiling | no two cuts overlap | 0 overlapping pairs | PASS |
| bay-ceiling.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| bay-ceiling.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 24 matched, 0 only in STEP, 0 only in DXF | PASS |
| bay-ceiling.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
| console-cap | one solid | 1 | PASS |
| console-cap | valid B-rep (BRepCheck) | 1 | PASS |
| console-cap | closed shells | 1 | PASS |
| console-cap | volume positive | 193403.1 | PASS |
| console-cap | in the assembly with the same volume and place | True | PASS |
| console-cap | section edges all closed | 0 | PASS |
| console-cap | every section loop is a circle, rectangle, slot or polygon | 1 loops, 0 unclassified | PASS |
| console-cap | every cut lies inside the outline | 0 | PASS |
| console-cap | no two cuts overlap | 0 overlapping pairs | PASS |
| console-cap.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| console-cap.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 1 matched, 0 only in STEP, 0 only in DXF | PASS |
| console-cap.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, -0.00) | PASS |
| console-cheek-left | one solid | 1 | PASS |
| console-cheek-left | valid B-rep (BRepCheck) | 1 | PASS |
| console-cheek-left | closed shells | 1 | PASS |
| console-cheek-left | volume positive | 41311.7 | PASS |
| console-cheek-left | in the assembly with the same volume and place | True | PASS |
| console-cheek-left | section edges all closed | 0 | PASS |
| console-cheek-left | every section loop is a circle, rectangle, slot or polygon | 1 loops, 0 unclassified | PASS |
| console-cheek-left | every cut lies inside the outline | 0 | PASS |
| console-cheek-left | no two cuts overlap | 0 overlapping pairs | PASS |
| console-cheek-left.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| console-cheek-left.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 1 matched, 0 only in STEP, 0 only in DXF | PASS |
| console-cheek-left.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
| console-cheek-right | one solid | 1 | PASS |
| console-cheek-right | valid B-rep (BRepCheck) | 1 | PASS |
| console-cheek-right | closed shells | 1 | PASS |
| console-cheek-right | volume positive | 41311.7 | PASS |
| console-cheek-right | in the assembly with the same volume and place | True | PASS |
| console-cheek-right | section edges all closed | 0 | PASS |
| console-cheek-right | every section loop is a circle, rectangle, slot or polygon | 1 loops, 0 unclassified | PASS |
| console-cheek-right | every cut lies inside the outline | 0 | PASS |
| console-cheek-right | no two cuts overlap | 0 overlapping pairs | PASS |
| console-cheek-right.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| console-cheek-right.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 1 matched, 0 only in STEP, 0 only in DXF | PASS |
| console-cheek-right.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
| console-face | one solid | 1 | PASS |
| console-face | valid B-rep (BRepCheck) | 1 | PASS |
| console-face | closed shells | 1 | PASS |
| console-face | volume positive | 121584.6 | PASS |
| console-face | in the assembly with the same volume and place | True | PASS |
| console-face | section edges all closed | 0 | PASS |
| console-face | every section loop is a circle, rectangle, slot or polygon | 6 loops, 0 unclassified | PASS |
| console-face | every cut lies inside the outline | 5 | PASS |
| console-face | no two cuts overlap | 0 overlapping pairs | PASS |
| console-face.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| console-face.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 6 matched, 0 only in STEP, 0 only in DXF | PASS |
| console-face.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
| door-disc | one solid | 1 | PASS |
| door-disc | valid B-rep (BRepCheck) | 1 | PASS |
| door-disc | closed shells | 1 | PASS |
| door-disc | volume positive | 458044.2 | PASS |
| door-disc | in the assembly with the same volume and place | True | PASS |
| door-disc | section edges all closed | 0 | PASS |
| door-disc | every section loop is a circle, rectangle, slot or polygon | 1 loops, 0 unclassified | PASS |
| door-disc | every cut lies inside the outline | 0 | PASS |
| door-disc | no two cuts overlap | 0 overlapping pairs | PASS |
| door-disc.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| door-disc.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 1 matched, 0 only in STEP, 0 only in DXF | PASS |
| door-disc.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 631.50) | PASS |
| door-ring | one solid | 1 | PASS |
| door-ring | valid B-rep (BRepCheck) | 1 | PASS |
| door-ring | closed shells | 1 | PASS |
| door-ring | volume positive | 145612.8 | PASS |
| door-ring | in the assembly with the same volume and place | True | PASS |
| door-ring | section edges all closed | 0 | PASS |
| door-ring | every section loop is a circle, rectangle, slot or polygon | 2 loops, 0 unclassified | PASS |
| door-ring | every cut lies inside the outline | 1 | PASS |
| door-ring | no two cuts overlap | 0 overlapping pairs | PASS |
| door-ring.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| door-ring.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 2 matched, 0 only in STEP, 0 only in DXF | PASS |
| door-ring.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 631.50) | PASS |
| drum-ring-front | one solid | 1 | PASS |
| drum-ring-front | valid B-rep (BRepCheck) | 1 | PASS |
| drum-ring-front | closed shells | 1 | PASS |
| drum-ring-front | volume positive | 237835.9 | PASS |
| drum-ring-front | in the assembly with the same volume and place | True | PASS |
| drum-ring-front | section edges all closed | 0 | PASS |
| drum-ring-front | every section loop is a circle, rectangle, slot or polygon | 32 loops, 0 unclassified | PASS |
| drum-ring-front | every cut lies inside the outline | 31 | PASS |
| drum-ring-front | no two cuts overlap | 0 overlapping pairs | PASS |
| drum-ring-rear | one solid | 1 | PASS |
| drum-ring-rear | valid B-rep (BRepCheck) | 1 | PASS |
| drum-ring-rear | closed shells | 1 | PASS |
| drum-ring-rear | volume positive | 237835.9 | PASS |
| drum-ring-rear | in the assembly with the same volume and place | True | PASS |
| drum-ring-rear | section edges all closed | 0 | PASS |
| drum-ring-rear | every section loop is a circle, rectangle, slot or polygon | 32 loops, 0 unclassified | PASS |
| drum-ring-rear | every cut lies inside the outline | 31 | PASS |
| drum-ring-rear | no two cuts overlap | 0 overlapping pairs | PASS |
| drum-sheet | one solid | 1 | PASS |
| drum-sheet | valid B-rep (BRepCheck) | 1 | PASS |
| drum-sheet | closed shells | 1 | PASS |
| drum-sheet | volume positive | 878507.5 | PASS |
| drum-sheet | in the assembly with the same volume and place | True | PASS |
| drum-splice | one solid | 1 | PASS |
| drum-splice | valid B-rep (BRepCheck) | 1 | PASS |
| drum-splice | closed shells | 1 | PASS |
| drum-splice | volume positive | 32391.2 | PASS |
| drum-splice | in the assembly with the same volume and place | True | PASS |
| front-bulkhead | one solid | 1 | PASS |
| front-bulkhead | valid B-rep (BRepCheck) | 1 | PASS |
| front-bulkhead | closed shells | 1 | PASS |
| front-bulkhead | volume positive | 402971.5 | PASS |
| front-bulkhead | in the assembly with the same volume and place | True | PASS |
| front-bulkhead | section edges all closed | 0 | PASS |
| front-bulkhead | every section loop is a circle, rectangle, slot or polygon | 12 loops, 0 unclassified | PASS |
| front-bulkhead | every cut lies inside the outline | 11 | PASS |
| front-bulkhead | no two cuts overlap | 0 overlapping pairs | PASS |
| front-bulkhead.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| front-bulkhead.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 12 matched, 0 only in STEP, 0 only in DXF | PASS |
| front-bulkhead.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
| front-lower-panel | one solid | 1 | PASS |
| front-lower-panel | valid B-rep (BRepCheck) | 1 | PASS |
| front-lower-panel | closed shells | 1 | PASS |
| front-lower-panel | volume positive | 242917.5 | PASS |
| front-lower-panel | in the assembly with the same volume and place | True | PASS |
| front-lower-panel | section edges all closed | 0 | PASS |
| front-lower-panel | every section loop is a circle, rectangle, slot or polygon | 65 loops, 0 unclassified | PASS |
| front-lower-panel | every cut lies inside the outline | 64 | PASS |
| front-lower-panel | no two cuts overlap | 0 overlapping pairs | PASS |
| front-lower-panel.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| front-lower-panel.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 65 matched, 0 only in STEP, 0 only in DXF | PASS |
| front-lower-panel.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
| front-upper-panel | one solid | 1 | PASS |
| front-upper-panel | valid B-rep (BRepCheck) | 1 | PASS |
| front-upper-panel | closed shells | 1 | PASS |
| front-upper-panel | volume positive | 493670.0 | PASS |
| front-upper-panel | in the assembly with the same volume and place | True | PASS |
| front-upper-panel | section edges all closed | 0 | PASS |
| front-upper-panel | every section loop is a circle, rectangle, slot or polygon | 18 loops, 0 unclassified | PASS |
| front-upper-panel | every cut lies inside the outline | 17 | PASS |
| front-upper-panel | no two cuts overlap | 0 overlapping pairs | PASS |
| front-upper-panel.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| front-upper-panel.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 18 matched, 0 only in STEP, 0 only in DXF | PASS |
| front-upper-panel.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
| heat-module-tray | one solid | 1 | PASS |
| heat-module-tray | valid B-rep (BRepCheck) | 1 | PASS |
| heat-module-tray | closed shells | 1 | PASS |
| heat-module-tray | volume positive | 120000.0 | PASS |
| heat-module-tray | in the assembly with the same volume and place | True | PASS |
| heat-module-tray | section edges all closed | 0 | PASS |
| heat-module-tray | every section loop is a circle, rectangle, slot or polygon | 1 loops, 0 unclassified | PASS |
| heat-module-tray | every cut lies inside the outline | 0 | PASS |
| heat-module-tray | no two cuts overlap | 0 overlapping pairs | PASS |
| lint-duct-transition | one solid | 1 | PASS |
| lint-duct-transition | valid B-rep (BRepCheck) | 1 | PASS |
| lint-duct-transition | closed shells | 1 | PASS |
| lint-duct-transition | volume positive | 1416800.0 | PASS |
| lint-duct-transition | in the assembly with the same volume and place | True | PASS |
| lint-duct | one solid | 1 | PASS |
| lint-duct | valid B-rep (BRepCheck) | 1 | PASS |
| lint-duct | closed shells | 1 | PASS |
| lint-duct | volume positive | 2800224.0 | PASS |
| lint-duct | in the assembly with the same volume and place | True | PASS |
| post-1 | one solid | 1 | PASS |
| post-1 | valid B-rep (BRepCheck) | 1 | PASS |
| post-1 | closed shells | 1 | PASS |
| post-1 | volume positive | 1600000.0 | PASS |
| post-1 | in the assembly with the same volume and place | True | PASS |
| post-2 | one solid | 1 | PASS |
| post-2 | valid B-rep (BRepCheck) | 1 | PASS |
| post-2 | closed shells | 1 | PASS |
| post-2 | volume positive | 1600000.0 | PASS |
| post-2 | in the assembly with the same volume and place | True | PASS |
| post-3 | one solid | 1 | PASS |
| post-3 | valid B-rep (BRepCheck) | 1 | PASS |
| post-3 | closed shells | 1 | PASS |
| post-3 | volume positive | 1600000.0 | PASS |
| post-3 | in the assembly with the same volume and place | True | PASS |
| post-4 | one solid | 1 | PASS |
| post-4 | valid B-rep (BRepCheck) | 1 | PASS |
| post-4 | closed shells | 1 | PASS |
| post-4 | volume positive | 1600000.0 | PASS |
| post-4 | in the assembly with the same volume and place | True | PASS |
| rail-bottom-front | one solid | 1 | PASS |
| rail-bottom-front | valid B-rep (BRepCheck) | 1 | PASS |
| rail-bottom-front | closed shells | 1 | PASS |
| rail-bottom-front | volume positive | 976000.0 | PASS |
| rail-bottom-front | in the assembly with the same volume and place | True | PASS |
| rail-bottom-left | one solid | 1 | PASS |
| rail-bottom-left | valid B-rep (BRepCheck) | 1 | PASS |
| rail-bottom-left | closed shells | 1 | PASS |
| rail-bottom-left | volume positive | 1072000.0 | PASS |
| rail-bottom-left | in the assembly with the same volume and place | True | PASS |
| rail-bottom-rear | one solid | 1 | PASS |
| rail-bottom-rear | valid B-rep (BRepCheck) | 1 | PASS |
| rail-bottom-rear | closed shells | 1 | PASS |
| rail-bottom-rear | volume positive | 976000.0 | PASS |
| rail-bottom-rear | in the assembly with the same volume and place | True | PASS |
| rail-bottom-right | one solid | 1 | PASS |
| rail-bottom-right | valid B-rep (BRepCheck) | 1 | PASS |
| rail-bottom-right | closed shells | 1 | PASS |
| rail-bottom-right | volume positive | 1072000.0 | PASS |
| rail-bottom-right | in the assembly with the same volume and place | True | PASS |
| rail-mid-front-left | one solid | 1 | PASS |
| rail-mid-front-left | valid B-rep (BRepCheck) | 1 | PASS |
| rail-mid-front-left | closed shells | 1 | PASS |
| rail-mid-front-left | volume positive | 216000.0 | PASS |
| rail-mid-front-left | in the assembly with the same volume and place | True | PASS |
| rail-mid-front-right | one solid | 1 | PASS |
| rail-mid-front-right | valid B-rep (BRepCheck) | 1 | PASS |
| rail-mid-front-right | closed shells | 1 | PASS |
| rail-mid-front-right | volume positive | 216000.0 | PASS |
| rail-mid-front-right | in the assembly with the same volume and place | True | PASS |
| rail-mid-left | one solid | 1 | PASS |
| rail-mid-left | valid B-rep (BRepCheck) | 1 | PASS |
| rail-mid-left | closed shells | 1 | PASS |
| rail-mid-left | volume positive | 1072000.0 | PASS |
| rail-mid-left | in the assembly with the same volume and place | True | PASS |
| rail-mid-rear | one solid | 1 | PASS |
| rail-mid-rear | valid B-rep (BRepCheck) | 1 | PASS |
| rail-mid-rear | closed shells | 1 | PASS |
| rail-mid-rear | volume positive | 976000.0 | PASS |
| rail-mid-rear | in the assembly with the same volume and place | True | PASS |
| rail-mid-rearcross | one solid | 1 | PASS |
| rail-mid-rearcross | valid B-rep (BRepCheck) | 1 | PASS |
| rail-mid-rearcross | closed shells | 1 | PASS |
| rail-mid-rearcross | volume positive | 976000.0 | PASS |
| rail-mid-rearcross | in the assembly with the same volume and place | True | PASS |
| rail-mid-right | one solid | 1 | PASS |
| rail-mid-right | valid B-rep (BRepCheck) | 1 | PASS |
| rail-mid-right | closed shells | 1 | PASS |
| rail-mid-right | volume positive | 1072000.0 | PASS |
| rail-mid-right | in the assembly with the same volume and place | True | PASS |
| rail-top-front | one solid | 1 | PASS |
| rail-top-front | valid B-rep (BRepCheck) | 1 | PASS |
| rail-top-front | closed shells | 1 | PASS |
| rail-top-front | volume positive | 976000.0 | PASS |
| rail-top-front | in the assembly with the same volume and place | True | PASS |
| rail-top-left | one solid | 1 | PASS |
| rail-top-left | valid B-rep (BRepCheck) | 1 | PASS |
| rail-top-left | closed shells | 1 | PASS |
| rail-top-left | volume positive | 1072000.0 | PASS |
| rail-top-left | in the assembly with the same volume and place | True | PASS |
| rail-top-rear | one solid | 1 | PASS |
| rail-top-rear | valid B-rep (BRepCheck) | 1 | PASS |
| rail-top-rear | closed shells | 1 | PASS |
| rail-top-rear | volume positive | 976000.0 | PASS |
| rail-top-rear | in the assembly with the same volume and place | True | PASS |
| rail-top-rearcross | one solid | 1 | PASS |
| rail-top-rearcross | valid B-rep (BRepCheck) | 1 | PASS |
| rail-top-rearcross | closed shells | 1 | PASS |
| rail-top-rearcross | volume positive | 976000.0 | PASS |
| rail-top-rearcross | in the assembly with the same volume and place | True | PASS |
| rail-top-right | one solid | 1 | PASS |
| rail-top-right | valid B-rep (BRepCheck) | 1 | PASS |
| rail-top-right | closed shells | 1 | PASS |
| rail-top-right | volume positive | 1072000.0 | PASS |
| rail-top-right | in the assembly with the same volume and place | True | PASS |
| rear-bulkhead | one solid | 1 | PASS |
| rear-bulkhead | valid B-rep (BRepCheck) | 1 | PASS |
| rear-bulkhead | closed shells | 1 | PASS |
| rear-bulkhead | volume positive | 652348.5 | PASS |
| rear-bulkhead | in the assembly with the same volume and place | True | PASS |
| rear-bulkhead | section edges all closed | 0 | PASS |
| rear-bulkhead | every section loop is a circle, rectangle, slot or polygon | 139 loops, 0 unclassified | PASS |
| rear-bulkhead | every cut lies inside the outline | 138 | PASS |
| rear-bulkhead | no two cuts overlap | 0 overlapping pairs | PASS |
| rear-bulkhead.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| rear-bulkhead.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 139 matched, 0 only in STEP, 0 only in DXF | PASS |
| rear-bulkhead.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
| rear-lower-panel | one solid | 1 | PASS |
| rear-lower-panel | valid B-rep (BRepCheck) | 1 | PASS |
| rear-lower-panel | closed shells | 1 | PASS |
| rear-lower-panel | volume positive | 239717.0 | PASS |
| rear-lower-panel | in the assembly with the same volume and place | True | PASS |
| rear-lower-panel | section edges all closed | 0 | PASS |
| rear-lower-panel | every section loop is a circle, rectangle, slot or polygon | 43 loops, 0 unclassified | PASS |
| rear-lower-panel | every cut lies inside the outline | 42 | PASS |
| rear-lower-panel | no two cuts overlap | 0 overlapping pairs | PASS |
| rear-lower-panel.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| rear-lower-panel.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 43 matched, 0 only in STEP, 0 only in DXF | PASS |
| rear-lower-panel.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
| rear-upper-panel | one solid | 1 | PASS |
| rear-upper-panel | valid B-rep (BRepCheck) | 1 | PASS |
| rear-upper-panel | closed shells | 1 | PASS |
| rear-upper-panel | volume positive | 765004.1 | PASS |
| rear-upper-panel | in the assembly with the same volume and place | True | PASS |
| rear-upper-panel | section edges all closed | 0 | PASS |
| rear-upper-panel | every section loop is a circle, rectangle, slot or polygon | 19 loops, 0 unclassified | PASS |
| rear-upper-panel | every cut lies inside the outline | 18 | PASS |
| rear-upper-panel | no two cuts overlap | 0 overlapping pairs | PASS |
| rear-upper-panel.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| rear-upper-panel.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 19 matched, 0 only in STEP, 0 only in DXF | PASS |
| rear-upper-panel.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
| riser-duct | one solid | 1 | PASS |
| riser-duct | valid B-rep (BRepCheck) | 1 | PASS |
| riser-duct | closed shells | 1 | PASS |
| riser-duct | volume positive | 8339500.0 | PASS |
| riser-duct | in the assembly with the same volume and place | True | PASS |
| side-panel-left | one solid | 1 | PASS |
| side-panel-left | valid B-rep (BRepCheck) | 1 | PASS |
| side-panel-left | closed shells | 1 | PASS |
| side-panel-left | volume positive | 1123556.5 | PASS |
| side-panel-left | in the assembly with the same volume and place | True | PASS |
| side-panel-left | section edges all closed | 0 | PASS |
| side-panel-left | every section loop is a circle, rectangle, slot or polygon | 30 loops, 0 unclassified | PASS |
| side-panel-left | every cut lies inside the outline | 29 | PASS |
| side-panel-left | no two cuts overlap | 0 overlapping pairs | PASS |
| side-panel-left.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| side-panel-left.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 30 matched, 0 only in STEP, 0 only in DXF | PASS |
| side-panel-left.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
| side-panel-right | one solid | 1 | PASS |
| side-panel-right | valid B-rep (BRepCheck) | 1 | PASS |
| side-panel-right | closed shells | 1 | PASS |
| side-panel-right | volume positive | 1123556.5 | PASS |
| side-panel-right | in the assembly with the same volume and place | True | PASS |
| side-panel-right | section edges all closed | 0 | PASS |
| side-panel-right | every section loop is a circle, rectangle, slot or polygon | 30 loops, 0 unclassified | PASS |
| side-panel-right | every cut lies inside the outline | 29 | PASS |
| side-panel-right | no two cuts overlap | 0 overlapping pairs | PASS |
| side-panel-right.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| side-panel-right.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 30 matched, 0 only in STEP, 0 only in DXF | PASS |
| side-panel-right.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
| top-panel | one solid | 1 | PASS |
| top-panel | valid B-rep (BRepCheck) | 1 | PASS |
| top-panel | closed shells | 1 | PASS |
| top-panel | volume positive | 463699.8 | PASS |
| top-panel | in the assembly with the same volume and place | True | PASS |
| top-panel | section edges all closed | 0 | PASS |
| top-panel | every section loop is a circle, rectangle, slot or polygon | 11 loops, 0 unclassified | PASS |
| top-panel | every cut lies inside the outline | 10 | PASS |
| top-panel | no two cuts overlap | 0 overlapping pairs | PASS |
| top-panel.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| top-panel.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 11 matched, 0 only in STEP, 0 only in DXF | PASS |
| top-panel.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
| tray-rail-1 | one solid | 1 | PASS |
| tray-rail-1 | valid B-rep (BRepCheck) | 1 | PASS |
| tray-rail-1 | closed shells | 1 | PASS |
| tray-rail-1 | volume positive | 144000.0 | PASS |
| tray-rail-1 | in the assembly with the same volume and place | True | PASS |
| tray-rail-2 | one solid | 1 | PASS |
| tray-rail-2 | valid B-rep (BRepCheck) | 1 | PASS |
| tray-rail-2 | closed shells | 1 | PASS |
| tray-rail-2 | volume positive | 144000.0 | PASS |
| tray-rail-2 | in the assembly with the same volume and place | True | PASS |
| side-panel-left | every M6 hole sits on a frame rail centre line | 29 M6 holes, 0 off a rail | PASS |
| side-panel-right | every M6 hole sits on a frame rail centre line | 29 M6 holes, 0 off a rail | PASS |
| front-upper-panel | every M6 hole sits on a frame rail centre line | 16 M6 holes, 0 off a rail | PASS |
| front-lower-panel | every M6 hole sits on a frame rail centre line | 8 M6 holes, 0 off a rail | PASS |
| rear-upper-panel | every M6 hole sits on a frame rail centre line | 18 M6 holes, 0 off a rail | PASS |
| rear-lower-panel | every M6 hole sits on a frame rail centre line | 8 M6 holes, 0 off a rail | PASS |
| top-panel | every M6 hole sits on a frame rail centre line | 10 M6 holes, 0 off a rail | PASS |
| base-pan | every M6 hole sits on a frame rail centre line | 20 M6 holes, 0 off a rail | PASS |
| bay-ceiling | every M6 hole sits on a frame rail centre line | 20 M6 holes, 0 off a rail | PASS |
| front-bulkhead | every M6 hole sits on a frame rail centre line | 7 M6 holes, 0 off a rail | PASS |
| rear-bulkhead | every M6 hole sits on a frame rail centre line | 10 M6 holes, 0 off a rail | PASS |
| all parts | V-011: every round feature diameter is on the named list (4.5 M4 clearance, 5 louver slot ends (60 x 5), 6.5 M6 clearance, 8.5 M8 clearance, 10 inlet holes, 10.5 roller shafts, 22 cord strain relief bushing, 40 lint slot ends (260 x 40), 106 exhaust port (102 duct + 2 each side), 460 door opening, 470 door ring bore, 480 front panel ring opening / drum ring bore, 540 door disc, 560 door ring, 616.4 splice inside, 618.4 drum ring / sheet inside, 620 drum outside) | 0 off the list | PASS |
| air path | V-013: every opening in the air path is at least the blower outlet (102 round, 8171 mm2) | riser 13000, lint_duct 12096, lint_slot 10057, inlet_field 9896, exhaust_duct 8171 | PASS |
| assembly | no two solids overlap by more than 1 mm3 (file re-import) | 59 solids, 0 overlaps | PASS |
| assembly | every part file is a named solid in the assembly | 0 missing | PASS |
| drum-sheet.dxf | every hole in the rolled solid unwraps onto a hole in the flat pattern (0.05 mm) | 88 matched, 0 solid-only, 0 DXF-only | PASS |
| drum-sheet.dxf | flat pattern outline is the sheet's unrolled mid-surface length by its length plus the tabs | polygon 1945.274 x 590.000, 244 edges; unrolled 1945.274 | PASS |
| drum-splice.dxf | every hole in the curved splice unwraps onto a hole in the flat strip (0.05 mm) | 16 matched, 0 solid-only, 0 DXF-only | PASS |
| drum-splice.dxf | flat strip outline equals the curved strip's arc length by its length | 60.000 x 544.000; arc 60.010 x 544.000 | PASS |

## 4. Clearances measured in the assembly (mm)

| part a | part b | minimum distance |
|---|---|---|
| drum-sheet | front-bulkhead | 7.700 |
| drum-sheet | rear-bulkhead | 9.200 |
| drum-sheet | bay-ceiling | 20.000 |
| drum-sheet | side-panel-left | 35.000 |
| drum-sheet | side-panel-right | 35.000 |
| drum-sheet | top-panel | 58.500 |
| drum-sheet | rail-top-left | 138.260 |
| drum-sheet | rail-top-right | 138.260 |
| drum-sheet | rail-top-front | 21.030 |
| drum-sheet | roller-front-1 (bought) | 0.000 |
| drum-sheet | roller-front-2 (bought) | 0.000 |
| drum-sheet | roller-rear-1 (bought) | 0.000 |
| drum-sheet | roller-rear-2 (bought) | 0.000 |
| drum-sheet | drum-ring-front | 0.000 |
| drum-sheet | drum-ring-rear | 0.000 |
| drum-sheet | drum-splice | 0.000 |
| drum-sheet | baffle-1 (angle, cut to length) | 0.050 |
| drum-ring-front | front-bulkhead | 8.500 |
| drum-ring-rear | rear-bulkhead | 10.000 |
| door-ring | front-upper-panel | 0.000 |
| door-disc | door-ring | 8.000 |
| console-face | console-cheek-left | 0.000 |
| console-face | console-cheek-right | 0.000 |
| console-face | top-panel | 0.439 |
| console-face | console-cap | 0.000 |
| front-bulkhead | bay-ceiling | 0.500 |
| rear-bulkhead | bay-ceiling | 0.500 |
| lint-duct | rail-mid-front-left | 2.000 |
| lint-duct | rail-mid-front-right | 2.000 |
| lint-duct | front-bulkhead | 2.000 |
| lint-duct | front-upper-panel | 2.000 |
| riser-duct | rear-bulkhead | 42.000 |
| riser-duct | rail-mid-rear | 6.500 |
| riser-duct | bay-ceiling | 2.000 |
| heat-module (envelope) | heat-module-tray | 0.500 |
| heat-module (envelope) | bay-ceiling | 78.000 |
| motor (bought) | base-pan | 50.000 |
| blower (bought) | front-bulkhead | 55.057 |
| blower (bought) | lint-duct-transition | 0.000 |
| pulley (bought) | bay-ceiling | 166.108 |
| exhaust-duct (bought) | rear-lower-panel | 2.000 |
| power-module (envelope) | side-panel-left | 5.000 |
| power-module (envelope) | bay-ceiling | 80.000 |
| drum-sheet | front-upper-panel | 49.200 |

## 5. Inventory

Every part: bounding box, volume, faces. The full feature lists are in `measured-cylinders.csv` (every hole and round surface), `measured-planes.csv` (every flat face) and `measured-loops.csv` (every closed loop of every flat part's section and of every DXF).

| part | solids | X min..max | Y min..max | Z min..max | size | volume mm3 | faces (planar / cylindrical / other) | thickness | section loops |
|---|---|---|---|---|---|---|---|---|---|
| base-pan | 1 | -343.50..343.50 | 0.00..750.00 | -1.50..0.00 | 687.00 x 750.00 x 1.50 | 771879.5 | 26 (6 / 20 / 0) | 1.500 | 21 |
| bay-ceiling | 1 | -343.50..343.50 | 42.00..750.00 | 300.00..301.50 | 687.00 x 708.00 x 1.50 | 694781.0 | 42 (22 / 20 / 0) | 1.500 | 24 |
| console-cap | 1 | -345.00..345.00 | 563.14..750.00 | 1113.14..1114.64 | 690.00 x 186.86 x 1.50 | 193403.1 | 6 (6 / 0 / 0) | 1.500 | 1 |
| console-cheek-left | 1 | -345.00..-343.50 | 450.00..750.00 | 1000.00..1113.14 | 1.50 x 300.00 x 113.14 | 41311.7 | 6 (6 / 0 / 0) | 1.500 | 1 |
| console-cheek-right | 1 | 343.50..345.00 | 450.00..750.00 | 1000.00..1113.14 | 1.50 x 300.00 x 113.14 | 41311.7 | 6 (6 / 0 / 0) | 1.500 | 1 |
| console-face | 1 | -343.50..343.50 | 448.94..563.14 | 1000.00..1114.20 | 687.00 x 114.20 x 114.20 | 121584.6 | 14 (10 / 4 / 0) | 1.500 | 6 |
| door-disc | 1 | -270.00..270.00 | -13.50..-11.50 | 361.50..901.50 | 540.00 x 2.00 x 540.00 | 458044.2 | 3 (2 / 1 / 0) | 2.000 | 1 |
| door-ring | 1 | -280.00..280.00 | -3.50..-1.50 | 351.50..911.50 | 560.00 x 2.00 x 560.00 | 145612.8 | 4 (2 / 2 / 0) | 2.000 | 2 |
| drum-ring-front | 1 | -309.20..309.20 | 50.00..52.00 | 322.30..940.70 | 618.40 x 2.00 x 618.40 | 237835.9 | 34 (2 / 32 / 0) | 2.000 | 32 |
| drum-ring-rear | 1 | -309.20..309.20 | 598.00..600.00 | 322.30..940.70 | 618.40 x 2.00 x 618.40 | 237835.9 | 34 (2 / 32 / 0) | 2.000 | 32 |
| drum-sheet | 1 | -310.00..310.00 | 49.20..600.80 | 321.50..941.50 | 620.00 x 551.60 x 620.00 | 878507.5 | 480 (360 / 120 / 0) | | |
| drum-splice | 1 | -29.96..29.96 | 53.00..597.00 | 938.24..940.70 | 59.92 x 544.00 x 2.46 | 32391.2 | 22 (4 / 18 / 0) | | |
| front-bulkhead | 1 | -305.00..305.00 | 40.00..41.50 | 265.00..995.00 | 610.00 x 1.50 x 730.00 | 402971.5 | 20 (8 / 12 / 0) | 1.500 | 12 |
| front-lower-panel | 1 | -345.00..345.00 | -1.50..0.00 | 0.00..259.00 | 690.00 x 1.50 x 259.00 | 242917.5 | 238 (118 / 120 / 0) | 1.500 | 65 |
| front-upper-panel | 1 | -345.00..345.00 | -1.50..0.00 | 260.00..1000.00 | 690.00 x 1.50 x 740.00 | 493670.0 | 23 (6 / 17 / 0) | 1.500 | 18 |
| heat-module-tray | 1 | -160.00..160.00 | 420.00..670.00 | 60.00..61.50 | 320.00 x 250.00 x 1.50 | 120000.0 | 6 (6 / 0 / 0) | 1.500 | 1 |
| lint-duct-transition | 1 | -110.00..110.00 | 38.00..84.00 | 50.00..190.00 | 220.00 x 46.00 x 140.00 | 1416800.0 | 6 (6 / 0 / 0) | | |
| lint-duct | 1 | -168.00..168.00 | 2.00..38.00 | 150.00..381.50 | 336.00 x 36.00 x 231.50 | 2800224.0 | 6 (6 / 0 / 0) | | |
| post-1 | 1 | -345.00..-305.00 | 0.00..40.00 | 0.00..1000.00 | 40.00 x 40.00 x 1000.00 | 1600000.0 | 6 (6 / 0 / 0) | | |
| post-2 | 1 | 305.00..345.00 | 0.00..40.00 | 0.00..1000.00 | 40.00 x 40.00 x 1000.00 | 1600000.0 | 6 (6 / 0 / 0) | | |
| post-3 | 1 | -345.00..-305.00 | 710.00..750.00 | 0.00..1000.00 | 40.00 x 40.00 x 1000.00 | 1600000.0 | 6 (6 / 0 / 0) | | |
| post-4 | 1 | 305.00..345.00 | 710.00..750.00 | 0.00..1000.00 | 40.00 x 40.00 x 1000.00 | 1600000.0 | 6 (6 / 0 / 0) | | |
| rail-bottom-front | 1 | -305.00..305.00 | 0.00..40.00 | 0.00..40.00 | 610.00 x 40.00 x 40.00 | 976000.0 | 6 (6 / 0 / 0) | | |
| rail-bottom-left | 1 | -345.00..-305.00 | 40.00..710.00 | 0.00..40.00 | 40.00 x 670.00 x 40.00 | 1072000.0 | 6 (6 / 0 / 0) | | |
| rail-bottom-rear | 1 | -305.00..305.00 | 710.00..750.00 | 0.00..40.00 | 610.00 x 40.00 x 40.00 | 976000.0 | 6 (6 / 0 / 0) | | |
| rail-bottom-right | 1 | 305.00..345.00 | 40.00..710.00 | 0.00..40.00 | 40.00 x 670.00 x 40.00 | 1072000.0 | 6 (6 / 0 / 0) | | |
| rail-mid-front-left | 1 | -305.00..-170.00 | 0.00..40.00 | 260.00..300.00 | 135.00 x 40.00 x 40.00 | 216000.0 | 6 (6 / 0 / 0) | | |
| rail-mid-front-right | 1 | 170.00..305.00 | 0.00..40.00 | 260.00..300.00 | 135.00 x 40.00 x 40.00 | 216000.0 | 6 (6 / 0 / 0) | | |
| rail-mid-left | 1 | -345.00..-305.00 | 40.00..710.00 | 260.00..300.00 | 40.00 x 670.00 x 40.00 | 1072000.0 | 6 (6 / 0 / 0) | | |
| rail-mid-rear | 1 | -305.00..305.00 | 710.00..750.00 | 260.00..300.00 | 610.00 x 40.00 x 40.00 | 976000.0 | 6 (6 / 0 / 0) | | |
| rail-mid-rearcross | 1 | -305.00..305.00 | 611.50..651.50 | 260.00..300.00 | 610.00 x 40.00 x 40.00 | 976000.0 | 6 (6 / 0 / 0) | | |
| rail-mid-right | 1 | 305.00..345.00 | 40.00..710.00 | 260.00..300.00 | 40.00 x 670.00 x 40.00 | 1072000.0 | 6 (6 / 0 / 0) | | |
| rail-top-front | 1 | -305.00..305.00 | 0.00..40.00 | 960.00..1000.00 | 610.00 x 40.00 x 40.00 | 976000.0 | 6 (6 / 0 / 0) | | |
| rail-top-left | 1 | -345.00..-305.00 | 40.00..710.00 | 960.00..1000.00 | 40.00 x 670.00 x 40.00 | 1072000.0 | 6 (6 / 0 / 0) | | |
| rail-top-rear | 1 | -305.00..305.00 | 710.00..750.00 | 960.00..1000.00 | 610.00 x 40.00 x 40.00 | 976000.0 | 6 (6 / 0 / 0) | | |
| rail-top-rearcross | 1 | -305.00..305.00 | 611.50..651.50 | 960.00..1000.00 | 610.00 x 40.00 x 40.00 | 976000.0 | 6 (6 / 0 / 0) | | |
| rail-top-right | 1 | 305.00..345.00 | 40.00..710.00 | 960.00..1000.00 | 40.00 x 670.00 x 40.00 | 1072000.0 | 6 (6 / 0 / 0) | | |
| rear-bulkhead | 1 | -305.00..305.00 | 610.00..611.50 | 265.00..995.00 | 610.00 x 1.50 x 730.00 | 652348.5 | 144 (6 / 138 / 0) | 1.500 | 139 |
| rear-lower-panel | 1 | -345.00..345.00 | 750.00..751.50 | 0.00..259.00 | 690.00 x 1.50 x 259.00 | 239717.0 | 144 (70 / 74 / 0) | 1.500 | 43 |
| rear-upper-panel | 1 | -345.00..345.00 | 750.00..751.50 | 260.00..1000.00 | 690.00 x 1.50 x 740.00 | 765004.1 | 24 (6 / 18 / 0) | 1.500 | 19 |
| riser-duct | 1 | -130.00..130.00 | 653.50..703.50 | 180.00..821.50 | 260.00 x 50.00 x 641.50 | 8339500.0 | 6 (6 / 0 / 0) | | |
| side-panel-left | 1 | -346.50..-345.00 | 0.00..750.00 | 0.00..1000.00 | 1.50 x 750.00 x 1000.00 | 1123556.5 | 35 (6 / 29 / 0) | 1.500 | 30 |
| side-panel-right | 1 | 345.00..346.50 | 0.00..750.00 | 0.00..1000.00 | 1.50 x 750.00 x 1000.00 | 1123556.5 | 35 (6 / 29 / 0) | 1.500 | 30 |
| top-panel | 1 | -345.00..345.00 | 0.00..448.50 | 1000.00..1001.50 | 690.00 x 448.50 x 1.50 | 463699.8 | 16 (6 / 10 / 0) | 1.500 | 11 |
| tray-rail-1 | 1 | -170.00..-150.00 | 340.00..700.00 | 40.00..60.00 | 20.00 x 360.00 x 20.00 | 144000.0 | 6 (6 / 0 / 0) | | |
| tray-rail-2 | 1 | 150.00..170.00 | 340.00..700.00 | 40.00..60.00 | 20.00 x 360.00 x 20.00 | 144000.0 | 6 (6 / 0 / 0) | | |

Bought parts and envelopes in the assembly (no part file):

| solid | X min..max | Y min..max | Z min..max | volume mm3 |
|---|---|---|---|---|
| baffle-1 (angle, cut to length) | -277.17..-241.03 | 85.00..565.00 | 748.43..803.07 | 110481.8 |
| baffle-2 (angle, cut to length) | -20.00..20.00 | 85.00..565.00 | 323.00..363.00 | 110481.8 |
| baffle-3 (angle, cut to length) | 222.53..277.17 | 85.00..565.00 | 766.93..803.07 | 110481.8 |
| motor (bought) | -70.00..70.00 | 190.00..390.00 | 50.00..190.00 | 3078760.8 |
| pulley (bought) | -15.00..15.00 | 394.00..410.00 | 105.00..135.00 | 11309.7 |
| blower (bought) | -110.00..110.00 | 84.00..184.00 | 10.00..230.00 | 3801327.1 |
| heat-module (envelope) | -140.00..140.00 | 440.00..650.00 | 62.00..222.00 | 9408000.0 |
| power-module (envelope) | -340.00..-170.00 | 450.00..700.00 | 40.00..220.00 | 7650000.0 |
| exhaust-duct (bought) | 179.00..281.00 | 184.00..750.00 | 99.00..201.00 | 4624945.9 |
| roller-rear-1 (bought) | -200.00..-140.00 | 575.00..600.00 | 307.05..367.05 | 70685.8 |
| roller-front-1 (bought) | -200.00..-140.00 | 50.00..75.00 | 307.05..367.05 | 70685.8 |
| roller-rear-2 (bought) | 140.00..200.00 | 575.00..600.00 | 307.05..367.05 | 70685.8 |
| roller-front-2 (bought) | 140.00..200.00 | 50.00..75.00 | 307.05..367.05 | 70685.8 |

DXF drawings:

| drawing | entities | closed loops | open chains | loops by type |
|---|---|---|---|---|
| base-pan | CIRCLE 20, LINE 4 | 21 | 0 | circle 20, rect 1 |
| bay-ceiling | CIRCLE 20, LINE 20 | 24 | 0 | circle 20, polygon 1, rect 3 |
| console-cap | LINE 4 | 1 | 0 | rect 1 |
| console-cheek-left | LINE 4 | 1 | 0 | polygon 1 |
| console-cheek-right | LINE 4 | 1 | 0 | polygon 1 |
| console-face | CIRCLE 4, LINE 8 | 6 | 0 | circle 4, rect 2 |
| door-disc | CIRCLE 1 | 1 | 0 | circle 1 |
| door-ring | CIRCLE 2 | 2 | 0 | circle 2 |
| drum-ring | CIRCLE 32 | 32 | 0 | circle 32 |
| drum-sheet | CIRCLE 88, LINE 244 | 89 | 0 | circle 88, polygon 1 |
| drum-splice | CIRCLE 16, LINE 4 | 17 | 0 | circle 16, rect 1 |
| front-bulkhead | ARC 2, CIRCLE 10, LINE 6 | 12 | 0 | circle 10, rect 1, slot 1 |
| front-lower-panel | ARC 112, CIRCLE 8, LINE 116 | 65 | 0 | circle 8, rect 1, slot 56 |
| front-upper-panel | CIRCLE 17, LINE 4 | 18 | 0 | circle 17, rect 1 |
| rear-bulkhead | CIRCLE 138, LINE 4 | 139 | 0 | circle 138, rect 1 |
| rear-lower-panel | ARC 64, CIRCLE 10, LINE 68 | 43 | 0 | circle 10, rect 1, slot 32 |
| rear-upper-panel | CIRCLE 18, LINE 4 | 19 | 0 | circle 18, rect 1 |
| side-panel-left | CIRCLE 29, LINE 4 | 30 | 0 | circle 29, rect 1 |
| side-panel-right | CIRCLE 29, LINE 4 | 30 | 0 | circle 29, rect 1 |
| top-panel | CIRCLE 10, LINE 4 | 11 | 0 | circle 10, rect 1 |

## Notes

- drum-sheet.dxf offset from the unwrapped solid: (0.000, -0.000)
- drum-splice.dxf offset from the unwrapped solid: (-0.005, -0.000)
