# PPT QA report: Vishwakarma Stage 2 final deck

**Date:** 19 Oct 2026 (gap-review version; the decluttered version of 16 Oct is in git history).

**Files:** `FINAL_SUBMISSION/Vishwakarma_Stage2_Final.pptx` (4.5 MB) and `.pdf` (1.7 MB, exported by PowerPoint).

**Method:**
- `qa_deck.py` opens the deck in **Microsoft PowerPoint** and measures every rendered text box, table and figure. Raw output: `qa_results.json`.
- Every changed slide was then reviewed by eye.

## Final status

**READY FOR SUBMISSION, after one team action:** replace the bracketed repository placeholder on slide 11 with the real link. The full submission checklist is `../STAGE2_CHECKLIST.md`.

## What changed on 19 Oct, and why

A full review against the template, the organiser's website and the Stage 1 proposal (`../STAGE2_CHECKLIST.md`) found these gaps. Each one is closed in the deck:

| Gap found | Slide | Fix |
|---|---|---|
| Roadmap ran Nov → Feb, past the December prototype video and the IIT Indore finale (26 Jan – 1 Feb) | 14 | Plan and figure moved onto the programme's own dates (decision D-014) |
| Template asks for time, material and cost numbers; the slide said "not estimated" | 3 | Cited numbers: ≈ 18 min a visit (ref 13), ₹240–510 a dressing (ref 15) |
| "Quantified efficiency" had targets only | 4 | "up to 44.9 %" early changes, and the strip's payback, both labelled as projections |
| Sub-theme is *Remote Monitoring*, but the reader had no radio ("BLE later") | 4, 5, 6, 12 | Bluetooth state broadcast added to the firmware (compiled and tested in software, not on hardware; D-015) |
| BOM had no real prices; template wants part numbers, quantities, sources | 10 | Template table form; 3 key parts quoted on 19 Oct |
| A visual change indicator already exists (ALLEVYN LIFE) and was not cited | 2, 12 | Cited as prior art (ref 14); novelty stated as reading the line electrically |
| Stage 1 wrongly called Kapton "medical-grade" | 12 | Corrected openly (ref 11) |

| Measure | 16 Oct | 19 Oct |
|---|---|---|
| Words on content slides 2–16 | 1,476 | 1,563 |
| Average words per content slide | 98 | **104** (rule: about 100) |
| Most words on one slide | 140 (slide 16) | 143 (slide 16) |
| References | 12 | 15 |

## Template compliance

| Check | Result |
|---|---|
| Official template | `template/Vishwakarma Awards 2026-27 Stage 2 Submission Template (2).pptx`; MD5 `c58ef4fe…` unchanged |
| Design | Each section reuses the template's own example slide (logos, title, panels, icons, metric cards, rationale bar) |
| Section order | Correct: cover → Problem → User Journey → Architecture → CAD → Electronics → Maker Journey → Safety → Roadmap → Challenges → Solutions → References → Image Sources |
| Slide limits | All within limits (Journey, Architecture, CAD, Electronics, Maker Journey: 2 each; the rest: 1) |
| Slide count / size | 18, 13.33 × 7.5 in |

## Measured checks (PowerPoint layout engine)

| Check | Result |
|---|---|
| Text overflowing its box | **0** |
| Overlapping content | **0** |
| Content off the slide | **0** |
| Pictures under 150 dpi | **0** |
| Fonts | Poppins SemiBold, DM Sans and DM Sans Medium are **embedded** (from the template). The only non-embedded run is the template's own cover heading |
| PDF | 18 pages, 13.33 × 7.5 in, fonts subset-embedded; all slide titles found in the PDF text |

## Open items (stated in the deck, not hidden)

| Item | Where | Action |
|---|---|---|
| Repository link | Slide 11 (bracketed placeholder) | **Team:** create the Drive / GitHub link and paste it in (see the checklist for the IP note) |
| Lab photos with ID badges | Slide 11 says none yet | Photograph the team modelling in SolidWorks / KiCad now, and the first laser session (E2) |
| Faculty sign-off, institution name | Not shown (not confirmed) | Team decides |
| Measured results | Not claimed anywhere | Run E2, the reader bench test (T0–T11), then E4 |
