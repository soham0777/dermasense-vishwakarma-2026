# 08_submission: Stage 2 deck

**Final deck:** [`Stage2_Final/`](Stage2_Final/), built 15 Oct 2026 on the official template.

| File | What it is |
|---|---|
| `Stage2_Final/Vishwakarma_Stage2_Final.pptx` / `.pdf` | **The submission deck** (18 slides) and its PDF review copy |
| `Stage2_Final/PPT_Asset_Index.md` | Template section → slide → figures → evidence status |
| `Stage2_Final/PPT_Claim_and_Reference_Check.md` | 41 claims and 12 references, each traced to its source |
| `Stage2_Final/PPT_QA_Report.md` | PowerPoint-measured QA, template compliance, open items |
| `Stage2_Final/figures/` + `figures/src/` | Every deck image and the scripts that make it (`render_cad.py` needs SolidWorks) |
| `build_final_deck.py` | Builds the final deck from the template. Edit this, not the PPTX |
| `qa_final_deck.py` | QA in PowerPoint (overflow, overlap, fonts, sections) + PDF export |
| `template/` | Official templates, **never edited** (see `TEMPLATE_PROVENANCE.md`) |
| `VK26-IITI-HT-0050_Stage2_Dermasense.pptx`, `build_deck.py`, `make_figures.py`, `figures/` | **Superseded** v2 draft (14 Oct), kept as history |

**Before uploading:** replace the bracketed repository placeholder on slide 11 with the real link (in `build_final_deck.py`, function `maker`), then rebuild and re-run QA:

```bash
python build_final_deck.py
```

```bash
python qa_final_deck.py
```
