# Commissioning checklist

Draft 1, 2026-11-05. Status: written from the paper design. It has not yet been run on a real build, and it will change when it is.

What to test, in what order, before the dryer runs under power, and before it runs with heat. Do the stages in order. Do not skip a stage because the previous one went well. Every line is a box to tick; a line you cannot tick is a line you stop at.

Names like S1, X4:1, J1.11, and K_MOTOR are the ones in `electrical/wiring/common-power-module.md` and on the labels inside the power module. Voltages are DC unless they say AC.

## Before you start

- [ ] You have read the risk statement in `README.md` and you accept it.
- [ ] A second person is within earshot for stages 2 onward.
- [ ] Tools: a multimeter that reads continuity, ohms, DC volts, and AC volts; a clamp ammeter (strongly recommended for stage 4); insulated screwdrivers; a heat gun; a flashlight; the UCI test plug (appendix A).
- [ ] The dryer is on its feet, level, and has at least 150 mm of clear space behind it.
- [ ] The cord is not plugged in. The wall receptacle has been checked by someone who knows how: correct type, correct voltage, grounded, on the right breaker.
- [ ] No heat module is fitted. The bay holds the blanking duct. (Every build is commissioned with no heat first, whatever heat it will get.)
- [ ] No control module is fitted. The UCI test plug is in J1.

## Stage 0: mechanical, cord unplugged

- [ ] Drum turns by hand with no scraping, both directions, a full turn.
- [ ] Belt is seated in the drum groove and on the motor pulley, and the idler holds tension through a full turn.
- [ ] Blower wheel turns freely by hand and does not touch the housing.
- [ ] Lint filter seats fully and comes out without tools.
- [ ] Door closes and latches; it opens past 90 degrees without touching anything.
- [ ] With the door closed you hear or feel both door switches actuate (S1 and S2). With a continuity meter at X3:4 to X3:5, S1 reads closed with the door shut and open with the door open. Same at X5:1 to X5:2 for S2.
- [ ] Exhaust duct is connected at the rear port and runs to outside (or, for a no-heat build run indoors, to wherever you decided the lint goes).
- [ ] Every panel is on and bolted. Nothing rattles when you rock the cabinet.

## Stage 1: electrical, cord unplugged

Measure at the plug blades and inside the box with the lid off. "Short" means under 1 ohm. "Open" means over 1 megohm.

Bonding:

- [ ] Plug PE pin to the box ground stud: short.
- [ ] Plug PE pin to each of: rail A, rail B, the barrier, the lid (closed), the frame at four corners, every outer panel, the motor frame, the blower housing, the heater module tray rails, the console panel: short, each one measured separately.
- [ ] 0V bus to the ground stud: short (wire 21). Then lift wire 21 and confirm 0V to ground reads open; refit it. This proves there is exactly one bond.

Isolation, with CB1 on and the door closed:

- [ ] Plug L1 to plug PE: open.
- [ ] Plug N to plug PE: open.
- [ ] Plug L2 to plug PE: open (240 V cord).
- [ ] Plug L1 to plug N: open or over 100 kilohm (the supply's input filter may read high resistance; a reading under 10 kilohm is a fault).
- [ ] X2:1, X2:2, X2:3 to X2:4: open. (Nothing is on the heat module terminals yet.)
- [ ] +24V bus to 0V bus: open or over 10 kilohm.

Wiring:

- [ ] Every wire number from the wire list is present at both ends and lands where the list says. Tick them off on a printed copy.
- [ ] J1 pin 3 to pin 9: a few hundred ohms to a few kilohm (RLY_MOTOR coil). Same for pin 4 and pin 5. Open means a coil is not wired; a short means a wiring fault.
- [ ] J1 pin 11, 12, 13 to pin 9: open.
- [ ] TF2 reads short (X5:5 to X5:6). T_HI and T_LO read short at room temperature (X5:7 to X5:8, X5:9 to X5:10).
- [ ] PS1 reads open at rest (X5:3 to X5:4).
- [ ] Motor leads: X3:1 to X3:2 reads the motor winding (a few ohms); X3:1 to X3:3 reads open.

Thermostat function, with the heat gun on low, before they are mounted if that is easier:

- [ ] Warm T_HI slowly until it clicks; continuity goes open; it closes again as it cools.
- [ ] Same for T_LO. It should open at a lower temperature than T_HI.
- [ ] Do not heat TF2. It is a one-shot device; continuity at room temperature is the only test.

## Stage 2: first power, no heat module, test plug in J1

Lid on the power module, all panels on. All test plug switches off. Plug in.

Rail:

- [ ] Test plug +24V lamp lights. At J1 pin 1 to pin 9 (or at the test plug's test points): 21.6 to 26.4 V.
- [ ] Nothing else happens. No click, no hum, no motor.

Door status:

- [ ] Door open: STAT_DOOR lamp off, X5:2 to 0V reads 0 V.
- [ ] Door closed: STAT_DOOR lamp on, X5:2 reads 21 to 26 V.

Motor and airflow:

- [ ] Door open, MOTOR switch on: nothing happens. (Both S1 and S2 are open. If the motor runs, stop: S1 is bypassed or miswired.)
- [ ] Door closed, MOTOR switch on: K_MOTOR clicks, the motor runs, the drum turns in the direction the drawing shows, air comes out of the exhaust.
- [ ] Within 10 s of the motor starting, STAT_AIRFLOW lamp comes on and X5:4 reads 21 to 26 V. If it never does, PS1 or its tubing is wrong, or the setpoint is above what the blower makes; fix that before anything else.
- [ ] Open the door while running: the motor stops at once and STAT_DOOR goes off. Close the door: the motor starts again (the test plug is still asking; a real control module must not do this, which is tested in stage 3).
- [ ] MOTOR switch off: the motor stops. STAT_AIRFLOW goes off within a few seconds.
- [ ] Cover the lint filter opening with a flat board while the motor runs: STAT_AIRFLOW goes off within a few seconds and comes back when you uncover it. This is the airflow interlock proving it can open.

Heat permission (nothing is connected to X4 yet; you are measuring the permission, not heat):

- [ ] Motor off, HEAT switch on: X4:1 to X4:2 reads 0 V. (No airflow, no permission.)
- [ ] Motor on, air proven, HEAT on: X4:1 reads 21 to 26 V.
- [ ] HEAT off, HEAT_LO on: X4:1 reads 21 to 26 V.
- [ ] HEAT and HEAT_LO both on: X4:1 reads 21 to 26 V. Then warm T_LO with the heat gun until it clicks: X4:1 drops to 0 V even though T_HI is still closed. This proves LOW wins when both are asserted.
- [ ] HEAT on only, warm T_HI until it clicks: X4:1 drops to 0 V; it returns when T_HI cools.
- [ ] Motor on, HEAT on, cover the lint filter opening: X4:1 drops to 0 V while the motor keeps running; it returns when you uncover.
- [ ] Open the door with everything on: motor stops, X4:1 drops to 0 V, STAT_DOOR off.

Shorting test (this is the UCI chassis checklist, section 11, done for real):

- [ ] Unplug the test plug. With the door open, use a jumper to short J1 pin 3, 4, 5 together and to pin 9, all at once. Nothing runs and X4:1 reads 0 V.
- [ ] Same with the door closed: the motor runs and X4:1 reads 24 V once air is proven. Remove the jumper: everything stops.
- [ ] Short pin 11 to pin 9 with the door closed (this is a shorted status line): the PTC trips, nothing else changes, the motor is not affected. Remove the short; within a minute the PTC recovers and STAT_DOOR reads 24 V again.

Unplug the dryer before stage 3.

## Stage 3: the control module, no heat module

Remove the test plug. Fit the control module (Tier 0 is described here; an electronic tier follows its own list in `controls/tier1-basic/` or `controls/tier2-smart/`, which must include every line below).

- [ ] Plug in. Nothing happens.
- [ ] Door open, DRY TIME wound to 10 min, press START: nothing happens.
- [ ] Door closed, DRY TIME at zero, press START: nothing happens.
- [ ] Door closed, DRY TIME 5 min, HEAT switch on AIR, press START: the motor runs.
- [ ] Open the door: the motor stops. Close the door: it stays stopped. Press START: it runs again.
- [ ] Let DRY TIME run out: the motor stops on its own.
- [ ] DRY TIME 5 min, HEAT TIME 2 min, HEAT on HIGH, START: motor runs; X4:1 reads 24 V once air is proven; after about 2 min X4:1 drops to 0 V while the motor keeps running until DRY TIME ends.
- [ ] Same with HEAT on LOW: X4:1 reads 24 V (through T_LO).
- [ ] Mid-cycle, pull the plug for 10 s and plug back in: the dryer stays stopped until START is pressed.

Unplug the dryer before stage 4. If this is a no-heat build, go to stage 5.

## Stage 4: the heat module

Common to every heat module, cord unplugged:

- [ ] The tray is bolted to its rails and bonded to X2:4; tray to the plug PE pin reads short.
- [ ] The module's own limits read short at room temperature (electric: TF1 and T_HL; gas: T_BHL and TF1; heat pump: T_CHL, and FS1 with the float down).
- [ ] X4:1 to X4:2 now reads the module's contactor coil (a few hundred ohms to a few kilohm), not a short.
- [ ] X4:3 to X4:4 reads open.
- [ ] The riser flange and (heat pump) return duct are sealed with their gaskets.

### 4a. Electric

- [ ] Element terminals to the heater box: open, both leads.
- [ ] Element resistance, measured at the element terminals: about 10 to 12 ohms for a 5.0 to 5.6 kW element. Open means a broken element; under 5 ohms means a shorted turn.
- [ ] With the heat gun, warm T_HL until it clicks open and confirm it closes again as it cools. Do this before it is mounted in the box.
- [ ] Plug in. Run stage 3's HIGH test with the lower front panel off and a clamp meter on one element lead: K_HEAT clicks in once air is proven, the element draws about 21 to 24 A at 240 V (nameplate watts divided by your measured voltage), STAT_HEAT_ON lamp comes on (or J1 pin 13 reads 24 V).
- [ ] Exhaust air gets warm within 2 min. Within 15 min T_HI starts cycling: K_HEAT drops and picks up every minute or two. Measure the exhaust air at the duct when T_HI opens: 60 to 70 °C is the design target; write down what you get.
- [ ] Open the door mid-heat: motor and element stop at once.
- [ ] Run a LOW cycle: T_LO cycles at a lower exhaust temperature than T_HI. Write it down.
- [ ] Let the cycle end: heat drops first (HEAT TIME), the motor runs on, then stops.
- [ ] Unplug. Open the box. Nothing is discolored, no terminal is warm to the touch after a minute, no smell.

### 4b. Gas

Read this first: connecting a gas line and the first light may legally require a licensed person where you live. If you are not certain you are allowed to do this, and certain you know how, stop here and get that person. A CO detector in the room is required for every run in this stage.

- [ ] Gas type matches the burner's orifice (natural gas as supplied, or the LP conversion kit fitted and the regulator set per the kit).
- [ ] Shutoff valve outside the cabinet, flexible connector, every joint leak-tested with soap solution with the supply on and the dryer unplugged. No bubbles, anywhere, for a full minute.
- [ ] Exhaust duct runs to outside. No exception for gas.
- [ ] Plug in. Run stage 3's HIGH test with the lower front panel off so you can see the burner: the igniter glows within about 30 s, the valve clicks, the burner lights with a blue flame, STAT_HEAT_ON comes on (the valve relay). Yellow or lifting flame: stop, and check the orifice, the combustion air, and the gas type.
- [ ] Close the manual shutoff while it burns: the flame goes out, STAT_HEAT_ON drops, the igniter glows again (trial), nothing smells of gas. Open the shutoff: it relights on its own within a minute or two. (This is the flame sensor doing its job. If gas keeps flowing with no flame, pull the plug and close the valve; the burner assembly is faulty.)
- [ ] Open the door mid-burn: motor and burner stop at once.
- [ ] T_HI cycles the burner; exhaust temperature at the duct written down, as for electric.
- [ ] A full cycle with the panels on and the CO detector reading zero throughout.

### 4c. Heat pump

- [ ] Sealed unit nameplate: compressor FLA and LRA are within K_COMP's rating and the cord and breaker are right for them.
- [ ] Unit level, drain hose routed with a continuous fall, or the condensate pump wired and its safety switch in the FS1 position, or the tank fitted with its float.
- [ ] Lift the float (or trip the pump's safety switch): X4:1 to X4:2 reads open. Release: it reads the coil again.
- [ ] TMR1 set to 3 to 5 min.
- [ ] Plug in. Run stage 3's HIGH test: X4:1 shows 24 V once air is proven; K_COMP does not pull in until TMR1 expires (watch the clock); then the compressor starts, the clamp meter reads about the nameplate FLA within a few seconds, STAT_HEAT_ON comes on.
- [ ] Stop the cycle and press START again straight away: K_COMP does not pull in until the lockout expires. This is the anti-short-cycle protection.
- [ ] After 10 to 20 min, air out of the riser is warm, air into the evaporator is warmer than the room, and condensate appears at the drain.
- [ ] Open the door mid-cycle: motor and compressor stop at once.
- [ ] A full 2 to 3 h cycle with a real wet load. Write down the compressor current, the drum air temperature, the water collected, and the time.

## Stage 5: before the first real load

- [ ] The ladder drawing and the wire list are in the sleeve inside the power module lid, with your measured temperatures and currents written on them.
- [ ] The lid label is on. The disconnect (the plug) is labeled.
- [ ] `builds/` has a folder for this build with photos of every stage and every number you wrote down.
- [ ] You have told the people who will use this dryer what the risk statement says.

Then dry some towels and see what happens.

## Appendix A: the UCI test plug

A commissioning tool, not a control module. It lets you ask the chassis for things with switches and see what it reports with lamps, with no timers and no electronics to doubt. Build it before stage 2.

| Part | Spec | How many |
| --- | --- | --- |
| Plug housing | Mini-Fit Jr. 16-circuit plug with male crimp terminals (the same parts as the Tier 0 module's plug) | 1 |
| Toggle switches | SPST, panel mount, rated 1 A at 30 V DC or better | 3 (MOTOR, HEAT, HEAT_LO) |
| LEDs | Any color, 5 mm | 4 (+24V, DOOR, AIRFLOW, HEAT_ON) |
| Resistors | 4.7 kilohm, 1/2 W | 4 |
| Box | Any small plastic box | 1 |
| Wire | 20 AWG | about 1 m |

Wiring: pin 9 is 0V and is the common for everything. Each toggle connects one request pin (3, 4, 5) to pin 9. Each lamp is an LED in series with a 4.7 kilohm resistor from its pin (1 for +24V, 11 for DOOR, 12 for AIRFLOW, 13 for HEAT_ON) to pin 9, LED anode toward the pin. Nothing connects to any other pin. Label the switches and lamps.

Rules: it is not a control module and must never be left in a dryer that someone could run. It has no cool-down, no timer, and no idea what the door is doing; the chassis interlocks are what keep stage 2 safe, and stage 2 is written so that you are at the dryer with your hand on the switches the whole time.
