# Claim → evidence matrix

**Date:** 19 Oct 2026, for the 19-slide refined deck. It replaces `PPT_Claim_and_Reference_Check.md` (in git history). Every important claim in `FINAL_SUBMISSION/Vishwakarma_Stage2_Final.pptx` is listed with its source and status. Tool results were re-run on 19 Oct.

**Labels (only these are used):**

| Label | Meaning |
|---|---|
| COMPLETED AND VERIFIED | Exists in our files, and a tool or the source confirms it (software, CAD or document level) |
| COMPLETED, NOT YET HARDWARE-VALIDATED | Built in software or design, but never run or measured on hardware |
| CALCULATED / SIMULATED | Engineering calculation with stated inputs; not a measurement |
| SUPPORTED BY LITERATURE | A published or manufacturer source, with its reading depth |
| ESTIMATED | Our estimate or projection, labelled as such on the slide |
| PROPOSED | A plan, target or design intent |
| NOT YET COMPLETED | Stated as missing |

**Never claimed anywhere:**
- that the sensor works
- that a prototype exists
- that the layer is graphene
- any clinical benefit
- a working phone app or internet monitoring

## Claims

| # | Claim as shown | Slides | Evidence | Label |
|---|---|---|---|---|
| 1 | 44.9 % of 588 dressing changes were made while moisture was still optimal | 3, 4 | Ref 1, Milne 2016 (`2_research/literature.csv` L08), full text | SUPPORTED BY LITERATURE |
| 2 | Some foam dressings say "change when exudate approaches ≈ 2 cm from the pad edge" | 3 | Ref 2 (L28), IFU excerpts; Mepilex uses 3-edge strike-through instead | SUPPORTED BY LITERATURE |
| 3 | Makers' change signs are visual (ALLEVYN LIFE: "At 75%, it's time to change your dressing") | 3, 13 | Ref 14 (L40), manufacturer page read 19 Oct | SUPPORTED BY LITERATURE |
| 4 | Today's moisture sensor (WoundSense) reads at one point | 3 | Ref 1 | SUPPORTED BY LITERATURE |
| 5 | Moisture inside a dressing is uneven (8-point in-vitro map) | 3 | Ref 3, McColl 2007 (L26), abstract | SUPPORTED BY LITERATURE |
| 6 | Diaper wetness strips with clip-on readers exist | 3, 13 | Ref 4, 4 patents (summaries; claims not read) | SUPPORTED BY LITERATURE |
| 7 | Smart therapy bandages already shown at lab scale | 3, 13 | Ref 5, Jiang 2022 (listing + coverage) | SUPPORTED BY LITERATURE |
| 8 | "In our search, no low-cost sensor reads that change line" | 3 | `2_research/research_gap.md`; our own search, **not exhaustive** (worded "in our search") | SUPPORTED BY LITERATURE |
| 9 | ≈ 18 min per dressing visit (UK, patient-reported) | 4 | Ref 13 (L39): Mölnlycke-commissioned survey, 2018; industry-sponsored (stated) | SUPPORTED BY LITERATURE |
| 10 | ₹240–510 for one 10 × 10 cm foam dressing | 4, 5 | Ref 15 (L41): Truemeds listings; Border pack size unclear (stated) | SUPPORTED BY LITERATURE |
| 11 | Exudate rates 0.1–1.3 g/cm²/day, two methods | 4 | Ref 6, Dealey 2006 (abstract) | SUPPORTED BY LITERATURE |
| 12 | Conductive carbon can be laser-written on polyimide in one pass | 9 | Ref 7, Lin 2014 (full text) | SUPPORTED BY LITERATURE |
| 13 | LIG made in air wets easily, so the leads are sealed | 9 | Ref 9, Li 2017 (abstract) | SUPPORTED BY LITERATURE |
| 14 | CO₂ tubes fire unsteadily at low power | 16 | Ref 8 (**not peer-reviewed**, stated) | SUPPORTED BY LITERATURE |
| 15 | Polyimide film is not sold as medical grade (DuPont), which corrects our Stage 1 proposal | 13, 14 | Ref 11; Stage 1 PDF (`_private/`) | SUPPORTED BY LITERATURE |
| 16 | "Solution A" simulated exudate per EN 13726 | 14 | Ref 10 (catalogue; link unreachable, stated) | SUPPORTED BY LITERATURE |
| 17 | Mechanism: fluid bridges a 1.0 mm gap between sense and common electrodes; the reader sees the resistance drop | 6 | `3_decisions/sensor_selection.md`; figure labelled "concept drawing" | PROPOSED (tested by E2 Part W and E4) |
| 18 | Layer order: cover film / strip (carbon down) + seal / pad / wound-contact layer / wound; the strip never touches the wound | 5, 6 | `sensor_selection.md` §2 | PROPOSED (design) |
| 19 | 2 zones; windows 6 mm long; 1.0 mm lines and gaps; 4 pads at 5.08 mm; strip 10 mm wide | 6, 9 | `4_sensor_strip/strip_v0_1_geometry.json`, DRC PASS | COMPLETED AND VERIFIED (design file; provisional until E2) |
| 20 | Wet < 100 kΩ, dry > 300 kΩ, 3 scans; check resistor ±5 % → FAULT | 6, 7 | `7_firmware/reader_v0_1/config.h` | COMPLETED, NOT YET HARDWARE-VALIDATED |
| 21 | Expected wet 4–15 kΩ, dry > 1 MΩ; drive ≤ 33 µA | 6, 10 | `6_electronics/calc_readout_report.md` (4.2–14.8 kΩ; 32 µA) | CALCULATED / SIMULATED |
| 22 | Bipolar drive, so no net DC on the wet strip | 6, 7, 10, 14 | Firmware `measure()`; bench test T8 checks < 5 mV | COMPLETED, NOT YET HARDWARE-VALIDATED |
| 23 | 23 compile-time tests + 16 PC tests pass; compiles with 0 warnings, 650,349 bytes (49 %) | 2, 7, 12 | `zone_logic_tests.h` (a deliberately wrong test breaks the build, re-proved 19 Oct); pytest; arduino-cli | COMPLETED AND VERIFIED (software only) |
| 24 | Reader has not run on hardware | 2, 7, 12 | `7_firmware/BENCH_TEST.md` not executed | NOT YET COMPLETED |
| 25 | State broadcast over Bluetooth LE (13-byte advertisement), readable with any scanner app; no custom app | 2, 5, 6, 7, 13, 17 | `ble_beacon.h`, `reader_v0_1.ino`, `tools/decode_beacon.py`; D-015. Range and reception not tested (T11) | COMPLETED, NOT YET HARDWARE-VALIDATED |
| 26 | 9 SolidWorks parts, 1 assembly (13 components), 7 A3 drawings, STEP | 2, 8, 12 | `5_cad/solidworks/` (counted 19 Oct) | COMPLETED AND VERIFIED |
| 27 | CAD checks: 99 pass, 0 fail, 5 wait for E2 | 2, 8, 12, 17 | `5_cad/verify_cad_report.md`, re-run 19 Oct 23:21 in SolidWorks | COMPLETED AND VERIFIED |
| 28 | Seal clash 9.0 mm³ found and fixed: seal starts at x = 23 mm, 0 interference | 8, 16, 17 | `verify_cad` report; `3_decisions/decisions.md` D-013 | COMPLETED AND VERIFIED |
| 29 | Pin force 0.72 N each (2.9 N); lid bending 11 µm; alignment 0.49 mm of ±1.35 mm; strip strain 0.62 % | 8 | `5_cad/calc_mechanical_report.md` (datasheet inputs) | CALCULATED / SIMULATED |
| 30 | FEA not run (loads under 3 N) | 8 | Stated on the slide | NOT YET COMPLETED |
| 31 | STEP exported in cm, now mm; a drawing showed 0.13 for 0.125 mm, fixed | 16 | Commit `fba39ef`; `verify_cad` STEP checks | COMPLETED AND VERIFIED |
| 32 | Materials: polyimide strip, PETG clamp, acrylic rig, stainless dowels, P75-B1 pins | 8 | `sw_build.py` part properties; BOM | PROPOSED (selected; not bought) |
| 33 | 4 laser files pass 35/35 file checks; nothing lased yet | 2, 9, 12 | `4_sensor_strip/laser_files_check.md` (19 Oct) | COMPLETED AND VERIFIED (files only) / NOT YET COMPLETED (lasing) |
| 34 | Laser machine: 1200 × 900 mm bed, 20 kHz PWM, 98 % cap | 9 (notes) | `C:\LaserCAD\AWCCfg\SysCfg.ini` on the laptop; match to the lab machine pending | COMPLETED AND VERIFIED (laptop config) |
| 35 | "12" is most likely a % PWM command, not watts | 9, 16 | Inference from the config + ref 8 | ESTIMATED |
| 36 | E2: 7 coupons, 2 days, 72 pre-registered samples; pass rules fixed in advance | 2, 9 | `e2_experiment/e2_sample_matrix.csv`, `E2_procedure.md` | PROPOSED (ready, not run) |
| 37 | ERC 0 violations; netlist ↔ firmware ↔ pads 0 mismatches | 2, 10, 12 | kicad-cli 10.0.6 re-run 19 Oct; `check_consistency.py` | COMPLETED AND VERIFIED |
| 38 | Measurement path R1–R3–R5, R6 check, C1, U2 ADS1115, pin map | 10 | `6_electronics/kicad/out/reader_v0_1.net`, `config.h`, `WIRING.md` | COMPLETED AND VERIFIED (design) |
| 39 | ESP32-C3 ₹242 (Probots PRO4607), ADS1115 ₹125 (PRO789), P75-B1 ×100 ₹354 (Hubtronics 05880), in stock | 11 | Shop pages read 19 Oct 2026, incl. GST; **nothing ordered** | COMPLETED AND VERIFIED (price check) |
| 40 | Prototype total ≈ ₹2,259–6,942 | 11 | Builder sum of `bom_v0_1.csv` groups (leaves out the borrowed meter, USB cable, E4 dressings) | ESTIMATED |
| 41 | Strip ≤ ₹100 | 5 | Requirement R8 | ESTIMATED (target) |
| 42 | "up to 44.9 %" early changes a reliable alert could avoid | 5 | Upper bound from ref 1; caveat in notes | ESTIMATED (projection) |
| 43 | A ≤ ₹100 strip pays for itself if 1 in 2–5 changes is avoided (strip only; reader reused) | 5 | 100 ÷ 242–514 = 0.19–0.41 | ESTIMATED (projection) |
| 44 | Alert within ±10 % of the visible front | 5 | E4 plan | PROPOSED (target) |
| 45 | Concept scores 4.36 / 4.29 / 3.96 / 3.46 / 3.39 | 13 | `3_decisions/decision_matrix.md` | COMPLETED AND VERIFIED (file; scores are judgement) |
| 46 | FMEA top 5: 224 / 210 / 150 / 140 / 120 of 15 modes | 14 | `3_decisions/fmea_v0_1.csv` (F15 also 120) | ESTIMATED (ratings before tests) |
| 47 | Standards ISO 14971, IEC 60601-1, ISO 10993-1, EN 13726, IEC 60825-1 | 14 | Design intent | PROPOSED ("considered, not claimed") |
| 48 | Roadmap: prototype video in early Dec, semi-final interview in Jan, IIT Indore finale 26 Jan – 1 Feb; gates G1–G4 | 15 | vishwakarma-awards.org (L42), Internshala (L43); D-014 | PROPOSED (plan on the organisers' dates) |
| 49 | 15 dated git commits since 14 Oct; native files available | 12 | `git log` | COMPLETED AND VERIFIED |
| 50 | Scripts written with AI assistance (Claude), directed by the team, build the CAD, schematic and firmware | 12, 19 | `Co-Authored-By` lines in every commit; lab notebook | COMPLETED AND VERIFIED |
| 51 | Team: Soham Prabhakar Kadu, Bhakti Ajay Kadam; Sanjivani University; ID VK26-IITI-HT-0050; Health Tech / Emergency Response & Remote Monitoring | 1, 2 | Shortlist email; team instruction | As registered; **roles: team to add** |
| 52 | Lab photos with ID badges | 2, 12 | Placeholders only | NOT YET COMPLETED (team) |
| 53 | Repository link | 12 | Placeholder; zip prepared | NOT YET COMPLETED (team) |

## References as printed on slide 18

| # | Source | Reading depth | Link check |
|---|---|---|---|
| 1 | Milne S.D. et al., Int. Wound J. 13(6):1309–1314 (2016), doi:10.1111/iwj.12521 | full text | DOI resolves |
| 2 | Dressing IFUs (foam dressings: ~2 cm rule; Mepilex Border Flex: 3 edges) | excerpts | brochure URL resolves |
| 3 | McColl D. et al., Int. J. Surg. 5(5):316–322 (2007), doi:10.1016/j.ijsu.2007.02.008 | abstract | DOI resolves |
| 4 | US 5,469,145; US 5,838,240; US 9,291,589; US 10,928,344 | summaries | 2 of 4 pages opened |
| 5 | Jiang Y. et al., Nat. Biotechnol. (2022), doi:10.1038/s41587-022-01528-3 | listing + coverage | DOI resolves |
| 6 | Dealey C., Cameron J., Arrowsmith M., J. Wound Care 15(4):149–153 (2006) | abstract | repository page opened 15 Oct |
| 7 | Lin J. et al., Nat. Commun. 5:5714 (2014), doi:10.1038/ncomms6714 | full text | DOI resolves |
| 8 | softsolder.com, CO₂ tube current vs PWM (2022) | not peer-reviewed | resolves |
| 9 | Li Y. et al., Adv. Mater. 29:1700496 (2017), doi:10.1002/adma.201700496 | abstract | DOI resolves |
| 10 | EN 13726-1:2002 / EN 13726:2023 | catalogue entry | **not reachable (stated)** |
| 11 | DuPont position statement on medical applications | web page | resolves |
| 12 | TI ADS1115 datasheet (SBAS444); Espressif ESP32-C3 datasheet | vendor documents | ESP32-C3 PDF resolves |
| 13 | Wounds UK news, 22 Aug 2018 (Mölnlycke survey) | web page; patient-reported, industry-sponsored | opened 19 Oct |
| 14 | Smith+Nephew ALLEVYN LIFE product page | manufacturer page | opened 19 Oct |
| 15 | Truemeds.in listings, Mepilex Lite / Border 10 × 10 cm | retail pages | Border page opened 19 Oct |

**Image credits:** slide 19 lists all 14 deck figures. They are made from our own files (SolidWorks renders and screen capture, the KiCad export, and plots from our scripts, which were written with AI assistance). No stock photos and no AI image generators are used. Team photos will be the team's own.
