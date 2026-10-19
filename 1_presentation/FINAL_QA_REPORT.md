# Final QA report: Vishwakarma Stage 2 deck (refined)

**Date:** 19 Oct 2026. Replaces `PPT_QA_Report.md` (in git history).

**Files:** `FINAL_SUBMISSION/Vishwakarma_Stage2_Final.pptx` (editable source) and `Vishwakarma_Stage2_Final.pdf` (exported by PowerPoint from that PPTX).

**Status:**
- **QA passed for layout and content.**
- **Not yet ready to upload.** The team must add photos, roles and the repository link (`../STAGE2_REMAINING_ACTIONS.md`), then re-export the PDF.

## Method

1. **Automated:** `qa_deck.py` opens the PPTX in Microsoft PowerPoint, measures every rendered text box, table and picture, checks section order and limits against the template, checks fonts, exports the PDF and checks it. Raw output: `qa_results.json`.
2. **Visual:** every one of the 19 slides was rendered from the PDF and inspected by eye, at slide size and zoomed. Each new figure was also inspected on its own.
3. **Content:** every number on the slides was traced to its source (`CLAIM_EVIDENCE_MATRIX.md`, 53 claims). Tool results were re-run on 19 Oct.

## Automated results

| Check | Result |
|---|---|
| Slides | **19**, 13.33 × 7.5 in |
| Template sections in order | **Yes** (cover → Problem Context ×2 → User Journey ×2 → Architecture ×2 → CAD ×2 → Electronics ×2 → Maker Journey ×2 → Safety → Roadmap → Challenges → Solutions → References → Image Sources) |
| Section limits | **All within limits** (every 1–2 section uses 2; 19 is the most the template allows) |
| Text overflow / overlap / off-slide | **0 / 0 / 0** |
| Pictures under 150 dpi | **0** |
| Fonts | Poppins SemiBold, DM Sans, DM Sans Medium embedded from the template |
| PDF | 19 pages, same size, fonts subset-embedded; no animations, videos, links to media or hidden content |
| Template file | MD5 `c58ef4fe…`, unchanged |

## Visual inspection (by eye)

| Slide | Finding | Action |
|---|---|---|
| 2 | Empty space under the list | 3 real thumbnails added |
| 6 | "How it works" labels clipped and overlapping (first draft) | Figure redrawn; checked |
| 8 | Legend text overlapping (first draft) | Two-line legend; checked |
| 10 | Capacitor symbol and notes overlapping the KiCad thumbnail (first draft) | Figure redrawn; checked |
| 12 | Tool-output columns overlapping (first draft) | One result per line; checked |
| 14 | 5th FMEA row touching the panel edge | Panels re-spaced; checked |
| All | No clipped text, no unreadable tables; smallest figure text is about 6 pt at full-screen PDF size (in figure captions and the KiCad thumbnail, which is shown as evidence, not for reading) | – |

## Content audit

- **Every number on the slides matches its source:**
  - `config.h` thresholds
  - `calc_readout_report.md` (4.2–14.8 kΩ, 32 µA)
  - `calc_mechanical_report.md` (0.72 N, 11.2 µm, 0.49 / 1.35 mm, 0.62 %)
  - `strip_v0_1_geometry.json` (1.0 mm lines and gaps, 5.08 mm pitch, 75 mm pad)
  - FMEA RPNs
  - BOM sum
  - test counts
- **Pin map (slide 10)** matches `config.h` and the netlist; `check_consistency.py` reports 0 mismatches.
- **Firmware excerpt (slide 12)** is checked against `zone_logic.h` by `make_figures.py`, so it cannot drift.
- **Present tense is used only for things that exist.** Bluetooth, the phone and the reader are described as "designed", "compiled" or "hardware test pending".

## Final quality questions

| # | Question | Answer |
|---|---|---|
| 1 | Can a non-technical person explain what Dermasense does? | Yes: slides 3–6 (problem → journey → "how it senses" figure in three plain steps) |
| 2 | Real-world problem and intended user clear? | Yes: slide 3 (nurses and home carers; covered dressings) |
| 3 | Sensing mechanism explained correctly? | Yes: slide 6; labelled as a concept until E2/E4 |
| 4 | Innovation specific and defensible? | Yes: reading the maker's change line electrically, with an order check (slides 2, 13); prior art cited (refs 1, 4, 5, 14); "in our search" qualifier kept |
| 5 | Engineering work visible? | Yes: slides 2, 6–12 show real CAD, schematic, firmware, laser files and tool output |
| 6 | Mechanical and electronic architecture understandable? | Yes: annotated exploded view (8), measurement path + pin map (10) |
| 7 | Remote monitoring represented accurately? | Yes: a Bluetooth broadcast, compiled and tested in software, not on hardware; no app; nearby range only (slides 5, 7) |
| 8 | Research connected to design decisions? | Yes: slides 3, 9, 13 (refs → change line, sealing, pivot) |
| 9 | Calculations, costs and tests traceable? | Yes: Basis columns on slides 6 and 8; SKUs on 11; tool output on 12; matrix |
| 10 | Completed vs proposed distinguished? | Yes: status pill on every slide, Basis columns, "Not yet" line on slide 2 |
| 11 | Limitations disclosed? | Yes: nothing built, FEA not run, BLE untested, no photos yet, AI assistance stated |
| 12 | Every template section present? | Yes: 13 sections in the template's order |
| 13 | Team slide ready for photos? | Yes: slide 2 (and lab photos on 12); placeholders are pictures for *Change Picture* |
| 14 | Slide count compliant? | Yes: 19, the maximum the section limits allow |
| 15 | PDF works without animation or video? | Yes |
| 16 | Every important claim defensible ("how do you know?")? | Yes: see `CLAIM_EVIDENCE_MATRIX.md` |
| 17 | Genuine progress shown, not just an idea? | Yes for design and software. **No physical progress yet**, and the deck says so. E2 is the next proof |

## Open items (team)

| Item | Where | Status |
|---|---|---|
| Team photos and roles | Slide 2 | Placeholders |
| Lab photos with ID badges | Slide 12 | Placeholders |
| Repository / Drive link | Slide 12 | Placeholder |
| Re-export the PDF after the edits | `FINAL_SUBMISSION/` | Required before upload |
| Deadline confirmation | – | Email says 25 Oct 23:59; listing says 16 Oct |
