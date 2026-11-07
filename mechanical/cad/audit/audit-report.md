# CAD audit report

Produced by `mechanical/cad/cad_audit.py` from the STEP and DXF files on disk. Every number below was measured from the files, not read from the script.

Parts measured: 80 STEP files, 213 named solids in the assembly, 48 DXF drawings.
Document checks: 603, generic checks: 741, Fusion comparisons: 1099. **Failures: 0.**

## 1. Values stated in the documents, against the files

| id | part | check | expected | measured | result | source |
|---|---|---|---|---|---|---|
| A-001 | assembly | assembly_solids | 213 | 213 | PASS | 7a: made parts, bought parts and envelopes, and the hardware sets, each one named solid or compound (draft 9 adds the blower plate and its feet, the exhaust duct set, the tap, barb and tube, the two sensors, the two blanks, the cable clamps and their hardware) |
| A-002 | assembly | assembly_size x | 704.2 | 704.2 | PASS | 7: 690 wide cabinet + two 1.5 side panels + the side panels' bolt heads (1.6 washer + 4 hex) each side |
| A-003 | assembly | assembly_min x | -352.1 | -352.1 | PASS | 7: half width 345 + 1.5 panel + 5.6 bolt head |
| A-004 | assembly | assembly_max x | 352.1 | 352.1 | PASS | 7: half width 345 + 1.5 panel + 5.6 bolt head |
| A-005 | assembly | assembly_min y | -57 | -57.0 | PASS | 7a Door: handle bar (14 round) on 30 standoffs in front of the disc at -13.5: -13.5 - 30 - 14 + 0.5 overlap |
| A-006 | assembly | assembly_max y | 820 | 820.0 | PASS | 7: 750 deep + 1.5 rear panel; the cord (draft 6: through the base pan, under the pan to the back) is drawn 70 past the panel |
| A-007 | assembly | assembly_min z | -19.5 | -19.5 | PASS | 7c Feet: 10 pad + 8 hex under the 1.5 base pan (draft 6: 18 under the pan, room for the cord to pass under) |
| A-008 | assembly | assembly_max z | 1208.6 | 1208.6 | PASS | 7a Console: 1000 + 1.5 top panel + 200 frame + 1.5 cap = 1203; the cap's bolt heads (1.6 washer + 4 hex) reach 1208.6 |
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
| F-017 | rail-bottom-front | max z | 40 | 40.00000000000007 | PASS | 7a Frame bottom level 0..40 |
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
| F-040 | rail-top-front | max z | 1000 | 1000.0000000000001 | PASS | 7a Frame top level 960..1000 |
| F-041 | rail-top-rear | size x | 610 | 610.0 | PASS | 7a Frame |
| F-042 | rail-top-left | size y | 670 | 670.0 | PASS | 7a Frame |
| F-043 | rail-top-right | size y | 670 | 670.0 | PASS | 7a Frame |
| F-044 | rail-top-rearcross | size x | 610 | 610.0 | PASS | 7a Frame |
| F-045 | rail-top-rearcross | min y | 611.5 | 611.5 | PASS | 7a Frame |
| F-046 | rail-top-rearcross | min z | 960 | 960.0 | PASS | 7a Frame |
| F-047 | tray-rail-1 | size y | 750 | 750.0 | PASS | 7a Frame (draft 7): 2020 tray rails the full depth of the cabinet, on the bottom end rails |
| F-048 | tray-rail-1 | size x | 20 | 20.0 | PASS | 7a Frame 2020 |
| F-049 | tray-rail-1 | size z | 20 | 20.000000000000085 | PASS | 7a Frame 2020 |
| F-050 | tray-rail-1 | min z | 40 | 40.0 | PASS | 7a Frame: on the bottom rails |
| F-051 | tray-rail-2 | size y | 750 | 750.0 | PASS | 7a Frame (draft 7) |
| F-052 | tray-rail-2 | min z | 40 | 40.0 | PASS | 7a Frame |
| F-052b | tray-rail-1 | min y | 0 | -1.1102230246251565e-15 | PASS | 7a Frame (draft 7): from the front bottom rail to the rear one |
| F-052c | tray-rail-brackets (bought, 4 x 2020 inside corner brackets) | solids | 4 | 4 | PASS | 7a Frame (draft 7): one 2020 inside corner bracket at each end of each tray rail, on the end rail's top slot |
| F-052d | hardware-tray-rails (bought, 8 x M4 x 8 button head, T-nuts for the 6 and 8 mm slots) | solids | 8 | 8 | PASS | 7a Frame (draft 7): two M4 per bracket |
| F-062 | console-post-1 | size z | 200 | 200.0 | PASS | 7a Console: posts 200, the console height |
| F-063 | console-post-1 | size x | 40 | 40.0 | PASS | 7a Console 4040 |
| F-064 | console-post-1 | min x | -345 | -345.0 | PASS | 7a Console: posts at the cabinet's width, over the side rails |
| F-065 | console-post-1 | min y | 611.5 | 611.5 | PASS | 7a Console: front posts over the top rear cross rail (611.5..651.5) |
| F-066 | console-post-1 | min z | 1001.5 | 1001.5 | PASS | 7a Console: on the top panel (1000 + 1.5) |
| F-067 | console-post-4 | max x | 345 | 345.0 | PASS | 7a Console |
| F-068 | console-post-4 | max y | 750 | 750.0 | PASS | 7a Console: rear posts over the cabinet's rear posts |
| F-069 | console-post-4 | max z | 1201.5 | 1201.5 | PASS | 7a Console: 1001.5 + 200 |
| F-070 | console-rail-front | size x | 610 | 610.0 | PASS | 7a Console: end rails 610 between the posts, like the cabinet's |
| F-071 | console-rail-front | min z | 1161.5 | 1161.5 | PASS | 7a Console: top rails in the top 40 |
| F-072 | console-rail-front | max z | 1201.5 | 1201.5 | PASS | 7a Console |
| F-073 | console-rail-front | min y | 611.5 | 611.5 | PASS | 7a Console |
| F-074 | console-rail-rear | max y | 750 | 750.0 | PASS | 7a Console |
| F-075 | console-rail-left | size y | 58.5 | 58.5 | PASS | 7a Console: side rails between the posts: 138.5 - 2 x 40 |
| F-076 | console-rail-left | min x | -345 | -345.0 | PASS | 7a Console |
| F-077 | console-rail-right | max x | 345 | 345.0 | PASS | 7a Console |
| F-053 | cut-list | cut post-1 | 1000 | 1000.0 | PASS | frame-cut-list.csv |
| F-054 | cut-list | cut rail-bottom-left | 670 | 670.0 | PASS | frame-cut-list.csv |
| F-055 | cut-list | cut rail-bottom-front | 610 | 610.0 | PASS | frame-cut-list.csv |
| F-056 | cut-list | cut rail-mid-front-left | 135 | 135.0 | PASS | frame-cut-list.csv |
| F-057 | cut-list | cut rail-mid-rearcross | 610 | 610.0 | PASS | frame-cut-list.csv |
| F-058 | cut-list | cut tray-rail-1 | 750 | 750.0 | PASS | frame-cut-list.csv (draft 7) |
| F-058b | cut-list | cut console-post-1 | 200 | 200.0 | PASS | frame-cut-list.csv (7a Console) |
| F-058c | cut-list | cut console-rail-front | 610 | 610.0 | PASS | frame-cut-list.csv (7a Console) |
| F-058d | cut-list | cut console-rail-left | 58.5 | 58.5 | PASS | frame-cut-list.csv (7a Console) |
| F-059 | cut-list | cut baffle-1..3 | 480 | 480.0 | PASS | 7b Baffles 480 long |
| F-060 | cut-list | cut_qty baffle-1..3 | 3 | 3 | PASS | 7b three baffles |
| F-061 | cut-list | cut belt (bought) | 2222 | 2222.0 | PASS | 7a Drive: length of the drawn path round the drum (R 310 + half the 3.5 belt), the 20 pulley (draft 7) and the 40 idler at (-60, 165), nearest catalog J length chosen at V-012 |
| B-001 | front-bulkhead | size x | 610 | 610.0 | PASS | 7a Bulkheads 610 wide |
| B-002 | front-bulkhead | thickness | 1.5 | 1.5 | PASS | 7a Bulkheads 1.5 steel |
| B-003 | front-bulkhead | normal | 0,1,0 | (-0.0, -1.0, -0.0) | PASS | 7a: front-facing plate |
| B-004 | front-bulkhead | min y | 40 | 40.0 | PASS | 7a: sits behind the front rails (0..40) |
| B-005 | front-bulkhead | min z | 265 | 265.0 | PASS | 7a: from the mid rails (260..300) to the top rails, 5 in from each rail edge |
| B-006 | front-bulkhead | max z | 995 | 995.0 | PASS | 7a: to the top rails (960..1000) |
| B-007 | front-bulkhead | loop circle;0;631.5;460;460 | 1 | 1 | PASS | 7a: door opening 460 on the drum axis; axis Z = 300 + 1.5 + 20 + 310 |
| B-008 | front-bulkhead | loop sector;0;401.727;313.877;74.454 | 1 | 1 | PASS | 7a Bulkheads (draft 8): curved lint slot between radii 238 and 267 about the drum axis (8 outside the 460 opening, 3 inside the 540 bore), 36 degrees each side of straight down: its box is 2 x 267 sin 36 wide, from 631.5 - 267 to 631.5 - 238 cos 36 high |
| B-009 | front-bulkhead | hole_at 8.5;-180.173;343.164 | 1 | (-180.173, 343.164) d 8.500 | PASS | 7b Rollers (draft 7): 8.5 holes for the roller studs' M8 threads, 32 degrees each side of bottom on radius 310 + 30 = 340: 340 sin 32 = 180.173, 631.5 - 340 cos 32 = 343.164 (30 degrees put the studs' nuts into the lint duct's sides) |
| B-010 | front-bulkhead | hole_at 8.5;180.173;343.164 | 1 | (180.173, 343.164) d 8.500 | PASS | 7b roller stud holes (draft 7) |
| B-011 | front-bulkhead | holes 8.5;y | 2 | 2 | PASS | 7b two rollers per bulkhead |
| B-011b | front-bulkhead | holes 4.5;y | 12 | 12 | PASS | 7b Seals (draft 7): two M4 per drum glide, two glides per bulkhead; draft 8 adds six for the lint box's side bars; draft 9 two for the moisture bar set |
| B-011c | front-bulkhead | hole_at 4.5;-207.889;822.419 | 1 | (-207.889, 822.419) d 4.500 | PASS | 7b Seals (draft 7): glide at 45 degrees from straight up on radius 282 (centre -199.404, 830.904), holes 12 each side along the tangent: -199.404 - 12 cos 45, 830.904 - 12 sin 45 |
| B-012 | front-bulkhead | outline 610;730 | 1 | rrect 610.000 x 730.000 | PASS | 7a Bulkheads |
| B-013 | rear-bulkhead | size x | 610 | 610.0 | PASS | 7a Bulkheads |
| B-014 | rear-bulkhead | thickness | 1.5 | 1.5 | PASS | 7a Bulkheads |
| B-015 | rear-bulkhead | min y | 610 | 610.0 | PASS | 7a: in front of the rear cross rails; drum front 50 + length 550 + 10 |
| B-016 | rear-bulkhead | hole_at 8.5;-180.173;343.164 | 1 | (-180.173, 343.164) d 8.500 | PASS | 7b roller stud holes (draft 7) |
| B-017 | rear-bulkhead | hole_at 8.5;180.173;343.164 | 1 | (180.173, 343.164) d 8.500 | PASS | 7b roller stud holes (draft 7) |
| B-018 | rear-bulkhead | holes 10;y | 126 | 126 | PASS | 7a: inlet field 200 x 130 above the axis, 10 mm holes on a 14 pitch: 14 x 9 |
| B-019 | rear-bulkhead | hole_at 10;-93;681.5 | 1 | (-93.000, 681.500) d 10.000 | PASS | 7a inlet field: first hole 7 in from the field edge, field starts 50 above the axis |
| B-020 | rear-bulkhead | hole_at 10;89;793.5 | 1 | (89.000, 793.500) d 10.000 | PASS | 7a inlet field: last hole |
| B-021 | rear-bulkhead | loops circle | 152 | 152 | PASS | 7a: 126 inlet + 2 roller + 10 M6 + 4 glide M4 + 10 nozzle M4 (draft 8) |
| B-022 | rear-bulkhead | outline 610;730 | 1 | rrect 610.000 x 730.000 | PASS | 7a Bulkheads |
| C-001 | bay-ceiling | thickness | 1.5 | 1.5 | PASS | 7a Bay ceiling 1.5 plate |
| C-002 | bay-ceiling | min z | 300 | 300.0 | PASS | 7a: on the mid rails (top at 300) |
| C-003 | bay-ceiling | min y | 42 | 42.0 | PASS | 7a: starts 0.5 behind the front bulkhead (40 + 1.5) |
| C-004 | bay-ceiling | max y | 750 | 750.0 | PASS | 7a |
| C-005 | bay-ceiling | size x | 687 | 687.0 | PASS | 7a: between the side panels, 690 - 2 x 1.5 |
| C-006 | bay-ceiling | loop rect;-137.9;402;40;90 | 1 | 1 | PASS | 7a: left belt slot where the run from the idler to the drum crosses the plate, Y 402 (draft 4: the belt could not pass a single slot on the centre line) |
| C-006b | bay-ceiling | loop rect;145.4;402;40;90 | 1 | 1 | PASS | 7a: right belt slot where the run from the drum to the 20 pulley (draft 7) crosses the plate |
| C-007 | bay-ceiling | loop rect;0;610.75;612;2.5 | 1 | 1 | PASS | 7a: rear bulkhead passes through (610..611.5, 1 mm clearance) |
| C-008 | bay-ceiling | loop rect;0;679;264;57 | 1 | 1 | PASS | 7a (draft 8): the riser trunk's plates (260 x 53) through the ceiling behind the rear cross rail with 2 mm clearance |
| C-009 | bay-ceiling | holes 6.5;z | 20 | 20 | PASS | 7a Panels: M6 at 150 pitch; 5 on the rear cross rail, 5 on the rear rail, 5 on each side rail |
| C-010 | bay-ceiling | loops rpoly | 1 | 1 | PASS | 7a: outline notched at the two rear posts, 6 mm corner radii (draft 5) |
| C-010b | bay-ceiling | hole_at 22;-275;690 | 1 | (-275.000, 690.000) d 22.000 | PASS | 7a Panels (draft 7): grommet over the cord bushing; the cord comes up through the bay to the power module |
| C-010c | bay-ceiling | hole_at 30;-200;690 | 1 | (-200.000, 690.000) d 30.000 | PASS | 7a Panels (draft 7): grommet for the bay harness (motor, heat module, door switch leads) down from the power module |
| C-010d | bay-ceiling | loop rect;-225;652.25;152;3.5 | 1 | 1 | PASS | 7a Power module (draft 7): the plate on the rear cross rails' rear faces (Y 651.5..653, X -300..-150) passes through the ceiling with 1 mm each side |
| C-010e | bay-ceiling | loops circle | 23 | 23 | PASS | 7a: 20 M6, the two harness grommet holes and the door switch cable's grommet hole (draft 8) |
| C-011 | base-pan | thickness | 1.5 | 1.5 | PASS | 7a Panels 1.5 steel |
| C-012 | base-pan | max z | 0 | 0.0 | PASS | 7a: under the frame |
| C-013 | base-pan | size x | 687 | 687.0 | PASS | 7a between the side panels |
| C-014 | base-pan | size y | 750 | 750.0 | PASS | 7a |
| C-015 | base-pan | holes 6.5;z | 34 | 34 | PASS | 7a Panels M6 at 150 pitch: 20 to the rails plus 4 through-bolted for the idler and spring brackets, 4 for the motor cradles and 2 for the PS1 bracket (draft 8), 4 for the blower plate's feet (draft 9) |
| C-016 | base-pan | loops circle | 43 | 43 | PASS | 7a: 34 M6, 4 feet holes, the cord bushing hole and 4 M4 cable clamp holes (draft 8); no other cut-outs in the base pan |
| C-016b | base-pan | holes 8.5;z | 4 | 4 | PASS | 7c Feet: M8 studs through the pan into the posts' centre bores |
| C-016c | base-pan | hole_at 8.5;-325;20 | 1 | (-325.000, 20.000) d 8.500 | PASS | 7c Feet: on the post centres |
| C-016d | base-pan | hole_at 8.5;325;730 | 1 | (325.000, 730.000) d 8.500 | PASS | 7c Feet |
| C-016e | base-pan | hole_at 6.5;-128;370 | 1 | (-128.000, 370.000) d 6.500 | PASS | 7a Drive: idler bracket bolt, nut under the pan |
| C-016f | base-pan | hole_at 6.5;75;370 | 1 | (75.000, 370.000) d 6.500 | PASS | 7a Drive: spring bracket bolt |
| C-016g | base-pan | hole_at 22;-275;690 | 1 | (-275.000, 690.000) d 22.000 | PASS | 7a Panels (draft 7): cord strain relief bushing through the pan at the rear left, under its ceiling grommet |
| C-017 | base-pan | outline 687;750 | 1 | rrect 687.000 x 750.000 | PASS | 7a |
| P-001 | side-panel-left | thickness | 1.5 | 1.5 | PASS | 7a Panels |
| P-002 | side-panel-left | max x | -345 | -345.0 | PASS | 7: 690 wide |
| P-003 | side-panel-left | size y | 750 | 750.0 | PASS | 7: 750 deep |
| P-004 | side-panel-left | size z | 1000 | 1000.0 | PASS | 7a Frame posts 1000 |
| P-005 | side-panel-left | holes 6.5;x | 29 | 29 | PASS | 7a: 7 per post x 2, 5 per rail x 3 levels |
| P-006 | side-panel-left | outline 750;1000 | 1 | rrect 750.000 x 1000.000 | PASS | 7a |
| P-007 | side-panel-right | min x | 345 | 345.0 | PASS | 7: 690 wide |
| P-008 | side-panel-right | holes 6.5;x | 29 | 29 | PASS | 7a |
| P-009 | side-panel-right | outline 750;1000 | 1 | rrect 750.000 x 1000.000 | PASS | 7a |
| P-010 | front-upper-panel | thickness | 1.5 | 1.5 | PASS | 7a Panels |
| P-011 | front-upper-panel | max y | 0 | 0.0 | PASS | 7a: on the front of the frame |
| P-012 | front-upper-panel | size x | 690 | 690.0 | PASS | 7: 690 wide |
| P-013 | front-upper-panel | min z | 260 | 260.0 | PASS | 7a: the front panels split at the bottom of the mid rail (260) so the upper one bolts to that rail |
| P-014 | front-upper-panel | max z | 1000 | 1000.0 | PASS | 7a |
| P-015 | front-upper-panel | loop circle;0;631.5;480;480 | 1 | 1 | PASS | 7a Door: ring opening, 470 ring bore + 10 |
| P-016 | front-upper-panel | holes 6.5;y | 18 | 18 | PASS | 7a: 5 per post x 2, 2 on the mid stubs, 4 on the top rail, plus 2 for the fixed hinge leaf (nuts behind) |
| P-016b | front-upper-panel | holes 4.5;y | 10 | 10 | PASS | 7a Door: the ring's 8 M4 bolts pass through the panel; draft 8 adds the door switch's two ear holes |
| P-016c | front-upper-panel | hole_at 4.5;237.899;730.041 | 1 | (237.899, 730.041) d 4.500 | PASS | 7a Door: ring bolts on radius 257.5 at 22.5 + 45 k degrees: (257.5 cos 22.5, 631.5 + 257.5 sin 22.5) |
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
| P-027 | rear-lower-panel | loops circle | 15 | 15 | PASS | 7a: the exhaust port and 8 M6; the cord enters through the base pan (draft 6), not this panel; draft 9 adds the gas entry (25), the condensate drain (20) and their blanks' four M4 |
| P-028 | rear-lower-panel | loops slot | 32 | 32 | PASS | 7a: louvers, 4 columns x 8 rows, clear of the exhaust port |
| P-029 | rear-lower-panel | holes 6.5;y | 8 | 8 | PASS | 7a: 2 per post x 2, 4 on the bottom rail |
| P-030 | top-panel | min z | 1000 | 1000.0 | PASS | 7a: on the top rails |
| P-031 | top-panel | thickness | 1.5 | 1.5 | PASS | 7a Panels |
| P-032 | top-panel | max y | 750 | 750.0 | PASS | 7a Console (draft 6): the top panel runs the full depth; the console stands on it |
| P-033 | top-panel | size x | 690 | 690.0 | PASS | 7 |
| P-034 | top-panel | holes 6.5;z | 20 | 20 | PASS | 7a: 4 on the front rail, 4 on the rear rail, 4 on each side rail (none under the console posts), 4 for the console's foot brackets |
| P-034b | top-panel | hole_at 6.5;282;631.5 | 1 | (282.000, 631.500) d 6.500 | PASS | 7a Console (draft 6): foot bracket bolt into the top rear cross rail's top slot, 23 inboard of the post |
| P-034c | top-panel | hole_at 6.5;-282;730 | 1 | (-282.000, 730.000) d 6.500 | PASS | 7a Console (draft 6): foot bracket bolt into the rear top rail's top slot |
| P-034d | top-panel | hole_at 22;-225;690 | 1 | (-225.000, 690.000) d 22.000 | PASS | 7a Power module (draft 7): grommet for the console harness, up from the power module into the console |
| P-034e | top-panel | loops circle | 21 | 21 | PASS | 7a: 20 M6 and the console harness grommet (draft 7) |
| K-001 | console-face | thickness | 1.5 | 1.5 | PASS | 7a all flat plates 1.5 |
| K-002 | console-face | normal | 0,1,0 | (-0.0, -1.0, -0.0) | PASS | 7a: vertical, facing front |
| K-003 | console-face | outline 690;200 | 1 | rrect 690.000 x 200.000 | PASS | 7a: 690 wide between the cheeks, 200 tall from the top panel to the top of the frame |
| K-004 | console-face | loop rect;0;1084.5;560;120 | 1 | 1 | PASS | uci-spec 4.1 (draft 6) aperture 560 x 120, centred 83 above the top panel's top (1001.5) |
| K-005 | console-face | hole_at 4.5;-295;1014.5 | 1 | (-295.000, 1014.500) d 4.500 | PASS | uci-spec 4.1 (draft 6) holes on 590 x 140 and the centre line |
| K-006 | console-face | hole_at 4.5;295;1014.5 | 1 | (295.000, 1014.500) d 4.500 | PASS | uci-spec 4.1 |
| K-007 | console-face | hole_at 4.5;-295;1154.5 | 1 | (-295.000, 1154.500) d 4.500 | PASS | uci-spec 4.1 |
| K-008 | console-face | hole_at 4.5;295;1154.5 | 1 | (295.000, 1154.500) d 4.500 | PASS | uci-spec 4.1 |
| K-008b | console-face | hole_at 4.5;0;1014.5 | 1 | (0.000, 1014.500) d 4.500 | PASS | uci-spec 4.1: the two centre-line holes |
| K-008c | console-face | hole_at 4.5;0;1154.5 | 1 | (0.000, 1154.500) d 4.500 | PASS | uci-spec 4.1 |
| K-009 | console-face | holes 4.5 | 6 | 6 | PASS | uci-spec 4.1 six holes |
| K-010 | console-face | min y | 610 | 610.0 | PASS | 7a: on the front faces of the front posts (611.5), 1.5 thick |
| K-011 | console-face | min z | 1001.5 | 1001.5 | PASS | 7a: on the top panel |
| K-012 | console-face | max z | 1201.5 | 1201.5 | PASS | 7a: to the top of the frame |
| K-012b | console-face | holes 6.5;y | 8 | 8 | PASS | 7a Console: 2 per front post, 4 on the front rail at 150 pitch |
| K-013 | console-cap | min z | 1201.5 | 1201.5 | PASS | 7a: on the frame |
| K-014 | console-cap | min y | 610 | 610.0 | PASS | 7a: over the face plate |
| K-015 | console-cap | max y | 751.5 | 751.5 | PASS | 7a: over the rear plate |
| K-016 | console-cap | outline 693;141.5 | 1 | rrect 693.000 x 141.500 | PASS | 7a: over the cheeks (690 + 2 x 1.5) and from the face plate's front to the rear plate's back (1.5 + 138.5 + 1.5) |
| K-016b | console-cap | holes 6.5;z | 10 | 10 | PASS | 7a Console: 4 on each end rail, 1 on each side rail |
| K-017 | console-cheek-left | thickness | 1.5 | 1.5 | PASS | 7a |
| K-018 | console-cheek-left | normal | 1,0,0 | (1.0, 0.0, 0.0) | PASS | 7a: side plate |
| K-019 | console-cheek-left | loops rrect | 1 | 1 | PASS | 7a: a rectangle with 6 mm corners, no cuts but its holes |
| K-020 | console-cheek-left | outline 141.5;201.5 | 1 | rrect 141.500 x 201.500 | PASS | 7a: from the face plate's front (610) to the rear plate's back (751.5), from the top of the body (1000) to the top of the frame (1201.5) |
| K-021 | console-cheek-right | outline 141.5;201.5 | 1 | rrect 141.500 x 201.500 | PASS | 7a (see K-020) |
| K-022 | console-cheek-right | min x | 345 | 345.0 | PASS | 7a: continuing the side panel |
| K-023 | console-cheek-right | holes 6.5;x | 5 | 5 | PASS | 7a Console: 2 per post, 1 on the side rail |
| K-024 | console-rear | thickness | 1.5 | 1.5 | PASS | 7a |
| K-025 | console-rear | min y | 750 | 750.0 | PASS | 7a: continuing the rear panel |
| K-026 | console-rear | outline 690;201.5 | 1 | rrect 690.000 x 201.500 | PASS | 7a: from the top panel's back edge (1000) to the top of the frame |
| K-027 | console-rear | holes 6.5;y | 8 | 8 | PASS | 7a Console: 2 per rear post, 4 on the rear rail |
| D-001 | door-ring | thickness | 2 | 2.0 | PASS | 7a Door 2 mm |
| D-002 | door-ring | loop circle;0;631.5;560;560 | 1 | 1 | PASS | 7a Door ring 560 outside on the drum axis |
| D-003 | door-ring | loop circle;0;631.5;470;470 | 1 | 1 | PASS | 7a Door ring 470 inside |
| D-004 | door-ring | max y | -1.5 | -1.5 | PASS | 7a: on the front panel |
| D-004b | door-ring | holes 4.5;y | 8 | 8 | PASS | 7a Door: 8 M4 bolts on radius 257.5 |
| D-004c | door-ring | holes 6.5;y | 2 | 2 | PASS | 7a Door: the fixed hinge leaf, 2 x M6 countersunk at X -266 and -252, 50 below the axis |
| D-004d | door-ring | hole_at 6.5;-266;581.5 | 1 | (-266.000, 581.500) d 6.500 | PASS | 7a Door hinge |
| D-005 | door-disc | thickness | 2 | 1.9999999999999982 | PASS | 7a Door 2 mm |
| D-006 | door-disc | loop circle;0;631.5;540;540 | 1 | 1 | PASS | 7a Door disc 540 |
| D-007 | door-disc | loops circle | 5 | 5 | PASS | 7a: a plain disc on the first build, no window; 2 handle holes and 2 hinge screw holes, all M4 |
| D-007b | door-disc | hole_at 4.5;220;567.5 | 1 | (220.000, 567.500) d 4.500 | PASS | 7a Door: handle on 128 centres at X 220 |
| D-007c | door-disc | hole_at 4.5;220;695.5 | 1 | (220.000, 695.500) d 4.500 | PASS | 7a Door handle |
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
| R-012 | drum-ring-front | cyl 270;y;0,631.5 | 1 | 1 | PASS | 7b: ring 540 inside (draft 6: room for the curved lint slot inside the bore) |
| R-013 | drum-ring-front | thickness | 2 | 2.0 | PASS | 7b: 2 mm rings |
| R-014 | drum-ring-front | min y | 50 | 50.0 | PASS | 7b: front ring at the sheet's front edge |
| R-015 | drum-ring-front | holes 4.5;y | 30 | 30 | PASS | 7b: 30 tab holes |
| R-016 | drum-ring-front | loop circle;0;631.5;618.4;618.4 | 1 | 1 | PASS | 7b ring outside |
| R-017 | drum-ring-front | loop circle;0;631.5;540;540 | 1 | 1 | PASS | 7b ring inside |
| R-018 | drum-ring-rear | max y | 600 | 600.0 | PASS | 7b: rear ring at the sheet's rear edge |
| R-019 | drum-ring-rear | holes 4.5;y | 30 | 30 | PASS | 7b |
| R-020 | drum-ring-rear | cyl 270;y;0,631.5 | 1 | 1 | PASS | 7b |
| R-021 | drum-splice | size y | 544 | 544.0000001999999 | PASS | 7b Splice 60 x 544 |
| R-022 | drum-splice | min y | 53 | 52.9999999 | PASS | 7b: between the rings, 1 mm off each |
| R-023 | drum-splice | holes 4.5;radial | 16 | 16 | PASS | 7b: holes matching the seam holes |
| R-024 | drum-splice | cyl 309.2;y;0,631.5 | 1 | 1 | PASS | 7b: inside the sheet |
| R-025 | drum-splice | cyl 308.2;y;0,631.5 | 1 | 1 | PASS | 7b: 1 mm strip |
| R-026 | dxf | dxf_outline drum-sheet;1945.274;582 |  | rpoly 1945.274 x 582.000 | PASS | 7b: 1945.3 x 550 plus 16 mm tabs on both long edges (draft 6) |
| R-027 | dxf | dxf_circles_d drum-sheet;4.5 | 76 | 76 | PASS | 7b: 60 tab holes + 16 seam holes |
| R-028 | dxf | dxf_circles_d drum-sheet;6.5 | 12 | 12 | PASS | 7b: baffle holes |
| R-029 | dxf | dxf_circle_at drum-sheet;4.5;15;55 | 1 | 1 | PASS | 7b: seam hole 15 in from the edge, first one 55 from the front (roller track 45 + 10) |
| R-030 | dxf | dxf_circle_at drum-sheet;4.5;1930.274;455 | 1 | 1 | PASS | 7b: seam hole on the other edge, last one before the rear roller track |
| R-031 | dxf | dxf_circle_at drum-sheet;6.5;324.212;105 | 1 | 1 | PASS | 7b: first baffle hole; column at a sixth of the width, 170 before the middle |
| R-032 | dxf | dxf_circle_at drum-sheet;4.5;32.421;-8 | 1 | 1 | PASS | 7b: first tab hole, tab centred half a pitch from the seam, hole 8 out on the 16 tab |
| R-033 | dxf | dxf_outline drum-ring;618.4;618.4 |  | circle 618.400 x 618.400 | PASS | 7b Rings 618.4 outside |
| R-034 | dxf | dxf_circles_d drum-ring;540 | 1 | 1 | PASS | 7b Rings 540 inside (draft 6) |
| R-035 | dxf | dxf_circles_d drum-ring;4.5 | 30 | 30 | PASS | 7b: 30 holes |
| R-036 | dxf | dxf_circle_at drum-ring;4.5;-31.484;299.55 | 1 | 1 | PASS | 7b: tab hole on radius 301.2 (309.2 - 8) at 6 degrees from the top (first tab centre) |
| R-037 | dxf | dxf_outline drum-splice;60;544 |  | rrect 60.000 x 544.000 | PASS | 7b Splice 60 x 544 |
| R-038 | dxf | dxf_circles_d drum-splice;4.5 | 16 | 16 | PASS | 7b |
| R-039 | dxf | dxf_circle_at drum-splice;4.5;15;52 | 1 | 1 | PASS | 7b: splice hole under the first seam hole (55 - 2 ring - 1) |
| R-040 | dxf | dxf_outline felt-seal-long;582;478.927 |  | sector 582.000 x 478.927 | PASS | 7b Seals (draft 7): the long felt arc, 130.225 degrees each side of straight down between radii 273 and 291 (the 45 degree glides take 4.775 degrees each side): 582 wide, 291 + 291 cos 49.775 tall |
| R-041 | dxf | dxf_loops felt-seal-long;sector | 1 | 1 | PASS | 7b Seals (draft 7): one annular sector |
| R-041b | dxf | dxf_outline felt-seal-short;375.853;82.562 |  | sector 375.853 x 82.562 | PASS | 7b Seals (draft 7): the short felt arc over the top, 40.225 degrees each side: 2 x 291 sin 40.225 wide, 291 - 273 cos 40.225 tall |
| R-041c | dxf | dxf_loops felt-seal-short;sector | 1 | 1 | PASS | 7b Seals (draft 7) |
| R-041d | cut-list | cut felt-seal-long | 1282 | 1282.0 | PASS | 7b Seals (draft 7): strip length on the glide radius 282: 2 x 2.2729 x 282 |
| R-041e | cut-list | cut felt-seal-short | 396 | 396.0 | PASS | 7b Seals (draft 7): 2 x 0.7021 x 282 |
| M-001 | motor (bought) | size y | 208.5 | 208.5 | PASS | bom: NEMA 48 frame envelope 200 long (V-106) plus the 4.5 mm front shaft to the blower (draft 9: the housing stands 1.5 further back on the blower plate) and the 4 mm rear shaft to the pulley |
| M-002 | motor (bought) | min y | 185.5 | 185.5 | PASS | 7a: motor behind the blower (frame from 190, shaft stub to the blower's back face at 185.5, draft 9) |
| M-003 | motor (bought) | cyl 70;y;0,120 | 1 | 1 | PASS | 7a Drive: axis at 120 high, 140 envelope |
| M-004 | pulley (bought) | cyl 10;y;0,120 | 5 | 5 | PASS | 7a Drive (draft 7): PJ pulley, 20 pitch diameter: 1725 x 20 / 620 = 56 drum rpm (V-012); five rib bands between four grooves |
| M-004b | pulley (bought) | cyl 11;y;0,120 | 1 | 1 | PASS | 7a Drive (draft 7): the pulley's hub, 22 |
| M-003b | motor (bought) | cyl 6.35;y;0,120 | 2 | 2 | PASS | bom (draft 7): 1/2 in shafts both ends (V-106) |
| M-005 | pulley (bought) | min y | 394 | 394.0 | PASS | 7a Drive: pulley centred at Y 402, 16 wide |
| M-006 | blower (bought) | cyl 110;y;0,120 | 1 | 1 | PASS | 7a Blower envelope 220 on the motor axis |
| M-007 | blower (bought) | min y | 85.5 | 85.5 | PASS | 7a Blower on the front shaft; its inlet face on the back of the 1.5 blower plate at 84 (draft 9) |
| M-008 | exhaust-duct (bought, 4 in aluminium pipe, 102 x 1, cut to length, one 6.5 hole for the tap) | cyl 51;y;230,150 | 1 | 1 | PASS | 7a Air: 102 exhaust along the bay floor at X 230, 150 high (draft 9: a catalog 4 in pipe, 1 mm wall) |
| M-008b | exhaust-duct (bought, 4 in aluminium pipe, 102 x 1, cut to length, one 6.5 hole for the tap) | cyl 50;y;230,150 | 1 | 1 | PASS | 7a Air (draft 9): the pipe's 100 bore |
| M-009 | exhaust-duct (bought, 4 in aluminium pipe, 102 x 1, cut to length, one 6.5 hole for the tap) | max y | 801.5 | 801.5000001 | PASS | 7a Air (draft 9): through the rear lower panel's port, 50 proud of its outer face (751.5) as the vent hose spigot |
| M-009b | exhaust-duct (bought, 4 in aluminium pipe, 102 x 1, cut to length, one 6.5 hole for the tap) | min y | 192 | 191.9999999 | PASS | 7a Air (draft 9): over the housing's 25 long collar from 2 past the outlet box's rear face (190), along the bay floor to the port |
| M-010 | heat-module-tray | min y | 420 | 420.0 | PASS | 7a Air: tray Y 420 to 670 |
| M-011 | heat-module-tray | max y | 700 | 700.0 | PASS | 7a Air (draft 7): tray Y 420 to 700, starting 3 behind the idler spring |
| M-012 | heat-module-tray | size x | 340 | 340.0 | PASS | 7a (draft 7): tray 340 wide, centred, out to the tray rails' outer faces |
| M-013 | heat-module-tray | min z | 60 | 60.0 | PASS | 7a: on the 2020 tray rails (40 + 20) |
| M-014 | hood-bottom | size x | 350 | 350.0 | PASS | 7a Air (draft 8): the hood's plates are 350 wide over 25 x 8 bars, 334 between the bars |
| M-015 | hood-bottom | size y | 257.5 | 257.5 | PASS | 7a Air (draft 8): hood from Y 448 to the trunk's back at 705.5 |
| M-016 | hood-bottom | min y | 448 | 448.0 | PASS | 7a Air (draft 7): the hood starts over the collar's gasket ring (450..600) with 2 to spare |
| M-016b | hood-bottom | min z | 230 | 230.0 | PASS | 7a Air: hood bottom at 230, above the module's collar (227) and its 3 mm gasket, so the module leaves by the back under it |
| M-016c | hood-top | max z | 258 | 258.0 | PASS | 7a Air (draft 8): hood top plate's top at 258, 2 under the mid rear cross rail |
| M-016d | trunk-front | min y | 652.5 | 652.5 | PASS | 7a Air (draft 8): the trunk's front plate 1 behind the mid rear cross rail's back face (651.5) |
| M-016e | trunk-rear | max y | 705.5 | 705.5 | PASS | 7a Air (draft 8): the trunk's back plate 4.5 in front of the rear rail (710) |
| M-016f | trunk-front | size x | 260 | 260.0 | PASS | 7a Air (draft 8): trunk plates 260 wide over 50 x 8 bars, 244 between them |
| M-016g | trunk-front | max z | 831.5 | 831.5 | PASS | 7a Air (draft 8): the trunk ends 20 over the hole field (811.5), its top bar above the nozzle |
| M-016h | trunk-front | loop rect;0;737.5;212;142 | 1 | 1 | PASS | 7a Air (draft 8): the nozzle's opening in the trunk's front plate, 212 x 142 round the 200 x 130 hole field |
| M-017 | lint-box-front | size x | 332 | 332.0 | PASS | 7a Air (draft 8): lint box 332 wide between the front stubs, hung on them through 4 mm spacers |
| M-018 | lint-box-front | min y | 7 | 7.0 | PASS | 7a Air (draft 8): the front plate 2.5 behind the ring bolts' tips (4.5), 7 off the front panel's back |
| M-019 | lint-box-back | max y | 40 | 40.0 | PASS | 7a Air (draft 8): the lower back plate on the bulkhead's front face; above 265 the bulkhead is the box's back |
| M-020 | lint-box-front | max z | 462.066 | 462.06611909066066 | PASS | 7a Air (draft 8): the front plate's top follows the liner on radius 237.2: 631.5 - sqrt(237.2^2 - 166^2) at its corners |
| M-020b | lint-box-back | loop rect;0;130;140;120 | 1 | 1 | PASS | 7a Air (draft 8): the opening into the spool, 140 x 120 round the blower's 130 mouth |
| M-020c | liner | size x | 474 | 474.0000002 | PASS | 7a Door (draft 8): throat liner 237 outside, inside the ring's 235 edge |
| M-020d | liner | min y | -1.5 | -1.5000001 | PASS | 7a Door (draft 8): the liner starts on the ring's back face |
| M-020e | liner | max y | 39.8 | 39.8000001 | PASS | 7a Door (draft 8): the liner ends 0.2 short of the bulkhead |
| M-020f | basket-lip-plate | min y | 41.5 | 41.5 | PASS | 7 Lint management (draft 8): the lip plate on the bulkhead's drum side |
| M-020g | basket-far-plate | min y | 9 | 9.0 | PASS | 7 Lint management (draft 8): the far plate 2 behind the box's front plate |
| M-020h | basket-far-plate | size y | 3 | 3.0 | PASS | 7 Lint management (draft 8): 3 mm plates, tapped M3 |
| M-020i | lint-box-front | cyl 237.2;y;0,631.5 | 1 | 1 | PASS | 7a Air (draft 8): the plate's top edge is an arc 0.2 outside the liner |
| M-020j | liner | cyl 235.5;y;0,631.5 | 1 | 1 | PASS | 7a Door (draft 8): liner inside radius 235.5 |
| M-020k | basket-far-plate | loop sector;0;401.381;309.107;70.762 | 1 | 1 | PASS | 7 Lint management (draft 8): the basket's sector plates between radii 239.5 and 265.5, 35.6 degrees each side of straight down |
| M-025 | roller-front-1 (bought) | cyl 30;y;-180.173,343.164 | 1 | 1 | PASS | 7b Rollers (draft 7): 60 diameter at 32 degrees below the axis on radius 340 |
| M-026 | roller-front-1 (bought) | min y | 50 | 50.0 | PASS | 7b: running over the ring, flush with the drum end |
| M-027 | roller-front-1 (bought) | size y | 25 | 25.0 | PASS | bom: catalog roller 25 wide (V-106) |
| M-028 | roller-rear-2 (bought) | cyl 30;y;180.173,343.164 | 1 | 1 | PASS | 7b Rollers (draft 7) |
| M-029 | roller-rear-2 (bought) | max y | 601.5 | 601.5 | PASS | 7b (draft 7): over the rear ring and 1.5 proud of the drum's rear end (600), so one 35 shoulder serves both ends |
| M-029b | roller-front-1 (bought) | cyl 5.25;y;-180.173,343.164 | 1 | 1 | PASS | 7b (draft 7): 10.5 bore on the 10 shoulder (V-106) |
| M-030 | baffle-1 (angle, cut to length) | size y | 480 | 480.0 | PASS | 7b Baffles 480 long |
| M-031 | baffle-2 (angle, cut to length) | size y | 480 | 480.0 | PASS | 7b |
| M-032 | baffle-3 (angle, cut to length) | size y | 480 | 480.0 | PASS | 7b |
| M-033 | baffle-1 (angle, cut to length) | holes 6.5;radial | 4 | 4 | PASS | 7b: four bolts per baffle |
| X-001 | clearance | clearance drum-sheet;bay-ceiling | 20 | 20.0 | PASS | 7a: 20 mm under the drum (bay top 300 + 1.5 plate) |
| X-002 | clearance | clearance drum-sheet;rail-top-front | 21.754 | 21.754 | PASS | 7a: drum top 941.5 is 18.5 under the top rails (960); the nearest rail corner is the top front rail's rear bottom edge at Y 40, rounded R2 (draft 5): sqrt(12^2 + 20.5^2) - 2 |
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
| X-016 | clearance | clearance lint-box-bars (30 x 8 aluminium flat bar: 2 sides mitred at the top, 1 bottom);rail-mid-front-left | 4 | 4.0 | PASS | 7a (draft 8): 4 mm spacers between the box's side bars and the stubs |
| X-017 | clearance | clearance lint-box-bars (30 x 8 aluminium flat bar: 2 sides mitred at the top, 1 bottom);rail-mid-front-right | 4 | 4.0 | PASS | 7a (draft 8) |
| X-018 | clearance | clearance lint-box-bars (30 x 8 aluminium flat bar: 2 sides mitred at the top, 1 bottom);front-bulkhead | 1.5 | 1.5 | PASS | 7a (draft 8): 1.5 of compressed foam between the side bars and the bulkhead |
| X-019 | clearance | clearance trunk-front;bay-ceiling | 2 | 2.0 | PASS | 7a: 2 mm all round in the ceiling cut |
| X-020 | clearance | clearance trunk-rear;rail-mid-rear | 4.5 | 4.5 | PASS | 7a (draft 8): the trunk ends at 705.5, the rear rail starts at 710 |
| X-021 | clearance | clearance heat-module-element (bought, 279838 class open-coil element on its frame, envelope);heat-module-tray | 20 | 20.0 | PASS | 7a Heat module (draft 7): the element sits on the rails' top legs at 81.5, the tray's top at 61.5 |
| X-022 | clearance | clearance motor (bought);base-pan | 50 | 50.0 | PASS | 7a: motor axis 120 high |
| X-023 | clearance | clearance blower (bought);spool-bars (40 x 8 aluminium flat bar: 2 x 136, 2 x 140) | 5.5 | 5.5 | PASS | 7a (draft 9): the spool's bars end 4 in front of the blower plate (6 mm foam compressed to 4 fills it) and the plate is 1.5 in front of the housing's inlet face |
| X-024 | clearance | clearance exhaust-duct (bought, 4 in aluminium pipe, 102 x 1, cut to length, one 6.5 hole for the tap);rear-lower-panel | 2 | 2.0 | PASS | 7a: duct through the port with 2 mm |
| X-025 | clearance | clearance power-module-plate;trunk-front | 20 | 20.0 | PASS | 7a Power module (draft 8): the plate's right edge at X -150, the trunk's front plate from X -130 |
| X-026 | clearance | clearance drum-sheet;top-panel | 58.5 | 58.5 | PASS | 7a: drum top 941.5, top panel at 1000 |
| X-027 | clearance | clearance hood-top;rail-mid-rearcross | 2 | 2.0 | PASS | 7a Air (draft 8): the hood's top plate (258) passes under the mid rear cross rail (260) |
| X-028 | clearance | clearance hood-bottom;heat-module-collar (bought, 125 flanged starting collar, cut to 55.5) | 3.354 | 3.354 | PASS | 7a Air (draft 8): hood bottom at 230 over the collar's rim (227) with the 128 hole round the 125 collar: sqrt(3^2 + 1.5^2); the foam ring fills the 3 |
| X-029 | clearance | clearance felt-seal-front-long;drum-ring-front | 0.5 | 0.5 | PASS | 7b Seals: front felt from 41.5 to 49.5 on the front bulkhead, ring face at 50 |
| X-029b | clearance | clearance felt-seal-rear-long;drum-ring-rear | 0 | 0.0 | PASS | 7b Seals (draft 7): rear felt 10 thick from 600 to 610, on the ring face |
| X-029c | clearance | clearance drum-glides-front (bought, 2 x nylon drum glide pads, 45 x 20 x 8);drum-ring-front | 0.5 | 0.5 | PASS | 7b Seals (draft 7): front glides 8 thick on the bulkhead's back (41.5..49.5), ring face at 50 |
| X-029d | clearance | clearance drum-glides-rear (bought, 2 x nylon drum glide pads, 45 x 20 x 9.5);drum-ring-rear | 0.5 | 0.5 | PASS | 7b Seals (draft 7): rear glides 9.5 thick (600.5..610), ring face at 600: the drum floats 1 mm between the glides |
| X-030 | clearance | clearance lint-box-front;hardware-door-ring (bought, 8 x M4 x 8 button head, nuts) | 2.5 | 2.5 | PASS | 7a (draft 8): M4 x 8 ring bolts end at 4.5, the box's front plate starts at 7 |
| X-031 | clearance | clearance console-post-1;top-panel | 0 | 0.0 | PASS | 7a Console: posts on the top panel |
| X-032 | clearance | clearance power-cord (bought);feet (bought, 4 x M8 leveling feet, 50 pad) | 20.5 | 20.5 | PASS | 7a Panels (draft 7): the cord runs at X -275 (radius 4.5), the rear left foot pad (radius 25) at X -325 |
| X-033 | clearance | clearance power-cord (bought);base-pan | 6 | 6.0 | PASS | 7a (draft 6): cord centre line 10.5 under the pan's bottom, 4.5 radius |
| H-001 | feet (bought, 4 x M8 leveling feet, 50 pad) | min z | -19.5 | -19.5 | PASS | 7c Feet (draft 6): pad 10 and hex 8 under the pan |
| H-002 | feet (bought, 4 x M8 leveling feet, 50 pad) | size x | 700 | 700.0000001000001 | PASS | 7c Feet: 50 pads on the post centres at X +-325 |
| H-003 | belt (bought, PJ 5 rib) | size y | 12 | 12.0 | PASS | 7a Drive: PJ 5 ribs, 12 wide, centred on the pulley at Y 402 |
| H-004 | belt (bought, PJ 5 rib) | min y | 396 | 396.0 | PASS | 7a Drive |
| H-005 | belt (bought, PJ 5 rib) | max z | 945 | 945.0 | PASS | 7a Drive: round the drum outside (941.5 + 3.5 belt) |
| H-006 | belt (bought, PJ 5 rib) | min z | 106.5 | 106.5 | PASS | 7a Drive (draft 7): under the 20 pulley at 120: 120 - 10 - 3.5 |
| H-007 | idler-pulley (bought, flat idler 40 with bearing) | cyl 20;y;-60,165 | 1 | 1 | PASS | 7a Drive: flat idler 40 at (-60, 165), on the slack run |
| H-008 | clearance | clearance belt (bought, PJ 5 rib);drum-sheet | 0 | 0.0 | PASS | 7a Drive: belt on the drum |
| H-009 | clearance | clearance belt (bought, PJ 5 rib);pulley (bought) | 0 | 0.0 | PASS | 7a Drive: belt on the pulley |
| H-010 | clearance | clearance belt (bought, PJ 5 rib);idler-pulley (bought, flat idler 40 with bearing) | 0 | 0.0 | PASS | 7a Drive: belt on the idler |
| H-011 | clearance | clearance belt (bought, PJ 5 rib);motor (bought) | 4.162 | 4.162 | PASS | 7a Drive (draft 7): belt plane 396..408 behind the motor frame (to 390); nearest is the rear shaft stub's end (radius 6.35, to 394) under the belt's inner face on the 20 pulley: sqrt(2^2 + 3.65^2) |
| H-012 | clearance | clearance belt (bought, PJ 5 rib);heat-module-tray | 46.573 | 46.573 | PASS | 7a Air (draft 7): tray plate (Z 60 to 61.5) from Y 420, belt to 408 and down to 106.5: sqrt(12^2 + 45^2) |
| H-013 | door-hinge-1-fixed (bought, flag hinge, pinned half) | cyl 4;z;-278.5,-14 | 2 | 2 | PASS | 7a Door: 8 pin at X -278.5, Y -14, outside the 540 disc; two lengths of pin surface, below and above the fixed knuckle |
| H-014 | door-hinge-1-fixed (bought, flag hinge, pinned half) | cyl 9;z;-278.5,-14 | 1 | 1 | PASS | 7a Door: 18 knuckle |
| H-015 | clearance | clearance door-hinge-1-fixed (bought, flag hinge, pinned half);door-disc | 1.775 | 1.775 | PASS | 7a Door: knuckle face at X -269.5, disc edge at 35 below the axis at sqrt(270^2 - 35^2) = 267.725 |
| H-016 | clearance | clearance door-hinge-2-swing (bought, flag hinge, lift-off half);door-ring | 1.523 | 1.523 | PASS | 7a Door: swinging knuckle 1.5 off the ring face plane, and just outside the ring's 280 edge, so the nearest point is on that edge |
| H-017 | clearance | clearance door-seal (bought, OEM door seal);door-ring | 2 | 2.0 | PASS | 7a Door: 6 seal on the disc, 2 off the ring face when closed (compressed on the real door) |
| H-018 | door-handle (bought, D handle 128 centres) | min y | -57 | -57.0000001 | PASS | 7a Door: handle 128 centres |
| H-019 | door-handle (bought, D handle 128 centres) | cyl 7;y;220,567.5 | 1 | 1 | PASS | 7a Door: handle standoff |
| H-020 | felt-seal-rear-long | thickness | 10 | 10.0 | PASS | 7b Seals (draft 7): 10 mm felt at the rear, where the ring face is 10 off the bulkhead |
| H-021 | felt-seal-rear-long | loops sector | 1 | 1 | PASS | 7b Seals (draft 7): the felt is two arcs with the glides in the gaps; this is the long one round the bottom |
| H-022 | felt-seal-rear-long | size x | 582 | 582.0 | PASS | 7b Seals: to radius 291, inboard of the 16 tall tabs (293.2) |
| H-023 | felt-seal-rear-long | min y | 600 | 600.0 | PASS | 7b Seals (draft 7): felt from 600 to 610, on the ring's back face |
| H-023b | felt-seal-front-long | thickness | 8 | 7.999999999999993 | PASS | 7b Seals: 10 mm felt drawn compressed to the front gap of 8.5 (0.5 to the ring face) |
| H-023c | felt-seal-front-short | loops sector | 1 | 1 | PASS | 7b Seals (draft 7) |
| H-023d | felt-seal-front-long | max y | 49.5 | 49.5 | PASS | 7b Seals: on the front bulkhead's back (41.5), ring face at 50 |
| H-024 | tier0-faceplate | thickness | 2 | 2.0 | PASS | tier0 README: 2 mm aluminum |
| H-025 | tier0-faceplate | outline 620;160 | 1 | rrect 620.000 x 160.000 | PASS | tier0 README: 620 x 160 (UCI-D draft 6) |
| H-026 | tier0-faceplate | holes 4.5 | 10 | 10 | PASS | tier0_drawings: 6 mounting, 2 DIN rail standoffs, 2 cable ties |
| H-027 | tier0-faceplate | holes 12 | 2 | 2 | PASS | tier0_drawings: two timer shaft holes |
| H-028 | tier0-faceplate | holes 4 | 4 | 4 | PASS | tier0_drawings: four yoke holes at 83.3 |
| H-029 | tier0-faceplate | holes 22.3 | 2 | 2 | PASS | tier0_drawings: two 22 mm devices |
| H-030 | tier0-faceplate | hole_at 12;-150;1084.5 | 1 | (-150.000, 1084.500) d 12.000 | PASS | tier0_drawings (faceplate draft 3): DRY TIME shaft at X -150 on the faceplate's centre line, the aperture centre (1084.5) |
| H-031 | tier0-faceplate | hole_at 22.3;130;1104.5 | 1 | (130.000, 1104.500) d 22.300 | PASS | tier0_drawings (faceplate draft 3): START at X 130, 20 above the centre line so K1 fits below the 22 mm devices |
| H-031b | tier0-faceplate | hole_at 4.5;50;1060.5 | 1 | (50.000, 1060.500) d 4.500 | PASS | tier0_drawings (faceplate draft 3): K1 rail standoff at X 50, 24 below the centre line; the socket hangs 36 below it, to the aperture's edge |
| H-032 | clearance | clearance tier0-faceplate;console-face | 0 | 0.0 | PASS | uci-spec 4.1: faceplate on the chassis panel |
| H-034 | clearance | clearance feet (bought, 4 x M8 leveling feet, 50 pad);base-pan | 0 | 0.0 | PASS | 7c Feet: hex against the pan |
| H-035 | clearance | clearance hardware-drum-tabs (bought, 60 x M4 x 8 button head, nuts);front-bulkhead | 2.5 | 2.5 | PASS | 7b: bolt tips at 44, bulkhead back face at 41.5 |
| H-036 | clearance | clearance idler-pulley (bought, flat idler 40 with bearing);motor (bought) | 4.5 | 4.5 | PASS | 7a Drive: idler flange at 394.5, motor end bell to 390 |
| H-038 | cut-list | cut idler-arm | 175.4 | 175.4 | PASS | 7a Drive: pivot (-115, 25) to idler (-60, 165) is 150.4 plus 12.5 past each hole |
| H-039 | cut-list | cut_qty idler-bracket, spring-bracket | 2 | 2 | PASS | 7a Drive |
| G-001 | drum-glides-front (bought, 2 x nylon drum glide pads, 45 x 20 x 8) | solids | 2 | 2 | PASS | 7b Seals (draft 7): two pads per bulkhead |
| G-002 | drum-glides-front (bought, 2 x nylon drum glide pads, 45 x 20 x 8) | min y | 41.5 | 41.5 | PASS | 7b Seals (draft 7): on the front bulkhead's back face |
| G-003 | drum-glides-front (bought, 2 x nylon drum glide pads, 45 x 20 x 8) | max y | 49.5 | 49.5 | PASS | 7b Seals (draft 7): 8 thick |
| G-004 | drum-glides-rear (bought, 2 x nylon drum glide pads, 45 x 20 x 9.5) | min y | 600.5 | 600.5 | PASS | 7b Seals (draft 7): 9.5 thick, 0.5 off the rear ring face |
| G-005 | drum-glides-rear (bought, 2 x nylon drum glide pads, 45 x 20 x 9.5) | max y | 610 | 610.0 | PASS | 7b Seals (draft 7): on the rear bulkhead's front face |
| G-007 | hardware-drum-glides (bought, 4 x M4 x 8 and 4 x M4 x 10 button head, nuts) | solids | 16 | 16 | PASS | 7b Seals (draft 7): a bolt and a nut at each of 16 holes |
| G-008 | hardware-roller-studs (bought, 4 x ISO 7379 shoulder screws 10 x 35 M8, 1.0 shims, spacers 16 x 10.5 x 8.5, M8 washers and nuts) | solids | 20 | 20 | PASS | 7b Rollers (draft 7): per roller a shoulder screw, a shim, a spacer, a washer and a nut |
| G-009 | hardware-roller-studs (bought, 4 x ISO 7379 shoulder screws 10 x 35 M8, 1.0 shims, spacers 16 x 10.5 x 8.5, M8 washers and nuts) | cyl 5;y;-180.173,343.164 | 2 | 2 | PASS | 7b Rollers (draft 7): the 10 shoulders of the two left studs |
| G-010 | hardware-roller-studs (bought, 4 x ISO 7379 shoulder screws 10 x 35 M8, 1.0 shims, spacers 16 x 10.5 x 8.5, M8 washers and nuts) | cyl 8;y;180.173,343.164 | 8 | 8 | PASS | 7b Rollers (draft 7): the two right studs' heads, shims, spacers and washers, all 16 outside |
| G-011 | clearance | clearance hardware-roller-studs (bought, 4 x ISO 7379 shoulder screws 10 x 35 M8, 1.0 shims, spacers 16 x 10.5 x 8.5, M8 washers and nuts);lint-box-bars (30 x 8 aluminium flat bar: 2 sides mitred at the top, 1 bottom) | 6.173 | 6.173 | PASS | 7b Rollers (draft 8): the front nuts' washers (radius 8) at X 180.173 beside the box's side bars at 166, overlapping them in Y |
| G-012 | clearance | clearance hardware-roller-studs (bought, 4 x ISO 7379 shoulder screws 10 x 35 M8, 1.0 shims, spacers 16 x 10.5 x 8.5, M8 washers and nuts);drum-sheet | 22 | 22.0 | PASS | 7b Rollers (draft 7): the heads (radius 8) on radius 340, the sheet at 310 |
| G-013 | clearance | clearance hardware-roller-studs (bought, 4 x ISO 7379 shoulder screws 10 x 35 M8, 1.0 shims, spacers 16 x 10.5 x 8.5, M8 washers and nuts);roller-front-1 (bought) | 0 | 0.0 | PASS | 7b Rollers (draft 7): the shim and the spacer touch the roller's faces; the shoulder has 0.25 in the bore |
| G-014 | grommets (bought, 5 x rubber grommets for 1.5 panels: 22 mm hole x 2, 30 mm hole x 1, 16 mm hole x 2) | solids | 5 | 5 | PASS | 7a Panels (draft 8): cord, bay harness and door switch cable grommets in the bay ceiling, console harness grommet in the top panel, door switch cable grommet in the front bulkhead |
| G-015 | clearance | clearance power-cord (bought);bay-ceiling | 6.5 | 6.5 | PASS | 7a (draft 7): the 9 cord up the middle of the 22 grommet hole |
| G-016 | clearance | clearance power-cord (bought);grommets (bought, 5 x rubber grommets for 1.5 panels: 22 mm hole x 2, 30 mm hole x 1, 16 mm hole x 2) | 3 | 3.0 | PASS | 7a (draft 7): the grommet's 15 bore round the 9 cord |
| G-017 | power-cord (bought) | max z | 320 | 320.0 | PASS | 7a Power module (draft 7): the cord ends under X1 (rail A1 at 360, blocks 47 tall) after its grommet |
| G-018 | clearance | clearance power-cord (bought);power-module-rail-A1-devices (bought, envelopes: X1 cord: 4 x UK 6 N (L1, L2, N, PE), CB1: 1P MCB, F1: UK 5-HESI fuse terminal, 2 end clamps) | 16.5 | 16.5 | PASS | 7a Power module (draft 7): the cord's end at 320 under X1's bottom at 336.5 |
| E-001 | heat-module-tray | holes 4.5;z | 13 | 13 | PASS | 7a Heat module (draft 7): 4 into the tray rails' slots (which also hold the box's side angles), 3 each for the two inside bottom angles and the terminal plate's foot |
| E-002 | heat-module-tray | hole_at 4.5;160;470 | 1 | (160.000, 470.000) d 4.500 | PASS | 7a (draft 7): on the right tray rail's slot centre line |
| E-003 | heat-module-tray | hole_at 6.6;140;680 | 1 | (140.000, 680.000) d 6.600 | PASS | 3.1 rule 7 (draft 7): bonding stud, M6 with two nuts |
| E-004 | heat-module-tray | loops circle | 14 | 14 | PASS | 7a (draft 7): 13 M4 and the bonding stud |
| E-005 | heat-module-wall-left | thickness | 1.5 | 1.5 | PASS | 7a (draft 7): the box is the same 1.5 sheet as the panels, one stock to order |
| E-006 | heat-module-wall-left | min x | -145 | -145.0 | PASS | 7a (draft 7): box 290 wide outside |
| E-007 | heat-module-wall-left | min y | 422 | 422.0 | PASS | 7a (draft 7): box from Y 422 (2 behind the tray's front edge, 5 behind the idler spring) to 627 |
| E-008 | heat-module-wall-left | size y | 205 | 205.0 | PASS | 7a (draft 7): 205 long: the 190 element and 6 each side plus the end walls |
| E-009 | heat-module-wall-left | size z | 108.5 | 108.5 | PASS | 7a (draft 7): walls from the tray's top (61.5) to under the lid (170) |
| E-010 | heat-module-wall-left | loop rect;525;114;150;60 | 1 | 1 | PASS | 7a Air (draft 7): inlet opening 150 x 60 = 9000 mm2 in the left end, above the bottom angle's leg and below the lid angle's, between the corner angles |
| E-011 | heat-module-wall-left | holes 4.5;x | 6 | 6 | PASS | 7a (draft 7): 2 for the bottom angle (and the element rail behind it), 2 for the lid angle, 2 for the corner angles |
| E-012 | heat-module-wall-right | loop rect;525;107;40;25 | 1 | 1 | PASS | 7a (draft 7): the element's terminals leave through the right end; final position from the element bought (V-108) |
| E-013 | heat-module-wall-right | max x | 145 | 145.0 | PASS | 7a (draft 7) |
| E-014 | heat-module-wall-front | min y | 422 | 422.0 | PASS | 7a (draft 7) |
| E-015 | heat-module-wall-front | size x | 287 | 287.0 | PASS | 7a (draft 7): the end walls sit between the side walls |
| E-016 | heat-module-wall-front | holes 4.5;y | 8 | 8 | PASS | 7a (draft 7): 3 for the inside bottom angle, 3 for the lid angle, 2 for the corner angles |
| E-017 | heat-module-wall-rear | max y | 627 | 627.0 | PASS | 7a (draft 7) |
| E-018 | heat-module-top | min z | 170 | 170.0 | PASS | 7a (draft 7): the lid on the walls' top edges, 110 above the tray's top |
| E-019 | heat-module-top | size x | 290 | 290.0 | PASS | 7a (draft 7) |
| E-020 | heat-module-top | size y | 205 | 205.0 | PASS | 7a (draft 7) |
| E-021 | heat-module-top | loop circle;0;525;126;126 | 1 | 1 | PASS | 7a Air (draft 7): the 125 collar's opening, centred on the box (X 0, Y 524.5 is the box's middle; 525 keeps the collar's 155 flange 4.5 off the rear lid angle) |
| E-022 | heat-module-top | holes 4.5;z | 18 | 18 | PASS | 7a (draft 7): 4 + 6 for the lid angles, 4 for the collar's flange, 4 for the two thermostats |
| E-023 | heat-module-top | hole_at 4.5;110;520 | 1 | (110.000, 520.000) d 4.500 | PASS | 7a (draft 7): thermostat bracket holes 40 apart along Y at X +-110, between the collar's flange and the lid's side angle |
| E-024 | heat-module-element (bought, 279838 class open-coil element on its frame, envelope) | size y | 190 | 190.0 | PASS | bom HE-ELEM (draft 7): 10.5 x 7.5 x 2 in from a seller listing (V-108) |
| E-025 | heat-module-element (bought, 279838 class open-coil element on its frame, envelope) | size z | 51 | 51.0 | PASS | bom HE-ELEM (draft 7) |
| E-026 | heat-module-element (bought, 279838 class open-coil element on its frame, envelope) | min x | -133.5 | -133.5 | PASS | 7a (draft 7): 267 long along X, centred, 10 inside each side wall |
| E-027 | heat-module-element (bought, 279838 class open-coil element on its frame, envelope) | min z | 81.5 | 81.5 | PASS | 7a (draft 7): on the two angle rails' top legs (61.5 + 20) |
| E-028 | heat-module-collar (bought, 125 flanged starting collar, cut to 55.5) | max z | 227 | 227.0 | PASS | 7a Air (draft 7): the collar's rim 3 under the hood; the module slides out under the hood (230) and the mid rear end rail (260) |
| E-029 | heat-module-collar (bought, 125 flanged starting collar, cut to 55.5) | cyl 62.5;z;0,525 | 1 | 1 | PASS | 7a Air (draft 7): 125 outside, 12272 mm2 of air inside the 0.6 wall |
| E-030 | heat-module-collar (bought, 125 flanged starting collar, cut to 55.5) | cyl 77.5;z;0,525 | 1 | 1 | PASS | 7a (draft 7): 155 flange on the lid, four M4 |
| E-031 | hood-gasket (bought, 3 mm foam ring 150 x 125, glued under the hood's bottom plate) | min z | 227 | 227.0 | PASS | 7a Air (draft 7): foam ring under the hood, 150 outside, 125 inside, 3 thick: the collar's rim brushes it |
| E-032 | hood-gasket (bought, 3 mm foam ring 150 x 125, glued under the hood's bottom plate) | cyl 75;z;0,525 | 1 | 1 | PASS | 7a Air (draft 7) |
| E-033 | heat-module-thermostats (bought, 279816 class high-limit and thermal cut-off, envelopes) | solids | 2 | 2 | PASS | 5.2 (draft 7): high-limit and thermal cut-off on the lid beside the collar |
| E-034 | heat-module-thermostats (bought, 279816 class high-limit and thermal cut-off, envelopes) | max z | 186.5 | 186.5 | PASS | 7a (draft 7): 2 bracket + 13 body on the lid (171.5) |
| E-035 | heat-module-terminal-plate | min y | 634 | 634.0 | PASS | 7a (draft 7): terminal plate 7 behind the box's rear wall (627), room for the lid angle's leg and the bolt heads on the plate's front |
| E-036 | heat-module-terminal-plate | size x | 290 | 290.0 | PASS | 7a (draft 7): the box's width |
| E-037 | heat-module-terminal-plate | size z | 100 | 100.0 | PASS | 7a (draft 7): 100 tall on the tray |
| E-038 | heat-module-terminal-plate | holes 4.5;y | 5 | 5 | PASS | 7a (draft 7): 3 to its foot angle, 2 for the DIN rail |
| E-039 | heat-module-din-rail (bought, 35 x 7.5 top hat, 280) | size x | 280 | 280.0 | PASS | 7a (draft 7) |
| E-040 | heat-module-din-rail (bought, 35 x 7.5 top hat, 280) | min y | 635.5 | 635.5 | PASS | 7a (draft 7): web on the plate's rear face |
| E-041 | heat-module-din-rail (bought, 35 x 7.5 top hat, 280) | max y | 643 | 643.0 | PASS | 7a (draft 7): 7.5 deep; the devices clip on at 643 |
| E-042 | heat-module-devices (bought, envelopes: 2 end clamps, X_HM mains and SELV strips, partition, K_HEAT, CS1) | max y | 729 | 729.0 | PASS | 7a (draft 7): K_HEAT (LC1D18 class, 86 deep from the rail) is the deepest device: 643 + 86, 21 clear of the rear lower panel |
| E-043 | heat-module-devices (bought, envelopes: 2 end clamps, X_HM mains and SELV strips, partition, K_HEAT, CS1) | min z | 73 | 73.0 | PASS | 7a (draft 7): K_HEAT 77 tall on the rail's centre line at 111.5 |
| E-044 | heat-module-devices (bought, envelopes: 2 end clamps, X_HM mains and SELV strips, partition, K_HEAT, CS1) | solids | 7 | 7 | PASS | 7a (draft 7): end clamp, X_HM mains (4 x UK 6 N), K_HEAT, partition, X_HM SELV (4 x UK 2.5 N), CS1, end clamp |
| E-045 | heat-module-angles-bottom (20x20x2 aluminium angle, 2 x 205 outside, 2 x 283 inside) | solids | 4 | 4 | PASS | 7a (draft 7): outside the side walls (legs on the tray, bolted into the tray rails), inside the end walls (legs on the tray, nuts under it) |
| E-046 | heat-module-angles-top (20x20x2 aluminium angle, 2 x 165, 2 x 290) | solids | 4 | 4 | PASS | 7a (draft 7): outside, legs on the lid; the lid comes off with its 10 M4 to change the element |
| E-047 | heat-module-angles-corner (20x20x2 aluminium angle, 4 x 72) | solids | 4 | 4 | PASS | 7a (draft 7): between the bottom and top angles' legs |
| E-048 | heat-module-angles-corner (20x20x2 aluminium angle, 4 x 72) | min z | 81.5 | 81.5 | PASS | 7a (draft 7): above the bottom angles' legs |
| E-049 | heat-module-angles-corner (20x20x2 aluminium angle, 4 x 72) | max z | 153.5 | 153.5 | PASS | 7a (draft 7): below the lid angles' legs |
| E-050 | heat-module-element-rails (20x20x2 aluminium angle, 2 x 198) | solids | 2 | 2 | PASS | 7a (draft 7): inside the side walls, sharing the bottom angles' bolts, top legs under the element's ends |
| E-051 | heat-module-element-rails (20x20x2 aluminium angle, 2 x 198) | max z | 81.5 | 81.5 | PASS | 7a (draft 7) |
| E-052 | heat-module-hardware (bought, 64 x M4 x 8 button head, 60 nuts, 4 T-nuts for the 6 mm slot) | solids | 124 | 124 | PASS | 7a (draft 7): 64 bolts and 60 nuts; the 4 bolts into the tray rails take T-nuts, which are not drawn |
| E-053 | clearance | clearance heat-module-collar (bought, 125 flanged starting collar, cut to 55.5);hood-gasket (bought, 3 mm foam ring 150 x 125, glued under the hood's bottom plate) | 0 | 0.0 | PASS | 7a Air (draft 7): the rim brushes the foam |
| E-054 | clearance | clearance heat-module-wall-front;idler-spring (bought, extension spring) | 5 | 5.0 | PASS | 7a (draft 7): the spring runs at Y 409 to 417, the box's front wall at 422 |
| E-055 | clearance | clearance heat-module-tray;idler-spring (bought, extension spring) | 3 | 3.0 | PASS | 7a (draft 7): the tray starts at 420 |
| E-056 | clearance | clearance heat-module-devices (bought, envelopes: 2 end clamps, X_HM mains and SELV strips, partition, K_HEAT, CS1);rear-lower-panel | 21 | 21.0 | PASS | 7a (draft 7): K_HEAT's front at 729, the panel at 750 |
| E-057 | clearance | clearance heat-module-thermostats (bought, 279816 class high-limit and thermal cut-off, envelopes);hood-bottom | 43.5 | 43.5 | PASS | 7a (draft 8): thermostats to 186.5 under the hood's bottom plate at 230 |
| E-058 | clearance | clearance heat-module-tray;tray-rail-1 | 0 | 0.0 | PASS | 7a (draft 7): the tray on the rails |
| E-059 | clearance | clearance heat-module-tray;rail-bottom-rear | 23.06 | 23.06 | PASS | 7a (draft 7): the tray (Z 60..61.5) ends at 700, the rear bottom rail (to Z 40) starts at 710 with its edge rounded 2: sqrt(12^2 + 22^2) - 2; the tray slides out over the rail |
| E-060 | clearance | clearance heat-module-terminal-plate;heat-module-wall-rear | 7 | 7.0 | PASS | 7a (draft 7) |
| E-061 | clearance | clearance heat-module-top;bay-ceiling | 128.5 | 128.5 | PASS | 7a (draft 7): lid top at 171.5, ceiling at 300 |
| E-062 | cut-list | cut_qty heat-module angles | 1 | 1 | PASS | frame-cut-list.csv (draft 7): the cut list keys by item, so this row only proves the angles are listed (the last entry, the terminal plate foot, 1 piece) |
| W-001 | power-module-plate | thickness | 1.5 | 1.5 | PASS | 4 (draft 7): laser-cut steel plate |
| W-002 | power-module-plate | min x | -300 | -300.0 | PASS | 7a Power module (draft 7): 150 wide, 5 from the left post |
| W-003 | power-module-plate | size x | 150 | 150.0 | PASS | 7a (draft 7): the space left of the riser (X -130) behind the rear bulkhead is 155 |
| W-004 | power-module-plate | min z | 270 | 270.0 | PASS | 7a (draft 7): over the mid rear cross rail (260..300) by 30 |
| W-005 | power-module-plate | max z | 990 | 990.0 | PASS | 7a (draft 7): over the top rear cross rail (960..1000) by 30 |
| W-006 | power-module-plate | min y | 651.5 | 651.5 | PASS | 7a (draft 7): on the cross rails' rear faces |
| W-007 | power-module-plate | holes 6.5;y | 4 | 4 | PASS | 7a (draft 7): M6 x 12 into the cross rails' rear slots with T-nuts, two per rail |
| W-008 | power-module-plate | hole_at 6.5;-285;280 | 1 | (-285.000, 280.000) d 6.500 | PASS | 7a (draft 7): on the mid rear cross rail's centre line |
| W-009 | power-module-plate | hole_at 6.5;-165;980 | 1 | (-165.000, 980.000) d 6.500 | PASS | 7a (draft 7): on the top rear cross rail's centre line |
| W-010 | power-module-plate | holes 4.5;y | 16 | 16 | PASS | 7a (draft 7): 2 per DIN rail (10), 4 cover standoffs, 2 for the barrier angle |
| W-011 | power-module-plate | hole_at 6.6;-165;950 | 1 | (-165.000, 950.000) d 6.600 | PASS | 3.1 rule 7 (draft 7): the ground stud, M6 with two nuts; the cord's PE ring terminal and the bonding leads land here |
| W-012 | power-module-din-rails (bought, 5 x 35 x 7.5 top hat, 140) | solids | 5 | 5 | PASS | 4 (draft 7): five rails, A1, A2, A3 (mains) and B1, B2 (SELV), at Z 360, 470, 580, 700, 820 |
| W-013 | power-module-din-rails (bought, 5 x 35 x 7.5 top hat, 140) | size x | 140 | 140.0 | PASS | 7a (draft 7): rails 5 in from the plate's edges |
| W-014 | power-module-din-rails (bought, 5 x 35 x 7.5 top hat, 140) | max y | 660.5 | 660.5 | PASS | 7a (draft 7): devices clip on at 660.5 |
| W-015 | power-module-rail-A1-devices (bought, envelopes: X1 cord: 4 x UK 6 N (L1, L2, N, PE), CB1: 1P MCB, F1: UK 5-HESI fuse terminal, 2 end clamps) | solids | 5 | 5 | PASS | wiring: X1, CB1, F1 and two end clamps on rail A1 |
| W-016 | power-module-rail-A1-devices (bought, envelopes: X1 cord: 4 x UK 6 N (L1, L2, N, PE), CB1: 1P MCB, F1: UK 5-HESI fuse terminal, 2 end clamps) | max x | -217.5 | -217.5 | PASS | 7a (draft 7): 9.5 + 32.8 + 17.5 + 8.2 + 9.5 = 77.5 along the rail from X -295 |
| W-017 | power-module-rail-A1-devices (bought, envelopes: X1 cord: 4 x UK 6 N (L1, L2, N, PE), CB1: 1P MCB, F1: UK 5-HESI fuse terminal, 2 end clamps) | min z | 315 | 315.0 | PASS | 7a (draft 7): CB1 90 tall on the rail at 360 (typical, V-112), 5 inside the cover's bottom edge |
| W-018 | power-module-rail-A2-devices (bought, envelopes: PSU: HDR-60-24, K_MOTOR: LC1K0910BD class mini contactor, 2 end clamps) | max y | 717.5 | 717.5 | PASS | 7a (draft 7): K_MOTOR 57 deep (listing, V-112); the PSU 54.5 (datasheet) |
| W-019 | power-module-rail-B1-devices (bought, envelopes: RLY_MOTOR, RLY_HEAT, RLY_HEAT_LO: 3 x 38.51 class, PTC1 to PTC3 in fuse terminals, F2: UK 5-HESI, X4 heat module SELV: 4 x UK 2.5 N, 2 end clamps) | max y | 730.5 | 730.5 | PASS | 7a (draft 7): the relays 70 deep (typical, V-112): 660.5 + 70, 19.5 from the rear upper panel |
| W-020 | power-module-rail-B1-devices (bought, envelopes: RLY_MOTOR, RLY_HEAT, RLY_HEAT_LO: 3 x 38.51 class, PTC1 to PTC3 in fuse terminals, F2: UK 5-HESI, X4 heat module SELV: 4 x UK 2.5 N, 2 end clamps) | min z | 653.5 | 653.5 | PASS | 7a (draft 7): relays 93 tall on rail B1 at 700, 11.5 above the barrier |
| W-021 | power-module-rail-B2-devices (bought, envelopes: X5 chassis switches: 10 x UK 2.5 N, X6 sensors: 6 x UK 2.5 N, 2 end clamps) | max x | -176.8 | -176.8 | PASS | wiring (draft 7): 9.5 + 62 + 37.2 + 9.5 = 118.2 from X -295 |
| W-022 | power-module-barrier-angle (20x20x2 aluminium angle, 150) | min z | 640 | 640.0 | PASS | 3.1 rule 9 (draft 7): the barrier between mains (A3's blocks end at 603.5) and SELV (B1's relays start at 653.5) |
| W-023 | power-module-barrier | min z | 642 | 642.0 | PASS | 7a (draft 7): 1.5 mm shelf on the angle's leg, out to the devices' depth |
| W-024 | power-module-barrier | max y | 730.5 | 730.5 | PASS | 7a (draft 7): to the deepest device (the relays) |
| W-025 | power-module-barrier | size x | 150 | 150.0 | PASS | 7a (draft 7) |
| W-026 | power-module-cover | min y | 728 | 728.0 | PASS | 7a (draft 7): 1.5 mm cover over the mains rails on four M4 x 75 standoffs from the plate's rear face (653) |
| W-027 | power-module-cover | min z | 310 | 310.0 | PASS | 7a (draft 7): from 3 above the bay ceiling's rear bolt heads (307.1) |
| W-028 | power-module-cover | max z | 640 | 640.0 | PASS | 7a (draft 7): to the barrier |
| W-029 | power-module-cover | holes 4.5;y | 4 | 4 | PASS | 7a (draft 7): the standoffs |
| W-030 | power-module-standoffs (bought, 4 x M4 x 75 hex standoffs, female both ends) | solids | 4 | 4 | PASS | 7a (draft 7) |
| W-031 | power-module-standoffs (bought, 4 x M4 x 75 hex standoffs, female both ends) | size y | 75 | 75.0 | PASS | 7a (draft 7) |
| W-032 | clearance | clearance power-module-cover;rear-upper-panel | 20.5 | 20.5 | PASS | 7a (draft 7): cover back face at 729.5, panel at 750 |
| W-033 | clearance | clearance power-module-rail-B1-devices (bought, envelopes: RLY_MOTOR, RLY_HEAT, RLY_HEAT_LO: 3 x 38.51 class, PTC1 to PTC3 in fuse terminals, F2: UK 5-HESI, X4 heat module SELV: 4 x UK 2.5 N, 2 end clamps);rear-upper-panel | 19.5 | 19.5 | PASS | 7a (draft 7): 15 or more to the panel (the design rule for the module's devices) |
| W-034 | clearance | clearance power-module-plate;rail-mid-rearcross | 0 | 0.0 | PASS | 7a (draft 7): on the rail's rear face |
| W-035 | clearance | clearance power-module-plate;bay-ceiling | 1 | 1.0 | PASS | 7a (draft 7): through the ceiling's slot with 1 each side |
| W-036 | clearance | clearance power-module-rail-A1-devices (bought, envelopes: X1 cord: 4 x UK 6 N (L1, L2, N, PE), CB1: 1P MCB, F1: UK 5-HESI fuse terminal, 2 end clamps);power-module-cover | 7.5 | 7.5 | PASS | 7a (draft 7): CB1's front at 720.5, the cover at 728 |
| W-037 | power-module-hardware (bought, 22 x M4 x 8 button head, 14 nuts) | solids | 36 | 36 | PASS | 7a (draft 7): 10 rail bolts with nuts in the rails' channels, 8 standoff bolts, 4 barrier bolts with nuts |
| W-038 | hardware-power-module-plate (bought, 4 x M6 x 12 hex, washers, T-nuts) | solids | 4 | 4 | PASS | 7a (draft 7) |
| N-001 | front-bulkhead | hole_at 4.5;162;310 | 1 | (162.000, 310.000) d 4.500 | PASS | 7a Bulkheads (draft 8): M4 from the drum side into the lint box's side bars, outside the felt; the lowest head clears the bay ceiling's front edge |
| N-002 | front-bulkhead | hole_at 4.5;-162;380 | 1 | (-162.000, 380.000) d 4.500 | PASS | 7a Bulkheads (draft 8) |
| N-003 | front-bulkhead | holes 4.5;y | 12 | 12 | PASS | 7a Bulkheads (draft 8): four glide holes and six lint box holes; draft 9 adds the moisture bar set's two |
| N-004 | rear-bulkhead | hole_at 4.5;110;690 | 1 | (110.000, 690.000) d 4.500 | PASS | 7a Bulkheads (draft 8): M4 from the drum side into the nozzle's side bars |
| N-005 | rear-bulkhead | hole_at 4.5;-70;812.5 | 1 | (-70.000, 812.500) d 4.500 | PASS | 7a Bulkheads (draft 8): into the nozzle's top bar |
| N-006 | rear-bulkhead | holes 4.5;y | 14 | 14 | PASS | 7a Bulkheads (draft 8): four glide holes and ten nozzle holes |
| N-007 | front-upper-panel | hole_at 8.5;182.434;449.066 | 1 | (182.434, 449.066) d 8.500 | PASS | 7a Door (draft 8): the door switch plunger, on radius 258 at 45 degrees right of bottom |
| N-008 | door-ring | hole_at 8.5;182.434;449.066 | 1 | (182.434, 449.066) d 8.500 | PASS | 7a Door (draft 8): the same hole through the ring |
| N-009 | front-upper-panel | hole_at 4.5;210.718;434.924 | 1 | (210.718, 434.924) d 4.500 | PASS | 7a Door (draft 8): door switch ear, on radius 288, 10 along the tangent |
| N-010 | front-upper-panel | hole_at 4.5;196.576;420.782 | 1 | (196.576, 420.782) d 4.500 | PASS | 7a Door (draft 8): door switch ear |
| N-011 | base-pan | hole_at 6.5;22;230 | 1 | (22.000, 230.000) d 6.500 | PASS | 7a Drive (draft 8): motor cradle bolts, two per cradle |
| N-012 | base-pan | hole_at 6.5;-22;350 | 1 | (-22.000, 350.000) d 6.500 | PASS | 7a Drive (draft 8) |
| N-013 | base-pan | hole_at 6.5;235;70 | 1 | (235.000, 70.000) d 6.500 | PASS | 7a Air (draft 8): the air-proving switch's bracket |
| N-014 | base-pan | hole_at 6.5;265;70 | 1 | (265.000, 70.000) d 6.500 | PASS | 7a Air (draft 8) |
| N-015 | hood-bottom | loop circle;0;525;128;128 | 1 | 1 | PASS | 7a Air (draft 8): the collar's hole in the hood's bottom plate, 125 + 3 |
| N-016 | hood-top | loop rect;0;679;244;50 | 1 | 1 | PASS | 7a Air (draft 8): the trunk's opening in the hood's top plate, the trunk's interior |
| N-017 | cut-list | cut lint-box side bar | 400.1 | 400.1 | PASS | 7a Air (draft 8): the box's side bars from 62 to the liner at their outer corner (462.1) |
| N-018 | cut-list | cut trunk side bar | 573.5 | 573.5 | PASS | 7a Air (draft 8): trunk side bars from the hood's top plate (258) to 831.5 |
| N-019 | cut-list | cut hood side bar | 257.5 | 257.5 | PASS | 7a Air (draft 8): hood side bars, 448 to 705.5 |
| N-020 | cut-list | cut nozzle side bar | 158 | 158.0 | PASS | 7a Air (draft 8): nozzle side bars, 658.5 to 816.5 |
| N-021 | cut-list | cut spool side bar | 136 | 136.0 | PASS | 7a Air (draft 8): spool side bars, 62 to 198 |
| N-022 | cut-list | cut liner | 1482.4 | 1482.4 | PASS | 7a Door (draft 8): the liner's strip, the mid-surface circumference less the 2 mm seam gap |
| N-023 | clearance | clearance liner;door-ring | 0 | 0.0 | PASS | 7a Door (draft 8): the liner's front edge on the ring's back face |
| N-024 | clearance | clearance liner;front-bulkhead | 0.2 | 0.2 | PASS | 7a Door (draft 8): 0.2 float, seated against the bulkhead in use |
| N-025 | clearance | clearance liner;lint-box-front | 0.2 | 0.2 | PASS | 7a Air (draft 8): the box's plates follow the liner 0.2 outside it |
| N-026 | clearance | clearance basket-mesh (bought, stainless 18 x 16 mesh strip, 42 wide, 350 long, wrapped and folded 5 at each edge);front-bulkhead | 0.9 | 0.9 | PASS | 7 Lint management (draft 8): the basket passes the slot (238 to 267) with 0.9 each side |
| N-027 | clearance | clearance basket-far-plate;lint-box-front | 0.5 | 0.5 | PASS | 7 Lint management (draft 8): the far plate 0.5 behind the front plate's back face |
| N-028 | clearance | clearance basket-lip-plate;drum-ring-front | 5.701 | 5.701 | PASS | 7 Lint management (draft 8): the lip (radius to 268.5, Y to 44.5) to the ring face (radius from 270 at Y 50): sqrt(5.5^2 + 1.5^2) |
| N-029 | clearance | clearance basket-lip-plate;felt-seal-front-long | 4.5 | 4.5 | PASS | 7 Lint management (draft 8): the lip's outer radius 268.5 inside the felt's 273 |
| N-030 | clearance | clearance door-switch (bought, two-contact plunger switch, envelope);door-disc | 0.5 | 0.5 | PASS | 7a Door (draft 8): the plunger, drawn pressed, 0.5 off the closed disc's back face |
| N-031 | clearance | clearance nozzle-bars (40 x 8 aluminium flat bar: 2 sides, top, bottom);rear-bulkhead | 1 | 1.0 | PASS | 7a Air (draft 8): 1 of compressed foam between the nozzle's bars and the bulkhead |
| N-032 | clearance | clearance basket-pull (bought, D-pull, 64 mm centres, 25 projection);door-disc | 28 | 28.0 | PASS | 7 Lint management (draft 8): the pull's bar ends at Y 16.5, the closed disc's back at -11.5 |
| N-033 | bay-ceiling | hole_at 16;290;60 | 1 | (290.000, 60.000) d 16.000 | PASS | 7a Panels (draft 8): the door switch cable's grommet at the right front, behind the bulkhead; 16 in draft 9 so the moisture pair shares it |
| N-034 | front-bulkhead | hole_at 16;290;330 | 1 | (290.000, 330.000) d 16.000 | PASS | 7a Bulkheads (draft 8): the door switch cable's grommet, outside the felt and the drum; 16 in draft 9 so the moisture pair shares it |
| N-035 | base-pan | hole_at 4.5;-250;280 | 1 | (-250.000, 280.000) d 4.500 | PASS | 7a Panels (draft 8): one of four M4 cable clamp holes along the left side for the bay harness |
| N-036 | base-pan | holes 4.5;z | 4 | 4 | PASS | 7a Panels (draft 8): the four cable clamp holes |
| N-037 | cut-list | cut trunk top bar | 244 | 244.0 | PASS | 7a Air (draft 8): the trunk's top bar between its side bars |
| N-038 | cut-list | cut hood end bar | 334 | 334.0 | PASS | 7a Air (draft 8): the hood's front and rear bars between its side bars |
| N-039 | cut-list | cut nozzle end bar | 212 | 212.0 | PASS | 7a Air (draft 8) |
| N-040 | cut-list | cut_qty lint-box side bar | 2 | 2 | PASS | 7a Air (draft 8) |
| Q-001 | blower-plate | thickness | 1.5 | 1.5 | PASS | 7a Drive (draft 9): 1.5 steel |
| Q-002 | blower-plate | normal | 0,1,0 | (-0.0, -1.0, -0.0) | PASS | 7a Drive (draft 9): stands across the bay in front of the housing |
| Q-003 | blower-plate | outline 260;245 | 1 | rrect 260.000 x 245.000 | PASS | 7a Drive (draft 9): 260 wide, from the pan to 245, 15 under the mid rails |
| Q-004 | blower-plate | min y | 84 | 84.0 | PASS | 7a Drive (draft 9): its front face carries the spool's foam |
| Q-005 | blower-plate | max y | 85.5 | 85.5 | PASS | 7a Drive (draft 9): the housing's inlet face sits on its back |
| Q-006 | blower-plate | loop rect;0;130;140;120 | 1 | 1 | PASS | 7a Drive (draft 9): the spool's bore, 140 x 120, cut through it |
| Q-007 | blower-plate | holes 4.5;y | 8 | 8 | PASS | 7a Drive (draft 9): four for the housing's screws (nominal pattern, V-107), four into the feet's legs |
| Q-008 | blower-plate | hole_at 4.5;88;60 | 1 | (88.000, 60.000) d 4.500 | PASS | 7a Drive (draft 9): housing screw |
| Q-009 | blower-plate | hole_at 4.5;-88;180 | 1 | (-88.000, 180.000) d 4.500 | PASS | 7a Drive (draft 9): housing screw |
| Q-010 | blower-plate | hole_at 4.5;110;10 | 1 | (110.000, 10.000) d 4.500 | PASS | 7a Drive (draft 9): into the right foot's leg |
| Q-011 | blower-plate | loops circle | 8 | 8 | PASS | 7a Drive (draft 9) |
| Q-012 | base-pan | hole_at 6.5;70;74 | 1 | (70.000, 74.000) d 6.500 | PASS | 7a Drive (draft 9): blower plate foot bolt |
| Q-013 | base-pan | hole_at 6.5;-110;74 | 1 | (-110.000, 74.000) d 6.500 | PASS | 7a Drive (draft 9): blower plate foot bolt |
| Q-014 | entry-blank | thickness | 1.5 | 1.5 | PASS | 7a Panels (draft 9): 1.5 steel |
| Q-015 | entry-blank | outline 60;44 | 1 | rrect 60.000 x 44.000 | PASS | 7a Panels (draft 9): 60 x 44, inside the rear lower panel over the gas entry |
| Q-016 | entry-blank | holes 4.5;y | 2 | 2 | PASS | 7a Panels (draft 9): two M4 |
| Q-017 | entry-blank | hole_at 4.5;-251;150 | 1 | (-251.000, 150.000) d 4.500 | PASS | 7a Panels (draft 9): 21 left of the entry |
| Q-018 | entry-blank | min y | 748.5 | 748.5 | PASS | 7a Panels (draft 9): on the panel's inside face |
| Q-019 | entry-blank | max y | 750 | 750.0 | PASS | 7a Panels (draft 9) |
| Q-020 | rear-lower-panel | hole_at 25;-230;150 | 1 | (-230.000, 150.000) d 25.000 | PASS | 7a Panels (draft 9): the gas entry, for a 3/8 NPT bulkhead fitting on the gas module; blanked otherwise |
| Q-021 | rear-lower-panel | hole_at 20;-230;66 | 1 | (-230.000, 66.000) d 20.000 | PASS | 7a Panels (draft 9): the condensate drain, for a hose grommet on the heat pump module; blanked otherwise |
| Q-022 | rear-lower-panel | holes 4.5;y | 4 | 4 | PASS | 7a Panels (draft 9): the two blanks' M4 |
| Q-023 | rear-lower-panel | hole_at 4.5;-209;66 | 1 | (-209.000, 66.000) d 4.500 | PASS | 7a Panels (draft 9) |
| Q-024 | front-bulkhead | hole_at 16;212.012;499.02 | 1 | (212.012, 499.020) d 16.000 | PASS | 7a Bulkheads (draft 9): the moisture bar set's terminals, on radius 250 at 58 degrees right of bottom: 250 sin 58, 631.5 - 250 cos 58 |
| Q-025 | front-bulkhead | hole_at 4.5;193.465;469.339 | 1 | (193.465, 469.339) d 4.500 | PASS | 7a Bulkheads (draft 9): the bar set's M4, 35 along the bars from its centre |
| Q-026 | front-bulkhead | hole_at 4.5;230.559;528.702 | 1 | (230.559, 528.702) d 4.500 | PASS | 7a Bulkheads (draft 9) |
| Q-027 | lint-box-back | hole_at 4.5;120;170 | 1 | (120.000, 170.000) d 4.500 | PASS | 7a Air (draft 9): the exhaust thermistor's M4, right of the spool |
| Q-028 | lint-box-back | loop rect;120;155;12;18 | 1 | 1 | PASS | 7a Air (draft 9): the thermistor's nib through the plate into the box, 12 x 18 |
| Q-029 | lint-box-back | holes 4.5;y | 19 | 19 | PASS | 7a Air (draft 8): 6 side bar, 2 bottom bar, 4 spool side, 3 spool top, 3 spool bottom; draft 9 adds the thermistor's one |
| Q-030 | cut-list | cut exhaust duct (bought) | 609.5 | 609.5 | PASS | 7a Air (draft 9): from Y 192 to 801.5 |
| Q-031 | cut-list | cut blower-plate feet | 90 | 90.0 | PASS | 7a Drive (draft 9) |
| Q-032 | cut-list | cut_qty blower-plate feet | 2 | 2 | PASS | 7a Drive (draft 9) |
| Q-033 | clearance | clearance blower-plate;blower (bought) | 0 | 0.0 | PASS | 7a Drive (draft 9): the housing's inlet face on the plate's back |
| Q-034 | clearance | clearance blower-plate;spool-foam (bought, 6 mm closed-cell foam tape 8 wide, 600, compressed to 4 on the blower plate) | 0 | 0.0 | PASS | 7a Drive (draft 9): the spool's foam on the plate's front face |
| Q-035 | clearance | clearance th1-exhaust-thermistor (bought, 10 k NTC appliance thermistor, envelope);blower-plate | 22 | 22.0 | PASS | 7a Air (draft 9): the thermistor's terminals end at Y 62, the plate at 84 |
| Q-036 | clearance | clearance exhaust-duct (bought, 4 in aluminium pipe, 102 x 1, cut to length, one 6.5 hole for the tap);tray-rail-2 | 57.75 | 57.747 | PASS | 7a Air (draft 9): the pipe (axis 230, 150, radius 51) beside and above the right tray rail: its top inner corner (168.5, 58.5, rounded 1.5) is 110.25 from the axis |
| Q-037 | clearance | clearance exhaust-duct (bought, 4 in aluminium pipe, 102 x 1, cut to length, one 6.5 hole for the tap);heat-module-tray | 55.92 | 55.922 | PASS | 7a Air (draft 9): beside and above the tray: its top right edge (170, 61.5) is 106.92 from the pipe's axis |
| Q-038 | clearance | clearance moisture-bars (bought, dryer moisture sensor bar set, two stainless strips on an insulating base, envelope);basket-lip-plate | 40.15 | 40.148 | PASS | 7 Lint management (draft 9): the bar set (47.2 degrees right of bottom at its near end, radius 235 to 265) clear of the lip ring (to 37.5 degrees, radius 232 to 268.5): measured 40.15 |
| Q-039 | clearance | clearance moisture-bars (bought, dryer moisture sensor bar set, two stainless strips on an insulating base, envelope);drum-ring-front | 1.3 | 1.306 | PASS | 7a Bulkheads (draft 9): the bar set ends at Y 49.5, the ring's front face is at 50, and its corners reach radius 268.8 inside the 270 bore: sqrt(0.5^2 + 1.2^2) |
| Q-040 | clearance | clearance ps1-tube (bought, 6 mm silicone tube from the tap to PS1, drawn on its route);exhaust-thermostats (bought, TF2 thermal fuse, T_HI and T_LO cycling thermostats, envelopes on the blower outlet) | 16.16 | 16.162 | PASS | 7a Air (draft 9): the tube (radius 3, on 240) runs over the thermostats (to 221): 16 plus the rounded bend |
| Q-041 | clearance | clearance exhaust-clamps (bought, 2 x worm-drive hose clamps for 102, envelopes);rear-lower-panel | 0 | 0.0 | PASS | 7a Air (draft 9): the inside clamp bears on the panel |
| Q-042 | clearance | clearance entry-blank;rear-lower-panel | 0 | 0.0 | PASS | 7a Panels (draft 9) |
| Q-043 | clearance | clearance cable-clamps (bought, 4 x nylon P-clip for a 12 mm bundle, envelopes);base-pan | 0 | 0.0 | PASS | 7a Panels (draft 9) |
| Q-044 | clearance | clearance blower-plate-feet (angle 20x20x2, 2 x 90);base-pan | 0 | 0.0 | PASS | 7a Drive (draft 9) |
| Q-045 | clearance | clearance blower-plate;tray-rail-2 | 20 | 20.0 | PASS | 7a Drive (draft 9): the plate (to X 130) and the tray rails (from 150) |
| Q-046 | clearance | clearance exhaust-duct (bought, 4 in aluminium pipe, 102 x 1, cut to length, one 6.5 hole for the tap);motor (bought) | 110.95 | 110.948 | PASS | 7a Air (draft 9): the pipe's axis (230, 150) is 231.95 from the motor's (0, 120), less the frame's 70 and the pipe's 51 |
| Q-047 | clearance | clearance exhaust-duct (bought, 4 in aluminium pipe, 102 x 1, cut to length, one 6.5 hole for the tap);exhaust-clamps (bought, 2 x worm-drive hose clamps for 102, envelopes) | 0 | 0.0 | PASS | 7a Air (draft 9): the clamps on the pipe |

## 2. Generic checks on every part

| part | check | measured | result |
|---|---|---|---|
| base-pan | one solid | 1 | PASS |
| base-pan | valid B-rep (BRepCheck) | 1 | PASS |
| base-pan | closed shells | 1 | PASS |
| base-pan | volume positive | 770130.2 | PASS |
| base-pan | in the assembly with the same volume and place | True | PASS |
| base-pan | section edges all closed | 0 | PASS |
| base-pan | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 44 loops, 0 unclassified | PASS |
| base-pan | every cut lies inside the outline | 43 | PASS |
| base-pan | no two cuts overlap | 0 overlapping pairs | PASS |
| base-pan.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| base-pan.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 44 matched, 0 only in STEP, 0 only in DXF | PASS |
| base-pan.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
| basket-far-clamp | one solid | 1 | PASS |
| basket-far-clamp | valid B-rep (BRepCheck) | 1 | PASS |
| basket-far-clamp | closed shells | 1 | PASS |
| basket-far-clamp | volume positive | 12155.5 | PASS |
| basket-far-clamp | in the assembly with the same volume and place | True | PASS |
| basket-far-clamp | section edges all closed | 0 | PASS |
| basket-far-clamp | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 7 loops, 0 unclassified | PASS |
| basket-far-clamp | every cut lies inside the outline | 6 | PASS |
| basket-far-clamp | no two cuts overlap | 0 overlapping pairs | PASS |
| basket-far-clamp.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| basket-far-clamp.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 7 matched, 0 only in STEP, 0 only in DXF | PASS |
| basket-far-clamp.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
| basket-far-plate | one solid | 1 | PASS |
| basket-far-plate | valid B-rep (BRepCheck) | 1 | PASS |
| basket-far-plate | closed shells | 1 | PASS |
| basket-far-plate | volume positive | 24347.2 | PASS |
| basket-far-plate | in the assembly with the same volume and place | True | PASS |
| basket-far-plate | section edges all closed | 0 | PASS |
| basket-far-plate | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 7 loops, 0 unclassified | PASS |
| basket-far-plate | every cut lies inside the outline | 6 | PASS |
| basket-far-plate | no two cuts overlap | 0 overlapping pairs | PASS |
| basket-far-plate.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| basket-far-plate.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 7 matched, 0 only in STEP, 0 only in DXF | PASS |
| basket-far-plate.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
| basket-lip-clamp | one solid | 1 | PASS |
| basket-lip-clamp | valid B-rep (BRepCheck) | 1 | PASS |
| basket-lip-clamp | closed shells | 1 | PASS |
| basket-lip-clamp | volume positive | 5002.1 | PASS |
| basket-lip-clamp | in the assembly with the same volume and place | True | PASS |
| basket-lip-clamp | section edges all closed | 0 | PASS |
| basket-lip-clamp | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 8 loops, 0 unclassified | PASS |
| basket-lip-clamp | every cut lies inside the outline | 7 | PASS |
| basket-lip-clamp | no two cuts overlap | 0 overlapping pairs | PASS |
| basket-lip-clamp.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| basket-lip-clamp.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 8 matched, 0 only in STEP, 0 only in DXF | PASS |
| basket-lip-clamp.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
| basket-lip-plate | one solid | 1 | PASS |
| basket-lip-plate | valid B-rep (BRepCheck) | 1 | PASS |
| basket-lip-plate | closed shells | 1 | PASS |
| basket-lip-plate | volume positive | 14075.0 | PASS |
| basket-lip-plate | in the assembly with the same volume and place | True | PASS |
| basket-lip-plate | section edges all closed | 0 | PASS |
| basket-lip-plate | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon (composite outline allowed) | 8 loops, 1 unclassified | PASS |
| basket-lip-plate | every cut lies inside the outline | 7 | PASS |
| basket-lip-plate | no two cuts overlap | 0 overlapping pairs | PASS |
| basket-lip-plate.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| basket-lip-plate.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 8 matched, 0 only in STEP, 0 only in DXF | PASS |
| basket-lip-plate.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
| bay-ceiling | one solid | 1 | PASS |
| bay-ceiling | valid B-rep (BRepCheck) | 1 | PASS |
| bay-ceiling | closed shells | 1 | PASS |
| bay-ceiling | volume positive | 685439.8 | PASS |
| bay-ceiling | in the assembly with the same volume and place | True | PASS |
| bay-ceiling | section edges all closed | 0 | PASS |
| bay-ceiling | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 29 loops, 0 unclassified | PASS |
| bay-ceiling | every cut lies inside the outline | 28 | PASS |
| bay-ceiling | no two cuts overlap | 0 overlapping pairs | PASS |
| bay-ceiling.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| bay-ceiling.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 29 matched, 0 only in STEP, 0 only in DXF | PASS |
| bay-ceiling.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
| blower-plate | one solid | 1 | PASS |
| blower-plate | valid B-rep (BRepCheck) | 1 | PASS |
| blower-plate | closed shells | 1 | PASS |
| blower-plate | volume positive | 70112.8 | PASS |
| blower-plate | in the assembly with the same volume and place | True | PASS |
| blower-plate | section edges all closed | 0 | PASS |
| blower-plate | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 10 loops, 0 unclassified | PASS |
| blower-plate | every cut lies inside the outline | 9 | PASS |
| blower-plate | no two cuts overlap | 0 overlapping pairs | PASS |
| blower-plate.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| blower-plate.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 10 matched, 0 only in STEP, 0 only in DXF | PASS |
| blower-plate.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
| console-cap | one solid | 1 | PASS |
| console-cap | valid B-rep (BRepCheck) | 1 | PASS |
| console-cap | closed shells | 1 | PASS |
| console-cap | volume positive | 146545.1 | PASS |
| console-cap | in the assembly with the same volume and place | True | PASS |
| console-cap | section edges all closed | 0 | PASS |
| console-cap | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 11 loops, 0 unclassified | PASS |
| console-cap | every cut lies inside the outline | 10 | PASS |
| console-cap | no two cuts overlap | 0 overlapping pairs | PASS |
| console-cap.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| console-cap.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 11 matched, 0 only in STEP, 0 only in DXF | PASS |
| console-cap.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
| console-cheek-left | one solid | 1 | PASS |
| console-cheek-left | valid B-rep (BRepCheck) | 1 | PASS |
| console-cheek-left | closed shells | 1 | PASS |
| console-cheek-left | volume positive | 42473.1 | PASS |
| console-cheek-left | in the assembly with the same volume and place | True | PASS |
| console-cheek-left | section edges all closed | 0 | PASS |
| console-cheek-left | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 6 loops, 0 unclassified | PASS |
| console-cheek-left | every cut lies inside the outline | 5 | PASS |
| console-cheek-left | no two cuts overlap | 0 overlapping pairs | PASS |
| console-cheek-left.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| console-cheek-left.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 6 matched, 0 only in STEP, 0 only in DXF | PASS |
| console-cheek-left.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
| console-cheek-right | one solid | 1 | PASS |
| console-cheek-right | valid B-rep (BRepCheck) | 1 | PASS |
| console-cheek-right | closed shells | 1 | PASS |
| console-cheek-right | volume positive | 42473.1 | PASS |
| console-cheek-right | in the assembly with the same volume and place | True | PASS |
| console-cheek-right | section edges all closed | 0 | PASS |
| console-cheek-right | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 6 loops, 0 unclassified | PASS |
| console-cheek-right | every cut lies inside the outline | 5 | PASS |
| console-cheek-right | no two cuts overlap | 0 overlapping pairs | PASS |
| console-cheek-right.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| console-cheek-right.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 6 matched, 0 only in STEP, 0 only in DXF | PASS |
| console-cheek-right.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
| console-face | one solid | 1 | PASS |
| console-face | valid B-rep (BRepCheck) | 1 | PASS |
| console-face | closed shells | 1 | PASS |
| console-face | volume positive | 105612.3 | PASS |
| console-face | in the assembly with the same volume and place | True | PASS |
| console-face | section edges all closed | 0 | PASS |
| console-face | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 16 loops, 0 unclassified | PASS |
| console-face | every cut lies inside the outline | 15 | PASS |
| console-face | no two cuts overlap | 0 overlapping pairs | PASS |
| console-face.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| console-face.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 16 matched, 0 only in STEP, 0 only in DXF | PASS |
| console-face.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
| console-post-1 | one solid | 1 | PASS |
| console-post-1 | valid B-rep (BRepCheck) | 1 | PASS |
| console-post-1 | closed shells | 1 | PASS |
| console-post-1 | volume positive | 217723.5 | PASS |
| console-post-1 | in the assembly with the same volume and place | True | PASS |
| console-post-2 | one solid | 1 | PASS |
| console-post-2 | valid B-rep (BRepCheck) | 1 | PASS |
| console-post-2 | closed shells | 1 | PASS |
| console-post-2 | volume positive | 217723.5 | PASS |
| console-post-2 | in the assembly with the same volume and place | True | PASS |
| console-post-3 | one solid | 1 | PASS |
| console-post-3 | valid B-rep (BRepCheck) | 1 | PASS |
| console-post-3 | closed shells | 1 | PASS |
| console-post-3 | volume positive | 217723.5 | PASS |
| console-post-3 | in the assembly with the same volume and place | True | PASS |
| console-post-4 | one solid | 1 | PASS |
| console-post-4 | valid B-rep (BRepCheck) | 1 | PASS |
| console-post-4 | closed shells | 1 | PASS |
| console-post-4 | volume positive | 217723.5 | PASS |
| console-post-4 | in the assembly with the same volume and place | True | PASS |
| console-rail-front | one solid | 1 | PASS |
| console-rail-front | valid B-rep (BRepCheck) | 1 | PASS |
| console-rail-front | closed shells | 1 | PASS |
| console-rail-front | volume positive | 664056.7 | PASS |
| console-rail-front | in the assembly with the same volume and place | True | PASS |
| console-rail-left | one solid | 1 | PASS |
| console-rail-left | valid B-rep (BRepCheck) | 1 | PASS |
| console-rail-left | closed shells | 1 | PASS |
| console-rail-left | volume positive | 63684.1 | PASS |
| console-rail-left | in the assembly with the same volume and place | True | PASS |
| console-rail-rear | one solid | 1 | PASS |
| console-rail-rear | valid B-rep (BRepCheck) | 1 | PASS |
| console-rail-rear | closed shells | 1 | PASS |
| console-rail-rear | volume positive | 664056.7 | PASS |
| console-rail-rear | in the assembly with the same volume and place | True | PASS |
| console-rail-right | one solid | 1 | PASS |
| console-rail-right | valid B-rep (BRepCheck) | 1 | PASS |
| console-rail-right | closed shells | 1 | PASS |
| console-rail-right | volume positive | 63684.1 | PASS |
| console-rail-right | in the assembly with the same volume and place | True | PASS |
| console-rear | one solid | 1 | PASS |
| console-rear | valid B-rep (BRepCheck) | 1 | PASS |
| console-rear | closed shells | 1 | PASS |
| console-rear | volume positive | 208107.9 | PASS |
| console-rear | in the assembly with the same volume and place | True | PASS |
| console-rear | section edges all closed | 0 | PASS |
| console-rear | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 9 loops, 0 unclassified | PASS |
| console-rear | every cut lies inside the outline | 8 | PASS |
| console-rear | no two cuts overlap | 0 overlapping pairs | PASS |
| console-rear.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| console-rear.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 9 matched, 0 only in STEP, 0 only in DXF | PASS |
| console-rear.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
| door-disc | one solid | 1 | PASS |
| door-disc | valid B-rep (BRepCheck) | 1 | PASS |
| door-disc | closed shells | 1 | PASS |
| door-disc | volume positive | 457917.0 | PASS |
| door-disc | in the assembly with the same volume and place | True | PASS |
| door-disc | section edges all closed | 0 | PASS |
| door-disc | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 5 loops, 0 unclassified | PASS |
| door-disc | every cut lies inside the outline | 4 | PASS |
| door-disc | no two cuts overlap | 0 overlapping pairs | PASS |
| door-disc.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| door-disc.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 5 matched, 0 only in STEP, 0 only in DXF | PASS |
| door-disc.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 631.50) | PASS |
| door-ring | one solid | 1 | PASS |
| door-ring | valid B-rep (BRepCheck) | 1 | PASS |
| door-ring | closed shells | 1 | PASS |
| door-ring | volume positive | 145112.1 | PASS |
| door-ring | in the assembly with the same volume and place | True | PASS |
| door-ring | section edges all closed | 0 | PASS |
| door-ring | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 13 loops, 0 unclassified | PASS |
| door-ring | every cut lies inside the outline | 12 | PASS |
| door-ring | no two cuts overlap | 0 overlapping pairs | PASS |
| door-ring.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| door-ring.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 13 matched, 0 only in STEP, 0 only in DXF | PASS |
| door-ring.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 631.50) | PASS |
| drum-ring-front | one solid | 1 | PASS |
| drum-ring-front | valid B-rep (BRepCheck) | 1 | PASS |
| drum-ring-front | closed shells | 1 | PASS |
| drum-ring-front | volume positive | 141703.2 | PASS |
| drum-ring-front | in the assembly with the same volume and place | True | PASS |
| drum-ring-front | section edges all closed | 0 | PASS |
| drum-ring-front | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 32 loops, 0 unclassified | PASS |
| drum-ring-front | every cut lies inside the outline | 31 | PASS |
| drum-ring-front | no two cuts overlap | 0 overlapping pairs | PASS |
| drum-ring-rear | one solid | 1 | PASS |
| drum-ring-rear | valid B-rep (BRepCheck) | 1 | PASS |
| drum-ring-rear | closed shells | 1 | PASS |
| drum-ring-rear | volume positive | 141703.2 | PASS |
| drum-ring-rear | in the assembly with the same volume and place | True | PASS |
| drum-ring-rear | section edges all closed | 0 | PASS |
| drum-ring-rear | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 32 loops, 0 unclassified | PASS |
| drum-ring-rear | every cut lies inside the outline | 31 | PASS |
| drum-ring-rear | no two cuts overlap | 0 overlapping pairs | PASS |
| drum-sheet | one solid | 1 | PASS |
| drum-sheet | valid B-rep (BRepCheck) | 1 | PASS |
| drum-sheet | closed shells | 1 | PASS |
| drum-sheet | volume positive | 873714.1 | PASS |
| drum-sheet | in the assembly with the same volume and place | True | PASS |
| drum-splice | one solid | 1 | PASS |
| drum-splice | valid B-rep (BRepCheck) | 1 | PASS |
| drum-splice | closed shells | 1 | PASS |
| drum-splice | volume positive | 32383.4 | PASS |
| drum-splice | in the assembly with the same volume and place | True | PASS |
| entry-blank | one solid | 1 | PASS |
| entry-blank | valid B-rep (BRepCheck) | 1 | PASS |
| entry-blank | closed shells | 1 | PASS |
| entry-blank | volume positive | 3865.9 | PASS |
| entry-blank | in the assembly with the same volume and place | True | PASS |
| entry-blank | section edges all closed | 0 | PASS |
| entry-blank | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 3 loops, 0 unclassified | PASS |
| entry-blank | every cut lies inside the outline | 2 | PASS |
| entry-blank | no two cuts overlap | 0 overlapping pairs | PASS |
| entry-blank.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| entry-blank.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 3 matched, 0 only in STEP, 0 only in DXF | PASS |
| entry-blank.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
| felt-seal-front-long | one solid | 1 | PASS |
| felt-seal-front-long | valid B-rep (BRepCheck) | 1 | PASS |
| felt-seal-front-long | closed shells | 1 | PASS |
| felt-seal-front-long | volume positive | 184592.7 | PASS |
| felt-seal-front-long | in the assembly with the same volume and place | True | PASS |
| felt-seal-front-long | section edges all closed | 0 | PASS |
| felt-seal-front-long | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 1 loops, 0 unclassified | PASS |
| felt-seal-front-long | every cut lies inside the outline | 0 | PASS |
| felt-seal-front-long | no two cuts overlap | 0 overlapping pairs | PASS |
| felt-seal-front-short | one solid | 1 | PASS |
| felt-seal-front-short | valid B-rep (BRepCheck) | 1 | PASS |
| felt-seal-front-short | closed shells | 1 | PASS |
| felt-seal-front-short | volume positive | 57018.9 | PASS |
| felt-seal-front-short | in the assembly with the same volume and place | True | PASS |
| felt-seal-front-short | section edges all closed | 0 | PASS |
| felt-seal-front-short | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 1 loops, 0 unclassified | PASS |
| felt-seal-front-short | every cut lies inside the outline | 0 | PASS |
| felt-seal-front-short | no two cuts overlap | 0 overlapping pairs | PASS |
| felt-seal-rear-long | one solid | 1 | PASS |
| felt-seal-rear-long | valid B-rep (BRepCheck) | 1 | PASS |
| felt-seal-rear-long | closed shells | 1 | PASS |
| felt-seal-rear-long | volume positive | 230740.9 | PASS |
| felt-seal-rear-long | in the assembly with the same volume and place | True | PASS |
| felt-seal-rear-long | section edges all closed | 0 | PASS |
| felt-seal-rear-long | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 1 loops, 0 unclassified | PASS |
| felt-seal-rear-long | every cut lies inside the outline | 0 | PASS |
| felt-seal-rear-long | no two cuts overlap | 0 overlapping pairs | PASS |
| felt-seal-rear-short | one solid | 1 | PASS |
| felt-seal-rear-short | valid B-rep (BRepCheck) | 1 | PASS |
| felt-seal-rear-short | closed shells | 1 | PASS |
| felt-seal-rear-short | volume positive | 71273.6 | PASS |
| felt-seal-rear-short | in the assembly with the same volume and place | True | PASS |
| felt-seal-rear-short | section edges all closed | 0 | PASS |
| felt-seal-rear-short | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 1 loops, 0 unclassified | PASS |
| felt-seal-rear-short | every cut lies inside the outline | 0 | PASS |
| felt-seal-rear-short | no two cuts overlap | 0 overlapping pairs | PASS |
| front-bulkhead | one solid | 1 | PASS |
| front-bulkhead | valid B-rep (BRepCheck) | 1 | PASS |
| front-bulkhead | closed shells | 1 | PASS |
| front-bulkhead | volume positive | 403407.6 | PASS |
| front-bulkhead | in the assembly with the same volume and place | True | PASS |
| front-bulkhead | section edges all closed | 0 | PASS |
| front-bulkhead | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 26 loops, 0 unclassified | PASS |
| front-bulkhead | every cut lies inside the outline | 25 | PASS |
| front-bulkhead | no two cuts overlap | 0 overlapping pairs | PASS |
| front-bulkhead.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| front-bulkhead.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 26 matched, 0 only in STEP, 0 only in DXF | PASS |
| front-bulkhead.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
| front-lower-panel | one solid | 1 | PASS |
| front-lower-panel | valid B-rep (BRepCheck) | 1 | PASS |
| front-lower-panel | closed shells | 1 | PASS |
| front-lower-panel | volume positive | 242871.1 | PASS |
| front-lower-panel | in the assembly with the same volume and place | True | PASS |
| front-lower-panel | section edges all closed | 0 | PASS |
| front-lower-panel | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 65 loops, 0 unclassified | PASS |
| front-lower-panel | every cut lies inside the outline | 64 | PASS |
| front-lower-panel | no two cuts overlap | 0 overlapping pairs | PASS |
| front-lower-panel.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| front-lower-panel.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 65 matched, 0 only in STEP, 0 only in DXF | PASS |
| front-lower-panel.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
| front-upper-panel | one solid | 1 | PASS |
| front-upper-panel | valid B-rep (BRepCheck) | 1 | PASS |
| front-upper-panel | closed shells | 1 | PASS |
| front-upper-panel | volume positive | 493200.4 | PASS |
| front-upper-panel | in the assembly with the same volume and place | True | PASS |
| front-upper-panel | section edges all closed | 0 | PASS |
| front-upper-panel | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 31 loops, 0 unclassified | PASS |
| front-upper-panel | every cut lies inside the outline | 30 | PASS |
| front-upper-panel | no two cuts overlap | 0 overlapping pairs | PASS |
| front-upper-panel.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| front-upper-panel.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 31 matched, 0 only in STEP, 0 only in DXF | PASS |
| front-upper-panel.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
| heat-module-terminal-plate | one solid | 1 | PASS |
| heat-module-terminal-plate | valid B-rep (BRepCheck) | 1 | PASS |
| heat-module-terminal-plate | closed shells | 1 | PASS |
| heat-module-terminal-plate | volume positive | 43369.1 | PASS |
| heat-module-terminal-plate | in the assembly with the same volume and place | True | PASS |
| heat-module-terminal-plate | section edges all closed | 0 | PASS |
| heat-module-terminal-plate | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 6 loops, 0 unclassified | PASS |
| heat-module-terminal-plate | every cut lies inside the outline | 5 | PASS |
| heat-module-terminal-plate | no two cuts overlap | 0 overlapping pairs | PASS |
| heat-module-terminal-plate.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| heat-module-terminal-plate.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 6 matched, 0 only in STEP, 0 only in DXF | PASS |
| heat-module-terminal-plate.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
| heat-module-top | one solid | 1 | PASS |
| heat-module-top | valid B-rep (BRepCheck) | 1 | PASS |
| heat-module-top | closed shells | 1 | PASS |
| heat-module-top | volume positive | 70030.5 | PASS |
| heat-module-top | in the assembly with the same volume and place | True | PASS |
| heat-module-top | section edges all closed | 0 | PASS |
| heat-module-top | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 20 loops, 0 unclassified | PASS |
| heat-module-top | every cut lies inside the outline | 19 | PASS |
| heat-module-top | no two cuts overlap | 0 overlapping pairs | PASS |
| heat-module-top.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| heat-module-top.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 20 matched, 0 only in STEP, 0 only in DXF | PASS |
| heat-module-top.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
| heat-module-tray | one solid | 1 | PASS |
| heat-module-tray | valid B-rep (BRepCheck) | 1 | PASS |
| heat-module-tray | closed shells | 1 | PASS |
| heat-module-tray | volume positive | 142392.2 | PASS |
| heat-module-tray | in the assembly with the same volume and place | True | PASS |
| heat-module-tray | section edges all closed | 0 | PASS |
| heat-module-tray | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 15 loops, 0 unclassified | PASS |
| heat-module-tray | every cut lies inside the outline | 14 | PASS |
| heat-module-tray | no two cuts overlap | 0 overlapping pairs | PASS |
| heat-module-tray.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| heat-module-tray.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 15 matched, 0 only in STEP, 0 only in DXF | PASS |
| heat-module-tray.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
| heat-module-wall-front | one solid | 1 | PASS |
| heat-module-wall-front | valid B-rep (BRepCheck) | 1 | PASS |
| heat-module-wall-front | closed shells | 1 | PASS |
| heat-module-wall-front | volume positive | 46506.8 | PASS |
| heat-module-wall-front | in the assembly with the same volume and place | True | PASS |
| heat-module-wall-front | section edges all closed | 0 | PASS |
| heat-module-wall-front | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 9 loops, 0 unclassified | PASS |
| heat-module-wall-front | every cut lies inside the outline | 8 | PASS |
| heat-module-wall-front | no two cuts overlap | 0 overlapping pairs | PASS |
| heat-module-wall-front.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| heat-module-wall-front.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 9 matched, 0 only in STEP, 0 only in DXF | PASS |
| heat-module-wall-front.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
| heat-module-wall-left | one solid | 1 | PASS |
| heat-module-wall-left | valid B-rep (BRepCheck) | 1 | PASS |
| heat-module-wall-left | closed shells | 1 | PASS |
| heat-module-wall-left | volume positive | 19709.0 | PASS |
| heat-module-wall-left | in the assembly with the same volume and place | True | PASS |
| heat-module-wall-left | section edges all closed | 0 | PASS |
| heat-module-wall-left | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 8 loops, 0 unclassified | PASS |
| heat-module-wall-left | every cut lies inside the outline | 7 | PASS |
| heat-module-wall-left | no two cuts overlap | 0 overlapping pairs | PASS |
| heat-module-wall-left.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| heat-module-wall-left.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 8 matched, 0 only in STEP, 0 only in DXF | PASS |
| heat-module-wall-left.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
| heat-module-wall-rear | one solid | 1 | PASS |
| heat-module-wall-rear | valid B-rep (BRepCheck) | 1 | PASS |
| heat-module-wall-rear | closed shells | 1 | PASS |
| heat-module-wall-rear | volume positive | 46506.8 | PASS |
| heat-module-wall-rear | in the assembly with the same volume and place | True | PASS |
| heat-module-wall-rear | section edges all closed | 0 | PASS |
| heat-module-wall-rear | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 9 loops, 0 unclassified | PASS |
| heat-module-wall-rear | every cut lies inside the outline | 8 | PASS |
| heat-module-wall-rear | no two cuts overlap | 0 overlapping pairs | PASS |
| heat-module-wall-rear.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| heat-module-wall-rear.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 9 matched, 0 only in STEP, 0 only in DXF | PASS |
| heat-module-wall-rear.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
| heat-module-wall-right | one solid | 1 | PASS |
| heat-module-wall-right | valid B-rep (BRepCheck) | 1 | PASS |
| heat-module-wall-right | closed shells | 1 | PASS |
| heat-module-wall-right | volume positive | 31709.0 | PASS |
| heat-module-wall-right | in the assembly with the same volume and place | True | PASS |
| heat-module-wall-right | section edges all closed | 0 | PASS |
| heat-module-wall-right | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 8 loops, 0 unclassified | PASS |
| heat-module-wall-right | every cut lies inside the outline | 7 | PASS |
| heat-module-wall-right | no two cuts overlap | 0 overlapping pairs | PASS |
| heat-module-wall-right.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| heat-module-wall-right.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 8 matched, 0 only in STEP, 0 only in DXF | PASS |
| heat-module-wall-right.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
| hood-bottom | one solid | 1 | PASS |
| hood-bottom | valid B-rep (BRepCheck) | 1 | PASS |
| hood-bottom | closed shells | 1 | PASS |
| hood-bottom | volume positive | 115600.6 | PASS |
| hood-bottom | in the assembly with the same volume and place | True | PASS |
| hood-bottom | section edges all closed | 0 | PASS |
| hood-bottom | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 12 loops, 0 unclassified | PASS |
| hood-bottom | every cut lies inside the outline | 11 | PASS |
| hood-bottom | no two cuts overlap | 0 overlapping pairs | PASS |
| hood-bottom.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| hood-bottom.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 12 matched, 0 only in STEP, 0 only in DXF | PASS |
| hood-bottom.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
| hood-top | one solid | 1 | PASS |
| hood-top | valid B-rep (BRepCheck) | 1 | PASS |
| hood-top | closed shells | 1 | PASS |
| hood-top | volume positive | 116507.2 | PASS |
| hood-top | in the assembly with the same volume and place | True | PASS |
| hood-top | section edges all closed | 0 | PASS |
| hood-top | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 16 loops, 0 unclassified | PASS |
| hood-top | every cut lies inside the outline | 15 | PASS |
| hood-top | no two cuts overlap | 0 overlapping pairs | PASS |
| hood-top.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| hood-top.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 16 matched, 0 only in STEP, 0 only in DXF | PASS |
| hood-top.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
| liner-splice | one solid | 1 | PASS |
| liner-splice | valid B-rep (BRepCheck) | 1 | PASS |
| liner-splice | closed shells | 1 | PASS |
| liner-splice | volume positive | 2270.8 | PASS |
| liner-splice | in the assembly with the same volume and place | True | PASS |
| liner | one solid | 1 | PASS |
| liner | valid B-rep (BRepCheck) | 1 | PASS |
| liner | closed shells | 1 | PASS |
| liner | volume positive | 91807.6 | PASS |
| liner | in the assembly with the same volume and place | True | PASS |
| lint-box-back | one solid | 1 | PASS |
| lint-box-back | valid B-rep (BRepCheck) | 1 | PASS |
| lint-box-back | closed shells | 1 | PASS |
| lint-box-back | volume positive | 80050.4 | PASS |
| lint-box-back | in the assembly with the same volume and place | True | PASS |
| lint-box-back | section edges all closed | 0 | PASS |
| lint-box-back | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 22 loops, 0 unclassified | PASS |
| lint-box-back | every cut lies inside the outline | 21 | PASS |
| lint-box-back | no two cuts overlap | 0 overlapping pairs | PASS |
| lint-box-back.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| lint-box-back.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 22 matched, 0 only in STEP, 0 only in DXF | PASS |
| lint-box-back.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
| lint-box-front | one solid | 1 | PASS |
| lint-box-front | valid B-rep (BRepCheck) | 1 | PASS |
| lint-box-front | closed shells | 1 | PASS |
| lint-box-front | volume positive | 175620.6 | PASS |
| lint-box-front | in the assembly with the same volume and place | True | PASS |
| lint-box-front | section edges all closed | 0 | PASS |
| lint-box-front | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon (composite outline allowed) | 16 loops, 1 unclassified | PASS |
| lint-box-front | every cut lies inside the outline | 15 | PASS |
| lint-box-front | no two cuts overlap | 0 overlapping pairs | PASS |
| lint-box-front.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| lint-box-front.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 16 matched, 0 only in STEP, 0 only in DXF | PASS |
| lint-box-front.dxf | DXF drawn in world coordinates or about the origin | offset (-0.00, 0.00) | PASS |
| post-1 | one solid | 1 | PASS |
| post-1 | valid B-rep (BRepCheck) | 1 | PASS |
| post-1 | closed shells | 1 | PASS |
| post-1 | volume positive | 1088617.6 | PASS |
| post-1 | in the assembly with the same volume and place | True | PASS |
| post-2 | one solid | 1 | PASS |
| post-2 | valid B-rep (BRepCheck) | 1 | PASS |
| post-2 | closed shells | 1 | PASS |
| post-2 | volume positive | 1088617.6 | PASS |
| post-2 | in the assembly with the same volume and place | True | PASS |
| post-3 | one solid | 1 | PASS |
| post-3 | valid B-rep (BRepCheck) | 1 | PASS |
| post-3 | closed shells | 1 | PASS |
| post-3 | volume positive | 1088617.6 | PASS |
| post-3 | in the assembly with the same volume and place | True | PASS |
| post-4 | one solid | 1 | PASS |
| post-4 | valid B-rep (BRepCheck) | 1 | PASS |
| post-4 | closed shells | 1 | PASS |
| post-4 | volume positive | 1088617.6 | PASS |
| post-4 | in the assembly with the same volume and place | True | PASS |
| power-module-barrier | one solid | 1 | PASS |
| power-module-barrier | valid B-rep (BRepCheck) | 1 | PASS |
| power-module-barrier | closed shells | 1 | PASS |
| power-module-barrier | volume positive | 16928.2 | PASS |
| power-module-barrier | in the assembly with the same volume and place | True | PASS |
| power-module-barrier | section edges all closed | 0 | PASS |
| power-module-barrier | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 3 loops, 0 unclassified | PASS |
| power-module-barrier | every cut lies inside the outline | 2 | PASS |
| power-module-barrier | no two cuts overlap | 0 overlapping pairs | PASS |
| power-module-barrier.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| power-module-barrier.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 3 matched, 0 only in STEP, 0 only in DXF | PASS |
| power-module-barrier.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
| power-module-cover | one solid | 1 | PASS |
| power-module-cover | valid B-rep (BRepCheck) | 1 | PASS |
| power-module-cover | closed shells | 1 | PASS |
| power-module-cover | volume positive | 74108.2 | PASS |
| power-module-cover | in the assembly with the same volume and place | True | PASS |
| power-module-cover | section edges all closed | 0 | PASS |
| power-module-cover | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 5 loops, 0 unclassified | PASS |
| power-module-cover | every cut lies inside the outline | 4 | PASS |
| power-module-cover | no two cuts overlap | 0 overlapping pairs | PASS |
| power-module-cover.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| power-module-cover.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 5 matched, 0 only in STEP, 0 only in DXF | PASS |
| power-module-cover.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
| power-module-plate | one solid | 1 | PASS |
| power-module-plate | valid B-rep (BRepCheck) | 1 | PASS |
| power-module-plate | closed shells | 1 | PASS |
| power-module-plate | volume positive | 161321.5 | PASS |
| power-module-plate | in the assembly with the same volume and place | True | PASS |
| power-module-plate | section edges all closed | 0 | PASS |
| power-module-plate | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 22 loops, 0 unclassified | PASS |
| power-module-plate | every cut lies inside the outline | 21 | PASS |
| power-module-plate | no two cuts overlap | 0 overlapping pairs | PASS |
| power-module-plate.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| power-module-plate.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 22 matched, 0 only in STEP, 0 only in DXF | PASS |
| power-module-plate.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
| rail-bottom-front | one solid | 1 | PASS |
| rail-bottom-front | valid B-rep (BRepCheck) | 1 | PASS |
| rail-bottom-front | closed shells | 1 | PASS |
| rail-bottom-front | volume positive | 664056.7 | PASS |
| rail-bottom-front | in the assembly with the same volume and place | True | PASS |
| rail-bottom-left | one solid | 1 | PASS |
| rail-bottom-left | valid B-rep (BRepCheck) | 1 | PASS |
| rail-bottom-left | closed shells | 1 | PASS |
| rail-bottom-left | volume positive | 729373.8 | PASS |
| rail-bottom-left | in the assembly with the same volume and place | True | PASS |
| rail-bottom-rear | one solid | 1 | PASS |
| rail-bottom-rear | valid B-rep (BRepCheck) | 1 | PASS |
| rail-bottom-rear | closed shells | 1 | PASS |
| rail-bottom-rear | volume positive | 664056.7 | PASS |
| rail-bottom-rear | in the assembly with the same volume and place | True | PASS |
| rail-bottom-right | one solid | 1 | PASS |
| rail-bottom-right | valid B-rep (BRepCheck) | 1 | PASS |
| rail-bottom-right | closed shells | 1 | PASS |
| rail-bottom-right | volume positive | 729373.8 | PASS |
| rail-bottom-right | in the assembly with the same volume and place | True | PASS |
| rail-mid-front-left | one solid | 1 | PASS |
| rail-mid-front-left | valid B-rep (BRepCheck) | 1 | PASS |
| rail-mid-front-left | closed shells | 1 | PASS |
| rail-mid-front-left | volume positive | 146963.4 | PASS |
| rail-mid-front-left | in the assembly with the same volume and place | True | PASS |
| rail-mid-front-right | one solid | 1 | PASS |
| rail-mid-front-right | valid B-rep (BRepCheck) | 1 | PASS |
| rail-mid-front-right | closed shells | 1 | PASS |
| rail-mid-front-right | volume positive | 146963.4 | PASS |
| rail-mid-front-right | in the assembly with the same volume and place | True | PASS |
| rail-mid-left | one solid | 1 | PASS |
| rail-mid-left | valid B-rep (BRepCheck) | 1 | PASS |
| rail-mid-left | closed shells | 1 | PASS |
| rail-mid-left | volume positive | 729373.8 | PASS |
| rail-mid-left | in the assembly with the same volume and place | True | PASS |
| rail-mid-rear | one solid | 1 | PASS |
| rail-mid-rear | valid B-rep (BRepCheck) | 1 | PASS |
| rail-mid-rear | closed shells | 1 | PASS |
| rail-mid-rear | volume positive | 664056.7 | PASS |
| rail-mid-rear | in the assembly with the same volume and place | True | PASS |
| rail-mid-rearcross | one solid | 1 | PASS |
| rail-mid-rearcross | valid B-rep (BRepCheck) | 1 | PASS |
| rail-mid-rearcross | closed shells | 1 | PASS |
| rail-mid-rearcross | volume positive | 664056.7 | PASS |
| rail-mid-rearcross | in the assembly with the same volume and place | True | PASS |
| rail-mid-right | one solid | 1 | PASS |
| rail-mid-right | valid B-rep (BRepCheck) | 1 | PASS |
| rail-mid-right | closed shells | 1 | PASS |
| rail-mid-right | volume positive | 729373.8 | PASS |
| rail-mid-right | in the assembly with the same volume and place | True | PASS |
| rail-top-front | one solid | 1 | PASS |
| rail-top-front | valid B-rep (BRepCheck) | 1 | PASS |
| rail-top-front | closed shells | 1 | PASS |
| rail-top-front | volume positive | 664056.7 | PASS |
| rail-top-front | in the assembly with the same volume and place | True | PASS |
| rail-top-left | one solid | 1 | PASS |
| rail-top-left | valid B-rep (BRepCheck) | 1 | PASS |
| rail-top-left | closed shells | 1 | PASS |
| rail-top-left | volume positive | 729373.8 | PASS |
| rail-top-left | in the assembly with the same volume and place | True | PASS |
| rail-top-rear | one solid | 1 | PASS |
| rail-top-rear | valid B-rep (BRepCheck) | 1 | PASS |
| rail-top-rear | closed shells | 1 | PASS |
| rail-top-rear | volume positive | 664056.7 | PASS |
| rail-top-rear | in the assembly with the same volume and place | True | PASS |
| rail-top-rearcross | one solid | 1 | PASS |
| rail-top-rearcross | valid B-rep (BRepCheck) | 1 | PASS |
| rail-top-rearcross | closed shells | 1 | PASS |
| rail-top-rearcross | volume positive | 664056.7 | PASS |
| rail-top-rearcross | in the assembly with the same volume and place | True | PASS |
| rail-top-right | one solid | 1 | PASS |
| rail-top-right | valid B-rep (BRepCheck) | 1 | PASS |
| rail-top-right | closed shells | 1 | PASS |
| rail-top-right | volume positive | 729373.8 | PASS |
| rail-top-right | in the assembly with the same volume and place | True | PASS |
| rear-bulkhead | one solid | 1 | PASS |
| rear-bulkhead | valid B-rep (BRepCheck) | 1 | PASS |
| rear-bulkhead | closed shells | 1 | PASS |
| rear-bulkhead | volume positive | 652057.6 | PASS |
| rear-bulkhead | in the assembly with the same volume and place | True | PASS |
| rear-bulkhead | section edges all closed | 0 | PASS |
| rear-bulkhead | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 153 loops, 0 unclassified | PASS |
| rear-bulkhead | every cut lies inside the outline | 152 | PASS |
| rear-bulkhead | no two cuts overlap | 0 overlapping pairs | PASS |
| rear-bulkhead.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| rear-bulkhead.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 153 matched, 0 only in STEP, 0 only in DXF | PASS |
| rear-bulkhead.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
| rear-lower-panel | one solid | 1 | PASS |
| rear-lower-panel | valid B-rep (BRepCheck) | 1 | PASS |
| rear-lower-panel | closed shells | 1 | PASS |
| rear-lower-panel | volume positive | 238937.9 | PASS |
| rear-lower-panel | in the assembly with the same volume and place | True | PASS |
| rear-lower-panel | section edges all closed | 0 | PASS |
| rear-lower-panel | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 48 loops, 0 unclassified | PASS |
| rear-lower-panel | every cut lies inside the outline | 47 | PASS |
| rear-lower-panel | no two cuts overlap | 0 overlapping pairs | PASS |
| rear-lower-panel.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| rear-lower-panel.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 48 matched, 0 only in STEP, 0 only in DXF | PASS |
| rear-lower-panel.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
| rear-upper-panel | one solid | 1 | PASS |
| rear-upper-panel | valid B-rep (BRepCheck) | 1 | PASS |
| rear-upper-panel | closed shells | 1 | PASS |
| rear-upper-panel | volume positive | 764957.7 | PASS |
| rear-upper-panel | in the assembly with the same volume and place | True | PASS |
| rear-upper-panel | section edges all closed | 0 | PASS |
| rear-upper-panel | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 19 loops, 0 unclassified | PASS |
| rear-upper-panel | every cut lies inside the outline | 18 | PASS |
| rear-upper-panel | no two cuts overlap | 0 overlapping pairs | PASS |
| rear-upper-panel.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| rear-upper-panel.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 19 matched, 0 only in STEP, 0 only in DXF | PASS |
| rear-upper-panel.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
| side-panel-left | one solid | 1 | PASS |
| side-panel-left | valid B-rep (BRepCheck) | 1 | PASS |
| side-panel-left | closed shells | 1 | PASS |
| side-panel-left | volume positive | 1123510.2 | PASS |
| side-panel-left | in the assembly with the same volume and place | True | PASS |
| side-panel-left | section edges all closed | 0 | PASS |
| side-panel-left | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 30 loops, 0 unclassified | PASS |
| side-panel-left | every cut lies inside the outline | 29 | PASS |
| side-panel-left | no two cuts overlap | 0 overlapping pairs | PASS |
| side-panel-left.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| side-panel-left.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 30 matched, 0 only in STEP, 0 only in DXF | PASS |
| side-panel-left.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
| side-panel-right | one solid | 1 | PASS |
| side-panel-right | valid B-rep (BRepCheck) | 1 | PASS |
| side-panel-right | closed shells | 1 | PASS |
| side-panel-right | volume positive | 1123510.2 | PASS |
| side-panel-right | in the assembly with the same volume and place | True | PASS |
| side-panel-right | section edges all closed | 0 | PASS |
| side-panel-right | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 30 loops, 0 unclassified | PASS |
| side-panel-right | every cut lies inside the outline | 29 | PASS |
| side-panel-right | no two cuts overlap | 0 overlapping pairs | PASS |
| side-panel-right.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| side-panel-right.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 30 matched, 0 only in STEP, 0 only in DXF | PASS |
| side-panel-right.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
| tier0-faceplate | one solid | 1 | PASS |
| tier0-faceplate | valid B-rep (BRepCheck) | 1 | PASS |
| tier0-faceplate | closed shells | 1 | PASS |
| tier0-faceplate | volume positive | 195756.6 | PASS |
| tier0-faceplate | in the assembly with the same volume and place | True | PASS |
| tier0-faceplate | section edges all closed | 0 | PASS |
| tier0-faceplate | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 19 loops, 0 unclassified | PASS |
| tier0-faceplate | every cut lies inside the outline | 18 | PASS |
| tier0-faceplate | no two cuts overlap | 0 overlapping pairs | PASS |
| tier0-faceplate.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| tier0-faceplate.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 19 matched, 0 only in STEP, 0 only in DXF | PASS |
| tier0-faceplate.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 1084.50) | PASS |
| top-panel | one solid | 1 | PASS |
| top-panel | valid B-rep (BRepCheck) | 1 | PASS |
| top-panel | closed shells | 1 | PASS |
| top-panel | volume positive | 774638.0 | PASS |
| top-panel | in the assembly with the same volume and place | True | PASS |
| top-panel | section edges all closed | 0 | PASS |
| top-panel | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 22 loops, 0 unclassified | PASS |
| top-panel | every cut lies inside the outline | 21 | PASS |
| top-panel | no two cuts overlap | 0 overlapping pairs | PASS |
| top-panel.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| top-panel.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 22 matched, 0 only in STEP, 0 only in DXF | PASS |
| top-panel.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
| tray-rail-1 | one solid | 1 | PASS |
| tray-rail-1 | valid B-rep (BRepCheck) | 1 | PASS |
| tray-rail-1 | closed shells | 1 | PASS |
| tray-rail-1 | volume positive | 151936.6 | PASS |
| tray-rail-1 | in the assembly with the same volume and place | True | PASS |
| tray-rail-2 | one solid | 1 | PASS |
| tray-rail-2 | valid B-rep (BRepCheck) | 1 | PASS |
| tray-rail-2 | closed shells | 1 | PASS |
| tray-rail-2 | volume positive | 151936.6 | PASS |
| tray-rail-2 | in the assembly with the same volume and place | True | PASS |
| trunk-front | one solid | 1 | PASS |
| trunk-front | valid B-rep (BRepCheck) | 1 | PASS |
| trunk-front | closed shells | 1 | PASS |
| trunk-front | volume positive | 177913.9 | PASS |
| trunk-front | in the assembly with the same volume and place | True | PASS |
| trunk-front | section edges all closed | 0 | PASS |
| trunk-front | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 25 loops, 0 unclassified | PASS |
| trunk-front | every cut lies inside the outline | 24 | PASS |
| trunk-front | no two cuts overlap | 0 overlapping pairs | PASS |
| trunk-front.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| trunk-front.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 25 matched, 0 only in STEP, 0 only in DXF | PASS |
| trunk-front.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
| trunk-rear | one solid | 1 | PASS |
| trunk-rear | valid B-rep (BRepCheck) | 1 | PASS |
| trunk-rear | closed shells | 1 | PASS |
| trunk-rear | volume positive | 223308.5 | PASS |
| trunk-rear | in the assembly with the same volume and place | True | PASS |
| trunk-rear | section edges all closed | 0 | PASS |
| trunk-rear | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 14 loops, 0 unclassified | PASS |
| trunk-rear | every cut lies inside the outline | 13 | PASS |
| trunk-rear | no two cuts overlap | 0 overlapping pairs | PASS |
| trunk-rear.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| trunk-rear.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 14 matched, 0 only in STEP, 0 only in DXF | PASS |
| trunk-rear.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
| side-panel-left | every M6 hole sits on a frame rail centre line (or is a listed through-bolted hole) | 29 M6 holes, 0 through-bolted, 0 off a rail | PASS |
| side-panel-right | every M6 hole sits on a frame rail centre line (or is a listed through-bolted hole) | 29 M6 holes, 0 through-bolted, 0 off a rail | PASS |
| front-upper-panel | every M6 hole sits on a frame rail centre line (or is a listed through-bolted hole) | 18 M6 holes, 2 through-bolted, 0 off a rail | PASS |
| front-lower-panel | every M6 hole sits on a frame rail centre line (or is a listed through-bolted hole) | 8 M6 holes, 0 through-bolted, 0 off a rail | PASS |
| rear-upper-panel | every M6 hole sits on a frame rail centre line (or is a listed through-bolted hole) | 18 M6 holes, 0 through-bolted, 0 off a rail | PASS |
| rear-lower-panel | every M6 hole sits on a frame rail centre line (or is a listed through-bolted hole) | 8 M6 holes, 0 through-bolted, 0 off a rail | PASS |
| top-panel | every M6 hole sits on a frame rail centre line (or is a listed through-bolted hole) | 20 M6 holes, 0 through-bolted, 0 off a rail | PASS |
| base-pan | every M6 hole sits on a frame rail centre line (or is a listed through-bolted hole) | 34 M6 holes, 14 through-bolted, 0 off a rail | PASS |
| bay-ceiling | every M6 hole sits on a frame rail centre line (or is a listed through-bolted hole) | 20 M6 holes, 0 through-bolted, 0 off a rail | PASS |
| front-bulkhead | every M6 hole sits on a frame rail centre line (or is a listed through-bolted hole) | 7 M6 holes, 0 through-bolted, 0 off a rail | PASS |
| rear-bulkhead | every M6 hole sits on a frame rail centre line (or is a listed through-bolted hole) | 10 M6 holes, 0 through-bolted, 0 off a rail | PASS |
| console-face | every M6 hole sits on a frame rail centre line (or is a listed through-bolted hole) | 8 M6 holes, 0 through-bolted, 0 off a rail | PASS |
| console-rear | every M6 hole sits on a frame rail centre line (or is a listed through-bolted hole) | 8 M6 holes, 0 through-bolted, 0 off a rail | PASS |
| console-cap | every M6 hole sits on a frame rail centre line (or is a listed through-bolted hole) | 10 M6 holes, 0 through-bolted, 0 off a rail | PASS |
| console-cheek-left | every M6 hole sits on a frame rail centre line (or is a listed through-bolted hole) | 5 M6 holes, 0 through-bolted, 0 off a rail | PASS |
| console-cheek-right | every M6 hole sits on a frame rail centre line (or is a listed through-bolted hole) | 5 M6 holes, 0 through-bolted, 0 off a rail | PASS |
| power-module-plate | every M6 hole sits on a frame rail centre line (or is a listed through-bolted hole) | 4 M6 holes, 0 through-bolted, 0 off a rail | PASS |
| console-face | the only M4 holes are the six UCI-D module holes (uci-spec 4.1, draft 5) | 6 M4 holes | PASS |
| all parts | V-011: every round feature deeper than 0.5 mm has a diameter on the named list (3 M3 tapped (basket plates), 3.4 M3 clearance (liner, basket clamps), 4 4040 corner radius 2 / timer yoke holes, 4.2 2020 centre bore / M4 tapped in the duct bars, drawn at the thread, 4.5 M4 clearance, 5 louver slot ends (60 x 5), 6 corner radius 3 (cheeks, tabs, splice, idler arm ends), 6.5 M6 clearance / air-proving tap in the exhaust pipe, 6.6 M6 bonding studs (nutted), 6.8 4040 centre bore (tapped M8 for the feet), 8 door switch plunger, 8.5 M8 clearance (feet studs, roller studs) / door switch plunger hole, 10 inlet holes / D-pull bar, 12 plate corner radius 6 / timer shaft holes / lint box hang spacers, 16 door switch cable and moisture pair grommets (draft 9) / moisture bar terminals, 20 condensate drain (hose grommet) / faceplate corner radius 10, 22 cord strain relief bushing, cord and console grommets, 22.3 22 mm panel devices, 25 gas entry (3/8 NPT bulkhead fitting), 30 bay harness grommet, 40 lint slot ends (260 x 40), 106 exhaust port (102 duct + 2 each side), 126 collar opening (125 collar + 1), 128 hood collar hole (125 collar + 3), 141 motor cradle saddle (140 motor + 1), 460 door opening, 464 basket lip inside (radius 232), 467.8 basket lip flange inside (radius 233.9), 468 liner splice inside (radius 234), 470 door ring bore, 471 liner inside (radius 235.5), 474 liner outside (radius 237), 474.4 lint box plates and bars follow the liner (radius 237.2), 476 lint slot inner arc (radius 238), 477.8 basket mesh inside (radius 238.9), 479 basket plates inside (radius 239.5), 480 front panel ring opening, 489 basket far flange inside (radius 244.5), 521 basket far flange outside (radius 260.5), 531 basket plates outside (radius 265.5), 532.2 basket mesh outside (radius 266.1), 534 lint slot outer arc (radius 267, draft 8), 537 basket lip outside (radius 268.5), 540 door disc / drum ring bore, 546 felt seal inside (radius 273), 560 door ring, 582 felt seal outside (radius 291), 616.4 splice inside, 618.4 drum ring / sheet inside, 620 drum outside) | 0 off the list | PASS |
| air path | V-013: every opening in the air path is at least the blower outlet (102 round, 8171 mm2) | module_inlet 9000, module_collar 12037, hood 8350, trunk 12200, nozzle 30104, inlet_field 9896, lint_slot 9202, basket_outer_wall 9294, lint_box 9480, spool 16800, exhaust_duct 8171 | PASS |
| assembly | no two solids overlap by more than 1 mm3 (file re-import, boolean and point sample) | 213 solids, 0 overlaps | PASS |
| assembly | every part file is a named solid in the assembly | 0 missing | PASS |
| drum-sheet.dxf | every hole in the rolled solid unwraps onto a hole in the flat pattern (0.05 mm) | 88 matched, 0 solid-only, 0 DXF-only | PASS |
| drum-sheet.dxf | flat pattern outline is the sheet's unrolled mid-surface length by its length plus the tabs | rpoly 1945.274 x 582.000, 244 edges; unrolled 1945.274 | PASS |
| drum-splice.dxf | every hole in the curved splice unwraps onto a hole in the flat strip (0.05 mm) | 16 matched, 0 solid-only, 0 DXF-only | PASS |
| drum-splice.dxf | flat strip outline equals the curved strip's arc length by its length | 60.000 x 544.000; arc 60.010 x 544.000 | PASS |
| liner.dxf | flat pattern outline is the rolled part's mid-surface arc length by its width | 1482.403 x 41.300; arc 1482.403 x 41.300 | PASS |
| liner.dxf | two M3 holes in the solid and the flat pattern, 3 degrees each side of the seam at the top | 2 in the solid at 87.0 deg, 93.0 deg; 2 in the DXF | PASS |
| liner-splice.dxf | flat pattern outline is the rolled part's mid-surface arc length by its width | 40.000 x 38.300; arc 40.000 x 38.300 | PASS |
| liner-splice.dxf | two M3 holes in the solid and the flat pattern, 3 degrees each side of the seam at the top | 2 in the solid at 87.0 deg, 93.0 deg; 2 in the DXF | PASS |

## 3. The same files measured inside Autodesk Fusion

Fusion record: `fusion-measured.csv`, written by `fusion_audit.py` running inside Fusion. CHECK means the two kernels count faces differently (Fusion may split or merge periodic faces); it is not a geometry difference.

| file | body | comparison | values | result |
|---|---|---|---|---|
| base-pan | Body1 | volume (mm3) | OCP 770130.214 / Fusion 770130.214 | PASS |
| base-pan | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| base-pan | Body1 | face count | OCP 53 / Fusion 53 | PASS |
| base-pan | Body1 | solid body | 1 | PASS |
| basket-far-clamp | Body1 | volume (mm3) | OCP 12155.524 / Fusion 12155.524 | PASS |
| basket-far-clamp | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| basket-far-clamp | Body1 | face count | OCP 12 / Fusion 12 | PASS |
| basket-far-clamp | Body1 | solid body | 1 | PASS |
| basket-far-plate | Body1 | volume (mm3) | OCP 24347.238 / Fusion 24347.238 | PASS |
| basket-far-plate | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| basket-far-plate | Body1 | face count | OCP 12 / Fusion 12 | PASS |
| basket-far-plate | Body1 | solid body | 1 | PASS |
| basket-lip-clamp | Body1 | volume (mm3) | OCP 5002.108 / Fusion 5002.108 | PASS |
| basket-lip-clamp | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| basket-lip-clamp | Body1 | face count | OCP 16 / Fusion 16 | PASS |
| basket-lip-clamp | Body1 | solid body | 1 | PASS |
| basket-lip-plate | Body1 | volume (mm3) | OCP 14075.046 / Fusion 14075.046 | PASS |
| basket-lip-plate | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| basket-lip-plate | Body1 | face count | OCP 24 / Fusion 24 | PASS |
| basket-lip-plate | Body1 | solid body | 1 | PASS |
| bay-ceiling | Body1 | volume (mm3) | OCP 685439.751 / Fusion 685439.751 | PASS |
| bay-ceiling | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| bay-ceiling | Body1 | face count | OCP 55 / Fusion 55 | PASS |
| bay-ceiling | Body1 | solid body | 1 | PASS |
| blower-plate | Body1 | volume (mm3) | OCP 70112.794 / Fusion 70112.794 | PASS |
| blower-plate | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| blower-plate | Body1 | face count | OCP 22 / Fusion 22 | PASS |
| blower-plate | Body1 | solid body | 1 | PASS |
| console-cap | Body1 | volume (mm3) | OCP 146545.150 / Fusion 146545.150 | PASS |
| console-cap | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| console-cap | Body1 | face count | OCP 20 / Fusion 20 | PASS |
| console-cap | Body1 | solid body | 1 | PASS |
| console-cheek-left | Body1 | volume (mm3) | OCP 42473.148 / Fusion 42473.148 | PASS |
| console-cheek-left | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| console-cheek-left | Body1 | face count | OCP 15 / Fusion 15 | PASS |
| console-cheek-left | Body1 | solid body | 1 | PASS |
| console-cheek-right | Body1 | volume (mm3) | OCP 42473.148 / Fusion 42473.148 | PASS |
| console-cheek-right | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| console-cheek-right | Body1 | face count | OCP 15 / Fusion 15 | PASS |
| console-cheek-right | Body1 | solid body | 1 | PASS |
| console-face | Body1 | volume (mm3) | OCP 105612.310 / Fusion 105612.310 | PASS |
| console-face | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| console-face | Body1 | face count | OCP 28 / Fusion 28 | PASS |
| console-face | Body1 | solid body | 1 | PASS |
| console-post-1 | Body1 | volume (mm3) | OCP 217723.512 / Fusion 217723.512 | PASS |
| console-post-1 | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| console-post-1 | Body1 | face count | OCP 59 / Fusion 59 | PASS |
| console-post-1 | Body1 | solid body | 1 | PASS |
| console-post-2 | Body1 | volume (mm3) | OCP 217723.512 / Fusion 217723.512 | PASS |
| console-post-2 | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| console-post-2 | Body1 | face count | OCP 59 / Fusion 59 | PASS |
| console-post-2 | Body1 | solid body | 1 | PASS |
| console-post-3 | Body1 | volume (mm3) | OCP 217723.512 / Fusion 217723.512 | PASS |
| console-post-3 | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| console-post-3 | Body1 | face count | OCP 59 / Fusion 59 | PASS |
| console-post-3 | Body1 | solid body | 1 | PASS |
| console-post-4 | Body1 | volume (mm3) | OCP 217723.512 / Fusion 217723.512 | PASS |
| console-post-4 | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| console-post-4 | Body1 | face count | OCP 59 / Fusion 59 | PASS |
| console-post-4 | Body1 | solid body | 1 | PASS |
| console-rail-front | Body1 | volume (mm3) | OCP 664056.711 / Fusion 664056.711 | PASS |
| console-rail-front | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| console-rail-front | Body1 | face count | OCP 59 / Fusion 59 | PASS |
| console-rail-front | Body1 | solid body | 1 | PASS |
| console-rail-left | Body1 | volume (mm3) | OCP 63684.127 / Fusion 63684.127 | PASS |
| console-rail-left | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| console-rail-left | Body1 | face count | OCP 59 / Fusion 59 | PASS |
| console-rail-left | Body1 | solid body | 1 | PASS |
| console-rail-rear | Body1 | volume (mm3) | OCP 664056.711 / Fusion 664056.711 | PASS |
| console-rail-rear | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| console-rail-rear | Body1 | face count | OCP 59 / Fusion 59 | PASS |
| console-rail-rear | Body1 | solid body | 1 | PASS |
| console-rail-right | Body1 | volume (mm3) | OCP 63684.127 / Fusion 63684.127 | PASS |
| console-rail-right | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| console-rail-right | Body1 | face count | OCP 59 / Fusion 59 | PASS |
| console-rail-right | Body1 | solid body | 1 | PASS |
| console-rear | Body1 | volume (mm3) | OCP 208107.949 / Fusion 208107.949 | PASS |
| console-rear | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| console-rear | Body1 | face count | OCP 18 / Fusion 18 | PASS |
| console-rear | Body1 | solid body | 1 | PASS |
| door-disc | Body1 | volume (mm3) | OCP 457916.974 / Fusion 457916.974 | PASS |
| door-disc | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| door-disc | Body1 | face count | OCP 7 / Fusion 7 | PASS |
| door-disc | Body1 | solid body | 1 | PASS |
| door-ring | Body1 | volume (mm3) | OCP 145112.128 / Fusion 145112.128 | PASS |
| door-ring | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| door-ring | Body1 | face count | OCP 15 / Fusion 15 | PASS |
| door-ring | Body1 | solid body | 1 | PASS |
| drum-ring-front | Body1 | volume (mm3) | OCP 141703.202 / Fusion 141703.202 | PASS |
| drum-ring-front | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| drum-ring-front | Body1 | face count | OCP 34 / Fusion 34 | PASS |
| drum-ring-front | Body1 | solid body | 1 | PASS |
| drum-ring-rear | Body1 | volume (mm3) | OCP 141703.202 / Fusion 141703.202 | PASS |
| drum-ring-rear | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| drum-ring-rear | Body1 | face count | OCP 34 / Fusion 34 | PASS |
| drum-ring-rear | Body1 | solid body | 1 | PASS |
| drum-sheet | Body1 | volume (mm3) | OCP 873714.067 / Fusion 873712.681 | PASS |
| drum-sheet | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| drum-sheet | Body1 | face count | OCP 600 / Fusion 570 | CHECK |
| drum-sheet | Body1 | solid body | 1 | PASS |
| drum-splice | Body1 | volume (mm3) | OCP 32383.401 / Fusion 32384.592 | PASS |
| drum-splice | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| drum-splice | Body1 | face count | OCP 26 / Fusion 26 | PASS |
| drum-splice | Body1 | solid body | 1 | PASS |
| entry-blank | Body1 | volume (mm3) | OCP 3865.933 / Fusion 3865.933 | PASS |
| entry-blank | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| entry-blank | Body1 | face count | OCP 12 / Fusion 12 | PASS |
| entry-blank | Body1 | solid body | 1 | PASS |
| felt-seal-front-long | Body1 | volume (mm3) | OCP 184592.692 / Fusion 184592.692 | PASS |
| felt-seal-front-long | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| felt-seal-front-long | Body1 | face count | OCP 6 / Fusion 6 | PASS |
| felt-seal-front-long | Body1 | solid body | 1 | PASS |
| felt-seal-front-short | Body1 | volume (mm3) | OCP 57018.897 / Fusion 57018.897 | PASS |
| felt-seal-front-short | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| felt-seal-front-short | Body1 | face count | OCP 6 / Fusion 6 | PASS |
| felt-seal-front-short | Body1 | solid body | 1 | PASS |
| felt-seal-rear-long | Body1 | volume (mm3) | OCP 230740.865 / Fusion 230740.865 | PASS |
| felt-seal-rear-long | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| felt-seal-rear-long | Body1 | face count | OCP 6 / Fusion 6 | PASS |
| felt-seal-rear-long | Body1 | solid body | 1 | PASS |
| felt-seal-rear-short | Body1 | volume (mm3) | OCP 71273.622 / Fusion 71273.621 | PASS |
| felt-seal-rear-short | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| felt-seal-rear-short | Body1 | face count | OCP 6 / Fusion 6 | PASS |
| felt-seal-rear-short | Body1 | solid body | 1 | PASS |
| front-bulkhead | Body1 | volume (mm3) | OCP 403407.561 / Fusion 403407.561 | PASS |
| front-bulkhead | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| front-bulkhead | Body1 | face count | OCP 38 / Fusion 38 | PASS |
| front-bulkhead | Body1 | solid body | 1 | PASS |
| front-lower-panel | Body1 | volume (mm3) | OCP 242871.113 / Fusion 242871.113 | PASS |
| front-lower-panel | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| front-lower-panel | Body1 | face count | OCP 242 / Fusion 242 | PASS |
| front-lower-panel | Body1 | solid body | 1 | PASS |
| front-upper-panel | Body1 | volume (mm3) | OCP 493200.416 / Fusion 493200.416 | PASS |
| front-upper-panel | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| front-upper-panel | Body1 | face count | OCP 40 / Fusion 40 | PASS |
| front-upper-panel | Body1 | solid body | 1 | PASS |
| heat-module-terminal-plate | Body1 | volume (mm3) | OCP 43369.129 / Fusion 43369.129 | PASS |
| heat-module-terminal-plate | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| heat-module-terminal-plate | Body1 | face count | OCP 15 / Fusion 15 | PASS |
| heat-module-terminal-plate | Body1 | solid body | 1 | PASS |
| heat-module-top | Body1 | volume (mm3) | OCP 70030.523 / Fusion 70030.523 | PASS |
| heat-module-top | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| heat-module-top | Body1 | face count | OCP 29 / Fusion 29 | PASS |
| heat-module-top | Body1 | solid body | 1 | PASS |
| heat-module-tray | Body1 | volume (mm3) | OCP 142392.194 / Fusion 142392.194 | PASS |
| heat-module-tray | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| heat-module-tray | Body1 | face count | OCP 24 / Fusion 24 | PASS |
| heat-module-tray | Body1 | solid body | 1 | PASS |
| heat-module-wall-front | Body1 | volume (mm3) | OCP 46506.810 / Fusion 46506.810 | PASS |
| heat-module-wall-front | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| heat-module-wall-front | Body1 | face count | OCP 18 / Fusion 18 | PASS |
| heat-module-wall-front | Body1 | solid body | 1 | PASS |
| heat-module-wall-left | Body1 | volume (mm3) | OCP 19709.023 / Fusion 19709.023 | PASS |
| heat-module-wall-left | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| heat-module-wall-left | Body1 | face count | OCP 20 / Fusion 20 | PASS |
| heat-module-wall-left | Body1 | solid body | 1 | PASS |
| heat-module-wall-rear | Body1 | volume (mm3) | OCP 46506.810 / Fusion 46506.810 | PASS |
| heat-module-wall-rear | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| heat-module-wall-rear | Body1 | face count | OCP 18 / Fusion 18 | PASS |
| heat-module-wall-rear | Body1 | solid body | 1 | PASS |
| heat-module-wall-right | Body1 | volume (mm3) | OCP 31709.023 / Fusion 31709.023 | PASS |
| heat-module-wall-right | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| heat-module-wall-right | Body1 | face count | OCP 20 / Fusion 20 | PASS |
| heat-module-wall-right | Body1 | solid body | 1 | PASS |
| hood-bottom | Body1 | volume (mm3) | OCP 115600.636 / Fusion 115600.636 | PASS |
| hood-bottom | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| hood-bottom | Body1 | face count | OCP 21 / Fusion 21 | PASS |
| hood-bottom | Body1 | solid body | 1 | PASS |
| hood-top | Body1 | volume (mm3) | OCP 116507.155 / Fusion 116507.155 | PASS |
| hood-top | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| hood-top | Body1 | face count | OCP 28 / Fusion 28 | PASS |
| hood-top | Body1 | solid body | 1 | PASS |
| liner-splice | Body1 | volume (mm3) | OCP 2270.762 / Fusion 2270.749 | PASS |
| liner-splice | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| liner-splice | Body1 | face count | OCP 8 / Fusion 8 | PASS |
| liner-splice | Body1 | solid body | 1 | PASS |
| liner | Body1 | volume (mm3) | OCP 91807.599 / Fusion 91807.543 | PASS |
| liner | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| liner | Body1 | face count | OCP 10 / Fusion 8 | CHECK |
| liner | Body1 | solid body | 1 | PASS |
| lint-box-back | Body1 | volume (mm3) | OCP 80050.373 / Fusion 80050.373 | PASS |
| lint-box-back | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| lint-box-back | Body1 | face count | OCP 37 / Fusion 37 | PASS |
| lint-box-back | Body1 | solid body | 1 | PASS |
| lint-box-front | Body1 | volume (mm3) | OCP 175620.605 / Fusion 175620.605 | PASS |
| lint-box-front | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| lint-box-front | Body1 | face count | OCP 23 / Fusion 23 | PASS |
| lint-box-front | Body1 | solid body | 1 | PASS |
| osa-dryer-assembly | post-1 | volume (mm3) | OCP 1088617.560 / Fusion 1088617.559 | PASS |
| osa-dryer-assembly | post-1 | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | post-1 | solid body | 1 | PASS |
| osa-dryer-assembly | post-2 | volume (mm3) | OCP 1088617.560 / Fusion 1088617.559 | PASS |
| osa-dryer-assembly | post-2 | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | post-2 | solid body | 1 | PASS |
| osa-dryer-assembly | post-3 | volume (mm3) | OCP 1088617.560 / Fusion 1088617.559 | PASS |
| osa-dryer-assembly | post-3 | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | post-3 | solid body | 1 | PASS |
| osa-dryer-assembly | post-4 | volume (mm3) | OCP 1088617.560 / Fusion 1088617.559 | PASS |
| osa-dryer-assembly | post-4 | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | post-4 | solid body | 1 | PASS |
| osa-dryer-assembly | rail-bottom-front | volume (mm3) | OCP 664056.711 / Fusion 664056.711 | PASS |
| osa-dryer-assembly | rail-bottom-front | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | rail-bottom-front | solid body | 1 | PASS |
| osa-dryer-assembly | rail-bottom-rear | volume (mm3) | OCP 664056.711 / Fusion 664056.711 | PASS |
| osa-dryer-assembly | rail-bottom-rear | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | rail-bottom-rear | solid body | 1 | PASS |
| osa-dryer-assembly | rail-bottom-left | volume (mm3) | OCP 729373.765 / Fusion 729373.765 | PASS |
| osa-dryer-assembly | rail-bottom-left | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | rail-bottom-left | solid body | 1 | PASS |
| osa-dryer-assembly | rail-bottom-right | volume (mm3) | OCP 729373.765 / Fusion 729373.765 | PASS |
| osa-dryer-assembly | rail-bottom-right | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | rail-bottom-right | solid body | 1 | PASS |
| osa-dryer-assembly | rail-mid-front-left | volume (mm3) | OCP 146963.371 / Fusion 146963.370 | PASS |
| osa-dryer-assembly | rail-mid-front-left | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | rail-mid-front-left | solid body | 1 | PASS |
| osa-dryer-assembly | rail-mid-front-right | volume (mm3) | OCP 146963.371 / Fusion 146963.370 | PASS |
| osa-dryer-assembly | rail-mid-front-right | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | rail-mid-front-right | solid body | 1 | PASS |
| osa-dryer-assembly | rail-mid-rear | volume (mm3) | OCP 664056.711 / Fusion 664056.711 | PASS |
| osa-dryer-assembly | rail-mid-rear | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | rail-mid-rear | solid body | 1 | PASS |
| osa-dryer-assembly | rail-mid-left | volume (mm3) | OCP 729373.765 / Fusion 729373.765 | PASS |
| osa-dryer-assembly | rail-mid-left | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | rail-mid-left | solid body | 1 | PASS |
| osa-dryer-assembly | rail-mid-right | volume (mm3) | OCP 729373.765 / Fusion 729373.765 | PASS |
| osa-dryer-assembly | rail-mid-right | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | rail-mid-right | solid body | 1 | PASS |
| osa-dryer-assembly | rail-mid-rearcross | volume (mm3) | OCP 664056.711 / Fusion 664056.711 | PASS |
| osa-dryer-assembly | rail-mid-rearcross | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | rail-mid-rearcross | solid body | 1 | PASS |
| osa-dryer-assembly | rail-top-front | volume (mm3) | OCP 664056.711 / Fusion 664056.711 | PASS |
| osa-dryer-assembly | rail-top-front | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | rail-top-front | solid body | 1 | PASS |
| osa-dryer-assembly | rail-top-rear | volume (mm3) | OCP 664056.711 / Fusion 664056.711 | PASS |
| osa-dryer-assembly | rail-top-rear | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | rail-top-rear | solid body | 1 | PASS |
| osa-dryer-assembly | rail-top-left | volume (mm3) | OCP 729373.765 / Fusion 729373.765 | PASS |
| osa-dryer-assembly | rail-top-left | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | rail-top-left | solid body | 1 | PASS |
| osa-dryer-assembly | rail-top-right | volume (mm3) | OCP 729373.765 / Fusion 729373.765 | PASS |
| osa-dryer-assembly | rail-top-right | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | rail-top-right | solid body | 1 | PASS |
| osa-dryer-assembly | rail-top-rearcross | volume (mm3) | OCP 664056.711 / Fusion 664056.711 | PASS |
| osa-dryer-assembly | rail-top-rearcross | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | rail-top-rearcross | solid body | 1 | PASS |
| osa-dryer-assembly | tray-rail-1 | volume (mm3) | OCP 151936.620 / Fusion 151936.620 | PASS |
| osa-dryer-assembly | tray-rail-1 | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | tray-rail-1 | solid body | 1 | PASS |
| osa-dryer-assembly | tray-rail-2 | volume (mm3) | OCP 151936.620 / Fusion 151936.620 | PASS |
| osa-dryer-assembly | tray-rail-2 | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | tray-rail-2 | solid body | 1 | PASS |
| osa-dryer-assembly | tray-rail-brackets (bought, 4 x 2020 inside corner brackets) | volume (mm3) (4 bodies added) | OCP 6056.914 / Fusion 6056.914 | PASS |
| osa-dryer-assembly | tray-rail-brackets (bought, 4 x 2020 inside corner brackets) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | tray-rail-brackets (bought, 4 x 2020 inside corner brackets) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-tray-rails (bought, 8 x M4 x 8 button head, T-nuts for the 6 and 8 mm slots) | volume (mm3) (8 bodies added) | OCP 1429.360 / Fusion 1429.359 | PASS |
| osa-dryer-assembly | hardware-tray-rails (bought, 8 x M4 x 8 button head, T-nuts for the 6 and 8 mm slots) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-tray-rails (bought, 8 x M4 x 8 button head, T-nuts for the 6 and 8 mm slots) | solid body | 1 | PASS |
| osa-dryer-assembly | feet (bought, 4 x M8 leveling feet, 50 pad) | volume (mm3) (4 bodies added) | OCP 93105.692 / Fusion 93105.692 | PASS |
| osa-dryer-assembly | feet (bought, 4 x M8 leveling feet, 50 pad) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | feet (bought, 4 x M8 leveling feet, 50 pad) | solid body | 1 | PASS |
| osa-dryer-assembly | front-bulkhead | volume (mm3) | OCP 403407.561 / Fusion 403407.561 | PASS |
| osa-dryer-assembly | front-bulkhead | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | front-bulkhead | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-front-bulkhead (bought, 7 x M6 x 12 hex, washers, T-nuts) | volume (mm3) (7 bodies added) | OCP 6009.126 / Fusion 6009.126 | PASS |
| osa-dryer-assembly | hardware-front-bulkhead (bought, 7 x M6 x 12 hex, washers, T-nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-front-bulkhead (bought, 7 x M6 x 12 hex, washers, T-nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | rear-bulkhead | volume (mm3) | OCP 652057.649 / Fusion 652057.649 | PASS |
| osa-dryer-assembly | rear-bulkhead | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | rear-bulkhead | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-rear-bulkhead (bought, 10 x M6 x 12 hex, washers, T-nuts) | volume (mm3) (10 bodies added) | OCP 8584.466 / Fusion 8584.466 | PASS |
| osa-dryer-assembly | hardware-rear-bulkhead (bought, 10 x M6 x 12 hex, washers, T-nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-rear-bulkhead (bought, 10 x M6 x 12 hex, washers, T-nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | felt-seal-rear-long | volume (mm3) | OCP 230740.865 / Fusion 230740.865 | PASS |
| osa-dryer-assembly | felt-seal-rear-long | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | felt-seal-rear-long | solid body | 1 | PASS |
| osa-dryer-assembly | felt-seal-rear-short | volume (mm3) | OCP 71273.622 / Fusion 71273.621 | PASS |
| osa-dryer-assembly | felt-seal-rear-short | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | felt-seal-rear-short | solid body | 1 | PASS |
| osa-dryer-assembly | felt-seal-front-long | volume (mm3) | OCP 184592.692 / Fusion 184592.692 | PASS |
| osa-dryer-assembly | felt-seal-front-long | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | felt-seal-front-long | solid body | 1 | PASS |
| osa-dryer-assembly | felt-seal-front-short | volume (mm3) | OCP 57018.897 / Fusion 57018.897 | PASS |
| osa-dryer-assembly | felt-seal-front-short | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | felt-seal-front-short | solid body | 1 | PASS |
| osa-dryer-assembly | drum-glides-front (bought, 2 x nylon drum glide pads, 45 x 20 x 8) | volume (mm3) (2 bodies added) | OCP 13153.340 / Fusion 13153.340 | PASS |
| osa-dryer-assembly | drum-glides-front (bought, 2 x nylon drum glide pads, 45 x 20 x 8) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | drum-glides-front (bought, 2 x nylon drum glide pads, 45 x 20 x 8) | solid body | 1 | PASS |
| osa-dryer-assembly | drum-glides-rear (bought, 2 x nylon drum glide pads, 45 x 20 x 9.5) | volume (mm3) (2 bodies added) | OCP 15734.737 / Fusion 15734.737 | PASS |
| osa-dryer-assembly | drum-glides-rear (bought, 2 x nylon drum glide pads, 45 x 20 x 9.5) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | drum-glides-rear (bought, 2 x nylon drum glide pads, 45 x 20 x 9.5) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-drum-glides (bought, 4 x M4 x 8 and 4 x M4 x 10 button head, nuts) | volume (mm3) (16 bodies added) | OCP 2261.560 / Fusion 2261.559 | PASS |
| osa-dryer-assembly | hardware-drum-glides (bought, 4 x M4 x 8 and 4 x M4 x 10 button head, nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-drum-glides (bought, 4 x M4 x 8 and 4 x M4 x 10 button head, nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | bay-ceiling | volume (mm3) | OCP 685439.751 / Fusion 685439.751 | PASS |
| osa-dryer-assembly | bay-ceiling | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | bay-ceiling | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-bay-ceiling (bought, 20 x M6 x 12 hex, washers, T-nuts) | volume (mm3) (20 bodies added) | OCP 17168.933 / Fusion 17168.932 | PASS |
| osa-dryer-assembly | hardware-bay-ceiling (bought, 20 x M6 x 12 hex, washers, T-nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-bay-ceiling (bought, 20 x M6 x 12 hex, washers, T-nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | base-pan | volume (mm3) | OCP 770130.214 / Fusion 770130.214 | PASS |
| osa-dryer-assembly | base-pan | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | base-pan | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-base-pan (bought, 20 x M6 x 12 hex, washers, T-nuts) | volume (mm3) (20 bodies added) | OCP 17168.933 / Fusion 17168.932 | PASS |
| osa-dryer-assembly | hardware-base-pan (bought, 20 x M6 x 12 hex, washers, T-nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-base-pan (bought, 20 x M6 x 12 hex, washers, T-nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | side-panel-left | volume (mm3) | OCP 1123510.182 / Fusion 1123510.182 | PASS |
| osa-dryer-assembly | side-panel-left | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | side-panel-left | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-side-panel-left (bought, 29 x M6 x 12 hex, washers, T-nuts) | volume (mm3) (29 bodies added) | OCP 24894.953 / Fusion 24894.951 | PASS |
| osa-dryer-assembly | hardware-side-panel-left (bought, 29 x M6 x 12 hex, washers, T-nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-side-panel-left (bought, 29 x M6 x 12 hex, washers, T-nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | side-panel-right | volume (mm3) | OCP 1123510.182 / Fusion 1123510.182 | PASS |
| osa-dryer-assembly | side-panel-right | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | side-panel-right | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-side-panel-right (bought, 29 x M6 x 12 hex, washers, T-nuts) | volume (mm3) (29 bodies added) | OCP 24894.953 / Fusion 24894.951 | PASS |
| osa-dryer-assembly | hardware-side-panel-right (bought, 29 x M6 x 12 hex, washers, T-nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-side-panel-right (bought, 29 x M6 x 12 hex, washers, T-nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | front-upper-panel | volume (mm3) | OCP 493200.416 / Fusion 493200.416 | PASS |
| osa-dryer-assembly | front-upper-panel | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | front-upper-panel | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-front-upper-panel (bought, 16 x M6 x 12 hex, washers, T-nuts) | volume (mm3) (16 bodies added) | OCP 13735.146 / Fusion 13735.146 | PASS |
| osa-dryer-assembly | hardware-front-upper-panel (bought, 16 x M6 x 12 hex, washers, T-nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-front-upper-panel (bought, 16 x M6 x 12 hex, washers, T-nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | front-lower-panel | volume (mm3) | OCP 242871.113 / Fusion 242871.113 | PASS |
| osa-dryer-assembly | front-lower-panel | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | front-lower-panel | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-front-lower-panel (bought, 8 x M6 x 12 hex, washers, T-nuts) | volume (mm3) (8 bodies added) | OCP 6867.573 / Fusion 6867.573 | PASS |
| osa-dryer-assembly | hardware-front-lower-panel (bought, 8 x M6 x 12 hex, washers, T-nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-front-lower-panel (bought, 8 x M6 x 12 hex, washers, T-nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | rear-upper-panel | volume (mm3) | OCP 764957.703 / Fusion 764957.703 | PASS |
| osa-dryer-assembly | rear-upper-panel | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | rear-upper-panel | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-rear-upper-panel (bought, 18 x M6 x 12 hex, washers, T-nuts) | volume (mm3) (18 bodies added) | OCP 15452.040 / Fusion 15452.039 | PASS |
| osa-dryer-assembly | hardware-rear-upper-panel (bought, 18 x M6 x 12 hex, washers, T-nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-rear-upper-panel (bought, 18 x M6 x 12 hex, washers, T-nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | rear-lower-panel | volume (mm3) | OCP 238937.895 / Fusion 238937.895 | PASS |
| osa-dryer-assembly | rear-lower-panel | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | rear-lower-panel | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-rear-lower-panel (bought, 8 x M6 x 12 hex, washers, T-nuts) | volume (mm3) (8 bodies added) | OCP 6867.573 / Fusion 6867.573 | PASS |
| osa-dryer-assembly | hardware-rear-lower-panel (bought, 8 x M6 x 12 hex, washers, T-nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-rear-lower-panel (bought, 8 x M6 x 12 hex, washers, T-nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | top-panel | volume (mm3) | OCP 774637.955 / Fusion 774637.955 | PASS |
| osa-dryer-assembly | top-panel | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | top-panel | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-top-panel (bought, 16 x M6 x 12 hex, washers, T-nuts) | volume (mm3) (16 bodies added) | OCP 13735.146 / Fusion 13735.146 | PASS |
| osa-dryer-assembly | hardware-top-panel (bought, 16 x M6 x 12 hex, washers, T-nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-top-panel (bought, 16 x M6 x 12 hex, washers, T-nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | console-post-1 | volume (mm3) | OCP 217723.512 / Fusion 217723.512 | PASS |
| osa-dryer-assembly | console-post-1 | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | console-post-1 | solid body | 1 | PASS |
| osa-dryer-assembly | console-post-2 | volume (mm3) | OCP 217723.512 / Fusion 217723.512 | PASS |
| osa-dryer-assembly | console-post-2 | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | console-post-2 | solid body | 1 | PASS |
| osa-dryer-assembly | console-post-3 | volume (mm3) | OCP 217723.512 / Fusion 217723.512 | PASS |
| osa-dryer-assembly | console-post-3 | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | console-post-3 | solid body | 1 | PASS |
| osa-dryer-assembly | console-post-4 | volume (mm3) | OCP 217723.512 / Fusion 217723.512 | PASS |
| osa-dryer-assembly | console-post-4 | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | console-post-4 | solid body | 1 | PASS |
| osa-dryer-assembly | console-rail-front | volume (mm3) | OCP 664056.711 / Fusion 664056.711 | PASS |
| osa-dryer-assembly | console-rail-front | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | console-rail-front | solid body | 1 | PASS |
| osa-dryer-assembly | console-rail-rear | volume (mm3) | OCP 664056.711 / Fusion 664056.711 | PASS |
| osa-dryer-assembly | console-rail-rear | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | console-rail-rear | solid body | 1 | PASS |
| osa-dryer-assembly | console-rail-left | volume (mm3) | OCP 63684.127 / Fusion 63684.127 | PASS |
| osa-dryer-assembly | console-rail-left | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | console-rail-left | solid body | 1 | PASS |
| osa-dryer-assembly | console-rail-right | volume (mm3) | OCP 63684.127 / Fusion 63684.127 | PASS |
| osa-dryer-assembly | console-rail-right | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | console-rail-right | solid body | 1 | PASS |
| osa-dryer-assembly | console-brackets (bought, 12 x 4040 inside corner brackets) | volume (mm3) (12 bodies added) | OCP 104526.425 / Fusion 104526.425 | PASS |
| osa-dryer-assembly | console-brackets (bought, 12 x 4040 inside corner brackets) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | console-brackets (bought, 12 x 4040 inside corner brackets) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-console-brackets (bought, 24 x M6 x 12 hex, washers, T-nuts) | volume (mm3) (24 bodies added) | OCP 20602.719 / Fusion 20602.718 | PASS |
| osa-dryer-assembly | hardware-console-brackets (bought, 24 x M6 x 12 hex, washers, T-nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-console-brackets (bought, 24 x M6 x 12 hex, washers, T-nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | console-face | volume (mm3) | OCP 105612.310 / Fusion 105612.310 | PASS |
| osa-dryer-assembly | console-face | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | console-face | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-console-face (bought, 8 x M6 x 12 hex, washers, T-nuts) | volume (mm3) (8 bodies added) | OCP 6867.573 / Fusion 6867.573 | PASS |
| osa-dryer-assembly | hardware-console-face (bought, 8 x M6 x 12 hex, washers, T-nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-console-face (bought, 8 x M6 x 12 hex, washers, T-nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | console-rear | volume (mm3) | OCP 208107.949 / Fusion 208107.949 | PASS |
| osa-dryer-assembly | console-rear | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | console-rear | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-console-rear (bought, 8 x M6 x 12 hex, washers, T-nuts) | volume (mm3) (8 bodies added) | OCP 6867.573 / Fusion 6867.573 | PASS |
| osa-dryer-assembly | hardware-console-rear (bought, 8 x M6 x 12 hex, washers, T-nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-console-rear (bought, 8 x M6 x 12 hex, washers, T-nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | console-cap | volume (mm3) | OCP 146545.150 / Fusion 146545.150 | PASS |
| osa-dryer-assembly | console-cap | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | console-cap | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-console-cap (bought, 10 x M6 x 12 hex, washers, T-nuts) | volume (mm3) (10 bodies added) | OCP 8584.466 / Fusion 8584.466 | PASS |
| osa-dryer-assembly | hardware-console-cap (bought, 10 x M6 x 12 hex, washers, T-nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-console-cap (bought, 10 x M6 x 12 hex, washers, T-nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | console-cheek-left | volume (mm3) | OCP 42473.148 / Fusion 42473.148 | PASS |
| osa-dryer-assembly | console-cheek-left | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | console-cheek-left | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-console-cheek-left (bought, 5 x M6 x 12 hex, washers, T-nuts) | volume (mm3) (5 bodies added) | OCP 4292.233 / Fusion 4292.233 | PASS |
| osa-dryer-assembly | hardware-console-cheek-left (bought, 5 x M6 x 12 hex, washers, T-nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-console-cheek-left (bought, 5 x M6 x 12 hex, washers, T-nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | console-cheek-right | volume (mm3) | OCP 42473.148 / Fusion 42473.148 | PASS |
| osa-dryer-assembly | console-cheek-right | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | console-cheek-right | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-console-cheek-right (bought, 5 x M6 x 12 hex, washers, T-nuts) | volume (mm3) (5 bodies added) | OCP 4292.233 / Fusion 4292.233 | PASS |
| osa-dryer-assembly | hardware-console-cheek-right (bought, 5 x M6 x 12 hex, washers, T-nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-console-cheek-right (bought, 5 x M6 x 12 hex, washers, T-nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | tier0-faceplate | volume (mm3) | OCP 195756.562 / Fusion 195756.562 | PASS |
| osa-dryer-assembly | tier0-faceplate | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | tier0-faceplate | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-tier0-faceplate (bought, 6 x M4 x 10 button head, nuts) | volume (mm3) (12 bodies added) | OCP 1771.568 / Fusion 1771.568 | PASS |
| osa-dryer-assembly | hardware-tier0-faceplate (bought, 6 x M4 x 10 button head, nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-tier0-faceplate (bought, 6 x M4 x 10 button head, nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | tier0-knob-dry-time (bought) | volume (mm3) | OCP 15189.251 / Fusion 15189.251 | PASS |
| osa-dryer-assembly | tier0-knob-dry-time (bought) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | tier0-knob-dry-time (bought) | solid body | 1 | PASS |
| osa-dryer-assembly | tier0-timer-dry-time (bought) | volume (mm3) | OCP 90563.210 / Fusion 90563.210 | PASS |
| osa-dryer-assembly | tier0-timer-dry-time (bought) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | tier0-timer-dry-time (bought) | solid body | 1 | PASS |
| osa-dryer-assembly | tier0-knob-heat-time (bought) | volume (mm3) | OCP 15189.251 / Fusion 15189.251 | PASS |
| osa-dryer-assembly | tier0-knob-heat-time (bought) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | tier0-knob-heat-time (bought) | solid body | 1 | PASS |
| osa-dryer-assembly | tier0-timer-heat-time (bought) | volume (mm3) | OCP 90563.210 / Fusion 90563.210 | PASS |
| osa-dryer-assembly | tier0-timer-heat-time (bought) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | tier0-timer-heat-time (bought) | solid body | 1 | PASS |
| osa-dryer-assembly | tier0-selector-body (bought) | volume (mm3) (2 bodies added) | OCP 34073.174 / Fusion 34073.174 | PASS |
| osa-dryer-assembly | tier0-selector-body (bought) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | tier0-selector-body (bought) | solid body | 1 | PASS |
| osa-dryer-assembly | tier0-selector (bought) | volume (mm3) | OCP 2878.124 / Fusion 2878.124 | PASS |
| osa-dryer-assembly | tier0-selector (bought) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | tier0-selector (bought) | solid body | 1 | PASS |
| osa-dryer-assembly | tier0-start-body (bought) | volume (mm3) (2 bodies added) | OCP 34073.174 / Fusion 34073.174 | PASS |
| osa-dryer-assembly | tier0-start-body (bought) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | tier0-start-body (bought) | solid body | 1 | PASS |
| osa-dryer-assembly | tier0-start-button (bought) | volume (mm3) | OCP 2984.142 / Fusion 2984.142 | PASS |
| osa-dryer-assembly | tier0-start-button (bought) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | tier0-start-button (bought) | solid body | 1 | PASS |
| osa-dryer-assembly | tier0-k1-relay-on-din-rail (bought) | volume (mm3) | OCP 127556.372 / Fusion 127556.372 | PASS |
| osa-dryer-assembly | tier0-k1-relay-on-din-rail (bought) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | tier0-k1-relay-on-din-rail (bought) | solid body | 1 | PASS |
| osa-dryer-assembly | door-ring | volume (mm3) | OCP 145112.128 / Fusion 145112.128 | PASS |
| osa-dryer-assembly | door-ring | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | door-ring | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-door-ring (bought, 8 x M4 x 8 button head, nuts) | volume (mm3) (16 bodies added) | OCP 2161.029 / Fusion 2161.028 | PASS |
| osa-dryer-assembly | hardware-door-ring (bought, 8 x M4 x 8 button head, nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-door-ring (bought, 8 x M4 x 8 button head, nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | door-disc | volume (mm3) | OCP 457916.974 / Fusion 457916.974 | PASS |
| osa-dryer-assembly | door-disc | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | door-disc | solid body | 1 | PASS |
| osa-dryer-assembly | door-hinge-1-fixed (bought, flag hinge, pinned half) | volume (mm3) | OCP 17840.613 / Fusion 17840.613 | PASS |
| osa-dryer-assembly | door-hinge-1-fixed (bought, flag hinge, pinned half) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | door-hinge-1-fixed (bought, flag hinge, pinned half) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-door-hinge-1 (bought, 2 x M6 x 16 countersunk, nuts) | volume (mm3) (4 bodies added) | OCP 1692.210 / Fusion 1692.210 | PASS |
| osa-dryer-assembly | hardware-door-hinge-1 (bought, 2 x M6 x 16 countersunk, nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-door-hinge-1 (bought, 2 x M6 x 16 countersunk, nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | door-hinge-2-swing (bought, flag hinge, lift-off half) | volume (mm3) | OCP 10700.959 / Fusion 10700.959 | PASS |
| osa-dryer-assembly | door-hinge-2-swing (bought, flag hinge, lift-off half) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | door-hinge-2-swing (bought, flag hinge, lift-off half) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-door-hinge-2 (bought, 2 x M4 x 8 button head into the tapped leaf) | volume (mm3) (2 bodies added) | OCP 357.340 / Fusion 357.340 | PASS |
| osa-dryer-assembly | hardware-door-hinge-2 (bought, 2 x M4 x 8 button head into the tapped leaf) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-door-hinge-2 (bought, 2 x M4 x 8 button head into the tapped leaf) | solid body | 1 | PASS |
| osa-dryer-assembly | door-handle (bought, D handle 128 centres) | volume (mm3) | OCP 30386.464 / Fusion 30386.454 | PASS |
| osa-dryer-assembly | door-handle (bought, D handle 128 centres) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | door-handle (bought, D handle 128 centres) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-door-handle (bought, 2 x M4 x 10 button head into the handle) | volume (mm3) (2 bodies added) | OCP 407.605 / Fusion 407.605 | PASS |
| osa-dryer-assembly | hardware-door-handle (bought, 2 x M4 x 10 button head into the handle) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-door-handle (bought, 2 x M4 x 10 button head into the handle) | solid body | 1 | PASS |
| osa-dryer-assembly | door-seal (bought, OEM door seal) | volume (mm3) | OCP 81939.020 / Fusion 81939.020 | PASS |
| osa-dryer-assembly | door-seal (bought, OEM door seal) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | door-seal (bought, OEM door seal) | solid body | 1 | PASS |
| osa-dryer-assembly | door-catch (bought, magnetic catch) | volume (mm3) | OCP 936.000 / Fusion 936.000 | PASS |
| osa-dryer-assembly | door-catch (bought, magnetic catch) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | door-catch (bought, magnetic catch) | solid body | 1 | PASS |
| osa-dryer-assembly | door-catch-strike (bought) | volume (mm3) | OCP 144.000 / Fusion 144.000 | PASS |
| osa-dryer-assembly | door-catch-strike (bought) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | door-catch-strike (bought) | solid body | 1 | PASS |
| osa-dryer-assembly | drum-sheet | volume (mm3) | OCP 873714.067 / Fusion 873712.681 | PASS |
| osa-dryer-assembly | drum-sheet | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | drum-sheet | solid body | 1 | PASS |
| osa-dryer-assembly | drum-ring-front | volume (mm3) | OCP 141703.202 / Fusion 141703.202 | PASS |
| osa-dryer-assembly | drum-ring-front | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | drum-ring-front | solid body | 1 | PASS |
| osa-dryer-assembly | drum-ring-rear | volume (mm3) | OCP 141703.202 / Fusion 141703.202 | PASS |
| osa-dryer-assembly | drum-ring-rear | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | drum-ring-rear | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-drum-tabs (bought, 60 x M4 x 8 button head, nuts) | volume (mm3) (120 bodies added) | OCP 16207.714 / Fusion 16207.710 | PASS |
| osa-dryer-assembly | hardware-drum-tabs (bought, 60 x M4 x 8 button head, nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-drum-tabs (bought, 60 x M4 x 8 button head, nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | drum-splice | volume (mm3) | OCP 32383.401 / Fusion 32384.592 | PASS |
| osa-dryer-assembly | drum-splice | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | drum-splice | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-drum-seam (bought, 16 x M4 x 8 button head, nuts) | volume (mm3) (32 bodies added) | OCP 4322.057 / Fusion 4322.056 | PASS |
| osa-dryer-assembly | hardware-drum-seam (bought, 16 x M4 x 8 button head, nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-drum-seam (bought, 16 x M4 x 8 button head, nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | baffle-1 (angle, cut to length) | volume (mm3) | OCP 110481.803 / Fusion 110481.803 | PASS |
| osa-dryer-assembly | baffle-1 (angle, cut to length) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | baffle-1 (angle, cut to length) | solid body | 1 | PASS |
| osa-dryer-assembly | baffle-2 (angle, cut to length) | volume (mm3) | OCP 110481.803 / Fusion 110481.803 | PASS |
| osa-dryer-assembly | baffle-2 (angle, cut to length) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | baffle-2 (angle, cut to length) | solid body | 1 | PASS |
| osa-dryer-assembly | baffle-3 (angle, cut to length) | volume (mm3) | OCP 110481.803 / Fusion 110481.803 | PASS |
| osa-dryer-assembly | baffle-3 (angle, cut to length) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | baffle-3 (angle, cut to length) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-drum-baffles (bought, 12 x M6 x 12 button head, nuts) | volume (mm3) (24 bodies added) | OCP 10142.813 / Fusion 10142.807 | PASS |
| osa-dryer-assembly | hardware-drum-baffles (bought, 12 x M6 x 12 button head, nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-drum-baffles (bought, 12 x M6 x 12 button head, nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | motor (bought) | volume (mm3) | OCP 3046373.714 / Fusion 3046373.714 | PASS |
| osa-dryer-assembly | motor (bought) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | motor (bought) | solid body | 1 | PASS |
| osa-dryer-assembly | motor-mount-1 (bought, cradle bracket) | volume (mm3) | OCP 39966.897 / Fusion 39966.897 | PASS |
| osa-dryer-assembly | motor-mount-1 (bought, cradle bracket) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | motor-mount-1 (bought, cradle bracket) | solid body | 1 | PASS |
| osa-dryer-assembly | motor-mount-2 (bought, cradle bracket) | volume (mm3) | OCP 39966.897 / Fusion 39966.897 | PASS |
| osa-dryer-assembly | motor-mount-2 (bought, cradle bracket) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | motor-mount-2 (bought, cradle bracket) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-motor-mounts (bought, 4 x M6 x 12 hex, washers, nuts, through the base pan) | volume (mm3) (8 bodies added) | OCP 4562.023 / Fusion 4562.023 | PASS |
| osa-dryer-assembly | hardware-motor-mounts (bought, 4 x M6 x 12 hex, washers, nuts, through the base pan) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-motor-mounts (bought, 4 x M6 x 12 hex, washers, nuts, through the base pan) | solid body | 1 | PASS |
| osa-dryer-assembly | pulley (bought) | volume (mm3) | OCP 6967.148 / Fusion 6967.148 | PASS |
| osa-dryer-assembly | pulley (bought) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | pulley (bought) | solid body | 1 | PASS |
| osa-dryer-assembly | blower (bought) | volume (mm3) | OCP 5340928.083 / Fusion 5340928.083 | PASS |
| osa-dryer-assembly | blower (bought) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | blower (bought) | solid body | 1 | PASS |
| osa-dryer-assembly | heat-module-tray | volume (mm3) | OCP 142392.194 / Fusion 142392.194 | PASS |
| osa-dryer-assembly | heat-module-tray | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | heat-module-tray | solid body | 1 | PASS |
| osa-dryer-assembly | heat-module-wall-left | volume (mm3) | OCP 19709.023 / Fusion 19709.023 | PASS |
| osa-dryer-assembly | heat-module-wall-left | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | heat-module-wall-left | solid body | 1 | PASS |
| osa-dryer-assembly | heat-module-wall-right | volume (mm3) | OCP 31709.023 / Fusion 31709.023 | PASS |
| osa-dryer-assembly | heat-module-wall-right | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | heat-module-wall-right | solid body | 1 | PASS |
| osa-dryer-assembly | heat-module-wall-front | volume (mm3) | OCP 46506.810 / Fusion 46506.810 | PASS |
| osa-dryer-assembly | heat-module-wall-front | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | heat-module-wall-front | solid body | 1 | PASS |
| osa-dryer-assembly | heat-module-wall-rear | volume (mm3) | OCP 46506.810 / Fusion 46506.810 | PASS |
| osa-dryer-assembly | heat-module-wall-rear | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | heat-module-wall-rear | solid body | 1 | PASS |
| osa-dryer-assembly | heat-module-top | volume (mm3) | OCP 70030.523 / Fusion 70030.523 | PASS |
| osa-dryer-assembly | heat-module-top | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | heat-module-top | solid body | 1 | PASS |
| osa-dryer-assembly | heat-module-angles-bottom (20x20x2 aluminium angle, 2 x 205 outside, 2 x 283 inside) | volume (mm3) (4 bodies added) | OCP 73539.827 / Fusion 73539.827 | PASS |
| osa-dryer-assembly | heat-module-angles-bottom (20x20x2 aluminium angle, 2 x 205 outside, 2 x 283 inside) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | heat-module-angles-bottom (20x20x2 aluminium angle, 2 x 205 outside, 2 x 283 inside) | solid body | 1 | PASS |
| osa-dryer-assembly | heat-module-angles-top (20x20x2 aluminium angle, 2 x 165, 2 x 290) | volume (mm3) (4 bodies added) | OCP 68523.827 / Fusion 68523.827 | PASS |
| osa-dryer-assembly | heat-module-angles-top (20x20x2 aluminium angle, 2 x 165, 2 x 290) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | heat-module-angles-top (20x20x2 aluminium angle, 2 x 165, 2 x 290) | solid body | 1 | PASS |
| osa-dryer-assembly | heat-module-angles-corner (20x20x2 aluminium angle, 4 x 72) | volume (mm3) (4 bodies added) | OCP 21633.531 / Fusion 21633.531 | PASS |
| osa-dryer-assembly | heat-module-angles-corner (20x20x2 aluminium angle, 4 x 72) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | heat-module-angles-corner (20x20x2 aluminium angle, 4 x 72) | solid body | 1 | PASS |
| osa-dryer-assembly | heat-module-element-rails (20x20x2 aluminium angle, 2 x 198) | volume (mm3) (2 bodies added) | OCP 29968.765 / Fusion 29968.765 | PASS |
| osa-dryer-assembly | heat-module-element-rails (20x20x2 aluminium angle, 2 x 198) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | heat-module-element-rails (20x20x2 aluminium angle, 2 x 198) | solid body | 1 | PASS |
| osa-dryer-assembly | heat-module-element (bought, 279838 class open-coil element on its frame, envelope) | volume (mm3) | OCP 2592870.000 / Fusion 2592870.000 | PASS |
| osa-dryer-assembly | heat-module-element (bought, 279838 class open-coil element on its frame, envelope) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | heat-module-element (bought, 279838 class open-coil element on its frame, envelope) | solid body | 1 | PASS |
| osa-dryer-assembly | heat-module-collar (bought, 125 flanged starting collar, cut to 55.5) | volume (mm3) | OCP 19547.838 / Fusion 19547.838 | PASS |
| osa-dryer-assembly | heat-module-collar (bought, 125 flanged starting collar, cut to 55.5) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | heat-module-collar (bought, 125 flanged starting collar, cut to 55.5) | solid body | 1 | PASS |
| osa-dryer-assembly | heat-module-thermostats (bought, 279816 class high-limit and thermal cut-off, envelopes) | volume (mm3) (2 bodies added) | OCP 15480.765 / Fusion 15480.765 | PASS |
| osa-dryer-assembly | heat-module-thermostats (bought, 279816 class high-limit and thermal cut-off, envelopes) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | heat-module-thermostats (bought, 279816 class high-limit and thermal cut-off, envelopes) | solid body | 1 | PASS |
| osa-dryer-assembly | heat-module-terminal-plate | volume (mm3) | OCP 43369.129 / Fusion 43369.129 | PASS |
| osa-dryer-assembly | heat-module-terminal-plate | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | heat-module-terminal-plate | solid body | 1 | PASS |
| osa-dryer-assembly | heat-module-terminal-angle (20x20x2 aluminium angle, 290) | volume (mm3) | OCP 21849.148 / Fusion 21849.148 | PASS |
| osa-dryer-assembly | heat-module-terminal-angle (20x20x2 aluminium angle, 290) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | heat-module-terminal-angle (20x20x2 aluminium angle, 290) | solid body | 1 | PASS |
| osa-dryer-assembly | heat-module-din-rail (bought, 35 x 7.5 top hat, 280) | volume (mm3) | OCP 13377.655 / Fusion 13377.655 | PASS |
| osa-dryer-assembly | heat-module-din-rail (bought, 35 x 7.5 top hat, 280) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | heat-module-din-rail (bought, 35 x 7.5 top hat, 280) | solid body | 1 | PASS |
| osa-dryer-assembly | heat-module-devices (bought, envelopes: 2 end clamps, X_HM mains and SELV strips, partition, K_HEAT, CS1) | volume (mm3) (7 bodies added) | OCP 502878.000 / Fusion 502878.000 | PASS |
| osa-dryer-assembly | heat-module-devices (bought, envelopes: 2 end clamps, X_HM mains and SELV strips, partition, K_HEAT, CS1) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | heat-module-devices (bought, envelopes: 2 end clamps, X_HM mains and SELV strips, partition, K_HEAT, CS1) | solid body | 1 | PASS |
| osa-dryer-assembly | heat-module-bonding-stud (bought, M6 x 16 hex bolt, 2 nuts, star washers; the PE ring terminal goes between the nuts) | volume (mm3) (3 bodies added) | OCP 1535.662 / Fusion 1535.662 | PASS |
| osa-dryer-assembly | heat-module-bonding-stud (bought, M6 x 16 hex bolt, 2 nuts, star washers; the PE ring terminal goes between the nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | heat-module-bonding-stud (bought, M6 x 16 hex bolt, 2 nuts, star washers; the PE ring terminal goes between the nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | heat-module-hardware (bought, 64 x M4 x 8 button head, 60 nuts, 4 T-nuts for the 6 mm slot) | volume (mm3) (124 bodies added) | OCP 16922.394 / Fusion 16922.390 | PASS |
| osa-dryer-assembly | heat-module-hardware (bought, 64 x M4 x 8 button head, 60 nuts, 4 T-nuts for the 6 mm slot) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | heat-module-hardware (bought, 64 x M4 x 8 button head, 60 nuts, 4 T-nuts for the 6 mm slot) | solid body | 1 | PASS |
| osa-dryer-assembly | power-module-plate | volume (mm3) | OCP 161321.526 / Fusion 161321.526 | PASS |
| osa-dryer-assembly | power-module-plate | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | power-module-plate | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-power-module-plate (bought, 4 x M6 x 12 hex, washers, T-nuts) | volume (mm3) (4 bodies added) | OCP 3433.787 / Fusion 3433.786 | PASS |
| osa-dryer-assembly | hardware-power-module-plate (bought, 4 x M6 x 12 hex, washers, T-nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-power-module-plate (bought, 4 x M6 x 12 hex, washers, T-nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | power-module-rail-A1-devices (bought, envelopes: X1 cord: 4 x UK 6 N (L1, L2, N, PE), CB1: 1P MCB, F1: UK 5-HESI fuse terminal, 2 end clamps) | volume (mm3) (5 bodies added) | OCP 213485.200 / Fusion 213485.200 | PASS |
| osa-dryer-assembly | power-module-rail-A1-devices (bought, envelopes: X1 cord: 4 x UK 6 N (L1, L2, N, PE), CB1: 1P MCB, F1: UK 5-HESI fuse terminal, 2 end clamps) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | power-module-rail-A1-devices (bought, envelopes: X1 cord: 4 x UK 6 N (L1, L2, N, PE), CB1: 1P MCB, F1: UK 5-HESI fuse terminal, 2 end clamps) | solid body | 1 | PASS |
| osa-dryer-assembly | power-module-rail-A2-devices (bought, envelopes: PSU: HDR-60-24, K_MOTOR: LC1K0910BD class mini contactor, 2 end clamps) | volume (mm3) (4 bodies added) | OCP 433870.500 / Fusion 433870.500 | PASS |
| osa-dryer-assembly | power-module-rail-A2-devices (bought, envelopes: PSU: HDR-60-24, K_MOTOR: LC1K0910BD class mini contactor, 2 end clamps) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | power-module-rail-A2-devices (bought, envelopes: PSU: HDR-60-24, K_MOTOR: LC1K0910BD class mini contactor, 2 end clamps) | solid body | 1 | PASS |
| osa-dryer-assembly | power-module-rail-A3-devices (bought, envelopes: X2 heat module mains: 4 x UK 6 N, X3 motor and S1: 5 x UK 2.5 N, 2 end clamps) | volume (mm3) (4 bodies added) | OCP 138091.200 / Fusion 138091.200 | PASS |
| osa-dryer-assembly | power-module-rail-A3-devices (bought, envelopes: X2 heat module mains: 4 x UK 6 N, X3 motor and S1: 5 x UK 2.5 N, 2 end clamps) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | power-module-rail-A3-devices (bought, envelopes: X2 heat module mains: 4 x UK 6 N, X3 motor and S1: 5 x UK 2.5 N, 2 end clamps) | solid body | 1 | PASS |
| osa-dryer-assembly | power-module-rail-B1-devices (bought, envelopes: RLY_MOTOR, RLY_HEAT, RLY_HEAT_LO: 3 x 38.51 class, PTC1 to PTC3 in fuse terminals, F2: UK 5-HESI, X4 heat module SELV: 4 x UK 2.5 N, 2 end clamps) | volume (mm3) (6 bodies added) | OCP 291878.800 / Fusion 291878.800 | PASS |
| osa-dryer-assembly | power-module-rail-B1-devices (bought, envelopes: RLY_MOTOR, RLY_HEAT, RLY_HEAT_LO: 3 x 38.51 class, PTC1 to PTC3 in fuse terminals, F2: UK 5-HESI, X4 heat module SELV: 4 x UK 2.5 N, 2 end clamps) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | power-module-rail-B1-devices (bought, envelopes: RLY_MOTOR, RLY_HEAT, RLY_HEAT_LO: 3 x 38.51 class, PTC1 to PTC3 in fuse terminals, F2: UK 5-HESI, X4 heat module SELV: 4 x UK 2.5 N, 2 end clamps) | solid body | 1 | PASS |
| osa-dryer-assembly | power-module-rail-B2-devices (bought, envelopes: X5 chassis switches: 10 x UK 2.5 N, X6 sensors: 6 x UK 2.5 N, 2 end clamps) | volume (mm3) (4 bodies added) | OCP 174007.200 / Fusion 174007.200 | PASS |
| osa-dryer-assembly | power-module-rail-B2-devices (bought, envelopes: X5 chassis switches: 10 x UK 2.5 N, X6 sensors: 6 x UK 2.5 N, 2 end clamps) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | power-module-rail-B2-devices (bought, envelopes: X5 chassis switches: 10 x UK 2.5 N, X6 sensors: 6 x UK 2.5 N, 2 end clamps) | solid body | 1 | PASS |
| osa-dryer-assembly | power-module-din-rails (bought, 5 x 35 x 7.5 top hat, 140) | volume (mm3) (5 bodies added) | OCP 33288.275 / Fusion 33288.276 | PASS |
| osa-dryer-assembly | power-module-din-rails (bought, 5 x 35 x 7.5 top hat, 140) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | power-module-din-rails (bought, 5 x 35 x 7.5 top hat, 140) | solid body | 1 | PASS |
| osa-dryer-assembly | power-module-barrier-angle (20x20x2 aluminium angle, 150) | volume (mm3) | OCP 11272.765 / Fusion 11272.765 | PASS |
| osa-dryer-assembly | power-module-barrier-angle (20x20x2 aluminium angle, 150) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | power-module-barrier-angle (20x20x2 aluminium angle, 150) | solid body | 1 | PASS |
| osa-dryer-assembly | power-module-barrier | volume (mm3) | OCP 16928.199 / Fusion 16928.199 | PASS |
| osa-dryer-assembly | power-module-barrier | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | power-module-barrier | solid body | 1 | PASS |
| osa-dryer-assembly | power-module-cover | volume (mm3) | OCP 74108.220 / Fusion 74108.220 | PASS |
| osa-dryer-assembly | power-module-cover | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | power-module-cover | solid body | 1 | PASS |
| osa-dryer-assembly | power-module-standoffs (bought, 4 x M4 x 75 hex standoffs, female both ends) | volume (mm3) (4 bodies added) | OCP 11733.055 / Fusion 11733.055 | PASS |
| osa-dryer-assembly | power-module-standoffs (bought, 4 x M4 x 75 hex standoffs, female both ends) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | power-module-standoffs (bought, 4 x M4 x 75 hex standoffs, female both ends) | solid body | 1 | PASS |
| osa-dryer-assembly | power-module-ground-stud (bought, M6 x 16 hex bolt, 2 nuts, star washers; the cord's PE ring terminal goes between the nuts) | volume (mm3) (3 bodies added) | OCP 1535.662 / Fusion 1535.662 | PASS |
| osa-dryer-assembly | power-module-ground-stud (bought, M6 x 16 hex bolt, 2 nuts, star washers; the cord's PE ring terminal goes between the nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | power-module-ground-stud (bought, M6 x 16 hex bolt, 2 nuts, star washers; the cord's PE ring terminal goes between the nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | power-module-hardware (bought, 22 x M4 x 8 button head, 14 nuts) | volume (mm3) (36 bodies added) | OCP 5211.159 / Fusion 5211.158 | PASS |
| osa-dryer-assembly | power-module-hardware (bought, 22 x M4 x 8 button head, 14 nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | power-module-hardware (bought, 22 x M4 x 8 button head, 14 nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | grommets (bought, 5 x rubber grommets for 1.5 panels: 22 mm hole x 2, 30 mm hole x 1, 16 mm hole x 2) | volume (mm3) (5 bodies added) | OCP 6693.713 / Fusion 6693.713 | PASS |
| osa-dryer-assembly | grommets (bought, 5 x rubber grommets for 1.5 panels: 22 mm hole x 2, 30 mm hole x 1, 16 mm hole x 2) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | grommets (bought, 5 x rubber grommets for 1.5 panels: 22 mm hole x 2, 30 mm hole x 1, 16 mm hole x 2) | solid body | 1 | PASS |
| osa-dryer-assembly | cord-bushing (bought, PG16 strain relief) | volume (mm3) | OCP 8877.396 / Fusion 8877.396 | PASS |
| osa-dryer-assembly | cord-bushing (bought, PG16 strain relief) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | cord-bushing (bought, PG16 strain relief) | solid body | 1 | PASS |
| osa-dryer-assembly | power-cord (bought) | volume (mm3) | OCP 29269.670 / Fusion 29269.670 | PASS |
| osa-dryer-assembly | power-cord (bought) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | power-cord (bought) | solid body | 1 | PASS |
| osa-dryer-assembly | liner | volume (mm3) | OCP 91807.599 / Fusion 91807.543 | PASS |
| osa-dryer-assembly | liner | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | liner | solid body | 1 | PASS |
| osa-dryer-assembly | liner-splice | volume (mm3) | OCP 2270.762 / Fusion 2270.749 | PASS |
| osa-dryer-assembly | liner-splice | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | liner-splice | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-liner (bought, 2 x M3 x 6 button head, nuts) | volume (mm3) (4 bodies added) | OCP 234.826 / Fusion 234.826 | PASS |
| osa-dryer-assembly | hardware-liner (bought, 2 x M3 x 6 button head, nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-liner (bought, 2 x M3 x 6 button head, nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | lint-box-bars (30 x 8 aluminium flat bar: 2 sides mitred at the top, 1 bottom) | volume (mm3) (3 bodies added) | OCP 261325.657 / Fusion 261325.657 | PASS |
| osa-dryer-assembly | lint-box-bars (30 x 8 aluminium flat bar: 2 sides mitred at the top, 1 bottom) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | lint-box-bars (30 x 8 aluminium flat bar: 2 sides mitred at the top, 1 bottom) | solid body | 1 | PASS |
| osa-dryer-assembly | lint-box-front | volume (mm3) | OCP 175620.605 / Fusion 175620.605 | PASS |
| osa-dryer-assembly | lint-box-front | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | lint-box-front | solid body | 1 | PASS |
| osa-dryer-assembly | lint-box-back | volume (mm3) | OCP 80050.373 / Fusion 80050.373 | PASS |
| osa-dryer-assembly | lint-box-back | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | lint-box-back | solid body | 1 | PASS |
| osa-dryer-assembly | lint-box-foam (bought, 3 mm closed-cell foam tape 8 wide, 2 x 190, compressed to 1.5) | volume (mm3) (2 bodies added) | OCP 4255.258 / Fusion 4255.258 | PASS |
| osa-dryer-assembly | lint-box-foam (bought, 3 mm closed-cell foam tape 8 wide, 2 x 190, compressed to 1.5) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | lint-box-foam (bought, 3 mm closed-cell foam tape 8 wide, 2 x 190, compressed to 1.5) | solid body | 1 | PASS |
| osa-dryer-assembly | spool-bars (40 x 8 aluminium flat bar: 2 x 136, 2 x 140) | volume (mm3) (4 bodies added) | OCP 175718.681 / Fusion 175718.681 | PASS |
| osa-dryer-assembly | spool-bars (40 x 8 aluminium flat bar: 2 x 136, 2 x 140) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | spool-bars (40 x 8 aluminium flat bar: 2 x 136, 2 x 140) | solid body | 1 | PASS |
| osa-dryer-assembly | spool-foam (bought, 6 mm closed-cell foam tape 8 wide, 600, compressed to 4 on the blower plate) | volume (mm3) (4 bodies added) | OCP 17664.000 / Fusion 17664.000 | PASS |
| osa-dryer-assembly | spool-foam (bought, 6 mm closed-cell foam tape 8 wide, 600, compressed to 4 on the blower plate) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | spool-foam (bought, 6 mm closed-cell foam tape 8 wide, 600, compressed to 4 on the blower plate) | solid body | 1 | PASS |
| osa-dryer-assembly | lint-box-hardware (bought, 40 pieces: M4 x 8, M4 x 10 and M4 x 40 button heads, 2 x M6 x 20 button heads with 4 mm spacers and T-nuts) | volume (mm3) (40 bodies added) | OCP 11200.987 / Fusion 11200.986 | PASS |
| osa-dryer-assembly | lint-box-hardware (bought, 40 pieces: M4 x 8, M4 x 10 and M4 x 40 button heads, 2 x M6 x 20 button heads with 4 mm spacers and T-nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | lint-box-hardware (bought, 40 pieces: M4 x 8, M4 x 10 and M4 x 40 button heads, 2 x M6 x 20 button heads with 4 mm spacers and T-nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | basket-far-plate | volume (mm3) | OCP 24347.238 / Fusion 24347.238 | PASS |
| osa-dryer-assembly | basket-far-plate | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | basket-far-plate | solid body | 1 | PASS |
| osa-dryer-assembly | basket-far-clamp | volume (mm3) | OCP 12155.524 / Fusion 12155.524 | PASS |
| osa-dryer-assembly | basket-far-clamp | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | basket-far-clamp | solid body | 1 | PASS |
| osa-dryer-assembly | basket-lip-plate | volume (mm3) | OCP 14075.046 / Fusion 14075.046 | PASS |
| osa-dryer-assembly | basket-lip-plate | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | basket-lip-plate | solid body | 1 | PASS |
| osa-dryer-assembly | basket-lip-clamp | volume (mm3) | OCP 5002.108 / Fusion 5002.108 | PASS |
| osa-dryer-assembly | basket-lip-clamp | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | basket-lip-clamp | solid body | 1 | PASS |
| osa-dryer-assembly | basket-mesh (bought, stainless 18 x 16 mesh strip, 42 wide, 350 long, wrapped and folded 5 at each edge) | volume (mm3) (3 bodies added) | OCP 16043.178 / Fusion 16043.178 | PASS |
| osa-dryer-assembly | basket-mesh (bought, stainless 18 x 16 mesh strip, 42 wide, 350 long, wrapped and folded 5 at each edge) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | basket-mesh (bought, stainless 18 x 16 mesh strip, 42 wide, 350 long, wrapped and folded 5 at each edge) | solid body | 1 | PASS |
| osa-dryer-assembly | basket-pull (bought, D-pull, 64 mm centres, 25 projection) | volume (mm3) | OCP 8057.275 / Fusion 8057.275 | PASS |
| osa-dryer-assembly | basket-pull (bought, D-pull, 64 mm centres, 25 projection) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | basket-pull (bought, D-pull, 64 mm centres, 25 projection) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-basket (bought, 12 x M3 x 5 button head into the tapped plates, 2 x M4 x 10 button head into the pull) | volume (mm3) (14 bodies added) | OCP 1208.883 / Fusion 1208.883 | PASS |
| osa-dryer-assembly | hardware-basket (bought, 12 x M3 x 5 button head into the tapped plates, 2 x M4 x 10 button head into the pull) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-basket (bought, 12 x M3 x 5 button head into the tapped plates, 2 x M4 x 10 button head into the pull) | solid body | 1 | PASS |
| osa-dryer-assembly | hood-bars (25 x 8 aluminium flat bar: 2 sides, front, rear) | volume (mm3) (4 bodies added) | OCP 234798.925 / Fusion 234798.925 | PASS |
| osa-dryer-assembly | hood-bars (25 x 8 aluminium flat bar: 2 sides, front, rear) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hood-bars (25 x 8 aluminium flat bar: 2 sides, front, rear) | solid body | 1 | PASS |
| osa-dryer-assembly | hood-bottom | volume (mm3) | OCP 115600.636 / Fusion 115600.636 | PASS |
| osa-dryer-assembly | hood-bottom | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hood-bottom | solid body | 1 | PASS |
| osa-dryer-assembly | hood-top | volume (mm3) | OCP 116507.155 / Fusion 116507.155 | PASS |
| osa-dryer-assembly | hood-top | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hood-top | solid body | 1 | PASS |
| osa-dryer-assembly | hood-gasket (bought, 3 mm foam ring 150 x 125, glued under the hood's bottom plate) | volume (mm3) | OCP 16198.837 / Fusion 16198.837 | PASS |
| osa-dryer-assembly | hood-gasket (bought, 3 mm foam ring 150 x 125, glued under the hood's bottom plate) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hood-gasket (bought, 3 mm foam ring 150 x 125, glued under the hood's bottom plate) | solid body | 1 | PASS |
| osa-dryer-assembly | trunk-bars (50 x 8 aluminium flat bar: 2 sides, 1 top) | volume (mm3) (3 bodies added) | OCP 553698.387 / Fusion 553698.388 | PASS |
| osa-dryer-assembly | trunk-bars (50 x 8 aluminium flat bar: 2 sides, 1 top) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | trunk-bars (50 x 8 aluminium flat bar: 2 sides, 1 top) | solid body | 1 | PASS |
| osa-dryer-assembly | trunk-front | volume (mm3) | OCP 177913.947 / Fusion 177913.947 | PASS |
| osa-dryer-assembly | trunk-front | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | trunk-front | solid body | 1 | PASS |
| osa-dryer-assembly | trunk-rear | volume (mm3) | OCP 223308.512 / Fusion 223308.512 | PASS |
| osa-dryer-assembly | trunk-rear | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | trunk-rear | solid body | 1 | PASS |
| osa-dryer-assembly | nozzle-bars (40 x 8 aluminium flat bar: 2 sides, top, bottom) | volume (mm3) (4 bodies added) | OCP 234860.381 / Fusion 234860.381 | PASS |
| osa-dryer-assembly | nozzle-bars (40 x 8 aluminium flat bar: 2 sides, top, bottom) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | nozzle-bars (40 x 8 aluminium flat bar: 2 sides, top, bottom) | solid body | 1 | PASS |
| osa-dryer-assembly | nozzle-foam (bought, 2 mm closed-cell foam tape 8 wide, 900, compressed to 1 on the bulkhead) | volume (mm3) (4 bodies added) | OCP 5760.957 / Fusion 5760.957 | PASS |
| osa-dryer-assembly | nozzle-foam (bought, 2 mm closed-cell foam tape 8 wide, 900, compressed to 1 on the bulkhead) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | nozzle-foam (bought, 2 mm closed-cell foam tape 8 wide, 900, compressed to 1 on the bulkhead) | solid body | 1 | PASS |
| osa-dryer-assembly | riser-hardware (bought, 70 x M4 x 8 and M4 x 10 button heads) | volume (mm3) (70 bodies added) | OCP 12758.223 / Fusion 12758.221 | PASS |
| osa-dryer-assembly | riser-hardware (bought, 70 x M4 x 8 and M4 x 10 button heads) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | riser-hardware (bought, 70 x M4 x 8 and M4 x 10 button heads) | solid body | 1 | PASS |
| osa-dryer-assembly | door-switch (bought, two-contact plunger switch, envelope) | volume (mm3) | OCP 34081.250 / Fusion 34081.249 | PASS |
| osa-dryer-assembly | door-switch (bought, two-contact plunger switch, envelope) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | door-switch (bought, two-contact plunger switch, envelope) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-door-switch (bought, 2 x M4 x 8 button head into the switch's tapped ears) | volume (mm3) (2 bodies added) | OCP 357.340 / Fusion 357.340 | PASS |
| osa-dryer-assembly | hardware-door-switch (bought, 2 x M4 x 8 button head into the switch's tapped ears) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-door-switch (bought, 2 x M4 x 8 button head into the switch's tapped ears) | solid body | 1 | PASS |
| osa-dryer-assembly | ps1-bracket (angle 20x20x2, 60) | volume (mm3) | OCP 4363.650 / Fusion 4363.650 | PASS |
| osa-dryer-assembly | ps1-bracket (angle 20x20x2, 60) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | ps1-bracket (angle 20x20x2, 60) | solid body | 1 | PASS |
| osa-dryer-assembly | ps1-air-proving-switch (bought, envelope) | volume (mm3) | OCP 100578.329 / Fusion 100578.329 | PASS |
| osa-dryer-assembly | ps1-air-proving-switch (bought, envelope) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | ps1-air-proving-switch (bought, envelope) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-ps1 (bought, 2 x M6 x 12 hex, nuts, through the base pan; 2 x M4 x 8 button head into the switch) | volume (mm3) (6 bodies added) | OCP 2638.352 / Fusion 2638.351 | PASS |
| osa-dryer-assembly | hardware-ps1 (bought, 2 x M6 x 12 hex, nuts, through the base pan; 2 x M4 x 8 button head into the switch) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-ps1 (bought, 2 x M6 x 12 hex, nuts, through the base pan; 2 x M4 x 8 button head into the switch) | solid body | 1 | PASS |
| osa-dryer-assembly | exhaust-thermostats (bought, TF2 thermal fuse, T_HI and T_LO cycling thermostats, envelopes on the blower outlet) | volume (mm3) (3 bodies added) | OCP 23221.148 / Fusion 23221.148 | PASS |
| osa-dryer-assembly | exhaust-thermostats (bought, TF2 thermal fuse, T_HI and T_LO cycling thermostats, envelopes on the blower outlet) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | exhaust-thermostats (bought, TF2 thermal fuse, T_HI and T_LO cycling thermostats, envelopes on the blower outlet) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-exhaust-thermostats (bought, 6 x M4 x 8 button head into the housing) | volume (mm3) (6 bodies added) | OCP 1072.020 / Fusion 1072.019 | PASS |
| osa-dryer-assembly | hardware-exhaust-thermostats (bought, 6 x M4 x 8 button head into the housing) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-exhaust-thermostats (bought, 6 x M4 x 8 button head into the housing) | solid body | 1 | PASS |
| osa-dryer-assembly | blower-plate | volume (mm3) | OCP 70112.794 / Fusion 70112.794 | PASS |
| osa-dryer-assembly | blower-plate | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | blower-plate | solid body | 1 | PASS |
| osa-dryer-assembly | blower-plate-feet (angle 20x20x2, 2 x 90) | volume (mm3) (2 bodies added) | OCP 13287.301 / Fusion 13287.301 | PASS |
| osa-dryer-assembly | blower-plate-feet (angle 20x20x2, 2 x 90) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | blower-plate-feet (angle 20x20x2, 2 x 90) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-blower-plate (bought, 4 x M4 x 8 button head into the housing, 4 x M4 x 8 and nuts into the feet, 4 x M6 x 12 hex, washers, nuts through the base pan) | volume (mm3) (20 bodies added) | OCP 6357.217 / Fusion 6357.217 | PASS |
| osa-dryer-assembly | hardware-blower-plate (bought, 4 x M4 x 8 button head into the housing, 4 x M4 x 8 and nuts into the feet, 4 x M6 x 12 hex, washers, nuts through the base pan) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-blower-plate (bought, 4 x M4 x 8 button head into the housing, 4 x M4 x 8 and nuts into the feet, 4 x M6 x 12 hex, washers, nuts through the base pan) | solid body | 1 | PASS |
| osa-dryer-assembly | exhaust-duct (bought, 4 in aluminium pipe, 102 x 1, cut to length, one 6.5 hole for the tap) | volume (mm3) | OCP 193361.673 / Fusion 193361.597 | PASS |
| osa-dryer-assembly | exhaust-duct (bought, 4 in aluminium pipe, 102 x 1, cut to length, one 6.5 hole for the tap) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | exhaust-duct (bought, 4 in aluminium pipe, 102 x 1, cut to length, one 6.5 hole for the tap) | solid body | 1 | PASS |
| osa-dryer-assembly | exhaust-clamps (bought, 2 x worm-drive hose clamps for 102, envelopes) | volume (mm3) (4 bodies added) | OCP 10700.378 / Fusion 10700.378 | PASS |
| osa-dryer-assembly | exhaust-clamps (bought, 2 x worm-drive hose clamps for 102, envelopes) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | exhaust-clamps (bought, 2 x worm-drive hose clamps for 102, envelopes) | solid body | 1 | PASS |
| osa-dryer-assembly | exhaust-tap-barb (bought, 1/8 NPT or M6 brass barb fitting with a locknut, 5 mm barb, envelope) | volume (mm3) | OCP 1215.319 / Fusion 1215.319 | PASS |
| osa-dryer-assembly | exhaust-tap-barb (bought, 1/8 NPT or M6 brass barb fitting with a locknut, 5 mm barb, envelope) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | exhaust-tap-barb (bought, 1/8 NPT or M6 brass barb fitting with a locknut, 5 mm barb, envelope) | solid body | 1 | PASS |
| osa-dryer-assembly | ps1-tube (bought, 6 mm silicone tube from the tap to PS1, drawn on its route) | volume (mm3) | OCP 11236.853 / Fusion 11236.845 | PASS |
| osa-dryer-assembly | ps1-tube (bought, 6 mm silicone tube from the tap to PS1, drawn on its route) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | ps1-tube (bought, 6 mm silicone tube from the tap to PS1, drawn on its route) | solid body | 1 | PASS |
| osa-dryer-assembly | th1-exhaust-thermistor (bought, 10 k NTC appliance thermistor, envelope) | volume (mm3) | OCP 17281.340 / Fusion 17281.340 | PASS |
| osa-dryer-assembly | th1-exhaust-thermistor (bought, 10 k NTC appliance thermistor, envelope) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | th1-exhaust-thermistor (bought, 10 k NTC appliance thermistor, envelope) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-th1 (bought, 1 x M4 x 20 button head from inside the lint box, nut on the body) | volume (mm3) (2 bodies added) | OCP 420.925 / Fusion 420.925 | PASS |
| osa-dryer-assembly | hardware-th1 (bought, 1 x M4 x 20 button head from inside the lint box, nut on the body) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-th1 (bought, 1 x M4 x 20 button head from inside the lint box, nut on the body) | solid body | 1 | PASS |
| osa-dryer-assembly | moisture-bars (bought, dryer moisture sensor bar set, two stainless strips on an insulating base, envelope) | volume (mm3) | OCP 20769.531 / Fusion 20769.531 | PASS |
| osa-dryer-assembly | moisture-bars (bought, dryer moisture sensor bar set, two stainless strips on an insulating base, envelope) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | moisture-bars (bought, dryer moisture sensor bar set, two stainless strips on an insulating base, envelope) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-moisture-bars (bought, 2 x M4 x 16 button head from the drum side, nuts in the front gap) | volume (mm3) (4 bodies added) | OCP 741.319 / Fusion 741.319 | PASS |
| osa-dryer-assembly | hardware-moisture-bars (bought, 2 x M4 x 16 button head from the drum side, nuts in the front gap) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-moisture-bars (bought, 2 x M4 x 16 button head from the drum side, nuts in the front gap) | solid body | 1 | PASS |
| osa-dryer-assembly | entry-blank | volume (mm3) | OCP 3865.933 / Fusion 3865.933 | PASS |
| osa-dryer-assembly | entry-blank | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | entry-blank | solid body | 1 | PASS |
| osa-dryer-assembly | entry-blank-2 (the second entry-blank, cut two to drawings/entry-blank.dxf; on the condensate drain) | volume (mm3) | OCP 3865.933 / Fusion 3865.933 | PASS |
| osa-dryer-assembly | entry-blank-2 (the second entry-blank, cut two to drawings/entry-blank.dxf; on the condensate drain) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | entry-blank-2 (the second entry-blank, cut two to drawings/entry-blank.dxf; on the condensate drain) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-entry-blanks (bought, 4 x M4 x 8 button head, nuts) | volume (mm3) (8 bodies added) | OCP 1080.514 / Fusion 1080.514 | PASS |
| osa-dryer-assembly | hardware-entry-blanks (bought, 4 x M4 x 8 button head, nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-entry-blanks (bought, 4 x M4 x 8 button head, nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | cable-clamps (bought, 4 x nylon P-clip for a 12 mm bundle, envelopes) | volume (mm3) (8 bodies added) | OCP 3409.264 / Fusion 3409.264 | PASS |
| osa-dryer-assembly | cable-clamps (bought, 4 x nylon P-clip for a 12 mm bundle, envelopes) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | cable-clamps (bought, 4 x nylon P-clip for a 12 mm bundle, envelopes) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-cable-clamps (bought, 4 x M4 x 8 button head, nuts under the pan) | volume (mm3) (8 bodies added) | OCP 1080.514 / Fusion 1080.514 | PASS |
| osa-dryer-assembly | hardware-cable-clamps (bought, 4 x M4 x 8 button head, nuts under the pan) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-cable-clamps (bought, 4 x M4 x 8 button head, nuts under the pan) | solid body | 1 | PASS |
| osa-dryer-assembly | roller-front-1 (bought) | volume (mm3) | OCP 68521.081 / Fusion 68521.081 | PASS |
| osa-dryer-assembly | roller-front-1 (bought) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | roller-front-1 (bought) | solid body | 1 | PASS |
| osa-dryer-assembly | roller-rear-1 (bought) | volume (mm3) | OCP 68521.081 / Fusion 68521.081 | PASS |
| osa-dryer-assembly | roller-rear-1 (bought) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | roller-rear-1 (bought) | solid body | 1 | PASS |
| osa-dryer-assembly | roller-front-2 (bought) | volume (mm3) | OCP 68521.081 / Fusion 68521.081 | PASS |
| osa-dryer-assembly | roller-front-2 (bought) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | roller-front-2 (bought) | solid body | 1 | PASS |
| osa-dryer-assembly | roller-rear-2 (bought) | volume (mm3) | OCP 68521.081 / Fusion 68521.081 | PASS |
| osa-dryer-assembly | roller-rear-2 (bought) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | roller-rear-2 (bought) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-roller-studs (bought, 4 x ISO 7379 shoulder screws 10 x 35 M8, 1.0 shims, spacers 16 x 10.5 x 8.5, M8 washers and nuts) | volume (mm3) (20 bodies added) | OCP 26570.921 / Fusion 26570.920 | PASS |
| osa-dryer-assembly | hardware-roller-studs (bought, 4 x ISO 7379 shoulder screws 10 x 35 M8, 1.0 shims, spacers 16 x 10.5 x 8.5, M8 washers and nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-roller-studs (bought, 4 x ISO 7379 shoulder screws 10 x 35 M8, 1.0 shims, spacers 16 x 10.5 x 8.5, M8 washers and nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | belt (bought, PJ 5 rib) | volume (mm3) | OCP 93324.744 / Fusion 93324.744 | PASS |
| osa-dryer-assembly | belt (bought, PJ 5 rib) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | belt (bought, PJ 5 rib) | solid body | 1 | PASS |
| osa-dryer-assembly | idler-pulley (bought, flat idler 40 with bearing) | volume (mm3) | OCP 18849.085 / Fusion 18849.085 | PASS |
| osa-dryer-assembly | idler-pulley (bought, flat idler 40 with bearing) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | idler-pulley (bought, flat idler 40 with bearing) | solid body | 1 | PASS |
| osa-dryer-assembly | idler-arm (flat bar 25x4, cut to length) | volume (mm3) | OCP 16879.089 / Fusion 16879.089 | PASS |
| osa-dryer-assembly | idler-arm (flat bar 25x4, cut to length) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | idler-arm (flat bar 25x4, cut to length) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-idler-axle (bought, M8 x 30 bolt, nut) | volume (mm3) | OCP 2443.760 / Fusion 2443.760 | PASS |
| osa-dryer-assembly | hardware-idler-axle (bought, M8 x 30 bolt, nut) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-idler-axle (bought, M8 x 30 bolt, nut) | solid body | 1 | PASS |
| osa-dryer-assembly | idler-bracket (angle 40x40x3, cut to length) | volume (mm3) | OCP 11180.667 / Fusion 11180.666 | PASS |
| osa-dryer-assembly | idler-bracket (angle 40x40x3, cut to length) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | idler-bracket (angle 40x40x3, cut to length) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-idler-pivot (bought, M8 x 25 bolt, nut) | volume (mm3) | OCP 1865.707 / Fusion 1865.707 | PASS |
| osa-dryer-assembly | hardware-idler-pivot (bought, M8 x 25 bolt, nut) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-idler-pivot (bought, M8 x 25 bolt, nut) | solid body | 1 | PASS |
| osa-dryer-assembly | spring-bracket (angle 40x40x3, cut to length) | volume (mm3) | OCP 8977.190 / Fusion 8977.190 | PASS |
| osa-dryer-assembly | spring-bracket (angle 40x40x3, cut to length) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | spring-bracket (angle 40x40x3, cut to length) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-idler-spring-posts (bought, 2 x M5 shoulder posts) | volume (mm3) (2 bodies added) | OCP 1256.637 / Fusion 1256.637 | PASS |
| osa-dryer-assembly | hardware-idler-spring-posts (bought, 2 x M5 shoulder posts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-idler-spring-posts (bought, 2 x M5 shoulder posts) | solid body | 1 | PASS |
| osa-dryer-assembly | idler-spring (bought, extension spring) | volume (mm3) | OCP 7580.847 / Fusion 7580.847 | PASS |
| osa-dryer-assembly | idler-spring (bought, extension spring) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | idler-spring (bought, extension spring) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-idler-brackets (bought, 4 x M6 x 12 hex, nuts, through the base pan) | volume (mm3) (8 bodies added) | OCP 4562.023 / Fusion 4562.023 | PASS |
| osa-dryer-assembly | hardware-idler-brackets (bought, 4 x M6 x 12 hex, nuts, through the base pan) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-idler-brackets (bought, 4 x M6 x 12 hex, nuts, through the base pan) | solid body | 1 | PASS |
| post-1 | Body1 | volume (mm3) | OCP 1088617.560 / Fusion 1088617.559 | PASS |
| post-1 | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| post-1 | Body1 | face count | OCP 59 / Fusion 59 | PASS |
| post-1 | Body1 | solid body | 1 | PASS |
| post-2 | Body1 | volume (mm3) | OCP 1088617.560 / Fusion 1088617.559 | PASS |
| post-2 | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| post-2 | Body1 | face count | OCP 59 / Fusion 59 | PASS |
| post-2 | Body1 | solid body | 1 | PASS |
| post-3 | Body1 | volume (mm3) | OCP 1088617.560 / Fusion 1088617.559 | PASS |
| post-3 | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| post-3 | Body1 | face count | OCP 59 / Fusion 59 | PASS |
| post-3 | Body1 | solid body | 1 | PASS |
| post-4 | Body1 | volume (mm3) | OCP 1088617.560 / Fusion 1088617.559 | PASS |
| post-4 | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| post-4 | Body1 | face count | OCP 59 / Fusion 59 | PASS |
| post-4 | Body1 | solid body | 1 | PASS |
| power-module-barrier | Body1 | volume (mm3) | OCP 16928.199 / Fusion 16928.199 | PASS |
| power-module-barrier | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| power-module-barrier | Body1 | face count | OCP 12 / Fusion 12 | PASS |
| power-module-barrier | Body1 | solid body | 1 | PASS |
| power-module-cover | Body1 | volume (mm3) | OCP 74108.220 / Fusion 74108.220 | PASS |
| power-module-cover | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| power-module-cover | Body1 | face count | OCP 14 / Fusion 14 | PASS |
| power-module-cover | Body1 | solid body | 1 | PASS |
| power-module-plate | Body1 | volume (mm3) | OCP 161321.526 / Fusion 161321.526 | PASS |
| power-module-plate | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| power-module-plate | Body1 | face count | OCP 31 / Fusion 31 | PASS |
| power-module-plate | Body1 | solid body | 1 | PASS |
| rail-bottom-front | Body1 | volume (mm3) | OCP 664056.711 / Fusion 664056.711 | PASS |
| rail-bottom-front | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| rail-bottom-front | Body1 | face count | OCP 59 / Fusion 59 | PASS |
| rail-bottom-front | Body1 | solid body | 1 | PASS |
| rail-bottom-left | Body1 | volume (mm3) | OCP 729373.765 / Fusion 729373.765 | PASS |
| rail-bottom-left | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| rail-bottom-left | Body1 | face count | OCP 59 / Fusion 59 | PASS |
| rail-bottom-left | Body1 | solid body | 1 | PASS |
| rail-bottom-rear | Body1 | volume (mm3) | OCP 664056.711 / Fusion 664056.711 | PASS |
| rail-bottom-rear | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| rail-bottom-rear | Body1 | face count | OCP 59 / Fusion 59 | PASS |
| rail-bottom-rear | Body1 | solid body | 1 | PASS |
| rail-bottom-right | Body1 | volume (mm3) | OCP 729373.765 / Fusion 729373.765 | PASS |
| rail-bottom-right | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| rail-bottom-right | Body1 | face count | OCP 59 / Fusion 59 | PASS |
| rail-bottom-right | Body1 | solid body | 1 | PASS |
| rail-mid-front-left | Body1 | volume (mm3) | OCP 146963.371 / Fusion 146963.370 | PASS |
| rail-mid-front-left | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| rail-mid-front-left | Body1 | face count | OCP 59 / Fusion 59 | PASS |
| rail-mid-front-left | Body1 | solid body | 1 | PASS |
| rail-mid-front-right | Body1 | volume (mm3) | OCP 146963.371 / Fusion 146963.370 | PASS |
| rail-mid-front-right | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| rail-mid-front-right | Body1 | face count | OCP 59 / Fusion 59 | PASS |
| rail-mid-front-right | Body1 | solid body | 1 | PASS |
| rail-mid-left | Body1 | volume (mm3) | OCP 729373.765 / Fusion 729373.765 | PASS |
| rail-mid-left | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| rail-mid-left | Body1 | face count | OCP 59 / Fusion 59 | PASS |
| rail-mid-left | Body1 | solid body | 1 | PASS |
| rail-mid-rear | Body1 | volume (mm3) | OCP 664056.711 / Fusion 664056.711 | PASS |
| rail-mid-rear | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| rail-mid-rear | Body1 | face count | OCP 59 / Fusion 59 | PASS |
| rail-mid-rear | Body1 | solid body | 1 | PASS |
| rail-mid-rearcross | Body1 | volume (mm3) | OCP 664056.711 / Fusion 664056.711 | PASS |
| rail-mid-rearcross | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| rail-mid-rearcross | Body1 | face count | OCP 59 / Fusion 59 | PASS |
| rail-mid-rearcross | Body1 | solid body | 1 | PASS |
| rail-mid-right | Body1 | volume (mm3) | OCP 729373.765 / Fusion 729373.765 | PASS |
| rail-mid-right | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| rail-mid-right | Body1 | face count | OCP 59 / Fusion 59 | PASS |
| rail-mid-right | Body1 | solid body | 1 | PASS |
| rail-top-front | Body1 | volume (mm3) | OCP 664056.711 / Fusion 664056.711 | PASS |
| rail-top-front | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| rail-top-front | Body1 | face count | OCP 59 / Fusion 59 | PASS |
| rail-top-front | Body1 | solid body | 1 | PASS |
| rail-top-left | Body1 | volume (mm3) | OCP 729373.765 / Fusion 729373.765 | PASS |
| rail-top-left | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| rail-top-left | Body1 | face count | OCP 59 / Fusion 59 | PASS |
| rail-top-left | Body1 | solid body | 1 | PASS |
| rail-top-rear | Body1 | volume (mm3) | OCP 664056.711 / Fusion 664056.711 | PASS |
| rail-top-rear | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| rail-top-rear | Body1 | face count | OCP 59 / Fusion 59 | PASS |
| rail-top-rear | Body1 | solid body | 1 | PASS |
| rail-top-rearcross | Body1 | volume (mm3) | OCP 664056.711 / Fusion 664056.711 | PASS |
| rail-top-rearcross | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| rail-top-rearcross | Body1 | face count | OCP 59 / Fusion 59 | PASS |
| rail-top-rearcross | Body1 | solid body | 1 | PASS |
| rail-top-right | Body1 | volume (mm3) | OCP 729373.765 / Fusion 729373.765 | PASS |
| rail-top-right | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| rail-top-right | Body1 | face count | OCP 59 / Fusion 59 | PASS |
| rail-top-right | Body1 | solid body | 1 | PASS |
| rear-bulkhead | Body1 | volume (mm3) | OCP 652057.649 / Fusion 652057.649 | PASS |
| rear-bulkhead | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| rear-bulkhead | Body1 | face count | OCP 162 / Fusion 162 | PASS |
| rear-bulkhead | Body1 | solid body | 1 | PASS |
| rear-lower-panel | Body1 | volume (mm3) | OCP 238937.895 / Fusion 238937.895 | PASS |
| rear-lower-panel | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| rear-lower-panel | Body1 | face count | OCP 153 / Fusion 153 | PASS |
| rear-lower-panel | Body1 | solid body | 1 | PASS |
| rear-upper-panel | Body1 | volume (mm3) | OCP 764957.703 / Fusion 764957.703 | PASS |
| rear-upper-panel | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| rear-upper-panel | Body1 | face count | OCP 28 / Fusion 28 | PASS |
| rear-upper-panel | Body1 | solid body | 1 | PASS |
| side-panel-left | Body1 | volume (mm3) | OCP 1123510.182 / Fusion 1123510.182 | PASS |
| side-panel-left | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| side-panel-left | Body1 | face count | OCP 39 / Fusion 39 | PASS |
| side-panel-left | Body1 | solid body | 1 | PASS |
| side-panel-right | Body1 | volume (mm3) | OCP 1123510.182 / Fusion 1123510.182 | PASS |
| side-panel-right | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| side-panel-right | Body1 | face count | OCP 39 / Fusion 39 | PASS |
| side-panel-right | Body1 | solid body | 1 | PASS |
| tier0-faceplate | Body1 | volume (mm3) | OCP 195756.562 / Fusion 195756.562 | PASS |
| tier0-faceplate | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| tier0-faceplate | Body1 | face count | OCP 515 / Fusion 515 | PASS |
| tier0-faceplate | Body1 | solid body | 1 | PASS |
| top-panel | Body1 | volume (mm3) | OCP 774637.955 / Fusion 774637.955 | PASS |
| top-panel | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| top-panel | Body1 | face count | OCP 31 / Fusion 31 | PASS |
| top-panel | Body1 | solid body | 1 | PASS |
| tray-rail-1 | Body1 | volume (mm3) | OCP 151936.620 / Fusion 151936.620 | PASS |
| tray-rail-1 | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| tray-rail-1 | Body1 | face count | OCP 59 / Fusion 59 | PASS |
| tray-rail-1 | Body1 | solid body | 1 | PASS |
| tray-rail-2 | Body1 | volume (mm3) | OCP 151936.620 / Fusion 151936.620 | PASS |
| tray-rail-2 | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| tray-rail-2 | Body1 | face count | OCP 59 / Fusion 59 | PASS |
| tray-rail-2 | Body1 | solid body | 1 | PASS |
| trunk-front | Body1 | volume (mm3) | OCP 177913.947 / Fusion 177913.947 | PASS |
| trunk-front | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| trunk-front | Body1 | face count | OCP 37 / Fusion 37 | PASS |
| trunk-front | Body1 | solid body | 1 | PASS |
| trunk-rear | Body1 | volume (mm3) | OCP 223308.512 / Fusion 223308.512 | PASS |
| trunk-rear | Body1 | bounding box (mm) | max deviation 0.0000 | PASS |
| trunk-rear | Body1 | face count | OCP 23 / Fusion 23 | PASS |
| trunk-rear | Body1 | solid body | 1 | PASS |
| base-pan |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 47 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| basket-far-clamp |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 8 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| basket-far-plate |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 8 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| basket-lip-clamp |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 10 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| basket-lip-plate |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 12 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| bay-ceiling |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 25 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| blower-plate |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 12 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| console-cap |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 14 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| console-cheek-left |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 9 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| console-cheek-right |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 9 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| console-face |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 18 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| console-post-1 |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 5 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| console-post-2 |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 5 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| console-post-3 |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 5 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| console-post-4 |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 5 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| console-rail-front |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 5 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| console-rail-left |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 5 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| console-rail-rear |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 5 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| console-rail-right |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 5 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| console-rear |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 12 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| door-disc |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 5 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| door-ring |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 13 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| drum-ring-front |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 32 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| drum-ring-rear |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 32 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| drum-sheet |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 210 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| drum-splice |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 22 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| entry-blank |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 6 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| felt-seal-front-long |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 2 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| felt-seal-front-short |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 2 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| felt-seal-rear-long |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 2 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| felt-seal-rear-short |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 2 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| front-bulkhead |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 30 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| front-lower-panel |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 124 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| front-upper-panel |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 34 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| heat-module-terminal-plate |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 9 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| heat-module-top |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 23 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| heat-module-tray |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 18 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| heat-module-wall-front |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 12 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| heat-module-wall-left |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 10 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| heat-module-wall-rear |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 12 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| heat-module-wall-right |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 10 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| hood-bottom |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 15 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| hood-top |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 18 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| liner-splice |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 4 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| liner |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 4 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| lint-box-back |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 23 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| lint-box-front |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 18 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| post-1 |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 5 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| post-2 |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 5 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| post-3 |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 5 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| post-4 |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 5 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| power-module-barrier |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 6 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| power-module-cover |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 8 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| power-module-plate |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 25 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| rail-bottom-front |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 5 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| rail-bottom-left |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 5 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| rail-bottom-rear |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 5 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| rail-bottom-right |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 5 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| rail-mid-front-left |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 5 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| rail-mid-front-right |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 5 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| rail-mid-left |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 5 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| rail-mid-rear |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 5 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| rail-mid-rearcross |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 5 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| rail-mid-right |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 5 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| rail-top-front |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 5 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| rail-top-left |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 5 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| rail-top-rear |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 5 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| rail-top-rearcross |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 5 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| rail-top-right |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 5 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| rear-bulkhead |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 156 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| rear-lower-panel |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 83 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| rear-upper-panel |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 22 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| side-panel-left |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 33 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| side-panel-right |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 33 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| tier0-faceplate |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 22 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| top-panel |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 25 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| tray-rail-1 |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 5 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| tray-rail-2 |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 5 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| trunk-front |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 27 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| trunk-rear |  | every cylinder (hole or drum) seen by OCP is seen by Fusion with the same diameter and axis | 17 matched, 0 missing in Fusion, 0 extra in Fusion | PASS |
| osa-dryer-assembly | drum-sheet / front-bulkhead | minimum distance (mm) | OCP 7.700 / Fusion 7.700 | PASS |
| osa-dryer-assembly | drum-sheet / rear-bulkhead | minimum distance (mm) | OCP 9.200 / Fusion 9.200 | PASS |
| osa-dryer-assembly | drum-sheet / bay-ceiling | minimum distance (mm) | OCP 20.000 / Fusion 20.000 | PASS |
| osa-dryer-assembly | drum-sheet / side-panel-left | minimum distance (mm) | OCP 35.000 / Fusion 35.000 | PASS |
| osa-dryer-assembly | drum-sheet / side-panel-right | minimum distance (mm) | OCP 35.000 / Fusion 35.000 | PASS |
| osa-dryer-assembly | drum-sheet / top-panel | minimum distance (mm) | OCP 58.500 / Fusion 58.500 | PASS |
| osa-dryer-assembly | drum-sheet / rail-top-left | minimum distance (mm) | OCP 139.087 / Fusion 139.087 | PASS |
| osa-dryer-assembly | drum-sheet / rail-top-right | minimum distance (mm) | OCP 139.087 / Fusion 139.087 | PASS |
| osa-dryer-assembly | drum-sheet / rail-top-front | minimum distance (mm) | OCP 21.754 / Fusion 21.754 | PASS |
| osa-dryer-assembly | drum-sheet / roller-front-1 (bought) | minimum distance (mm) | OCP 0.000 / Fusion 0.000 | PASS |
| osa-dryer-assembly | drum-sheet / roller-front-2 (bought) | minimum distance (mm) | OCP 0.000 / Fusion 0.000 | PASS |
| osa-dryer-assembly | drum-sheet / roller-rear-1 (bought) | minimum distance (mm) | OCP 0.000 / Fusion 0.000 | PASS |
| osa-dryer-assembly | drum-sheet / roller-rear-2 (bought) | minimum distance (mm) | OCP 0.000 / Fusion 0.000 | PASS |
| osa-dryer-assembly | drum-sheet / drum-ring-front | minimum distance (mm) | OCP 0.000 / Fusion 0.000 | PASS |
| osa-dryer-assembly | drum-sheet / drum-ring-rear | minimum distance (mm) | OCP 0.000 / Fusion 0.000 | PASS |
| osa-dryer-assembly | drum-sheet / drum-splice | minimum distance (mm) | OCP 0.000 / Fusion 0.000 | PASS |
| osa-dryer-assembly | drum-sheet / baffle-1 (angle, cut to length) | minimum distance (mm) | OCP 0.050 / Fusion 0.050 | PASS |
| osa-dryer-assembly | drum-ring-front / front-bulkhead | minimum distance (mm) | OCP 8.500 / Fusion 8.500 | PASS |
| osa-dryer-assembly | drum-ring-rear / rear-bulkhead | minimum distance (mm) | OCP 10.000 / Fusion 10.000 | PASS |
| osa-dryer-assembly | door-ring / front-upper-panel | minimum distance (mm) | OCP 0.000 / Fusion 0.000 | PASS |
| osa-dryer-assembly | door-disc / door-ring | minimum distance (mm) | OCP 8.000 / Fusion 8.000 | PASS |
| osa-dryer-assembly | console-face / console-cheek-left | minimum distance (mm) | OCP 0.000 / Fusion 0.000 | PASS |
| osa-dryer-assembly | console-face / console-cheek-right | minimum distance (mm) | OCP 0.000 / Fusion 0.000 | PASS |
| osa-dryer-assembly | console-face / top-panel | minimum distance (mm) | OCP 0.000 / Fusion 0.000 | PASS |
| osa-dryer-assembly | console-face / console-cap | minimum distance (mm) | OCP 0.000 / Fusion 0.000 | PASS |
| osa-dryer-assembly | front-bulkhead / bay-ceiling | minimum distance (mm) | OCP 0.500 / Fusion 0.500 | PASS |
| osa-dryer-assembly | rear-bulkhead / bay-ceiling | minimum distance (mm) | OCP 0.500 / Fusion 0.500 | PASS |
| osa-dryer-assembly | lint-box-front / front-upper-panel | minimum distance (mm) | OCP 7.000 / Fusion 7.000 | PASS |
| osa-dryer-assembly | lint-box-front / liner | minimum distance (mm) | OCP 0.200 / Fusion 0.200 | PASS |
| osa-dryer-assembly | liner / door-ring | minimum distance (mm) | OCP 0.000 / Fusion 0.000 | PASS |
| osa-dryer-assembly | liner / front-bulkhead | minimum distance (mm) | OCP 0.200 / Fusion 0.200 | PASS |
| osa-dryer-assembly | basket-far-plate / lint-box-front | minimum distance (mm) | OCP 0.500 / Fusion 0.500 | PASS |
| osa-dryer-assembly | basket-lip-plate / drum-ring-front | minimum distance (mm) | OCP 5.701 / Fusion 5.701 | PASS |
| osa-dryer-assembly | basket-lip-plate / felt-seal-front-long | minimum distance (mm) | OCP 4.500 / Fusion 4.500 | PASS |
| osa-dryer-assembly | trunk-front / rear-bulkhead | minimum distance (mm) | OCP 41.000 / Fusion 41.000 | PASS |
| osa-dryer-assembly | trunk-front / rail-mid-rearcross | minimum distance (mm) | OCP 1.000 / Fusion 1.000 | PASS |
| osa-dryer-assembly | trunk-rear / rail-mid-rear | minimum distance (mm) | OCP 4.500 / Fusion 4.500 | PASS |
| osa-dryer-assembly | trunk-front / bay-ceiling | minimum distance (mm) | OCP 2.000 / Fusion 2.000 | PASS |
| osa-dryer-assembly | hood-top / rail-mid-rearcross | minimum distance (mm) | OCP 2.000 / Fusion 2.000 | PASS |
| osa-dryer-assembly | hood-bottom / heat-module-collar (bought, 125 flanged starting collar, cut to 55.5) | minimum distance (mm) | OCP 3.354 / Fusion 3.354 | PASS |
| osa-dryer-assembly | heat-module-top / bay-ceiling | minimum distance (mm) | OCP 128.500 / Fusion 128.500 | PASS |
| osa-dryer-assembly | motor (bought) / base-pan | minimum distance (mm) | OCP 50.000 / Fusion 50.000 | PASS |
| osa-dryer-assembly | blower (bought) / front-bulkhead | minimum distance (mm) | OCP 56.223 / Fusion 56.223 | PASS |
| osa-dryer-assembly | lint-box-back / front-bulkhead | minimum distance (mm) | OCP 0.000 / Fusion 0.000 | PASS |
| osa-dryer-assembly | pulley (bought) / bay-ceiling | minimum distance (mm) | OCP 169.000 / Fusion 169.000 | PASS |
| osa-dryer-assembly | exhaust-duct (bought, 4 in aluminium pipe, 102 x 1, cut to length, one 6.5 hole for the tap) / rear-lower-panel | minimum distance (mm) | OCP 2.000 / Fusion 2.000 | PASS |
| osa-dryer-assembly | blower-plate / blower (bought) | minimum distance (mm) | OCP 0.000 / Fusion 0.000 | PASS |
| osa-dryer-assembly | blower-plate / tray-rail-2 | minimum distance (mm) | OCP 20.000 / Fusion 20.000 | PASS |
| osa-dryer-assembly | entry-blank / rear-lower-panel | minimum distance (mm) | OCP 0.000 / Fusion 0.000 | PASS |
| osa-dryer-assembly | power-module-plate / trunk-front | minimum distance (mm) | OCP 20.000 / Fusion 20.000 | PASS |
| osa-dryer-assembly | power-module-plate / bay-ceiling | minimum distance (mm) | OCP 1.000 / Fusion 1.000 | PASS |
| osa-dryer-assembly | drum-sheet / front-upper-panel | minimum distance (mm) | OCP 49.200 / Fusion 49.200 | PASS |
| osa-dryer-assembly | heat-module-wall-front / idler-spring (bought, extension spring) | minimum distance (mm) | OCP 5.000 / Fusion 5.000 | PASS |
| osa-dryer-assembly | heat-module-tray / idler-spring (bought, extension spring) | minimum distance (mm) | OCP 3.000 / Fusion 3.000 | PASS |
| osa-dryer-assembly | heat-module-terminal-plate / heat-module-wall-rear | minimum distance (mm) | OCP 7.000 / Fusion 7.000 | PASS |
| osa-dryer-assembly | power-module-cover / rear-upper-panel | minimum distance (mm) | OCP 20.500 / Fusion 20.500 | PASS |
| osa-dryer-assembly | power-module-plate / rail-mid-rearcross | minimum distance (mm) | OCP 0.000 / Fusion 0.000 | PASS |
| osa-dryer-assembly | felt-seal-rear-long / drum-ring-rear | minimum distance (mm) | OCP 0.000 / Fusion 0.000 | PASS |
| osa-dryer-assembly | felt-seal-front-long / drum-ring-front | minimum distance (mm) | OCP 0.500 / Fusion 0.500 | PASS |
| osa-dryer-assembly | heat-module-tray / tray-rail-1 | minimum distance (mm) | OCP 0.000 / Fusion 0.000 | PASS |

## 4. Clearances measured in the assembly (mm)

| part a | part b | minimum distance |
|---|---|---|
| drum-sheet | front-bulkhead | 7.700 |
| drum-sheet | rear-bulkhead | 9.200 |
| drum-sheet | bay-ceiling | 20.000 |
| drum-sheet | side-panel-left | 35.000 |
| drum-sheet | side-panel-right | 35.000 |
| drum-sheet | top-panel | 58.500 |
| drum-sheet | rail-top-left | 139.087 |
| drum-sheet | rail-top-right | 139.087 |
| drum-sheet | rail-top-front | 21.754 |
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
| console-face | top-panel | 0.000 |
| console-face | console-cap | 0.000 |
| front-bulkhead | bay-ceiling | 0.500 |
| rear-bulkhead | bay-ceiling | 0.500 |
| lint-box-bars (30 x 8 aluminium flat bar: 2 sides mitred at the top, 1 bottom) | rail-mid-front-left | 4.000 |
| lint-box-bars (30 x 8 aluminium flat bar: 2 sides mitred at the top, 1 bottom) | rail-mid-front-right | 4.000 |
| lint-box-bars (30 x 8 aluminium flat bar: 2 sides mitred at the top, 1 bottom) | front-bulkhead | 1.500 |
| lint-box-front | front-upper-panel | 7.000 |
| lint-box-front | liner | 0.200 |
| lint-box-bars (30 x 8 aluminium flat bar: 2 sides mitred at the top, 1 bottom) | liner | 0.200 |
| liner | door-ring | 0.000 |
| liner | front-bulkhead | 0.200 |
| liner | front-upper-panel | 3.000 |
| basket-mesh (bought, stainless 18 x 16 mesh strip, 42 wide, 350 long, wrapped and folded 5 at each edge) | front-bulkhead | 0.900 |
| basket-mesh (bought, stainless 18 x 16 mesh strip, 42 wide, 350 long, wrapped and folded 5 at each edge) | liner | 1.900 |
| basket-far-plate | lint-box-front | 0.500 |
| basket-lip-plate | drum-ring-front | 5.701 |
| basket-lip-plate | felt-seal-front-long | 4.500 |
| basket-pull (bought, D-pull, 64 mm centres, 25 projection) | door-disc | 28.000 |
| trunk-front | rear-bulkhead | 41.000 |
| trunk-front | rail-mid-rearcross | 1.000 |
| trunk-rear | rail-mid-rear | 4.500 |
| trunk-front | bay-ceiling | 2.000 |
| hood-top | rail-mid-rearcross | 2.000 |
| hood-bottom | heat-module-collar (bought, 125 flanged starting collar, cut to 55.5) | 3.354 |
| heat-module-top | bay-ceiling | 128.500 |
| heat-module-collar (bought, 125 flanged starting collar, cut to 55.5) | hood-bottom | 3.354 |
| heat-module-collar (bought, 125 flanged starting collar, cut to 55.5) | hood-gasket (bought, 3 mm foam ring 150 x 125, glued under the hood) | not measured |
| heat-module-wall-front | idler-spring (bought, extension spring) | 5.000 |
| heat-module-tray | idler-spring (bought, extension spring) | 3.000 |
| heat-module-devices (bought, envelopes: 2 end clamps, X_HM mains and SELV strips, partition, K_HEAT, CS1) | rear-lower-panel | 21.000 |
| heat-module-thermostats (bought, 279816 class high-limit and thermal cut-off, envelopes) | hood-bottom | 43.500 |
| heat-module-tray | tray-rail-1 | 0.000 |
| heat-module-tray | rail-bottom-rear | 23.060 |
| heat-module-terminal-plate | heat-module-wall-rear | 7.000 |
| power-module-plate | trunk-front | 20.000 |
| power-module-plate | rail-mid-rearcross | 0.000 |
| power-module-plate | post-3 | 57.414 |
| power-module-cover | rear-upper-panel | 20.500 |
| power-module-plate | bay-ceiling | 1.000 |
| power-module-rail-B1-devices (bought, envelopes: RLY_MOTOR, RLY_HEAT, RLY_HEAT_LO: 3 x 38.51 class, PTC1 to PTC3 in fuse terminals, F2: UK 5-HESI, X4 heat module SELV: 4 x UK 2.5 N, 2 end clamps) | rear-upper-panel | 19.500 |
| power-module-rail-A1-devices (bought, envelopes: X1 cord: 4 x UK 6 N (L1, L2, N, PE), CB1: 1P MCB, F1: UK 5-HESI fuse terminal, 2 end clamps) | power-module-cover | 7.500 |
| power-cord (bought) | bay-ceiling | 6.500 |
| power-cord (bought) | grommets (bought, 5 x rubber grommets for 1.5 panels: 22 mm hole x 2, 30 mm hole x 1, 16 mm hole x 2) | 3.000 |
| power-cord (bought) | power-module-rail-A1-devices (bought, envelopes: X1 cord: 4 x UK 6 N (L1, L2, N, PE), CB1: 1P MCB, F1: UK 5-HESI fuse terminal, 2 end clamps) | 16.500 |
| hardware-roller-studs (bought, 4 x ISO 7379 shoulder screws 10 x 35 M8, 1.0 shims, spacers 16 x 10.5 x 8.5, M8 washers and nuts) | lint-box-bars (30 x 8 aluminium flat bar: 2 sides mitred at the top, 1 bottom) | 6.173 |
| hardware-roller-studs (bought, 4 x ISO 7379 shoulder screws 10 x 35 M8, 1.0 shims, spacers 16 x 10.5 x 8.5, M8 washers and nuts) | drum-sheet | 22.000 |
| hardware-roller-studs (bought, 4 x ISO 7379 shoulder screws 10 x 35 M8, 1.0 shims, spacers 16 x 10.5 x 8.5, M8 washers and nuts) | roller-front-1 (bought) | 0.000 |
| drum-glides-front (bought, 2 x nylon drum glide pads, 45 x 20 x 8) | drum-ring-front | 0.500 |
| drum-glides-rear (bought, 2 x nylon drum glide pads, 45 x 20 x 9.5) | drum-ring-rear | 0.500 |
| drum-glides-front (bought, 2 x nylon drum glide pads, 45 x 20 x 8) | felt-seal-front-long | 0.458 |
| drum-glides-front (bought, 2 x nylon drum glide pads, 45 x 20 x 8) | felt-seal-front-short | 0.458 |
| motor (bought) | base-pan | 50.000 |
| blower (bought) | front-bulkhead | 56.223 |
| blower (bought) | spool-bars (40 x 8 aluminium flat bar: 2 x 156, 2 x 140) | not measured |
| blower (bought) | ps1-air-proving-switch (bought, envelope) | 34.180 |
| pulley (bought) | bay-ceiling | 169.000 |
| exhaust-duct (bought, 4 in aluminium pipe, 102 x 1, cut to length, one 6.5 hole for the tap) | rear-lower-panel | 2.000 |
| exhaust-duct (bought, 4 in aluminium pipe, 102 x 1, cut to length, one 6.5 hole for the tap) | tray-rail-2 | 57.747 |
| drum-sheet | front-upper-panel | 49.200 |
| belt (bought, PJ 5 rib) | drum-sheet | 0.000 |
| belt (bought, PJ 5 rib) | pulley (bought) | 0.000 |
| belt (bought, PJ 5 rib) | idler-pulley (bought, flat idler 40 with bearing) | 0.000 |
| belt (bought, PJ 5 rib) | bay-ceiling | 13.565 |
| belt (bought, PJ 5 rib) | motor (bought) | 4.162 |
| belt (bought, PJ 5 rib) | heat-module-tray | 46.573 |
| door-hinge-1-fixed (bought, flag hinge, pinned half) | door-disc | 1.775 |
| door-hinge-2-swing (bought, flag hinge, lift-off half) | door-ring | 1.523 |
| door-seal (bought, OEM door seal) | door-ring | 2.000 |
| felt-seal-rear-long | drum-ring-rear | 0.000 |
| felt-seal-front-long | drum-ring-front | 0.500 |
| felt-seal-front-long | drum-sheet | 2.200 |
| felt-seal-rear-long | drum-sheet | 2.200 |
| felt-seal-front-short | drum-ring-front | 0.500 |
| tier0-faceplate | console-face | 0.000 |
| hood-bottom | heat-module-tray | 168.500 |
| hood-bottom | belt (bought, PJ 5 rib) | 40.000 |
| nozzle-bars (40 x 8 aluminium flat bar: 2 sides, top, bottom) | rear-bulkhead | 1.000 |
| lint-box-front | hardware-door-ring (bought, 8 x M4 x 8 button head, nuts) | 2.500 |
| door-switch (bought, two-contact plunger switch, envelope) | lint-box-front | 0.170 |
| door-switch (bought, two-contact plunger switch, envelope) | door-disc | 0.500 |
| exhaust-thermostats (bought, TF2 thermal fuse, T_HI and T_LO cycling thermostats, envelopes on the blower outlet) | motor (bought) | 83.895 |
| console-post-1 | top-panel | 0.000 |
| console-post-1 | console-cheek-left | 0.000 |
| console-rail-front | console-cap | 0.000 |
| console-rear | rear-upper-panel | 0.000 |
| console-cheek-left | side-panel-left | 0.000 |
| tier0-k1-relay-on-din-rail (bought) | console-rail-front | 82.000 |
| tier0-k1-relay-on-din-rail (bought) | top-panel | 23.000 |
| power-cord (bought) | cord-bushing (bought, PG16 strain relief) | 0.100 |
| power-cord (bought) | feet (bought, 4 x M8 leveling feet, 50 pad) | 20.500 |
| power-cord (bought) | base-pan | 6.000 |
| feet (bought, 4 x M8 leveling feet, 50 pad) | base-pan | 0.000 |
| hardware-drum-tabs (bought, 60 x M4 x 8 button head, nuts) | front-bulkhead | 2.500 |
| idler-pulley (bought, flat idler 40 with bearing) | motor (bought) | 4.500 |
| hardware-idler-axle (bought, M8 x 30 bolt, nut) | motor (bought) | 7.000 |
| blower-plate | blower (bought) | 0.000 |
| blower-plate | spool-foam (bought, 6 mm closed-cell foam tape 8 wide, 600, compressed to 4 on the blower plate) | 0.000 |
| th1-exhaust-thermistor (bought, 10 k NTC appliance thermistor, envelope) | blower-plate | 22.000 |
| exhaust-duct (bought, 4 in aluminium pipe, 102 x 1, cut to length, one 6.5 hole for the tap) | heat-module-tray | 55.922 |
| moisture-bars (bought, dryer moisture sensor bar set, two stainless strips on an insulating base, envelope) | basket-lip-plate | 40.148 |
| moisture-bars (bought, dryer moisture sensor bar set, two stainless strips on an insulating base, envelope) | drum-ring-front | 1.306 |
| ps1-tube (bought, 6 mm silicone tube from the tap to PS1, drawn on its route) | exhaust-thermostats (bought, TF2 thermal fuse, T_HI and T_LO cycling thermostats, envelopes on the blower outlet) | 16.162 |
| exhaust-clamps (bought, 2 x worm-drive hose clamps for 102, envelopes) | rear-lower-panel | 0.000 |
| entry-blank | rear-lower-panel | 0.000 |
| cable-clamps (bought, 4 x nylon P-clip for a 12 mm bundle, envelopes) | base-pan | 0.000 |
| blower-plate-feet (angle 20x20x2, 2 x 90) | base-pan | 0.000 |
| blower-plate | tray-rail-2 | 20.000 |
| exhaust-duct (bought, 4 in aluminium pipe, 102 x 1, cut to length, one 6.5 hole for the tap) | motor (bought) | 110.948 |
| exhaust-duct (bought, 4 in aluminium pipe, 102 x 1, cut to length, one 6.5 hole for the tap) | exhaust-clamps (bought, 2 x worm-drive hose clamps for 102, envelopes) | 0.000 |

## 5. Inventory

Every part: bounding box, volume, faces. The full feature lists are in `measured-cylinders.csv` (every hole and round surface), `measured-planes.csv` (every flat face) and `measured-loops.csv` (every closed loop of every flat part's section and of every DXF).

| part | solids | X min..max | Y min..max | Z min..max | size | volume mm3 | faces (planar / cylindrical / other) | thickness | section loops |
|---|---|---|---|---|---|---|---|---|---|
| base-pan | 1 | -343.50..343.50 | -0.00..750.00 | -1.50..0.00 | 687.00 x 750.00 x 1.50 | 770130.2 | 53 (6 / 47 / 0) | 1.500 | 44 |
| basket-far-clamp | 1 | -154.55..154.55 | 12.60..14.10 | 366.00..436.76 | 309.11 x 1.50 x 70.76 | 12155.5 | 12 (4 / 8 / 0) | 1.500 | 7 |
| basket-far-plate | 1 | -154.55..154.55 | 9.00..12.00 | 366.00..436.76 | 309.11 x 3.00 x 70.76 | 24347.2 | 12 (4 / 8 / 0) | 3.000 | 7 |
| basket-lip-clamp | 1 | -163.45..163.45 | 45.10..46.60 | 363.00..447.44 | 326.90 x 1.50 x 84.44 | 5002.1 | 16 (6 / 10 / 0) | 1.500 | 8 |
| basket-lip-plate | 1 | -163.45..163.45 | 41.50..44.50 | 363.00..447.44 | 326.90 x 3.00 x 84.44 | 14075.0 | 24 (11 / 13 / 0) | 3.000 | 8 |
| bay-ceiling | 1 | -343.50..343.50 | 42.00..750.00 | 300.00..301.50 | 687.00 x 708.00 x 1.50 | 685439.8 | 55 (30 / 25 / 0) | 1.500 | 29 |
| blower-plate | 1 | -130.00..130.00 | 84.00..85.50 | -0.00..245.00 | 260.00 x 1.50 x 245.00 | 70112.8 | 22 (10 / 12 / 0) | 1.500 | 10 |
| console-cap | 1 | -346.50..346.50 | 610.00..751.50 | 1201.50..1203.00 | 693.00 x 141.50 x 1.50 | 146545.1 | 20 (6 / 14 / 0) | 1.500 | 11 |
| console-cheek-left | 1 | -346.50..-345.00 | 610.00..751.50 | 1000.00..1201.50 | 1.50 x 141.50 x 201.50 | 42473.1 | 15 (6 / 9 / 0) | 1.500 | 6 |
| console-cheek-right | 1 | 345.00..346.50 | 610.00..751.50 | 1000.00..1201.50 | 1.50 x 141.50 x 201.50 | 42473.1 | 15 (6 / 9 / 0) | 1.500 | 6 |
| console-face | 1 | -345.00..345.00 | 610.00..611.50 | 1001.50..1201.50 | 690.00 x 1.50 x 200.00 | 105612.3 | 28 (10 / 18 / 0) | 1.500 | 16 |
| console-post-1 | 1 | -345.00..-305.00 | 611.50..651.50 | 1001.50..1201.50 | 40.00 x 40.00 x 200.00 | 217723.5 | 59 (54 / 5 / 0) | | |
| console-post-2 | 1 | -345.00..-305.00 | 710.00..750.00 | 1001.50..1201.50 | 40.00 x 40.00 x 200.00 | 217723.5 | 59 (54 / 5 / 0) | | |
| console-post-3 | 1 | 305.00..345.00 | 611.50..651.50 | 1001.50..1201.50 | 40.00 x 40.00 x 200.00 | 217723.5 | 59 (54 / 5 / 0) | | |
| console-post-4 | 1 | 305.00..345.00 | 710.00..750.00 | 1001.50..1201.50 | 40.00 x 40.00 x 200.00 | 217723.5 | 59 (54 / 5 / 0) | | |
| console-rail-front | 1 | -305.00..305.00 | 611.50..651.50 | 1161.50..1201.50 | 610.00 x 40.00 x 40.00 | 664056.7 | 59 (54 / 5 / 0) | | |
| console-rail-left | 1 | -345.00..-305.00 | 651.50..710.00 | 1161.50..1201.50 | 40.00 x 58.50 x 40.00 | 63684.1 | 59 (54 / 5 / 0) | | |
| console-rail-rear | 1 | -305.00..305.00 | 710.00..750.00 | 1161.50..1201.50 | 610.00 x 40.00 x 40.00 | 664056.7 | 59 (54 / 5 / 0) | | |
| console-rail-right | 1 | 305.00..345.00 | 651.50..710.00 | 1161.50..1201.50 | 40.00 x 58.50 x 40.00 | 63684.1 | 59 (54 / 5 / 0) | | |
| console-rear | 1 | -345.00..345.00 | 750.00..751.50 | 1000.00..1201.50 | 690.00 x 1.50 x 201.50 | 208107.9 | 18 (6 / 12 / 0) | 1.500 | 9 |
| door-disc | 1 | -270.00..270.00 | -13.50..-11.50 | 361.50..901.50 | 540.00 x 2.00 x 540.00 | 457917.0 | 7 (2 / 5 / 0) | 2.000 | 5 |
| door-ring | 1 | -280.00..280.00 | -3.50..-1.50 | 351.50..911.50 | 560.00 x 2.00 x 560.00 | 145112.1 | 15 (2 / 13 / 0) | 2.000 | 13 |
| drum-ring-front | 1 | -309.20..309.20 | 50.00..52.00 | 322.30..940.70 | 618.40 x 2.00 x 618.40 | 141703.2 | 34 (2 / 32 / 0) | 2.000 | 32 |
| drum-ring-rear | 1 | -309.20..309.20 | 598.00..600.00 | 322.30..940.70 | 618.40 x 2.00 x 618.40 | 141703.2 | 34 (2 / 32 / 0) | 2.000 | 32 |
| drum-sheet | 1 | -310.00..310.00 | 49.20..600.80 | 321.50..941.50 | 620.00 x 551.60 x 620.00 | 873714.1 | 600 (360 / 240 / 0) | | |
| drum-splice | 1 | -29.96..29.96 | 53.00..597.00 | 938.24..940.70 | 59.92 x 544.00 x 2.46 | 32383.4 | 26 (4 / 22 / 0) | | |
| entry-blank | 1 | -260.00..-200.00 | 748.50..750.00 | 128.00..172.00 | 60.00 x 1.50 x 44.00 | 3865.9 | 12 (6 / 6 / 0) | 1.500 | 3 |
| felt-seal-front-long | 1 | -291.00..291.00 | 41.50..49.50 | 340.50..819.43 | 582.00 x 8.00 x 478.93 | 184592.7 | 6 (4 / 2 / 0) | 8.000 | 1 |
| felt-seal-front-short | 1 | -187.93..187.93 | 41.50..49.50 | 839.94..922.50 | 375.85 x 8.00 x 82.56 | 57018.9 | 6 (4 / 2 / 0) | 8.000 | 1 |
| felt-seal-rear-long | 1 | -291.00..291.00 | 600.00..610.00 | 340.50..819.43 | 582.00 x 10.00 x 478.93 | 230740.9 | 6 (4 / 2 / 0) | 10.000 | 1 |
| felt-seal-rear-short | 1 | -187.93..187.93 | 600.00..610.00 | 839.94..922.50 | 375.85 x 10.00 x 82.56 | 71273.6 | 6 (4 / 2 / 0) | 10.000 | 1 |
| front-bulkhead | 1 | -305.00..305.00 | 40.00..41.50 | 265.00..995.00 | 610.00 x 1.50 x 730.00 | 403407.6 | 38 (8 / 30 / 0) | 1.500 | 26 |
| front-lower-panel | 1 | -345.00..345.00 | -1.50..0.00 | -0.00..259.00 | 690.00 x 1.50 x 259.00 | 242871.1 | 242 (118 / 124 / 0) | 1.500 | 65 |
| front-upper-panel | 1 | -345.00..345.00 | -1.50..0.00 | 260.00..1000.00 | 690.00 x 1.50 x 740.00 | 493200.4 | 40 (6 / 34 / 0) | 1.500 | 31 |
| heat-module-terminal-plate | 1 | -145.00..145.00 | 634.00..635.50 | 61.50..161.50 | 290.00 x 1.50 x 100.00 | 43369.1 | 15 (6 / 9 / 0) | 1.500 | 6 |
| heat-module-top | 1 | -145.00..145.00 | 422.00..627.00 | 170.00..171.50 | 290.00 x 205.00 x 1.50 | 70030.5 | 29 (6 / 23 / 0) | 1.500 | 20 |
| heat-module-tray | 1 | -170.00..170.00 | 420.00..700.00 | 60.00..61.50 | 340.00 x 280.00 x 1.50 | 142392.2 | 24 (6 / 18 / 0) | 1.500 | 15 |
| heat-module-wall-front | 1 | -143.50..143.50 | 422.00..423.50 | 61.50..170.00 | 287.00 x 1.50 x 108.50 | 46506.8 | 18 (6 / 12 / 0) | 1.500 | 9 |
| heat-module-wall-left | 1 | -145.00..-143.50 | 422.00..627.00 | 61.50..170.00 | 1.50 x 205.00 x 108.50 | 19709.0 | 20 (10 / 10 / 0) | 1.500 | 8 |
| heat-module-wall-rear | 1 | -143.50..143.50 | 625.50..627.00 | 61.50..170.00 | 287.00 x 1.50 x 108.50 | 46506.8 | 18 (6 / 12 / 0) | 1.500 | 9 |
| heat-module-wall-right | 1 | 143.50..145.00 | 422.00..627.00 | 61.50..170.00 | 1.50 x 205.00 x 108.50 | 31709.0 | 20 (10 / 10 / 0) | 1.500 | 8 |
| hood-bottom | 1 | -175.00..175.00 | 448.00..705.50 | 230.00..231.50 | 350.00 x 257.50 x 1.50 | 115600.6 | 21 (6 / 15 / 0) | 1.500 | 12 |
| hood-top | 1 | -175.00..175.00 | 448.00..705.50 | 256.50..258.00 | 350.00 x 257.50 x 1.50 | 116507.2 | 28 (10 / 18 / 0) | 1.500 | 16 |
| liner-splice | 1 | -20.04..20.04 | -0.00..38.30 | 864.65..867.00 | 40.08 x 38.30 x 2.35 | 2270.8 | 8 (4 / 4 / 0) | | |
| liner | 1 | -237.00..237.00 | -1.50..39.80 | 394.50..868.50 | 474.00 x 41.30 x 474.00 | 91807.6 | 10 (4 / 6 / 0) | | |
| lint-box-back | 1 | -166.00..166.00 | 38.50..40.00 | 62.00..275.00 | 332.00 x 1.50 x 213.00 | 80050.4 | 37 (14 / 23 / 0) | 1.500 | 22 |
| lint-box-front | 1 | -166.00..166.00 | 7.00..8.50 | 62.00..462.07 | 332.00 x 1.50 x 400.07 | 175620.6 | 23 (5 / 18 / 0) | 1.500 | 16 |
| post-1 | 1 | -345.00..-305.00 | 0.00..40.00 | 0.00..1000.00 | 40.00 x 40.00 x 1000.00 | 1088617.6 | 59 (54 / 5 / 0) | | |
| post-2 | 1 | 305.00..345.00 | 0.00..40.00 | 0.00..1000.00 | 40.00 x 40.00 x 1000.00 | 1088617.6 | 59 (54 / 5 / 0) | | |
| post-3 | 1 | -345.00..-305.00 | 710.00..750.00 | 0.00..1000.00 | 40.00 x 40.00 x 1000.00 | 1088617.6 | 59 (54 / 5 / 0) | | |
| post-4 | 1 | 305.00..345.00 | 710.00..750.00 | 0.00..1000.00 | 40.00 x 40.00 x 1000.00 | 1088617.6 | 59 (54 / 5 / 0) | | |
| power-module-barrier | 1 | -300.00..-150.00 | 655.00..730.50 | 642.00..643.50 | 150.00 x 75.50 x 1.50 | 16928.2 | 12 (6 / 6 / 0) | 1.500 | 3 |
| power-module-cover | 1 | -300.00..-150.00 | 728.00..729.50 | 310.00..640.00 | 150.00 x 1.50 x 330.00 | 74108.2 | 14 (6 / 8 / 0) | 1.500 | 5 |
| power-module-plate | 1 | -300.00..-150.00 | 651.50..653.00 | 270.00..990.00 | 150.00 x 1.50 x 720.00 | 161321.5 | 31 (6 / 25 / 0) | 1.500 | 22 |
| rail-bottom-front | 1 | -305.00..305.00 | 0.00..40.00 | 0.00..40.00 | 610.00 x 40.00 x 40.00 | 664056.7 | 59 (54 / 5 / 0) | | |
| rail-bottom-left | 1 | -345.00..-305.00 | 40.00..710.00 | 0.00..40.00 | 40.00 x 670.00 x 40.00 | 729373.8 | 59 (54 / 5 / 0) | | |
| rail-bottom-rear | 1 | -305.00..305.00 | 710.00..750.00 | 0.00..40.00 | 610.00 x 40.00 x 40.00 | 664056.7 | 59 (54 / 5 / 0) | | |
| rail-bottom-right | 1 | 305.00..345.00 | 40.00..710.00 | 0.00..40.00 | 40.00 x 670.00 x 40.00 | 729373.8 | 59 (54 / 5 / 0) | | |
| rail-mid-front-left | 1 | -305.00..-170.00 | 0.00..40.00 | 260.00..300.00 | 135.00 x 40.00 x 40.00 | 146963.4 | 59 (54 / 5 / 0) | | |
| rail-mid-front-right | 1 | 170.00..305.00 | 0.00..40.00 | 260.00..300.00 | 135.00 x 40.00 x 40.00 | 146963.4 | 59 (54 / 5 / 0) | | |
| rail-mid-left | 1 | -345.00..-305.00 | 40.00..710.00 | 260.00..300.00 | 40.00 x 670.00 x 40.00 | 729373.8 | 59 (54 / 5 / 0) | | |
| rail-mid-rear | 1 | -305.00..305.00 | 710.00..750.00 | 260.00..300.00 | 610.00 x 40.00 x 40.00 | 664056.7 | 59 (54 / 5 / 0) | | |
| rail-mid-rearcross | 1 | -305.00..305.00 | 611.50..651.50 | 260.00..300.00 | 610.00 x 40.00 x 40.00 | 664056.7 | 59 (54 / 5 / 0) | | |
| rail-mid-right | 1 | 305.00..345.00 | 40.00..710.00 | 260.00..300.00 | 40.00 x 670.00 x 40.00 | 729373.8 | 59 (54 / 5 / 0) | | |
| rail-top-front | 1 | -305.00..305.00 | 0.00..40.00 | 960.00..1000.00 | 610.00 x 40.00 x 40.00 | 664056.7 | 59 (54 / 5 / 0) | | |
| rail-top-left | 1 | -345.00..-305.00 | 40.00..710.00 | 960.00..1000.00 | 40.00 x 670.00 x 40.00 | 729373.8 | 59 (54 / 5 / 0) | | |
| rail-top-rear | 1 | -305.00..305.00 | 710.00..750.00 | 960.00..1000.00 | 610.00 x 40.00 x 40.00 | 664056.7 | 59 (54 / 5 / 0) | | |
| rail-top-rearcross | 1 | -305.00..305.00 | 611.50..651.50 | 960.00..1000.00 | 610.00 x 40.00 x 40.00 | 664056.7 | 59 (54 / 5 / 0) | | |
| rail-top-right | 1 | 305.00..345.00 | 40.00..710.00 | 960.00..1000.00 | 40.00 x 670.00 x 40.00 | 729373.8 | 59 (54 / 5 / 0) | | |
| rear-bulkhead | 1 | -305.00..305.00 | 610.00..611.50 | 265.00..995.00 | 610.00 x 1.50 x 730.00 | 652057.6 | 162 (6 / 156 / 0) | 1.500 | 153 |
| rear-lower-panel | 1 | -345.00..345.00 | 750.00..751.50 | -0.00..259.00 | 690.00 x 1.50 x 259.00 | 238937.9 | 153 (70 / 83 / 0) | 1.500 | 48 |
| rear-upper-panel | 1 | -345.00..345.00 | 750.00..751.50 | 260.00..1000.00 | 690.00 x 1.50 x 740.00 | 764957.7 | 28 (6 / 22 / 0) | 1.500 | 19 |
| side-panel-left | 1 | -346.50..-345.00 | -0.00..750.00 | -0.00..1000.00 | 1.50 x 750.00 x 1000.00 | 1123510.2 | 39 (6 / 33 / 0) | 1.500 | 30 |
| side-panel-right | 1 | 345.00..346.50 | -0.00..750.00 | -0.00..1000.00 | 1.50 x 750.00 x 1000.00 | 1123510.2 | 39 (6 / 33 / 0) | 1.500 | 30 |
| tier0-faceplate | 1 | -310.00..310.00 | 608.00..610.00 | 1004.50..1164.50 | 620.00 x 2.00 x 160.00 | 195756.6 | 515 (359 / 22 / 134) | 2.000 | 19 |
| top-panel | 1 | -345.00..345.00 | -0.00..750.00 | 1000.00..1001.50 | 690.00 x 750.00 x 1.50 | 774638.0 | 31 (6 / 25 / 0) | 1.500 | 22 |
| tray-rail-1 | 1 | -170.00..-150.00 | -0.00..750.00 | 40.00..60.00 | 20.00 x 750.00 x 20.00 | 151936.6 | 59 (54 / 5 / 0) | | |
| tray-rail-2 | 1 | 150.00..170.00 | -0.00..750.00 | 40.00..60.00 | 20.00 x 750.00 x 20.00 | 151936.6 | 59 (54 / 5 / 0) | | |
| trunk-front | 1 | -130.00..130.00 | 652.50..654.00 | 258.00..831.50 | 260.00 x 1.50 x 573.50 | 177913.9 | 37 (10 / 27 / 0) | 1.500 | 25 |
| trunk-rear | 1 | -130.00..130.00 | 704.00..705.50 | 258.00..831.50 | 260.00 x 1.50 x 573.50 | 223308.5 | 23 (6 / 17 / 0) | 1.500 | 14 |

Bought parts and envelopes in the assembly (no part file):

| solid | X min..max | Y min..max | Z min..max | volume mm3 |
|---|---|---|---|---|
| tray-rail-brackets (bought, 4 x 2020 inside corner brackets) | -190.00..190.00 | 11.50..738.50 | 40.00..60.00 | 6056.9 |
| hardware-tray-rails (bought, 8 x M4 x 8 button head, T-nuts for the 6 and 8 mm slots) | -185.80..185.80 | 16.20..733.80 | 34.50..53.80 | 1429.4 |
| feet (bought, 4 x M8 leveling feet, 50 pad) | -350.00..350.00 | -5.00..755.00 | -19.50..35.00 | 93105.7 |
| hardware-front-bulkhead (bought, 7 x M6 x 12 hex, washers, T-nuts) | -281.00..281.00 | 29.50..47.10 | 274.00..986.00 | 6009.1 |
| hardware-rear-bulkhead (bought, 10 x M6 x 12 hex, washers, T-nuts) | -281.00..281.00 | 604.40..622.00 | 274.00..986.00 | 8584.5 |
| drum-glides-front (bought, 2 x nylon drum glide pads, 45 x 20 x 8) | -221.14..221.14 | 41.50..49.50 | 809.17..852.64 | 13153.3 |
| drum-glides-rear (bought, 2 x nylon drum glide pads, 45 x 20 x 9.5) | -221.14..221.14 | 600.50..610.00 | 809.17..852.64 | 15734.7 |
| hardware-drum-glides (bought, 4 x M4 x 8 and 4 x M4 x 10 button head, nuts) | -211.93..211.93 | 37.80..613.70 | 818.62..843.19 | 2261.6 |
| hardware-bay-ceiling (bought, 20 x M6 x 12 hex, washers, T-nuts) | -331.00..331.00 | 74.00..736.00 | 289.50..307.10 | 17168.9 |
| hardware-base-pan (bought, 20 x M6 x 12 hex, washers, T-nuts) | -331.00..331.00 | 14.00..736.00 | -7.10..10.50 | 17168.9 |
| hardware-side-panel-left (bought, 29 x M6 x 12 hex, washers, T-nuts) | -352.10..-334.50 | 14.00..736.00 | 14.00..986.00 | 24895.0 |
| hardware-side-panel-right (bought, 29 x M6 x 12 hex, washers, T-nuts) | 334.50..352.10 | 14.00..736.00 | 14.00..986.00 | 24895.0 |
| hardware-front-upper-panel (bought, 16 x M6 x 12 hex, washers, T-nuts) | -331.00..331.00 | -7.10..10.50 | 274.00..986.00 | 13735.1 |
| hardware-front-lower-panel (bought, 8 x M6 x 12 hex, washers, T-nuts) | -331.00..331.00 | -7.10..10.50 | 14.00..205.00 | 6867.6 |
| hardware-rear-upper-panel (bought, 18 x M6 x 12 hex, washers, T-nuts) | -331.00..331.00 | 739.50..757.10 | 274.00..986.00 | 15452.0 |
| hardware-rear-lower-panel (bought, 8 x M6 x 12 hex, washers, T-nuts) | -331.00..331.00 | 739.50..757.10 | 14.00..205.00 | 6867.6 |
| hardware-top-panel (bought, 16 x M6 x 12 hex, washers, T-nuts) | -331.00..331.00 | 14.00..736.00 | 989.50..1007.10 | 13735.1 |
| console-brackets (bought, 12 x 4040 inside corner brackets) | -342.00..342.00 | 614.50..747.00 | 1001.50..1198.50 | 104526.4 |
| hardware-console-brackets (bought, 24 x M6 x 12 hex, washers, T-nuts) | -331.00..331.00 | 625.50..736.00 | 993.50..1187.50 | 20602.7 |
| hardware-console-face (bought, 8 x M6 x 12 hex, washers, T-nuts) | -331.00..331.00 | 604.40..622.00 | 1024.00..1187.50 | 6867.6 |
| hardware-console-rear (bought, 8 x M6 x 12 hex, washers, T-nuts) | -331.00..331.00 | 739.50..757.10 | 1024.00..1187.50 | 6867.6 |
| hardware-console-cap (bought, 10 x M6 x 12 hex, washers, T-nuts) | -331.00..331.00 | 625.50..736.00 | 1191.00..1208.60 | 8584.5 |
| hardware-console-cheek-left (bought, 5 x M6 x 12 hex, washers, T-nuts) | -352.10..-334.50 | 625.50..736.00 | 1024.00..1187.50 | 4292.2 |
| hardware-console-cheek-right (bought, 5 x M6 x 12 hex, washers, T-nuts) | 334.50..352.10 | 625.50..736.00 | 1024.00..1187.50 | 4292.2 |
| hardware-tier0-faceplate (bought, 6 x M4 x 10 button head, nuts) | -299.04..299.04 | 605.80..618.00 | 1010.70..1158.30 | 1771.6 |
| tier0-knob-dry-time (bought) | -170.00..-130.00 | 586.80..611.50 | 1064.50..1104.50 | 15189.3 |
| tier0-timer-dry-time (bought) | -170.30..-129.70 | 610.00..641.70 | 1031.30..1137.70 | 90563.2 |
| tier0-knob-heat-time (bought) | -80.00..-40.00 | 586.80..611.50 | 1064.50..1104.50 | 15189.3 |
| tier0-timer-heat-time (bought) | -80.30..-39.70 | 610.00..641.70 | 1031.30..1137.70 | 90563.2 |
| tier0-selector-body (bought) | 45.00..75.00 | 605.50..656.50 | 1087.00..1122.00 | 34073.2 |
| tier0-selector (bought) | 49.00..71.00 | 595.50..605.50 | 1089.50..1119.50 | 2878.1 |
| tier0-start-body (bought) | 115.00..145.00 | 605.50..656.50 | 1087.00..1122.00 | 34073.2 |
| tier0-start-button (bought) | 119.00..141.00 | 597.50..605.50 | 1093.50..1115.50 | 2984.1 |
| tier0-k1-relay-on-din-rail (bought) | 40.00..140.00 | 610.00..694.50 | 1024.50..1079.50 | 127556.4 |
| hardware-door-ring (bought, 8 x M4 x 8 button head, nuts) | -241.94..241.94 | -5.70..4.50 | 389.80..873.20 | 2161.0 |
| door-hinge-1-fixed (bought, flag hinge, pinned half) | -287.50..-245.00 | -23.00..-3.50 | 561.50..701.50 | 17840.6 |
| hardware-door-hinge-1 (bought, 2 x M6 x 16 countersunk, nuts) | -272.00..-246.00 | -9.50..6.50 | 575.50..587.50 | 1692.2 |
| door-hinge-2-swing (bought, flag hinge, lift-off half) | -287.50..-245.00 | -23.00..-5.00 | 666.50..696.50 | 10701.0 |
| hardware-door-hinge-2 (bought, 2 x M4 x 8 button head into the tapped leaf) | -262.80..-246.20 | -15.70..-5.50 | 677.70..685.30 | 357.3 |
| door-handle (bought, D handle 128 centres) | 213.00..227.00 | -57.00..-13.50 | 560.50..702.50 | 30386.5 |
| hardware-door-handle (bought, 2 x M4 x 10 button head into the handle) | 216.20..223.80 | -21.50..-9.30 | 563.70..699.30 | 407.6 |
| door-seal (bought, OEM door seal) | -246.00..246.00 | -11.50..-5.50 | 385.50..877.50 | 81939.0 |
| door-catch (bought, magnetic catch) | 256.00..268.00 | -10.00..-3.50 | 625.50..637.50 | 936.0 |
| door-catch-strike (bought) | 256.00..268.00 | -11.50..-10.50 | 625.50..637.50 | 144.0 |
| hardware-drum-tabs (bought, 60 x M4 x 8 button head, nuts) | -305.24..305.24 | 44.00..606.00 | 328.15..934.85 | 16207.7 |
| hardware-drum-seam (bought, 16 x M4 x 8 button head, nuts) | -19.21..19.21 | 101.20..508.80 | 936.99..947.36 | 4322.1 |
| baffle-1 (angle, cut to length) | -277.17..-241.03 | 85.00..565.00 | 748.43..803.07 | 110481.8 |
| baffle-2 (angle, cut to length) | -20.00..20.00 | 85.00..565.00 | 323.00..363.00 | 110481.8 |
| baffle-3 (angle, cut to length) | 222.53..277.17 | 85.00..565.00 | 766.93..803.07 | 110481.8 |
| hardware-drum-baffles (bought, 12 x M6 x 12 button head, nuts) | -272.98..272.98 | 149.75..500.25 | 318.20..791.73 | 10142.8 |
| motor (bought) | -70.00..70.00 | 185.50..394.00 | 50.00..210.00 | 3046373.7 |
| motor-mount-1 (bought, cradle bracket) | -35.00..35.00 | 215.00..245.00 | 0.00..58.80 | 39966.9 |
| motor-mount-2 (bought, cradle bracket) | -35.00..35.00 | 335.00..365.00 | 0.00..58.80 | 39966.9 |
| hardware-motor-mounts (bought, 4 x M6 x 12 hex, washers, nuts, through the base pan) | -28.00..28.00 | 224.00..356.00 | -7.10..10.50 | 4562.0 |
| pulley (bought) | -11.00..11.00 | 394.00..416.00 | 109.00..131.00 | 6967.1 |
| blower (bought) | -110.00..291.00 | 85.50..215.00 | 10.00..230.00 | 5340928.1 |
| heat-module-angles-bottom (20x20x2 aluminium angle, 2 x 205 outside, 2 x 283 inside) | -165.00..165.00 | 422.00..627.00 | 61.50..81.50 | 73539.8 |
| heat-module-angles-top (20x20x2 aluminium angle, 2 x 165, 2 x 290) | -147.00..147.00 | 420.00..629.00 | 153.50..173.50 | 68523.8 |
| heat-module-angles-corner (20x20x2 aluminium angle, 4 x 72) | -147.00..147.00 | 420.00..629.00 | 81.50..153.50 | 21633.5 |
| heat-module-element-rails (20x20x2 aluminium angle, 2 x 198) | -143.50..143.50 | 425.50..623.50 | 61.50..81.50 | 29968.8 |
| heat-module-element (bought, 279838 class open-coil element on its frame, envelope) | -133.50..157.00 | 429.50..619.50 | 81.50..132.50 | 2592870.0 |
| heat-module-collar (bought, 125 flanged starting collar, cut to 55.5) | -77.50..77.50 | 447.50..602.50 | 171.50..227.00 | 19547.8 |
| heat-module-thermostats (bought, 279816 class high-limit and thermal cut-off, envelopes) | -121.00..121.00 | 473.00..527.00 | 171.50..186.50 | 15480.8 |
| heat-module-terminal-angle (20x20x2 aluminium angle, 290) | -145.00..145.00 | 635.50..655.50 | 61.50..81.50 | 21849.1 |
| heat-module-din-rail (bought, 35 x 7.5 top hat, 280) | -140.00..140.00 | 635.50..643.00 | 94.00..129.00 | 13377.7 |
| heat-module-devices (bought, envelopes: 2 end clamps, X_HM mains and SELV strips, partition, K_HEAT, CS1) | -140.00..43.60 | 643.00..729.00 | 73.00..150.00 | 502878.0 |
| heat-module-bonding-stud (bought, M6 x 16 hex bolt, 2 nuts, star washers; the PE ring terminal goes between the nuts) | 134.00..146.00 | 674.00..686.00 | 54.40..76.00 | 1535.7 |
| heat-module-hardware (bought, 64 x M4 x 8 button head, 60 nuts, 4 T-nuts for the 6 mm slot) | -163.80..163.80 | 417.80..649.30 | 55.50..175.70 | 16922.4 |
| hardware-power-module-plate (bought, 4 x M6 x 12 hex, washers, T-nuts) | -291.00..-159.00 | 641.00..658.60 | 274.00..986.00 | 3433.8 |
| power-module-rail-A1-devices (bought, envelopes: X1 cord: 4 x UK 6 N (L1, L2, N, PE), CB1: 1P MCB, F1: UK 5-HESI fuse terminal, 2 end clamps) | -295.00..-217.50 | 660.50..720.50 | 315.00..405.00 | 213485.2 |
| power-module-rail-A2-devices (bought, envelopes: PSU: HDR-60-24, K_MOTOR: LC1K0910BD class mini contactor, 2 end clamps) | -295.00..-178.50 | 660.50..717.50 | 425.00..515.00 | 433870.5 |
| power-module-rail-A3-devices (bought, envelopes: X2 heat module mains: 4 x UK 6 N, X3 motor and S1: 5 x UK 2.5 N, 2 end clamps) | -295.00..-212.20 | 660.50..702.50 | 556.50..603.50 | 138091.2 |
| power-module-rail-B1-devices (bought, envelopes: RLY_MOTOR, RLY_HEAT, RLY_HEAT_LO: 3 x 38.51 class, PTC1 to PTC3 in fuse terminals, F2: UK 5-HESI, X4 heat module SELV: 4 x UK 2.5 N, 2 end clamps) | -295.00..-199.80 | 660.50..730.50 | 653.50..746.50 | 291878.8 |
| power-module-rail-B2-devices (bought, envelopes: X5 chassis switches: 10 x UK 2.5 N, X6 sensors: 6 x UK 2.5 N, 2 end clamps) | -295.00..-176.80 | 660.50..696.50 | 798.00..842.00 | 174007.2 |
| power-module-din-rails (bought, 5 x 35 x 7.5 top hat, 140) | -295.00..-155.00 | 653.00..660.50 | 342.50..837.50 | 33288.3 |
| power-module-barrier-angle (20x20x2 aluminium angle, 150) | -300.00..-150.00 | 653.00..673.00 | 640.00..660.00 | 11272.8 |
| power-module-standoffs (bought, 4 x M4 x 75 hex standoffs, female both ends) | -294.04..-155.96 | 653.00..728.00 | 316.50..633.50 | 11733.1 |
| power-module-ground-stud (bought, M6 x 16 hex bolt, 2 nuts, star washers; the cord's PE ring terminal goes between the nuts) | -171.00..-159.00 | 645.90..667.50 | 944.00..956.00 | 1535.7 |
| power-module-hardware (bought, 22 x M4 x 8 button head, 14 nuts) | -293.80..-156.20 | 649.30..731.70 | 316.20..823.80 | 5211.2 |
| grommets (bought, 5 x rubber grommets for 1.5 panels: 22 mm hole x 2, 30 mm hole x 1, 16 mm hole x 2) | -289.00..301.00 | 38.75..708.00 | 298.75..1002.75 | 6693.7 |
| cord-bushing (bought, PG16 strain relief) | -290.01..-259.99 | 677.00..703.00 | -6.50..18.00 | 8877.4 |
| power-cord (bought) | -279.50..-270.50 | 685.50..820.00 | -16.50..320.00 | 29269.7 |
| hardware-liner (bought, 2 x M3 x 6 button head, nuts) | -15.70..15.70 | 16.30..22.00 | 863.45..871.23 | 234.8 |
| lint-box-bars (30 x 8 aluminium flat bar: 2 sides mitred at the top, 1 bottom) | -166.00..166.00 | 8.50..38.50 | 62.00..462.07 | 261325.7 |
| lint-box-foam (bought, 3 mm closed-cell foam tape 8 wide, 2 x 190, compressed to 1.5) | -166.00..166.00 | 38.50..40.00 | 275.00..462.07 | 4255.3 |
| spool-bars (40 x 8 aluminium flat bar: 2 x 136, 2 x 140) | -78.00..78.00 | 40.00..80.00 | 62.00..198.00 | 175718.7 |
| spool-foam (bought, 6 mm closed-cell foam tape 8 wide, 600, compressed to 4 on the blower plate) | -78.00..78.00 | 80.00..84.00 | 62.00..198.00 | 17664.0 |
| lint-box-hardware (bought, 40 pieces: M4 x 8, M4 x 10 and M4 x 40 button heads, 2 x M6 x 20 button heads with 4 mm spacers and T-nuts) | -178.00..178.00 | 4.80..47.00 | 62.20..423.80 | 11201.0 |
| basket-mesh (bought, stainless 18 x 16 mesh strip, 42 wide, 350 long, wrapped and folded 5 at each edge) | -163.45..163.45 | 12.00..45.10 | 363.00..445.93 | 16043.2 |
| basket-pull (bought, D-pull, 64 mm centres, 25 projection) | -37.00..37.00 | 16.50..41.50 | 409.00..419.00 | 8057.3 |
| hardware-basket (bought, 12 x M3 x 5 button head into the tapped plates, 2 x M4 x 10 button head into the pull) | -153.75..153.75 | 9.10..48.25 | 370.33..431.90 | 1208.9 |
| hood-bars (25 x 8 aluminium flat bar: 2 sides, front, rear) | -175.00..175.00 | 448.00..705.50 | 231.50..256.50 | 234798.9 |
| hood-gasket (bought, 3 mm foam ring 150 x 125, glued under the hood's bottom plate) | -75.00..75.00 | 450.00..600.00 | 227.00..230.00 | 16198.8 |
| trunk-bars (50 x 8 aluminium flat bar: 2 sides, 1 top) | -130.00..130.00 | 654.00..704.00 | 258.00..831.50 | 553698.4 |
| nozzle-bars (40 x 8 aluminium flat bar: 2 sides, top, bottom) | -114.00..114.00 | 612.50..652.50 | 658.50..816.50 | 234860.4 |
| nozzle-foam (bought, 2 mm closed-cell foam tape 8 wide, 900, compressed to 1 on the bulkhead) | -114.00..114.00 | 611.50..612.50 | 658.50..816.50 | 5761.0 |
| riser-hardware (bought, 70 x M4 x 8 and M4 x 10 button heads) | -174.80..174.80 | 448.20..707.70 | 227.80..831.30 | 12758.2 |
| door-switch (bought, two-contact plunger switch, envelope) | 166.17..219.20 | -11.00..25.00 | 412.30..465.33 | 34081.2 |
| hardware-door-switch (bought, 2 x M4 x 8 button head into the switch's tapped ears) | 192.78..214.52 | -3.70..6.50 | 416.98..438.72 | 357.3 |
| ps1-bracket (angle 20x20x2, 60) | 220.00..280.00 | 60.00..80.00 | 0.00..20.00 | 4363.7 |
| ps1-air-proving-switch (bought, envelope) | 220.00..280.00 | 80.00..108.00 | 0.00..60.00 | 100578.3 |
| hardware-ps1 (bought, 2 x M6 x 12 hex, nuts, through the base pan; 2 x M4 x 8 button head into the switch) | 229.00..271.00 | 64.00..86.00 | -10.00..15.80 | 2638.4 |
| exhaust-thermostats (bought, TF2 thermal fuse, T_HI and T_LO cycling thermostats, envelopes on the blower outlet) | 119.00..241.00 | 123.00..177.00 | 206.00..221.00 | 23221.1 |
| hardware-exhaust-thermostats (bought, 6 x M4 x 8 button head into the housing) | 126.20..233.80 | 126.20..173.80 | 200.00..210.20 | 1072.0 |
| blower-plate-feet (angle 20x20x2, 2 x 90) | -135.00..135.00 | 64.00..84.00 | 0.00..20.00 | 13287.3 |
| hardware-blower-plate (bought, 4 x M4 x 8 button head into the housing, 4 x M4 x 8 and nuts into the feet, 4 x M6 x 12 hex, washers, nuts through the base pan) | -116.00..116.00 | 68.00..92.00 | -7.10..183.80 | 6357.2 |
| exhaust-duct (bought, 4 in aluminium pipe, 102 x 1, cut to length, one 6.5 hole for the tap) | 179.00..281.00 | 192.00..801.50 | 99.00..201.00 | 193361.7 |
| exhaust-clamps (bought, 2 x worm-drive hose clamps for 102, envelopes) | 178.30..281.70 | 198.00..750.00 | 98.30..211.70 | 10700.4 |
| exhaust-tap-barb (bought, 1/8 NPT or M6 brass barb fitting with a locknut, 5 mm barb, envelope) | 224.23..235.77 | 295.00..305.00 | 192.00..221.00 | 1215.3 |
| ps1-tube (bought, 6 mm silicone tube from the tap to PS1, drawn on its route) | 227.00..253.00 | 91.00..303.00 | 60.00..243.00 | 11236.9 |
| th1-exhaust-thermistor (bought, 10 k NTC appliance thermistor, envelope) | 102.00..138.00 | 31.50..62.00 | 145.00..175.00 | 17281.3 |
| hardware-th1 (bought, 1 x M4 x 20 button head from inside the lint box, nut on the body) | 115.96..124.04 | 36.30..58.50 | 166.20..173.80 | 420.9 |
| moisture-bars (bought, dryer moisture sensor bar set, two stainless strips on an insulating base, envelope) | 175.44..248.58 | 41.50..49.50 | 452.91..545.13 | 20769.5 |
| hardware-moisture-bars (bought, 2 x M4 x 16 button head from the drum side, nuts in the front gap) | 189.42..234.60 | 33.50..51.70 | 465.54..532.50 | 741.3 |
| entry-blank-2 (the second entry-blank, cut two to drawings/entry-blank.dxf; on the condensate drain) | -260.00..-200.00 | 748.50..750.00 | 44.00..88.00 | 3865.9 |
| hardware-entry-blanks (bought, 4 x M4 x 8 button head, nuts) | -255.04..-204.96 | 743.50..753.70 | 62.20..153.80 | 1080.5 |
| cable-clamps (bought, 4 x nylon P-clip for a 12 mm bundle, envelopes) | -258.00..-227.50 | 115.00..605.00 | 0.00..15.00 | 3409.3 |
| hardware-cable-clamps (bought, 4 x M4 x 8 button head, nuts under the pan) | -254.04..-245.96 | 116.20..603.80 | -6.50..3.70 | 1080.5 |
| roller-front-1 (bought) | -210.17..-150.17 | 50.00..75.00 | 313.16..373.16 | 68521.1 |
| roller-rear-1 (bought) | -210.17..-150.17 | 576.50..601.50 | 313.16..373.16 | 68521.1 |
| roller-front-2 (bought) | 150.17..210.17 | 50.00..75.00 | 313.16..373.16 | 68521.1 |
| roller-rear-2 (bought) | 150.17..210.17 | 576.50..601.50 | 313.16..373.16 | 68521.1 |
| hardware-roller-studs (bought, 4 x ISO 7379 shoulder screws 10 x 35 M8, 1.0 shims, spacers 16 x 10.5 x 8.5, M8 washers and nuts) | -188.17..188.17 | 28.50..623.00 | 335.16..351.16 | 26570.9 |
| belt (bought, PJ 5 rib) | -313.50..313.50 | 396.00..408.00 | 106.50..945.00 | 93324.7 |
| idler-pulley (bought, flat idler 40 with bearing) | -82.00..-38.00 | 394.50..409.50 | 143.00..187.00 | 18849.1 |
| idler-arm (flat bar 25x4, cut to length) | -129.43..-45.57 | 390.00..394.00 | 10.57..179.43 | 16879.1 |
| hardware-idler-axle (bought, M8 x 30 bolt, nut) | -67.51..-52.49 | 385.00..414.50 | 158.50..171.50 | 2443.8 |
| idler-bracket (angle 40x40x3, cut to length) | -140.00..-90.00 | 350.00..390.00 | 0.00..40.00 | 11180.7 |
| hardware-idler-pivot (bought, M8 x 25 bolt, nut) | -122.51..-107.49 | 382.00..400.00 | 18.50..31.50 | 1865.7 |
| spring-bracket (angle 40x40x3, cut to length) | 45.00..85.00 | 350.00..390.00 | 0.00..40.00 | 8977.2 |
| hardware-idler-spring-posts (bought, 2 x M5 shoulder posts) | -84.50..67.50 | 384.00..417.50 | 22.50..111.50 | 1256.6 |
| idler-spring (bought, extension spring) | -80.19..63.19 | 409.00..417.00 | 25.51..108.49 | 7580.8 |
| hardware-idler-brackets (bought, 4 x M6 x 12 hex, nuts, through the base pan) | -134.00..81.00 | 364.00..376.00 | -9.00..8.60 | 4562.0 |

DXF drawings:

| drawing | entities | closed loops | open chains | loops by type |
|---|---|---|---|---|
| base-pan | ARC 4, CIRCLE 43, LINE 4 | 44 | 0 | circle 43, rrect 1 |
| basket-far-clamp | ARC 2, CIRCLE 6, LINE 2 | 7 | 0 | circle 6, sector 1 |
| basket-far-plate | ARC 2, CIRCLE 6, LINE 2 | 7 | 0 | circle 6, sector 1 |
| basket-lip-clamp | ARC 4, CIRCLE 6, LINE 4 | 8 | 0 | circle 6, sector 2 |
| basket-lip-plate | ARC 7, CIRCLE 6, LINE 9 | 8 | 0 | circle 6, other 1, sector 1 |
| bay-ceiling | ARC 2, CIRCLE 23, LINE 28 | 29 | 0 | circle 23, rect 5, rpoly 1 |
| blower-plate | ARC 4, CIRCLE 8, LINE 8 | 10 | 0 | circle 8, rect 1, rrect 1 |
| console-cap | ARC 4, CIRCLE 10, LINE 4 | 11 | 0 | circle 10, rrect 1 |
| console-cheek-left | ARC 4, CIRCLE 5, LINE 4 | 6 | 0 | circle 5, rrect 1 |
| console-cheek-right | ARC 4, CIRCLE 5, LINE 4 | 6 | 0 | circle 5, rrect 1 |
| console-face | ARC 4, CIRCLE 14, LINE 8 | 16 | 0 | circle 14, rect 1, rrect 1 |
| console-rear | ARC 4, CIRCLE 8, LINE 4 | 9 | 0 | circle 8, rrect 1 |
| door-disc | CIRCLE 5 | 5 | 0 | circle 5 |
| door-ring | CIRCLE 13 | 13 | 0 | circle 13 |
| drum-ring | CIRCLE 32 | 32 | 0 | circle 32 |
| drum-sheet | ARC 120, CIRCLE 88, LINE 244 | 89 | 0 | circle 88, rpoly 1 |
| drum-splice | ARC 4, CIRCLE 16, LINE 4 | 17 | 0 | circle 16, rrect 1 |
| entry-blank | ARC 4, CIRCLE 2, LINE 4 | 3 | 0 | circle 2, rrect 1 |
| felt-seal-long | ARC 2, LINE 2 | 1 | 0 | sector 1 |
| felt-seal-short | ARC 2, LINE 2 | 1 | 0 | sector 1 |
| front-bulkhead | ARC 6, CIRCLE 24, LINE 6 | 26 | 0 | circle 24, rrect 1, sector 1 |
| front-lower-panel | ARC 116, CIRCLE 8, LINE 116 | 65 | 0 | circle 8, rrect 1, slot 56 |
| front-upper-panel | ARC 4, CIRCLE 30, LINE 4 | 31 | 0 | circle 30, rrect 1 |
| heat-module-terminal-plate | ARC 4, CIRCLE 5, LINE 4 | 6 | 0 | circle 5, rrect 1 |
| heat-module-top | ARC 4, CIRCLE 19, LINE 4 | 20 | 0 | circle 19, rrect 1 |
| heat-module-tray | ARC 4, CIRCLE 14, LINE 4 | 15 | 0 | circle 14, rrect 1 |
| heat-module-wall-front | ARC 4, CIRCLE 8, LINE 4 | 9 | 0 | circle 8, rrect 1 |
| heat-module-wall-left | ARC 4, CIRCLE 6, LINE 8 | 8 | 0 | circle 6, rect 1, rrect 1 |
| heat-module-wall-rear | ARC 4, CIRCLE 8, LINE 4 | 9 | 0 | circle 8, rrect 1 |
| heat-module-wall-right | ARC 4, CIRCLE 6, LINE 8 | 8 | 0 | circle 6, rect 1, rrect 1 |
| hood-bottom | ARC 4, CIRCLE 11, LINE 4 | 12 | 0 | circle 11, rrect 1 |
| hood-top | ARC 4, CIRCLE 14, LINE 8 | 16 | 0 | circle 14, rect 1, rrect 1 |
| liner-splice | ARC 4, CIRCLE 2, LINE 4 | 3 | 0 | circle 2, rrect 1 |
| liner | CIRCLE 2, LINE 4 | 3 | 0 | circle 2, rect 1 |
| lint-box-back | ARC 4, CIRCLE 19, LINE 12 | 22 | 0 | circle 19, rect 2, rrect 1 |
| lint-box-front | ARC 3, CIRCLE 15, LINE 3 | 16 | 0 | circle 15, other 1 |
| power-module-barrier | ARC 4, CIRCLE 2, LINE 4 | 3 | 0 | circle 2, rrect 1 |
| power-module-cover | ARC 4, CIRCLE 4, LINE 4 | 5 | 0 | circle 4, rrect 1 |
| power-module-plate | ARC 4, CIRCLE 21, LINE 4 | 22 | 0 | circle 21, rrect 1 |
| rear-bulkhead | ARC 4, CIRCLE 152, LINE 4 | 153 | 0 | circle 152, rrect 1 |
| rear-lower-panel | ARC 68, CIRCLE 15, LINE 68 | 48 | 0 | circle 15, rrect 1, slot 32 |
| rear-upper-panel | ARC 4, CIRCLE 18, LINE 4 | 19 | 0 | circle 18, rrect 1 |
| side-panel-left | ARC 4, CIRCLE 29, LINE 4 | 30 | 0 | circle 29, rrect 1 |
| side-panel-right | ARC 4, CIRCLE 29, LINE 4 | 30 | 0 | circle 29, rrect 1 |
| tier0-faceplate | CIRCLE 18, LWPOLYLINE 1, LWPOLYLINE (not CUT) 1, TEXT (not CUT) 6 | 19 | 0 | circle 18, rrect 1 |
| top-panel | ARC 4, CIRCLE 21, LINE 4 | 22 | 0 | circle 21, rrect 1 |
| trunk-front | ARC 4, CIRCLE 23, LINE 8 | 25 | 0 | circle 23, rect 1, rrect 1 |
| trunk-rear | ARC 4, CIRCLE 13, LINE 4 | 14 | 0 | circle 13, rrect 1 |

## Notes

- clearance pair missing in the assembly: heat-module-collar (bought, 125 flanged starting collar, cut to 55.5) / hood-gasket (bought, 3 mm foam ring 150 x 125, glued under the hood)
- clearance pair missing in the assembly: blower (bought) / spool-bars (40 x 8 aluminium flat bar: 2 x 156, 2 x 140)
- drum-sheet.dxf offset from the unwrapped solid: (0.000, -0.000)
- drum-splice.dxf offset from the unwrapped solid: (-0.005, -0.000)
