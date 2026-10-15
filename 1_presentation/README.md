# 1_presentation: how the deck is made

The deck itself lives in **`../FINAL_SUBMISSION/`** (`.pptx` + `.pdf`). This folder holds what builds and checks it.

| File | What it is |
|---|---|
| `build_deck.py` | Builds the 18-slide deck on the official template. Edit this, not the PPTX |
| `qa_deck.py` → `qa_results.json` | Opens the deck in PowerPoint and measures overflow, overlap, fonts and sections; exports the PDF |
| `make_figures.py` | Draws the figures from project data |
| `render_cad.py` | Renders the SolidWorks images (needs SolidWorks; never modifies a CAD file) |
| `figures/` | Every image used in the deck |
| `template/` | The official Vishwakarma template, **never edited** (see `TEMPLATE_PROVENANCE.md`) |
| `PPT_QA_Report.md` | QA results and the open items |
| `PPT_Claim_and_Reference_Check.md` | Every claim and reference, traced to its source |
| `PPT_Asset_Index.md` | Template section → slide → figure → evidence status |

**Before uploading:** put the repository link into `build_deck.py` (function `maker`, the bracketed text), then rebuild and re-check:

```bash
python build_deck.py
```

```bash
python qa_deck.py
```
