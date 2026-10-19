# QA report: Vishwakarma_Stage2_Refined (20 Oct 2026)

**Files checked:**

| File | MD5 |
|---|---|
| `Vishwakarma_Stage2_Refined.pptx` | `89e6fbb8…` |
| `Vishwakarma_Stage2_Refined.pdf` | `fd4d8a33…` (exported by Microsoft PowerPoint from that saved PPTX) |

**Verdict:**
- **Passes layout, content and format checks.**
- **Not yet ready to upload.** Slide 12 still needs the team's photos, roles and Drive link, and then a PDF re-export (`User_Action_Checklist.md`).

## 1. Template and rules

| Check | Result |
|---|---|
| Template used | The team's `Vishwakarma Awards 2026-27 Stage 2 Submission Template.pptx`, MD5 `4d96244a…`. The copy in `build/template_source/` is unchanged |
| Template read twice | Yes (`Evidence_Map_PreEdit.md` §2–3) |
| Previous template "(2)" | Same 20 slides, text, notes and shape positions; only re-encoded images and fonts differ |
| Section order | **Correct:** cover → Problem Context ×2 → User Journey ×2 → Architecture ×2 → CAD ×2 → Electronics ×2 → Maker Journey ×2 → Safety → Roadmap → Challenges → Solutions → References → Image Sources |
| Section limits | **All within limits**; 19 slides is the maximum the limits allow. No total slide count is stated by the organisers |
| Slide 1 | Application ID + team names only (team instruction) |
| Problem Context | 2 slides, problem only; Project Overview in the bottom bar as in template example page 4 |
| User Journey | Who is affected (cited Indian data), native before/after journey maps, time / waste / cost / safety figures |
| Team photos | Maker Journey, slide 12 (template pages 11–12); 2 marked placeholders |
| Deadline | Organiser's email: "Deadline: 11:59 PM on 25th October 2026" (timezone not stated). Secondary listing: 16 Oct. Not put in the deck |

## 2. Measured by PowerPoint (`build/qa_refined.py`)

| Check | Result |
|---|---|
| Slides / size | 19 · 13.33 × 7.5 in |
| Text overflowing its box | **0** (first build had 2, both fixed: slide 2 bar, slide 18 references) |
| Overlapping content | **0** |
| Content off the slide | **0** |
| Pictures under 150 dpi | **0** |
| Fonts | Poppins SemiBold, DM Sans, DM Sans Medium embedded from the template |
| PDF | 19 pages, same order as the PPTX, fonts subset-embedded |
| Animations / video / audio | **None** (no slide timing, no media relationships) |
| Links in the PDF | **0** (no public share link) |
| Editable | Yes: native text, tables and journey-map shapes; figures are pictures; no slide is flattened |
| PowerPoint safety | The QA quits PowerPoint only if none of the user's windows are open |

## 3. Checked by eye (every slide rendered at 1600 × 900)

| Slide | Finding | Action |
|---|---|---|
| 2, 4, 5 | Some card labels wrapped onto a second line | Shortened; checked |
| 2 | Project Overview bar ran onto two lines | Shorter text at 8.8 pt; checked |
| 18 | 20 references overflowed | 8.6 pt, tighter spacing; checked |
| 19 | Text still said photos were on "slides 2 and 12" | Now "slide 12"; checked |
| All | No clipped or overlapping text; tables readable; journey maps readable at full-screen PDF size | – |

**Words per content slide:** 92–231, average 144.
- Slides 3–5 are the densest (213, 231, 212). The words sit in a table and in journey-map boxes, not paragraphs, and give the "who / what / how much" data the team asked for.
- The other slides are unchanged from the 19 Oct version (98–182).

## 4. Claims and sources

- **Every number has a nearby superscript or a stated basis.** Slides 6–17 keep the 19 Oct claim matrix (`1_presentation/CLAIM_EVIDENCE_MATRIX.md`, 53 claims).
- **New on slides 2–5:**

| Claim | Slide | Source | Class |
|---|---|---|---|
| 1.9–4.5 per 1,000 have a chronic wound | 4 | refs 16, 17 | published |
| 101 million Indians with diabetes | 4 | ref 18 | published |
| 19–34 % lifetime foot-ulcer risk | 4 | ref 19, labelled EST. (contested upper bound) | published estimate |
| 40.3 % say change pain is the worst part | 3, 4, 5 | ref 20 | published (15 countries) |
| 18 min per visit, about 5 visits a week | 4 | ref 13, labelled UK, patient-reported | published |
| ₹240–510 per foam dressing | 4 | ref 15 | retail listing |
| 0 lifts to check | 5 | design intent | by design |
| up to 44.9 % avoidable | 5 | ref 1, projection | projection |
| ≤ ₹100 strip | 5 | estimate | target |
| Payback 1 in 2–5 | 5 | calculation from the target and ref 15 | projection |
| Comparison-table ticks | 3 | our reading of refs 1, 4, 5, 14; "not exhaustive" stated | – |

- **WoundSense** is marked "◐ spot check", because ref 1's readings were taken at dressing change.
- **Persona:** labelled "illustrative, from the cited data; not a real patient". No quotes or interviews are invented.
- **Status words:** "intended", "projection", "estimate", "to be tested" and "not clinically validated" appear wherever they apply. Bluetooth is "compiled; hardware test pending"; there is no phone app.
- **Never claimed:** a working device, measurements, graphene, clinical benefit, or diagnosis ("not our goal" on slide 3).

## 5. Privacy and disclosure

- **Private files:** no `_private/` content, e-mail addresses or private files in the deck, notes or output folder. The Stage 1 proposal was used only to describe the pivot in general terms (slide 13).
- **Sharing:** no repository or share link was created.
- **IP:** the IP note is in `User_Action_Checklist.md`.

## 6. What was not checked

- The Design Stage Form itself (not opened) and the deadline timezone.
- The physical prototype: none exists.
- Bluetooth on hardware: not run.
- FEA: not run.
