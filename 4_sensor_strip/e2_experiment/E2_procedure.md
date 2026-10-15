# E2: Can our laser make the strip? (fabrication validation)

**Status:** READY TO RUN. Not performed. No E2 results exist yet (2026-10-14).

**Question:** At the reference setting "12", does our laser make a conductive, LIG-like layer on our film? Does it do so repeatably, on two different days?

We also need four numbers. They decide whether strip v0.1 can be built as drawn (1.0 mm lines, 0.95–1.0 mm gaps, 2.0 mm holes):
1. the smallest line we can trust
2. the smallest gap that stays insulating
3. how much lines grow
4. the size of a laser-cut hole

**Answers we will NOT get from E2:**
- Whether the layer is graphene. That needs Raman.
- Its thickness and porosity. That needs SEM.
- How it behaves in wound fluid. That is E4.

Until Raman is done, we call it a **laser-carbonised conductive layer (LIG-like)**.

**Evidence:** the earlier "12" observation is `[A1]`. Everything E2 produces is `[B]`. Literature values are `[C]` and are for comparison only.

E2 **includes and replaces E1** as Part A: same coupon, same matrix, new sample IDs. The original E1 plan is kept in git history.

---

## What runs when

| Block | File for LaserCAD | Coupons | Time |
|---|---|---|---|
| **S0** Machine and film check, units of "12", cut-setting search, import check | `e2_res_coupon.dxf`, `../lig_test_coupon.dxf` | scrap only (+ A-R if speed unknown) | 45–60 min |
| **Part A** Reference + bracket (power 10/12/14; speed 0.67/1/1.5 × S_ref) | `../lig_test_coupon.dxf` | D1: C1, C2 · D2: C1, C2 | 5 min lasing per coupon + about 45 min measuring |
| **Part B** Resolution, isolation, holes (at the reference setting) | `e2_res_coupon.dxf` | D1: C1, C2 · D2: C1 | 5 min lasing per coupon + about 60 min measuring |
| **Part W** *(optional, last)* Saline-drop preview across a 1.0 mm gap | already-made coupon `E2-B-D2-C1` | none new | 15 min |

**Day 1 and Day 2 must be different days.** That is what tests the day-to-day repeatability.

## Equipment: confirm each item before booking the laser

| Item | Used for | Have it? (model) | If we don't have it |
|---|---|---|---|
| CO₂ laser with LaserCAD V8.28, lab in-charge present | everything | | No session |
| Digital multimeter, **highest resistance range ≥ 20 MΩ** | resistance, isolation | | With a 2 MΩ meter the isolation result is only "> 2 MΩ", which is below our 3 MΩ rule. Mark isolation **inconclusive** and borrow a better meter |
| Optical or stereo microscope with an eyepiece reticle or a 0.01 mm stage micrometer | line width, gap, hole | | Phone macro photo with a steel rule in the frame (about ±0.05 mm). Write "photo" as the instrument |
| Digital micrometer 0.001 mm | film thickness; LIG relief (optional) | | Vernier caliper 0.02 mm for film thickness only; skip LIG relief |
| Silver conductive paint | pad contacts | | Firm probe pressure on the pad centre; write "probe" as the contact method |
| Resistors 100 Ω, 10 kΩ, 1 MΩ (1 %) | meter check | | Buy them (about ₹10 each) |
| 2.00 mm dowel pin, or a 2.00 mm drill bit shank | hole fit | | Use the clamp's actual dowels |
| IPA, lint-free wipes, flat glass/acrylic plate, masking tape, fine marker, Scotch tape | mounting, labels, tape test | | |
| Thermometer/hygrometer | room °C and % RH | | Phone weather app (note it) |
| Part W only: 0.9 % NaCl saline, 20 µL pipette (or a counted drop from a 1 mL syringe), DI water | wet preview | | Skip Part W |

## Step by step

Each step ends with a **check**. If a check fails, stop and write down what happened. A failed check is data, not a reason to improvise.

### S0: before any coupon

| Step | Do | Check |
|---|---|---|
| S0-1 | Go through `E2_safety_checklist.md` section 1 with the lab in-charge. | Signed |
| S0-2 | Fill in `../machine_record.md`: nameplate, controller, tube rating, lens, mA meter, chiller. Photograph the nameplate. | Every field filled in, or marked "not visible" |
| S0-3 | Find how "12" was set. Open a LaserCAD layer, photograph the **Min power** and **Max power** fields and their units, and ask who ran the first trial. Record this in `e2_session.csv` (S0) and `e2_machine_log.csv`. | We know which field "12" goes into and its units |
| S0-4 | Film: photograph the label. Take 5 micrometer readings across the sheet. | Readings within ±0.005 mm of each other, or the spread is noted |
| S0-5 | Exhaust ON: a tissue at the grille is pulled in. Chiller running: write down the water °C. | Both OK |
| S0-6 | **Import check.** Import `e2_res_coupon.dxf`. LaserCAD must show **180.0 × 20.0 mm**, two layers (green = ENGRAVE, blue = CUT), and the 0.30 mm line filled. Import `../lig_test_coupon.dxf`: **237.0 × 20.0 mm** with 6 colour layers plus the black outline. | Sizes and layers as stated. If a size is wrong, fix the import units. **Never rescale by hand.** |
| S0-7 | If there is a mA meter: run the setting → current check from `machine_record.md`. | Values written down (a flickering needle is itself a finding) |
| S0-8 | **Cut-setting search** on scrap of the same film. Cut a 10 × 10 mm square in Cut mode at 20 mm/s. Start at the reference power and add 3 points per attempt until the square drops out cleanly. Stop at 40 and ask the lab in-charge. Log every attempt (`CUTSEARCH` rows). CUT setting = the lowest clean value + 3. | One clean drop-out, recorded |
| S0-9 | **S_ref.** If the speed of the earlier trial is known, use it and write down the source. If not, lase coupon **A-R**: all 6 cells at setting 12, speeds 50/100/150/200/300/400 mm/s. S_ref = the slowest speed that gives continuous black with no holes. | S_ref and its source written in `e2_session.csv` |

### Part A: reference and bracket (`../lig_test_coupon.dxf`)

| Step | Do | Check |
|---|---|---|
| A-1 | Wipe the film with IPA and tape it flat on the plate at the **marked bed corner**. Write the coupon ID by the notch. Photograph it. | No bubbles; ID readable |
| A-2 | Set the layers from the matrix (`e2_sample_matrix.csv`), all in Scan mode, interval 0.1 mm, 1 pass. **Keep the layer order identical on every coupon.** Outline layer: Cut at the CUT setting, or turned off and cut with scissors (write which). Photograph every layer dialog and copy the values into `e2_machine_log.csv`. | Values typed in equal the planned values |
| A-3 | Frame the job to check its position, then run it. **Stay at the machine with the lid closed.** | Job completed without a stop |
| A-4 | Wait until the smoke has cleared, then remove the coupon. Don't touch the black areas. Grade each cell 0–5 and take a macro photo with a ruler (`e2_visual.csv`). | Every cell graded |
| A-5 | Controls (`e2_controls.csv`): shorted leads, open leads, 100 Ω, 10 kΩ, 1 MΩ, un-lased film. | Each resistor within 1 % + meter spec; un-lased film = OL |
| A-6 | Silver paint on every pad; let it dry for at least 10 min. Measure each strip (L08, L16, L24) **3 times**, lifting and re-placing the probes each time (`e2_resistance.csv`). | 3 readings per strip; OL written as OL with its range |
| A-7 | Measure the width of each L16 strip at 3 positions (`e2_linewidth.csv`). | 3 values per strip |
| A-8 | **Last, because it is destructive:** tape test on the L08 strips. Record pass/fail in `e2_visual.csv`. | Recorded |

### Part B: resolution, isolation and holes (`e2_res_coupon.dxf`)

| Step | Do | Check |
|---|---|---|
| B-0 | **Setting rule (decided before testing).** Use the reference (12 @ S_ref). If that day's GREEN cell is not grade 3, use that day's grade-3 cell with the lowest L16 resistance, and write down why. | Setting recorded |
| B-1 | Mount the film as in A-1. ENGRAVE (green) = the setting from B-0. CUT (blue) = the CUT setting. **Engrave first, cut second** (cutting first can let the coupon move). Log both layers. | Two log rows per coupon |
| B-2 | Grade every feature (W030…W150, G020…G150). | Graded |
| B-3 | Silver paint the pads. Measure W030…W150 **3 times** each (`e2_resistance.csv`). | 3 readings each |
| B-4 | **Isolation.** On the highest resistance range, measure between pad A (lower left) and pad B (upper right) of each G pair, 2 readings. Write OL plus the range. Then look at each gap under the microscope for black bridges (`e2_isolation.csv`). | 2 readings + bridge Y/N per gap |
| B-5 | Under the microscope, measure 3 positions on each line and each gap, and 2 perpendicular diameters on each hole H1–H3 (`e2_linewidth.csv`). | All filled in |
| B-6 | For each hole: is it cut through? Does a 2.00 mm dowel slide in, fit tight, or not go in? (`e2_holes.csv`) | Recorded |
| B-7 | *(optional, needs a 0.001 mm micrometer)* 3 readings on the W150 pad and 3 on bare film right next to it (`e2_thickness.csv`). | 6 readings |

### Part W *(optional; Day 2, last; only on `E2-B-D2-C1`, gaps G100 and G150)*

1. Take a dry reading. It should be OL.
2. Put a 20 µL drop of 0.9 % saline across the middle of the gap. Read at 10 s and at 60 s.
3. Blot, rinse with a drop of DI water, blot again, and let it dry for 30 min. Read again.

Record everything in `e2_wet_check.csv`.

**This is only a yes/no preview** of "liquid bridges a 1 mm gap below about 100 kΩ". A DC meter polarises the electrodes, so the reading drifts. Calibration belongs to E4, with the bipolar reader.

## Data handling

- Write on the printed `E2_bench_sheets.pdf` at the bench. Type the values into the matching `e2_*.csv` the same day.
- **Keep the paper sheets.** Scan or photograph them into `../photos/`.
- Raw numbers only: no averaging by hand and no "corrected" values.
- Photos go in `../photos/` named after the sample ID. Never edit an original; edited copies go in `../photos/edited/`.
- Then run:
  - `python analyze_e2.py`. This writes `e2_summary.md`, `e2_plots.png` and `measured_process.json`, but only once real data exists.
  - `python ../../5_cad/verify_cad.py`. This compares the strip CAD with what the laser actually made.

## Decision rules (fixed now, before any data)

| Quantity | Rule |
|---|---|
| **LIG-like layer formed** (Part A cell) | Grade 3 **and** R² ≥ 0.95 for R vs L **and** R(24 mm) < 1 MΩ **and** tape test pass **and** no burn-through |
| **Process window** | Conditions where ≥ 3 of 4 cells meet the rule above |
| **Reference sheet resistance Rs** | Median of the 8 GREEN/MAGENTA cells (fit R = Rs·L/W + R₀, using the measured W) |
| **Repeatability (CV of Rs)** | ≤ 20 % reproducible · 20–40 % marginal · > 40 % not reproducible: check tube current and focus before any sensor work |
| **Line growth** | Median of (measured − drawn) over the 0.8, 1.0 and 1.5 mm lines |
| **Smallest reliable line** | Smallest drawn width (and every wider one) for which every replicate is grade 3, not open, and has Rs within ±30 % of the 1.5 mm line on the same coupon |
| **Smallest isolating gap** | Smallest drawn gap (and every wider one) for which every reading is > 3 MΩ (or OL on a range ≥ 3 MΩ) with no bridge seen. 3 MΩ = 10 × the reader's 300 kΩ "dry" threshold |
| **Strip v0.1 buildable as drawn** | F = 1.0 mm ≥ smallest reliable line · 0.95 mm − growth ≥ smallest isolating gap · Rs × 85 mm / (1.0 + growth) ≤ 10 kΩ · laser-cut hole 2.00–2.10 mm |

If any strip rule fails:
1. Change the parameters in `../make_strip.py` (F, GAP, MIN_CLEAR, hole compensation).
2. Regenerate the strip files and rebuild the CAD (`5_cad/sw_build.py`).
3. Run `verify_cad.py` again.
4. Log the decision in `3_decisions/decisions.md`.

Rs much higher than the literature (tens of Ω/sq, Lin 2014 `[C1]`) is **not** a failure. It is our honest number.
