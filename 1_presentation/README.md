# 1_presentation: how the deck is made

The deck itself lives in **`../FINAL_SUBMISSION/`** (`.pptx` + `.pdf`). This folder holds what builds and checks it.

| File | What it is |
|---|---|
| `build_deck.py` | Builds the 19-slide deck on the official template. Edit this, not the PPTX |
| `qa_deck.py` → `qa_results.json` | Opens the deck in PowerPoint and measures overflow, overlap, fonts and sections; exports the PDF |
| `make_figures.py` | Draws the figures from project data (how it works, annotated CAD, measurement path, evidence gallery, …) |
| `render_cad.py` | Renders the SolidWorks images (needs SolidWorks; never modifies a CAD file) |
| `figures/` | Every image used in the deck, plus the two photo placeholders |
| `team_photos/` | *(create it when you have photos)* Real team photos: `member1`, `member2`, `lab1`, `lab2` (.jpg/.png) |
| `template/` | The official Vishwakarma template, **never edited** (see `TEMPLATE_PROVENANCE.md`) |
| `TEMPLATE_EVIDENCE_MAP.md` | The template read twice: what each section asks → our slide → files → what is missing |
| `CLAIM_EVIDENCE_MATRIX.md` | Every claim on the slides → source → status label |
| `SLIDE_BY_SLIDE_CHANGELOG.md` | The plan for each slide and what changed |
| `FINAL_QA_REPORT.md` | QA results and open items |

## Adding your photos and link

**Option A, in PowerPoint (simplest):**
1. Open the PPTX.
2. Right-click each placeholder (slides 2 and 12) → **Change Picture**.
3. Type the roles on slide 2 and the Drive link on slide 12.
4. Save, then **File → Export → Create PDF**.

**Option B, rebuild:**
1. Put the photos in `team_photos/` as `member1.jpg`, `member2.jpg`, `lab1.jpg` and `lab2.jpg`.
2. Put the link in `build_deck.py` (function `maker`, the bracketed text) and the roles in `overview`.
3. Run:

```bash
python build_deck.py
```

```bash
python qa_deck.py
```

The builder crops photos to fit and never alters them.

**Important:** running `build_deck.py` rebuilds the PPTX from the template, so it **overwrites Option A edits**. Do Option A only as the very last step, or use Option B.
