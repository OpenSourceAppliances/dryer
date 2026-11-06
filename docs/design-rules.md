# Dryer design rules

Draft 6, 2026-11-06. Status: proposed, not yet reviewed against a real build.

Changes in draft 6: the three findings of draft 5 are settled (`DECISIONS.md`, 2026-11-06). The drum rings' bore grows from 480 to 540 and the lint slot becomes a curved slot inside that bore, below the 460 door opening, so the front felt fits and both seals are drawn (7a Bulkheads, 7b). The heat module leaves by the back: the riser's bottom rises to 230, with a hood over the module's outlet, and the cord enters through the base pan instead of the rear lower panel (7a Air, 7a Panels, 7 Access). The console is a 200 mm box across the rear of the top on its own small 4040 frame, deep enough for the whole UCI-D envelope (7a Console). Every M4 is a button head with a hex socket (section 8). The Tier 0 faceplate moves its 22 mm devices up and K1's rail down so K1 stays inside the aperture (`controls/tier0-mechanical`). The feet grow to 18 mm under the pan for the cord.

Changes in draft 3: the mechanical architecture is decided (section 7a) and exists as a parametric model in `mechanical/cad/osa_dryer_cad.py`; the drum is made by the builder from a laser-cut sheet on two laser-cut rings (section 7b); drum 620 mm; the verification plan (`docs/verification.md`) is the gate structure for building this fully on paper and then once for real.

Changes in draft 5: the model now draws what this document already called for but had only implied: the T-slot profiles of every extrusion, 6 mm corner radii on every plate (3 mm on the cheeks, the splice and the tabs), every panel bolt (M6 x 12 hex with washer into a T-nut), the four leveling feet, the belt on its real path with the flat idler, its arm and spring, the door's two flag hinges, handle, seal and catch with their screws, the ring's eight M4 bolts, the Tier 0 control module (faceplate, timers, knobs, selector, START, K1), the rear felt seal, the cord bushing, and the detail of the motor, pulley and blower. Drawing the belt showed that a single ceiling slot on the centre line cannot pass it; the bay ceiling now has two slots where the runs cross (7a). Drawing the felt showed that the front felt annulus and the lint slot occupy the same band of the front bulkhead, and that the slot's ends lie outside the drum; the front felt is not drawn and the slot waits on a decision (`docs/verification.md` V-010, V-016). The drum's M4 bolts are 8 long, not 10, and the baffle bolts are M6 (the holes were always 6.5).

Changes in draft 4: numbers in 7a and 7b corrected to what the model and the drawings hold after the CAD audit (`mechanical/cad/cad_audit.py`, V-010): inlet field 200 x 130, lint duct 336 x 36, rings' hole circle 299.2, bay ceiling behind the front bulkhead, front and rear panels split at the bottom of the mid rail, belt track on the drum at the pulley, rollers over the rings. The audit also found and fixed a console face plate drawn sloping the wrong way.

Changes in draft 2: the heat source is a module and the builder picks one of four (none, electric, gas, heat pump); the cabinet base is the heat module bay; the heat module interface (section 3.2); the door switch has a contact in the motor line; a note on fastener heads.

The charter sets the rules for every appliance. This document sets the rules for this one. The UCI-D spec (`controls/uci-spec.md`) sets the control interface. CAD, the schematic, the BOM, and the build guide must meet all three. Where this document and the charter disagree, the charter wins unless `DECISIONS.md` records why not.

## 1. One chassis, four heat choices

The chassis (frame, cabinet, drum, drive, blower, console, common power module, control module) is the same whatever makes the heat. The builder picks a heat module. The heat module and the cord are the only things that change.

| Heat choice | What goes in the bay | Supply and cord | What else the builder needs | Dry time, 4 kg cotton (target) | Difficulty | Status |
| --- | --- | --- | --- | --- | --- | --- |
| None | A blanking duct so room air reaches the drum | 120 V, 15 A, NEMA 5-15 | Nothing. Vent outside, or into the room if lint is acceptable there. | Not a target. It is a tumbling fan: line-dry assist, fluffing, airing, pet hair. | Easiest. Every build runs this way first (section 5.1). | Part of every build |
| Electric | Element box, 5.0 to 5.6 kW, thermal fuse, high-limit, contactor | 240 V split phase, 30 A, NEMA 14-30 | A dryer circuit | 45 to 60 min | Easy. The deepest parts market there is. | Reference build |
| Gas | Listed burner assembly (valve, igniter, flame sensor, orifice), burner high-limit, thermal fuse, relay | 120 V, 15 A, NEMA 5-15, plus a gas line | A gas supply with a shutoff, an LP orifice kit on propane, combustion air, and venting outdoors, which is not optional | 45 to 60 min | Moderate. Connecting gas may legally require a licensed person; the builder finds that out before buying anything. | Variant, after the reference build |
| Heat pump | Sealed, pre-charged heat pump unit, compressor contactor, anti-short-cycle timer, condensate pump or tank with float switch, secondary lint filter, return duct | 120 V, 15 or 20 A | A drain or a tank to empty; no vent | 2 to 3 h | Hardest. Depends on a sealed unit being obtainable (section 5.4). No refrigerant work, ever. | Variant, blocked on sourcing |

Rules that follow from the table:

- The reference build is electric. It is the first one built and the one the build guide is written from.
- Every build, whatever its heat choice, is first run with no heat module fitted, during commissioning, to prove the drum, drive, airflow, and interlocks before anything hot goes in.
- A builder may change heat choice later by swapping the module and the cord. Nothing else moves.
- 230 V single-phase (Europe, UK, Australia and elsewhere) is the same chassis with a 230 V motor and a 230 V heat module. It is documented after the reference build works.

## 2. Six blocks

Everything in the dryer belongs to one of these, and each one comes out as a unit.

| Block | What is in it | Expected life | What wears |
| --- | --- | --- | --- |
| Frame and cabinet | T-slot aluminum extrusion or bolted steel angle frame, laser-cut flat panels bolted on, the console, the heat module bay, feet | The life of the building | Nothing. A dented panel is unbolted and a new one cut. |
| Drum and door | Drum, front and rear bulkheads, drum support (rollers or bearings), felt seals, door, door glass or panel, hinge, latch, door switch | Decades | Rollers, bearings, felts, glides, door switch, latch |
| Drive and air | Motor, belt, idler, blower wheel and housing, lint filter, riser duct, exhaust or return duct | Decades for the housings and ducts | Belt, idler bearing, motor (as a whole; it is a catalog part), lint filter |
| Heat module | One of: nothing but a blanking duct; an element box with its limits; a burner assembly with its limits; a sealed heat pump unit with its contactor, timer, and condensate handling. Each on its own tray. | Element: years to decades. Burner: decades, parts by the kit. Heat pump: as long as the sealed unit lasts, then the whole unit. | Element, every fuse and thermostat, igniter, flame sensor, valve coils, compressor contactor, condensate pump |
| Common power module | Terminal block for the cord, 24 V supply, motor contactor, interface relays, air-proving switch, exhaust thermal fuse, cycling thermostats, PTC fuses, harness to J1 and J2, terminals to the heat module | Decades | Contactor contacts, relays, supply (as a whole), thermostats |
| Control module | Whatever is bolted into the UCI-D aperture | Until its technology is gone, then it is replaced by whatever exists | The whole thing, by design |

## 3. Electrical architecture: the interlock chain

This is the part of the design that decides whether the dryer is safe, so it is fixed here before any schematic is drawn. The ladder diagram and the part families are in `controls/uci-spec.md` section 9. This section states the rules behind it.

### 3.1 Rules

1. Every heat module has its own listed limits in series with its heat source, independent of everything else: a one-shot thermal fuse and an auto-reset high-limit for the element and for the burner, both rated for their circuit; the compressor's own thermal protector and a condenser outlet high-limit for the heat pump. No control, relay, or contactor can bypass them. (Charter: every heat source has a non-resettable thermal fuse and a resettable high-limit in series, independent of any control board.)
2. The common power module permits heat through one 24 V terminal, HEAT_EN, which is live only while all of these are closed, in series: the door switch, the air-proving switch, the exhaust thermal fuse, the selected cycling thermostat, and the contact of the interface relay that the control module drives. Every one of those is a plain switch. Opening any one of them removes the permission.
3. The door switch has two contacts. One is in the motor's 120 V line and is rated for the motor, so opening the door opens the motor circuit itself (the charter's hardwired interlock in the mains path). The other gates the 24 V bus that every coil circuit and STAT_DOOR hang from. The motor contactor's coil circuit passes through that bus and the contact of its interface relay. The motor has its own overload: a built-in thermal protector or a separate listed overload relay. No heat module has a door contact in its own mains line, because no door switch is rated for element current; heat is cut by the 24 V bus and by the air-proving switch when the motor stops.
4. Airflow is proven by a switch that senses the blower, not by assuming the motor is turning. With the motor stopped, a broken belt, or a seized blower, no heat module can be energized.
5. Everything the control module touches is 24 V DC or less. There is no mains voltage in the console.
6. The 24 V supply is a listed unit. 0V is bonded to protective earth at one point in the common power module.
7. The cord enters through a strain relief into a terminal block. PE bonds to the frame at that block with a ring terminal and a star washer on bare metal, and every panel and tray that carries anything electrical is bonded to the frame the same way.
8. Wire colors follow the US convention on the mains side (black and red for L1 and L2, white for N, green for PE) and are listed on the wiring drawing. The 24 V side uses its own distinct colors, listed on the same drawing.
9. Mains and the 24 V side are separated inside the common power module and inside every heat module: mains on one side of a barrier or in its own compartment, 24 V on the other. The SELV side never shares a terminal strip with mains.

### 3.2 The heat module interface

The common power module and the heat module meet at one terminal strip and three flanges. This interface is fixed for the dryer family the same way the UCI-D is fixed for controls, so a heat module designed later fits a chassis built earlier.

Electrical, on two DIN terminal strips in the common power module (mains and SELV never share a strip), reached with the rear lower panel off. The full terminal map and wire list are in `electrical/wiring/common-power-module.md`.

| Terminals | What | Rule |
| --- | --- | --- |
| X2:1 to X2:4 (L1, L2, N, PE), on the mains strip | Unswitched mains from the cord terminal block | The heat module carries its own listed switching device (contactor or relay) and its own fuse if its circuit needs one. L2 is live only with a 240 V cord; a 120 V heat module leaves it unconnected. |
| X4:1, X4:2 (HEAT_EN, 0V), on the SELV strip | 24 V DC, up to 1 A, present only while the common chain in rule 2 is closed | The heat module makes heat only while HEAT_EN is present, and only through its own limits (rule 1), which it must have whether or not HEAT_EN is there. The heat module may put more switches in series with HEAT_EN on its side (the heat pump's anti-short-cycle timer, high-limit, and condensate safety switch). |
| X4:3, X4:4 (HEAT_ON_A, HEAT_ON_B), on the SELV strip | A dry contact from the heat module, closed while it is producing heat, or as close to that as a listed part can sense | The common power module puts 24 V through this contact and a PTC to STAT_HEAT_ON on J1. The source per heat module is listed in `controls/uci-spec.md` 6.3. The "none" module leaves it open. |

Mechanical, in the cabinet base (section 7):

| Flange or feature | What | Rule |
| --- | --- | --- |
| Riser flange | The inlet of the duct that carries air up to the rear bulkhead and into the drum | Fixed position and size, set in CAD. Every heat module's outlet mates to it with a gasket and M6 bolts. |
| Blower outlet flange | 102 mm round, the blower's discharge | Vented modules leave it to the exhaust duct. The heat pump module takes it as the return duct inlet and blanks the rear exhaust port. |
| Tray rails | Two rails in the base that any heat module tray slides onto and bolts to with M6 | The tray is laser-cut flat stock; the heat module is built on it on the bench, then slid in. |
| Air inlet | Louvers in the lower rear and side panels | Vented modules draw room air through them into the module and up the riser. The gas module draws its combustion air through them too. |
| Gas inlet | A 3/8 in NPT entry point in the lower rear panel, blanked on every other build | Gas module only. The shutoff valve is outside the cabinet. |
| Condensate outlet | A grommeted hole in the lower rear panel for a drain hose, blanked on every other build | Heat pump module only. |

### 3.3 Why the cycling thermostats are in the coil circuit (proposed)

Residential dryers put the cycling thermostat in the element circuit, where it switches the full element current. Commercial dryers with contactors put it in the coil circuit. This design proposes the coil circuit because:

- it keeps every temperature control except each heat module's own limits at 24 V,
- it lets the control module select high or low heat through a 24 V relay contact instead of switching element current,
- the thermostats then carry milliamps and last longer,
- it means the same two thermostats serve every heat module, with only their L-ratings changing.

The cost is that the contactor operates every time the thermostat cycles, a few times per load. The contactor is a catalog wear part and gets an entry in the failure-mode guide. If the chosen contactor's rated electrical life does not cover 20 years of that, the thermostats move to the element circuit and this section is rewritten with a `DECISIONS.md` entry. For the heat pump the anti-short-cycle timer sits between the thermostat and the compressor, so the thermostat cannot short-cycle it.

### 3.4 What the control module can and cannot do

Can: start and stop the motor, ask for high or low heat, end heat early, read the door, airflow, and heater state, read temperature and moisture.

Cannot: energize any heat module with the door open, without airflow, past a tripped limit, past the cycling thermostat, or without the motor; keep the motor running with the door open; raise the temperature above the hardware thermostats; restart a compressor against a pressure head; reach mains; tell which heat module is fitted, except by being told in its configuration.

## 4. Common power module rules

- Lives in its own laser-cut steel box, bolted to the frame at the rear of the base, behind the rear lower panel. One panel off gives access to every terminal, relay, and fuse, and to the heat module terminal strip.
- DIN rail inside for the supply, motor contactor, interface relays, PTC holders, and terminal blocks. All catalog, all clip on and off without tools.
- Terminals: screw or spring-clamp DIN terminal blocks for mains, with the cord, motor leads, and heat module leads landing on them with crimped ferrules or ring terminals. No wire is ever cut to remove a part; every lead unplugs or unscrews.
- The harness to J1 and J2 leaves the box through a grommet with strain relief, and is the only thing that goes to the console.
- Thermistor and moisture leads are twisted pairs routed away from the mains harness.
- It is identical for all four heat choices. A no-heat build may omit the heat-enable chain parts (air-proving switch, exhaust thermal fuse, cycling thermostats, RLY_HEAT, RLY_HEAT_LO); the BOM marks those lines "omit only if a heat module will never be fitted". The default is to fit them, so heat can be added later by sliding in a tray.
- The wiring drawing shows physical routing, every wire color, every terminal number, and the torque for the mains terminals.

## 5. Heat modules

Each heat module is built on its own tray, has its own BOM file (`bom/heat-<choice>.csv`), its own wiring diagram, and its own entries in the failure-mode guide. Each must meet 3.1 rule 1 and 3.2 on its own.

### 5.1 None

- The tray carries a blanking duct: a laser-cut sheet box from the louvered inlet to the riser flange, so room air reaches the drum. Nothing electrical.
- This is the first stage of commissioning for every build: the drum turns, the belt tracks, the blower proves airflow, the door stops everything, the control module starts and stops a cycle, and only then does a heat module go in.
- As a finished dryer it is an unheated tumbler. It will not dry a wet load in an evening, and the docs say so. It is the right build for someone who line-dries and wants to soften and de-lint, or who will add heat later.
- A control module at Tier 1 or 2 is configured `heat: none` so it never calls a heat fault. Tier 0 needs nothing; its HEAT switch does nothing and its docs say so.

### 5.2 Electric

- Element 5.0 to 5.6 kW at 240 V, open coil in a steel box, switched on both poles by a contactor in the module.
- The heater-box thermal fuse and high-limit are in the element's mains path, rated for the element current.
- Preferred box: an appliance-market heater element assembly (cheap, listed, imperial). Alternative: a laser-cut box with a bought coil on ceramic insulators (metric, but the mounting is our design and the listing covers only the coil).
- Element terminals use rated high-temperature wire and listed terminals.

### 5.3 Gas

- The burner is a listed dryer burner assembly bought as one unit from the appliance market: valve body with its coils, hot surface igniter, radiant flame sensor, orifice, and burner tube. Its parts stay available by the kit for decades. The flame safety is electromechanical and lives in the assembly: the igniter heats through the sensor, the sensor opens when it sees the glow, that opens the valve, and if the flame goes out the sensor closes and the valve closes with it. No board.
- 120 V. The module's relay switches the burner circuit on HEAT_EN. The burner high-limit and a thermal fuse are in that circuit on the burner housing.
- The burner tube is sealed from the lint path. Combustion air comes through the cabinet louvers; the cabinet is lint-managed (section 7) because lint reaching a burner is the classic dryer fire.
- Natural gas by default, LP by the maker's conversion kit (orifice and regulator setting). The docs say which and how to tell.
- The gas connection: a shutoff valve outside the cabinet, a listed flexible connector, a leak test with soap solution before the first light. Many places require a licensed person to connect gas; the build guide says so in the first paragraph of the gas section, and the builder is responsible for finding out.
- Venting outdoors is mandatory for gas. The docs do not describe any other arrangement.
- STAT_HEAT_ON comes from a relay with a 120 V coil wired across the gas valve, so the control module sees "valve open", which is as close to "flame" as a listed part gets without a flame rod.

### 5.4 Heat pump

Rules:

- The refrigeration circuit is a sealed, pre-charged unit bought as one part and never opened. No brazing, no charging, no refrigerant handling. (Charter decision on the fridge: refrigerant loops are not hobbyist work. In the US, handling refrigerant also needs certification.)
- The compressor is fixed-speed and driven by a contactor from HEAT_EN through an anti-short-cycle timer. An inverter-driven compressor is not acceptable, because the inverter is the OEM's board: firmware and a single source in the heat path, which breaks the Tier 0 rule.
- Closed air loop: blower outlet, return duct, evaporator (air is cooled and the water condenses out), condenser (air is reheated), riser, drum, lint filter, blower. The rear exhaust port is blanked. Nothing is vented.
- A secondary fine lint filter sits at the evaporator inlet and is reachable by the person without tools, because lint on the evaporator is what kills heat pump dryers.
- Condensate goes to a drain hose through the rear panel, or to a condensate pump with a safety switch, or to a removable tank with a float switch. The float or safety switch is in series with HEAT_EN on the module side: a full tank or a failed pump stops heat without a board. (Charter, wet appliances: a float switch that cuts the fill without a board; this is the dryer's version of it.)
- A condenser outlet high-limit thermostat is in series with HEAT_EN on the module side, in addition to the compressor's own protector and any high-pressure switch the sealed unit has.
- Weight: a sealed unit is 20 to 35 kg. The tray and rails are sized for it, and the build guide says it is a two-person lift.
- The cycling thermostats for this module are a lower L-rating than for electric, chosen when the unit is known.

What is known about sourcing, as of this draft: Whirlpool lists the heat pump unit of its WHD560CHW family of 24 in dryers as a repair part (W11551760), and GE lists the heat pump module of its combination washer-dryer (WE03X36780). Both are single-source OEM assemblies tied to one model family. Whether their compressors are fixed-speed (usable here) or inverter-driven (not usable), what refrigerant they hold, what they weigh, how they ship, and what they cost on the day, all need checking against the OEM's own documentation before this module gets past paper. A dehumidifier's sealed unit is the same arrangement (evaporator and condenser in series in one air stream) in a cheap, many-maker package, but a dehumidifier is built for room-temperature air and this loop runs warmer; it is an experiment, not a part, until someone measures one. Until a unit is confirmed, this module is specified in principle and blocked in practice, and the docs say so.

## 6. Controls

- UCI-D as published in `controls/uci-spec.md`. Nothing about the controls is decided anywhere else.
- The control module never knows which heat module is fitted. It asks for heat; the chassis decides. Tier 1 and 2 modules are told the heat choice in their configuration file only so they can set the fault timeout and hide the heat settings on a no-heat build.
- Tier 0 is the reference build: two spring-wound interval timers, a heat selector, a start button, and a hold relay. See `controls/tier0-mechanical/`. Timers of 0 to 2 h suit vented builds, 0 to 4 h a heat pump build.
- Tiers 1 and 2 are built after the Tier 0 dryer dries clothes, not before.
- A screen is a Tier 3 accessory with its own mounting spec on the console or the door, never part of the chassis.

## 7a. Mechanical architecture (decided, modeled)

The whole machine is one parametric model, `mechanical/cad/osa_dryer_cad.py`, which writes every STEP and DXF, the extrusion cut list, and the check views in `mechanical/drawings/`. The numbers below are the model's defaults; a measured part changes a parameter, not a drawing.

| Element | How it is done |
| --- | --- |
| Frame | Four 4040 corner posts, 1000 mm. Three levels of rails: bottom (0 to 40), mid (260 to 300, the bay ceiling), top (960 to 1000). Each level has two side rails (670) and a rear end rail (610); bottom and top have a front end rail (610); the mid level has two front stubs (135 each) with a gap for the lint duct. The mid and top levels each have a rear cross rail (610) at the rear bulkhead. Two 2020 tray rails (360) on the bottom rails. The console's own frame (below) adds four 200 posts, two 610 end rails and two 58.5 side rails. 29 pieces, all square cuts; `drawings/frame-cut-list.csv`. Every piece is drawn with its T-slot profile (a generic 8 mm slot 4040 with a 6.8 centre bore, 6 mm slot 2020 with a 4.2 bore; the bought profile's own drawing governs, V-105), so a bolt in the model sits in a slot and a foot in a bore. The four post bores are tapped M8 at the bottom for the feet. |
| Bulkheads | Two 1.5 mm steel plates, 610 wide, from the mid rails to the top rails. The front one sits behind the front rails and carries the door opening (460), the lint slot (draft 6: a curved slot between radius 238 and 266 about the drum axis, 36 degrees each side of straight down, 8867 mm2; it sits 8 outside the opening and 4 inside the rings' 540 bore, so the air leaves the drum through the rings, not past them) and the glide positions. The rear one sits in front of the rear cross rails and carries the roller shaft holes (at plus and minus 30 degrees below the axis, on the rim radius plus the roller radius) and the air inlet hole field (200 x 130 above the axis: 14 x 9 holes of 10 mm on a 14 mm pitch, 126 holes, inside the ring opening). The rear one passes through a slot in the bay ceiling plate and the front one stands at the plate's front edge, so no lint path exists between the bay and the drum compartment. |
| Bay ceiling | One 1.5 mm plate on the mid rails from 0.5 mm behind the front bulkhead to the back, notched at the rear posts, slotted for the rear bulkhead, cut for the belt (two slots of 40 x 90 at the pulley's Y 402, centred at X -137.9 and X 148.1, where the two belt runs cross the plate: a run from a 30 pulley 200 mm below the drum leaves the drum far from the centre line, so the single slot at X 0 of draft 4 was 138 mm from one run and 148 from the other) and the riser (264 x 54, 2 mm around the duct). In front of the bulkhead the two front stubs and the lint duct close the bay. |
| Drum | Made by the builder: one laser-cut 0.8 mm 304 sheet wrapped around two laser-cut 2 mm rings, a splice strip under a butt seam, three catalog aluminum angle baffles, four catalog dryer rollers. Section 7b. Every piece is flat stock, extrusion, or catalog, and the DXF is the documentation. |
| Drive | A dual-shaft NEMA 48 frame 1/3 hp 1725 rpm motor on the bay floor, axis along the drum, at 120 mm height, on two cradle mounts from a dryer motor mount kit. Blower wheel on the front shaft in a catalog blower housing, inlet facing front, outlet box on its right side turning into the exhaust duct at Y 190. PJ poly-V pulley (5 ribs) on the rear shaft at Y 402, a catalog J-section poly-V belt, 5 ribs, 12 wide: 2232 mm along the drawn path (round the drum on the 40 mm belt track centred on the pulley, 352 from the drum's front edge; down the right run through the right ceiling slot to the pulley; up the left run over the idler and through the left slot), nearest catalog length chosen at V-012. The idler is a catalog 40 mm flat idler pulley on the left (slack) run at X -60, Z 165, on a 25 x 4 aluminium flat bar arm that pivots on an M8 bolt through an angle bracket on the base pan at X -115, Z 25, pulled toward the belt by an extension spring from a post on the arm to a post on a second bracket at X 65; the arm runs from Y 390 to 394, just behind the motor, the belt 396 to 408, the spring 409 to 417, the heat module tray starts at 420. The pulley wraps 120 degrees with the idler where it is drawn; V-105 sets the final idler position from the bought belt. |
| Air, vented | Louvers in the lower panels, heat module tray (Y 420 to 670), the module's outlet collar on its top at the back (240 x 60 at Y 580 to 640, up to 229), the riser's hood over it (300 wide, 28 tall, from Y 560 to the riser, its bottom at 230, its top under the mid rear cross rail), riser (260 x 50, up the back behind the rear bulkhead), inlet field, drum, lint slot, lint duct (336 x 33, between the front panel and the front bulkhead, 5 behind the panel so the ring bolts' nuts and tips clear it, 2 mm from each front stub), transition box, blower, 102 mm exhaust along the bay floor at X 230, 150 high, through a 106 port in the rear lower panel. The hood is what lets the module slide out the back: nothing of the riser reaches below 230. |
| Panels | 1.5 mm steel, flat, 6 mm corner radii, bolted to the extrusion slots with M6 x 12 hex head bolts, flat washers and drop-in T-nuts at 150 mm pitch, every hole on a rail centre line (the model draws every bolt; the T-nuts are not drawn): two side panels, front upper (260 to 1000, door ring opening, bolted to the posts, the mid stubs and the top rail) and lower (0 to 259, 56 louvers of 60 x 5, bolted to the posts and the bottom rail; comes off for the bay), rear upper and lower (the same split; 32 louvers, the 106 exhaust port), top panel (full depth; the console stands on it, so its side rows of bolts stop short of the console posts and four more holes take the console's foot bolts), base pan (with a 22 mm hole at X -250, Y 690, under the power module, for the cord's strain relief bushing: the cord comes up through the pan into the module and runs under the pan to the back, in the 18 mm the feet give). |
| Console | A 200 mm tall box across the rear of the top, from the top rear cross rail (Y 611.5) to the back, on its own small 4040 frame built like the cabinet's: four 200 posts standing on the top panel over the cabinet's top rear cross rail and rear top rail, two 610 end rails and two 58.5 side rails between the posts at the top, twelve catalog inside corner brackets with M6 x 12 hex bolts and T-nuts (the foot brackets bolt down through the top panel into those cabinet rails' top slots, so the console's weight and the push on its knobs go into the frame). Five flat plates bolt to its slots like the cabinet's panels: the vertical face (690 x 200) carrying the UCI-D aperture centred 83 above the top panel (the module's nuts clear the front rail, the faceplate clears the rail's bolts), a cap, a rear plate and two cheeks that continue the rear and side panels. 138.5 deep inside, which holds the UCI-D envelope (240 x 120 x 120 behind the panel plane) with 18 to spare. Total height 1203 on the frame, 1221 on the feet. The Tier 0 module is drawn on the face: faceplate on four M4 button heads, two timers with their yokes and 40 mm skirted knobs, the 22 mm selector and START 20 above the centre line, K1 on its DIN rail segment 24 below it, inside the aperture's projection. |
| Door | 2 mm steel ring (560 outside, 470 inside) bolted to the front panel with eight M4 x 8 button heads on a 257.5 radius, 22.5 degrees off the axes, nuts behind the panel. 2 mm steel disc (540), 8 mm in front of the ring, on two catalog flag hinges at the left: an 8 mm vertical pin at X -278.5, 14 mm in front of the panel, 18 mm knuckles 30 tall at 50 above and 50 below the axis; the pinned halves bolt through the ring and panel with two M6 x 16 countersunk screws each, 14 mm apart (nuts behind the panel), the lift-off halves to the disc with two M4 x 8 button heads from the door's front into tapped leaves (a 2 mm disc cannot take a countersink, and the DXF stays a plain 4.5 hole). A 128 mm D-handle (14 round, 30 standoffs) at X 220, M4 from the back of the disc. A 6 mm OEM seal on the disc's back between radius 237 and 246. A magnetic catch on the ring at X 256 to 268 with its strike on the disc. Opens past 90 degrees (100 in the motion model). No window on the first build. |
| Power module | 170 x 250 x 180 box at the rear left of the bay; the cord comes up through the base pan under it; the heat module tray at the center; the exhaust along the right. |

## 7b. The drum

The drum is the one part the charter's fabrication rule makes hard, so it gets its own section. A cylinder cannot be laser-cut, but a thin sheet can be wrapped: 0.8 mm 304 bent to a 310 mm radius stays elastic (about 0.13 percent strain), so the sheet does not take a set and does not need a roll; it needs something round to hold it. Two laser-cut rings do that.

| Piece | What it is | Drawing |
| --- | --- | --- |
| Sheet | One laser-cut 304 blank, 0.8 mm, 1945.3 x 550 plus 30 tabs on each long edge (24 wide, 16 tall, one 4.5 hole each, 8 mm out from the fold), eight seam holes down each short edge (15 in from the edge, 50 mm pitch from 55 to 455, skipping the belt track at 352 and both 45 mm roller tracks), and three columns (at a sixth, a half and five sixths of the width) of four 6.5 baffle holes at 105, 225, 325 and 445 from the front edge | `mechanical/drawings/drum-sheet.dxf` |
| Rings | Two laser-cut 304 rings, 2 mm, 618.4 outside (the sheet's inside), 540 inside (the drum opening; draft 6, up from 480, so the curved lint slot sits inside the bore and the felt has a 18 mm face to ride on), 30 holes of 4.5 on a 301.2 mm radius for the tabs, 12 degrees apart | `drum-ring.dxf` (cut two) |
| Splice | One laser-cut 304 strip, 1 mm, 60 x 544, holes matching the seam holes | `drum-splice.dxf` |
| Baffles | Three pieces of catalog aluminum angle 40 x 40 x 3, 480 long, drilled on the drill press to the sheet's baffle holes, bolted through the wall at 120 degrees apart | `frame-cut-list.csv` |
| Hardware | M4 x 8 button head bolts, nuts, and washers: 60 for the tabs (the stack is 2 ring + 0.8 tab + 3.2 nut; a 10 mm bolt would stop 0.5 mm from the front bulkhead), 16 for the seam; M6 x 12 button heads and nuts, 12 for the baffles (the baffle holes are 6.5, so the M4 of draft 4 was a misprint); button heads inside the drum, nuts outside, except at the baffles where the angle is inside | |
| Rollers | Four catalog dryer drum rollers with shafts, two on each bulkhead, their faces flush with the drum ends so they run on the sheet's outer surface over the rings; whether a 0.8 mm sheet backed by a 2 mm ring carries the roller load without denting is a V-208 question | |
| Seals | Felt strip, 8 mm, glued to each bulkhead in an annulus between radius 273 and 291, riding on the ring faces outside the 540 bore and inboard of the tabs (the 16 tall tabs start at 293.2); bolt heads sit outside it. Both are drawn: the rear one from Y 602 to 610, the front one from 41.5 to 49.5. The lint slot sits inside the bore (7a Bulkheads), so the front felt and the slot no longer compete (the draft 5 finding, settled in `DECISIONS.md`) | `felt-seal.dxf` (cut two) |

The tab holes are placed for a sharp 90 degree fold at the sheet's inner surface; the hole then lands on the ring's 301.2 radius. A real fold has a small radius, so V-208 checks that the holes line up and the tab height absorbs the bend allowance if they do not. The seam is at the top in the model (12 o'clock), the first tab centre 6 degrees to each side of it, the baffles at 60, 180 and 300 degrees from the seam.

How it goes together: lay the sheet flat, fold every tab inward 90 degrees with a hand seamer, stand the two rings on their edges, wrap the sheet around them with two people, bolt the tabs to the rings working from the seam outward in both directions, close the seam over the splice strip, then fit the baffles. The rings make the ends round; the seam and the tabs hold the middle. The seam goes at the top of the drum in the model only so the drawing is unambiguous; it rotates with the drum.

What is not settled by reasoning and is checked at V-208 before any stainless is cut: how round the wrapped sheet is at mid-length, how much the belt pulls it out of round, and whether 0.8 mm is the right thickness (0.6 wraps more easily and dents more easily). A wrap in 0.5 mm aluminum flashing or heavy card with the real rings answers it for a few dollars.

The no-fabrication alternative, for a builder who will not wrap a sheet: a 55 gallon stainless open-head shipping drum has standardized, published dimensions (572 mm inside, about 1.0 to 1.2 mm wall) from a dozen makers. Cut to length and fitted with a laser-cut front ring, it is a 140 to 155 L drum, a 5 cu ft dryer. The bulkheads are parameters, so it is a parameter change, not a redesign.

## 7. Mechanical targets and rules

Targets, to be fixed in CAD. Anything here that CAD cannot meet comes back to this document and `DECISIONS.md`. `mechanical/drawings/layout-concept.svg` draws these numbers to scale, side and front, so the bay, the drum, and the air path can be argued about before CAD.

| Item | Target or rule |
| --- | --- |
| Outside size | Fits a standard laundry space: about 690 wide, 1203 high (1221 on the feet), 750 deep, including the console, all in mm |
| Capacity | About 6 kg of dry laundry, drum about 165 L (620 mm diameter by 550 mm long as modeled). The 300 mm bay under the drum is what caps it; the measured OEM drum sets the final number and the body height follows it in the model. |
| Frame | 40 series T-slot aluminum extrusion (8 mm slot) as the default. Bolted steel angle is the documented alternative for a builder who cannot get extrusion. No welding anywhere. |
| Panels | Laser-cut flat stock, bolted to the frame with no bends. 1.5 mm steel outside, 1.0 to 1.5 mm inside. Where a bend is unavoidable, it is drawn for an online cut-and-bend service and a flat-and-bolted version is also drawn. |
| Heat module bay | The cabinet base below the drum, full width and depth, about 300 mm high. Tray rails, the riser flange, the blower outlet flange, the louvered inlets, the gas and condensate entries, and the common power module all live here. The rear lower panel comes off to slide a tray in or out (draft 6: the drive sits on the centre line in front of the tray, so the tray leaves by the back, under the riser's hood). |
| Air path, vented | Louvers, heat module, riser duct up the back, rear bulkhead inlet, drum, front lint filter, blower at the base front, exhaust duct through the base, rear port. |
| Air path, heat pump | Blower, return duct, heat module (evaporator then condenser), riser, drum, lint filter, blower. Rear port blanked. |
| Lint management | The lint filter is upstream of the blower and reachable from the front without tools: a curved screen in the front bulkhead's lint slot, below the door opening and inside the rings' bore, lifted out through the open door by a lip that sits inside the opening (the screen and its frame are drawn at V-018). The base is sealed from the drum compartment except through the riser and the lint filter, so lint does not collect around a burner or a compressor. The failure-mode guide has a lint inspection schedule. |
| Drum | Made from a wrapped laser-cut 304 sheet on two laser-cut rings, 620 mm diameter by 550 mm long (about 165 L), 35 mm to each side panel. Section 7b. |
| Drum support | Four catalog dryer drum rollers, two on each bulkhead, 30 degrees each side of bottom, running on the sheet's outer surface where the rings back it. |
| Drum seals | Felt strip glued to the bulkheads in an annulus that rides on the ring faces, replaceable with the front panel off. |
| Drive | Belt drive. A catalog J-section poly-V belt in the nearest standard length, a catalog flat idler on a spring, a PJ poly-V pulley with a 1/2 in bore on the motor's rear shaft. |
| Blower | Catalog blower wheel and housing set, 1/2 in bore, on the motor's front shaft, inlet facing front, fed by the lint duct through a transition box. |
| Door | Laser-cut ring, a glass or stainless panel, a catalog hinge, a catalog latch, and the door switch. Opens past 90 degrees. |
| Console | Part of the cabinet, carrying the UCI-D aperture: a box on its own small frame across the rear of the top (7a), sized to the UCI-D envelope so any module in the family fits without touching the chassis. |
| Feet | Four catalog M8 leveling feet (50 mm pad), screwed into the posts' tapped centre bores through 8.5 holes in the base pan; 18 mm from the floor to the pan with the feet run in, which leaves 3 mm under the cord where it runs under the pan. |
| Access | Door open: lint filter. Front upper panel off: drum front, front felt, front rollers, belt, lint duct. Rear lower panel off: heat module tray (out the back under the riser's hood), heat module terminals, common power module, cord bushing, motor, pulley, idler and belt tension, blower. Front lower panel off: blower inlet, transition box, exhaust duct. Nothing needs two panels off at once. |
| Tolerances | Laser-cut and drill-press tolerances. Nothing tighter than plus or minus 0.5 mm without a reason in `DECISIONS.md`. |

## 8. Fastener budget

The charter allows four fastener sizes per appliance. The dryer's four:

| Size | Head | Tool | Used for |
| --- | --- | --- | --- |
| M8 | Hex | 13 mm socket | Frame joints with T-nuts, motor mount, leveling feet |
| M6 | Hex | 10 mm socket | Panels to frame, brackets, trays to rails, duct flanges, power module box, heater box, door hinge |
| M4 | Button head, hex socket | 2.5 mm hex key | Drum tabs and seam, door ring, hinge lift-off halves, control faceplate, DIN rail, cable clamps, small brackets, sensor mounts |
| M3 | Pan head Phillips | Phillips driver | PCB standoffs inside control modules |

Nylon lock nuts or thread locker on anything that vibrates (motor, blower housing, idler, compressor tray). T-nuts for the extrusion. No rivets, no self-tappers into plastic, no snap fits on anything that opens.

Head types in the model, draft 6: hex head M6 x 12 with washers on every panel and in the console frame's brackets; button head M4 x 8 inside the drum (7b) and on the door ring, M4 x 10 on the faceplate and the hinge lift-off halves, button head M6 x 12 at the baffles; countersunk M6 x 16 at the fixed hinge halves, where a proud head would foul the door. Every M4 is a button head with a 2.5 mm hex socket (`DECISIONS.md` 2026-11-06): one head type, one key, no washer under the small heads inside the drum. The countersunk screws take a 4 mm key. The service set is therefore the charter's four tools plus a 2.5 mm and a 4 mm hex key.

If a bought part comes with its own imperial screws (the spring timers come with 6-32, for example), they are used as supplied and listed in the BOM as "supplied with part".

Charter note: the fastener rule says hex head or socket head, which the button heads are. The charter's service set (10 and 13 mm sockets, a Phillips driver, a multimeter) is a target; this appliance adds two hex keys to it and keeps the Phillips driver for the M3 pan heads inside control modules and for whatever bought parts bring (the timers' 6-32 yoke screws, for example). Recorded in `DECISIONS.md`.

## 9. Performance targets

To be measured on the first build, not promised.

| Item | Target |
| --- | --- |
| Airflow at the exhaust, clean filter, 2 m of straight 102 mm duct, vented builds | 2.5 to 4 m3/min (about 90 to 140 cfm, since blowers are sold that way) |
| Exhaust temperature, electric and gas, high heat, steady state | 60 to 70 °C, set by the high cycling thermostat |
| Exhaust temperature, electric and gas, low heat | 50 to 60 °C, set by the low cycling thermostat |
| Heat input, gas | About 6 kW (20,000 to 22,000 BTU/h, since burners are sold that way) |
| Heat pump loop temperature and compressor power | Unknown until a unit is chosen; typical commercial units run the drum air at 50 to 60 °C on 400 to 700 W of compressor |
| Dry time, 4 kg cotton load from a spin-dried washer | Electric and gas, high heat: 45 to 60 min. Heat pump: 2 to 3 h. None: not a target. |
| Drum speed | 45 to 55 rpm |
| Noise | Not specified. A frame with no thin sheet metal to resonate should be quieter than a commercial dryer; measure and report. |

## 10. What the dryer will not do

- Steam, drum reversal, sanitize cycles, or any function that needs a part the appliance market does not already sell for a basic dryer. A later revision may add any of these through the reserved UCI-D pins.
- Lock the door. Opening the door stops the machine, and that is the whole of the door's safety story.
- Run two heat modules at once (no hybrid heat pump with a booster element). One tray, one module.
- Use an inverter-driven compressor, or any refrigeration circuit that is not bought sealed and charged.
- Anything that needs an account or the internet.

## 11. Open questions for the CAD and electrical phases

Decided in draft 3 and logged in `DECISIONS.md`: the drum (made by the builder from a wrapped sheet on laser-cut rings), the motor (dual-shaft NEMA 48), the drum support (four catalog rollers), the bay height (300, fixed by the drum and the overall height), the riser and lint duct (laser-cut and bolted sheet, drawings to follow the measured parts).

Still open:

1. The drum wrap: roundness at mid-length and the sheet thickness, answered by the cheap-material wrap at V-208 before the stainless is cut.
2. Air proving. Pressure switch against sail switch, tap location, setpoint, lint behavior. V-205 is the bench test; the setpoint cannot be reasoned out.
3. The gas burner assembly family and the heat pump sealed unit, both outside the first build's scope (section 5).
4. Duct details: gaskets, tabs, and clamps for the riser, lint duct, and transition box, drawn once the blower housing is measured (V-107).
5. The motor mount plate and the blower mount, drawn from the measured motor and housing (V-106, V-107).

## 12. Needs a real-world check

- Every rating and typical value quoted for appliance-market fuses, thermostats, burners, and heat pump units anywhere in this repo. They are typical of the US parts market and have not yet been read off a datasheet for a specific part.
- The 30 A circuit and the 14-30 plug are the US norm for an electric dryer, and 15 A on 5-15 for gas and most heat pump dryers. The builder is responsible for their own circuit, receptacle, gas supply, and local code, and the build guide says so.
- Whether an auto-reset high-limit is acceptable under the builder's local code reading, or whether a manual-reset one is wanted. Both are catalog.
- The 20-year contactor life claim in section 3.3, against the chosen contactor's datasheet.
- A listed door switch with a motor-rated contact and a second contact, available from two makers (see `controls/uci-spec.md` section 13).
- Whether the no-heat build needs any airflow interlock at all, and whether leaving the heat-enable chain unfitted changes anything in commissioning.
- Gas: the legal position on connecting gas appliances where the builder lives, before any gas parts are bought.
