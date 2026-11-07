# Common power module: wiring

Draft 2, 2026-11-06 (draft 1 2026-11-05). Status: paper design. Nothing has been built or tested. This document and the two ladder drawings are the electrical design; no KiCad schematic is drawn (`DECISIONS.md` 2026-11-06). Draft 2 changes only where the parts sit: the module is a plate with five short DIN rails behind the rear bulkhead, reached with the rear upper panel off (`DECISIONS.md` 2026-11-06, `docs/design-rules.md` section 4); every designator, terminal number and wire is as in draft 1. K_MOTOR becomes a mini contactor (LC1K0910BD class) for depth.

The common power module is the plate behind the rear bulkhead, left of the riser duct, that every build gets, whatever makes the heat. It takes the cord in, makes the 24 V rail, runs the motor, holds the interlock chain, and ends at two terminal strips for the heat module and two connectors for the control module. The ladder drawings `ladder-common-power-module.svg` and `ladder-heat-modules.svg` are the picture of this document; regenerate them with `ladder.py` after any change here.

Every designator below appears on the ladder, in the BOM, and on the labels on the plate and the cover.

## 1. Parts by designator

| Designator | Part | Generic spec | Terminals used |
| --- | --- | --- | --- |
| X1 | Cord terminal group, mains | DIN screw or spring terminal blocks rated 600 V, 30 A, for 10 AWG; one green ground block | 1 L1, 2 L2, 3 N, 4 PE |
| X2 | Heat module terminal group, mains | Same blocks as X1 | 1 L1, 2 L2, 3 N, 4 PE |
| X3 | Motor and door switch group, mains | DIN terminal blocks rated 600 V, 20 A, for 14 AWG; one green ground block | 1 motor L, 2 motor N, 3 motor PE, 4 S1 feed, 5 S1 return |
| X4 | Heat module terminal group, SELV | DIN terminal blocks, 2.5 mm2, on the SELV rail | 1 HEAT_EN, 2 0V, 3 HEAT_ON_A, 4 HEAT_ON_B |
| X5 | Chassis switch group, SELV | DIN terminal blocks, 2.5 mm2 | 1 S2 feed (+24V), 2 S2 return (24V_ILK), 3 PS1 feed, 4 PS1 return, 5 TF2 feed, 6 TF2 return, 7 T_HI feed, 8 T_HI return, 9 T_LO feed, 10 T_LO return |
| X6 | Sensor pass-through, SELV | DIN terminal blocks, 2.5 mm2 | 1-2 TEMP_EXH, 3-4 MOIST, 5-6 SENS2 |
| CB1 | Supplementary circuit breaker | 1-pole, 10 A, C curve, DIN rail, UL 1077 recognized or IEC 60947-2 | line, load |
| F1 | Fuse, supply input | 5 x 20 mm, 2 A time-delay, 250 V, in a DIN fuse terminal | line, load |
| F2 | Fuse, control module rail | 2 A, DIN fuse terminal, or a resettable PTC of 2 A hold | line, load |
| PSU | Power supply | 24 V DC, 2.5 A or more, universal input 85 to 264 V AC, listed, DIN rail | L, N, PE in; +V, -V out |
| K_MOTOR | Motor contactor | IEC contactor, AC-3 9 A or more at 120 V, 24 V DC coil, listed | 1-2 (pole 1), A1-A2 (coil) |
| RLY_MOTOR | Interface relay, motor request | Slim interface relay, 24 V DC coil with suppression diode, 1 changeover contact, 6 A, DIN socket | A1-A2 coil, 11-14 n.o. |
| RLY_HEAT | Interface relay, heat request | Same | A1-A2 coil, 11-14 n.o. |
| RLY_HEAT_LO | Interface relay, low heat request | Same | A1-A2 coil, 11-12 n.c., 11-14 n.o. |
| PTC1, PTC2, PTC3 | Resettable fuses, status lines | PTC, 100 mA hold class, 30 V or more, in a DIN terminal with a fuse holder or on a small screw-terminal carrier | line, load |
| S1 | Door switch, contact 1 (mains) | Listed appliance dryer door switch, contact rated for the motor at 120 V including starting current | COM, NO |
| S2 | Door switch, contact 2 (SELV) | Listed snap-action or IEC limit switch, 24 V DC, 1 A or more, on the same door actuator as S1 | COM, NO |
| PS1 | Air-proving switch | Listed air pressure switch, normally open, closes on blower pressure; setpoint to be measured | COM, NO |
| TF2 | Exhaust thermal fuse | One-shot thermal cutoff on the blower housing, appliance market (for example the 3392519 family and its aftermarket equivalents) | 2 tabs |
| T_HI | Cycling thermostat, high | Bimetal disc thermostat, normally closed, appliance market, L-rating per heat module | 2 tabs |
| T_LO | Cycling thermostat, low | Same, lower L-rating | 2 tabs |
| J1 | Control connector | Mini-Fit Jr. 16-circuit receptacle housing with female crimp terminals, on a 250 mm flying lead | per `controls/uci-spec.md` 5.4 |
| J2 | Sensor connector | JST XH 8-position housing with female crimp terminals, on a 250 mm flying lead | per `controls/uci-spec.md` 5.5 |
| M1 | Motor (in the bay) | 120 V, 1/4 to 1/3 hp, 1725 rpm class, built-in thermal protector | L, N, PE |

Mounting (draft 2): five 140 mm DIN rails across a 150 x 720 laser-cut steel plate on the rear faces of the cabinet's two rear cross rails, devices facing the back. Rail A is three rails under a cover: A1 (360 from the floor) X1, CB1, F1; A2 (470) the PSU and K_MOTOR; A3 (580) X2, X3. The PSU's output leads cross the barrier through a grommeted notch. Rail B is two rails above the barrier: B1 (700) RLY_MOTOR, RLY_HEAT, RLY_HEAT_LO, PTC1 to PTC3, F2, X4; B2 (820) X5, X6. The barrier is a 20x20x2 aluminium angle on the plate at 640 carrying a 1.5 mm steel shelf out to the devices' depth; the cover is 1.5 mm steel on four M4 x 75 standoffs over A1 to A3. The rails, the barrier, the cover and the plate are bonded to the ground stud at the plate's top right with star washers on bare metal, and the plate to the frame through its four M6. The cord comes up through the bay ceiling's grommet to X1; the bay harness (X2, X3, X5's door and air switch lines) goes down through the second ceiling grommet; the J1 and J2 leads go up through the top panel's grommet into the console. Device sizes in the model are from datasheets and listings (V-112).

## 2. Terminal map

| Terminal | Signal | Side | Wire to |
| --- | --- | --- | --- |
| X1:1 | L1 | mains | cord black |
| X1:2 | L2 | mains | cord red (240 V cord only; empty on a 120 V cord) |
| X1:3 | N | mains | cord white |
| X1:4 | PE | mains | cord green; also the plate's ground stud |
| X2:1 | L1 to heat module | mains | heat module tray |
| X2:2 | L2 to heat module | mains | heat module tray (electric module only) |
| X2:3 | N to heat module | mains | heat module tray |
| X2:4 | PE to heat module | mains | heat module tray bonding lead |
| X3:1 | motor L (switched) | mains | M1 L |
| X3:2 | motor N | mains | M1 N |
| X3:3 | motor PE | mains | M1 frame |
| X3:4 | S1 feed | mains | S1 COM |
| X3:5 | S1 return | mains | S1 NO |
| X4:1 | HEAT_EN | SELV | heat module tray |
| X4:2 | 0V | SELV | heat module tray |
| X4:3 | HEAT_ON_A | SELV | heat module tray (contact) |
| X4:4 | HEAT_ON_B | SELV | heat module tray (contact) |
| X5:1 | S2 feed, +24V | SELV | S2 COM |
| X5:2 | S2 return, 24V_ILK | SELV | S2 NO |
| X5:3 | PS1 feed, 24V_ILK | SELV | PS1 COM |
| X5:4 | PS1 return | SELV | PS1 NO |
| X5:5 | TF2 feed | SELV | TF2 tab 1 |
| X5:6 | TF2 return | SELV | TF2 tab 2 |
| X5:7 | T_HI feed | SELV | T_HI tab 1 |
| X5:8 | T_HI return, to HEAT_EN | SELV | T_HI tab 2 |
| X5:9 | T_LO feed | SELV | T_LO tab 1 |
| X5:10 | T_LO return, to HEAT_EN | SELV | T_LO tab 2 |
| X6:1, X6:2 | TEMP_EXH pair | SELV | exhaust thermistor; J2 pins 1, 2 |
| X6:3, X6:4 | MOIST pair | SELV | moisture bars; J2 pins 3, 4 |
| X6:5, X6:6 | SENS2 pair | SELV | second thermistor if fitted; J2 pins 5, 6 |

## 3. Wire list

Colors follow the US convention on the mains side and NFPA 79 style on the DC side: blue for 24 V DC control, white with a blue stripe for 0V. The J1 harness uses its own colors so a person can read the connector without the drawing.

| No. | From | To | Gauge | Color | Note |
| --- | --- | --- | --- | --- | --- |
| 1 | cord L1 | X1:1 | 10 AWG (cord) | black | 240 V cord. A 120 V cord is 14 AWG. |
| 2 | cord L2 | X1:2 | 10 AWG (cord) | red | 240 V cord only |
| 3 | cord N | X1:3 | 10 AWG (cord) | white | |
| 4 | cord PE | X1:4 | 10 AWG (cord) | green | ring terminal on the plate's ground stud, then X1:4 |
| 5 | X1:1 | X2:1 | 10 AWG, 105 °C | black | carries element current on the electric build |
| 6 | X1:2 | X2:2 | 10 AWG, 105 °C | red | |
| 7 | X1:3 | X2:3 | 10 AWG, 105 °C | white | |
| 8 | X1:4 | X2:4 | 10 AWG, 105 °C | green | |
| 9 | X1:1 | CB1 line | 14 AWG, 105 °C | black | |
| 10 | CB1 load | X3:4 | 14 AWG | black | to S1 COM |
| 11 | X3:5 | K_MOTOR 1 | 14 AWG | black | from S1 NO |
| 12 | K_MOTOR 2 | X3:1 | 14 AWG | black | switched motor L |
| 13 | X1:3 | X3:2 | 14 AWG | white | motor N |
| 14 | X1:4 | X3:3 | 14 AWG | green | motor PE |
| 15 | CB1 load | F1 line | 18 AWG | black | |
| 16 | F1 load | PSU L | 18 AWG | black | |
| 17 | X1:3 | PSU N | 18 AWG | white | |
| 18 | X1:4 | PSU PE | 18 AWG | green | |
| 19 | PSU +V | +24V bus (rail B distribution block) | 18 AWG | blue | through the barrier slot |
| 20 | PSU -V | 0V bus (rail B distribution block) | 18 AWG | white/blue | through the barrier slot |
| 21 | 0V bus | plate ground stud | 18 AWG | green | the one bond between 0V and PE |
| 22 | +24V bus | X5:1 | 18 AWG | blue | S2 feed |
| 23 | X5:2 | 24V_ILK bus | 18 AWG | blue | S2 return; label the bus 24V_ILK |
| 24 | 24V_ILK bus | RLY_MOTOR 11 | 18 AWG | blue | |
| 25 | RLY_MOTOR 14 | K_MOTOR A1 | 18 AWG | blue | |
| 26 | K_MOTOR A2 | 0V bus | 18 AWG | white/blue | |
| 27 | 24V_ILK bus | X5:3 | 18 AWG | blue | PS1 feed |
| 28 | X5:4 | X5:5 | 18 AWG | blue | PS1 return to TF2 feed; also PTC2 line (wire 44) |
| 29 | X5:6 | RLY_HEAT_LO 11 | 18 AWG | blue | TF2 return to the changeover common |
| 30 | RLY_HEAT_LO 12 | RLY_HEAT 11 | 18 AWG | blue | n.c., high branch |
| 31 | RLY_HEAT 14 | X5:7 | 18 AWG | blue | to T_HI feed |
| 32 | X5:8 | X4:1 | 18 AWG | blue | T_HI return to HEAT_EN |
| 33 | RLY_HEAT_LO 14 | X5:9 | 18 AWG | blue | n.o., low branch, to T_LO feed |
| 34 | X5:10 | X4:1 | 18 AWG | blue | T_LO return to HEAT_EN (both branches land on X4:1) |
| 35 | 0V bus | X4:2 | 18 AWG | white/blue | |
| 36 | +24V bus | RLY_MOTOR A1 | 20 AWG | blue | coil, polarity per the relay's diode marking |
| 37 | RLY_MOTOR A2 | J1 pin 3 | 20 AWG | orange | REQ_MOTOR |
| 38 | +24V bus | RLY_HEAT A1 | 20 AWG | blue | |
| 39 | RLY_HEAT A2 | J1 pin 4 | 20 AWG | orange | REQ_HEAT |
| 40 | +24V bus | RLY_HEAT_LO A1 | 20 AWG | blue | |
| 41 | RLY_HEAT_LO A2 | J1 pin 5 | 20 AWG | orange | REQ_HEAT_LO |
| 42 | 24V_ILK bus | PTC1 line | 20 AWG | blue | |
| 43 | PTC1 load | J1 pin 11 | 20 AWG | yellow | STAT_DOOR |
| 44 | X5:4 | PTC2 line | 20 AWG | blue | downstream of PS1 |
| 45 | PTC2 load | J1 pin 12 | 20 AWG | yellow | STAT_AIRFLOW |
| 46 | +24V bus | X4:3 | 20 AWG | blue | HEAT_ON contact feed |
| 47 | X4:4 | PTC3 line | 20 AWG | blue | HEAT_ON contact return |
| 48 | PTC3 load | J1 pin 13 | 20 AWG | yellow | STAT_HEAT_ON |
| 49 | +24V bus | F2 line | 18 AWG | blue | |
| 50 | F2 load | J1 pins 1 and 2 | 18 AWG | blue | two wires, one per pin |
| 51 | 0V bus | J1 pins 9 and 10 | 18 AWG | white/blue | two wires, one per pin |
| 52 | X6:1, X6:2 | J2 pins 1, 2 | 22 AWG twisted pair | brown, brown/white | TEMP_EXH |
| 53 | X6:3, X6:4 | J2 pins 3, 4 | 22 AWG twisted pair | green, green/white | MOIST |
| 54 | X6:5, X6:6 | J2 pins 5, 6 | 22 AWG twisted pair | gray, gray/white | SENS2 |
| 55 | exhaust thermistor | X6:1, X6:2 | 22 AWG twisted pair, 105 °C | brown, brown/white | run apart from the mains harness |
| 56 | moisture bars | X6:3, X6:4 | 22 AWG twisted pair | green, green/white | |
| 57 | S1 COM, NO | X3:4, X3:5 | 14 AWG, 105 °C | black | door switch, mains contact, 6.3 mm quick-disconnects at the switch |
| 58 | S2 COM, NO | X5:1, X5:2 | 18 AWG | blue | door switch, SELV contact |
| 59 | PS1 COM, NO | X5:3, X5:4 | 18 AWG | blue | |
| 60 | TF2 | X5:5, X5:6 | 18 AWG, 105 °C | blue | 6.3 mm quick-disconnects |
| 61 | T_HI | X5:7, X5:8 | 18 AWG, 105 °C | blue | |
| 62 | T_LO | X5:9, X5:10 | 18 AWG, 105 °C | blue | |
| 63 | M1 L, N, PE | X3:1, X3:2, X3:3 | 14 AWG, 105 °C | black, white, green | motor leads, with the motor's own plug if it has one |

J1 pins 6, 7, 8, 14, 15, 16 and J2 pins 7, 8 are not wired in chassis v1.0; the housing positions are left empty.

All mains terminations are crimped ferrules (into screw or spring blocks) or crimped ring and spade terminals, made with a ratcheting crimper for that terminal. Mains wire inside the box is appliance wire rated 105 °C and 600 V. Torque for the terminal blocks is whatever the block maker prints on it; write it on the inside of the lid.

## 4. Separation, bonding, and labels

- Rails A1 to A3 carry mains; rails B1 and B2 carry SELV. The barrier between them runs the plate's full width out to the devices' depth, and the only crossing is the PSU output through a grommeted notch. No SELV wire runs along a mains bundle. The J1 and J2 leads leave through the top panel's grommet, the bay harness through its own ceiling grommet, never the cord's.
- The plate, every rail, the barrier, the cover, the heat module tray (its own M6 stud), and every panel carrying anything electrical are bonded to X1:4 through the ground stud, each with its own ring terminal and a star washer on bare metal. One bond each; no daisy chains through hinges or slides.
- 0V is bonded to PE once, by wire 21. Nothing else connects 0V to the frame, including the control module faceplate (which is bonded to the panel, not to 0V).
- Every terminal block is numbered as in section 2 with a printed marker strip. Every wire carries its number from section 3 on a heat-shrink or wrap-around label at both ends. The ladder drawing and this document are fixed to the inside of the lid in a plastic sleeve.
- A label on the cover: "Unplug the dryer before opening. 240 V inside. Rails A1 to A3 under this cover are mains. Rails B1 and B2 above are 24 V."

## 4a. Harness routes (draft 8)

Three harnesses leave the plate. Every one passes through a rubber grommet in a 1.5 mm plate and is clamped so it cannot touch the belt, the drum, or anything that gets hot.

- Cord: up from its strain relief bushing in the base pan (X -275, Y 690), straight up the back of the bay, through the 22 mm grommet in the bay ceiling at the same X and Y, to X1 on rail A1. One cable clamp on the base pan beside the bushing.
- Bay harness (motor M1 L and N, PS1, TF2, T_HI, T_LO, the heat module's X2 and X4 leads, the door switch S1): down through the 30 mm grommet in the bay ceiling at X -200, Y 690, then forward along the base pan's left side on four M4 cable clamps at X -250, Y 600, 440, 280 and 120 (4.5 holes in the pan), clear of the belt's left run (which crosses the ceiling at X -138) and the idler bracket (X -140 to -90, Y 366 to 390). Branches: to the motor's terminal box on its top (X 0, Y 260 to 320, by the clamp at Y 280); to TF2, T_HI and T_LO on the blower's outlet box (X 130 to 230, Y 150, Z 190) and PS1 on its bracket (X 250, Y 70) from the clamp at Y 120, crossing the bay in front of the motor and under the blower's outlet; to the heat module's terminal plate (X2 mains and X4 SELV, DIN rail at Y 635.5) from the clamp at Y 600, which is the harness that is unplugged to take the tray out. The mains and SELV conductors run as two bundles in the same clamps, and the thermistor pair (wire 55) runs apart from the mains bundle as its row says.
- Door switch S1: its two cables leave the bay harness at the clamp at Y 120, run along the pan to the right front, up through the 12 mm grommet in the bay ceiling at X 290, Y 60 (behind the front bulkhead, in the drum compartment outside the drum), 30 mm up the bulkhead's back face, through the 12 mm grommet in the bulkhead at X 290, Z 330 (outside the felt and the front roller's nut), and across the front of the bulkhead to the switch at X 182, Z 449 behind the front upper panel. Nothing of this run is inside the drum's sweep or in the air path; the drum compartment leg is 30 mm long and is where a sleeve of split loom goes.
- Console harness (the UCI-D cable, J1): up through the 22 mm grommet in the top panel at X -225, Y 690, to the console's module.

The door switch's motor-rated contact is in the motor's 120 V line (wire 57, S1 COM and NO to X3:4 and X3:5) and its second contact gates the 24 V bus (wire 58, S2 to X5:1 and X5:2); both pairs run in the bay harness, the mains pair with the mains bundle and the 24 V pair with the SELV bundle, and they separate only at the switch.

## 5. Cord variants

| Build | Cord | X1:2 (L2) | CB1 | Note |
| --- | --- | --- | --- | --- |
| Electric | NEMA 14-30P, 4-wire, 10 AWG, 1.8 m | wired | 10 A | the 30 A branch breaker protects the element path; CB1 protects the 120 V side |
| Gas, heat pump, none | NEMA 5-15P (or 5-20P for a heat pump unit that needs it), 3-wire, 14 or 12 AWG, 1.8 m | empty | 10 A | the branch breaker is the only protection for the heat module path |

The cord is listed appliance cord with a molded plug, entering through a listed strain relief sized to it. The plug is the disconnect; the lid label says so.

## 6. What the heat module tray must bring to X2 and X4

See `docs/design-rules.md` section 3.2 and `ladder-heat-modules.svg`. In short: the tray's own contactor or relay switches its own mains from X2; its coil is driven from X4:1 through whatever limits it adds on its side and returns to X4:2; it closes X4:3 to X4:4 while making heat; and its tray is bonded to X2:4.

## 7. Needs a real-world check before the parts are bought

1. CB1 curve against the motor's starting current. A C-curve 10 A breaker should hold a 1/3 hp motor start; a B curve may not.
2. F1 against the PSU's inrush. Supply makers state it; a 2 A time-delay fuse normally holds a 60 W supply.
3. The interface relays switching DC contactor coils. A DC coil is an inductive load that is hard on small contacts. The contactor's own suppression (some DC coils have it built in) or a diode across A1-A2 is required; confirm with the contactor datasheet.
4. The PTC hold values against the real loads: the Tier 0 hold relay on STAT_DOOR, and the electronic tiers' input dividers.
5. The thermostat and thermal fuse tabs: 6.3 mm quick-disconnects fit the usual appliance parts; confirm on the chosen parts.
6. S1's rating for the chosen motor, and that a second switch (S2) fits on the same actuator in CAD.
7. Terminal block ratings: 30 A blocks for X1 and X2 on the electric build; confirm the chosen family carries 10 AWG.
