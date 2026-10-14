# PPT asset index: Vishwakarma Stage 2 final deck

**Deck:** `Vishwakarma_Stage2_Final.pptx`, 18 slides, 16:9 (13.33 × 7.5 in). Review copy: `Vishwakarma_Stage2_Final.pdf`.

**Built on:** the official file `08_submission/template/Vishwakarma Awards 2026-27 Stage 2 Submission Template (2).pptx`.
- The template file is unchanged: MD5 `c58ef4fe…`, same before and after the build.
- **Builder:** `08_submission/build_final_deck.py`
- **Figures:** `figures/src/render_cad.py` and `figures/src/make_final_figures.py`

## How the official template was followed

The template has 20 slides:
- the cover
- **guideline slides** (instructions)
- **example slides** (the intended layout)
- References, and Image Sources

**What the deck keeps:**
- the template's section order and its slide limits
- each section's example-slide design: background, logos, title position, panels, heading icons, metric cards and the rationale bar

**What changes:**
- The example content is replaced with ours.
- The guideline slides are dropped, as the template intends. Each of their requirements is mapped below.

| Template section (limit) | Template slides | Final deck slides |
|---|---|---|
| Application ID (cover) | 1 | 1 |
| Problem Context (1–2) | 2 guideline, 4 example | 2 |
| User Journey (1–2) | 3 guideline, 4 example | 3, 4 |
| System Architecture & Specs (1–2) | 5 guideline, 6 example | 5, 6 |
| CAD Design & Mechanical Specs (1–2) | 7 guideline, 8 example | 7, 8 |
| Electronics Schematics & BOM (1–2) | 9 guideline, 10 example | 9, 10 |
| Maker Journey (1–2) | 11 guideline, 12 example | 11, 12 |
| Safety & Hazard Mitigation (1) | 13 guideline, 15 example | 13 |
| Roadmap (1) | 14 guideline, 15 example | 14 |
| Technical Challenges & Risks (1) | 16 guideline, 18 example | 15 |
| Potential Solutions & Risk Mitigation (1) | 17 guideline, 18 example | 16 |
| References & Sources | 19 | 17 |
| Image Sources | 20 | 18 |

**Evidence status:** each content slide carries one status pill, top right, where the template's example badge sits.
- **Green:** completed and verified, in software or by source.
- **Amber:** designed; physical validation pending.
- **Grey:** future scope.
- **Blue:** research or documented decision.

The cover explains this key.

## Slide by slide

| # | Slide title | Template requirement covered | Brief item | Visual assets (file → made from) | Evidence status |
|---|---|---|---|---|---|
| 1 | Vishwakarma Application ID | Title, team ID, track, 1-line innovation | 1 | Template cover; text only | Identity as registered |
| 2 | Problem Context | Problem statement; target beneficiary; operational pain point | 2 | `fig_problem.png` ← `strip_v0_1_geometry.json` (to-scale dressing and strip) | Blue: cited refs 1–5, 7 |
| 3 | User Journey: Before State | Before-state flowchart; quantified inefficiency | 3 | `fig_journey_before.png` ← refs 1–3 | Blue: refs 1, 2, 3, 6. No unsourced numbers |
| 4 | User Journey: After State (Intended) | After-state flowchart; quantified efficiency | 4 | `fig_journey_after.png` ← firmware states | Amber: targets only, labelled intended / not clinically validated |
| 5 | System Architecture & Specs | Block diagram; target specs; hardware selection | 5 | `fig_block.png`; native spec table ← `config.h`, `calc_readout_report.md`, geometry JSON | Amber, with software ✓ per block |
| 6 | System Architecture & Specs: Firmware & Data Flow | Firmware / logic flow (template slide 5) | 9 | `fig_dataflow.png` ← `reader_v0_1` source | Green in software; hardware pending |
| 7 | CAD Design & Mechanical Specs | 3D renders (iso + exploded); material selection; stress analysis | 6 | `fig_cad.png` ← `render_cad.py` (SolidWorks renders of the verified models) + clamp drawing PDF extract | Amber: CAD verified, not built |
| 8 | CAD Design & Mechanical Specs: Sensing Strip & Laser Process | Mechanical spec of the sensor; fabrication | 7 | `fig_strip.png` ← `strip_v0_1.dxf`, `e2_res_coupon.dxf` | Amber: files verified, not lased |
| 9 | Electronics Schematics & BOM | Schematic, pinout, power distribution | 8 | `fig_schematic.png` ← KiCad 10 PDF export; native pin table ← netlist | Green: ERC 0; not wired |
| 10 | Electronics Schematics & BOM: Bill of Materials | Itemised BOM, costs, sourcing | 8 | `fig_window.png` ← `calc_readout.py`; native BOM table ← `09_procurement/bom_v0_1.csv` | Amber: estimates, not ordered |
| 11 | Maker Journey | Authenticity; work-in-progress software evidence; repository | 12 | `fig_maker.png` ← `sw_ui_assembly.png` (screen capture of our SolidWorks) + verbatim tool output + git log | Green: genuine artefacts; **no lab photos yet** |
| 12 | Maker Journey: Engineering Iterations | Stage 1 → 2 iterations; design thinking | 10 | `fig_decision.png` ← `decision_matrix.md`, `decisions.md`, git history | Blue: documented decisions |
| 13 | Safety & Hazard Mitigation | Fail-safes; FMEA matrix; standards | 11 | `fig_fmea.png` ← `fmea_v0_1.csv`; native FMEA table | Amber: ratings estimated |
| 14 | Roadmap | 4-month plan; Stage 3 target | 14, 15 | `fig_roadmap.png` ← E2, bench-test and E4 plans | Grey: plan with gates |
| 15 | Technical Challenges & Risks | Engineering bottlenecks | 13 | `fig_challenges.png` ← geometry + FMEA F04 | Blue: found by our own verification |
| 16 | Potential Solutions & Risk Mitigation | Backup solutions; fallback logic | 13, 15 | Template cards + native future-scope panel | Grey / green / amber per card |
| 17 | References & Sources | References | 16 | Text (12 sources, each with its reading depth) | Blue |
| 18 | Image Sources | Image credits | 16 | 14 thumbnails with their generating script and data | Green: all images original |

## Template requirements that are not fully met (stated, not hidden)

| Requirement (template guideline slide) | Status in this deck | What closes it |
|---|---|---|
| Lab photos of team members with ID badges (Maker Journey) | **None exist.** Slide 11 says so | Photograph the E2 session |
| Accessible Drive / GitHub repository link (Maker Journey) | **Placeholder on slide 11** | Team creates the repository and replaces the bracketed text |
| Faculty / mentor sign-off (Maker Journey example) | Not shown; no mentor confirmed | Add after a mentor reviews E2 |
| Verified vendor lead times (Electronics & BOM) | Sources listed, lead times not verified | Check supplier pages when ordering |
| Exact part numbers for every component | Module names and specs given; resistor and capacitor part numbers not yet chosen | Choose them when ordering |
| FEA / stress plots (CAD) | Hand calculations instead; loads < 3 N, justified on slide 7 | Not needed unless the contact test shows deformation |
| Quantified time loss and labour cost (User Journey) | Not estimated; only published numbers used | Nurse interviews (planned) |

## Figure sources

| File | Generator | Data |
|---|---|---|
| `cad_assembly_iso.png`, `cad_exploded_iso.png`, `cad_clamp_closeup.png`, `sw_ui_assembly.png` | `figures/src/render_cad.py` (SolidWorks 2019 COM, read-only; colours applied to temporary copies) | `06_cad/solidworks/*` |
| All `fig_*.png` | `figures/src/make_final_figures.py` | the project files named in the slide table above |
