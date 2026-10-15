# PPT claim and reference check

**Checked:** 15 Oct 2026; re-checked 16 Oct after the slides were shortened (four claims regained a qualifier: "reported rates span", "can leak", "would lift", "likely a % command"). Checked against the project files and sources named below. Each important claim in the deck is listed with where it comes from.

**Status words:**

| Status | Meaning |
|---|---|
| **Verified (file / tool)** | Reproduced from a project file or tool output on 14–15 Oct |
| **Cited (depth)** | Published source; reading depth stated |
| **Calculation** | Engineering calculation with stated inputs; not a measurement |
| **Target** | A goal for future tests |
| **Description** | Qualitative workflow or general knowledge, no number |
| **Our search** | Result of our own, non-exhaustive search |

**Not claimed anywhere in the deck:**
- that the sensor works
- that the prototype has been demonstrated
- that the material is graphene (it is called *LIG-like laser-carbonised conductive material*)
- any clinical benefit

**Correction made during this check:** earlier project documents said the firmware had "22" compile-time tests. The file contains **19** `static_assert` checks. Every document and slide now says 19.

## Claims

| # | Claim as shown | Slide | Source / evidence | Status |
|---|---|---|---|---|
| 1 | 44.9 % of 588 dressing changes were made while moisture was optimal | 2, 3 | Ref 1, Milne 2016 (`literature.csv` L08) | Cited (full text) |
| 2 | Some makers' change rule: exudate ≈ 2 cm from the pad edge | 2, 3, 4 | Ref 2, dressing IFUs (L28). Mepilex instead uses strike-through reaching 3 edges | Cited (excerpts); wording says "some makers" |
| 3 | Today's moisture sensor (WoundSense) reads at one point | 2 | Ref 1 | Cited (full text) |
| 4 | Moisture inside a dressing is uneven (8-point in-vitro map) | 2, 3 | Ref 3, McColl 2007 (L26) | Cited (abstract) |
| 5 | Diaper wetness strips with clip-on readers exist | 2, 12 | Ref 4, patents P01/P02 | Cited (patent summaries; claims not read) |
| 6 | Smart bandages use custom electronics | 2 | Ref 5, Jiang 2022 (L03) | Cited (listing + coverage) |
| 7 | "In our search, none reads a dressing's own change line" | 2 | `2_research/research_gap.md` | Our search; not exhaustive |
| 8 | Exudate production 0.10–1.3 g/cm²/day across patients and two methods | 3 | Ref 6, Dealey 2006 (L38). Repository page read 15 Oct: 0.10 and 0.21 (method A, 2 patients); mean 1.3 (method B, 5 patients) | Cited (abstract) |
| 9 | Conductive carbon can be laser-written on polyimide in one pass | 2, 8 | Ref 7, Lin 2014 (L01) | Cited (full text) |
| 10 | LIG made in air is superhydrophilic → leads are sealed | 8 | Ref 9, Li 2017 (L37) | Cited (abstract) |
| 11 | CO₂ tubes fire unevenly at low settings | 15 | Ref 8, softsolder.com (L34) | Cited; **not peer-reviewed** (stated) |
| 12 | Polyimide film is not sold as medical grade | 13 | Ref 11, DuPont statement (L22) | Cited (web page) |
| 13 | "Solution A" simulated exudate per EN 13726 | 13 | Ref 10 (L29) | Cited (catalogue); link unreachable from our network |
| 14 | 2 zones; windows 6 × 3.9 mm; strip 96 mm; 4 pads at 5.08 mm; lines/gaps 1.0 mm (provisional) | 5, 8 | `4_sensor_strip/strip_v0_1_geometry.json`, DRC PASS | Verified (file) |
| 15 | Wet < 100 kΩ, dry > 300 kΩ, 3-scan persistence, check ±5 % | 5, 6 | `7_firmware/reader_v0_1/config.h` | Verified (file); thresholds are design values |
| 16 | Expected wet 4.2–14.8 kΩ, dry ≥ 1 MΩ | 5, 10 | `6_electronics/calc_readout_report.md` | Calculation |
| 17 | Excitation ≤ 33 µA | 5 | `calc_readout_report.md`: 32 µA | Calculation (rounded up) |
| 18 | ADS1115 single-shot, 128 SPS, auto-range; A1 = 3V3 (ratiometric) | 6 | `reader_v0_1/ads1115.h`, `reader_v0_1.ino`, schematic | Verified (source) |
| 19 | 19 compile-time tests; 10 PC-side tests; compiles with 0 warnings, 327,176 bytes (24 %) | 5, 6, 11 | `zone_logic_tests.h` (19 `static_assert`), pytest output, arduino-cli output | Verified (tool) |
| 20 | The firmware has not run on hardware | 5, 6, 9 | `7_firmware/BENCH_TEST.md` not executed | Stated as pending |
| 21 | 9 parts, 1 assembly, 7 A3 drawings, STEP; 13 component positions | 7, 11 | `5_cad/solidworks/`, `verify_cad_results.json` | Verified (tool) |
| 22 | CAD verification: 99 pass, 0 fail, 5 blocked (waiting for E2) | 7, 11 | `5_cad/verify_cad_results.json` (run 14 Oct 23:38) | Verified (tool) |
| 23 | Seal clash 9.0 mm³ found by interference detection; seal moved to x = 23 mm; 0 interference | 7, 15, 16 | `verify_cad` report; `3_decisions/decisions.md` D-013 | Verified (tool) |
| 24 | Pin force 0.72 N (2.9 N total); lid deflection 11 µm; tolerance 0.49 vs ±1.35 mm; strain 0.62 %; 20 vs 231 MPa | 7 | `5_cad/calc_mechanical_report.md` | Calculation (datasheet inputs) |
| 25 | STEP exported in cm, fixed to mm; drawings showed 0.13 for 0.125 mm, fixed | 12, 15, 16 | Commit `fba39ef`; `verify_cad` STEP checks | Verified (tool) |
| 26 | 4 DXFs pass 35/35 file checks | 8 | `4_sensor_strip/laser_files_check.md` | Verified (tool) |
| 27 | Laser: 1200 × 900 mm bed, 20 kHz PWM, 98 % cap | 8 | `C:\LaserCAD\AWCCfg\SysCfg.ini` (laptop copy) | Verified on the laptop; match to the lab machine pending (E2 S0-2) |
| 28 | "12" is most likely a % PWM command, not watts | 8, 15 | Inference from the config + Ref 8 | Hypothesis, worded "most likely" |
| 29 | E2: 4 bracket + 3 resolution coupons, 72 pre-registered samples; pass rules | 8 | `4_sensor_strip/e2_experiment/e2_sample_matrix.csv`, `E2_procedure.md` | Verified (file) |
| 30 | ERC 0 violations; netlist ↔ firmware ↔ pads 0 mismatches; pin map | 9 | `6_electronics/kicad/out/erc.json`, `7_firmware/tools/check_consistency.py` | Verified (tool) |
| 31 | BOM groups and total ≈ ₹2,078–7,361 | 10 | Computed by the builder from `6_electronics/bom_v0_1.csv` | Calculation from **estimated** prices; nothing ordered |
| 32 | Concept scores 4.36 / 4.29 / 3.96 / 3.46 / 3.39 | 12 | `3_decisions/decision_matrix.md` | Verified (file); scores are engineering judgement |
| 33 | FMEA RPN 224 / 210 / 150 / 140 / 120; 15 modes | 13 | `3_decisions/fmea_v0_1.csv` | Verified (file); ratings are **estimates** |
| 34 | Standards ISO 14971, IEC 60601-1, ISO 10993-1, EN 13726, IEC 60825-1 | 13 | Design intent | "Considered, not claimed" |
| 35 | Bench test T8 checks average DC < 5 mV | 13 | `7_firmware/BENCH_TEST.md` | Planned test |
| 36 | Alert within ±10 % of the visible-front volume; ≤ ₹100 per strip; who benefits | 4 | E4 plan; BOM film price | Target, labelled "target" / "expected, to verify" |
| 37 | Roadmap months, gates G1–G4, Stage 3 target | 14 | E2, bench-test and E4 plans | Plan |
| 38 | Git history from `330b474`; commits shown | 11, 12 | `git log` | Verified (tool) |
| 39 | SolidWorks window with the FeatureManager tree | 11 | Screen capture of our machine by `render_cad.py`, 15 Oct | Verified (genuine capture) |
| 40 | Team names, application ID VK26-IITI-HT-0050, track | 1, 2 | As registered (team records) | As provided; not independently verifiable here |
| 41 | Workflow steps, maceration risk of late changes, time per check "to be measured" | 3 | Dressing-care practice | Description; no number given |

## References as printed on slide 17

Link checks were run by our submission checker on 14 Oct (DOI resolution through doi.org) and in the browser on 15 Oct.

| # | Source | Reading depth (as printed) | Link check |
|---|---|---|---|
| 1 | Milne S.D. et al., Int. Wound J. 13(6):1309–1314 (2016), doi:10.1111/iwj.12521 | full text read | DOI resolves |
| 2 | Dressing IFUs (some foam dressings: 2 cm rule; Mepilex Border Flex: 3-edge strike-through) | excerpts | Mölnlycke brochure URL resolves |
| 3 | McColl D. et al., Int. J. Surg. 5(5):316–322 (2007), doi:10.1016/j.ijsu.2007.02.008 | abstract | DOI resolves |
| 4 | US 5,469,145; US 5,838,240; US 9,291,589; US 10,928,344 | summaries; claims not read | US5469145 and US10928344 pages resolve; the other two not link-checked |
| 5 | Jiang Y. et al., Nat. Biotechnol. (2022), doi:10.1038/s41587-022-01528-3 | listing + coverage | DOI resolves |
| 6 | Dealey C., Cameron J., Arrowsmith M., J. Wound Care 15(4):149–153 (2006) | abstract | Repository page opened 15 Oct; citation copied from it |
| 7 | Lin J. et al., Nat. Commun. 5:5714 (2014), doi:10.1038/ncomms6714 | full text read | DOI resolves |
| 8 | softsolder.com, CO₂ tube current vs PWM (2022) | not peer-reviewed | Resolves (after encoding the "₂" in the URL) |
| 9 | Li Y. et al., Adv. Mater. 29:1700496 (2017), doi:10.1002/adma.201700496 | abstract | DOI resolves |
| 10 | EN 13726-1:2002 / EN 13726:2023 | catalogue entry | **Not reachable from our network (stated on the slide)** |
| 11 | DuPont position statement on medical applications | web page | Resolves |
| 12 | TI ADS1115 datasheet (SBAS444); Espressif ESP32-C3 datasheet | vendor documents | ESP32-C3 PDF resolves; ADS1115 not link-checked |

**Image credits:** slide 18 lists all 14 deck images. Every one is generated from project files or captured from our own SolidWorks session. No external, stock or AI-generated image is used.
