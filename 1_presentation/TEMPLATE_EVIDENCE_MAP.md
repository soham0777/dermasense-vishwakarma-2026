# Template → evidence map

**Date:** 19 Oct 2026. Replaces `PPT_Asset_Index.md` (in git history).

**Template:** `template/Vishwakarma Awards 2026-27 Stage 2 Submission Template (2).pptx`, 20 slides, MD5 `c58ef4fe…`, never edited. It was read twice: once for what it asks, once against our files.

## What the template is made of (first reading)

| Template slide | Kind | What it says |
|---|---|---|
| T1 | Cover | "Vishwakarma Awards 2026-27 · Vishwakarma Application ID" |
| T2 | Guideline | **Problem Context (1–2 slides).** "Slide 1 & 2": **Project Overview** (title, Team ID, track, 1-line core innovation) and **Problem Statement** (operational pain point, exact target beneficiary) |
| T3 | Guideline | **User Journey (1–2).** Before-state flowchart/storyboard + **quantified inefficiency** (time loss, material waste, labour cost, safety hazards). After-state flowchart + **quantified efficiency** |
| T4 | Example | Problem Context & User Journey: 4 metric cards, photo, target user, bottleneck, before-state flow, public search disclosure |
| T5 | Guideline | **System Architecture & Specs (1–2).** Block diagram (mechanical, actuation/power, controllers, firmware/logic); target specifications; **exact** MCU, driver, sensors, protocols |
| T6 | Example | Figure + 3-column spec table (parameter, target, hardware) + architecture rationale bar |
| T7 | Guideline | **CAD Design & Mechanical Specs (1–2).** Isometric **and exploded** renders; material selection by stress and weight; **FEA / stress analysis** |
| T8 | Example | Exploded render + "Mechanical Validation & FEA Stress Report" + design-iteration bar |
| T9 | Guideline | **Electronics Schematics & BOM (1–2).** Pinout diagrams, power distribution, voltage regulation; **itemised BOM** (exact part numbers, qty, unit cost, total); local vs imported with **verified lead times** |
| T10 | Example | Schematic + 5-column BOM table + procurement-status bar |
| T11 | Guideline | **Your Maker Journey (1–2).** **Lab photos of team members with institutional ID badges**; joint photo with the faculty mentor if attached; CAD UI with the feature tree; EDA with rule-check logs; FEA convergence; **Drive / GitHub link with native files**; timestamps audited; no embedded videos |
| T12 | Example | Team photo + "Stage 1 to Stage 2 Engineering Iterations" + institutional sign-off bar |
| T13 | Guideline | **Safety & Hazard Mitigation (1).** Physical fail-safes, FMEA matrix, standards |
| T14 | Guideline | **Roadmap (1).** 4-month fabrication plan; **Stage 3 commitment** |
| T15 | Example | FMEA table + two roadmap panels (months 1–2, 3–4) |
| T16 | Guideline | **Technical Challenges & Risks (1).** Engineering bottlenecks |
| T17 | Guideline | **Potential Solutions & Risk Mitigation (1).** Backup solutions, fallback logic |
| T18 | Example | 3 cards (bottlenecks + standards) + empirical-verification bar |
| T19 | References | "Mention the references and sources used in your PPT" |
| T20 | Image sources | URL + source for every image |

**Findings:**
- The template has **no separate team-introduction slide**. Team photos are required on the **Maker Journey** slide.
- The **Project Overview** may be its own slide (the first of the two Problem Context slides). That is where the team slide goes.
- The 10 guideline slides and 7 example slides are instructions; they are replaced by our content, not submitted.
- **Maximum length** within the section limits: 1 + 2 + 2 + 2 + 2 + 2 + 2 + 1 + 1 + 1 + 1 + 1 + 1 = **19 slides**. No total slide count is stated anywhere (the website says only "a PPT deck of design specifications").

## Slide-by-slide map (second reading): final deck of 19 slides

| # | Final slide | Template asks | What we have (files) | Visual | Missing / to create | Judge should understand | Must not be removed |
|---|---|---|---|---|---|---|---|
| 1 | Cover | Application ID | Shortlist email (ID VK26-IITI-HT-0050) | Template cover | – | Who we are, which ID | ID, title, track |
| 2 | **Project Overview & Team** (new) | Title, Team ID, track, 1-line innovation | Email; `README.md`; `PROJECT_AUDIT.md` (Stage 2 output counts) | **Photo placeholders for the team** | **Team photos, roles (team adds)** | Who the team is; the one-line idea; how much was built | ID, track, one-line innovation, what Stage 2 produced |
| 3 | Problem Context | Pain point + exact beneficiary | `2_research/literature.csv` L08, L26, L28, L40; `research_gap.md` | `fig_problem.png` (to scale, from `strip_v0_1_geometry.json`) | – | Carers can't see when a covered dressing is full | Cited numbers 1–4, 14; "in our search" qualifier |
| 4 | User Journey: Before | Flowchart + time / material / cost loss | Refs 1, 6, 13, 15 | `fig_journey_before.png` | Indian nurse time (interviews) | Today's checks are guesses; each costs time and a dressing | 44.9 %, 18 min, ₹240–510, exudate range |
| 5 | User Journey: After | Flowchart + quantified gain | Firmware states; ref 1; BOM | `fig_journey_after.png` | Measured gain (E4) | Same routine, clear signal, no unwrapping | "Intended / not validated"; projections labelled |
| 6 | Architecture: **How it works** & specs | Block diagram, target specs, exact hardware | `sensor_selection.md`, `calc_readout_report.md`, `config.h`, geometry JSON, netlist | **New `fig_howitworks.png`**: dressing layers → dry vs wet gap → signal path | Plain-English mechanism (it was missing) | How a wet pad becomes OK / CHANGE | Mechanism, spec values with their basis (calc / datasheet / E2) |
| 7 | Architecture: Firmware, data flow & remote view | Firmware/logic flow, protocols | `7_firmware/reader_v0_1/*`, `ble_beacon.h`, `tools/` | `fig_dataflow.png` | Hardware test (T0–T11) | What the reader decides, and how the state leaves the reader (LEDs, USB, BLE) | Test counts (23 + 16), "not run on hardware", BLE limits |
| 8 | CAD: Mechanical | Iso + exploded renders, materials, FEA | `5_cad/solidworks/*`, `calc_mechanical_report.md`, `verify_cad_report.md` | **New annotated exploded render** (`fig_cad.png`), real SolidWorks images | **FEA not done** (stated); hand calculations shown | A clip-on clamp holds the strip on 4 spring pins; checked in CAD | Part list, materials and why, 5 key calculations, 99/0/5 checks, D-013 fix |
| 9 | CAD: Strip & laser process | Mechanical spec of the sensor, fabrication | `4_sensor_strip/*.dxf`, `laser_files_check.md`, `e2_experiment/*`, `machine_record.md` | `fig_strip.png` | E2 results | The strip is laser-written; E2 will prove sizes | 35/35 file checks (files only), E2 plan + pass rules, "LIG-like" |
| 10 | Electronics: Schematic & pinout | Pinout, power distribution, regulation | `6_electronics/kicad/*` (netlist, ERC), `WIRING.md` | **New `fig_schematic.png`**: measurement path drawn from the netlist + the real KiCad sheet | Wiring and bench test | The circuit that reads each zone, and how it checks itself | Pin/net table, ERC 0, 0 mismatches, power path |
| 11 | Electronics: BOM | Itemised BOM, part numbers, cost, sourcing, lead time | `6_electronics/bom_v0_1.csv` | `fig_window.png` + BOM table | Lead times (shops do not state them) | It is cheap and all parts are sold in India | Quoted prices with SKUs, total, "reader reused" |
| 12 | Maker Journey | Lab photos with ID badges, CAD UI, EDA logs, FEA, repo link | All native files; `verify_cad`, ERC, compile logs; git | **New evidence gallery** (`fig_maker.png`) + **lab photo placeholder** | **Lab photos, repository link (team)**; FEA | The work is real, dated and re-checkable; how AI assistance was used | Native files, checks, git history, honesty about photos and AI |
| 13 | Maker Journey: Iterations | Stage 1 → 2 iterations | `decisions.md`, `decision_matrix.md`, Stage 1 proposal | `fig_decision.png` | – | Why the project changed and what was corrected | Pivot reason, scores, corrections, prior art |
| 14 | Safety & Hazard Mitigation | Fail-safes, FMEA, standards | `fmea_v0_1.*`, `BENCH_TEST.md`, `E2_safety_checklist.md` | FMEA table + `fig_fmea.png` | Tests | Risks are known and each has a check | Top-5 FMEA with effects, fail-safes, standards "considered, not claimed" |
| 15 | Roadmap | 4-month plan + Stage 3 commitment | E2 / bench / E4 plans; website dates | `fig_roadmap.png` | – | What happens by the December video and the finale | Gates G1–G4, real programme dates |
| 16 | Technical Challenges | Bottlenecks | `verify_cad_report.md`, FMEA F04, `machine_record.md` | `fig_challenges.png` | – | Problems we found ourselves | 3 bottlenecks with evidence |
| 17 | Solutions & Mitigation | Backups, fallbacks | Decisions, FMEA | Cards | – | Each risk has a fix or fallback | Fixed / designed / fallback split |
| 18 | References | Sources | `literature.csv` | Text | – | Every number has a source and a reading depth | 15 references |
| 19 | Image Sources | Every image | `make_figures.py`, `render_cad.py` | Thumbnails | – | No stock or AI-generated images | Origin of each image |

## Template requirements we cannot meet yet (stated openly in the deck)

| Requirement | Status | Closed by |
|---|---|---|
| Lab photos with institutional ID badges | Placeholder on slides 2 and 12 | Team photographs |
| Accessible Drive / GitHub link | Placeholder on slide 12 | Team (see IP note in `STAGE2_REMAINING_ACTIONS.md`) |
| Faculty mentor photo / sign-off | Only if a mentor is attached | Team |
| FEA plot, convergence and mesh statistics | Not done; hand calculations shown (loads < 3 N) | Optional: SolidWorks Simulation (licensed on this PC) |
| Verified vendor lead times | Shops state "in stock" only | Check when ordering |
| Quantified time loss from our own users | Cited numbers only | Nurse interviews |
