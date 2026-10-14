# Submission readiness report (2026-10-14 23:41, commit 501ee05)

**9 Verified · 5 Complete · 6 Pending Physical Experiment · 1 Blocked** (of 21 deliverables).

| Status | Meaning |
|---|---|
| **Verified** | An automated check passed on the copy in this folder: it opened in its intended software and its content checks passed |
| **Complete** | Finished and reviewed. Not machine-verifiable, or it carries stated estimates |
| **Pending Physical Experiment** | Can't be finished without lab work (E2 laser runs, reader bench test, photos) |
| **Blocked** | Waiting for a team decision or resource that we can't create ourselves |

Nothing is labelled final just because it was generated. The material is a **laser-carbonised conductive layer (LIG-like)**; graphene is not confirmed (no Raman).

| ID | Deliverable | Path | Format | Status | Verification evidence | Remaining action |
|---|---|---|---|---|---|---|
| D01 | Official Vishwakarma Stage 2 template (base of the final deck) | [01_presentation/official_template/](01_presentation/official_template/) | PPTX | **Verified** | opens in Microsoft PowerPoint (read-only): 20 slides; MD5 c58ef4fe526045f1a82a806e6532bc3c matches the provenance record | Build the final deck on this file. Never edit it in place. |
| D02 | Stage 2 presentation (VK26-IITI-HT-0050) | `08_submission/VK26-IITI-HT-0050_Stage2_Dermasense.pptx` | PPTX | **Pending Physical Experiment** | v2 draft opens (11 slides) but is NOT submission-ready: it has no E2 or bench results and predates the CAD freeze and the reader. Personal-data scan: none found | After E2 and the reader bench test, put the real results into the existing v2 slides (no redesign), then copy here. |
| D03 | SolidWorks native models: 9 parts, 1 assembly, 7 drawings (v0.1) | [02_cad_solidworks/native/](02_cad_solidworks/native/) | SLDPRT/SLDASM/SLDDRW | **Verified** | 9/9 copied parts open in SolidWorks 2019, MMGS units, volumes match the independent expected values · assembly copy opens with 13 components; 13/13 resolved from the copied folder (self-contained) · 7/7 copied drawings open and reference the copied models | Update the strip and seal from the E2 measurements (verify_cad section 5), then rebuild. |
| D04 | STEP exports (neutral CAD) | [02_cad_solidworks/step/](02_cad_solidworks/step/) | STEP AP214 | **Verified** | 10 STEP files: millimetre units and solid bodies in every header; SolidWorks re-import volumes: see verify_cad_report.md (section 2) | Re-export after any CAD change (sw_build.py does this automatically). |
| D05 | CAD renders | [02_cad_solidworks/renders/](02_cad_solidworks/renders/) | JPG | **Verified** | 5 renders open, sizes [(945, 685)] | None. |
| D06 | CAD build + independent verification scripts and reports | [02_cad_solidworks/verification/](02_cad_solidworks/verification/) | PY/MD/JSON | **Verified** | verify_cad.py (2026-10-14 23:38:14): 99 PASS, 0 FAIL, 5 BLOCKED (blocked = waiting for E2 data) | Re-run verify_cad.py after E2. |
| D07 | CAD checked against measured LIG geometry (E2) | - | - | **Pending Physical Experiment** | no E2 measurements exist; verify_cad section 5 is BLOCKED | Run E2, then analyze_e2.py, then verify_cad.py. Its 5 BLOCKED checks become PASS/FAIL. |
| D08 | 2D drawings (A3, first-angle, PDF) | [03_drawings/pdf/](03_drawings/pdf/) | PDF | **Verified** | 7/7 PDFs open, A3 landscape, title block + PROVISIONAL note present | Re-issue after the E2 update (revision v0.2). |
| D09 | Laser job files (strip, seal, E1/E2 coupons) + DRC | [03_drawings/laser_dxf/](03_drawings/laser_dxf/) | DXF R2000 (mm) | **Verified** | 4/4 DXF open and audit cleanly in ezdxf, mm units; verify_laser_files.py: 35 PASS, 0 FAIL | Physical check at the machine: LaserCAD import sizes and layers (E2 step S0-6). |
| D10 | KiCad schematic of the two-zone reader (ERC clean) | [04_kicad/](04_kicad/) | KiCad 10 / PDF / netlist | **Verified** | copied schematic opens in KiCad 10 (kicad-cli); ERC on the copy: 0 violations | None for v0.1. A PCB only after the bench test and E4. |
| D11 | Reader firmware v0.1 + PC tools + wiring table | [05_firmware/](05_firmware/) | Arduino C++ / Python | **Verified** | copied sketch compiles with arduino-cli (esp32:esp32:esp32c3:CDCOnBoot=cdc): 327176 bytes (24% flash), 0 warnings, 22 compile-time tests · tool tests on the source: 10 passed (copies SHA-identical) · PASS: schematic <-> firmware <-> strip pads (0 mismatches) | Flash it to the real board (see D12). |
| D12 | Reader bench test with known resistors | [05_firmware/](05_firmware/) | MD/CSV | **Pending Physical Experiment** | document present; it is checked by reading, not by software | Buy parts (D13), wire per WIRING.md, run BENCH_TEST.md T0-T10, fill bench_test.csv. |
| D13 | Bill of materials v0.1 / procurement | [06_bom_procurement/](06_bom_procurement/) | CSV | **Complete** | bom_v0_1.csv: 23 rows x 13 columns, consistent | Check supplier prices and stock, fill have_it_YN, order the first batch (README). |
| D14 | E2 fabrication-validation package (procedure, matrix, sheets, analysis) | [07_experimental_data/E2_protocol/](07_experimental_data/E2_protocol/) | MD/PDF/CSV/PY | **Complete** | bench sheets PDF opens (17 pages); analysis tests 3 passed (synthetic data only); no measured_process.json exists (correct: no data yet) | Run it at the laser (Session S0, then Day 1 and Day 2). |
| D15 | E2 measured data and plots | [07_experimental_data/E2_data/](07_experimental_data/E2_data/) | CSV/PNG | **Pending Physical Experiment** | - | Fill the e2_*.csv files from the bench sheets and run analyze_e2.py. Copy the results here only after that. |
| D16 | Lab photographs (machine, coupons, microscope, bench reader) | [08_lab_photographs/](08_lab_photographs/) | JPG | **Pending Physical Experiment** | - | Take the originals during E2 and the bench test (rules: 04_lig_lab/e2/E2_procedure.md, data handling). |
| D17 | E2 safety checklist | [09_safety_fmea/](09_safety_fmea/) | MD | **Complete** | document present; it is checked by reading, not by software | Sign it at every session; scan the signed sheet into 08_lab_photographs. |
| D18 | Design FMEA v0.1 (15 failure modes, RPN ranked) | [09_safety_fmea/](09_safety_fmea/) | MD/CSV | **Complete** | fmea_v0_1.csv: 15 rows x 12 columns, consistent | Replace the estimated ratings with E2/E4/T-CON-01 results. Decide the F04 design change (loop each sense lead). |
| D19 | References: literature (36) + research matrix (16) | [10_references/](10_references/) | CSV/MD | **Complete** | literature.csv: 36 rows x 11 columns, consistent · research_matrix.csv: 16 rows x 12 columns, consistent · 35/39 DOIs/URLs resolve automatically; 1 answered but refused robots; 1 confirmed in the browser; 0 broken (HTTP 404/410) · 2 link(s) unreachable from this network (no HTTP answer, browser too): https://iteh.es/catalog/standards/cen/3eb17b79-e68a-4ea2-a2a8-dd6d98145e73/en-13726-1-2002, https://journals.ioffe.ru/articles/viewPDF/62275 | Open the unconfirmed links from another network; replace or drop any that are dead (L32 is already marked weak). |
| D20 | Public repository link | [11_repository_links/](11_repository_links/) | MD | **Blocked** | git remote: none configured; branch dev/stage2-rebuild @ 501ee05 | Team decision: create a GitHub repository (public or private), add it as the git remote, push dev/stage2-rebuild, then re-run this script. |
| D21 | Requirements, decisions, traceability, evidence register (control documents) | `00_control/requirements.md`, `00_control/decisions.md`, `00_control/traceability.csv`, `00_control/evidence_register.csv` | MD/CSV | **Pending Physical Experiment** | files exist in 00_control; they must be updated with E2 and bench results before submission | Update traceability and the evidence register with the E2 and bench-test results; then copy here. |

## Cross-checks on the whole folder

- Every copy is byte-identical to its source (SHA-256): **107/107**.
- Relative links in Markdown files: **all resolve**.
- Personal-data scan (e-mail, phone, ID-number patterns) over 57 text files: **none found**.
- Duplicates: a SHA-256 scan of the whole working tree found no duplicate files, so nothing was removed. The two template files differ in bytes but have identical content; both are kept (see TEMPLATE_PROVENANCE.md).

## The single next action for the team

**Book the laser and run E2 Session S0 + Day 1** (`07_experimental_data/E2_protocol/E2_procedure.md`).
Before that, buy or borrow silver paint, the 1 % resistor set and a DMM that reads 20 MΩ or more. Every Pending item depends on those measurements: the CAD update, deck results, photos and traceability.
