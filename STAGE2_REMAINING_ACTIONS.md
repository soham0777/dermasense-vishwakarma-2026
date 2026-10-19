# Stage 2: what the team still has to do

**Status:** 19 Oct 2026. Replaces `STAGE2_CHECKLIST.md` (in git history).
- The full picture: `PROJECT_AUDIT.md`.
- What the template asks for, slide by slide: `1_presentation/TEMPLATE_EVIDENCE_MAP.md`.

**The deck is refined and checked:**
- 19 slides on the official template, every section present.
- QA: 0 layout issues.
- Every claim traced (`1_presentation/CLAIM_EVIDENCE_MATRIX.md`).

**What is left only you can do.** Each step has a pass check.

## Before 25 Oct (in this order)

| # | Do | Time | Pass when |
|---|---|---|---|
| 1 | **Confirm the deadline.** The organiser's email says **25 Oct 2026, 23:59**; the website says only "Submit Oct"; the Internshala listing says **16 Oct**. Ask in the official WhatsApp group or reply to the organiser's email (quote VK26-IITI-HT-0050) | 10 min | You have the deadline in writing |
| 2 | **Decide on the AI line.** Slide 12 says the CAD, schematic and firmware scripts were written with AI assistance (Claude) under your direction; slide 19 says the same about the figures. No competition rule forbids AI. We recommend keeping these lines because the git history shows it anyway | 5 min | You agree, or tell us to change the wording |
| 3 | **Team photos, slide 2.** Portraits of Soham and Bhakti, institutional ID badges visible. Real photos only | 15 min | Both placeholders replaced |
| 4 | **Roles, slide 2.** Replace "[team to add]" (e.g. design lead, research and testing) | 2 min | No "[team to add]" left |
| 5 | **Lab photos, slide 12.** Two photos of you working: for example, modelling in SolidWorks on this laptop and wiring or at the laser. ID badges in the frame. If you have only one, use it twice or delete the second placeholder | 30 min | Placeholders replaced |
| 6 | **Repository link, slide 12.** Upload `Desktop/Dermasense_VK26-IITI-HT-0050_repository.zip` (all project files + `WORK_HISTORY.txt`; no private files) to Google Drive and share it as *Anyone with the link: Viewer* | 20 min | The link opens in a private/incognito window |
| 7 | **Re-export the PDF.** Option A: in PowerPoint, *Change Picture* / type, then File → Export → PDF. Option B: put the photos in `1_presentation/team_photos/` and the link and roles in `build_deck.py`, then run `build_deck.py` and `qa_deck.py` (see `1_presentation/README.md`). **Don't mix the two:** a rebuild overwrites manual edits | 10 min | PDF has 19 pages and no placeholder is left |
| 8 | **Final check** (below) | 10 min | All boxes ticked |
| 9 | **Submit by 24 Oct** (a day early) through the Design Stage Form in the organiser's email. Rename the file `VK26-IITI-HT-0050_Dermasense_Stage2.pdf` if allowed. Screenshot the confirmation into `_private/` | 15 min | Confirmation saved |

**Optional, but the strongest boost:**
- **Run E2 Session S0 + Day 1** (`4_sensor_strip/e2_experiment/E2_procedure.md`, 4–5 h at the laser). Real measurements are the one thing the deck cannot show yet. Send the filled CSVs and we will add the results to slides 9 and 16.
- **FEA of the clamp in SolidWorks Simulation** (licensed on this PC, about 2 h). It closes the template's FEA request. Ask if you want it.

> **IP note (not legal advice):** a public GitHub repository counts as public disclosure. If you might patent the change-line strip, keep the Drive link view-only and ask Sanjivani University's IPR cell before posting anything publicly.

### Final check before uploading

- [ ] Slide 1: ID `VK26-IITI-HT-0050`; names spelled correctly
- [ ] Slide 2: two real photos; roles filled in
- [ ] Slide 12: real lab photos; the link opens when logged out
- [ ] Searching the PDF for "[team" finds nothing
- [ ] The PDF has 19 pages and opens on another computer
- [ ] Nothing in the deck claims a measurement, a working device, graphene or a clinical benefit

## After 25 Oct: the road to the December video (slide 15)

| By | Deliverable | Gate |
|---|---|---|
| mid-Nov | E2 done; strip sizes confirmed | G1: Rs CV ≤ 20 %, gaps > 3 MΩ |
| mid-Nov | Reader wired; bench test T0–T11 (incl. Bluetooth) | G2: all steps pass |
| early Dec | First strips on a dressing; **3-minute prototype video** + updated PPT | OK → CHANGE on camera, raw log kept |
| Dec – Jan | Strip v0.2, printed clamp, E4 wet tests, repeatability | G3: alert within ±10 % |
| Jan | Virtual semi-final: 5-minute live demo | Rehearsed twice with real hardware |
| 26 Jan – 1 Feb | IIT Indore finale (if selected) | G4: live demo with logged data |

**For the January interview:** you must be able to explain every design choice yourselves. Read the decision log (`3_decisions/decisions.md`), the requirements and `PROJECT_AUDIT.md`, and walk through the CAD and the firmware together once.
