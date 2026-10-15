# 5_cad: SolidWorks models of the bench prototype (v0.1)

| File | What it is |
|---|---|
| `solidworks/` | 9 parts, the bench assembly, 7 A3 drawings (`.SLDDRW` + PDF), STEP files, renders, `build_log.txt` |
| `sw_build.py` | Builds every model and drawing in SolidWorks from `../4_sensor_strip/strip_v0_1_geometry.json` and `calc_mechanical.py` |
| `verify_cad.py` → `verify_cad_report.md` | Re-opens every file and checks units, volumes, positions, interference and drawings (99 pass, 0 fail, 5 waiting for E2 data) |
| `calc_mechanical.py` → `calc_mechanical_report.md` | Hand calculations: pin force, lid deflection, tolerance stack, bending strain |

**Status:** v0.1 drawings are **PROVISIONAL**: strip dimensions are updated after E2.
