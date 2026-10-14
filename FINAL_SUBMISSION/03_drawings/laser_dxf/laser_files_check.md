# Laser job file check (verify_laser_files.py, 2026-10-14 22:50)

**35 PASS, 0 FAIL.**
This checks the files only. LaserCAD's colour-to-layer mapping and import scale are checked at the machine (E2 procedure, step S0-6).

| File | Check | Result | Detail |
|---|---|---|---|
| lig_test_coupon.dxf | opens and audits | PASS | 0 errors, 0 fixes |
| lig_test_coupon.dxf | DXF version / units | PASS | AC1015, INSUNITS 4 (4 = mm) |
| lig_test_coupon.dxf | only closed outlines on expected layers | PASS | 18 engrave + 2 cut outlines |
| lig_test_coupon.dxf | overall size mm | PASS | 237.00 x 20.00 (expected 237.0 x 20.0) |
| lig_test_coupon.dxf | fits the laser bed | PASS | 237 x 20 within 1200 x 900 |
| lig_test_coupon.dxf | engrave regions do not overlap | PASS | overlap area 0.0000 mm2 |
| lig_test_coupon.dxf | smallest spacing between engrave regions | PASS | 2.000 mm (design min 2.0) |
| lig_test_coupon.dxf | no engrave feature narrower than 2.0 mm | PASS | 0 too-narrow outlines |
| lig_test_coupon.dxf | engraving inside the cut outline (margin 1.0 mm) | PASS | all inside |
| e2/e2_res_coupon.dxf | opens and audits | PASS | 0 errors, 0 fixes |
| e2/e2_res_coupon.dxf | DXF version / units | PASS | AC1015, INSUNITS 4 (4 = mm) |
| e2/e2_res_coupon.dxf | only closed outlines on expected layers | PASS | 17 engrave + 5 cut outlines |
| e2/e2_res_coupon.dxf | overall size mm | PASS | 180.00 x 20.00 (expected 180.0 x 20.0) |
| e2/e2_res_coupon.dxf | fits the laser bed | PASS | 180 x 20 within 1200 x 900 |
| e2/e2_res_coupon.dxf | engrave regions do not overlap | PASS | overlap area 0.0000 mm2 |
| e2/e2_res_coupon.dxf | smallest spacing between engrave regions | PASS | 0.200 mm (design min 0.2) |
| e2/e2_res_coupon.dxf | no engrave feature narrower than 0.3 mm | PASS | 0 too-narrow outlines |
| e2/e2_res_coupon.dxf | engraving inside the cut outline (margin 1.0 mm) | PASS | all inside |
| strip_v0_1.dxf | opens and audits | PASS | 0 errors, 0 fixes |
| strip_v0_1.dxf | DXF version / units | PASS | AC1015, INSUNITS 4 (4 = mm) |
| strip_v0_1.dxf | only closed outlines on expected layers | PASS | 3 engrave + 3 cut outlines |
| strip_v0_1.dxf | overall size mm | PASS | 96.00 x 28.24 (expected 96.0 x 28.24) |
| strip_v0_1.dxf | fits the laser bed | PASS | 96 x 28 within 1200 x 900 |
| strip_v0_1.dxf | engrave regions do not overlap | PASS | overlap area 0.0000 mm2 |
| strip_v0_1.dxf | smallest spacing between engrave regions | PASS | 1.000 mm (design min 0.95) |
| strip_v0_1.dxf | no engrave feature narrower than 1.0 mm | PASS | 0 too-narrow outlines |
| strip_v0_1.dxf | engraving inside the cut outline (margin 0.4 mm) | PASS | all inside |
| strip_v0_1_encap.dxf | opens and audits | PASS | 0 errors, 0 fixes |
| strip_v0_1_encap.dxf | DXF version / units | PASS | AC1015, INSUNITS 4 (4 = mm) |
| strip_v0_1_encap.dxf | only closed outlines on expected layers | PASS | 0 engrave + 3 cut outlines |
| strip_v0_1_encap.dxf | overall size mm | PASS | 73.00 x 10.00 (expected 73.0 x 10.0) |
| strip_v0_1_encap.dxf | fits the laser bed | PASS | 73 x 10 within 1200 x 900 |
| strip_v0_1.dxf | LIG area matches geometry JSON (CAD source) | PASS | DXF 392.30 mm2 vs JSON 392.30 mm2 |
| strip_v0_1_encap.dxf | seal outline matches geometry JSON | PASS | DXF 730.00 mm2 vs JSON 730.00 mm2 |
| strip_v0_1.dxf | nets are separate pieces | PASS | 3 pieces for 3 nets |
