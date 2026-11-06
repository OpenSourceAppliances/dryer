# CAD audit report

Produced by `mechanical/cad/cad_audit.py` from the STEP and DXF files on disk. Every number below was measured from the files, not read from the script.

Parts measured: 58 STEP files, 127 named solids in the assembly, 23 DXF drawings.
Document checks: 364, generic checks: 468, Fusion comparisons: 0. **Failures: 0.**

## 1. Values stated in the documents, against the files

| id | part | check | expected | measured | result | source |
|---|---|---|---|---|---|---|
| A-001 | assembly | assembly_solids | 127 | 127 | PASS | 7a: 54 made parts (draft 6 adds the console frame, its rear plate and the front felt), the bought parts and envelopes, and the hardware sets, each one named solid or compound |
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
| F-047 | tray-rail-1 | size y | 360 | 360.0 | PASS | 7a Frame 2020 tray rail 360 |
| F-048 | tray-rail-1 | size x | 20 | 20.0 | PASS | 7a Frame 2020 |
| F-049 | tray-rail-1 | size z | 20 | 20.000000000000043 | PASS | 7a Frame 2020 |
| F-050 | tray-rail-1 | min z | 40 | 40.0 | PASS | 7a Frame: on the bottom rails |
| F-051 | tray-rail-2 | size y | 360 | 360.0 | PASS | 7a Frame |
| F-052 | tray-rail-2 | min z | 40 | 40.0 | PASS | 7a Frame |
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
| F-058 | cut-list | cut tray-rail-1 | 360 | 360.0 | PASS | frame-cut-list.csv |
| F-058b | cut-list | cut console-post-1 | 200 | 200.0 | PASS | frame-cut-list.csv (7a Console) |
| F-058c | cut-list | cut console-rail-front | 610 | 610.0 | PASS | frame-cut-list.csv (7a Console) |
| F-058d | cut-list | cut console-rail-left | 58.5 | 58.5 | PASS | frame-cut-list.csv (7a Console) |
| F-059 | cut-list | cut baffle-1..3 | 480 | 480.0 | PASS | 7b Baffles 480 long |
| F-060 | cut-list | cut_qty baffle-1..3 | 3 | 3 | PASS | 7b three baffles |
| F-061 | cut-list | cut belt (bought) | 2232 | 2232.0 | PASS | 7a Drive: length of the drawn path round the drum (R 310 + half the 3.5 belt), the 30 pulley and the 40 idler at (-60, 165), replaces the 2214 two-pulley estimate (V-012) |
| B-001 | front-bulkhead | size x | 610 | 610.0 | PASS | 7a Bulkheads 610 wide |
| B-002 | front-bulkhead | thickness | 1.5 | 1.5 | PASS | 7a Bulkheads 1.5 steel |
| B-003 | front-bulkhead | normal | 0,1,0 | (-0.0, -1.0, -0.0) | PASS | 7a: front-facing plate |
| B-004 | front-bulkhead | min y | 40 | 40.0 | PASS | 7a: sits behind the front rails (0..40) |
| B-005 | front-bulkhead | min z | 265 | 265.0 | PASS | 7a: from the mid rails (260..300) to the top rails, 5 in from each rail edge |
| B-006 | front-bulkhead | max z | 995 | 995.0 | PASS | 7a: to the top rails (960..1000) |
| B-007 | front-bulkhead | loop circle;0;631.5;460;460 | 1 | 1 | PASS | 7a: door opening 460 on the drum axis; axis Z = 300 + 1.5 + 20 + 310 |
| B-008 | front-bulkhead | loop sector;0;402.227;312.702;73.454 | 1 | 1 | PASS | 7a Bulkheads (draft 6): curved lint slot between radii 238 and 266 about the drum axis (8 outside the 460 opening, 4 inside the 540 bore), 36 degrees each side of straight down: its box is 2 x 266 sin 36 wide, from 631.5 - 266 to 631.5 - 238 cos 36 high |
| B-009 | front-bulkhead | hole_at 10.5;-170;337.05 | 1 | (-170.000, 337.051) d 10.500 | PASS | 7a: roller shaft holes 30 degrees each side of bottom on radius 310 + 30 = 340 |
| B-010 | front-bulkhead | hole_at 10.5;170;337.05 | 1 | (170.000, 337.051) d 10.500 | PASS | 7a roller shaft holes |
| B-011 | front-bulkhead | holes 10.5;y | 2 | 2 | PASS | 7a two rollers per bulkhead |
| B-012 | front-bulkhead | outline 610;730 | 1 | rrect 610.000 x 730.000 | PASS | 7a Bulkheads |
| B-013 | rear-bulkhead | size x | 610 | 610.0 | PASS | 7a Bulkheads |
| B-014 | rear-bulkhead | thickness | 1.5 | 1.5 | PASS | 7a Bulkheads |
| B-015 | rear-bulkhead | min y | 610 | 610.0 | PASS | 7a: in front of the rear cross rails; drum front 50 + length 550 + 10 |
| B-016 | rear-bulkhead | hole_at 10.5;-170;337.05 | 1 | (-170.000, 337.051) d 10.500 | PASS | 7a roller shaft holes |
| B-017 | rear-bulkhead | hole_at 10.5;170;337.05 | 1 | (170.000, 337.051) d 10.500 | PASS | 7a roller shaft holes |
| B-018 | rear-bulkhead | holes 10;y | 126 | 126 | PASS | 7a: inlet field 200 x 130 above the axis, 10 mm holes on a 14 pitch: 14 x 9 |
| B-019 | rear-bulkhead | hole_at 10;-93;681.5 | 1 | (-93.000, 681.500) d 10.000 | PASS | 7a inlet field: first hole 7 in from the field edge, field starts 50 above the axis |
| B-020 | rear-bulkhead | hole_at 10;89;793.5 | 1 | (89.000, 793.500) d 10.000 | PASS | 7a inlet field: last hole |
| B-021 | rear-bulkhead | loops circle | 138 | 138 | PASS | 7a: 126 inlet + 2 roller + 10 M6 |
| B-022 | rear-bulkhead | outline 610;730 | 1 | rrect 610.000 x 730.000 | PASS | 7a Bulkheads |
| C-001 | bay-ceiling | thickness | 1.5 | 1.5 | PASS | 7a Bay ceiling 1.5 plate |
| C-002 | bay-ceiling | min z | 300 | 300.0 | PASS | 7a: on the mid rails (top at 300) |
| C-003 | bay-ceiling | min y | 42 | 42.0 | PASS | 7a: starts 0.5 behind the front bulkhead (40 + 1.5) |
| C-004 | bay-ceiling | max y | 750 | 750.0 | PASS | 7a |
| C-005 | bay-ceiling | size x | 687 | 687.0 | PASS | 7a: between the side panels, 690 - 2 x 1.5 |
| C-006 | bay-ceiling | loop rect;-137.9;402;40;90 | 1 | 1 | PASS | 7a: left belt slot where the run from the idler to the drum crosses the plate, Y 402 (draft 4: the belt could not pass a single slot on the centre line) |
| C-006b | bay-ceiling | loop rect;148.1;402;40;90 | 1 | 1 | PASS | 7a: right belt slot where the run from the drum to the pulley crosses the plate |
| C-007 | bay-ceiling | loop rect;0;610.75;612;2.5 | 1 | 1 | PASS | 7a: rear bulkhead passes through (610..611.5, 1 mm clearance) |
| C-008 | bay-ceiling | loop rect;0;678.5;264;54 | 1 | 1 | PASS | 7a: riser 260 x 50 behind the rear cross rail with 2 mm clearance |
| C-009 | bay-ceiling | holes 6.5;z | 20 | 20 | PASS | 7a Panels: M6 at 150 pitch; 5 on the rear cross rail, 5 on the rear rail, 5 on each side rail |
| C-010 | bay-ceiling | loops rpoly | 1 | 1 | PASS | 7a: outline notched at the two rear posts, 6 mm corner radii (draft 5) |
| C-011 | base-pan | thickness | 1.5 | 1.5 | PASS | 7a Panels 1.5 steel |
| C-012 | base-pan | max z | 0 | 0.0 | PASS | 7a: under the frame |
| C-013 | base-pan | size x | 687 | 687.0 | PASS | 7a between the side panels |
| C-014 | base-pan | size y | 750 | 750.0 | PASS | 7a |
| C-015 | base-pan | holes 6.5;z | 24 | 24 | PASS | 7a Panels M6 at 150 pitch: 20 to the rails plus 4 through-bolted for the idler and spring brackets |
| C-016 | base-pan | loops circle | 29 | 29 | PASS | 7a: 24 M6, 4 feet holes and the cord bushing hole (draft 6); no other cut-outs in the base pan |
| C-016b | base-pan | holes 8.5;z | 4 | 4 | PASS | 7c Feet: M8 studs through the pan into the posts' centre bores |
| C-016c | base-pan | hole_at 8.5;-325;20 | 1 | (-325.000, 20.000) d 8.500 | PASS | 7c Feet: on the post centres |
| C-016d | base-pan | hole_at 8.5;325;730 | 1 | (325.000, 730.000) d 8.500 | PASS | 7c Feet |
| C-016e | base-pan | hole_at 6.5;-128;370 | 1 | (-128.000, 370.000) d 6.500 | PASS | 7a Drive: idler bracket bolt, nut under the pan |
| C-016f | base-pan | hole_at 6.5;75;370 | 1 | (75.000, 370.000) d 6.500 | PASS | 7a Drive: spring bracket bolt |
| C-016g | base-pan | hole_at 22;-250;690 | 1 | (-250.000, 690.000) d 22.000 | PASS | 7a Panels (draft 6): cord strain relief bushing through the pan under the power module |
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
| P-016b | front-upper-panel | holes 4.5;y | 8 | 8 | PASS | 7a Door: the ring's 8 M4 bolts pass through the panel |
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
| P-027 | rear-lower-panel | loops circle | 9 | 9 | PASS | 7a: the exhaust port and 8 M6; the cord enters through the base pan (draft 6), not this panel |
| P-028 | rear-lower-panel | loops slot | 32 | 32 | PASS | 7a: louvers, 4 columns x 8 rows, clear of the exhaust port |
| P-029 | rear-lower-panel | holes 6.5;y | 8 | 8 | PASS | 7a: 2 per post x 2, 4 on the bottom rail |
| P-030 | top-panel | min z | 1000 | 1000.0 | PASS | 7a: on the top rails |
| P-031 | top-panel | thickness | 1.5 | 1.5 | PASS | 7a Panels |
| P-032 | top-panel | max y | 750 | 750.0 | PASS | 7a Console (draft 6): the top panel runs the full depth; the console stands on it |
| P-033 | top-panel | size x | 690 | 690.0 | PASS | 7 |
| P-034 | top-panel | holes 6.5;z | 20 | 20 | PASS | 7a: 4 on the front rail, 4 on the rear rail, 4 on each side rail (none under the console posts), 4 for the console's foot brackets |
| P-034b | top-panel | hole_at 6.5;282;631.5 | 1 | (282.000, 631.500) d 6.500 | PASS | 7a Console (draft 6): foot bracket bolt into the top rear cross rail's top slot, 23 inboard of the post |
| P-034c | top-panel | hole_at 6.5;-282;730 | 1 | (-282.000, 730.000) d 6.500 | PASS | 7a Console (draft 6): foot bracket bolt into the rear top rail's top slot |
| K-001 | console-face | thickness | 1.5 | 1.5 | PASS | 7a all flat plates 1.5 |
| K-002 | console-face | normal | 0,1,0 | (-0.0, -1.0, -0.0) | PASS | 7a: vertical, facing front |
| K-003 | console-face | outline 690;200 | 1 | rrect 690.000 x 200.000 | PASS | 7a: 690 wide between the cheeks, 200 tall from the top panel to the top of the frame |
| K-004 | console-face | loop rect;0;1084.5;240;120 | 1 | 1 | PASS | uci-spec 4.1 aperture 240 x 120, centred 83 above the top panel's top: the module's nuts clear the front rail (1161.5), the faceplate clears the rail bolts |
| K-005 | console-face | hole_at 4.5;-130;1014.5 | 1 | (-130.000, 1014.500) d 4.500 | PASS | uci-spec 4.1 holes on 260 x 140 |
| K-006 | console-face | hole_at 4.5;130;1014.5 | 1 | (130.000, 1014.500) d 4.500 | PASS | uci-spec 4.1 |
| K-007 | console-face | hole_at 4.5;-130;1154.5 | 1 | (-130.000, 1154.500) d 4.500 | PASS | uci-spec 4.1 |
| K-008 | console-face | hole_at 4.5;130;1154.5 | 1 | (130.000, 1154.500) d 4.500 | PASS | uci-spec 4.1 |
| K-009 | console-face | holes 4.5 | 4 | 4 | PASS | uci-spec 4.1 four holes |
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
| R-040 | dxf | dxf_outline felt-seal;582;582 |  | circle 582.000 x 582.000 | PASS | 7b Seals (draft 6): felt annulus outside radius 291, one drawing for both ends |
| R-041 | dxf | dxf_circles_d felt-seal;546 | 1 | 1 | PASS | 7b Seals: inside radius 273, outside the 540 ring bore |
| M-001 | motor (bought) | size y | 210 | 210.0 | PASS | bom: NEMA 48 frame envelope 200 long (V-106) plus the 6 mm front shaft to the blower and the 4 mm rear shaft to the pulley |
| M-002 | motor (bought) | min y | 184 | 184.0 | PASS | 7a: motor behind the blower (frame from 190, shaft stub to the blower's back face at 184) |
| M-003 | motor (bought) | cyl 70;y;0,120 | 1 | 1 | PASS | 7a Drive: axis at 120 high, 140 envelope |
| M-004 | pulley (bought) | cyl 15;y;0,120 | 5 | 5 | PASS | 7a Drive: PJ pulley, 30 pitch diameter estimate (V-012); five rib bands between four grooves |
| M-005 | pulley (bought) | min y | 394 | 394.0 | PASS | 7a Drive: pulley centred at Y 402, 16 wide |
| M-006 | blower (bought) | cyl 110;y;0,120 | 1 | 1 | PASS | 7a Blower envelope 220 on the motor axis |
| M-007 | blower (bought) | min y | 84 | 84.0 | PASS | 7a Blower on the front shaft |
| M-008 | exhaust-duct (bought) | cyl 51;y;230,150 | 1 | 1 | PASS | 7a Air: 102 exhaust along the bay floor at X 230, 150 high |
| M-009 | exhaust-duct (bought) | max y | 750 | 750.0 | PASS | 7a Air: to the rear lower panel |
| M-009b | exhaust-duct (bought) | min y | 190 | 190.0 | PASS | 7a Air: from the back of the blower's outlet box (draft 4), along the bay floor to the port |
| M-010 | heat-module-tray | min y | 420 | 420.0 | PASS | 7a Air: tray Y 420 to 670 |
| M-011 | heat-module-tray | max y | 670 | 670.0 | PASS | 7a Air |
| M-012 | heat-module-tray | size x | 320 | 320.0 | PASS | 7a: tray 320 wide, centred |
| M-013 | heat-module-tray | min z | 60 | 60.0 | PASS | 7a: on the 2020 tray rails (40 + 20) |
| M-014 | riser-duct | size x | 300 | 300.0 | PASS | 7a Air (draft 6): the hood over the heat module's outlet is 300 wide; the riser itself 260 x 50 |
| M-015 | riser-duct | size y | 143.5 | 143.5 | PASS | 7a Air (draft 6): hood from Y 560 to the riser's back at 703.5 |
| M-016 | riser-duct | min y | 560 | 560.0 | PASS | 7a Air (draft 6): the hood starts over the module's outlet collar (580..640) with 20 to spare |
| M-016b | riser-duct | min z | 230 | 230.0 | PASS | 7a Air (draft 6): riser and hood bottom at 230, above the module's outlet collar (229), so the module leaves by the back under it |
| M-016c | riser-duct | max y | 703.5 | 703.5 | PASS | 7a: riser ends 6.5 in front of the rear rail (710) |
| M-017 | lint-duct | size x | 336 | 336.0 | PASS | 7a Air: lint duct 336 x 36 between the front stubs with 2 mm each side |
| M-018 | lint-duct | size y | 33 | 33.0 | PASS | 7a Air (draft 6): 33 deep, behind the ring bolts' nuts and tips |
| M-019 | lint-duct | min y | 5 | 5.0 | PASS | 7a (draft 6): 0.5 behind the ring bolts' tips (4.5), 5 off the front panel's back |
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
| X-027 | clearance | clearance riser-duct;rail-mid-rearcross | 2 | 2.0 | PASS | 7a Air (draft 6): the hood (top 258) passes under the mid rear cross rail (260) |
| X-028 | clearance | clearance riser-duct;heat-module (envelope) | 1 | 1.0 | PASS | 7a Air (draft 6): hood bottom 230 over the module's outlet collar (229) |
| X-029 | clearance | clearance felt-seal-front;drum-ring-front | 0.5 | 0.5 | PASS | 7b Seals (draft 6): front felt from 41.5 to 49.5 on the front bulkhead, ring face at 50 |
| X-030 | clearance | clearance lint-duct;hardware-door-ring (bought, 8 x M4 x 8 button head, nuts) | 0.5 | 0.5 | PASS | 7a (draft 6): M4 x 8 ring bolts end at 4.5, the duct starts at 5 |
| X-031 | clearance | clearance console-post-1;top-panel | 0 | 0.0 | PASS | 7a Console: posts on the top panel |
| X-032 | clearance | clearance power-cord (bought);feet (bought, 4 x M8 leveling feet, 50 pad) | 45.5 | 45.5 | PASS | 7a Panels (draft 6): the cord runs at X -250, the rear left foot pad (radius 25) at X -325 |
| X-033 | clearance | clearance power-cord (bought);base-pan | 6 | 6.0 | PASS | 7a (draft 6): cord centre line 10.5 under the pan's bottom, 4.5 radius |
| H-001 | feet (bought, 4 x M8 leveling feet, 50 pad) | min z | -19.5 | -19.5 | PASS | 7c Feet (draft 6): pad 10 and hex 8 under the pan |
| H-002 | feet (bought, 4 x M8 leveling feet, 50 pad) | size x | 700 | 700.0000001000001 | PASS | 7c Feet: 50 pads on the post centres at X +-325 |
| H-003 | belt (bought, PJ 5 rib) | size y | 12 | 12.0 | PASS | 7a Drive: PJ 5 ribs, 12 wide, centred on the pulley at Y 402 |
| H-004 | belt (bought, PJ 5 rib) | min y | 396 | 396.0 | PASS | 7a Drive |
| H-005 | belt (bought, PJ 5 rib) | max z | 945 | 945.0 | PASS | 7a Drive: round the drum outside (941.5 + 3.5 belt) |
| H-006 | belt (bought, PJ 5 rib) | min z | 101.5 | 101.5 | PASS | 7a Drive: under the 30 pulley at 120: 120 - 15 - 3.5 |
| H-007 | idler-pulley (bought, flat idler 40 with bearing) | cyl 20;y;-60,165 | 1 | 1 | PASS | 7a Drive: flat idler 40 at (-60, 165), on the slack run |
| H-008 | clearance | clearance belt (bought, PJ 5 rib);drum-sheet | 0 | 0.0 | PASS | 7a Drive: belt on the drum |
| H-009 | clearance | clearance belt (bought, PJ 5 rib);pulley (bought) | 0 | 0.0 | PASS | 7a Drive: belt on the pulley |
| H-010 | clearance | clearance belt (bought, PJ 5 rib);idler-pulley (bought, flat idler 40 with bearing) | 0 | 0.0 | PASS | 7a Drive: belt on the idler |
| H-011 | clearance | clearance belt (bought, PJ 5 rib);motor (bought) | 6 | 6.0 | PASS | 7a Drive: belt plane 396..408 behind the motor frame (to 390) |
| H-012 | clearance | clearance belt (bought, PJ 5 rib);heat-module-tray | 41.761 | 41.761 | PASS | 7a Air: tray plate (Z 60 to 61.5) from Y 420, belt to 408 and down to 101.5: sqrt(12^2 + 40^2) |
| H-013 | door-hinge-1-fixed (bought, flag hinge, pinned half) | cyl 4;z;-278.5,-14 | 2 | 2 | PASS | 7a Door: 8 pin at X -278.5, Y -14, outside the 540 disc; two lengths of pin surface, below and above the fixed knuckle |
| H-014 | door-hinge-1-fixed (bought, flag hinge, pinned half) | cyl 9;z;-278.5,-14 | 1 | 1 | PASS | 7a Door: 18 knuckle |
| H-015 | clearance | clearance door-hinge-1-fixed (bought, flag hinge, pinned half);door-disc | 1.775 | 1.775 | PASS | 7a Door: knuckle face at X -269.5, disc edge at 35 below the axis at sqrt(270^2 - 35^2) = 267.725 |
| H-016 | clearance | clearance door-hinge-2-swing (bought, flag hinge, lift-off half);door-ring | 1.523 | 1.523 | PASS | 7a Door: swinging knuckle 1.5 off the ring face plane, and just outside the ring's 280 edge, so the nearest point is on that edge |
| H-017 | clearance | clearance door-seal (bought, OEM door seal);door-ring | 2 | 2.0 | PASS | 7a Door: 6 seal on the disc, 2 off the ring face when closed (compressed on the real door) |
| H-018 | door-handle (bought, D handle 128 centres) | min y | -57 | -57.0000001 | PASS | 7a Door: handle 128 centres |
| H-019 | door-handle (bought, D handle 128 centres) | cyl 7;y;220,567.5 | 1 | 1 | PASS | 7a Door: handle standoff |
| H-020 | felt-seal-rear | thickness | 8 | 8.0 | PASS | 7a Drum and door: 8 mm felt |
| H-021 | felt-seal-rear | loop circle;0;631.5;582;582 | 1 | 1 | PASS | 7b Seals (draft 6): felt annulus to radius 291, inboard of the 16 tall tabs (293.2) |
| H-022 | felt-seal-rear | loop circle;0;631.5;546;546 | 1 | 1 | PASS | 7b Seals (draft 6): felt annulus from radius 273, outside the 540 ring bore |
| H-023 | clearance | clearance felt-seal-rear;drum-ring-rear | 2 | 2.0 | PASS | 7a: felt from 602 to 610, ring back face at 600 |
| H-023b | felt-seal-front | thickness | 8 | 8.0 | PASS | 7a Drum and door: 8 mm felt at the front too (draft 6) |
| H-023c | felt-seal-front | loop circle;0;631.5;582;582 | 1 | 1 | PASS | 7b Seals |
| H-023d | felt-seal-front | max y | 49.5 | 49.5 | PASS | 7b Seals: on the front bulkhead's back (41.5), ring face at 50 |
| H-024 | tier0-faceplate | thickness | 2 | 2.0 | PASS | tier0 README: 2 mm aluminum |
| H-025 | tier0-faceplate | outline 280;160 | 1 | rrect 280.000 x 160.000 | PASS | tier0 README: 280 x 160 |
| H-026 | tier0-faceplate | holes 4.5 | 8 | 8 | PASS | tier0_drawings: 4 mounting, 2 DIN rail standoffs, 2 cable ties |
| H-027 | tier0-faceplate | holes 12 | 2 | 2 | PASS | tier0_drawings: two timer shaft holes |
| H-028 | tier0-faceplate | holes 4 | 4 | 4 | PASS | tier0_drawings: four yoke holes at 83.3 |
| H-029 | tier0-faceplate | holes 22.3 | 2 | 2 | PASS | tier0_drawings: two 22 mm devices |
| H-030 | tier0-faceplate | hole_at 12;-80;1084.5 | 1 | (-80.000, 1084.500) d 12.000 | PASS | tier0_drawings: DRY TIME shaft on the faceplate's centre line, the aperture centre (1084.5) |
| H-031 | tier0-faceplate | hole_at 22.3;90;1104.5 | 1 | (90.000, 1104.500) d 22.300 | PASS | tier0_drawings (faceplate draft 2): START, 20 above the centre line so K1 fits below the 22 mm devices |
| H-031b | tier0-faceplate | hole_at 4.5;25;1060.5 | 1 | (25.000, 1060.500) d 4.500 | PASS | tier0_drawings (faceplate draft 2): K1 rail standoff, 24 below the centre line; the socket hangs 36 below it, to the aperture's edge |
| H-032 | clearance | clearance tier0-faceplate;console-face | 0 | 0.0 | PASS | uci-spec 4.1: faceplate on the chassis panel |
| H-034 | clearance | clearance feet (bought, 4 x M8 leveling feet, 50 pad);base-pan | 0 | 0.0 | PASS | 7c Feet: hex against the pan |
| H-035 | clearance | clearance hardware-drum-tabs (bought, 60 x M4 x 8 button head, nuts);front-bulkhead | 2.5 | 2.5 | PASS | 7b: bolt tips at 44, bulkhead back face at 41.5 |
| H-036 | clearance | clearance idler-pulley (bought, flat idler 40 with bearing);motor (bought) | 4.5 | 4.5 | PASS | 7a Drive: idler flange at 394.5, motor end bell to 390 |
| H-038 | cut-list | cut idler-arm | 175.4 | 175.4 | PASS | 7a Drive: pivot (-115, 25) to idler (-60, 165) is 150.4 plus 12.5 past each hole |
| H-039 | cut-list | cut_qty idler-bracket, spring-bracket | 2 | 2 | PASS | 7a Drive |

## 2. Generic checks on every part

| part | check | measured | result |
|---|---|---|---|
| base-pan | one solid | 1 | PASS |
| base-pan | valid B-rep (BRepCheck) | 1 | PASS |
| base-pan | closed shells | 1 | PASS |
| base-pan | volume positive | 770723.4 | PASS |
| base-pan | in the assembly with the same volume and place | True | PASS |
| base-pan | section edges all closed | 0 | PASS |
| base-pan | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 30 loops, 0 unclassified | PASS |
| base-pan | every cut lies inside the outline | 29 | PASS |
| base-pan | no two cuts overlap | 0 overlapping pairs | PASS |
| base-pan.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| base-pan.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 30 matched, 0 only in STEP, 0 only in DXF | PASS |
| base-pan.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
| bay-ceiling | one solid | 1 | PASS |
| bay-ceiling | valid B-rep (BRepCheck) | 1 | PASS |
| bay-ceiling | closed shells | 1 | PASS |
| bay-ceiling | volume positive | 689357.8 | PASS |
| bay-ceiling | in the assembly with the same volume and place | True | PASS |
| bay-ceiling | section edges all closed | 0 | PASS |
| bay-ceiling | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 25 loops, 0 unclassified | PASS |
| bay-ceiling | every cut lies inside the outline | 24 | PASS |
| bay-ceiling | no two cuts overlap | 0 overlapping pairs | PASS |
| bay-ceiling.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| bay-ceiling.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 25 matched, 0 only in STEP, 0 only in DXF | PASS |
| bay-ceiling.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
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
| console-face | volume positive | 163260.0 | PASS |
| console-face | in the assembly with the same volume and place | True | PASS |
| console-face | section edges all closed | 0 | PASS |
| console-face | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 14 loops, 0 unclassified | PASS |
| console-face | every cut lies inside the outline | 13 | PASS |
| console-face | no two cuts overlap | 0 overlapping pairs | PASS |
| console-face.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| console-face.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 14 matched, 0 only in STEP, 0 only in DXF | PASS |
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
| door-ring | volume positive | 145225.6 | PASS |
| door-ring | in the assembly with the same volume and place | True | PASS |
| door-ring | section edges all closed | 0 | PASS |
| door-ring | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 12 loops, 0 unclassified | PASS |
| door-ring | every cut lies inside the outline | 11 | PASS |
| door-ring | no two cuts overlap | 0 overlapping pairs | PASS |
| door-ring.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| door-ring.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 12 matched, 0 only in STEP, 0 only in DXF | PASS |
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
| felt-seal-front | one solid | 1 | PASS |
| felt-seal-front | valid B-rep (BRepCheck) | 1 | PASS |
| felt-seal-front | closed shells | 1 | PASS |
| felt-seal-front | volume positive | 255147.6 | PASS |
| felt-seal-front | in the assembly with the same volume and place | True | PASS |
| felt-seal-front | section edges all closed | 0 | PASS |
| felt-seal-front | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 2 loops, 0 unclassified | PASS |
| felt-seal-front | every cut lies inside the outline | 1 | PASS |
| felt-seal-front | no two cuts overlap | 0 overlapping pairs | PASS |
| felt-seal-rear | one solid | 1 | PASS |
| felt-seal-rear | valid B-rep (BRepCheck) | 1 | PASS |
| felt-seal-rear | closed shells | 1 | PASS |
| felt-seal-rear | volume positive | 255147.6 | PASS |
| felt-seal-rear | in the assembly with the same volume and place | True | PASS |
| felt-seal-rear | section edges all closed | 0 | PASS |
| felt-seal-rear | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 2 loops, 0 unclassified | PASS |
| felt-seal-rear | every cut lies inside the outline | 1 | PASS |
| felt-seal-rear | no two cuts overlap | 0 overlapping pairs | PASS |
| front-bulkhead | one solid | 1 | PASS |
| front-bulkhead | valid B-rep (BRepCheck) | 1 | PASS |
| front-bulkhead | closed shells | 1 | PASS |
| front-bulkhead | volume positive | 404709.8 | PASS |
| front-bulkhead | in the assembly with the same volume and place | True | PASS |
| front-bulkhead | section edges all closed | 0 | PASS |
| front-bulkhead | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 12 loops, 0 unclassified | PASS |
| front-bulkhead | every cut lies inside the outline | 11 | PASS |
| front-bulkhead | no two cuts overlap | 0 overlapping pairs | PASS |
| front-bulkhead.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| front-bulkhead.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 12 matched, 0 only in STEP, 0 only in DXF | PASS |
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
| front-upper-panel | volume positive | 493333.2 | PASS |
| front-upper-panel | in the assembly with the same volume and place | True | PASS |
| front-upper-panel | section edges all closed | 0 | PASS |
| front-upper-panel | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 28 loops, 0 unclassified | PASS |
| front-upper-panel | every cut lies inside the outline | 27 | PASS |
| front-upper-panel | no two cuts overlap | 0 overlapping pairs | PASS |
| front-upper-panel.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| front-upper-panel.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 28 matched, 0 only in STEP, 0 only in DXF | PASS |
| front-upper-panel.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
| heat-module-tray | one solid | 1 | PASS |
| heat-module-tray | valid B-rep (BRepCheck) | 1 | PASS |
| heat-module-tray | closed shells | 1 | PASS |
| heat-module-tray | volume positive | 120000.0 | PASS |
| heat-module-tray | in the assembly with the same volume and place | True | PASS |
| heat-module-tray | section edges all closed | 0 | PASS |
| heat-module-tray | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 1 loops, 0 unclassified | PASS |
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
| lint-duct | volume positive | 3270960.0 | PASS |
| lint-duct | in the assembly with the same volume and place | True | PASS |
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
| rear-bulkhead | volume positive | 652302.1 | PASS |
| rear-bulkhead | in the assembly with the same volume and place | True | PASS |
| rear-bulkhead | section edges all closed | 0 | PASS |
| rear-bulkhead | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 139 loops, 0 unclassified | PASS |
| rear-bulkhead | every cut lies inside the outline | 138 | PASS |
| rear-bulkhead | no two cuts overlap | 0 overlapping pairs | PASS |
| rear-bulkhead.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| rear-bulkhead.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 139 matched, 0 only in STEP, 0 only in DXF | PASS |
| rear-bulkhead.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
| rear-lower-panel | one solid | 1 | PASS |
| rear-lower-panel | valid B-rep (BRepCheck) | 1 | PASS |
| rear-lower-panel | closed shells | 1 | PASS |
| rear-lower-panel | volume positive | 240240.9 | PASS |
| rear-lower-panel | in the assembly with the same volume and place | True | PASS |
| rear-lower-panel | section edges all closed | 0 | PASS |
| rear-lower-panel | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 42 loops, 0 unclassified | PASS |
| rear-lower-panel | every cut lies inside the outline | 41 | PASS |
| rear-lower-panel | no two cuts overlap | 0 overlapping pairs | PASS |
| rear-lower-panel.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| rear-lower-panel.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 42 matched, 0 only in STEP, 0 only in DXF | PASS |
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
| riser-duct | one solid | 1 | PASS |
| riser-duct | valid B-rep (BRepCheck) | 1 | PASS |
| riser-duct | closed shells | 1 | PASS |
| riser-duct | volume positive | 8530900.0 | PASS |
| riser-duct | in the assembly with the same volume and place | True | PASS |
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
| tier0-faceplate | volume positive | 87020.2 | PASS |
| tier0-faceplate | in the assembly with the same volume and place | True | PASS |
| tier0-faceplate | section edges all closed | 0 | PASS |
| tier0-faceplate | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 17 loops, 0 unclassified | PASS |
| tier0-faceplate | every cut lies inside the outline | 16 | PASS |
| tier0-faceplate | no two cuts overlap | 0 overlapping pairs | PASS |
| tier0-faceplate.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| tier0-faceplate.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 17 matched, 0 only in STEP, 0 only in DXF | PASS |
| tier0-faceplate.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 1084.50) | PASS |
| top-panel | one solid | 1 | PASS |
| top-panel | valid B-rep (BRepCheck) | 1 | PASS |
| top-panel | closed shells | 1 | PASS |
| top-panel | volume positive | 775208.2 | PASS |
| top-panel | in the assembly with the same volume and place | True | PASS |
| top-panel | section edges all closed | 0 | PASS |
| top-panel | every section loop is a circle, rectangle, rounded rectangle or polygon, slot or polygon | 21 loops, 0 unclassified | PASS |
| top-panel | every cut lies inside the outline | 20 | PASS |
| top-panel | no two cuts overlap | 0 overlapping pairs | PASS |
| top-panel.dxf | DXF entities join into closed loops | 0 open chains | PASS |
| top-panel.dxf | every loop in the DXF matches a loop in the STEP section (type, centre, size, 0.01 mm) | 21 matched, 0 only in STEP, 0 only in DXF | PASS |
| top-panel.dxf | DXF drawn in world coordinates or about the origin | offset (0.00, 0.00) | PASS |
| tray-rail-1 | one solid | 1 | PASS |
| tray-rail-1 | valid B-rep (BRepCheck) | 1 | PASS |
| tray-rail-1 | closed shells | 1 | PASS |
| tray-rail-1 | volume positive | 72929.6 | PASS |
| tray-rail-1 | in the assembly with the same volume and place | True | PASS |
| tray-rail-2 | one solid | 1 | PASS |
| tray-rail-2 | valid B-rep (BRepCheck) | 1 | PASS |
| tray-rail-2 | closed shells | 1 | PASS |
| tray-rail-2 | volume positive | 72929.6 | PASS |
| tray-rail-2 | in the assembly with the same volume and place | True | PASS |
| side-panel-left | every M6 hole sits on a frame rail centre line (or is a listed through-bolted hole) | 29 M6 holes, 0 through-bolted, 0 off a rail | PASS |
| side-panel-right | every M6 hole sits on a frame rail centre line (or is a listed through-bolted hole) | 29 M6 holes, 0 through-bolted, 0 off a rail | PASS |
| front-upper-panel | every M6 hole sits on a frame rail centre line (or is a listed through-bolted hole) | 18 M6 holes, 2 through-bolted, 0 off a rail | PASS |
| front-lower-panel | every M6 hole sits on a frame rail centre line (or is a listed through-bolted hole) | 8 M6 holes, 0 through-bolted, 0 off a rail | PASS |
| rear-upper-panel | every M6 hole sits on a frame rail centre line (or is a listed through-bolted hole) | 18 M6 holes, 0 through-bolted, 0 off a rail | PASS |
| rear-lower-panel | every M6 hole sits on a frame rail centre line (or is a listed through-bolted hole) | 8 M6 holes, 0 through-bolted, 0 off a rail | PASS |
| top-panel | every M6 hole sits on a frame rail centre line (or is a listed through-bolted hole) | 20 M6 holes, 0 through-bolted, 0 off a rail | PASS |
| base-pan | every M6 hole sits on a frame rail centre line (or is a listed through-bolted hole) | 24 M6 holes, 4 through-bolted, 0 off a rail | PASS |
| bay-ceiling | every M6 hole sits on a frame rail centre line (or is a listed through-bolted hole) | 20 M6 holes, 0 through-bolted, 0 off a rail | PASS |
| front-bulkhead | every M6 hole sits on a frame rail centre line (or is a listed through-bolted hole) | 7 M6 holes, 0 through-bolted, 0 off a rail | PASS |
| rear-bulkhead | every M6 hole sits on a frame rail centre line (or is a listed through-bolted hole) | 10 M6 holes, 0 through-bolted, 0 off a rail | PASS |
| console-face | every M6 hole sits on a frame rail centre line (or is a listed through-bolted hole) | 8 M6 holes, 0 through-bolted, 0 off a rail | PASS |
| console-rear | every M6 hole sits on a frame rail centre line (or is a listed through-bolted hole) | 8 M6 holes, 0 through-bolted, 0 off a rail | PASS |
| console-cap | every M6 hole sits on a frame rail centre line (or is a listed through-bolted hole) | 10 M6 holes, 0 through-bolted, 0 off a rail | PASS |
| console-cheek-left | every M6 hole sits on a frame rail centre line (or is a listed through-bolted hole) | 5 M6 holes, 0 through-bolted, 0 off a rail | PASS |
| console-cheek-right | every M6 hole sits on a frame rail centre line (or is a listed through-bolted hole) | 5 M6 holes, 0 through-bolted, 0 off a rail | PASS |
| console-face | the only M4 holes are the four UCI-D module holes (uci-spec 4.1) | 4 M4 holes | PASS |
| all parts | V-011: every round feature deeper than 0.5 mm has a diameter on the named list (3 2020 corner radius 1.5, 4 4040 corner radius 2 / timer yoke holes, 4.2 2020 centre bore, 4.5 M4 clearance, 5 louver slot ends (60 x 5), 6 corner radius 3 (cheeks, tabs, splice, idler arm ends), 6.5 M6 clearance, 6.8 4040 centre bore (tapped M8 for the feet), 8.5 M8 clearance (feet studs), 10 inlet holes, 10.5 roller shafts, 12 plate corner radius 6 / timer shaft holes, 20 faceplate corner radius 10, 22 cord strain relief bushing, 22.3 22 mm panel devices, 40 lint slot ends (260 x 40), 106 exhaust port (102 duct + 2 each side), 460 door opening, 470 door ring bore, 476 lint slot inner arc (radius 238), 480 front panel ring opening, 532 lint slot outer arc (radius 266), 540 door disc / drum ring bore, 546 felt seal inside (radius 273), 560 door ring, 582 felt seal outside (radius 291), 616.4 splice inside, 618.4 drum ring / sheet inside, 620 drum outside) | 0 off the list | PASS |
| air path | V-013: every opening in the air path is at least the blower outlet (102 round, 8171 mm2) | riser 13000, riser_hood 8400, lint_duct 11088, lint_slot 8867, inlet_field 9896, exhaust_duct 8171 | PASS |
| assembly | no two solids overlap by more than 1 mm3 (file re-import) | 127 solids, 0 overlaps | PASS |
| assembly | every part file is a named solid in the assembly | 0 missing | PASS |
| drum-sheet.dxf | every hole in the rolled solid unwraps onto a hole in the flat pattern (0.05 mm) | 88 matched, 0 solid-only, 0 DXF-only | PASS |
| drum-sheet.dxf | flat pattern outline is the sheet's unrolled mid-surface length by its length plus the tabs | rpoly 1945.274 x 582.000, 244 edges; unrolled 1945.274 | PASS |
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
| lint-duct | rail-mid-front-left | 2.000 |
| lint-duct | rail-mid-front-right | 2.000 |
| lint-duct | front-bulkhead | 2.000 |
| lint-duct | front-upper-panel | 5.000 |
| riser-duct | rear-bulkhead | 7.000 |
| riser-duct | rail-mid-rear | 6.500 |
| riser-duct | bay-ceiling | 2.000 |
| heat-module (envelope) | heat-module-tray | 0.500 |
| heat-module (envelope) | bay-ceiling | 71.000 |
| motor (bought) | base-pan | 50.000 |
| blower (bought) | front-bulkhead | 55.057 |
| blower (bought) | lint-duct-transition | 0.000 |
| pulley (bought) | bay-ceiling | 165.000 |
| exhaust-duct (bought) | rear-lower-panel | 2.000 |
| power-module (envelope) | side-panel-left | 5.000 |
| power-module (envelope) | bay-ceiling | 80.000 |
| drum-sheet | front-upper-panel | 49.200 |
| belt (bought, PJ 5 rib) | drum-sheet | 0.000 |
| belt (bought, PJ 5 rib) | pulley (bought) | 0.000 |
| belt (bought, PJ 5 rib) | idler-pulley (bought, flat idler 40 with bearing) | 0.000 |
| belt (bought, PJ 5 rib) | bay-ceiling | 13.565 |
| belt (bought, PJ 5 rib) | motor (bought) | 6.000 |
| belt (bought, PJ 5 rib) | heat-module-tray | 41.761 |
| door-hinge-1-fixed (bought, flag hinge, pinned half) | door-disc | 1.775 |
| door-hinge-2-swing (bought, flag hinge, lift-off half) | door-ring | 1.523 |
| door-seal (bought, OEM door seal) | door-ring | 2.000 |
| felt-seal-rear | drum-ring-rear | 2.000 |
| felt-seal-front | drum-ring-front | 0.500 |
| felt-seal-front | drum-sheet | 2.200 |
| felt-seal-rear | drum-sheet | 2.506 |
| tier0-faceplate | console-face | 0.000 |
| riser-duct | heat-module (envelope) | 1.000 |
| riser-duct | rail-mid-rearcross | 2.000 |
| riser-duct | heat-module-tray | 168.500 |
| lint-duct | hardware-door-ring (bought, 8 x M4 x 8 button head, nuts) | 0.500 |
| console-post-1 | top-panel | 0.000 |
| console-post-1 | console-cheek-left | 0.000 |
| console-rail-front | console-cap | 0.000 |
| console-rear | rear-upper-panel | 0.000 |
| console-cheek-left | side-panel-left | 0.000 |
| tier0-k1-relay-on-din-rail (bought) | console-rail-front | 82.000 |
| tier0-k1-relay-on-din-rail (bought) | top-panel | 23.000 |
| power-cord (bought) | cord-bushing (bought, PG16 strain relief) | 0.100 |
| power-cord (bought) | feet (bought, 4 x M8 leveling feet, 50 pad) | 45.500 |
| power-cord (bought) | base-pan | 6.000 |
| feet (bought, 4 x M8 leveling feet, 50 pad) | base-pan | 0.000 |
| hardware-drum-tabs (bought, 60 x M4 x 8 button head, nuts) | front-bulkhead | 2.500 |
| idler-pulley (bought, flat idler 40 with bearing) | motor (bought) | 4.500 |
| hardware-idler-axle (bought, M8 x 30 bolt, nut) | motor (bought) | 7.000 |

## 5. Inventory

Every part: bounding box, volume, faces. The full feature lists are in `measured-cylinders.csv` (every hole and round surface), `measured-planes.csv` (every flat face) and `measured-loops.csv` (every closed loop of every flat part's section and of every DXF).

| part | solids | X min..max | Y min..max | Z min..max | size | volume mm3 | faces (planar / cylindrical / other) | thickness | section loops |
|---|---|---|---|---|---|---|---|---|---|
| base-pan | 1 | -343.50..343.50 | -0.00..750.00 | -1.50..0.00 | 687.00 x 750.00 x 1.50 | 770723.4 | 39 (6 / 33 / 0) | 1.500 | 30 |
| bay-ceiling | 1 | -343.50..343.50 | 42.00..750.00 | 300.00..301.50 | 687.00 x 708.00 x 1.50 | 689357.8 | 48 (26 / 22 / 0) | 1.500 | 25 |
| console-cap | 1 | -346.50..346.50 | 610.00..751.50 | 1201.50..1203.00 | 693.00 x 141.50 x 1.50 | 146545.1 | 20 (6 / 14 / 0) | 1.500 | 11 |
| console-cheek-left | 1 | -346.50..-345.00 | 610.00..751.50 | 1000.00..1201.50 | 1.50 x 141.50 x 201.50 | 42473.1 | 15 (6 / 9 / 0) | 1.500 | 6 |
| console-cheek-right | 1 | 345.00..346.50 | 610.00..751.50 | 1000.00..1201.50 | 1.50 x 141.50 x 201.50 | 42473.1 | 15 (6 / 9 / 0) | 1.500 | 6 |
| console-face | 1 | -345.00..345.00 | 610.00..611.50 | 1001.50..1201.50 | 690.00 x 1.50 x 200.00 | 163260.0 | 26 (10 / 16 / 0) | 1.500 | 14 |
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
| door-ring | 1 | -280.00..280.00 | -3.50..-1.50 | 351.50..911.50 | 560.00 x 2.00 x 560.00 | 145225.6 | 14 (2 / 12 / 0) | 2.000 | 12 |
| drum-ring-front | 1 | -309.20..309.20 | 50.00..52.00 | 322.30..940.70 | 618.40 x 2.00 x 618.40 | 141703.2 | 34 (2 / 32 / 0) | 2.000 | 32 |
| drum-ring-rear | 1 | -309.20..309.20 | 598.00..600.00 | 322.30..940.70 | 618.40 x 2.00 x 618.40 | 141703.2 | 34 (2 / 32 / 0) | 2.000 | 32 |
| drum-sheet | 1 | -310.00..310.00 | 49.20..600.80 | 321.50..941.50 | 620.00 x 551.60 x 620.00 | 873714.1 | 600 (360 / 240 / 0) | | |
| drum-splice | 1 | -29.96..29.96 | 53.00..597.00 | 938.24..940.70 | 59.92 x 544.00 x 2.46 | 32383.4 | 26 (4 / 22 / 0) | | |
| felt-seal-front | 1 | -291.00..291.00 | 41.50..49.50 | 340.50..922.50 | 582.00 x 8.00 x 582.00 | 255147.6 | 4 (2 / 2 / 0) | 8.000 | 2 |
| felt-seal-rear | 1 | -291.00..291.00 | 602.00..610.00 | 340.50..922.50 | 582.00 x 8.00 x 582.00 | 255147.6 | 4 (2 / 2 / 0) | 8.000 | 2 |
| front-bulkhead | 1 | -305.00..305.00 | 40.00..41.50 | 265.00..995.00 | 610.00 x 1.50 x 730.00 | 404709.8 | 24 (8 / 16 / 0) | 1.500 | 12 |
| front-lower-panel | 1 | -345.00..345.00 | -1.50..0.00 | -0.00..259.00 | 690.00 x 1.50 x 259.00 | 242871.1 | 242 (118 / 124 / 0) | 1.500 | 65 |
| front-upper-panel | 1 | -345.00..345.00 | -1.50..0.00 | 260.00..1000.00 | 690.00 x 1.50 x 740.00 | 493333.2 | 37 (6 / 31 / 0) | 1.500 | 28 |
| heat-module-tray | 1 | -160.00..160.00 | 420.00..670.00 | 60.00..61.50 | 320.00 x 250.00 x 1.50 | 120000.0 | 6 (6 / 0 / 0) | 1.500 | 1 |
| lint-duct-transition | 1 | -110.00..110.00 | 38.00..84.00 | 50.00..190.00 | 220.00 x 46.00 x 140.00 | 1416800.0 | 6 (6 / 0 / 0) | | |
| lint-duct | 1 | -168.00..168.00 | 5.00..38.00 | 150.00..445.00 | 336.00 x 33.00 x 295.00 | 3270960.0 | 6 (6 / 0 / 0) | | |
| post-1 | 1 | -345.00..-305.00 | 0.00..40.00 | 0.00..1000.00 | 40.00 x 40.00 x 1000.00 | 1088617.6 | 59 (54 / 5 / 0) | | |
| post-2 | 1 | 305.00..345.00 | 0.00..40.00 | 0.00..1000.00 | 40.00 x 40.00 x 1000.00 | 1088617.6 | 59 (54 / 5 / 0) | | |
| post-3 | 1 | -345.00..-305.00 | 710.00..750.00 | 0.00..1000.00 | 40.00 x 40.00 x 1000.00 | 1088617.6 | 59 (54 / 5 / 0) | | |
| post-4 | 1 | 305.00..345.00 | 710.00..750.00 | 0.00..1000.00 | 40.00 x 40.00 x 1000.00 | 1088617.6 | 59 (54 / 5 / 0) | | |
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
| rear-bulkhead | 1 | -305.00..305.00 | 610.00..611.50 | 265.00..995.00 | 610.00 x 1.50 x 730.00 | 652302.1 | 148 (6 / 142 / 0) | 1.500 | 139 |
| rear-lower-panel | 1 | -345.00..345.00 | 750.00..751.50 | -0.00..259.00 | 690.00 x 1.50 x 259.00 | 240240.9 | 147 (70 / 77 / 0) | 1.500 | 42 |
| rear-upper-panel | 1 | -345.00..345.00 | 750.00..751.50 | 260.00..1000.00 | 690.00 x 1.50 x 740.00 | 764957.7 | 28 (6 / 22 / 0) | 1.500 | 19 |
| riser-duct | 1 | -150.00..150.00 | 560.00..703.50 | 230.00..821.50 | 300.00 x 143.50 x 591.50 | 8530900.0 | 10 (10 / 0 / 0) | | |
| side-panel-left | 1 | -346.50..-345.00 | -0.00..750.00 | -0.00..1000.00 | 1.50 x 750.00 x 1000.00 | 1123510.2 | 39 (6 / 33 / 0) | 1.500 | 30 |
| side-panel-right | 1 | 345.00..346.50 | -0.00..750.00 | -0.00..1000.00 | 1.50 x 750.00 x 1000.00 | 1123510.2 | 39 (6 / 33 / 0) | 1.500 | 30 |
| tier0-faceplate | 1 | -140.00..140.00 | 608.00..610.00 | 1004.50..1164.50 | 280.00 x 2.00 x 160.00 | 87020.2 | 513 (359 / 20 / 134) | 2.000 | 17 |
| top-panel | 1 | -345.00..345.00 | -0.00..750.00 | 1000.00..1001.50 | 690.00 x 750.00 x 1.50 | 775208.2 | 30 (6 / 24 / 0) | 1.500 | 21 |
| tray-rail-1 | 1 | -170.00..-150.00 | 340.00..700.00 | 40.00..60.00 | 20.00 x 360.00 x 20.00 | 72929.6 | 59 (54 / 5 / 0) | | |
| tray-rail-2 | 1 | 150.00..170.00 | 340.00..700.00 | 40.00..60.00 | 20.00 x 360.00 x 20.00 | 72929.6 | 59 (54 / 5 / 0) | | |

Bought parts and envelopes in the assembly (no part file):

| solid | X min..max | Y min..max | Z min..max | volume mm3 |
|---|---|---|---|---|
| feet (bought, 4 x M8 leveling feet, 50 pad) | -350.00..350.00 | -5.00..755.00 | -19.50..35.00 | 93105.7 |
| hardware-front-bulkhead (bought, 7 x M6 x 12 hex, washers, T-nuts) | -281.00..281.00 | 29.50..47.10 | 274.00..986.00 | 6009.1 |
| hardware-rear-bulkhead (bought, 10 x M6 x 12 hex, washers, T-nuts) | -281.00..281.00 | 604.40..622.00 | 274.00..986.00 | 8584.5 |
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
| hardware-tier0-faceplate (bought, 4 x M4 x 10 button head, nuts) | -134.04..134.04 | 605.80..618.00 | 1010.70..1158.30 | 1181.0 |
| tier0-knob-dry-time (bought) | -100.00..-60.00 | 586.80..611.50 | 1064.50..1104.50 | 15189.3 |
| tier0-timer-dry-time (bought) | -100.30..-59.70 | 610.00..641.70 | 1031.30..1137.70 | 90563.2 |
| tier0-knob-heat-time (bought) | -40.00..0.00 | 586.80..611.50 | 1064.50..1104.50 | 15189.3 |
| tier0-timer-heat-time (bought) | -40.30..0.30 | 610.00..641.70 | 1031.30..1137.70 | 90563.2 |
| tier0-selector-body (bought) | 30.00..60.00 | 605.50..656.50 | 1087.00..1122.00 | 34073.2 |
| tier0-selector (bought) | 34.00..56.00 | 595.50..605.50 | 1089.50..1119.50 | 2878.1 |
| tier0-start-body (bought) | 75.00..105.00 | 605.50..656.50 | 1087.00..1122.00 | 34073.2 |
| tier0-start-button (bought) | 79.00..101.00 | 597.50..605.50 | 1093.50..1115.50 | 2984.1 |
| tier0-k1-relay-on-din-rail (bought) | 15.00..115.00 | 610.00..694.50 | 1024.50..1079.50 | 127556.4 |
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
| motor (bought) | -70.00..70.00 | 184.00..394.00 | 50.00..210.00 | 3047064.1 |
| motor-mount-1 (bought, cradle) | -35.00..35.00 | 215.00..245.00 | 0.00..58.80 | 110279.0 |
| motor-mount-2 (bought, cradle) | -35.00..35.00 | 335.00..365.00 | 0.00..58.80 | 110279.0 |
| pulley (bought) | -15.00..15.00 | 394.00..416.00 | 105.00..135.00 | 12673.5 |
| blower (bought) | -110.00..270.00 | 84.00..190.00 | 10.00..230.00 | 4753032.3 |
| heat-module (envelope) | -140.00..140.00 | 440.00..650.00 | 62.00..229.00 | 9508800.0 |
| power-module (envelope) | -340.00..-170.00 | 450.00..700.00 | 40.00..220.00 | 7650000.0 |
| exhaust-duct (bought) | 179.00..281.00 | 190.00..750.00 | 99.00..201.00 | 4575918.2 |
| cord-bushing (bought, PG16 strain relief) | -265.01..-234.99 | 677.00..703.00 | -6.50..18.00 | 8877.4 |
| power-cord (bought) | -254.50..-245.50 | 685.50..820.00 | -16.50..40.00 | 11456.8 |
| roller-rear-1 (bought) | -200.00..-140.00 | 575.00..600.00 | 307.05..367.05 | 70685.8 |
| roller-front-1 (bought) | -200.00..-140.00 | 50.00..75.00 | 307.05..367.05 | 70685.8 |
| roller-rear-2 (bought) | 140.00..200.00 | 575.00..600.00 | 307.05..367.05 | 70685.8 |
| roller-front-2 (bought) | 140.00..200.00 | 50.00..75.00 | 307.05..367.05 | 70685.8 |
| belt (bought, PJ 5 rib) | -313.50..313.50 | 396.00..408.00 | 101.50..945.00 | 93764.6 |
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
| base-pan | ARC 4, CIRCLE 29, LINE 4 | 30 | 0 | circle 29, rrect 1 |
| bay-ceiling | ARC 2, CIRCLE 20, LINE 24 | 25 | 0 | circle 20, rect 4, rpoly 1 |
| console-cap | ARC 4, CIRCLE 10, LINE 4 | 11 | 0 | circle 10, rrect 1 |
| console-cheek-left | ARC 4, CIRCLE 5, LINE 4 | 6 | 0 | circle 5, rrect 1 |
| console-cheek-right | ARC 4, CIRCLE 5, LINE 4 | 6 | 0 | circle 5, rrect 1 |
| console-face | ARC 4, CIRCLE 12, LINE 8 | 14 | 0 | circle 12, rect 1, rrect 1 |
| console-rear | ARC 4, CIRCLE 8, LINE 4 | 9 | 0 | circle 8, rrect 1 |
| door-disc | CIRCLE 5 | 5 | 0 | circle 5 |
| door-ring | CIRCLE 12 | 12 | 0 | circle 12 |
| drum-ring | CIRCLE 32 | 32 | 0 | circle 32 |
| drum-sheet | ARC 120, CIRCLE 88, LINE 244 | 89 | 0 | circle 88, rpoly 1 |
| drum-splice | ARC 4, CIRCLE 16, LINE 4 | 17 | 0 | circle 16, rrect 1 |
| felt-seal | CIRCLE 2 | 2 | 0 | circle 2 |
| front-bulkhead | ARC 6, CIRCLE 10, LINE 6 | 12 | 0 | circle 10, rrect 1, sector 1 |
| front-lower-panel | ARC 116, CIRCLE 8, LINE 116 | 65 | 0 | circle 8, rrect 1, slot 56 |
| front-upper-panel | ARC 4, CIRCLE 27, LINE 4 | 28 | 0 | circle 27, rrect 1 |
| rear-bulkhead | ARC 4, CIRCLE 138, LINE 4 | 139 | 0 | circle 138, rrect 1 |
| rear-lower-panel | ARC 68, CIRCLE 9, LINE 68 | 42 | 0 | circle 9, rrect 1, slot 32 |
| rear-upper-panel | ARC 4, CIRCLE 18, LINE 4 | 19 | 0 | circle 18, rrect 1 |
| side-panel-left | ARC 4, CIRCLE 29, LINE 4 | 30 | 0 | circle 29, rrect 1 |
| side-panel-right | ARC 4, CIRCLE 29, LINE 4 | 30 | 0 | circle 29, rrect 1 |
| tier0-faceplate | CIRCLE 16, LWPOLYLINE 1, LWPOLYLINE (not CUT) 1, TEXT (not CUT) 6 | 17 | 0 | circle 16, rrect 1 |
| top-panel | ARC 4, CIRCLE 20, LINE 4 | 21 | 0 | circle 20, rrect 1 |

## Notes

- drum-sheet.dxf offset from the unwrapped solid: (0.000, -0.000)
- drum-splice.dxf offset from the unwrapped solid: (-0.005, -0.000)
