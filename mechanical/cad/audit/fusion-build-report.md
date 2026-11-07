# The parametric Fusion build against the script's files

The Fusion comparison section of `cad_audit.py --fusion fusion-build-measured.csv --fusion-partial`, run on the document
`fusion_build.py` builds (stages A to G, 2026-11-07, Fusion 2706.1.17), measured there by `fusion_audit.py`'s
`measure_active()` at high accuracy: every body of the 213 components against the OpenCascade measurements of the
script's assembly STEP, by name. The document checks and generic checks of that run are the same as in
`audit-report.md`; this file keeps the comparison. The one allowed difference is the Tier 0 faceplate's engraved text
(`../fusion_build/README.md`, Intended differences).

Document checks: 603, generic checks: 741, Fusion comparisons: 640. **Failures: 0.**

## 3. The same files measured inside Autodesk Fusion

Fusion record: `fusion-build-measured.csv`, written by `fusion_audit.py` running inside Fusion. CHECK means the two kernels count faces differently (Fusion may split or merge periodic faces); it is not a geometry difference.

| file | body | comparison | values | result |
|---|---|---|---|---|
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
| osa-dryer-assembly | front-bulkhead | volume (mm3) | OCP 403407.561 / Fusion 403407.561 | PASS |
| osa-dryer-assembly | front-bulkhead | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | front-bulkhead | solid body | 1 | PASS |
| osa-dryer-assembly | rear-bulkhead | volume (mm3) | OCP 652057.649 / Fusion 652057.649 | PASS |
| osa-dryer-assembly | rear-bulkhead | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | rear-bulkhead | solid body | 1 | PASS |
| osa-dryer-assembly | bay-ceiling | volume (mm3) | OCP 685439.751 / Fusion 685439.751 | PASS |
| osa-dryer-assembly | bay-ceiling | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | bay-ceiling | solid body | 1 | PASS |
| osa-dryer-assembly | base-pan | volume (mm3) | OCP 770130.214 / Fusion 770130.214 | PASS |
| osa-dryer-assembly | base-pan | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | base-pan | solid body | 1 | PASS |
| osa-dryer-assembly | side-panel-left | volume (mm3) | OCP 1123510.182 / Fusion 1123510.182 | PASS |
| osa-dryer-assembly | side-panel-left | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | side-panel-left | solid body | 1 | PASS |
| osa-dryer-assembly | side-panel-right | volume (mm3) | OCP 1123510.182 / Fusion 1123510.182 | PASS |
| osa-dryer-assembly | side-panel-right | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | side-panel-right | solid body | 1 | PASS |
| osa-dryer-assembly | front-upper-panel | volume (mm3) | OCP 493200.416 / Fusion 493200.416 | PASS |
| osa-dryer-assembly | front-upper-panel | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | front-upper-panel | solid body | 1 | PASS |
| osa-dryer-assembly | front-lower-panel | volume (mm3) | OCP 242871.113 / Fusion 242871.113 | PASS |
| osa-dryer-assembly | front-lower-panel | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | front-lower-panel | solid body | 1 | PASS |
| osa-dryer-assembly | rear-upper-panel | volume (mm3) | OCP 764957.703 / Fusion 764957.703 | PASS |
| osa-dryer-assembly | rear-upper-panel | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | rear-upper-panel | solid body | 1 | PASS |
| osa-dryer-assembly | rear-lower-panel | volume (mm3) | OCP 238937.895 / Fusion 238937.895 | PASS |
| osa-dryer-assembly | rear-lower-panel | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | rear-lower-panel | solid body | 1 | PASS |
| osa-dryer-assembly | top-panel | volume (mm3) | OCP 774637.955 / Fusion 774637.955 | PASS |
| osa-dryer-assembly | top-panel | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | top-panel | solid body | 1 | PASS |
| osa-dryer-assembly | console-face | volume (mm3) | OCP 105612.310 / Fusion 105612.310 | PASS |
| osa-dryer-assembly | console-face | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | console-face | solid body | 1 | PASS |
| osa-dryer-assembly | console-rear | volume (mm3) | OCP 208107.949 / Fusion 208107.949 | PASS |
| osa-dryer-assembly | console-rear | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | console-rear | solid body | 1 | PASS |
| osa-dryer-assembly | console-cap | volume (mm3) | OCP 146545.150 / Fusion 146545.150 | PASS |
| osa-dryer-assembly | console-cap | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | console-cap | solid body | 1 | PASS |
| osa-dryer-assembly | console-cheek-left | volume (mm3) | OCP 42473.148 / Fusion 42473.148 | PASS |
| osa-dryer-assembly | console-cheek-left | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | console-cheek-left | solid body | 1 | PASS |
| osa-dryer-assembly | console-cheek-right | volume (mm3) | OCP 42473.148 / Fusion 42473.148 | PASS |
| osa-dryer-assembly | console-cheek-right | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | console-cheek-right | solid body | 1 | PASS |
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
| osa-dryer-assembly | heat-module-terminal-plate | volume (mm3) | OCP 43369.129 / Fusion 43369.129 | PASS |
| osa-dryer-assembly | heat-module-terminal-plate | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | heat-module-terminal-plate | solid body | 1 | PASS |
| osa-dryer-assembly | power-module-plate | volume (mm3) | OCP 161321.526 / Fusion 161321.526 | PASS |
| osa-dryer-assembly | power-module-plate | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | power-module-plate | solid body | 1 | PASS |
| osa-dryer-assembly | power-module-barrier | volume (mm3) | OCP 16928.199 / Fusion 16928.199 | PASS |
| osa-dryer-assembly | power-module-barrier | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | power-module-barrier | solid body | 1 | PASS |
| osa-dryer-assembly | power-module-cover | volume (mm3) | OCP 74108.220 / Fusion 74108.220 | PASS |
| osa-dryer-assembly | power-module-cover | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | power-module-cover | solid body | 1 | PASS |
| osa-dryer-assembly | lint-box-back | volume (mm3) | OCP 80050.373 / Fusion 80050.373 | PASS |
| osa-dryer-assembly | lint-box-back | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | lint-box-back | solid body | 1 | PASS |
| osa-dryer-assembly | hood-bottom | volume (mm3) | OCP 115600.636 / Fusion 115600.636 | PASS |
| osa-dryer-assembly | hood-bottom | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hood-bottom | solid body | 1 | PASS |
| osa-dryer-assembly | hood-top | volume (mm3) | OCP 116507.155 / Fusion 116507.155 | PASS |
| osa-dryer-assembly | hood-top | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hood-top | solid body | 1 | PASS |
| osa-dryer-assembly | trunk-front | volume (mm3) | OCP 177913.947 / Fusion 177913.947 | PASS |
| osa-dryer-assembly | trunk-front | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | trunk-front | solid body | 1 | PASS |
| osa-dryer-assembly | trunk-rear | volume (mm3) | OCP 223308.512 / Fusion 223308.512 | PASS |
| osa-dryer-assembly | trunk-rear | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | trunk-rear | solid body | 1 | PASS |
| osa-dryer-assembly | blower-plate | volume (mm3) | OCP 70112.794 / Fusion 70112.794 | PASS |
| osa-dryer-assembly | blower-plate | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | blower-plate | solid body | 1 | PASS |
| osa-dryer-assembly | entry-blank | volume (mm3) | OCP 3865.933 / Fusion 3865.933 | PASS |
| osa-dryer-assembly | entry-blank | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | entry-blank | solid body | 1 | PASS |
| osa-dryer-assembly | lint-box-front | volume (mm3) | OCP 175620.605 / Fusion 175620.605 | PASS |
| osa-dryer-assembly | lint-box-front | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | lint-box-front | solid body | 1 | PASS |
| osa-dryer-assembly | drum-sheet | volume (mm3) | OCP 873714.067 / Fusion 873710.647 | PASS |
| osa-dryer-assembly | drum-sheet | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | drum-sheet | solid body | 1 | PASS |
| osa-dryer-assembly | drum-ring-front | volume (mm3) | OCP 141703.202 / Fusion 141703.202 | PASS |
| osa-dryer-assembly | drum-ring-front | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | drum-ring-front | solid body | 1 | PASS |
| osa-dryer-assembly | drum-ring-rear | volume (mm3) | OCP 141703.202 / Fusion 141703.202 | PASS |
| osa-dryer-assembly | drum-ring-rear | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | drum-ring-rear | solid body | 1 | PASS |
| osa-dryer-assembly | drum-splice | volume (mm3) | OCP 32383.401 / Fusion 32382.005 | PASS |
| osa-dryer-assembly | drum-splice | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | drum-splice | solid body | 1 | PASS |
| osa-dryer-assembly | baffle-1 (angle, cut to length) | volume (mm3) | OCP 110481.803 / Fusion 110481.803 | PASS |
| osa-dryer-assembly | baffle-1 (angle, cut to length) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | baffle-1 (angle, cut to length) | solid body | 1 | PASS |
| osa-dryer-assembly | baffle-2 (angle, cut to length) | volume (mm3) | OCP 110481.803 / Fusion 110481.803 | PASS |
| osa-dryer-assembly | baffle-2 (angle, cut to length) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | baffle-2 (angle, cut to length) | solid body | 1 | PASS |
| osa-dryer-assembly | baffle-3 (angle, cut to length) | volume (mm3) | OCP 110481.803 / Fusion 110481.803 | PASS |
| osa-dryer-assembly | baffle-3 (angle, cut to length) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | baffle-3 (angle, cut to length) | solid body | 1 | PASS |
| osa-dryer-assembly | roller-front-1 (bought) | volume (mm3) | OCP 68521.081 / Fusion 68521.081 | PASS |
| osa-dryer-assembly | roller-front-1 (bought) | bounding box (mm) | max deviation 0.0001 | PASS |
| osa-dryer-assembly | roller-front-1 (bought) | solid body | 1 | PASS |
| osa-dryer-assembly | roller-rear-1 (bought) | volume (mm3) | OCP 68521.081 / Fusion 68521.081 | PASS |
| osa-dryer-assembly | roller-rear-1 (bought) | bounding box (mm) | max deviation 0.0001 | PASS |
| osa-dryer-assembly | roller-rear-1 (bought) | solid body | 1 | PASS |
| osa-dryer-assembly | roller-front-2 (bought) | volume (mm3) | OCP 68521.081 / Fusion 68521.081 | PASS |
| osa-dryer-assembly | roller-front-2 (bought) | bounding box (mm) | max deviation 0.0001 | PASS |
| osa-dryer-assembly | roller-front-2 (bought) | solid body | 1 | PASS |
| osa-dryer-assembly | roller-rear-2 (bought) | volume (mm3) | OCP 68521.081 / Fusion 68521.081 | PASS |
| osa-dryer-assembly | roller-rear-2 (bought) | bounding box (mm) | max deviation 0.0001 | PASS |
| osa-dryer-assembly | roller-rear-2 (bought) | solid body | 1 | PASS |
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
| osa-dryer-assembly | liner | volume (mm3) | OCP 91807.599 / Fusion 91807.420 | PASS |
| osa-dryer-assembly | liner | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | liner | solid body | 1 | PASS |
| osa-dryer-assembly | liner-splice | volume (mm3) | OCP 2270.762 / Fusion 2270.587 | PASS |
| osa-dryer-assembly | liner-splice | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | liner-splice | solid body | 1 | PASS |
| osa-dryer-assembly | lint-box-bars (30 x 8 aluminium flat bar: 2 sides mitred at the top, 1 bottom) | volume (mm3) (3 bodies added) | OCP 261325.657 / Fusion 261325.657 | PASS |
| osa-dryer-assembly | lint-box-bars (30 x 8 aluminium flat bar: 2 sides mitred at the top, 1 bottom) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | lint-box-bars (30 x 8 aluminium flat bar: 2 sides mitred at the top, 1 bottom) | solid body | 1 | PASS |
| osa-dryer-assembly | lint-box-foam (bought, 3 mm closed-cell foam tape 8 wide, 2 x 190, compressed to 1.5) | volume (mm3) (2 bodies added) | OCP 4255.258 / Fusion 4255.258 | PASS |
| osa-dryer-assembly | lint-box-foam (bought, 3 mm closed-cell foam tape 8 wide, 2 x 190, compressed to 1.5) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | lint-box-foam (bought, 3 mm closed-cell foam tape 8 wide, 2 x 190, compressed to 1.5) | solid body | 1 | PASS |
| osa-dryer-assembly | spool-bars (40 x 8 aluminium flat bar: 2 x 136, 2 x 140) | volume (mm3) (4 bodies added) | OCP 175718.681 / Fusion 175718.681 | PASS |
| osa-dryer-assembly | spool-bars (40 x 8 aluminium flat bar: 2 x 136, 2 x 140) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | spool-bars (40 x 8 aluminium flat bar: 2 x 136, 2 x 140) | solid body | 1 | PASS |
| osa-dryer-assembly | spool-foam (bought, 6 mm closed-cell foam tape 8 wide, 600, compressed to 4 on the blower plate) | volume (mm3) (4 bodies added) | OCP 17664.000 / Fusion 17664.000 | PASS |
| osa-dryer-assembly | spool-foam (bought, 6 mm closed-cell foam tape 8 wide, 600, compressed to 4 on the blower plate) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | spool-foam (bought, 6 mm closed-cell foam tape 8 wide, 600, compressed to 4 on the blower plate) | solid body | 1 | PASS |
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
| osa-dryer-assembly | basket-pull (bought, D-pull, 64 mm centres, 25 projection) | volume (mm3) | OCP 8057.275 / Fusion 8057.203 | PASS |
| osa-dryer-assembly | basket-pull (bought, D-pull, 64 mm centres, 25 projection) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | basket-pull (bought, D-pull, 64 mm centres, 25 projection) | solid body | 1 | PASS |
| osa-dryer-assembly | hood-bars (25 x 8 aluminium flat bar: 2 sides, front, rear) | volume (mm3) (4 bodies added) | OCP 234798.925 / Fusion 234798.925 | PASS |
| osa-dryer-assembly | hood-bars (25 x 8 aluminium flat bar: 2 sides, front, rear) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hood-bars (25 x 8 aluminium flat bar: 2 sides, front, rear) | solid body | 1 | PASS |
| osa-dryer-assembly | hood-gasket (bought, 3 mm foam ring 150 x 125, glued under the hood's bottom plate) | volume (mm3) | OCP 16198.837 / Fusion 16198.837 | PASS |
| osa-dryer-assembly | hood-gasket (bought, 3 mm foam ring 150 x 125, glued under the hood's bottom plate) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hood-gasket (bought, 3 mm foam ring 150 x 125, glued under the hood's bottom plate) | solid body | 1 | PASS |
| osa-dryer-assembly | trunk-bars (50 x 8 aluminium flat bar: 2 sides, 1 top) | volume (mm3) (3 bodies added) | OCP 553698.387 / Fusion 553698.388 | PASS |
| osa-dryer-assembly | trunk-bars (50 x 8 aluminium flat bar: 2 sides, 1 top) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | trunk-bars (50 x 8 aluminium flat bar: 2 sides, 1 top) | solid body | 1 | PASS |
| osa-dryer-assembly | nozzle-bars (40 x 8 aluminium flat bar: 2 sides, top, bottom) | volume (mm3) (4 bodies added) | OCP 234860.381 / Fusion 234860.381 | PASS |
| osa-dryer-assembly | nozzle-bars (40 x 8 aluminium flat bar: 2 sides, top, bottom) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | nozzle-bars (40 x 8 aluminium flat bar: 2 sides, top, bottom) | solid body | 1 | PASS |
| osa-dryer-assembly | nozzle-foam (bought, 2 mm closed-cell foam tape 8 wide, 900, compressed to 1 on the bulkhead) | volume (mm3) (4 bodies added) | OCP 5760.957 / Fusion 5760.957 | PASS |
| osa-dryer-assembly | nozzle-foam (bought, 2 mm closed-cell foam tape 8 wide, 900, compressed to 1 on the bulkhead) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | nozzle-foam (bought, 2 mm closed-cell foam tape 8 wide, 900, compressed to 1 on the bulkhead) | solid body | 1 | PASS |
| osa-dryer-assembly | blower-plate-feet (angle 20x20x2, 2 x 90) | volume (mm3) (2 bodies added) | OCP 13287.301 / Fusion 13287.301 | PASS |
| osa-dryer-assembly | blower-plate-feet (angle 20x20x2, 2 x 90) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | blower-plate-feet (angle 20x20x2, 2 x 90) | solid body | 1 | PASS |
| osa-dryer-assembly | exhaust-duct (bought, 4 in aluminium pipe, 102 x 1, cut to length, one 6.5 hole for the tap) | volume (mm3) | OCP 193361.673 / Fusion 193361.629 | PASS |
| osa-dryer-assembly | exhaust-duct (bought, 4 in aluminium pipe, 102 x 1, cut to length, one 6.5 hole for the tap) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | exhaust-duct (bought, 4 in aluminium pipe, 102 x 1, cut to length, one 6.5 hole for the tap) | solid body | 1 | PASS |
| osa-dryer-assembly | exhaust-clamps (bought, 2 x worm-drive hose clamps for 102, envelopes) | volume (mm3) (4 bodies added) | OCP 10700.378 / Fusion 10700.378 | PASS |
| osa-dryer-assembly | exhaust-clamps (bought, 2 x worm-drive hose clamps for 102, envelopes) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | exhaust-clamps (bought, 2 x worm-drive hose clamps for 102, envelopes) | solid body | 1 | PASS |
| osa-dryer-assembly | exhaust-tap-barb (bought, 1/8 NPT or M6 brass barb fitting with a locknut, 5 mm barb, envelope) | volume (mm3) | OCP 1215.319 / Fusion 1215.319 | PASS |
| osa-dryer-assembly | exhaust-tap-barb (bought, 1/8 NPT or M6 brass barb fitting with a locknut, 5 mm barb, envelope) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | exhaust-tap-barb (bought, 1/8 NPT or M6 brass barb fitting with a locknut, 5 mm barb, envelope) | solid body | 1 | PASS |
| osa-dryer-assembly | ps1-tube (bought, 6 mm silicone tube from the tap to PS1, drawn on its route) | volume (mm3) | OCP 11463.040 / Fusion 11463.040 | PASS |
| osa-dryer-assembly | ps1-tube (bought, 6 mm silicone tube from the tap to PS1, drawn on its route) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | ps1-tube (bought, 6 mm silicone tube from the tap to PS1, drawn on its route) | solid body | 1 | PASS |
| osa-dryer-assembly | motor (bought) | volume (mm3) | OCP 3046373.714 / Fusion 3046373.714 | PASS |
| osa-dryer-assembly | motor (bought) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | motor (bought) | solid body | 1 | PASS |
| osa-dryer-assembly | motor-mount-1 (bought, cradle bracket) | volume (mm3) | OCP 39966.897 / Fusion 39966.897 | PASS |
| osa-dryer-assembly | motor-mount-1 (bought, cradle bracket) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | motor-mount-1 (bought, cradle bracket) | solid body | 1 | PASS |
| osa-dryer-assembly | motor-mount-2 (bought, cradle bracket) | volume (mm3) | OCP 39966.897 / Fusion 39966.897 | PASS |
| osa-dryer-assembly | motor-mount-2 (bought, cradle bracket) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | motor-mount-2 (bought, cradle bracket) | solid body | 1 | PASS |
| osa-dryer-assembly | pulley (bought) | volume (mm3) | OCP 6967.148 / Fusion 6967.148 | PASS |
| osa-dryer-assembly | pulley (bought) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | pulley (bought) | solid body | 1 | PASS |
| osa-dryer-assembly | blower (bought) | volume (mm3) | OCP 5340928.083 / Fusion 5340928.083 | PASS |
| osa-dryer-assembly | blower (bought) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | blower (bought) | solid body | 1 | PASS |
| osa-dryer-assembly | belt (bought, PJ 5 rib) | volume (mm3) | OCP 93324.744 / Fusion 93324.744 | PASS |
| osa-dryer-assembly | belt (bought, PJ 5 rib) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | belt (bought, PJ 5 rib) | solid body | 1 | PASS |
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
| osa-dryer-assembly | power-module-din-rails (bought, 5 x 35 x 7.5 top hat, 140) | volume (mm3) (5 bodies added) | OCP 33288.275 / Fusion 33288.276 | PASS |
| osa-dryer-assembly | power-module-din-rails (bought, 5 x 35 x 7.5 top hat, 140) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | power-module-din-rails (bought, 5 x 35 x 7.5 top hat, 140) | solid body | 1 | PASS |
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
| osa-dryer-assembly | power-module-barrier-angle (20x20x2 aluminium angle, 150) | volume (mm3) | OCP 11272.765 / Fusion 11272.765 | PASS |
| osa-dryer-assembly | power-module-barrier-angle (20x20x2 aluminium angle, 150) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | power-module-barrier-angle (20x20x2 aluminium angle, 150) | solid body | 1 | PASS |
| osa-dryer-assembly | power-module-standoffs (bought, 4 x M4 x 75 hex standoffs, female both ends) | volume (mm3) (4 bodies added) | OCP 11733.055 / Fusion 11733.055 | PASS |
| osa-dryer-assembly | power-module-standoffs (bought, 4 x M4 x 75 hex standoffs, female both ends) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | power-module-standoffs (bought, 4 x M4 x 75 hex standoffs, female both ends) | solid body | 1 | PASS |
| osa-dryer-assembly | power-module-ground-stud (bought, M6 x 16 hex bolt, 2 nuts, star washers; the cord's PE ring terminal goes between the nuts) | volume (mm3) (3 bodies added) | OCP 1535.662 / Fusion 1535.662 | PASS |
| osa-dryer-assembly | power-module-ground-stud (bought, M6 x 16 hex bolt, 2 nuts, star washers; the cord's PE ring terminal goes between the nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | power-module-ground-stud (bought, M6 x 16 hex bolt, 2 nuts, star washers; the cord's PE ring terminal goes between the nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | grommets (bought, 5 x rubber grommets for 1.5 panels: 22 mm hole x 2, 30 mm hole x 1, 16 mm hole x 2) | volume (mm3) (5 bodies added) | OCP 6693.713 / Fusion 6693.713 | PASS |
| osa-dryer-assembly | grommets (bought, 5 x rubber grommets for 1.5 panels: 22 mm hole x 2, 30 mm hole x 1, 16 mm hole x 2) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | grommets (bought, 5 x rubber grommets for 1.5 panels: 22 mm hole x 2, 30 mm hole x 1, 16 mm hole x 2) | solid body | 1 | PASS |
| osa-dryer-assembly | cord-bushing (bought, PG16 strain relief) | volume (mm3) | OCP 8877.396 / Fusion 8877.396 | PASS |
| osa-dryer-assembly | cord-bushing (bought, PG16 strain relief) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | cord-bushing (bought, PG16 strain relief) | solid body | 1 | PASS |
| osa-dryer-assembly | power-cord (bought) | volume (mm3) | OCP 29365.096 / Fusion 29365.096 | PASS |
| osa-dryer-assembly | power-cord (bought) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | power-cord (bought) | solid body | 1 | PASS |
| osa-dryer-assembly | ps1-bracket (angle 20x20x2, 60) | volume (mm3) | OCP 4363.650 / Fusion 4363.650 | PASS |
| osa-dryer-assembly | ps1-bracket (angle 20x20x2, 60) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | ps1-bracket (angle 20x20x2, 60) | solid body | 1 | PASS |
| osa-dryer-assembly | ps1-air-proving-switch (bought, envelope) | volume (mm3) | OCP 100578.329 / Fusion 100578.329 | PASS |
| osa-dryer-assembly | ps1-air-proving-switch (bought, envelope) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | ps1-air-proving-switch (bought, envelope) | solid body | 1 | PASS |
| osa-dryer-assembly | exhaust-thermostats (bought, TF2 thermal fuse, T_HI and T_LO cycling thermostats, envelopes on the blower outlet) | volume (mm3) (3 bodies added) | OCP 23221.148 / Fusion 23221.148 | PASS |
| osa-dryer-assembly | exhaust-thermostats (bought, TF2 thermal fuse, T_HI and T_LO cycling thermostats, envelopes on the blower outlet) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | exhaust-thermostats (bought, TF2 thermal fuse, T_HI and T_LO cycling thermostats, envelopes on the blower outlet) | solid body | 1 | PASS |
| osa-dryer-assembly | th1-exhaust-thermistor (bought, 10 k NTC appliance thermistor, envelope) | volume (mm3) | OCP 17281.340 / Fusion 17281.340 | PASS |
| osa-dryer-assembly | th1-exhaust-thermistor (bought, 10 k NTC appliance thermistor, envelope) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | th1-exhaust-thermistor (bought, 10 k NTC appliance thermistor, envelope) | solid body | 1 | PASS |
| osa-dryer-assembly | moisture-bars (bought, dryer moisture sensor bar set, two stainless strips on an insulating base, envelope) | volume (mm3) | OCP 20769.531 / Fusion 20769.531 | PASS |
| osa-dryer-assembly | moisture-bars (bought, dryer moisture sensor bar set, two stainless strips on an insulating base, envelope) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | moisture-bars (bought, dryer moisture sensor bar set, two stainless strips on an insulating base, envelope) | solid body | 1 | PASS |
| osa-dryer-assembly | entry-blank-2 (the second entry-blank, cut two to drawings/entry-blank.dxf; on the condensate drain) | volume (mm3) | OCP 3865.933 / Fusion 3865.933 | PASS |
| osa-dryer-assembly | entry-blank-2 (the second entry-blank, cut two to drawings/entry-blank.dxf; on the condensate drain) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | entry-blank-2 (the second entry-blank, cut two to drawings/entry-blank.dxf; on the condensate drain) | solid body | 1 | PASS |
| osa-dryer-assembly | cable-clamps (bought, 4 x nylon P-clip for a 12 mm bundle, envelopes) | volume (mm3) (8 bodies added) | OCP 3409.264 / Fusion 3409.264 | PASS |
| osa-dryer-assembly | cable-clamps (bought, 4 x nylon P-clip for a 12 mm bundle, envelopes) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | cable-clamps (bought, 4 x nylon P-clip for a 12 mm bundle, envelopes) | solid body | 1 | PASS |
| osa-dryer-assembly | feet (bought, 4 x M8 leveling feet, 50 pad) | volume (mm3) (4 bodies added) | OCP 93105.692 / Fusion 93105.692 | PASS |
| osa-dryer-assembly | feet (bought, 4 x M8 leveling feet, 50 pad) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | feet (bought, 4 x M8 leveling feet, 50 pad) | solid body | 1 | PASS |
| osa-dryer-assembly | tray-rail-brackets (bought, 4 x 2020 inside corner brackets) | volume (mm3) (4 bodies added) | OCP 6056.914 / Fusion 6056.914 | PASS |
| osa-dryer-assembly | tray-rail-brackets (bought, 4 x 2020 inside corner brackets) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | tray-rail-brackets (bought, 4 x 2020 inside corner brackets) | solid body | 1 | PASS |
| osa-dryer-assembly | console-brackets (bought, 12 x 4040 inside corner brackets) | volume (mm3) (12 bodies added) | OCP 104526.425 / Fusion 104526.425 | PASS |
| osa-dryer-assembly | console-brackets (bought, 12 x 4040 inside corner brackets) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | console-brackets (bought, 12 x 4040 inside corner brackets) | solid body | 1 | PASS |
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
| osa-dryer-assembly | hardware-roller-studs (bought, 4 x ISO 7379 shoulder screws 10 x 35 M8, 1.0 shims, spacers 16 x 10.5 x 8.5, M8 washers and nuts) | volume (mm3) (20 bodies added) | OCP 26570.921 / Fusion 26570.920 | PASS |
| osa-dryer-assembly | hardware-roller-studs (bought, 4 x ISO 7379 shoulder screws 10 x 35 M8, 1.0 shims, spacers 16 x 10.5 x 8.5, M8 washers and nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-roller-studs (bought, 4 x ISO 7379 shoulder screws 10 x 35 M8, 1.0 shims, spacers 16 x 10.5 x 8.5, M8 washers and nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | door-ring | volume (mm3) | OCP 145112.128 / Fusion 145112.128 | PASS |
| osa-dryer-assembly | door-ring | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | door-ring | solid body | 1 | PASS |
| osa-dryer-assembly | door-disc | volume (mm3) | OCP 457916.974 / Fusion 457916.974 | PASS |
| osa-dryer-assembly | door-disc | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | door-disc | solid body | 1 | PASS |
| osa-dryer-assembly | door-hinge-1-fixed (bought, flag hinge, pinned half) | volume (mm3) | OCP 17840.613 / Fusion 17840.613 | PASS |
| osa-dryer-assembly | door-hinge-1-fixed (bought, flag hinge, pinned half) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | door-hinge-1-fixed (bought, flag hinge, pinned half) | solid body | 1 | PASS |
| osa-dryer-assembly | door-hinge-2-swing (bought, flag hinge, lift-off half) | volume (mm3) | OCP 10700.959 / Fusion 10700.959 | PASS |
| osa-dryer-assembly | door-hinge-2-swing (bought, flag hinge, lift-off half) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | door-hinge-2-swing (bought, flag hinge, lift-off half) | solid body | 1 | PASS |
| osa-dryer-assembly | door-handle (bought, D handle 128 centres) | volume (mm3) | OCP 30386.464 / Fusion 30386.463 | PASS |
| osa-dryer-assembly | door-handle (bought, D handle 128 centres) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | door-handle (bought, D handle 128 centres) | solid body | 1 | PASS |
| osa-dryer-assembly | door-seal (bought, OEM door seal) | volume (mm3) | OCP 81939.020 / Fusion 81939.020 | PASS |
| osa-dryer-assembly | door-seal (bought, OEM door seal) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | door-seal (bought, OEM door seal) | solid body | 1 | PASS |
| osa-dryer-assembly | door-catch (bought, magnetic catch) | volume (mm3) | OCP 936.000 / Fusion 936.000 | PASS |
| osa-dryer-assembly | door-catch (bought, magnetic catch) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | door-catch (bought, magnetic catch) | solid body | 1 | PASS |
| osa-dryer-assembly | door-catch-strike (bought) | volume (mm3) | OCP 144.000 / Fusion 144.000 | PASS |
| osa-dryer-assembly | door-catch-strike (bought) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | door-catch-strike (bought) | solid body | 1 | PASS |
| osa-dryer-assembly | door-switch (bought, two-contact plunger switch, envelope) | volume (mm3) | OCP 34081.250 / Fusion 34081.249 | PASS |
| osa-dryer-assembly | door-switch (bought, two-contact plunger switch, envelope) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | door-switch (bought, two-contact plunger switch, envelope) | solid body | 1 | PASS |
| osa-dryer-assembly | tier0-faceplate | volume (mm3) (allowed 0.05 percent: the labels are engraved with Fusion's own font) | OCP 195756.562 / Fusion 195720.130 | PASS |
| osa-dryer-assembly | tier0-faceplate | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | tier0-faceplate | solid body | 1 | PASS |
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
| osa-dryer-assembly | hardware-front-bulkhead (bought, 7 x M6 x 12 hex, washers, T-nuts) | volume (mm3) (7 bodies added) | OCP 6009.126 / Fusion 6009.126 | PASS |
| osa-dryer-assembly | hardware-front-bulkhead (bought, 7 x M6 x 12 hex, washers, T-nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-front-bulkhead (bought, 7 x M6 x 12 hex, washers, T-nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-rear-bulkhead (bought, 10 x M6 x 12 hex, washers, T-nuts) | volume (mm3) (10 bodies added) | OCP 8584.466 / Fusion 8584.466 | PASS |
| osa-dryer-assembly | hardware-rear-bulkhead (bought, 10 x M6 x 12 hex, washers, T-nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-rear-bulkhead (bought, 10 x M6 x 12 hex, washers, T-nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-bay-ceiling (bought, 20 x M6 x 12 hex, washers, T-nuts) | volume (mm3) (20 bodies added) | OCP 17168.933 / Fusion 17168.932 | PASS |
| osa-dryer-assembly | hardware-bay-ceiling (bought, 20 x M6 x 12 hex, washers, T-nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-bay-ceiling (bought, 20 x M6 x 12 hex, washers, T-nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-base-pan (bought, 20 x M6 x 12 hex, washers, T-nuts) | volume (mm3) (20 bodies added) | OCP 17168.933 / Fusion 17168.932 | PASS |
| osa-dryer-assembly | hardware-base-pan (bought, 20 x M6 x 12 hex, washers, T-nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-base-pan (bought, 20 x M6 x 12 hex, washers, T-nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-side-panel-left (bought, 29 x M6 x 12 hex, washers, T-nuts) | volume (mm3) (29 bodies added) | OCP 24894.953 / Fusion 24894.951 | PASS |
| osa-dryer-assembly | hardware-side-panel-left (bought, 29 x M6 x 12 hex, washers, T-nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-side-panel-left (bought, 29 x M6 x 12 hex, washers, T-nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-side-panel-right (bought, 29 x M6 x 12 hex, washers, T-nuts) | volume (mm3) (29 bodies added) | OCP 24894.953 / Fusion 24894.951 | PASS |
| osa-dryer-assembly | hardware-side-panel-right (bought, 29 x M6 x 12 hex, washers, T-nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-side-panel-right (bought, 29 x M6 x 12 hex, washers, T-nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-front-upper-panel (bought, 16 x M6 x 12 hex, washers, T-nuts) | volume (mm3) (16 bodies added) | OCP 13735.146 / Fusion 13735.146 | PASS |
| osa-dryer-assembly | hardware-front-upper-panel (bought, 16 x M6 x 12 hex, washers, T-nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-front-upper-panel (bought, 16 x M6 x 12 hex, washers, T-nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-front-lower-panel (bought, 8 x M6 x 12 hex, washers, T-nuts) | volume (mm3) (8 bodies added) | OCP 6867.573 / Fusion 6867.573 | PASS |
| osa-dryer-assembly | hardware-front-lower-panel (bought, 8 x M6 x 12 hex, washers, T-nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-front-lower-panel (bought, 8 x M6 x 12 hex, washers, T-nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-rear-upper-panel (bought, 18 x M6 x 12 hex, washers, T-nuts) | volume (mm3) (18 bodies added) | OCP 15452.040 / Fusion 15452.039 | PASS |
| osa-dryer-assembly | hardware-rear-upper-panel (bought, 18 x M6 x 12 hex, washers, T-nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-rear-upper-panel (bought, 18 x M6 x 12 hex, washers, T-nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-rear-lower-panel (bought, 8 x M6 x 12 hex, washers, T-nuts) | volume (mm3) (8 bodies added) | OCP 6867.573 / Fusion 6867.573 | PASS |
| osa-dryer-assembly | hardware-rear-lower-panel (bought, 8 x M6 x 12 hex, washers, T-nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-rear-lower-panel (bought, 8 x M6 x 12 hex, washers, T-nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-top-panel (bought, 16 x M6 x 12 hex, washers, T-nuts) | volume (mm3) (16 bodies added) | OCP 13735.146 / Fusion 13735.146 | PASS |
| osa-dryer-assembly | hardware-top-panel (bought, 16 x M6 x 12 hex, washers, T-nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-top-panel (bought, 16 x M6 x 12 hex, washers, T-nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-console-brackets (bought, 24 x M6 x 12 hex, washers, T-nuts) | volume (mm3) (24 bodies added) | OCP 20602.719 / Fusion 20602.718 | PASS |
| osa-dryer-assembly | hardware-console-brackets (bought, 24 x M6 x 12 hex, washers, T-nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-console-brackets (bought, 24 x M6 x 12 hex, washers, T-nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-console-face (bought, 8 x M6 x 12 hex, washers, T-nuts) | volume (mm3) (8 bodies added) | OCP 6867.573 / Fusion 6867.573 | PASS |
| osa-dryer-assembly | hardware-console-face (bought, 8 x M6 x 12 hex, washers, T-nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-console-face (bought, 8 x M6 x 12 hex, washers, T-nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-console-rear (bought, 8 x M6 x 12 hex, washers, T-nuts) | volume (mm3) (8 bodies added) | OCP 6867.573 / Fusion 6867.573 | PASS |
| osa-dryer-assembly | hardware-console-rear (bought, 8 x M6 x 12 hex, washers, T-nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-console-rear (bought, 8 x M6 x 12 hex, washers, T-nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-console-cap (bought, 10 x M6 x 12 hex, washers, T-nuts) | volume (mm3) (10 bodies added) | OCP 8584.466 / Fusion 8584.466 | PASS |
| osa-dryer-assembly | hardware-console-cap (bought, 10 x M6 x 12 hex, washers, T-nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-console-cap (bought, 10 x M6 x 12 hex, washers, T-nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-console-cheek-left (bought, 5 x M6 x 12 hex, washers, T-nuts) | volume (mm3) (5 bodies added) | OCP 4292.233 / Fusion 4292.233 | PASS |
| osa-dryer-assembly | hardware-console-cheek-left (bought, 5 x M6 x 12 hex, washers, T-nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-console-cheek-left (bought, 5 x M6 x 12 hex, washers, T-nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-console-cheek-right (bought, 5 x M6 x 12 hex, washers, T-nuts) | volume (mm3) (5 bodies added) | OCP 4292.233 / Fusion 4292.233 | PASS |
| osa-dryer-assembly | hardware-console-cheek-right (bought, 5 x M6 x 12 hex, washers, T-nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-console-cheek-right (bought, 5 x M6 x 12 hex, washers, T-nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-door-hinge-1 (bought, 2 x M6 x 16 countersunk, nuts) | volume (mm3) (4 bodies added) | OCP 1692.210 / Fusion 1692.210 | PASS |
| osa-dryer-assembly | hardware-door-hinge-1 (bought, 2 x M6 x 16 countersunk, nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-door-hinge-1 (bought, 2 x M6 x 16 countersunk, nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-motor-mounts (bought, 4 x M6 x 12 hex, washers, nuts, through the base pan) | volume (mm3) (8 bodies added) | OCP 4562.023 / Fusion 4562.023 | PASS |
| osa-dryer-assembly | hardware-motor-mounts (bought, 4 x M6 x 12 hex, washers, nuts, through the base pan) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-motor-mounts (bought, 4 x M6 x 12 hex, washers, nuts, through the base pan) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-power-module-plate (bought, 4 x M6 x 12 hex, washers, T-nuts) | volume (mm3) (4 bodies added) | OCP 3433.787 / Fusion 3433.786 | PASS |
| osa-dryer-assembly | hardware-power-module-plate (bought, 4 x M6 x 12 hex, washers, T-nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-power-module-plate (bought, 4 x M6 x 12 hex, washers, T-nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-idler-brackets (bought, 4 x M6 x 12 hex, nuts, through the base pan) | volume (mm3) (8 bodies added) | OCP 4562.023 / Fusion 4562.023 | PASS |
| osa-dryer-assembly | hardware-idler-brackets (bought, 4 x M6 x 12 hex, nuts, through the base pan) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-idler-brackets (bought, 4 x M6 x 12 hex, nuts, through the base pan) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-tray-rails (bought, 8 x M4 x 8 button head, T-nuts for the 6 and 8 mm slots) | volume (mm3) (8 bodies added) | OCP 1429.360 / Fusion 1429.359 | PASS |
| osa-dryer-assembly | hardware-tray-rails (bought, 8 x M4 x 8 button head, T-nuts for the 6 and 8 mm slots) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-tray-rails (bought, 8 x M4 x 8 button head, T-nuts for the 6 and 8 mm slots) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-drum-glides (bought, 4 x M4 x 8 and 4 x M4 x 10 button head, nuts) | volume (mm3) (16 bodies added) | OCP 2261.560 / Fusion 2261.559 | PASS |
| osa-dryer-assembly | hardware-drum-glides (bought, 4 x M4 x 8 and 4 x M4 x 10 button head, nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-drum-glides (bought, 4 x M4 x 8 and 4 x M4 x 10 button head, nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-tier0-faceplate (bought, 6 x M4 x 10 button head, nuts) | volume (mm3) (12 bodies added) | OCP 1771.568 / Fusion 1771.568 | PASS |
| osa-dryer-assembly | hardware-tier0-faceplate (bought, 6 x M4 x 10 button head, nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-tier0-faceplate (bought, 6 x M4 x 10 button head, nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-door-ring (bought, 8 x M4 x 8 button head, nuts) | volume (mm3) (16 bodies added) | OCP 2161.029 / Fusion 2161.028 | PASS |
| osa-dryer-assembly | hardware-door-ring (bought, 8 x M4 x 8 button head, nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-door-ring (bought, 8 x M4 x 8 button head, nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-door-hinge-2 (bought, 2 x M4 x 8 button head into the tapped leaf) | volume (mm3) (2 bodies added) | OCP 357.340 / Fusion 357.340 | PASS |
| osa-dryer-assembly | hardware-door-hinge-2 (bought, 2 x M4 x 8 button head into the tapped leaf) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-door-hinge-2 (bought, 2 x M4 x 8 button head into the tapped leaf) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-door-handle (bought, 2 x M4 x 10 button head into the handle) | volume (mm3) (2 bodies added) | OCP 407.605 / Fusion 407.605 | PASS |
| osa-dryer-assembly | hardware-door-handle (bought, 2 x M4 x 10 button head into the handle) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-door-handle (bought, 2 x M4 x 10 button head into the handle) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-drum-tabs (bought, 60 x M4 x 8 button head, nuts) | volume (mm3) (120 bodies added) | OCP 16207.714 / Fusion 16207.710 | PASS |
| osa-dryer-assembly | hardware-drum-tabs (bought, 60 x M4 x 8 button head, nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-drum-tabs (bought, 60 x M4 x 8 button head, nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-drum-seam (bought, 16 x M4 x 8 button head, nuts) | volume (mm3) (32 bodies added) | OCP 4322.057 / Fusion 4322.056 | PASS |
| osa-dryer-assembly | hardware-drum-seam (bought, 16 x M4 x 8 button head, nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-drum-seam (bought, 16 x M4 x 8 button head, nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-drum-baffles (bought, 12 x M6 x 12 button head, nuts) | volume (mm3) (24 bodies added) | OCP 10142.813 / Fusion 10142.807 | PASS |
| osa-dryer-assembly | hardware-drum-baffles (bought, 12 x M6 x 12 button head, nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-drum-baffles (bought, 12 x M6 x 12 button head, nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | heat-module-hardware (bought, 64 x M4 x 8 button head, 60 nuts, 4 T-nuts for the 6 mm slot) | volume (mm3) (124 bodies added) | OCP 16922.394 / Fusion 16922.390 | PASS |
| osa-dryer-assembly | heat-module-hardware (bought, 64 x M4 x 8 button head, 60 nuts, 4 T-nuts for the 6 mm slot) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | heat-module-hardware (bought, 64 x M4 x 8 button head, 60 nuts, 4 T-nuts for the 6 mm slot) | solid body | 1 | PASS |
| osa-dryer-assembly | power-module-hardware (bought, 22 x M4 x 8 button head, 14 nuts) | volume (mm3) (36 bodies added) | OCP 5211.159 / Fusion 5211.158 | PASS |
| osa-dryer-assembly | power-module-hardware (bought, 22 x M4 x 8 button head, 14 nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | power-module-hardware (bought, 22 x M4 x 8 button head, 14 nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-liner (bought, 2 x M3 x 6 button head, nuts) | volume (mm3) (4 bodies added) | OCP 234.826 / Fusion 234.826 | PASS |
| osa-dryer-assembly | hardware-liner (bought, 2 x M3 x 6 button head, nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-liner (bought, 2 x M3 x 6 button head, nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | lint-box-hardware (bought, 40 pieces: M4 x 8, M4 x 10 and M4 x 40 button heads, 2 x M6 x 20 button heads with 4 mm spacers and T-nuts) | volume (mm3) (40 bodies added) | OCP 11200.987 / Fusion 11200.986 | PASS |
| osa-dryer-assembly | lint-box-hardware (bought, 40 pieces: M4 x 8, M4 x 10 and M4 x 40 button heads, 2 x M6 x 20 button heads with 4 mm spacers and T-nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | lint-box-hardware (bought, 40 pieces: M4 x 8, M4 x 10 and M4 x 40 button heads, 2 x M6 x 20 button heads with 4 mm spacers and T-nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-basket (bought, 12 x M3 x 5 button head into the tapped plates, 2 x M4 x 10 button head into the pull) | volume (mm3) (14 bodies added) | OCP 1208.883 / Fusion 1208.883 | PASS |
| osa-dryer-assembly | hardware-basket (bought, 12 x M3 x 5 button head into the tapped plates, 2 x M4 x 10 button head into the pull) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-basket (bought, 12 x M3 x 5 button head into the tapped plates, 2 x M4 x 10 button head into the pull) | solid body | 1 | PASS |
| osa-dryer-assembly | riser-hardware (bought, 70 x M4 x 8 and M4 x 10 button heads) | volume (mm3) (70 bodies added) | OCP 12758.223 / Fusion 12758.221 | PASS |
| osa-dryer-assembly | riser-hardware (bought, 70 x M4 x 8 and M4 x 10 button heads) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | riser-hardware (bought, 70 x M4 x 8 and M4 x 10 button heads) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-door-switch (bought, 2 x M4 x 8 button head into the switch's tapped ears) | volume (mm3) (2 bodies added) | OCP 357.340 / Fusion 357.340 | PASS |
| osa-dryer-assembly | hardware-door-switch (bought, 2 x M4 x 8 button head into the switch's tapped ears) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-door-switch (bought, 2 x M4 x 8 button head into the switch's tapped ears) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-ps1 (bought, 2 x M6 x 12 hex, nuts, through the base pan; 2 x M4 x 8 button head into the switch) | volume (mm3) (6 bodies added) | OCP 2638.352 / Fusion 2638.351 | PASS |
| osa-dryer-assembly | hardware-ps1 (bought, 2 x M6 x 12 hex, nuts, through the base pan; 2 x M4 x 8 button head into the switch) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-ps1 (bought, 2 x M6 x 12 hex, nuts, through the base pan; 2 x M4 x 8 button head into the switch) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-exhaust-thermostats (bought, 6 x M4 x 8 button head into the housing) | volume (mm3) (6 bodies added) | OCP 1072.020 / Fusion 1072.019 | PASS |
| osa-dryer-assembly | hardware-exhaust-thermostats (bought, 6 x M4 x 8 button head into the housing) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-exhaust-thermostats (bought, 6 x M4 x 8 button head into the housing) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-blower-plate (bought, 4 x M4 x 8 button head into the housing, 4 x M4 x 8 and nuts into the feet, 4 x M6 x 12 hex, washers, nuts through the base pan) | volume (mm3) (20 bodies added) | OCP 6357.217 / Fusion 6357.217 | PASS |
| osa-dryer-assembly | hardware-blower-plate (bought, 4 x M4 x 8 button head into the housing, 4 x M4 x 8 and nuts into the feet, 4 x M6 x 12 hex, washers, nuts through the base pan) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-blower-plate (bought, 4 x M4 x 8 button head into the housing, 4 x M4 x 8 and nuts into the feet, 4 x M6 x 12 hex, washers, nuts through the base pan) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-th1 (bought, 1 x M4 x 20 button head from inside the lint box, nut on the body) | volume (mm3) (2 bodies added) | OCP 420.925 / Fusion 420.925 | PASS |
| osa-dryer-assembly | hardware-th1 (bought, 1 x M4 x 20 button head from inside the lint box, nut on the body) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-th1 (bought, 1 x M4 x 20 button head from inside the lint box, nut on the body) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-moisture-bars (bought, 2 x M4 x 16 button head from the drum side, nuts in the front gap) | volume (mm3) (4 bodies added) | OCP 741.319 / Fusion 741.319 | PASS |
| osa-dryer-assembly | hardware-moisture-bars (bought, 2 x M4 x 16 button head from the drum side, nuts in the front gap) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-moisture-bars (bought, 2 x M4 x 16 button head from the drum side, nuts in the front gap) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-entry-blanks (bought, 4 x M4 x 8 button head, nuts) | volume (mm3) (8 bodies added) | OCP 1080.514 / Fusion 1080.514 | PASS |
| osa-dryer-assembly | hardware-entry-blanks (bought, 4 x M4 x 8 button head, nuts) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-entry-blanks (bought, 4 x M4 x 8 button head, nuts) | solid body | 1 | PASS |
| osa-dryer-assembly | hardware-cable-clamps (bought, 4 x M4 x 8 button head, nuts under the pan) | volume (mm3) (8 bodies added) | OCP 1080.514 / Fusion 1080.514 | PASS |
| osa-dryer-assembly | hardware-cable-clamps (bought, 4 x M4 x 8 button head, nuts under the pan) | bounding box (mm) | max deviation 0.0000 | PASS |
| osa-dryer-assembly | hardware-cable-clamps (bought, 4 x M4 x 8 button head, nuts under the pan) | solid body | 1 | PASS |
| osa-dryer-assembly |  | parts of the parametric build compared with the script's assembly | 213 of 213 named solids | PASS |

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
| power-cord (bought) | -279.50..-270.50 | 685.50..820.00 | -16.50..320.00 | 29365.1 |
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
| ps1-tube (bought, 6 mm silicone tube from the tap to PS1, drawn on its route) | 227.00..253.00 | 91.00..303.00 | 60.00..243.00 | 11463.0 |
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
