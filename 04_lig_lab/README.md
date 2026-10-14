# 04_lig_lab: making and measuring our LIG

**Current experiment: E2 (fabrication validation): see `e2/README.md`.** Status: **ready to run, not yet performed.**
E2 Part A is the E1 plan below (same coupon and matrix) with new sample IDs. The E1 files are kept as the original plan;
new data goes into `e2/`. `verify_laser_files.py` checks every laser DXF before it goes to LaserCAD (`laser_files_check.md`).

*Original E1 plan (superseded by E2 Part A on 2026-10-14):* reproducing and bracketing the earlier "setting 12" observation.

| File | What it is | When |
|---|---|---|
| `machine_record.md` | Machine and film identification form (Session 0) | First, at the machine |
| `E1_protocol.md` | The full experiment: matrix, labels, controls, measurements, decision rules, safety | Read before the session |
| `lig_test_coupon.dxf` / `make_test_pattern.py` | Test coupon: 6 colour cells × 3 strips (2 mm wide; 8 / 16 / 24 mm long; 4 mm pads). Each colour gets its own power and speed in LaserCAD | Import into LaserCAD |
| `e1_samples.csv` | **Pre-filled** planned cells (labels, settings); fill in the measured columns | During and after lasing |
| `e1_resistance.csv` | Every multimeter reading (3 per strip) | After lasing |
| `e1_linewidth.csv` | Strip width readings under the microscope | After lasing |
| `e1_controls.csv` | Un-lased film + reference-resistor checks | Every session |
| `e1_setting_current.csv` | Setting → tube current (if the machine has a mA meter) | Session 0 |
| `analyze_e1.py` | Computes sheet resistance (transmission-line fit), applies the pre-registered rules, reports CV, makes plots | After data entry |
| `photos/` | **Original** photos only. Edited copies go in `photos/edited/` | Always |

**Order:**
1. `machine_record.md`
2. Coupon E1-R, only if the earlier speed is unknown
3. Day 1: coupons C1, C2
4. Measure
5. Day 2: coupons C1, C2
6. Measure
7. `python analyze_e1.py`

**What E1 can and cannot show:**
- **Can show:** sheet resistance, line growth, adhesion, and run-to-run / day-to-day repeatability.
- **Cannot show:** that the layer is graphene (that needs Raman), its morphology or thickness (SEM), or its conductivity (that needs thickness).
- Report it as a **"laser-carbonised conductive layer (LIG-like)"** until Raman is done.
