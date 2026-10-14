# CAD verification report (verify_cad.py, 2026-10-14 23:38)

**99 PASS · 0 FAIL · 5 BLOCKED · 0 INFO** (run time 51 s).

Expected values are recomputed from `strip_v0_1_geometry.json` and `calc_mechanical.DIMS`, not read from the build script. The measured-data checks stay BLOCKED until E2 data exists.

| Status | Group | Item | Check | Expected | Actual |
|---|---|---|---|---|---|
| PASS | 2 STEP | clamp_base_v0_1.STEP | schema / mm units / solids | AP2xx, mm, >=1 solid | CONFIG_CONTROL_DESIGN, mm, 1  |
| PASS | 2 STEP | clamp_lid_v0_1.STEP | schema / mm units / solids | AP2xx, mm, >=1 solid | CONFIG_CONTROL_DESIGN, mm, 1  |
| PASS | 2 STEP | dermasense_bench_v0_1.STEP | schema / mm units / solids | AP2xx, mm, >=1 solid | CONFIG_CONTROL_DESIGN, mm, 12  |
| PASS | 2 STEP | dowel_2x12.STEP | schema / mm units / solids | AP2xx, mm, >=1 solid | CONFIG_CONTROL_DESIGN, mm, 1  |
| PASS | 2 STEP | dressing_reference_bordered_foam.STEP | schema / mm units / solids | AP2xx, mm, >=1 solid | CONFIG_CONTROL_DESIGN, mm, 1  |
| PASS | 2 STEP | pogo_pin_P75_simplified.STEP | schema / mm units / solids | AP2xx, mm, >=1 solid | CONFIG_CONTROL_DESIGN, mm, 1  |
| PASS | 2 STEP | rig_base_v0_1.STEP | schema / mm units / solids | AP2xx, mm, >=1 solid | CONFIG_CONTROL_DESIGN, mm, 1  |
| PASS | 2 STEP | seal_v0_1.STEP | schema / mm units / solids | AP2xx, mm, >=1 solid | CONFIG_CONTROL_DESIGN, mm, 1  |
| PASS | 2 STEP | strip_v0_1.STEP | schema / mm units / solids | AP2xx, mm, >=1 solid | CONFIG_CONTROL_DESIGN, mm, 4  |
| PASS | 2 STEP | wound_bed_spacer_v0_1.STEP | schema / mm units / solids | AP2xx, mm, >=1 solid | CONFIG_CONTROL_DESIGN, mm, 1  |
| PASS | 4 drawing PDF | strip_v0_1_drawing.PDF | pages / A3 size | 1 page, 420x297 | 1, 420x297  |
| PASS | 4 drawing PDF | strip_v0_1_drawing.PDF | title block / scale / notes | LIG sensing strip, strip_v0_1, SCALE:1:1, PROVISIONAL, First-angle | all present  |
| PASS | 4 drawing PDF | strip_v0_1_drawing.PDF | key dimensions shown | 96.00, 10.00, 0.125, 2.00, 28.24, 16.00 | all present  |
| PASS | 4 drawing PDF | seal_v0_1_drawing.PDF | pages / A3 size | 1 page, 420x297 | 1, 420x297  |
| PASS | 4 drawing PDF | seal_v0_1_drawing.PDF | title block / scale / notes | Seal tape, seal_v0_1, SCALE:1:1, PROVISIONAL, First-angle | all present  |
| PASS | 4 drawing PDF | seal_v0_1_drawing.PDF | key dimensions shown | 73.00, 6.00, 3.90, 0.090, 17.50 | all present  |
| PASS | 4 drawing PDF | clamp_base_v0_1_drawing.PDF | pages / A3 size | 1 page, 420x297 | 1, 420x297  |
| PASS | 4 drawing PDF | clamp_base_v0_1_drawing.PDF | title block / scale / notes | Contact clamp, clamp_base_v0_1, SCALE:2:1, PROVISIONAL, First-angle | all present  |
| PASS | 4 drawing PDF | clamp_base_v0_1_drawing.PDF | key dimensions shown | 26.00, 43.24, 16.00, 1.10, 3.40, 5.08 | all present  |
| PASS | 4 drawing PDF | clamp_lid_v0_1_drawing.PDF | pages / A3 size | 1 page, 420x297 | 1, 420x297  |
| PASS | 4 drawing PDF | clamp_lid_v0_1_drawing.PDF | title block / scale / notes | Contact clamp lid, clamp_lid_v0_1, SCALE:2:1, PROVISIONAL, First-angle | all present  |
| PASS | 4 drawing PDF | clamp_lid_v0_1_drawing.PDF | key dimensions shown | 26.00, 4.00, 2.30 | all present  |
| PASS | 4 drawing PDF | rig_base_v0_1_drawing.PDF | pages / A3 size | 1 page, 420x297 | 1, 420x297  |
| PASS | 4 drawing PDF | rig_base_v0_1_drawing.PDF | title block / scale / notes | Bench rig base, rig_base_v0_1, SCALE:1:2, PROVISIONAL, First-angle | all present  |
| PASS | 4 drawing PDF | rig_base_v0_1_drawing.PDF | key dimensions shown | 160.00, 120.00, 5.00, 4.30 | all present  |
| PASS | 4 drawing PDF | wound_bed_spacer_v0_1_drawing.PDF | pages / A3 size | 1 page, 420x297 | 1, 420x297  |
| PASS | 4 drawing PDF | wound_bed_spacer_v0_1_drawing.PDF | title block / scale / notes | Wound-bed spacer, wound_bed_spacer_v0_1, SCALE:1:2, PROVISIONAL, First-angle | all present  |
| PASS | 4 drawing PDF | wound_bed_spacer_v0_1_drawing.PDF | key dimensions shown | 90.00, 11.91 | all present  |
| PASS | 4 drawing PDF | dermasense_bench_v0_1_drawing.PDF | pages / A3 size | 1 page, 420x297 | 1, 420x297  |
| PASS | 4 drawing PDF | dermasense_bench_v0_1_drawing.PDF | title block / scale / notes | Bench test, dermasense_bench_v0_1, SCALE:1:2, PROVISIONAL, First-angle | all present  |
| PASS | 4 drawing PDF | dermasense_bench_v0_1_drawing.PDF | key dimensions shown | ITEM NO., QTY. | all present  |
| PASS | 1 part | strip_v0_1 | unit system | 5 (MMGS) | 5  |
| PASS | 1 part | strip_v0_1 | volume mm3 | 179.5 | 179.5  |
| PASS | 1 part | strip_v0_1 | bounding box mm | (0, -9.12, -0.02, 96.0, 19.12, 0.125) | (0.0, -9.12, -0.02, 96.0, 19.12, 0.125)  |
| PASS | 1 part | strip_v0_1 | custom properties | ['Description', 'Revision', 'Material'] | ['Description', 'Revision', 'Material', 'Project', 'DrawnBy', 'MaterialNote']  |
| PASS | 1 part | seal_v0_1 | unit system | 5 (MMGS) | 5  |
| PASS | 1 part | seal_v0_1 | volume mm3 | 61.5 | 61.5  |
| PASS | 1 part | seal_v0_1 | bounding box mm | (23.0, 0, 0, 96.0, 10.0, 0.09) | (23.0, 0.0, 0.0, 96.0, 10.0, 0.09)  |
| PASS | 1 part | seal_v0_1 | custom properties | ['Description', 'Revision', 'Material'] | ['Description', 'Revision', 'Material', 'Project', 'DrawnBy', 'MaterialNote']  |
| PASS | 1 part | clamp_base_v0_1 | unit system | 5 (MMGS) | 5  |
| PASS | 1 part | clamp_base_v0_1 | volume mm3 | 16414.9 | 16414.9  |
| PASS | 1 part | clamp_base_v0_1 | bounding box mm | (-4.0, -16.62, 0, 22.0, 26.62, 16.0) | (-4.0, -16.62, 0.0, 22.0, 26.62, 16.0)  |
| PASS | 1 part | clamp_base_v0_1 | custom properties | ['Description', 'Revision', 'Material'] | ['Description', 'Revision', 'Material', 'Project', 'DrawnBy', 'MaterialNote']  |
| PASS | 1 part | clamp_lid_v0_1 | unit system | 5 (MMGS) | 5  |
| PASS | 1 part | clamp_lid_v0_1 | volume mm3 | 4391.1 | 4391.1  |
| PASS | 1 part | clamp_lid_v0_1 | bounding box mm | (-4.0, -16.62, 0, 22.0, 26.62, 4.0) | (-4.0, -16.62, 0.0, 22.0, 26.62, 4.0)  |
| PASS | 1 part | clamp_lid_v0_1 | custom properties | ['Description', 'Revision', 'Material'] | ['Description', 'Revision', 'Material', 'Project', 'DrawnBy', 'MaterialNote']  |
| PASS | 1 part | pogo_pin_P75_simplified | unit system | 5 (MMGS) | 5  |
| PASS | 1 part | pogo_pin_P75_simplified | volume mm3 | 12.9 | 12.9  |
| PASS | 1 part | pogo_pin_P75_simplified | bounding box mm | (-0.51, -0.51, 0, 0.51, 0.51, 15.8) | (-0.51, -0.51, 0.0, 0.51, 0.51, 15.8)  |
| PASS | 1 part | pogo_pin_P75_simplified | custom properties | ['Description', 'Revision', 'Material'] | ['Description', 'Revision', 'Material', 'Project', 'DrawnBy', 'MaterialNote']  |
| PASS | 1 part | dowel_2x12 | unit system | 5 (MMGS) | 5  |
| PASS | 1 part | dowel_2x12 | volume mm3 | 37.7 | 37.7  |
| PASS | 1 part | dowel_2x12 | bounding box mm | (-1.0, -1.0, 0, 1.0, 1.0, 12.0) | (-1.0, -1.0, 0.0, 1.0, 1.0, 12.0)  |
| PASS | 1 part | dowel_2x12 | custom properties | ['Description', 'Revision', 'Material'] | ['Description', 'Revision', 'Material', 'Project', 'DrawnBy', 'MaterialNote']  |
| PASS | 1 part | rig_base_v0_1 | unit system | 5 (MMGS) | 5  |
| PASS | 1 part | rig_base_v0_1 | volume mm3 | 95644.8 | 95644.8  |
| PASS | 1 part | rig_base_v0_1 | bounding box mm | (-10, -55.0, 0, 150.0, 65.0, 5.0) | (-10.0, -55.0, 0.0, 150.0, 65.0, 5.0)  |
| PASS | 1 part | rig_base_v0_1 | custom properties | ['Description', 'Revision', 'Material'] | ['Description', 'Revision', 'Material', 'Project', 'DrawnBy', 'MaterialNote']  |
| PASS | 1 part | wound_bed_spacer_v0_1 | unit system | 5 (MMGS) | 5  |
| PASS | 1 part | wound_bed_spacer_v0_1 | volume mm3 | 96433.6 | 96433.6  |
| PASS | 1 part | wound_bed_spacer_v0_1 | bounding box mm | (45.0, -40.0, 0, 135.0, 50.0, 11.91) | (45.0, -40.0, 0.0, 135.0, 50.0, 11.91)  |
| PASS | 1 part | wound_bed_spacer_v0_1 | custom properties | ['Description', 'Revision', 'Material'] | ['Description', 'Revision', 'Material', 'Project', 'DrawnBy', 'MaterialNote']  |
| PASS | 1 part | dressing_reference_bordered_foam | unit system | 5 (MMGS) | 5  |
| PASS | 1 part | dressing_reference_bordered_foam | volume mm3 | 23812.5 | 23812.5  |
| PASS | 1 part | dressing_reference_bordered_foam | bounding box mm | (-50.0, -50.0, 0, 50.0, 50.0, 4.0) | (-50.0, -50.0, 0.0, 50.0, 50.0, 4.0)  |
| PASS | 1 part | dressing_reference_bordered_foam | custom properties | ['Description', 'Revision', 'Material'] | ['Description', 'Revision', 'Material', 'Project', 'DrawnBy', 'MaterialNote']  |
| PASS | 2 STEP | strip_v0_1.STEP | re-imported volume mm3 | 179.5 | 179.5  |
| PASS | 2 STEP | seal_v0_1.STEP | re-imported volume mm3 | 61.5 | 61.5  |
| PASS | 2 STEP | clamp_base_v0_1.STEP | re-imported volume mm3 | 16414.9 | 16414.9  |
| PASS | 2 STEP | clamp_lid_v0_1.STEP | re-imported volume mm3 | 4391.1 | 4391.1  |
| PASS | 2 STEP | pogo_pin_P75_simplified.STEP | re-imported volume mm3 | 12.9 | 12.9  |
| PASS | 2 STEP | dowel_2x12.STEP | re-imported volume mm3 | 37.7 | 37.7  |
| PASS | 2 STEP | rig_base_v0_1.STEP | re-imported volume mm3 | 95644.8 | 95644.8  |
| PASS | 2 STEP | wound_bed_spacer_v0_1.STEP | re-imported volume mm3 | 96433.6 | 96433.6  |
| PASS | 2 STEP | dressing_reference_bordered_foam.STEP | re-imported volume mm3 | 23812.5 | 23812.5  |
| PASS | 3 assembly | dermasense_bench_v0_1 | unit system | 5 (MMGS) | 5  |
| PASS | 3 assembly | components | count | 13 | 13  |
| PASS | 3 assembly | rig_base_v0_1-1 | position mm (no rotation) | (0, 0, -21.02) | (0.0, 0.0, -21.02)  |
| PASS | 3 assembly | wound_bed_spacer_v0_1-1 | position mm (no rotation) | (0, 0, -16.02) | (0.0, 0.0, -16.02)  |
| PASS | 3 assembly | dressing_reference_bordered_foam-1 | position mm (no rotation) | (90.0, 5.0, -4.11) | (90.0, 5.0, -4.11)  |
| PASS | 3 assembly | seal_v0_1-1 | position mm (no rotation) | (0, 0, -0.11) | (0.0, 0.0, -0.11)  |
| PASS | 3 assembly | strip_v0_1-1 | position mm (no rotation) | (0, 0, 0) | (0.0, 0.0, 0.0)  |
| PASS | 3 assembly | clamp_base_v0_1-1 | position mm (no rotation) | (0, 0, -16.02) | (0.0, 0.0, -16.02)  |
| PASS | 3 assembly | clamp_lid_v0_1-1 | position mm (no rotation) | (0, 0, 0.125) | (0.0, 0.0, 0.125)  |
| PASS | 3 assembly | pogo_pin_P75_simplified-1 | position mm (no rotation) | (8.0, -2.62, -15.82) | (8.0, -2.62, -15.82)  |
| PASS | 3 assembly | pogo_pin_P75_simplified-2 | position mm (no rotation) | (8.0, 2.46, -15.82) | (8.0, 2.46, -15.82)  |
| PASS | 3 assembly | pogo_pin_P75_simplified-3 | position mm (no rotation) | (8.0, 7.54, -15.82) | (8.0, 7.54, -15.82)  |
| PASS | 3 assembly | pogo_pin_P75_simplified-4 | position mm (no rotation) | (8.0, 12.62, -15.82) | (8.0, 12.62, -15.82)  |
| PASS | 3 assembly | dowel_2x12-1 | position mm (no rotation) | (8.0, -6.62, -10.02) | (8.0, -6.62, -10.02)  |
| PASS | 3 assembly | dowel_2x12-2 | position mm (no rotation) | (8.0, 16.62, -10.02) | (8.0, 16.62, -10.02)  |
| PASS | 3 assembly | interference | volume clashes (coincident faces allowed) | none | none  |
| PASS | 4 drawing | strip_v0_1.SLDDRW | scale / projection / views | 1:1, first-angle, 4 views, sheets 1 | 1:1, first-angle, 4 views, sheets 1  |
| PASS | 4 drawing | seal_v0_1.SLDDRW | scale / projection / views | 1:1, first-angle, 4 views, sheets 1 | 1:1, first-angle, 4 views, sheets 1  |
| PASS | 4 drawing | clamp_base_v0_1.SLDDRW | scale / projection / views | 2:1, first-angle, 4 views, sheets 1 | 2:1, first-angle, 4 views, sheets 1  |
| PASS | 4 drawing | clamp_lid_v0_1.SLDDRW | scale / projection / views | 2:1, first-angle, 4 views, sheets 1 | 2:1, first-angle, 4 views, sheets 1  |
| PASS | 4 drawing | rig_base_v0_1.SLDDRW | scale / projection / views | 1:2, first-angle, 4 views, sheets 1 | 1:2, first-angle, 4 views, sheets 1  |
| PASS | 4 drawing | wound_bed_spacer_v0_1.SLDDRW | scale / projection / views | 1:2, first-angle, 4 views, sheets 1 | 1:2, first-angle, 4 views, sheets 1  |
| PASS | 4 drawing | dermasense_bench_v0_1.SLDDRW | scale / projection / views | 1:2, first-angle, 4 views, sheets 1 | 1:2, first-angle, 4 views, sheets 1  |
| BLOCKED | 5 measured | strip_v0_1 vs E2 | trace width F >= smallest reliable LIG line | E2 measurement | no data (waiting for 04_lig_lab/e2/measured_process.json) |
| BLOCKED | 5 measured | strip_v0_1 vs E2 | as-built gap >= smallest isolating gap | E2 measurement | no data (waiting for 04_lig_lab/e2/measured_process.json) |
| BLOCKED | 5 measured | strip_v0_1 vs E2 | lead resistance over 85 mm <= 10 kOhm | E2 measurement | no data (waiting for 04_lig_lab/e2/measured_process.json) |
| BLOCKED | 5 measured | strip_v0_1 vs E2 | laser-cut hole fits the 2.0 mm dowel | E2 measurement | no data (waiting for 04_lig_lab/e2/measured_process.json) |
| BLOCKED | 5 measured | strip_v0_1 vs E2 | LIG relief vs 0.02 mm CAD assumption | E2 measurement | no data (waiting for 04_lig_lab/e2/measured_process.json) |
