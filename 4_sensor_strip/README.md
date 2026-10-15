# 4_sensor_strip: strip design, laser files, E2 experiment

| File | What it is |
|---|---|
| `make_strip.py` | Generates the strip: `strip_v0_1.dxf` (laser job), `strip_v0_1_encap.dxf` (seal tape), `strip_v0_1_geometry.json` (shared with the CAD), `strip_v0_1_drc.txt` (design-rule check), `strip_v0_1_drawing.png` |
| `make_test_pattern.py` → `lig_test_coupon.dxf` | Test coupon: 6 colour cells × 3 strips; used in E2 Part A |
| `verify_laser_files.py` → `laser_files_check.md` | Checks every DXF before it goes to LaserCAD (35/35 pass) |
| `machine_record.md` | Form for recording the machine and film at the laser |
| `e2_experiment/` | **E2 fabrication validation, ready to run.** Start with its `README.md` |

**Status:** designed and checked in software. **Nothing has been lased yet.**
