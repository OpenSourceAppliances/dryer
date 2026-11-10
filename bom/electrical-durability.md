# Electrical parts and their durability

Checked 2026-11-09 against the makers' datasheets, for the electric reference build with Tier 0 controls. The part lines in `bom.csv` and `heat-electric-240.csv` carry the same notes.

Good electrical parts are still made. Industrial control gear from Schneider, Siemens, Eaton, ABB, Omron, Finder, Phoenix Contact, Honeywell and Molex is sold with published life ratings, in operations, from type testing. Those figures are below. The bad parts are mostly unbranded, and counterfeit copies of the real brands sold through marketplaces.

So the rule is where you buy: an authorized distributor (Digi-Key, Mouser, Newark, RS, AutomationDirect, Grainger, or a local electrical wholesaler), never Amazon, eBay or AliExpress for anything in the safety chain. A counterfeit contactor looks the same and has none of the testing behind the numbers.

The design also buys durability by running parts well under their ratings: the heater contactor carries 70 percent of its rating, and the relays and thermostats switch only contactor coils of a fraction of an amp. A contact's life goes up sharply as its load goes down.

What this is and is not: every figure below is the maker's own rating from their current datasheet, checked 2026-11-09. It is not a test of these parts in this dryer. That happens at the bench checks (V-201 to V-204) and the test run.

Duty assumed for the life figures: 5 loads a week (260 a year), one motor start per load, and the heat cycling on its thermostat up to 40 times a load (about 10,400 heater contactor operations a year).

## Switching: what wears out in most appliances

| Line | Part | Pick | Maker's rating | Duty here | Life at that duty | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| HE-K_HEAT | Heater contactor | Schneider LC1D18BD (TeSys Deca, 24 V DC coil) | 32 A AC-1; 30 million operations mechanical; 1 million at full 32 A; coil suppression built in; -40 to 60 C; UL 508, CSA ([datasheet](https://www.mouser.com/datasheet/3/187/9/LC1D18BD_document.pdf)) | Element draws 22.5 A (70 % of rating), about 10,400 operations a year | About 100 years at full rated current; longer at 70 % | Outlasts the machine |
| CPM-K_MOTOR | Motor contactor | Schneider LP4K0910BW3 (TeSys K, 24 V DC low-consumption coil) | 9 A AC-3; 30 million mechanical; 1.3 million at 9 A AC-3; suppressor built in; 1.8 W coil; -25 to 50 C; UL, CSA ([datasheet](https://www.mouser.com/datasheet/3/187/5/a145dea301aee1e11585acdf254d169cf17baf49.pdf)) | 1/3 hp motor, about 6 A typical (nameplate at V-106); 1 to 2 starts a load. Its 50 C ambient limit is the tightest of any part here: the power module's air temperature is measured in the test run | Effectively never wears out at this duty | Outlasts the machine |
| CPM-RLY | Interface relays (3) | Finder 38.51.7.024.0050 (6.2 mm DIN module) | 6 A; 10 million mechanical; 60,000 at full 6 A resistive; -40 to 70 C ([datasheet](https://docs.rs-online.com/8af8/A700000013600345.pdf)) | Each switches a contactor coil of 0.08 to 0.23 A at 24 V, about once a load | Far beyond the machine: at a few percent of rating, life approaches the 10 million mechanical figure | Outlasts the machine |
| T0-K1 | Tier 0 hold relay | Omron MY2N-D2 DC24 (S) (catalogue MY2N-D2-GS) in a PYFZ-08-E socket | 50 million mechanical; coil 37.7 mA at 24 V; -40 to 70 C; UL 508, CSA ([datasheet](https://www.ia.omron.com/data_pdf/cat/my-gs_ds_e_8_1_csm1051922.pdf)) | Once a load, small SELV loads | Effectively never wears out | Outlasts the machine |
| T0-SW | HEAT selector | Schneider XB4BD33 (22 mm, 3 positions, metal bezel) | 1 million operations mechanical and electrical (DC-13 0.5 A 24 V); IP66/67/69K; -40 to 70 C; UL, CSA ([datasheet](https://www.mouser.com/datasheet/2/357/Harmony_XB4_XB4BD33-1782419.pdf)) | Turned once or twice a load | Hundreds of years of turning | Outlasts the machine |
| T0-START | START button | Schneider XB4BA31 (22 mm, metal bezel) | 10 million mechanical; 1 million electrical; IP66/67/69K; -40 to 70 C; UL, CSA ([datasheet](https://www.stoneway.com/resources/Square-D---Schneider-Electric/XB4BA31/Specification-Sheet.pdf)) | Pressed once a load | Effectively never wears out | Outlasts the machine |
| CPM-S2 | Door switch, SELV contact | Honeywell MICRO SWITCH V7 series, roller lever, 6.3 mm tabs | Up to 10 million mechanical; -40 to 85 C; UL, CSA, ENEC ([datasheet](https://www.mouser.com/datasheet/2/187/SIOT-MICROSWITCH-V7-Basic-DTS-EN-LTR-V4-1119_00498-740331.pdf)) | 2 to 4 door openings a load | Effectively never wears out | Outlasts the machine |
| CPM-PS1 | Air-proving switch | Cleveland Controls NS2 series (black spring, 0.10 to 0.30 in w.c.) | 100,000 cycles minimum; SPDT fine silver contacts; -40 to 88 C; UL, cUL; field adjustable ([datasheet](https://assets.kele.com/Catalog/19%20Pressure/PDFs/NS2-0000-xx%20Data%20Sheet.pdf)) | Once a load (closes when the blower runs) | About 380 years at once a load | Outlasts the machine |

## Timers and thermostats: the parts meant to be replaced

| Line | Part | Pick | Maker's rating | Duty here | Life at that duty | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| T0-TMR | Timers (2) | Intermatic FD2HW (2 h, no hold, wall-device yoke) | 20 A at 125 V resistive, 1 hp at 125 V; UL, CSA; 1-year warranty; no published cycle life ([datasheet](https://assets.kele.com/Catalog/12%20Lighting%20Controls/PDFs/FD%20Decorator%20Series%20Catalog%20Page.pdf)) | Wound once a load each | Not published. Treat as a wear part: sold by every electrical supplier, swapped in minutes | Wear part, replace |
| CPM-T_HI, CPM-T_LO | Cycling thermostats | Bimetal disc, L155-25 and L135-25, 6.3 mm tabs (Therm-O-Disc 60T style, or the OEM part) | Therm-O-Disc 60T: 100,000 cycles at its full 25 A rating; UL and CSA recognized; made for clothes dryers ([datasheet](https://literature.neuco.com/b1370155.pdf)) | Switches only the heater contactor coil (0.23 A at 24 V), up to 40 cycles a load | About 10 years on the full-load figure; longer at this tiny load. Keep a spare | Wear part, replace |
| HE-TF1, CPM-TF2, HE-T_HL | Thermal fuses and high-limit | OEM Whirlpool parts (279816 kit, WP3392519) or Supco/ERP equivalents | Not yet checked against a maker's sheet | Never operate in normal running; they open only on a fault | Last until a fault; replace after any trip | Not yet checked |
| HE-R1 | Heating element | OEM Whirlpool 279838 (5400 W, 240 V) | Not yet checked against a maker's sheet | Every heated load | A wear part in every dryer; open coil, replaceable without tools beyond a nut driver | Wear part, replace |

## Power and protection

| Line | Part | Pick | Maker's rating | Duty here | Life at that duty | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| CPM-PSU | 24 V power supply | Mean Well HDR-60-24 (60 W, DIN rail) | MTBF over 500,000 h (Telcordia SR-332); -30 to 70 C; convection cooled, no fan; UL 62368-1, UL 508 ([datasheet](https://files.trcelectronics.com/datasheets/hdr60.pdf)) | About 10 W of its 60 W: coils, relays, the K1 hold | Runs cool and lightly loaded, which is what keeps a supply's capacitors alive | Outlasts the machine |
| CPM-CB1 | 120 V breaker | Eaton FAZ-C10/1-SP (FAZ, 10 A, C curve) | UL 1077 supplementary protector, CSA C22.2 No. 235, IEC 60947-2, 277 V (Digi-Key listing, 2026-11-09) | Carries the motor side; trips only on a fault | Operates only on a fault | Outlasts the machine |

## Connections

| Line | Part | Pick | Maker's rating | Duty here | Life at that duty | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| CPM-X1 to X6, HE-X | Terminal blocks | Phoenix Contact UK 6 N and UK 2.5 N families | UK 6 N: 41 A IEC, 50 A 600 V UL, 24 to 8 AWG, cULus recognized, -60 to 110 C ([datasheet](https://www.phoenixcontact.com/us/products/3004524/pdf)) | Static; the 10 AWG cord and heater wiring is 30 A | No moving parts; retighten at the yearly check | Outlasts the machine |
| UCI-J1, T0-PLUG | Control module connector | Molex Mini-Fit Jr. 16-circuit (5557/5559 housings, 5556/5558 terminals) | 600 V; 6 A per circuit at 18 AWG in a 16-way; 30 mating cycles; -40 to 105 C; UL, CSA ([datasheet](https://www.digikey.hk/htmldatasheets/production/1302087/0/0/1/87427-5557-5556-product-spec.html)) | Unplugged only when a control module is swapped | 30 swaps is decades of use; the terminals are cheap to re-crimp | Outlasts the machine |

## Corrections made to the BOM while checking

- CPM-K_MOTOR: Corrected: the BOM said LC1K0910BD, which does not exist (Schneider's DC-coil TeSys K is LP1K or LP4K). LP4K adds the built-in suppressor and triples the mechanical life.
- T0-K1: Corrected socket: PYF08A-E is not in Omron's catalogue; PYFZ-08-E (10 A, -55 to 70 C) replaces it.
- T0-SW: Corrected: the XB4BD33 already has its two NO contacts; the BOM listed two extra ZBE101 blocks.
- CPM-CB1: Changed the first choice: the BOM led with ABB S201-C10, an IEC part that is not the North American listed version. Changed again on 2026-11-09: the Eaton WMZT1C10 picked here is listed as discontinued, and it is UL 1077, not UL 489 as this record first said. The pick is now Eaton FAZ-C10/1-SP, the same FAZ breaker, UL 1077, which is what the spec asks for. For a UL 489 breaker use FAZ-C10/1-NA-SP.

## Not yet checked

Not yet checked against a maker's datasheet: the second-source lines (Dinkle, Wago, Siemens, Eaton M22, Finder 55.32), the fuse terminals and fuses, the PTC fuses, the door switch S1 (OEM 3406107), the thermal fuses, high-limit and element (OEM Whirlpool numbers), the exhaust thermistor and moisture bars, the current switch HE-CS1, the JST XH sensor connector, the cords, wire and crimp terminals. These are common listed parts, but the record does not vouch for them until each is checked.
