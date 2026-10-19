# Stage 2 checklist: what they expect, what we deliver

**Status:** 19 Oct 2026. **Deadline:** 25 Oct 2026, 23:59, as stated in the organiser's email to us (VK26-IITI-HT-0050).

**Built from:**
- the official template (every guideline slide)
- the organiser's shortlist email
- our Stage 1 proposal
- the official website and the Internshala listing (both read 19 Oct)
- every folder of this project

**Key:** ✅ done · ◐ partly done, or done in software only · ❌ missing · 👤 only the team can do it

---

## 1. The competition, start to end

| Stage | When | What is submitted | Our status |
|---|---|---|---|
| 1. Application | Aug – Sep 2026 | Problem + proposed solution | ✅ Shortlisted 25 Sep (3,600+ applications) |
| **2. Design specification** | **by 25 Oct, 23:59** | **PPT on the official template, via the "Design Stage Form" in the organiser's email** | ◐ Deck ready; **slide 11 still needs the repository link** 👤 |
| 3. Prototype | December (Internshala: 4 Dec) | **3-minute working-prototype video** + updated PPT | Planned (slide 14) |
| Semi-final | January (IIT Indore themes) | Virtual interview: 5-minute presentation + live prototype demo | Planned |
| Finale | IIT Indore, arrive 26 Jan – depart 1 Feb 2027 | 3-day bootcamp, pitch with the working prototype | Planned |

**Rules that shape our work** (official website):
- A **working hardware prototype** is required. Software-only entries are not eligible.
- **Only work done during the programme counts.** Our git history (from 14 Oct) and the file timestamps prove when the work was done.
- **IP belongs to the team members.**
- At least one member must attend the finale in person.

> ⚠️ **Date conflict.** The Internshala listing gives 16 Oct for the design proposal; the organiser's email to us says **25 Oct, 23:59**. The email is the direct instruction, but **confirm it today** in the official WhatsApp group or by replying to that email (quote VK26-IITI-HT-0050). 👤

---

## 2. How the jury scores: 8 criteria (official FAQ, no weights given)

| Criterion | What they look for | Where our deck answers it | Strength |
|---|---|---|---|
| Relevance | A real problem | 44.9 % of changes made too early (Milne 2016); covered pads hide the change line (slides 2–3) | Strong |
| Effectiveness | It works and is cost-effective | Design verified in software only; **nothing measured yet** | **Weak until E2 + bench test** |
| Clarity | A sound scientific chain of reasoning | Requirement → design → test → status; every number traced (claim check: 53 claims) | Strong |
| Uniqueness | Different from what is on the market | WoundSense reads 1 point; diaper strips; visual indicators (ALLEVYN LIFE). Ours reads the maker's change line electrically, with an order check (slides 2, 12) | Good |
| Patentability | Own IP | Novelty stated on slide 12; prior-art search (4 patents, 2 products). **No filing**; see the IP note in section 5 | OK |
| Commercial viability | Cost vs the market | Strip ≤ ₹100 (target) vs a ₹240–510 dressing; it pays for itself if it avoids 1 change in every 2–5 (slide 4, projection) | OK |
| Fact check | Knows what has been done before | 15 references, each with its reading depth; Stage 1 errors corrected openly | Strong |
| Ease of use | Practical | Same routine, clip-on, LEDs + phone (slide 4) | Good, not yet user-tested |

**The one thing that would lift the score most:** any real measurement before 25 Oct (E2 Day 1, section 5).

---

## 3. Template requirements → our slides

| Template asks for | Slide | Status |
|---|---|---|
| Title, Team ID, track, 1-line innovation | 1 | ✅ |
| Problem statement + exact target beneficiary | 2 | ✅ |
| Before-state flowchart + quantified time / material / cost loss | 3 | ✅ flowchart · ◐ cited numbers (UK survey, Indian retail prices); Indian nurse time not measured |
| After-state flowchart + quantified gain | 4 | ✅ flowchart · ◐ targets and projections, labelled as such |
| Block diagram, target specs, exact MCU / sensor / protocols | 5–6 | ✅ ESP32-C3, ADS1115 (I²C), USB, BLE |
| Isometric + exploded CAD, material choice | 7 | ✅ our SolidWorks models |
| FEA / stress analysis | 7 | ◐ Hand calculations (loads < 3 N, lid deflection 11 µm); no FEA plot. SolidWorks Simulation is licensed on this PC, so this can be added (optional, ~2 h) |
| Schematic, pinout, power | 9 | ✅ KiCad, ERC 0 |
| Itemised BOM: part, qty, cost, total, local vs imported, lead time | 10 | ◐ Template-style table; 3 key prices quoted and in stock; full 23 lines in `6_electronics/bom_v0_1.csv`; lead times not stated by the shops |
| Lab photos of the team **with institutional ID badges** | 11 | ❌ 👤 none yet |
| Joint photo with faculty mentor (if one is attached) | 11 | ❌ 👤 only if you have a mentor |
| CAD UI with the feature tree; EDA with rule-check log | 11 | ✅ SolidWorks capture; KiCad ERC log |
| FEA convergence plot and mesh statistics | 11 | ❌ no FEA (see slide 7 row) |
| **Accessible Drive / GitHub link with native files** | 11 | ❌ 👤 **placeholder** |
| Raw native files (.STEP, .SLDPRT, .kicad_sch) with timestamps | repo | ✅ all in the project |
| No embedded videos | all | ✅ |
| Physical fail-safes, FMEA, standards | 13 | ✅ |
| 4-month fabrication plan + Stage 3 commitment | 14 | ✅ moved onto the programme's real dates (19 Oct) |
| Bottlenecks; backup solutions | 15–16 | ✅ |
| References; image sources | 17–18 | ✅ 15 references; all images our own |

---

## 4. Stage 1 promises vs Stage 2 (the jury will compare them)

| Stage 1 proposal said | Stage 2 deck does | Why (decision) |
|---|---|---|
| AC impedance spectroscopy (1–100 kHz) of tissue | Two-zone wet/dry resistance at the dressing's change line | Buildable and testable by us now (D-012) |
| Temperature telemetry | Future scope | One sensor done properly first (D-002) |
| Galvanotaxis electrotherapy (10–100 µA) | Dropped | It is therapy (regulatory risk), already shown at lab scale (Jiang 2022), and DC on LIG makes H₂O₂ (D-003) |
| ESP32-C3 BLE clip-on module | ESP32-C3 clip-on reader **with a BLE state broadcast** | Kept; costs no extra hardware (D-015) |
| LIG "graphene", < 150 Ω/sq | "LIG-like" until Raman; Rs is measured in E2 | We claim only what we measure |
| "Kapton is medical-grade" | **Corrected** on slide 12 | DuPont cautions against medical use (ref 11) |
| "Reduces dressing changes by over 60 %" | Dropped; "up to 44.9 %" from a cited study | The 60 % had no source |
| Thermo-responsive hydrogel | Not in scope | Not ours to prove in 4 months |
| Patch < $1.50 | Strip ≤ ₹100 (target, estimate) | Same intent, in rupees |

**Check:** slide 12 explains the pivot and the correction. ✅

---

## 5. What only you can do before 25 Oct 👤

| # | Do | Time | Pass when |
|---|---|---|---|
| 1 | **Confirm the deadline** (WhatsApp group, or reply to the organiser's email quoting VK26-IITI-HT-0050) | 10 min | You have it in writing: 25 Oct, 23:59 |
| 2 | **Make the repository link.** Upload `Desktop/Dermasense_VK26-IITI-HT-0050_repository.zip` to Google Drive, then set Share to *Anyone with the link: Viewer*. The zip holds only project files; your private PDFs are not in it | 20 min | The link opens in a private/incognito browser window |
| 3 | **Send me the link.** I put it on slide 11, rebuild and re-check | 5 min | QA says `issues 0` and no "[team to insert" text is left |
| 4 | **Take photos with ID badges:** both of you modelling in SolidWorks; the KiCad schematic on screen; at the laser if you get access. Real moments only, no edits | 30 min | 3 or more sharp photos, faces and badges visible. Send them to me for slide 11 |
| 5 | *(Strongest, optional)* **Run E2 Session S0 + Day 1** (`4_sensor_strip/e2_experiment/E2_procedure.md`) | 4–5 h at the laser | The data sheets are filled; send me the CSVs and I'll add the first real results to slides 8 and 15 |
| 6 | **Order the reader parts now** (ESP32-C3 ₹242, ADS1115 ₹125, pogo pins ₹354, resistors). Needed for the December video, not for 25 Oct | 15 min | Order confirmation |
| 7 | **Submit by 24 Oct** (one day early): open the Design Stage Form from the email, enter VK26-IITI-HT-0050, and upload `FINAL_SUBMISSION/Vishwakarma_Stage2_Final.pptx` (rename it `VK26-IITI-HT-0050_Dermasense_Stage2.pptx` if the form allows). Add the PDF if a second file is allowed | 15 min | Screenshot of the confirmation saved in `_private/` |

> **IP note (not legal advice):** a public GitHub repository counts as public disclosure. If you might file a patent on the change-line strip, use a view-only Drive link, not a public repo, and ask your university's IPR cell before posting anything publicly.

### Final check just before uploading

- [ ] Slide 1: ID `VK26-IITI-HT-0050`, both names spelled correctly
- [ ] Slide 11: the real link, which opens when logged out
- [ ] `python 1_presentation/build_deck.py` then `python 1_presentation/qa_deck.py`: **issues 0**, 18 slides
- [ ] The PDF opens with 18 pages; searching it for "[team" finds nothing
- [ ] Nothing in the deck claims a measured result we don't have

---

## 6. After 25 Oct: the road to the December video (slide 14)

| By | Deliverable | Gate (must pass first) |
|---|---|---|
| mid-Nov | E2 done; strip sizes confirmed | G1: Rs CV ≤ 20 %, gaps isolate > 3 MΩ |
| mid-Nov | Reader wired and bench-tested, Bluetooth included (T0–T11) | G2: all bench steps pass |
| early Dec | First strips on a dressing; **3-minute prototype video** + updated PPT | Real OK → CHANGE on camera, with the raw log |
| Dec – Jan | Strip v0.2, printed clamp, E4 wet tests, repeatability | G3: alert within ±10 % of the visible front |
| Jan | Virtual semi-final: 5-minute live demo | Rehearsed twice with the real hardware |
| 26 Jan – 1 Feb | IIT Indore finale | G4: live demo with logged raw data |

---

## 7. What changed in the project on 19 Oct (from this review)

- **Deck:**
  - Roadmap on the real dates.
  - Cited time and cost numbers (slide 3), plus payback and "up to 44.9 %" as projections (slide 4).
  - BOM in template form with 3 quoted prices (slide 10).
  - ALLEVYN LIFE cited as prior art; the Stage 1 Kapton claim corrected (slide 12).
  - 15 references.
  - QA: 0 issues.
- **Firmware:** Bluetooth state broadcast for remote monitoring.
  - Compiles with 0 warnings.
  - 23 compile-time tests and 16 PC tests pass.
  - Bench test T11 added.
  - **Not yet run on hardware.**
- **Records:**
  - Decision log completed: D-012 written down; D-014 (dates) and D-015 (BLE) added; stale entries marked as superseded.
  - Old experiment names (E1/E3) replaced by E2/E4.
  - BOM totals made consistent.
  - 5 new sources added to `2_research/literature.csv`.

**Sources read for this checklist:**
- [vishwakarma-awards.org](https://vishwakarma-awards.org/)
- [Internshala listing](https://internshala.com/competitions/vishwakarma-awards-2026-27/)
- the official template in `1_presentation/template/`
- the organiser's email and our Stage 1 proposal (`_private/`, not in git)
