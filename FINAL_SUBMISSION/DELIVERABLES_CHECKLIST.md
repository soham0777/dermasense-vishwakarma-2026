# Deliverables checklist (2026-10-14 23:41)

☑ done (Verified or Complete) · ☐ waits for lab work · ☒ blocked by a team decision

- ☑ **D01** Official Vishwakarma Stage 2 template (base of the final deck) (Verified): Build the final deck on this file. Never edit it in place.
- ☐ **D02** Stage 2 presentation (VK26-IITI-HT-0050) (Pending Physical Experiment): After E2 and the reader bench test, put the real results into the existing v2 slides (no redesign), then copy here.
- ☑ **D03** SolidWorks native models: 9 parts, 1 assembly, 7 drawings (v0.1) (Verified): Update the strip and seal from the E2 measurements (verify_cad section 5), then rebuild.
- ☑ **D04** STEP exports (neutral CAD) (Verified): Re-export after any CAD change (sw_build.py does this automatically).
- ☑ **D05** CAD renders (Verified): None.
- ☑ **D06** CAD build + independent verification scripts and reports (Verified): Re-run verify_cad.py after E2.
- ☐ **D07** CAD checked against measured LIG geometry (E2) (Pending Physical Experiment): Run E2, then analyze_e2.py, then verify_cad.py. Its 5 BLOCKED checks become PASS/FAIL.
- ☑ **D08** 2D drawings (A3, first-angle, PDF) (Verified): Re-issue after the E2 update (revision v0.2).
- ☑ **D09** Laser job files (strip, seal, E1/E2 coupons) + DRC (Verified): Physical check at the machine: LaserCAD import sizes and layers (E2 step S0-6).
- ☑ **D10** KiCad schematic of the two-zone reader (ERC clean) (Verified): None for v0.1. A PCB only after the bench test and E4.
- ☑ **D11** Reader firmware v0.1 + PC tools + wiring table (Verified): Flash it to the real board (see D12).
- ☐ **D12** Reader bench test with known resistors (Pending Physical Experiment): Buy parts (D13), wire per WIRING.md, run BENCH_TEST.md T0-T10, fill bench_test.csv.
- ☑ **D13** Bill of materials v0.1 / procurement (Complete): Check supplier prices and stock, fill have_it_YN, order the first batch (README).
- ☑ **D14** E2 fabrication-validation package (procedure, matrix, sheets, analysis) (Complete): Run it at the laser (Session S0, then Day 1 and Day 2).
- ☐ **D15** E2 measured data and plots (Pending Physical Experiment): Fill the e2_*.csv files from the bench sheets and run analyze_e2.py. Copy the results here only after that.
- ☐ **D16** Lab photographs (machine, coupons, microscope, bench reader) (Pending Physical Experiment): Take the originals during E2 and the bench test (rules: 04_lig_lab/e2/E2_procedure.md, data handling).
- ☑ **D17** E2 safety checklist (Complete): Sign it at every session; scan the signed sheet into 08_lab_photographs.
- ☑ **D18** Design FMEA v0.1 (15 failure modes, RPN ranked) (Complete): Replace the estimated ratings with E2/E4/T-CON-01 results. Decide the F04 design change (loop each sense lead).
- ☑ **D19** References: literature (36) + research matrix (16) (Complete): Open the unconfirmed links from another network; replace or drop any that are dead (L32 is already marked weak).
- ☒ **D20** Public repository link (Blocked): Team decision: create a GitHub repository (public or private), add it as the git remote, push dev/stage2-rebuild, then re-run this script.
- ☐ **D21** Requirements, decisions, traceability, evidence register (control documents) (Pending Physical Experiment): Update traceability and the evidence register with the E2 and bench-test results; then copy here.
