# Maintenance and failure-mode guide

Draft 2, 2026-11-06 (draft 1 2026-11-05). Status: draft 2 adds the exhaust pipe and the two chassis sensors of model draft 9. written from the paper design and from what commonly fails on dryers built from the same parts. The "roughly when" numbers are typical for the appliance market, not measured on this design; the build log and your own notes will correct them.

For every wear part and every subassembly: what fails, roughly when, what it looks or sounds like, how to confirm it, what part to order, and how long the repair takes. Names like K_MOTOR, TF2, and X5:5 are the ones in `electrical/wiring/common-power-module.md` and on the labels inside the power module. Part IDs are from `bom/`.

Unplug the dryer before opening any panel. The plug is the disconnect.

## Quick table: what you see, where to look

| What you see | Look at, in this order |
| --- | --- |
| Nothing happens at all | Wall breaker and plug; CB1; F1; PSU (24 V at J1.1 to J1.9); the control module |
| Runs with the door open | Stop using it. S1 and S2 are both bypassed or miswired, or the door actuator is broken. |
| Will not start, 24 V present | Door switch S2 (STAT_DOOR); the control module (Tier 0: K1, START, DRY TIME timer); RLY_MOTOR; K_MOTOR |
| Motor hums, drum does not turn | Belt off or broken; idler; drum seized on its support |
| Motor runs, no heat, STAT_AIRFLOW never comes on | PS1 and its tube; blower wheel loose on the shaft; lint filter or duct blocked |
| Motor runs, air proven, no heat | TF2; T_HI or T_LO stuck open; RLY_HEAT or RLY_HEAT_LO; the heat module's own limits (TF1, T_HL, T_BHL, T_CHL, FS1, TMR1); K_HEAT or K_COMP; the element, the burner, or the sealed unit |
| Heats, but clothes take much longer than they did | Lint filter; exhaust duct; blower wheel; T_HI opening early (vent restricted); for a heat pump, the secondary filter and the evaporator |
| Heat stops partway through, comes back later | Normal: T_HI or T_LO cycling. If it stops for many minutes with a cold exhaust, the heat module's high-limit is tripping: vent restricted. |
| Thermal fuse keeps blowing | Never just replace it. The vent is restricted, the blower is weak, or the high-limit has failed closed. Find the cause first. |
| Buzzing or chatter from the power module | A contactor or relay coil at low voltage: PSU sagging, a loose terminal, a PTC half-tripped |
| Smell of hot dust the first few runs | Normal for a new element. Any other burning smell: unplug and open the panels. |
| Water on the floor (heat pump) | Drain hose, condensate pump, FS1 not stopping heat when it should |

## Drive and air

### Belt (bom: chassis, to be added when CAD fixes the length)

- What fails: it stretches, glazes, cracks, and finally breaks. Lint between belt and drum wears it faster.
- Roughly when: 8 to 15 years on a commercial dryer; sooner if the idler spring is weak.
- What it looks or sounds like: a squeal at start-up, a drum that slips under a heavy load, then a drum that does not turn while the motor runs.
- How to confirm: front panel off. Look at the belt: cracks across the ribs, a shiny glazed face, or a belt lying in the base.
- What to order: the belt from `bom.csv` by its generic length and rib count; any appliance parts house stocks the common lengths.
- How long: 30 min. Front panel off, drum lifted, belt threaded around the drum, motor pulley, and idler.

### Idler pulley and spring

- What fails: the idler bearing dries out and squeals, the pulley wears a groove, the spring weakens.
- Roughly when: 5 to 10 years.
- What it looks or sounds like: a squeal or rumble that follows drum speed and goes away when the belt is lifted off; belt slipping.
- How to confirm: belt off, spin the idler by hand: it should be silent and free. Wobble means the bearing is gone.
- What to order: the idler assembly or just its bearing (a 6200-series sealed bearing) from `bom.csv`.
- How long: 20 min, with the belt off.

### Motor M1 (bom: CH-M1)

- What fails: bearings first (noise), then the start winding or the built-in thermal protector (will not start, or stops hot).
- Roughly when: 15 to 25 years. A motor that stops after ten minutes and restarts when cool is a protector doing its job: look for a reason (lint in the motor, a dragging drum, a seized blower) before blaming the motor.
- What it looks or sounds like: a rumble that does not change with the belt off; a hum with no rotation (start winding or a seized shaft); a motor that cuts out hot.
- How to confirm: belt off, spin the shaft by hand: rough or noisy means bearings. Hum with no start: try spinning it by hand while powered (carefully, panels off, with the second person at the plug); if it then runs, the start winding or centrifugal switch is the fault. Winding resistance from X3:1 to X3:2 reads a few ohms; open means a winding or the protector.
- What to order: any motor of the same frame, voltage, and rating (`bom.csv` CH-M1). That is the point of a standard frame.
- How long: 1 h. Rear panel off, belt off, blower wheel off the shaft, four mount bolts, three wires at X3.

### Blower wheel and housing

- What fails: lint packs the wheel, the wheel works loose on the shaft, the housing fills with lint behind the wheel.
- Roughly when: lint build-up every 2 to 5 years depending on the filter habits; a loose wheel is a build error that shows up in the first year.
- What it looks or sounds like: weak exhaust, long dry times, PS1 failing to prove (STAT_AIRFLOW never comes on) while the motor runs, a rattle at start and stop.
- How to confirm: rear lower panel off, the clamp on the housing's collar loosened and the pipe slid back a hand's width, look into the blower outlet with a flashlight. Grab the wheel: no play on the shaft.
- What to order: nothing for lint; the wheel and its clamp from `bom.csv` if it is damaged. The housing comes off its four screws on the blower plate (model draft 9) with the front lower panel and the spool out of the way; the plate itself stays.
- How long: 30 min to clean; 45 min to replace the wheel.

### Exhaust pipe and vent (bom: CH-EXHAUST, CH-EXH-CLAMP)

- What fails: lint lines the pipe and the vent hose outside; the spigot's hose clamp loosens; a crushed or sagging vent hose (not ours, but it is the first thing to look at).
- Roughly when: clean every year; more often with a long vent run. A clamp loosens in the first months if it was not snugged after the pipe settled.
- What it looks or sounds like: long dry times, T_HI cycling early, a warm laundry room, lint at the outside hood, PS1 slow to prove.
- How to confirm: outside hood open and a flashlight up the hose; rear lower panel off and the inside clamp loosened, the pipe slid forward off the panel, a flashlight down it.
- What to order: a 4 in pipe cut to the length in `drawings/frame-cut-list.csv` if it is dented; clamps from `bom.csv`.
- How long: 20 min to clean the pipe; 10 min to swap a clamp.

### Exhaust thermistor TH1 and moisture bars (bom: CPM-TH1, CPM-MOIST)

Only a Tier 1 or higher control module uses them; Tier 0 does not read them and runs the same without them.

- What fails: the thermistor drifts or goes open; a moisture bar lead corrodes or a bar glazes with softener residue so a wet load reads dry.
- Roughly when: a decade for the thermistor; the bars glaze in a year of dryer sheets and clean up with vinegar and a cloth.
- What it looks or sounds like: a module with auto-dry ends cycles early with the clothes still damp (bars) or shows a temperature fault (thermistor). Nothing stops; the hardware thermostats hold the temperature whatever the module reads.
- How to confirm: at X6 on the power module with the J2 cable unplugged: the thermistor near 10 kilohm at room temperature and falling as it warms; the bars open with nothing across them and a few hundred kilohm with a damp cloth laid across both. Front upper panel off for the bars' nuts and terminals, front lower panel off for the thermistor on the lint box's back plate.
- What to order: CPM-TH1 or CPM-MOIST. The thermistor is one M4 x 20; the bar set is two M4 x 16 and two spade terminals.
- How long: 20 min either.

### Lint basket

A mesh basket on two laser-cut plates that slides through the curved slot at the bottom of the door opening; the D-pull sits at the bottom of the throat. Pull it 40 mm toward you and lift it out through the door. Push it back in until the lip sits on the bulkhead.

- What fails: the mesh tears or pulls out of its clamps, the pull works loose, fabric softener residue glazes the mesh so air will not pass even when it looks clean.
- Roughly when: 5 to 10 years for the mesh. Glazing shows up in months if dryer sheets are used.
- What it looks or sounds like: longer dry times, T_HI cycling too often, lint getting past the filter into the blower.
- How to confirm: hold the filter under a tap. If water beads on the mesh instead of running through, it is glazed; scrub it with a brush and warm soapy water. Hold it up to the light for tears.
- What to order: a new mesh strip, or the plates from `bom.csv` (CH-LINT); re-clamping the mesh is twelve M3 screws.
- How long: 1 min to clean. No tools. 30 min to re-mesh.

### Drum support rollers and glides (bom: CH-ROLLERS, CH-ROLLER-STUDS, CH-GLIDES)

- What fails: rollers flat-spot and their bores dry out; a stud's nut works loose; a glide pad wears through and the drum walks against a bulkhead.
- Roughly when: 10 to 20 years for the rollers; a loose nut in the first year if it was not torqued; glides 10 to 15 years.
- What it looks or sounds like: a thump once per drum turn (a flat roller), a rumble that changes with load, a drum that is hard to turn by hand with the belt off, a scrape at a ring face (a worn glide).
- How to confirm: belt off, turn the drum by hand: it should coast and have about 1 mm of end play between the glides. Front panel off, look at each roller: flat spots, cracks, play on its stud. Each front stud's nut is in front of the front bulkhead beside the lint duct; the rear ones are behind the rear bulkhead (rear upper panel off).
- What to order: CH-ROLLERS, all four at once; a stud set if a shoulder is scored; glides in pairs.
- How long: 1 h. A roller comes off its stud with the nut, the washer and the spacer; the drum is lifted a few mm with a block under it while that corner is bare.

### Drum sheet, rings, and seam (bom: CH-DRUM-SHEET, CH-DRUM-RINGS, CH-DRUM-HW)

- What fails: a tab bolt or seam bolt works loose; the sheet dents where something hard was dried; a roller track wears a groove in the sheet after many years.
- Roughly when: loose bolts in the first year if they were not torqued; dents whenever; wear at the roller tracks after decades.
- What it looks or sounds like: a tick once per turn (loose bolt or dent passing a roller), a drum that is out of round when you sight along it, lint escaping at a ring.
- How to confirm: front panel off, turn the drum and watch the roller tracks and the seam; put a hand on each tab bolt.
- What to order: hardware from CH-DRUM-HW; a new sheet (CH-DRUM-SHEET) if the wall is damaged, reusing the rings and baffles.
- How long: 20 min for bolts; a day for a new sheet, which is the drum build in the build guide done again.

### Felt seals (bom: CH-FELT)

- What fails: the felt wears thin, lifts at the ends next to the glides, and lets lint and air leak around the drum.
- Roughly when: 10 to 15 years.
- What it looks or sounds like: lint collecting in the base of the cabinet, a scraping sound at the drum edge, longer dry times (air bypassing the drum).
- How to confirm: front panel off (and rear upper panel off for the rear seal); each felt is two arcs with a glide in each gap, and should be continuous between the glides, bonded down, with the ring face riding on it, not on metal.
- What to order: the felt from `bom.csv`, cut to the two arc lengths or the two DXFs.
- How long: 1.5 h, including the adhesive's cure time stated on its tube.

### Door switches S1 and S2 (bom: CPM-S1, CPM-S2)

- What fails: S1's contact pits (it switches the motor), its actuator breaks; S2's lever bends.
- Roughly when: S1 10 to 15 years; S2 should outlast the dryer, but the actuator is in the door's path and takes abuse.
- What it looks or sounds like: the dryer will not start with the door closed (S2 open: STAT_DOOR stays off), or starts and stops when the door is jiggled (S1 intermittent), or runs with the door open (one switch bypassed: stop using the dryer).
- How to confirm: continuity at X3:4 to X3:5 (S1) and X5:1 to X5:2 (S2) with the door open and closed, cord unplugged.
- What to order: CPM-S1 or CPM-S2.
- How long: 20 min. Front panel off, two or three quick-disconnects.

## Common power module

### Air-proving switch PS1 (bom: CPM-PS1)

- What fails: its sensing tube fills with lint or water, its diaphragm stiffens, its contact pits.
- Roughly when: tube blockage every few years; the switch itself 10 to 20 years.
- What it looks or sounds like: motor runs, STAT_AIRFLOW never comes on, no heat ever; or heat drops out at random with a healthy blower.
- How to confirm: pull the tube and blow through it; check the tap on the blower housing is clear. With the motor running, measure X5:3 to X5:4: 0 V across the switch means it is closed (good); 24 V across it means it is open while air is moving.
- What to order: CPM-PS1, same setpoint and pressure direction. Write the setpoint from commissioning on the label.
- How long: 20 min. Rear upper panel off for X5 (the power module is behind it, draft 7), rear lower panel off for the tube on the blower housing.

### Exhaust thermal fuse TF2 (bom: CPM-TF2)

- What fails: it opens once, for good, when the blower housing passes about 91 °C. That is its job. It does not fail on its own.
- Roughly when: never, if the vent is clean. Every time the vent gets restricted enough.
- What it looks or sounds like: motor runs, air proven, no heat, X4:1 reads 0 V, and X5:5 to X5:6 reads open.
- How to confirm: continuity across TF2 with the cord unplugged. Open means blown.
- What to order: CPM-TF2. Buy two. Then clean the duct, the blower, and the filter, and check T_HI and the heat module's high-limit before fitting it, because something let the exhaust get that hot.
- How long: 15 min to replace; 1 h to find out why.

### Cycling thermostats T_HI and T_LO (bom: CPM-T_HI, CPM-T_LO)

- What fails: the disc wears and the setpoint drifts, or the contact sticks open (no heat) or closed (heat regulated only by the high-limit).
- Roughly when: 10 to 20 years.
- What it looks or sounds like: clothes come out cooler than they used to (drifted low), or too hot and the high-limit does the cycling (stuck closed), or no heat on one setting only (one thermostat open).
- How to confirm: cord unplugged, continuity at X5:7 to X5:8 and X5:9 to X5:10 at room temperature: both closed. Heat gun test as in commissioning: each clicks open at about its rating.
- What to order: the same L-rating from `bom.csv`.
- How long: 20 min. Rear panel off, two quick-disconnects, one screw.

### Interface relays RLY_MOTOR, RLY_HEAT, RLY_HEAT_LO (bom: CPM-RLY)

- What fails: contacts pit from switching DC coils; a coil goes open.
- Roughly when: 10 to 20 years of normal cycling; sooner if the contactor coil suppression was never fitted.
- What it looks or sounds like: a request that does nothing (the relay's LED lights but K_MOTOR or the heat module does not pull in: pitted contact), or a request that does nothing and no LED (coil, or the control module is not sinking).
- How to confirm: with the dryer running a cycle, the LED on each relay shows whether its coil is energized. Across the contact (11 to 14) with the coil energized: 0 V means closed.
- What to order: CPM-RLY. They plug into their base; keep one spare in the lid pocket.
- How long: 5 min.

### Motor contactor K_MOTOR (bom: CPM-K_MOTOR)

- What fails: contacts pit and eventually weld or fail to close; the coil goes open.
- Roughly when: 15 to 25 years at a few operations per load.
- What it looks or sounds like: a loud buzz (coil at low voltage or dirty pole faces), a motor that does not start although RLY_MOTOR's LED is on, or a motor that keeps running when it should stop (welded: open the door; S1 still stops it, which is why S1 is there).
- How to confirm: coil voltage at A1 to A2 (24 V when RLY_MOTOR is closed); voltage across pole 1 to 2 with the coil energized (0 V means closed).
- What to order: CPM-K_MOTOR, or the same family's replacement contact set.
- How long: 20 min.

### Power supply PSU (bom: CPM-PSU)

- What fails: its electrolytic capacitors dry out; output sags or ripples, relays chatter, then it dies.
- Roughly when: 10 to 15 years in a warm cabinet.
- What it looks or sounds like: everything dead with the wall breaker on and F1 good; or relays chattering and the control module resetting.
- How to confirm: 120 V AC at its input terminals; 24 V DC at its output. Input present and output missing or low: replace it.
- What to order: CPM-PSU or any listed DIN 24 V supply of 2.5 A or more.
- How long: 15 min. Four wires and a DIN clip.

### Fuses and breaker F1, F2, CB1, PTC1 to PTC3

- What fails: they do their job. F1 opens on a failed PSU; F2 on a shorted control module; CB1 on a motor fault or a short on the 120 V side; a PTC trips on a shorted status line and resets itself when the short is gone.
- What it looks or sounds like: a dead 24 V rail (F1, F2); a dead motor and PSU together (CB1); one status lamp that never lights (PTC).
- How to confirm: continuity across the fuse, the breaker's handle position, 24 V across a PTC (a tripped PTC drops nearly all of it).
- What to order: 5 x 20 mm 2 A T fuses by the card; the same breaker; CPM-PTC.
- How long: 5 min. Then find the reason.

### Terminal blocks and the harness

- What fails: screws relax with heat cycling, a ferrule works loose, a Mini-Fit Jr. contact backs out of its housing.
- Roughly when: check every terminal once a year; the first year is when most relax.
- What it looks or sounds like: intermittent anything, a warm terminal, discoloration on a block, a request or status line that works when the plug is wiggled.
- How to confirm: cord unplugged, go down the wire list with a screwdriver and a tug. On J1, push each wire gently into the housing from the back: a contact that moves is not latched.
- What to order: nothing, usually. Terminals and contacts from `bom.csv` if one is damaged.
- How long: 30 min for the yearly check.

## Electric heat module

### Element R1 (bom: HE-R1)

- What fails: the coil breaks (open), or sags and touches the box (shorted to ground, which trips the breaker).
- Roughly when: 8 to 15 years; sooner if it has been run with restricted airflow.
- What it looks or sounds like: motor runs, air proven, K_HEAT pulls in, no heat, STAT_HEAT_ON stays off with a current switch (or comes on with an auxiliary contact, which is why the current switch is preferred). Or the breaker trips when heat is requested.
- How to confirm: cord unplugged, element resistance at its terminals: 10 to 12 ohms. Open means broken. Any continuity from a terminal to the box means a sagged coil.
- What to order: HE-R1.
- How long: 45 min. Tray out, element box open, two leads, mounting screws.

### Heater box thermal cutoff TF1 and high-limit T_HL (bom: HE-TF1, HE-T_HL)

- What fails: TF1 opens for good when the heater box overheats; T_HL opens and resets as the box overheats and cools, and can eventually fail open.
- Roughly when: only when airflow through the heater box is restricted: a clogged filter, a packed blower, a crushed duct, a sagged element.
- What it looks or sounds like: TF1: no heat ever again until replaced. T_HL: heat comes and goes in long cycles with a cold exhaust, as the box overheats and cools.
- How to confirm: continuity across each at room temperature, cord unplugged.
- What to order: the kit that has both (HE-TF1, HE-T_HL). Fix the airflow first.
- How long: 30 min to replace; the airflow fault is the real job.

### Heater contactor K_HEAT (bom: HE-K_HEAT)

- What fails: as K_MOTOR, but it cycles every time T_HI does, so sooner.
- Roughly when: 10 to 20 years. If it fails before 10, the cycling thermostats move to the element circuit (see `DECISIONS.md`).
- What it looks or sounds like: buzzing; heat requested with air proven and 24 V at A1-A2 but no element current; or heat that will not stop when the request drops (welded: the thermostats and limits still cap it, STAT_HEAT_ON stays on, an electronic tier shows the "unplug it" fault).
- How to confirm: 24 V at A1-A2 when heat is permitted; voltage across each pole with the coil energized.
- What to order: HE-K_HEAT.
- How long: 20 min.

## Gas heat module

### Igniter

- What fails: the silicon carbide bar cracks. It is brittle; it fails from handling as often as from age.
- Roughly when: 5 to 10 years.
- What it looks or sounds like: heat requested, no glow, no flame, STAT_HEAT_ON never comes on.
- How to confirm: cord unplugged, continuity across the igniter: open means cracked. Look at it: a visible crack.
- What to order: the igniter from `heat-gas.csv`. Handle it by the ceramic, never the bar.
- How long: 20 min.

### Radiant flame sensor

- What fails: its contact pits, or it fails open (igniter never glows) or closed (valve never opens).
- Roughly when: 10 to 15 years.
- What it looks or sounds like: igniter never glows (sensor open); igniter glows and glows and the valve never clicks (sensor stuck closed).
- How to confirm: continuity across the sensor cold: closed. Watch the sequence with the lower panel off.
- What to order: the sensor from `heat-gas.csv`.
- How long: 15 min.

### Gas valve coils

- What fails: a coil goes open or weak with heat.
- Roughly when: 10 to 15 years.
- What it looks or sounds like: igniter glows, sensor opens, no valve click, no flame; or the flame lights and goes out a few seconds later, over and over.
- How to confirm: coil resistance per the kit's sheet (each coil reads hundreds to a couple of thousand ohms; open is the usual failure).
- What to order: the coil kit from `heat-gas.csv`. They come as a set.
- How long: 15 min. Two screws, push-on connectors.

### Burner high-limit T_BHL and thermal fuse TF1 (gas)

- As for the electric module: they open when combustion air or exhaust airflow is restricted. The fuse is one-shot. Fix the airflow, then replace.

## Heat pump module

### Secondary lint filter and the evaporator face

- What fails: lint that gets past the drum filter packs the secondary filter, then the evaporator fins.
- Roughly when: the filter every few loads; the fins a few years in if the filter is neglected.
- What it looks or sounds like: dry times grow from 2 h to 4 h; condensate drops off; the condenser outlet high-limit T_CHL starts tripping.
- How to confirm: pull the secondary filter: it should be nearly clean. Look at the evaporator face with a flashlight: fins should be visible, not felted.
- What to order: nothing. Vacuum the filter; brush the fins with the fin direction, gently, with the power off.
- How long: 5 min for the filter; 30 min for the fins.

### Condensate pump and float switch FS1

- What fails: the pump's float sticks or its impeller clogs with lint slime; a tank float sticks.
- Roughly when: yearly cleaning keeps it going; 5 to 10 years for the pump.
- What it looks or sounds like: water on the floor; or heat that stops partway (FS1 open) with a full pan or tank.
- How to confirm: lift the float by hand: FS1 should open (X4:1 to X4:2 open). Pour a cup of water into the pan: the pump should run and clear it.
- What to order: the pump or float from `heat-heatpump.csv`.
- How long: 30 min.

### Anti-short-cycle timer TMR1, compressor contactor K_COMP

- What fails: TMR1 fails open (compressor never starts) or short (no lockout, compressor stalls on restart and its protector trips); K_COMP as any contactor.
- How to confirm: TMR1: after the lockout time, 24 V should pass through it; K_COMP: as K_HEAT.
- What to order: from `heat-heatpump.csv`.
- How long: 20 min each.

### The sealed unit

- What fails: eventually the compressor, or a leak. There is nothing to repair; it is replaced as a unit, which is why the whole module is specified around a replaceable unit.
- What it looks or sounds like: compressor runs and draws current but the loop never warms (lost charge); compressor hums and trips its protector (locked rotor); loud knocking.
- How to confirm: compressor current against the nameplate; temperature rise across the condenser after 20 min.
- What to order: the same unit, or a different one with a new tray drawing and a `DECISIONS.md` entry.
- How long: 2 h and two people.

## Control module, Tier 0

### Spring-wound timers (bom: T0-TMR)

- What fails: the contact pits, the spring weakens, the dial slips.
- Roughly when: 10 to 20 years in household use; they are built for commercial fan duty.
- What it looks or sounds like: the dryer stops early or runs past the setting; a timer that will not wind or winds down too fast; the HEAT TIME knob doing nothing (contact).
- How to confirm: continuity across the timer contact wound versus at zero, module unplugged from J1.
- What to order: T0-TMR, the same range, without HOLD.
- How long: 20 min. Faceplate off, two quick-disconnects, two screws.

### Hold relay K1 and START button

- What fails: K1's contacts pit; the START button's contact block wears or its spring fails.
- What it looks or sounds like: START does nothing with the door closed and time wound (button, K1 coil, or STAT_DOOR); the dryer stops the moment you let go of START (K1 hold contact A).
- How to confirm: 24 V at J1.11 with the door closed; K1 clicks when START is pressed; continuity across contact A with K1 held in.
- What to order: T0-K1 (it plugs into its socket), or the button's contact block.
- How long: 10 min.

## Yearly, with the panels off

- Vacuum the base, the blower housing, the motor, and around the heat module. Lint in the base is the single biggest fire risk in any dryer.
- Check the exhaust duct end to end; replace crushed flexible duct with rigid.
- Tug every terminal and ferrule on the wire list. Look for discoloration.
- Spin the drum, the idler, and the blower by hand with the belt off and listen.
- Look at the felt seals and the rollers.
- Heat pump: brush the evaporator face, clean the pump, pour water through the drain.
- Gas: look at the burner tube for lint, check the flame color at the next cycle, test the CO detector.
- Write the date inside the lid.
