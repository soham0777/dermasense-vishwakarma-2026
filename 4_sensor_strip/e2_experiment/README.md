# E2: fabrication validation (current experiment)

**Status: ready to run, not performed.** No E2 data exists yet; every data file is a pre-filled template.

**Read first:**
1. `E2_procedure.md`: steps, checks, decision rules
2. `E2_safety_checklist.md`: tick it every session
3. `E2_measurements_and_unknowns.md`: what we measure, and what stays unknown

| File | What it is |
|---|---|
| `e2_res_coupon.dxf` / `.png` / `_features.csv` | Part B coupon (180 × 20 mm): 5 line widths, 6 isolation gaps, 3 cut holes. Made by `make_e2_coupon.py` |
| `../lig_test_coupon.dxf` | Part A coupon (existing): 6 colour cells × 3 strip lengths |
| `e2_sample_matrix.csv` | All 72 planned samples with their settings (pre-registered) |
| `E2_bench_sheets.pdf` | Printable sheets (17 pages, A4 landscape) to write on at the bench |
| `e2_session.csv`, `e2_machine_log.csv` | Session, film and **exact LaserCAD settings** log |
| `e2_resistance.csv`, `e2_linewidth.csv`, `e2_isolation.csv`, `e2_visual.csv`, `e2_holes.csv`, `e2_controls.csv`, `e2_thickness.csv`, `e2_wet_check.csv` | Raw data, one row per reading, pre-filled with sample IDs |
| `make_e2_sheets.py` | Regenerates the matrix, CSV templates and PDF. It refuses to overwrite a CSV that already has data |
| `analyze_e2.py` | Fits sheet resistance, applies the decision rules, writes `e2_summary.md`, `e2_plots.png` and (only with real data) `measured_process.json` |
| `test_analyze_e2.py` | Tests the analysis on **synthetic** data in a temporary folder (`python -m pytest test_analyze_e2.py -q`) |

**After the measurements:**
1. Type the data into the CSVs.
2. Run `python analyze_e2.py`.
3. Run `python ../../5_cad/verify_cad.py`. Its 5 "measured" checks change from BLOCKED to PASS/FAIL.
