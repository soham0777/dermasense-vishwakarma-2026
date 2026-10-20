> **Superseded (20 Oct 2026).** The submitted deck and the current checklist are in [`FINAL_SUBMISSION/`](../FINAL_SUBMISSION/SUBMIT_CHECKLIST.md). This file is kept as a record.

# User action checklist (team only)

**Already done** (not your job):
- deck rebuilt on your template, 19 slides, QA passed
- sources checked
- no private data and no links in the deck

The items below need **you**.

| # | Do | Pass when |
|---|---|---|
| 1 | **Deadline.** The organiser's email (25 Sep) says "11:59 PM on 25th October 2026", with no timezone; a third-party listing said 16 Oct. If unsure, reply to that email quoting VK26-IITI-HT-0050 | You know the cut-off in writing |
| 2 | **Slide 12: team photo.** Both of you, institutional ID badges visible. Real photo only | Placeholder replaced |
| 3 | **Slide 12: lab photo.** You at work (SolidWorks / KiCad on the laptop, wiring, or the laser) | Placeholder replaced |
| 4 | **Slide 12: roles.** Replace both "[team to add]" | No "[team" text left |
| 5 | **Slide 12: Drive link.** Upload `Desktop/Dermasense_VK26-IITI-HT-0050_repository.zip`, share it as *Anyone with the link: Viewer*, paste the link into the bracketed text. **Do not use a public GitHub repo** if you may file a patent (public disclosure); ask your university's IPR cell first | The link opens in a private/incognito window |
| 6 | **AI line (slides 12 and 19)** says the design scripts were written with AI assistance. No rule forbids it, and git shows it anyway. Keep it, or tell us how to word it | Your decision |
| 7 | **Faculty mentor:** add a joint photo and sign-off **only if** a mentor is really attached | Done or not applicable |
| 8 | **Re-export the PDF** after the edits | 19 pages; searching for "[team" finds nothing |
| 9 | **Submit** through the Design Stage Form in the organiser's email, a day early if you can | Confirmation screenshot in `_private/` |

## How to add the photos and roles

**Option A, in PowerPoint (simplest):**
1. Open `Vishwakarma_Stage2_Refined.pptx`.
2. On slide 12, right-click each placeholder → **Change Picture**, then type the roles and the link.
3. Save, then **File → Export → Create PDF**.

**Option B, rebuild:**
1. Put `team.jpg` and `lab1.jpg` in `Stage2_Review_Output_2026-10-20/team_photos/`.
2. Put the roles and link in `build/build_refined.py` (function `maker`).
3. Run `python build/build_refined.py`, then `python build/qa_refined.py`.

A rebuild overwrites Option A edits, so use only one method.

## Before the December prototype video (not needed for this upload)

- Run the **E2** laser experiment and record real measurements.
- Wire the reader and run **bench test T0–T11**, including Bluetooth.
- Add **FEA** only if it is actually run in SolidWorks Simulation, which is licensed on this PC.
- Decide whether any new result is verified enough to add before the video.

**This is a design-stage proposal:** no physical prototype exists yet, and the deck says so.
