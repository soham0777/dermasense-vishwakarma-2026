# Project audit: Dermasense, Stage 2

**Audit date:** 19 Oct 2026, from the files themselves, not from earlier status reports. Checks were re-run today where a tool exists.

**Authoritative version:**
- Project root: `C:\Users\dell\OneDrive\Desktop\MBF vishwakarma` (it has not moved).
- Git branch `dev/stage2-rebuild`, commit `9626ef0`; working tree clean at the start of the audit.
- Deck: `FINAL_SUBMISSION/Vishwakarma_Stage2_Final.pptx` / `.pdf`, built 19 Oct 23:00 by `1_presentation/build_deck.py`.
- Official template: `1_presentation/template/…Template (2).pptx`, MD5 `c58ef4fe526045f1a82a806e6532bc3c`, unchanged.
- Older versions are kept in git: the v2 deck (`5e7d08d`), the full deck before decluttering (`a5e776f`) and the decluttered deck (`86a7ac3`).
- `Desktop/MBF vishwakarma_TO_DELETE/` holds the old v1 archive and backups, which the team has not yet deleted. They are not used as evidence.

---

## 1. What the team proposed in Stage 1

From the Stage 1 proposal (`_private/`, 3 pages):
- **Product:** "Dermasense", an active, closed-loop wireless smart bandage on laser-induced graphene (LIG) on Kapton.
- **Sensing:** AC impedance spectroscopy (1–100 kHz) of tissue and temperature telemetry.
- **Therapy:** galvanotaxis electrotherapy (10–100 µA).
- **Electronics:** an ESP32-C3 BLE module clipped on with magnets.
- **Dressing:** a thermo-responsive hydrogel for painless removal.
- **Cost:** a patch under $1.50.
- **Plan:** 4 phases over 16 weeks.
- **Unsupported claims in it:**
  - "Kapton is medical-grade"
  - "reduce dressing changes by over 60 %"
  - sheet resistance "< 150 Ω/sq"

The Stage 1 proposal was submitted before this repository existed. Who wrote it is not recorded here.

## 2. What changed after Stage 1 (14 Oct onward)

| Stage 1 | Stage 2 design | Decision |
|---|---|---|
| Tissue impedance spectroscopy | Two-zone wet/dry resistance strip at the dressing maker's change line | D-012 |
| Temperature telemetry | Future scope | D-002 (superseded) |
| Electrotherapy | Dropped: therapy carries regulatory risk, has been shown at lab scale (Jiang 2022), and DC on LIG makes H₂O₂ | D-003 |
| BLE module | ESP32-C3 reader with a **BLE state broadcast** (no extra hardware) | D-004, D-015 |
| "Graphene" | "Laser-carbonised, LIG-like" until a Raman test | D-009 |
| "Kapton medical-grade", "60 % fewer changes" | Both withdrawn; corrected on slide 12 | 19 Oct review |
| Hydrogel, cost < $1.50 | Out of scope; strip ≤ ₹100 is a target (estimate) | requirements R8 |

## 3. Research performed

- **41 sources** in `2_research/literature.csv`. Each records how it was verified: full text, abstract, listing or excerpt.
- **16 key sources** compared side by side in `research_matrix.csv`.
- **Research gap analysis** (`research_gap.md`): 8 aspects, each with "what would kill the contribution".
- **Critique** of one uploaded paper (Rezaei 2024), not used as evidence because it is simulation only and physically implausible (D-007).
- **Prior-art search** (not exhaustive):
  - WoundSense (reads one point)
  - a moisture-map study (McColl 2007)
  - 4 diaper-wetness patents
  - a closed-loop smart bandage (Jiang 2022)
  - ALLEVYN LIFE's visual change indicator
- **Competition sources** (read 19 Oct): the official website, the Internshala listing, the shortlist email and the template.
- **Not yet done:**
  - nurse or carer interviews (the guide exists: `interview_guide.md`)
  - a formal patent search
  - measurements of nurse time in Indian clinics

## 4. Designs created (all digital; nothing has been fabricated)

| Area | What exists | Files |
|---|---|---|
| Sensor strip | Two-zone strip v0.1 (10 mm wide, 96 mm long, windows 6 × 3.9 mm, 1.0 mm lines/gaps, 4 pads at 5.08 mm, 2 dowel holes), a seal-tape layer and a design-rule check | `4_sensor_strip/make_strip.py` → `strip_v0_1.dxf`, `_encap.dxf`, `_geometry.json`, `_drc.txt` |
| Laser test coupons | E2 resolution coupon (5 line widths, 6 gaps, 3 holes) and a 6-cell bracket coupon | `e2_res_coupon.dxf`, `lig_test_coupon.dxf` |
| Mechanical (SolidWorks 2019) | **9 parts, 1 assembly (13 components with mates), 7 A3 drawings, 10 STEP files**: strip, seal, clamp base, clamp lid, pogo pin, dowel, rig base, wound-bed spacer, reference dressing | `5_cad/solidworks/`, built by `5_cad/sw_build.py` |
| Electronics (KiCad 10) | Two-zone reader schematic: ESP32-C3 SuperMini, ADS1115, 100 kΩ 0.1 % reference and check resistors, 1 kΩ protection, 10 nF C0G, 3 LEDs, 4-pin strip connector; netlist, BOM and PDF exports | `6_electronics/kicad/` |
| Firmware | `reader_v0_1` (477 lines): bipolar measurement, ratiometric ADC, self-check, hysteresis + 3-scan persistence, OK / CHANGE / CHECK / FAULT, CSV over USB, **BLE advertisement (13-byte payload)** | `7_firmware/reader_v0_1/` |
| PC tools | Validated serial logger, netlist ↔ firmware ↔ pad cross-check (writes `WIRING.md`), BLE payload decoder | `7_firmware/tools/` |
| Experiment design | E2 fabrication validation: procedure, safety checklist, **72 pre-registered samples**, 17-page bench sheets, CSV templates, analysis script | `4_sensor_strip/e2_experiment/` |
| Risk and requirements | Design FMEA (15 modes), requirements R1–R11 + R3a with tests, decision log D-001…D-015, decision matrix (5 concepts × 13 criteria), evidence register (22 claims) | `3_decisions/` |
| Deck | 18 slides on the official template, built by script; all figures generated from project files | `1_presentation/`, `FINAL_SUBMISSION/` |

## 5. Calculations (engineering estimates, not measurements)

- **Readout (`6_electronics/calc_readout_report.md`):**
  - expected wet reading 4.2–14.8 kΩ, dry ≥ 1 MΩ
  - excitation ≤ 33 µA
  - why a 100 kΩ reference
- **Mechanics (`5_cad/calc_mechanical_report.md`):**
  - pin compression 1.48 mm → 0.72 N per pin, 2.9 N total
  - lid deflection 11 µm
  - tolerance stack 0.49 mm vs ±1.35 mm allowed
  - bending strain 0.62 % at 10 mm radius
  - 20 MPa vs 231 MPa at the dowels
  - pointed-tip contact stress 23 MPa
- **Cost (`6_electronics/bom_v0_1.csv`):** 23 lines.
  - Prices quoted 19 Oct: ESP32-C3 SuperMini ₹242 (Probots PRO4607), ADS1115 ₹125 (Probots PRO789), P75-B1 ×100 ₹354 (Hubtronics 05880).
  - Everything else is an estimate.
  - Prototype total ≈ ₹2,259–6,942; all 23 lines ≈ ₹2,559–8,042.
- **No FEA has been run.** SolidWorks Simulation is licensed on this PC, so it could be done.

## 6. Tests run (re-run on 19 Oct unless stated)

| Check | Result | Scope |
|---|---|---|
| CAD verification (`verify_cad.py`, SolidWorks) | **99 pass, 0 fail, 5 blocked** (re-run 19 Oct 23:21) | Units, volumes, interference, drawings, STEP. The 5 blocked checks wait for E2 data |
| Laser file checks (`verify_laser_files.py`) | **35 / 35 pass** | DXF files only; not proof of fabrication |
| KiCad ERC | **0 violations** (KiCad 10.0.6, re-run 19 Oct) | Schematic rules only |
| Netlist ↔ firmware ↔ strip pads | **0 mismatches** | Design consistency |
| Firmware compile (ESP32-C3) | **0 warnings, 650,349 bytes (49 %)** | Builds; **never run on a board** |
| Firmware compile-time tests | **23 `static_assert`** (19 logic + 4 BLE payload); a deliberately wrong one breaks the build | Logic only |
| PC-side tests (pytest) | **16 pass** (10 logger/cross-check + 6 BLE decoder) | Software only |
| E2 analysis tests | **3 pass**, on synthetic data | The analysis script, not the process |
| **Physical tests** | **None.** No laser run, no strip, no board, no dressing test | – |

## 7. Verified vs not verified

**Verified (by a tool, today):**
- the files exist and are consistent with each other
- the CAD passes its geometric checks
- the schematic passes ERC
- the firmware builds and its logic tests pass
- the laser files pass their file checks

**Not verified:**
- that the laser makes a conductive layer on our film (E2)
- line width, gap and hole size as built
- that the strip senses moisture
- the wet/dry thresholds
- that the reader works on hardware, including BLE (bench test T0–T11)
- pogo-pin contact
- bending durability
- behaviour on a real dressing (E4)
- user value (no interviews)
- the cost of a strip

## 8. Work that is missing

| Missing | Needed for | Who |
|---|---|---|
| Lab photos with ID badges | Template, Maker Journey | Team |
| Repository / Drive link | Template, Maker Journey | Team |
| Team details (photos, roles) | Project Overview slide | Team |
| Any physical measurement (E2) | Effectiveness criterion | Team at the laser |
| FEA plot and mesh study | Template, CAD + Maker Journey (optional) | Can be done in SolidWorks Simulation |
| Nurse interviews | Quantified user-journey numbers | Team |
| Faculty mentor sign-off | Template example (only if a mentor exists) | Team |
| Written confirmation of the deadline | Submission | Team |

## 9. Claims in the 19 Oct deck that were weak or misleading (fixed in the refinement)

| Slide | Claim | Problem | Fix |
|---|---|---|---|
| 18 | "Every image … produced by the team … No AI-generated images" | The figures were made by scripts written with AI assistance; "produced by the team" overstates it | "Made from our own project files … no stock photos, no AI image generators"; AI assistance stated on Maker Journey |
| 4 | "the state **is broadcast** over Bluetooth to a phone" | Present tense reads as working hardware | "designed to broadcast …; firmware done, hardware test pending" |
| 4, 5, 6 | "phone" | No phone app exists; any BLE scanner app reads it | "any Bluetooth scanner app (no custom app yet)" |
| 4 | Strip payback "1 in 2–5 changes" | Leaves out the reader cost | Labelled "strip only; the reader is reused" |
| 1 | "a laser-written strip **that reads** …" | Implies a working device | "designed to read" |
| 7 | "99 automated CAD checks pass, 0 fail" | Omits the 5 blocked checks | "99 pass, 0 fail, 5 wait for E2 data" |
| 9 | Full KiCad sheet shrunk to fit | Unreadable at slide size; template asks for a clear pinout | Legible crop of the real measurement circuit + pin table |
| 7, 9, 13 | Engineering numbers, pin map, materials reasons, FMEA effects | Removed in the 16 Oct declutter, so the invention looked thin | Restored visibly, in compact tables and annotated figures |
| 5 | Block diagram shows only status ticks | Doesn't explain **how** the strip senses | New "how it works" figure: dry gap → wet bridge → reader → state |

No claim in the deck says the sensor works, that graphene was made, or that there is any clinical benefit.

## 10. Strongest evidence of real progress

1. **SolidWorks native files + drawings + automated verification.** The verification found a real design error (seal tape trapped under the clamp, 9.0 mm³), which was fixed (D-013).
2. **KiCad schematic + ERC + a script that cross-checks the netlist, firmware pins and strip pads.**
3. **Firmware with tests that run at compile time**, and a PC logger with tests.
4. **Laser files + checks + the E2 experiment, pre-registered before any data** (pass rules fixed in advance).
5. **Design FMEA that found an undetectable failure (F04)** and drove the v0.2 redesign.
6. **Decision log and git history** (15 dated commits, 14–19 Oct) showing the reasoning.

## 11. Who did what (stated plainly)

| Kind of work | What | Evidence |
|---|---|---|
| **Team** | Stage 1 proposal and shortlisting; choice of problem and theme; access to the laser, SolidWorks and KiCad; the earlier laser trial ("setting 12", recalled, not recorded); direction and approval of decisions (D-009 by team brief, D-011 by team feedback); review of the decks | Email, Stage 1 PDF, decision log |
| **AI-assisted (Claude, on the team's laptop, at the team's request)** | Python scripts that build the CAD and schematic; firmware; calculations; E2 experiment package; FMEA; research matrix; documents; figures; deck builder | Every commit 14–19 Oct carries a `Co-Authored-By: Claude` line; lab notebook entries say "Claude, for the team" |
| **External (cited)** | Literature, manufacturer pages, retail prices, competition rules | `2_research/literature.csv` |
| **Needs human confirmation** | Team roles; whether a mentor is attached; the laser machine's details (tube, lens, mA meter); film identity and thickness; the deadline | `machine_record.md`, `STAGE2_REMAINING_ACTIONS.md` |

**What this means:**
- The design work is real, consistent and verifiable in software.
- The **physical** work (laser, wiring, testing) has not started, and it must be done and documented by the team. The official rules require a working hardware prototype at the next stage.
- The team should be able to explain every design choice in the January interview. The decision log and this audit are the study material.

## 12. Competition rules (checked 19 Oct)

- **Deliverable:** a "PPT deck" of design specifications, submitted via the Design Stage Form in the organiser's email. The team reports that a PDF is what gets uploaded.
- **Slide count:** none stated. The template sets per-section limits that allow up to 19 slides (see `1_presentation/TEMPLATE_EVIDENCE_MAP.md`).
- **Deadline:** the email says 25 Oct 2026, 23:59. The website says only "Submit Oct". The Internshala listing says 16 Oct. **This is unresolved; the team must confirm.**
- **Criteria:** relevance, effectiveness, clarity, uniqueness, patentability ("IP shall belong to team members"), commercial viability, fact check, ease of use.
- **Rules:**
  - "Only work done during the program timeline will be evaluated." Our work dates from 14 Oct.
  - A working hardware component is required.
- **AI tools:** no rule found.
- **Public disclosure:** no rule found. A public repository could affect patentability; ask the university IPR cell.
