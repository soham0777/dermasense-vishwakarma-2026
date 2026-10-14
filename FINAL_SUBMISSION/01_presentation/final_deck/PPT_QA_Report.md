# PPT QA report: Vishwakarma Stage 2 final deck

**Date:** 15 Oct 2026.

**Files:**
- `Vishwakarma_Stage2_Final.pptx` (4.7 MB)
- `Vishwakarma_Stage2_Final.pdf` (1.7 MB), exported by PowerPoint

**How it was checked:**
1. `08_submission/qa_final_deck.py` opened the deck in **Microsoft PowerPoint** (COM, read-only) and measured every rendered text box, table and figure.
2. It then exported the PDF and re-checked it with PyMuPDF.
3. I reviewed every slide by eye, both as PowerPoint renders and as PDF pages.

Raw results: `08_submission/qa_final_deck_results.json`, kept outside this folder because it is working evidence.

## Final review status

**READY FOR SUBMISSION, after one team action:** replace the bracketed repository placeholder on slide 11 with the real GitHub / Drive link. That link does not exist yet; creating it is the team's decision.

Everything else in the deck is complete. It does not claim any result we do not have.

## Template compliance

| Check | Result |
|---|---|
| Built on the official template file | Yes: `08_submission/template/... Template (2).pptx`. Its MD5 `c58ef4fe526045f1a82a806e6532bc3c` is unchanged after the build (the file is never edited in place) |
| Template designs reused | Background, logos, title position, panels, heading icons, metric cards and the rationale bar come from the template's own example slides. No new visual style was introduced |
| Section order | **Correct.** Cover → Problem Context → User Journey → System Architecture → CAD → Electronics & BOM → Maker Journey → Safety → Roadmap → Technical Challenges → Potential Solutions → References → Image Sources |
| Slide limits | **All within limits.** Problem Context 1 (1–2), User Journey 2 (1–2), System Architecture 2 (1–2), CAD 2 (1–2), Electronics 2 (1–2), Maker Journey 2 (1–2), Safety 1 (1), Roadmap 1 (1), Challenges 1 (1), Solutions 1 (1) |
| Guideline slides | Removed, as the template intends. Each requirement is mapped in `PPT_Asset_Index.md` |
| Slide count / size | 18 slides, 13.33 × 7.5 in (16:9, same as the template) |

## Measured layout checks (PowerPoint layout engine)

| Check | Result |
|---|---|
| Text overflowing its box | **0** (on all 18 slides) |
| Overlapping content (text, tables, figures) | **0** |
| Content off the slide | **0** |
| Smallest font | 7.5 pt (status pills and figure captions); body text 9.2–10.4 pt; titles 20.25 pt (template size) |
| Picture resolution | **0** pictures below 150 dpi at their placed size. CAD renders and the schematic are 200–300 dpi sources |
| Status pill | Exactly one on each content slide (2–18); none on the cover |

**Defects found and fixed during QA:**
- Metric numbers on slides 2–4 ran 0.05 in into their labels. Fixed with resized boxes and the embedded font.
- The cover ID overflowed its box. The box was enlarged.
- Captions wrapped to two lines. They were shortened to one.
- The Problem and Journey slides had lost their heading icons. Restored.
- The Problem and Journey panels had empty space. It was filled with substantive points (why now, root cause, who benefits: labelled expected).
- An unclear phrase on slide 16 was rewritten.

## Fonts

| Font | Use | Embedded in the PPTX |
|---|---|---|
| Poppins SemiBold | titles, metric numbers, cover | **Yes** (from the template) |
| DM Sans / DM Sans Medium | all body text, tables, labels | **Yes** (from the template) |
| Poppins (regular) | only the template's own cover heading "Vishwakarma Application ID", left untouched | No (the template's own setting) |
| Arial / Calibri | theme defaults on empty paragraphs; no visible text | No (standard fonts) |

The PDF embeds its fonts as subsets.

Figures use Segoe UI rasterised inside the images, so they look the same on every machine.

## PDF review copy

| Check | Result |
|---|---|
| Pages | 18, one per slide |
| Page size | 13.33 × 7.5 in |
| Titles found in the PDF text | 18/18 |
| Visual check | All 18 pages reviewed after export. Layout matches the PowerPoint render; no missing images or substituted symbols |

## Content checks

| Check | Result |
|---|---|
| Numbers and claims | 41 claims traced in `PPT_Claim_and_Reference_Check.md`. One earlier error was found and corrected everywhere: "22" compile-time tests is really **19** |
| References | 12 on slide 17, each with its reading depth. Ref 6 was completed from the source page (authors, volume, pages). Ref 2 was made precise: the 2 cm rule applies to *some* foam dressings |
| Evidence discipline | Completed / designed / future status on every slide. "LIG-like laser-carbonised conductive material" everywhere; graphene not claimed; no sensor-performance or clinical claims; targets labelled as targets |
| Images | All 14 original (slide 18). No stock, external or AI-generated images; no fabricated lab photos |
| Personal data | Only the registered team names and application ID; no contact details |

## Missing content and unavailable assets (stated in the deck, not hidden)

| Item | Where | Why missing | Action |
|---|---|---|---|
| Repository link | Slide 11, bottom bar (bracketed placeholder) | No remote repository exists yet | **Team:** create the GitHub / Drive link and paste it in |
| Lab photographs with ID badges | Slide 11 says none yet | No lab session has happened | Photograph the E2 session; add to the Stage 3 materials |
| Faculty sign-off | Slide 11 says it follows the E2 review | No mentor confirmed | Add if a mentor reviews |
| Institution name on the cover | Not shown | Not confirmed for the application ID "IITI" | Team decides; one text line on slide 1 |
| Measured results (E2, bench test, E4) | Slides 6–10, 13–16 say pending | Experiments not yet run | Run E2 (next action) |
| Vendor lead times, exact passive part numbers | Slide 10 | Not ordered yet | Confirm when ordering |

## Regenerating the deck

```bash
python 08_submission/Stage2_Final/figures/src/render_cad.py
```

```bash
python 08_submission/Stage2_Final/figures/src/make_final_figures.py
```

```bash
python 08_submission/build_final_deck.py
```

```bash
python 08_submission/qa_final_deck.py
```

`render_cad.py` needs SolidWorks; it saves and restores your SolidWorks settings and never saves any CAD file. The QA step re-exports the PDF.
