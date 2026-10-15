# PPT QA report: Vishwakarma Stage 2 final deck (decluttered version)

**Date:** 16 Oct 2026.

**Files:** `FINAL_SUBMISSION/Vishwakarma_Stage2_Final.pptx` (4.5 MB) and `.pdf` (2.1 MB, exported by PowerPoint).

**Method:**
- `qa_deck.py` opens the deck in **Microsoft PowerPoint** and measures every rendered text box, table and figure. Raw output: `qa_results.json`.
- Every slide was then reviewed by eye.

## Final status

**READY FOR SUBMISSION, after one team action:** replace the bracketed repository placeholder on slide 11 with the real link.

## What changed in this version

The team reviewed the deck and found it crowded. It was rewritten to one design rule:

> One message per slide, one large visual, at most 4–5 short points, and a one-line takeaway in the template's rationale bar.

| Measure | Before (15 Oct) | Now (16 Oct) |
|---|---|---|
| Words on content slides 2–16 | 3,128 | **1,472 (53 % fewer)** |
| Average words per content slide | 209 | **98** |
| Panel text size | 9.2–10.4 pt | **11–12 pt** |
| Journey figures | 5 steps with sentences + 3 notes | 4 steps of 3–6 words + 1 highlighted number |
| Block diagram | paragraph per block | title + one line + status per block |
| Spec / BOM / FMEA tables | 3–5 columns | 2–3 columns |

**What moved:**
- Details left the slides for the speaker notes, this folder's claim-check document, and the project files.
- No fact was dropped from the record.
- Four claims regained a qualifier while being shortened:
  - "reported rates span"
  - "can leak"
  - "would lift"
  - "likely a % command"

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
| Repository link | Slide 11 (bracketed placeholder) | **Team:** create the GitHub / Drive link and paste it in |
| Lab photographs | Slide 11 says none yet | Photograph the first laser session (E2) |
| Faculty sign-off, institution name | Not shown (not confirmed) | Team decides |
| Measured results | Not claimed anywhere | Run E2, the reader bench test, then E4 |
