# Tier 0: mechanical control module

Draft 2, 2026-11-05. Status: faceplate drawn (`mechanical/drawings/tier0-faceplate.dxf` and `.svg`), wiring drawn (`tier0-wiring.svg`). Nothing built.

The reference control module for the dryer. No microcontroller, no firmware, no printed circuit board. Two knobs, a switch, a button, and one relay. It plugs into J1 only.

## What the person sees

| Control | What it is | What it does |
| --- | --- | --- |
| DRY TIME | Spring-wound interval timer, 0 to 120 min (0 to 4 h on a heat pump build), no HOLD position | Sets how long the drum turns. Wind it to set it. |
| HEAT TIME | Spring-wound interval timer, same range as DRY TIME, no HOLD position | Sets how long heat is asked for. Set it shorter than DRY TIME for a cool-down. On a heat pump build, set it equal to DRY TIME; the compressor should not be cycled. |
| HEAT | Three-position selector switch, 22 mm, AIR / LOW / HIGH | Picks no heat, the low thermostat, or the high thermostat. |
| START | Momentary push button, normally open | Starts the cycle. Must be pressed with the door closed and time on the DRY TIME knob. |

Stopping: open the door, or turn DRY TIME to zero. There is no stop button because the door is one.

## How it works

One relay, K1: a 24 V DC plug-in relay with two changeover contacts and a suppression diode, in a socket.

- K1's coil is fed from STAT_DOOR (J1 pin 11), which carries 24 V only while the door is closed, through the START button, through the DRY TIME timer contact, to 0V (J1 pin 9).
- K1 contact A is wired across the START button, so once K1 pulls in it holds itself.
- K1 contact B connects REQ_MOTOR (J1 pin 3) to 0V, which asks the chassis to run the motor.
- The same contact B also feeds the HEAT TIME timer contact, which feeds the HEAT switch, which connects REQ_HEAT (J1 pin 4), or REQ_HEAT_LO (J1 pin 5), or nothing, to 0V.

So:

- Door open: STAT_DOOR is 0 V, K1 cannot pull in and drops if it was in. Everything stops. Closing the door does not restart anything; START must be pressed again.
- Power out: K1 drops. When power returns, nothing happens until START is pressed.
- DRY TIME runs out: its contact opens, K1 drops, both requests open.
- HEAT TIME runs out: the heat request opens, the motor keeps running until DRY TIME runs out. That is the cool-down.
- HEAT TIME set longer than DRY TIME: heat ends when the motor does, because K1 drops, and because the chassis's air-proving switch opens anyway.
- START pressed with DRY TIME at zero: nothing happens.

Everything above is a switch. The chassis's own interlocks (door, airflow, thermal fuses, high-limit, cycling thermostats) are in series with everything this module can ask for, so a wiring mistake here can at worst make the dryer not run.

## Pins used

| J1 pin | Name | How Tier 0 uses it |
| --- | --- | --- |
| 3 | REQ_MOTOR | K1 contact B to 0V |
| 4 | REQ_HEAT | HEAT switch HIGH position, through HEAT TIME, through K1 contact B, to 0V |
| 5 | REQ_HEAT_LO | HEAT switch LOW position, same path |
| 9 | 0V | Return |
| 11 | STAT_DOOR | Supply for K1's coil, through START and DRY TIME |

Pins 1 and 2 (+24V) are not used. Tier 0 draws its only power from STAT_DOOR, well under the 50 mA that line allows. J2 is left unplugged.

## Known quirks

- A spring-wound timer keeps winding down while the dryer is stopped. Open the door for five minutes to add a sock and you lose five minutes of dry time. Wind it back up. A cam timer with a motor would pause; this one cannot, and that is the price of needing no power.
- The timers tick. Some people like that.
- On a build with no heat module, the HEAT switch and HEAT TIME knob do nothing. Leave them fitted anyway; a heat module can be added later with no change here.
- Both timers must be the version without a HOLD position. With HOLD, a person could set the heater to run until the door opens. The chassis thermostats would still keep the temperature in range, but it is a setting no dryer should offer.

## Parts, by generic spec

Vendor part numbers go in `bom.csv` with two vendors each. These are the part families.

| Item | Generic spec | Catalog families |
| --- | --- | --- |
| Timers, 2 off | Spring-wound interval timer, 0 to 2 h (0 to 4 h for a heat pump build), SPST contact closed while timing, no HOLD position, standard wall-device yoke | Intermatic FD2HW or FD2H (FD4HW or FD4H for 4 h); in this family W means white, not without hold, and the HOLD models carry a second H (FD6HH, FD12HH), so avoid those. Marktime 93 series is the second family. Body 70.9 x 40.6 x 30.2 mm per the maker's sheet. Check the maker's minimum load against the UCI-D 8 mA wetting current. |
| HEAT selector | 22 mm panel-mount 3-position selector switch with two normally open contact blocks (one closed in LOW, one in HIGH), rated for 24 V DC | Schneider XB4BD33 with ZBE101 blocks, Eaton M22-WRK3 with M22-K10 blocks |
| START | Momentary push button, normally open, 22 mm panel mount, rated for 24 V DC | Schneider XB4, Eaton M22, IDEC, Omron A22 |
| K1 | Plug-in relay, 24 V DC coil with suppression diode, 2 changeover contacts, 5 A or more, with a matching socket | Omron MY2, Finder 55.32 or 56.32, Schneider RXM2AB, IDEC RH2B, and their sockets |
| Plug to J1 | Mini-Fit Jr. 16-circuit plug housing with male crimp terminals | Molex 5559 and 5558, or compatible |
| Faceplate | Laser-cut 2 mm aluminum, 280 x 160 mm, UCI-D hole pattern, shaft holes and yoke holes for two timers, two 22.3 mm holes | `mechanical/drawings/tier0-faceplate.dxf`; the shaft hole size and knob diameter are to be checked on a timer in hand |
| K1 mounting | 100 mm of 35 mm DIN rail on two M4 standoffs, 12 mm long, behind the faceplate | Any |
| Timer nuts | 6-32 hex nuts and washers, 4 off, for the screws supplied with the timers | Hardware store |
| Wire and terminals | 0.5 mm2 stranded, 105 °C, with 6.3 mm insulated quick-disconnects for the timers and switch, crimped with a ratcheting crimper | Any |

## How the timers mount

The timers are wall-box devices. Their yoke (the steel strap with the slotted ears, about 106 mm long) sits against the back of the faceplate, held by the 6-32 screws that come with the timer, through the two 4 mm holes at 83.3 mm spacing, with nuts behind. The shaft comes through the 12 mm hole and the knob presses on from the front, exactly as it would through a wall plate. No wall plate is used.

## Still to do

1. Buy one timer and measure the yoke length, the shaft diameter, and the knob diameter against the faceplate drawing. The body size is from the maker's sheet; the rest is not.
2. Write the K1 socket's terminal numbers onto `tier0-wiring.svg` once the socket is in hand.
3. Confirm K1's coil current at 24 V is under 50 mA (most 24 V DC plug-in relays draw 30 to 40 mA).
4. Confirm the timer contacts are happy switching 24 V DC at the relay coil current. If the maker lists a minimum load above what the chassis provides, add a parallel load resistor on the chassis side and record it.
5. Cut one faceplate and fit everything to it before the drawing is called done.
