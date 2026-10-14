# 08_submission: Stage 2 deck

| File | What it is |
|---|---|
| `template/Vishwakarma Awards 2026-27 Stage 2 Submission Template.pptx` | Official template, **unchanged** (MD5 4d96244a04c6be5a3a952b42eb965679) |
| `make_figures.py` → `figures/` | All figures, drawn from project files and plain geometry (no stock or AI images); concept drawings are labelled |
| `build_deck.py` | Builds the deck from the template: 11 slides, one per section, in the template's order (decision D-011) |
| `VK26-IITI-HT-0050_Stage2_Dermasense.pptx` | **Output.** Rebuild with `python make_figures.py && python build_deck.py` |

**Slides:**
1. Application ID
2. Problem Context
3. User Journey
4. System Architecture & Specs
5. CAD Design & Mechanical Specs
6. Electronics Schematics & BOM
7. Maker Journey
8. Safety by Design & Roadmap
9. Technical Challenges & Risks
10. References
11. Image Sources

## Still needed from the team before submitting

1. **Title slide:** your institute name(s) exactly as registered.
2. **Maker Journey:** real lab photos from E1 (with ID badges), the repository link, and the mentor's name (only if they actually reviewed the work).
3. **After E1:** replace targets with measured values (sheet resistance, CV, line width).
4. **Fonts:** check the line breaks once in Google Slides; Poppins, Inter and DM Sans are not installed on this PC.
