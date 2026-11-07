# Dryer Universal Control Interface (UCI-D)

Version 1.0, draft 7, 2026-11-06 (draft 6 2026-11-06). Draft 7 only points sections 7.1 and 7.2 at where the chassis mounts the two sensors (model draft 9) and at their BOM lines; no pin, limit or envelope changes.

Status: draft. No chassis and no module implements it yet. Anything marked "check" in section 13 needs a real-world check before this becomes version 1.0.

Changes in draft 6: the aperture grows again, from 500 x 120 to 560 x 120, the faceplate to 620 x 160 and the hole pattern to 590 x 140 (the two centre-line holes stay), because the dryer's console face had 75 mm of bare panel beside a plate with 37 mm above it; 620 is as wide as the console's posts allow (their bolt heads sit at plus and minus 319, the plate ends at 310, the aperture 15 inside the posts). The module envelope grows with it to 560 x 120 x 120. Sections 4.1 to 4.3 and 10.

Changes in draft 5: the aperture grows from 240 x 120 to 500 x 120, the faceplate to 540 x 160, the hole pattern to 520 x 140 plus two holes on the centre line (six screws, so a 540 mm plate does not bow), and the envelope to 500 x 120 x 120. The Tier 0 module needs 240 of it; the rest is room for what later tiers put on the panel (a display beside the controls, more buttons, a Tier 3 screen) without a new chassis. The dryer's console was sized for it (`DECISIONS.md` 2026-11-06). Sections 4.1 to 4.3 and 10.

Changes in draft 4: the faceplate fasteners are M4 button head socket screws (2.5 mm hex key) instead of Phillips pan heads, following the dryer's decision to use one M4 head type everywhere (`DECISIONS.md` 2026-11-06); a chassis supplies nuts or press nuts behind its panel either way. Section 4.2.

Changes in draft 3: the aperture grows from 240 x 100 to 240 x 120, the faceplate to 280 x 160, the hole pattern to 260 x 140, and the envelope to 240 x 120 x 120 (the aperture's own projection), because a standard wall-device yoke (the spring-wound timers) is about 106 mm tall and would not pass a 100 mm opening. Section 13 item 1 updated.

Changes in draft 2: the heat source is a module (none, electric, gas, or heat pump) and the common power module ends at a HEAT_EN terminal (section 9); heat-source dependent start-up times (8.3 to 8.5); the door switch has a contact in the motor's mains line (section 9).

This is the interface between the dryer chassis and whatever controls it. The charter says the control interface is the product and the boards are examples of it. This document is that product for the dryer family. A control module built in 2046 that meets this document will run a chassis built in 2027, and the other way round.

## 1. What this document covers

The dryer chassis (frame, drum, door, motor, blower, heat module if one is fitted, power module, wiring) ends at:

- one rectangular hole in the control panel, with four screw holes around it,
- one 16-way connector called J1 that carries 24 V power, requests, and status,
- one 8-way connector called J2 that carries passive sensors.

A control module is anything that covers that hole and plugs into those connectors. Two mechanical timers and a relay (Tier 0), a small microcontroller board (Tier 1), a networked board with a web page (Tier 2), or anything else that follows this document (Tier 3).

This document defines the hole, the connectors, every pin, what the chassis guarantees without any help from the module, and what the module must and must not do.

It does not define the power module wiring, the design of any particular board, or the build steps. Those live in `electrical/`, `controls/tier*/`, and `docs/` and must agree with this document. Where they disagree, this document wins until it is changed under section 12.

## 2. Words used here

| Word | Meaning |
| --- | --- |
| Chassis | Everything that is not the control module. Frame, drum, door, motor, heater, power module, harness. |
| Power module | The metal box inside the chassis that holds the mains wiring, the 24 V power supply, the contactor, the relays, and the interlock chain. It is part of the chassis. |
| Heat module | The removable source of heat in the chassis base: an electric element box, a gas burner assembly, a sealed heat pump unit, or nothing at all. Part of the chassis, with its own interface defined in `docs/design-rules.md`. The control module never knows which one is fitted. |
| Control module, module | The removable controls: the faceplate, whatever is on it, and whatever is behind it. |
| Harness | The wires from the power module to J1 and J2. |
| Request | A line the module uses to ask the chassis for something (run the motor, give heat). |
| Status | A line the chassis uses to tell the module what is actually happening (door closed, airflow proven, heater on). |
| Assert | To make a request active. For request lines this means connecting the line to 0V. |
| Interlock | A hardwired switch in the chassis that cuts power on its own, with no board involved. |
| 0V | The return for the 24 V rail. Bonded to protective earth at one point inside the power module. |
| SELV | Safety extra-low voltage: 24 V DC or less, isolated from mains by a listed power supply. Everything at J1 and J2 is SELV. |

## 3. The contract on one page

**The chassis guarantees these on its own. The module cannot change them.**

1. The heat module, if one is fitted, is energized only while all of the following are true at the same time:
   - the door is closed, through a hardwired door switch,
   - the blower is moving air, through a hardwired air-proving switch,
   - the exhaust thermal fuse is intact,
   - the cycling thermostat for the selected heat level is calling for heat,
   - the heat module's own listed safety devices are all closed (electric: the heater-box thermal fuse and high-limit; gas: the burner high-limit, thermal fuse, and flame sensor circuit; heat pump: the compressor protector, the high-limit, and the anti-short-cycle timer; see section 9),
   - the module is asserting REQ_HEAT or REQ_HEAT_LO.
   With no heat module fitted, heat requests do nothing and STAT_HEAT_ON stays false. The dryer runs as an air-only tumbler.
2. The motor runs only while the door is closed and the module is asserting REQ_MOTOR. The motor has its own overload protection.
3. If the module asserts nothing, is unplugged, or has no power, the motor stops and the heater is off. There is no state of the module that the chassis treats as "keep going".
4. Nothing at J1 or J2 is above 24 V DC. It is isolated from mains by a listed power supply and by the coil-to-contact isolation of listed relays and a listed contactor. There is no mains voltage anywhere at the control panel.
5. The chassis needs nothing from the module for safety. With the module removed, the dryer does nothing at all.

**The module promises these.**

1. After power-up and after any reset it asserts nothing until a person starts a cycle at the faceplate.
2. It never asserts a heat request without also asserting REQ_MOTOR.
3. If it uses the exhaust temperature sensor, it stops requesting heat whenever that sensor reads open, shorted, or outside the range in section 7, and it shows a fault.
4. It changes REQ_HEAT and REQ_HEAT_LO at most once every 30 s. Turning heat off is allowed at any time.
5. It never drives voltage into a request, status, or sensor line. It stays within the current limits in section 6.
6. It is fully usable from its own faceplate. No network, phone, account, or other device is needed to run a cycle.
7. It comes out by unplugging J1 and J2 and removing four M4 screws, and nothing else.

## 4. Mechanical interface

All dimensions in millimeters. Tolerances are laser-cutter and drill-press tolerances: plus or minus 0.5 mm unless stated.

### 4.1 Panel aperture (chassis side)

The control panel has one rectangular opening for the module.

| Item | Value |
| --- | --- |
| Aperture, width x height | 560 x 120 |
| Corner radius | 5 max |
| Mounting holes | 6 x 4.5 diameter, clearance for M4 |
| Hole pattern | 590 x 140, centered on the aperture (one hole 15 mm outside each corner sideways, 10 above and below), plus one hole at the middle of each long edge (0, plus and minus 70) |
| Panel material and thickness | Laser-cut steel or aluminum, 1.5 to 3 |
| Nuts | Clip-on (U-type) sheet metal nuts, or plain M4 nuts with washers behind the panel. Both are catalog parts and need no press tooling. |
| Panel surface | Flat within 1 mm over the faceplate area, no stiffeners within 20 mm of the aperture edge |

The panel plane is the reference for everything else in this section. Where the aperture sits on the cabinet is up to the chassis design; it is normally in the raised console at the top rear, facing the person.

### 4.2 Faceplate (module side)

The module supplies its own faceplate. It covers the aperture and carries the knobs, buttons, lights, or screen.

| Item | Value |
| --- | --- |
| Faceplate, width x height | 620 x 160 |
| Corner radius | 10 max |
| Mounting holes | 6 x 4.5 diameter on the 590 x 140 pattern and the two centre-line holes |
| Thickness | 1.5 to 3 for metal; up to 4 for a printed plastic faceplate |
| Fasteners | 6 x M4 button head socket screws (ISO 7380, 2.5 mm hex key), 8 to 12 long, with washers under the heads where the faceplate is thinner than 2 mm. The chassis provides the nuts behind its panel (plain nuts, or press nuts if the panel is steel). One head type for every M4 on the appliance; the dryer's service set is the charter's four tools plus 2.5 and 4 mm hex keys. |
| Material | Laser-cut aluminum or steel preferred. A 3D-printed faceplate is acceptable for a module, since it is non-structural trim, and the print file must be in the repo. |
| Grounding | A metal faceplate is bonded to the chassis panel through at least one mounting screw with a star washer on bare metal, or by a separate ground wire with a ring terminal. |

### 4.3 Envelope

| Zone | Limit |
| --- | --- |
| Behind the panel plane | The module may occupy 560 wide x 120 high x 120 deep, measured from the panel plane: the aperture's own projection. The chassis keeps this volume clear of everything except the harness. Nothing on the module may sit behind the overlap band (30 at the sides, 20 above and below), because the chassis panel is there. |
| In front of the panel plane | Knobs, buttons, and screens may project up to 50 forward of the faceplate, within the faceplate outline. |
| Faceplate overlap | The faceplate overlaps the panel by 20 on each side. The chassis keeps that 20 mm band flat and free of other hardware. |

### 4.4 Harness reach

J1 and J2 arrive inside the envelope on flying leads from the power module.

- Free length: at least 200 from the panel plane to the connector face, so the module can be plugged in while it hangs outside the aperture.
- Both leads are strain-relieved to the chassis with a clip or cable tie anchor within 100 of the envelope, so pulling on a connector does not pull on the power module terminals.
- Nothing else enters the envelope. If a chassis option needs another connection to the module, it is a new pin on a reserved position under section 12, never a third connector.

### 4.5 Board footprint, recommended for PCB modules

Modules built on a printed circuit board should use this board size and hole pattern so that one faceplate, one set of standoffs, and one board outline serve every tier.

| Item | Value |
| --- | --- |
| Board outline | 160 x 100 (Eurocard size, so stock blanks and enclosures fit) |
| Mounting holes | 4 x 3.2 diameter, centers on a 150 x 90 pattern, 5 in from each edge |
| Standoffs | M3, 10 to 15 long, between the faceplate and the board |
| Keep-out | A knob or display cutout in the faceplate must not land on a standoff |

This is recommended, not required. A module that meets sections 4.1 to 4.4 and the electrical sections is compliant whatever is behind its faceplate. The envelope is wide enough for two of these boards side by side, or one board and a display.

## 5. Connectors

Two connectors, deliberately from two different families, so neither can be pushed into the other's socket.

### 5.1 J1, control: Molex Mini-Fit Jr., 16 circuits (2 x 8), 4.2 mm pitch

| Side | Part | Why |
| --- | --- | --- |
| Chassis harness | Receptacle housing with female crimp terminals (Molex 5557 housing, 5556 terminals, or compatible) | The chassis side is the side with 24 V on it, so it gets the recessed female contacts. This is the same reason a PC power cable is female. |
| Module, PCB | Header with male pins, vertical or right angle (Molex 5566 or 5569, or compatible) | Standard through-hole part. |
| Module, wired (Tier 0) | Plug housing with male crimp terminals (Molex 5559 housing, 5558 terminals, or compatible) | Lets a module with no PCB plug into the same harness. |

Wire: 0.5 to 0.75 mm2 (20 to 18 AWG), rated 105 °C. Crimped with a ratcheting crimper for Mini-Fit terminals.

### 5.2 J2, sensors: JST XH, 8 positions, single row, 2.5 mm pitch

| Side | Part |
| --- | --- |
| Chassis harness | XH housing with female crimp terminals (JST XHP-8 housing, SXH terminals, or compatible) |
| Module, PCB | XH header, top entry or side entry (JST B8B-XH-A or S8B-XH-A, or compatible) |
| Module, wired | Not needed. A module that does not read sensors leaves J2 unplugged. |

Wire: 0.2 to 0.35 mm2 (24 to 22 AWG), rated 105 °C.

### 5.3 Why these families

- Both are keyed, both latch or friction-lock, and both have been made by several companies for decades in volumes that will keep them alive.
- Mini-Fit Jr. is the PC power supply connector. Würth Elektronik sells an intermateable family (WR-MPC4) and many other makers sell compatible housings and terminals. JST XH is the battery balance connector and has the same breadth of compatible parts.
- A 16-way part from one family and an 8-way part from another cannot be forced into each other's socket. Two sizes of the same family could be, which is why there are two families.
- Both need a crimp tool. A ratcheting crimper for each family costs about the price of a good socket set, and the charter already assumes crimped terminals with the correct tool on the mains side.

Check before freezing the BOM: that the specific compatible parts chosen for `bom.csv` actually intermate (terminal and housing from one maker in the header from another), and the maker's current rating for the 16-way housing.

### 5.4 J1 pin table

Pin numbers follow the Molex convention: pins 1 to 8 in one row, 9 to 16 in the other, pin 9 directly across from pin 1.

| Pin | Name | Direction | Type | Safe state | Meaning |
| --- | --- | --- | --- | --- | --- |
| 1 | +24V | chassis to module | power | present | 24 V DC supply to the module |
| 2 | +24V | chassis to module | power | present | second contact, same rail |
| 3 | REQ_MOTOR | module to chassis | request | open | run the drum and blower motor |
| 4 | REQ_HEAT | module to chassis | request | open | heat, through the high cycling thermostat |
| 5 | REQ_HEAT_LO | module to chassis | request | open | heat, through the low cycling thermostat |
| 6 | REQ_AUX1 | module to chassis | request | open | reserved, not connected in chassis v1.0 |
| 7 | REQ_AUX2 | module to chassis | request | open | reserved, not connected in chassis v1.0 |
| 8 | RSVD_A | none | reserved | open | reserved, not connected |
| 9 | 0V | chassis to module | power | present | return for the 24 V rail |
| 10 | 0V | chassis to module | power | present | second contact, same return |
| 11 | STAT_DOOR | chassis to module | status | 0 V | 24 V while the door is closed |
| 12 | STAT_AIRFLOW | chassis to module | status | 0 V | 24 V while the air-proving switch is closed |
| 13 | STAT_HEAT_ON | chassis to module | status | 0 V | 24 V while the heater circuit is energized |
| 14 | STAT_AUX1 | chassis to module | status | 0 V | reserved, 0 V in chassis v1.0 |
| 15 | RSVD_B | none | reserved | open | reserved, not connected |
| 16 | RSVD_C | none | reserved | open | reserved, not connected |

### 5.5 J2 pin table

| Pin | Name | Type | Meaning |
| --- | --- | --- | --- |
| 1 | TEMP_EXH_A | sensor pair | exhaust air thermistor, one lead |
| 2 | TEMP_EXH_B | sensor pair | exhaust air thermistor, other lead |
| 3 | MOIST_A | sensor pair | moisture sensor bar 1 |
| 4 | MOIST_B | sensor pair | moisture sensor bar 2 |
| 5 | SENS2_A | sensor pair | optional second thermistor (heater box outlet or inlet air); may be left out |
| 6 | SENS2_B | sensor pair | second lead of the same |
| 7 | SENS3_A | sensor pair | reserved, not connected in chassis v1.0 |
| 8 | SENS3_B | sensor pair | reserved, not connected in chassis v1.0 |

Sensor pairs are passive and unpolarized. The module supplies whatever small excitation it needs (section 6.4).

## 6. Electrical definition of each signal type

### 6.1 Power: +24V and 0V

| Item | Value |
| --- | --- |
| Nominal | 24 V DC |
| At the connector, chassis guarantees | 21.6 to 26.4 V (24 V plus or minus 10 percent), ripple under 300 mV peak to peak |
| Module must work from | 20 to 28 V |
| Module must survive without damage | 0 to 32 V, any rate of rise or fall, brownouts, and repeated short interruptions |
| Module continuous draw, max | 1.0 A |
| Module peak draw, max | 2.0 A for 100 ms (a display backlight coming on, for example) |
| Chassis protection | The rail to J1 is protected at 2 A by a fuse or resettable PTC on the power module. The +24V pins are paralleled and the 0V pins are paralleled, so one poor contact does not drop the module. |
| Source | A listed DIN-rail or chassis-mount switch-mode supply, universal input (85 to 264 V AC), 24 V, at least 2.5 A, so the module's 1 A and the chassis's own coils fit with margin. Mean Well HDR and MDR series, Phoenix Contact UNO-PS, TDK-Lambda DRB, and others are equivalents. |
| Isolation | The supply provides reinforced isolation from mains per its listing. 0V is bonded to protective earth once, inside the power module. The module must not bond 0V to anything else. |
| Standby | The rail is live whenever the dryer is plugged in and the disconnect is on. A module that wants a true off has its own switch on its faceplate; the chassis has no soft-off. |

### 6.2 Request lines: REQ_MOTOR, REQ_HEAT, REQ_HEAT_LO, REQ_AUX1, REQ_AUX2

A request line is a sink. The chassis holds it at 24 V through the coil of its own interface relay; the module asserts the request by connecting the line to 0V.

This is the same arrangement as a furnace thermostat. A bare contact can do it (Tier 0), and so can a transistor (Tier 1 and up). A module with no power at all can still assert a request, which is what lets Tier 0 be nothing but timers and a relay.

| Item | Value |
| --- | --- |
| Open-circuit voltage on the line (not asserted) | The rail, up to 26.4 V |
| Current when asserted | 8 to 40 mA, set by the chassis's relay coil. The chassis guarantees at least 8 mA so that mechanical contacts in a module see enough wetting current to stay clean. |
| Module switch must handle | At least 100 mA and at least 40 V, open or closed indefinitely |
| Module leakage when not asserted | 0.5 mA or less, so a chassis relay can never be held in by a leaky output |
| Coil suppression | On the chassis, across each relay coil, so the module never sees more than the rail plus 1 V on the line. A module may add its own clamp. |
| Recognition time | A request held for 50 ms or longer is acted on. The chassis relay plus the contactor add up to about 100 ms before the motor or heater actually changes state. |
| Chatter | The chassis does not debounce. A module must not pulse a request line faster than the limits in section 8. |
| Line left open or cut | Not asserted. A cut harness wire is the same as "off". |

Two requests may be asserted at once. If REQ_HEAT and REQ_HEAT_LO are both asserted, the chassis gives low heat. A heat request without REQ_MOTOR gets no heat, because the air-proving interlock is open while the motor is stopped. REQ_AUX1 and REQ_AUX2 do nothing in chassis v1.0; a module may leave them open or drive them. When they are defined later (section 12) they may never be given a meaning that matters to safety.

### 6.3 Status lines: STAT_DOOR, STAT_AIRFLOW, STAT_HEAT_ON, STAT_AUX1

A status line carries 24 V when its condition is true and is open (so it reads 0 V through the module's own load) when it is false. True is the energized state on purpose: a broken wire, a tripped PTC, or an unplugged harness all read as "door not closed", "no airflow", "heater off".

| Item | Value |
| --- | --- |
| True | 18 V or more at the pin |
| False | 5 V or less at the pin |
| Between | Undefined. A module treats it as false. |
| Source | The chassis switches the rail onto the line through a contact and a resettable PTC fuse of about 100 mA hold, so a shorted line cannot take the rail down. |
| Module may draw | Up to 50 mA from a true status line. That is enough to hold in a small relay coil, which is how Tier 0 uses STAT_DOOR. |
| Module input, electronic | 4.7 kilohm or more to 0V, with the line divided down or opto-isolated to the module's logic level. A 24 V-tolerant input is required; a status line wired straight to a 3.3 V pin destroys the pin. |
| Response | The status follows the physical contact within 20 ms. There is no filtering on the chassis. |

What each one is wired to, in chassis v1.0:

- STAT_DOOR: the 24 V bus downstream of the hardwired door switch, called 24V_ILK in the power module. This is the same switch that cuts the motor and heater coil circuits, so STAT_DOOR going false means the chassis has already stopped, not that the module should stop it.
- STAT_AIRFLOW: downstream of the hardwired air-proving switch in the heater coil circuit. True means air is moving through the blower and heat is possible.
- STAT_HEAT_ON: true while the heat module is producing heat, or as close to that as a listed part can sense. Electric: a current-operated switch clamped around one element lead (preferred; it means current is flowing in the element) or the contactor's auxiliary contact (it means the contactor is pulled in). Gas: a relay with a 120 V coil wired across the gas valve, so true means the valve is open and the flame sensor has proved the igniter or the flame. Heat pump: a current switch on the compressor lead or the compressor contactor's auxiliary contact. None: permanently false. A chassis states which one it uses in its wiring documentation.
- STAT_AUX1: 0 V. Reserved.

### 6.4 Sensor pairs: TEMP_EXH, MOIST, SENS2, SENS3

A sensor pair is two wires to a passive element. The chassis puts nothing on them. The module supplies the excitation and does the measuring, so a module can use whatever measuring method its designer likes, and the chassis stays a bag of resistors and metal.

| Item | Value |
| --- | --- |
| Excitation the module may apply | 5 V or less open circuit, 1 mA or less short circuit, on any pair |
| Isolation | Every sensor is isolated from mains and from the chassis frame by its own construction. The moisture bars can be touched by hand inside the drum, which is why the excitation limit is what it is. |
| Chassis wiring | Twisted pair, 24 to 22 AWG, run apart from the mains harness. A thermistor pair may be up to 2 m long. |
| Open pair | Reads as open circuit (over 1 megohm). A module that is configured to use that sensor treats this as a fault. A module not configured for it ignores it. |

## 7. Sensors in detail

### 7.1 TEMP_EXH, exhaust air thermistor (J2 pins 1 and 2)

| Item | Value |
| --- | --- |
| Type | NTC thermistor, 10 kilohm at 25 °C, two wires, in a sealed probe or on a bracket in the exhaust air stream between the drum and the blower |
| Range it must report | minus 20 to 150 °C |
| Where it is | In the exhaust path between the drum and the blower: the chassis mounts it on the bay side of the lint box's back plate, right of the spool, its nib sensing inside the box (`docs/design-rules.md` 7a Air, model draft 9), upstream of the blower and of the cycling thermostats on its outlet, so the module sees the air a moment before the thermostats do; `bom.csv` CPM-TH1 |
| Exact part | Named in `bom.csv` with its resistance table or B value. Appliance-market dryer thermistors (sold as repair parts for several major brands) and industrial 10 kilohm NTC probes with a stainless sheath are both acceptable. Check: that the two chosen sources share a curve close enough that one table in the module works for both, or ship one table per part. |
| Module side | The module holds the resistance-to-temperature table in its human-readable configuration file, per the charter's firmware rules, so a replacement thermistor with a different curve is a config edit, not a firmware build. |
| Fail-safe reading | Below 500 ohm (shorted) or above 200 kilohm (open) at any time, or a jump of more than 30 °C between two samples 1 s apart, is a sensor fault. The module drops the heat request and shows a fault. The chassis's own thermostats and fuses protect the dryer whether or not the module gets this right. |

### 7.2 MOIST, moisture sensor bars (J2 pins 3 and 4)

| Item | Value |
| --- | --- |
| Type | Two stainless steel bars, electrically isolated from each other and from the drum, mounted on the front bulkhead or lint filter housing where tumbling clothes brush across both. Wet cloth conducts between them; dry cloth does not. |
| Reading | The module measures conductance between the bars with 5 V or less and 1 mA or less, by whatever method it likes (a divider and an ADC is enough). Readings are noisy by nature; the module averages over many seconds. |
| Open | Dry drum, no clothes, or a bar lead off. These look the same. A module uses moisture only to end a cycle early, never to extend it past the time the person set, so a broken bar lead costs nothing but the auto-dry feature. |
| Exact part | Appliance-market sensor bar sets are sold as repair parts for several brands. Two strips of 304 stainless on an insulating mount with a printable file is the fallback. `bom.csv` CPM-MOIST. The chassis mounts the set on the front bulkhead's drum side, inside the drum ring's bore at 58 degrees right of bottom, where the load brushes it on every turn, with its terminals through the bulkhead to the front gap (`docs/design-rules.md` 7a Bulkheads, model draft 9). |

### 7.3 SENS2, optional second thermistor (J2 pins 5 and 6)

Same type as TEMP_EXH. Intended for the heater box outlet or the inlet air, so a Tier 2 module can report the temperature rise across the element, which is a direct read on airflow and vent restriction. A chassis may leave it out, in which case the pair is open.

### 7.4 SENS3, reserved (J2 pins 7 and 8)

Not connected in chassis v1.0. A module leaves it alone.

## 8. Behavior rules

These are the rules a module follows. The chassis enforces the ones that matter for safety on its own. The module follows them anyway so that the dryer behaves well and the interlocks are not what stops it every day.

### 8.1 Power-up and reset

- At power-up, after a brownout, and after any reset or firmware restart, all request lines are open until a person starts a cycle at the faceplate.
- A module must not restart a cycle on its own after power returns. If it wants to offer "resume", it asks the person first.
- Tier 0 meets this with a start button and a hold relay: a power loss drops the relay and the dryer waits for the button (see `controls/tier0-mechanical/`).

### 8.2 Starting and stopping

- A cycle starts only from the faceplate. A Tier 2 module may also start from its local web page if its documentation says so, and the faceplate must still be able to stop it.
- When STAT_DOOR goes false during a cycle, the chassis has already stopped the motor and heater. The module drops all requests and waits for the person; it does not re-assert them when the door closes again. The dryer should not lurch back into motion when someone closes the door after fishing out a sock.
- Stopping is always allowed and always immediate. The module may open every request line at any time.

### 8.3 Heat

- Heat is requested only while REQ_MOTOR is asserted.
- A module that ends heat before the end of the cycle (cool-down) keeps REQ_MOTOR asserted for the rest of the cycle. Recommended cool-down: at least 5 min of motor with no heat at the end of every heated cycle.
- A module may choose REQ_HEAT or REQ_HEAT_LO per cycle. It may switch between them, within the rate limit.
- Rate limit: a module changes the state of REQ_HEAT or REQ_HEAT_LO at most once every 30 s, except that it may open either line at any time. The hardware cycling thermostats do the fast regulation; the module's job is to set the level and the schedule. A module that wants a temperature below the low thermostat's setpoint may pulse REQ_HEAT_LO at this rate limit using the exhaust thermistor, and should say in its documentation that this costs contactor life.
- On a chassis with a heat pump module, a module should hold its heat request for the whole heated part of the cycle and not toggle it. The chassis's anti-short-cycle timer protects the compressor whatever the module does, at the cost of a wait of several minutes each time heat is requested again.

### 8.4 Faults the module must notice

| What the module sees | What it means | What the module does |
| --- | --- | --- |
| REQ_MOTOR asserted, STAT_DOOR true, STAT_AIRFLOW stays false for more than 10 s | Motor not turning, belt or blower problem, or the air-proving switch or its tube is at fault | Drop all requests, show a fault |
| Heat requested, STAT_AIRFLOW true, exhaust temperature below 40 °C, STAT_HEAT_ON false for longer than the heat module's start-up time (8.5) | A limit has opened, a thermal fuse has blown, the burner failed to light, or the contactor, element, or compressor has failed. (With the exhaust above 40 °C the cycling thermostat may simply be open, which is normal regulation, not a fault.) | Keep the motor running for cool-down, drop the heat request, show a fault. Do not retry heat on its own. |
| TEMP_EXH out of range (section 7.1) | Sensor fault | Drop heat, show a fault |
| TEMP_EXH above 90 °C while heat is requested | Vent restricted or a thermostat stuck closed | Drop heat, keep the motor, show a fault |
| STAT_HEAT_ON true with no heat requested for more than 5 s | Chassis fault: welded contactor or shorted interface relay. The hardware limits still cap the temperature. | Drop all requests, show a fault that tells the person to unplug the dryer and not use it until the power module is repaired |

Tier 0 cannot notice any of these and does not need to; the chassis's own limits handle every one of them without a board. The table is what the electronic tiers add on top.

The heat choice and its start-up time are two lines in the module's human-readable configuration file (`heat: none | electric | gas | heatpump` and `heat_startup_s`, defaults in 8.5). A module configured for `heat: none` never requests heat and never raises a heat fault; the HIGH and LOW settings on its faceplate do nothing, and its documentation says so.

### 8.5 Timing summary

| Item | Value |
| --- | --- |
| Request recognized after | 50 ms |
| Motor or heater physically responds after | about 100 ms |
| Status follows physical state within | 20 ms |
| Minimum interval between heat level changes | 30 s |
| Airflow must prove within | 10 s of REQ_MOTOR |
| Heat module start-up time, electric | 30 s |
| Heat module start-up time, gas | 120 s (igniter warm-up and trial for ignition) |
| Heat module start-up time, heat pump | 6 min (anti-short-cycle lockout plus compressor start) |
| Heat module start-up time, none | never; the module is configured for no heat |
| Recommended cool-down | 5 min or more |

## 9. What a chassis provides, at block level

This is what the power module does behind J1 and J2. The wiring document and ladder drawings in `electrical/wiring/` are the authority for the actual wiring; this section is what they must amount to.

The chassis has a common power module, which is the same whatever makes the heat, and a heat module, which is one of four: none, electric, gas, or heat pump. The common power module ends at a terminal called HEAT_EN (X4:1). The heat module interface is defined in `docs/design-rules.md` section 3.2 and the terminal map and wire list are in `electrical/wiring/common-power-module.md`; the chain is drawn here so it is visible end to end, and in `electrical/wiring/ladder-common-power-module.svg` as a drawing.

```
COMMON POWER MODULE, mains side

L1 --[DOOR SWITCH contact 1]--[MOTOR OVERLOAD]--[K_MOTOR]--[MOTOR 120 V]-- N

L1 --[fuse]--[24 V POWER SUPPLY, listed, universal input]-- N
                          |
                          +24V and 0V   (0V bonded to PE here)

L1, L2, N, PE ---------------------------> heat module terminals (unswitched; the heat module has its own switching device)

COMMON POWER MODULE, 24 V side (SELV)

+24V --[DOOR SWITCH contact 2]-- 24V_ILK

24V_ILK --[RLY_MOTOR contact]--[K_MOTOR coil]-- 0V

24V_ILK --[AIR-PROVING SWITCH]--[EXHAUST THERMAL FUSE]--+--[RLY_HEAT_LO 11-12, n.c.]--[RLY_HEAT 11-14]--[CYCLING THERMOSTAT HI]--+--> HEAT_EN, terminal X4:1 (to the heat module)
                                                        |                                                                       |
                                                        +--[RLY_HEAT_LO 11-14, n.o.]--[CYCLING THERMOSTAT LO]------------------+

+24V --[RLY_MOTOR coil]----> J1.3  REQ_MOTOR      (module connects to 0V to assert)
+24V --[RLY_HEAT coil]-----> J1.4  REQ_HEAT
+24V --[RLY_HEAT_LO coil]--> J1.5  REQ_HEAT_LO

24V_ILK --------------------------------------------[PTC]--> J1.11 STAT_DOOR
downstream of AIR-PROVING SWITCH -------------------[PTC]--> J1.12 STAT_AIRFLOW
heat module STAT_HEAT_ON contact -------------------[PTC]--> J1.13 STAT_HEAT_ON

+24V --[2 A fuse or PTC]--> J1.1, J1.2
0V -----------------------> J1.9, J1.10

HEAT MODULE, one of:

none       HEAT_EN not connected. No STAT_HEAT_ON contact (the line stays open). The bay holds a blanking duct.

electric   HEAT_EN --[K_HEAT coil, 24 V DC]-- 0V
           L1 --[K_HEAT pole 1]--[THERMAL FUSE, heater box]--[HIGH-LIMIT, heater box]--[ELEMENT]--[K_HEAT pole 2]-- L2
           STAT_HEAT_ON: current switch on an element lead, or K_HEAT auxiliary contact

gas        HEAT_EN --[K_HEAT coil, 24 V DC]-- 0V
           L1 --[K_HEAT]--[BURNER HIGH-LIMIT]--[THERMAL FUSE]--[BURNER ASSEMBLY: igniter, radiant flame sensor, gas valve coils]-- N
           STAT_HEAT_ON: relay with a 120 V coil across the gas valve (true = valve open)

heat pump  HEAT_EN --[ANTI-SHORT-CYCLE TIMER]--[CONDENSER OUTLET HIGH-LIMIT]--[CONDENSATE SAFETY SWITCH]--[K_COMP coil, 24 V DC]-- 0V
           L1 --[K_COMP]--[SEALED UNIT: compressor with its own protector, and its high-pressure switch if it has one]-- N
           STAT_HEAT_ON: current switch on the compressor lead, or K_COMP auxiliary contact
```

Notes on the ladder:

- RLY_HEAT_LO is one changeover contact with its common (11) at the branch point: the n.c. side (12) feeds the high branch, the n.o. side (14) feeds the low branch. That is what makes low heat win when both heat requests are asserted.
- The door switch has two contacts. Contact 1 is in the motor's mains line, so opening the door opens the motor circuit itself, the way every residential dryer does it, and the way the charter asks (a hardwired interlock in the mains path). Contact 2 gates 24V_ILK, which every coil circuit and STAT_DOOR hang from. No heat module has a door contact in its own mains line, because no door switch is rated for element current; heat is cut by contact 2 and, a moment later, by the air-proving switch when the motor stops.
- HEAT_EN is a permission, not a command. A heat module may only make heat while it is present, and it must have its own listed limits in series with its heat source whether or not HEAT_EN is there. The electric module's thermal fuse and high-limit are in the element's mains path. The gas burner assembly carries its own flame safety: the igniter heats through the radiant sensor, the sensor opens when it sees the igniter glow, that opens the gas valve, and a flame that goes out closes the sensor and the valve with it. The heat pump's compressor has its own thermal protector, and the anti-short-cycle timer keeps a request that comes and goes from restarting it against a pressure head.
- Everything that decides whether heat happens is a switch, a fuse, or a bimetal disc. Nothing above contains firmware. The only decision the control module makes is when to pull a request line down.

Part families, with the generic spec that is their real identity:

| Block | Generic spec | Catalog families (examples, two or more makers each) |
| --- | --- | --- |
| K_HEAT, electric | 2-pole contactor, AC-1 rating 32 A or more at 240 V, 24 V DC coil, listed | IEC contactors with a DC coil option: Schneider LC1D, Siemens 3RT2, ABB AF, Eaton DILM |
| K_HEAT, gas | Relay or contactor rated for the burner circuit at 120 V including the igniter's inrush, 24 V DC coil, listed | Same families in the smallest size, or a 10 A plug-in relay rated for the load |
| K_COMP, heat pump | Contactor rated for the compressor's locked-rotor current at 120 V (AC-3 or hp rated), 24 V DC coil, listed | Same families, sized from the sealed unit's nameplate |
| K_MOTOR | Contactor or relay rated for the motor (AC-3 or hp rated) at 120 V, 24 V DC coil, listed | Same families in the smallest size, or a motor-rated plug-in relay |
| RLY_MOTOR, RLY_HEAT, RLY_HEAT_LO | Slim interface relay, 24 V DC coil with built-in suppression diode, 1 or 2 changeover contacts, 6 A, socket or DIN mount | Finder 38 and 39 series, Phoenix Contact PLC-RSC, Omron G2RV, Weidmüller TERMSERIES, Schneider RSL |
| Anti-short-cycle timer, heat pump | Timer relay, lockout (delay-on-break) function, 3 to 5 min, 24 V DC, listed | Multifunction timer relays: Finder 80 series, Omron H3DK, Schneider RE17, Macromatic; HVAC anti-short-cycle timers where the coil voltage matches |
| Power supply | 24 V DC, 2.5 A or more, universal input, listed, DIN rail or chassis mount | Mean Well HDR-60-24 and MDR-60-24, Phoenix UNO-PS, TDK-Lambda DRB |
| Door switch | Listed door interlock switch with two contacts: one rated for the motor at 120 V including starting current, one for the coil currents; or two listed switches on one actuator | Appliance-market dryer door switches (these are built to switch the motor directly); IEC safety limit switches such as Schneider XCK or Omron D4N for the coil contact |
| Air-proving switch | Listed air pressure switch with a normally open contact that closes on blower pressure; setpoint to be measured on the prototype | Furnace pressure switches: Honeywell, Tridelta, Cleveland Controls NS2 |
| Cycling thermostats | Bimetal disc thermostats, normally closed, open at the set exhaust temperature, appliance market; the L-ratings are chosen per heat module | Sold as dryer repair parts in the standard L-number ratings (L135, L155 and so on; the numbers are Fahrenheit because that is how the appliance market sells them) |
| Heater-box high-limit, electric | Bimetal disc thermostat, normally closed, auto reset, opens well above the cycling range, rated for the element current, appliance market | Dryer repair parts |
| Burner high-limit, gas | Bimetal disc thermostat on the burner housing, normally closed, rated for the burner circuit, appliance market | Dryer repair parts |
| Thermal fuses | One-shot thermal cutoff: one in the heater box or on the burner housing, rated for its circuit; one on the exhaust, carrying coil current only | Dryer repair parts |
| Burner assembly, gas | Listed dryer burner assembly: valve body with its coils, hot surface igniter, radiant flame sensor, orifice; LP conversion kit available | Appliance-market burner assemblies and their coil, igniter, and sensor kits |
| Sealed unit, heat pump | Pre-charged, sealed heat pump assembly with a fixed-speed compressor, evaporator, condenser, and drain pan, bought as one unit | OEM heat pump dryer assemblies sold as repair parts; see `docs/design-rules.md` 5.4 for what is known and what is not |
| Condensate safety switch, heat pump | Float switch in the drain pan, tank, or condensate pump, normally closed, opens on high level, listed | Condensate pumps with a safety switch (Little Giant, DiversiTech, Aspen); float switches (RectorSeal, DiversiTech) |
| STAT_HEAT_ON source | Current-operated switch, clamp type, listed, contact closes above a set current; or a relay with a 120 V coil; or the contactor's auxiliary contact block | Veris Hawkeye, NK Technologies, Functional Devices RIB current sensors; Finder 40 series and Omron MY relays with 120 V coils |
| PTC fuses | Resettable PTC, 100 mA hold class for status lines, 2 A hold class for the rail | Littelfuse, Bourns, Bel Fuse |

## 10. Tiers under this spec

| Tier | Uses | Typical faceplate | Notes |
| --- | --- | --- | --- |
| 0 Mechanical | J1 pins 3, 4, 5, 9, 11 | DRY TIME knob, HEAT TIME knob, AIR / LOW / HIGH switch, START button, spread across the plate | Two spring-wound interval timers, one hold relay, no electronics. Uses STAT_DOOR as the hold relay supply so the door and a power loss both end the latch. Timers of 0 to 2 h suit vented builds, 0 to 4 h a heat pump build. The reference build. |
| 1 Basic | J1 all, J2 pins 1 to 4 | Buttons, LEDs or a character display; the 560 mm plate has room for a 7 inch class display beside a row of buttons | Small microcontroller, 24 V to 5 V or 3.3 V buck module, open-drain outputs, divided inputs. Timed cycles, auto-dry from the moisture bars, fault display. |
| 2 Smart | J1 all, J2 all | Display and buttons, plus a local web page | ESP32 class. Everything Tier 1 does, plus logging and a local web interface. No feature needs the internet. |
| 3 Open slot | Anything | Anything within the envelope | Whatever follows sections 3 to 8. A screen is a Tier 3 accessory and brings its own mounting spec. |

## 11. Compliance checklists

A chassis is UCI-D compliant when every line below is true. The same for a module.

**Chassis**

- [ ] Aperture, hole pattern, panel flatness, and clear band per 4.1
- [ ] Envelope clear per 4.3
- [ ] J1 and J2 of the specified families, chassis-side genders, reach, and strain relief per 4.4 and 5
- [ ] Rail within the 6.1 limits, protected at 2 A, 0V bonded to PE once
- [ ] Every request line is a 24 V sink through a suppressed coil, 8 to 40 mA, and open means off
- [ ] Every status line is true-when-energized, PTC protected, and wired as 6.3 describes
- [ ] Every sensor pair is passive, isolated, and wired as section 7 describes, or left open and documented
- [ ] With the module removed and the J1 lines shorted together in any combination, the heat module cannot be energized with the door open, without airflow, with any limit open, or without a heat request
- [ ] With no heat module fitted, the dryer runs as an air-only tumbler, nothing but unswitched mains and an open HEAT_EN sits at the heat module terminals, and STAT_HEAT_ON is false
- [ ] With the module removed and the J1 lines shorted together in any combination, the motor cannot run with the door open
- [ ] No mains voltage at J1, J2, the faceplate, or anywhere in the envelope
- [ ] The wiring documentation names the STAT_HEAT_ON source and the exact thermistor

**Module**

- [ ] Faceplate outline, holes, thickness, material, and bonding per 4.2
- [ ] Stays within the envelope per 4.3
- [ ] Works from 20 to 28 V, survives 0 to 32 V, draws 1 A or less continuous and 2 A or less for 100 ms
- [ ] Request outputs are sinks rated 100 mA and 40 V, leak 0.5 mA or less, and are open at power-up and after any reset until a person acts
- [ ] Status inputs are 24 V tolerant, 4.7 kilohm or more, and never driven
- [ ] Sensor excitation 5 V and 1 mA or less, and sensor faults drop heat
- [ ] Never requests heat without the motor, never re-asserts after a door opening without a person, rate-limits heat changes to one per 30 s
- [ ] Fully usable from the faceplate alone
- [ ] For electronic tiers: its configuration states the heat choice and start-up time, and a `none` configuration never requests heat
- [ ] Removable with four M4 screws and two plugs
- [ ] Its repo folder holds everything needed to rebuild it: faceplate drawing, wiring or board files, a parts list with two vendors per line, and for electronic tiers the firmware source and build instructions

## 12. Versioning and reserved pins

- This document carries a version, MAJOR.MINOR. A chassis and a module each state which version they were built to.
- Within a MAJOR version nothing already defined ever changes meaning, direction, voltage, pin, or safe state. A 1.x module works on any 1.x chassis and the other way round, with a feature missing when a reserved pin is implemented on only one side.
- A MINOR version may define a reserved pin (REQ_AUX1, REQ_AUX2, STAT_AUX1, RSVD_A, RSVD_B, RSVD_C, SENS3), and only in a way where a chassis that leaves it unconnected and a module that leaves it open are both still safe and still compliant. A reserved request line may never be given a meaning where asserting it is needed for safety, or where a chassis that lacks it could be made unsafe by a module that drives it.
- Changing a connector family, the aperture, the hole pattern, or the rail voltage is a MAJOR version. The old version stays published forever, so a 1.x module can always be rebuilt.
- Every change is an entry in `DECISIONS.md` in the dryer repo and in `osa-charter/uci/`.

## 13. Needs a real-world check

Things in this draft that are reasoned, not measured. Each one blocks version 1.0 until someone has checked it on parts in hand.

1. The aperture and envelope against real parts. The Intermatic FD series sheet gives the timer body as 70.9 x 40.6 x 30.2 mm behind a standard wall-device yoke, which set the 120 mm height; the yoke length (about 106 mm) and the knob diameter are not on the sheet and must be measured on a part in hand. A 20 x 4 character display and a small touchscreen in a bezel still need checking against the envelope.
2. Mini-Fit Jr. and XH compatible parts from two makers actually intermating, and the current rating of the 16-way housing with the terminals chosen.
3. The wetting current. 8 mA is a reasoned minimum for mechanical contacts switching 24 V DC. If the spring-wound timer maker states a minimum load, that number wins.
4. The air-proving switch: whether a furnace-style pressure switch holds reliably on dryer blower pressure with a lint-laden stream, where the tap goes, and what setpoint. A sail switch is the fallback and has its own lint problem. This is the one interlock that is not a plain copy of the appliance industry's usual wiring, and it needs a test rig, not an argument.
5. Cycling thermostats in the 24 V coil circuit instead of the element circuit. This is how commercial dryers with contactors do it, and it keeps all temperature control at SELV, but it means the contactor operates every thermostat cycle. Confirm the chosen contactor's electrical life at the element load covers at least 20 years at a few cycles per load, or move the cycling thermostats into the element circuit and log the change.
6. Thermal fuse and high-limit current ratings against the element current. If the appliance-market heater-box parts are not rated for the full element current in this circuit, use ones that are, or move the under-rated one into the coil circuit and log the change.
7. The STAT_HEAT_ON current switch: that a listed clamp-type current switch exists with a pickup low enough and a contact rated for 24 V DC. Otherwise the contactor auxiliary contact is the fallback, and the spec already allows it.
8. 0V bonded to PE: confirm against the power supply maker's application notes and the local code reading before the first build.
9. A listed door switch with a motor-rated contact and a second contact, from two makers. If only single-contact switches exist, use two switches on one actuator. Dropping the mains-line contact and relying on the coil circuit alone would need a `DECISIONS.md` entry, since the charter asks for the interlock in the mains path.
10. The start-up times in 8.5 against a real gas ignition sequence and the chosen anti-short-cycle timer.
11. STAT_HEAT_ON for gas: a listed relay with a 120 V coil wired across the gas valve coil, or a current switch with a pickup below the valve's holding current.
12. The 40 °C exhaust threshold in 8.4 against the closing temperatures of the cycling thermostats chosen for every heat module, so a module never calls a fault during normal regulation.
