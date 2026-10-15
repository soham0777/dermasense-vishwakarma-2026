# E2: what we must physically measure, and what stays unknown

## A. We must measure these ourselves (nobody can supply them)

| # | Quantity | Instrument | Where it goes | Why we need it |
|---|---|---|---|---|
| 1 | Machine make, controller, tube rating, lens focal length | Nameplate / labels | `../machine_record.md` | Identifies the machine. The "100 W" figure is not yet confirmed |
| 2 | **What "12" means**: which field, what units | LaserCAD layer dialog photo | `e2_session.csv`, `e2_machine_log.csv` | Without it, "12" can't be reproduced anywhere else |
| 3 | Every layer value typed into LaserCAD (min/max power, speed, interval, passes, scan direction, order, focus) | Photo of each dialog | `e2_machine_log.csv` | The exact recipe |
| 4 | Speed of the earlier trial, or S_ref from the speed ladder | Memory/notes, or coupon A-R | `e2_session.csv` | The reference condition |
| 5 | Cut setting for this film | Scrap search (S0-8) | `e2_machine_log.csv` | Holes and outline |
| 6 | Tube current per setting (if there is a mA meter) | Panel meter | `e2_machine_log.csv` (column `tube_current_mA`) | The only physical check on delivered power |
| 7 | Film identity and thickness (5 readings) | Label photo, micrometer | `e2_session.csv` | Material control. CAD assumes 0.125 mm |
| 8 | Room °C, % RH, chiller °C (start/end) | Thermometer, chiller display | `e2_session.csv` | Explains day-to-day differences |
| 9 | Visual grade 0–5, burn-through, photos | Eye + macro photo with a ruler | `e2_visual.csv` | First pass/fail |
| 10 | Resistance of every strip, 3 readings | DMM (2-wire) | `e2_resistance.csv` | Sheet resistance Rs and contact R₀ |
| 11 | Line widths, gaps, hole diameters | Microscope + scale | `e2_linewidth.csv` | Line growth, as-built gap, hole fit → CAD update |
| 12 | Resistance across the gaps, plus bridges seen | DMM (highest range) + microscope | `e2_isolation.csv` | Smallest safe gap between nets |
| 13 | Dowel fit in laser-cut holes | 2.00 mm dowel | `e2_holes.csv` | Strip alignment in the clamp |
| 14 | Meter check against known resistors | DMM + 1 % resistors | `e2_controls.csv` | Trust in every other reading |
| 15 | *(optional)* LIG relief above the film | Micrometer 0.001 mm | `e2_thickness.csv` | CAD assumes 0.02 mm |
| 16 | *(optional)* Saline-drop R across a 1 mm gap | DMM | `e2_wet_check.csv` | First hint that the sensing principle works |

## B. Still unknown after E2 (we must not claim these)

| Unknown | Why E2 can't answer it | What would answer it |
|---|---|---|
| **Is it graphene?** | Resistance and colour don't identify a material | Raman (D, G, 2D bands). Ask the mentor or the IIT Indore SIC |
| Thickness, porosity, morphology | No cross-section imaging | SEM |
| Conductivity (S/m) | Needs thickness | SEM thickness + our Rs |
| Laser power and fluence at the film | The setting is a % command; we have no power meter | Laser power meter, or tube-current calibration from the manufacturer |
| Spot size, exact focus | Not measured | Burn test on card, or the manufacturer's data |
| Effect of scan direction (X vs Y lines) | E2 keeps one orientation (lines along the scan) | A later coupon rotated 90° |
| Behaviour in exudate (wet/dry thresholds, response time, drift) | E2 is dry, apart from an optional DC preview | **E4**: strip on a dressing, simulated exudate, the real reader |
| Contact resistance with pogo pins | E2 uses silver paint or probes | T-CON-01 with the printed clamp |
| Bending durability of the lines | Not tested | T-MECH-01: bend the 1.0 mm lines around a 10 mm radius |
| Long-term stability, humidity and temperature drift | Two days only | Repeat the measurements after 1–4 weeks of storage |
| Biocompatibility / skin safety | Not a lab test we can run | Literature + standards review. The strip doesn't touch the wound bed in our design, but this must be argued, not assumed |
| Batch-to-batch film variation | One film lot | A second lot later |

## C. Assumptions in the design that E2 data will replace

| Assumption today | Where it lives | Replaced by |
|---|---|---|
| Lines print at drawn width (growth 0) | `make_strip.py` F, GAP, MIN_CLEAR | Line growth (11) |
| 0.95 mm clearance is enough | `make_strip.py` MIN_CLEAR | Smallest isolating gap (12) |
| 2.0 mm laser-cut hole fits a 2 mm dowel | `make_strip.py` HOLE_D, CAD | Hole diameter + fit (11, 13) |
| LIG relief 0.02 mm | `5_cad/sw_build.py` strip | (15) |
| Film 0.125 mm | `calc_mechanical.py` film_t | (7) |
| Lead resistance negligible | `6_electronics/calc_readout.py` | Rs (10) × 85 mm lead |
