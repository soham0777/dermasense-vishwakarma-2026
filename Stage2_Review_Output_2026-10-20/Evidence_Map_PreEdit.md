# Evidence map: before any edit (20 Oct 2026)

This map is the editing gate: the deck is built only after this file is complete.

**Starting point:**
- Branch `dev/stage2-rebuild`, commit `1e7ab17`, working tree clean.
- Previous deck `FINAL_SUBMISSION/Vishwakarma_Stage2_Final.pptx` (19 slides, 19 Oct). It is **left untouched**, as are its scripts in `1_presentation/`.

## 1. The authoritative template

| Item | Finding |
|---|---|
| File | `Vishwakarma Awards 2026-27 Stage 2 Submission Template.pptx` from the team's Downloads (the file the team names as the template). Copy: `build/template_source/` |
| MD5 | `4d96244a04c6be5a3a952b42eb965679`. The earlier deck used "(2)" (`c58ef4fe…`) |
| Difference | Both have 20 slides with identical text, notes, shape IDs and positions. Only images and fonts are re-encoded: example slides 4, 6, 8, 10, 12, 15, 18 and 20 show tiny rendering differences (line wrapping, table shading). **Content and layout are the same.** The new deck is built on the team's file |
| Slide size | 13.33 × 7.5 in (16:9) |

## 2. First read: every page

| Page | Kind | What it requires |
|---|---|---|
| 1 | Cover | "Vishwakarma Awards 2026-27 · Vishwakarma Application ID" |
| 2 | Guideline | **Problem Context (1–2 slides).** "Slide 1 & 2 Template": **Project Overview** (title, Team ID, track, 1-line core innovation) and **Problem Statement** (operational pain point, exact target beneficiary segment) |
| 3 | Guideline | **User Journey (1–2).** Before: flowchart / storyboard / diagram of current issues + **quantified inefficiency** (time loss, material waste, labour cost, safety hazards). After: diagram of how the solution helps + **quantified efficiency** |
| 4 | Example | Problem Context & User Journey: 4 metric cards (cost, time, loss, safety), photo, target user, operational bottleneck, before-state flow, **public search disclosure**. **The bottom bar carries the Project Overview** ("Team ID … Track … Core Innovation") |
| 5 | Guideline | **System Architecture & Specs (1–2).** Block diagram (mechanical, power, controllers, firmware); target specs; exact MCU, sensors, protocols |
| 6 | Example | Photo + 3-column spec table + "Architecture Rationale" bar |
| 7 | Guideline | **CAD (1–2).** Isometric + exploded renders; material selection; FEA / stress |
| 8 | Example | Exploded render + "Mechanical Validation & FEA Stress Report" + "Design Iteration" bar |
| 9 | Guideline | **Electronics & BOM (1–2).** Pinout, power distribution, regulation; itemised BOM with part numbers, qty, unit cost, total; local vs imported, lead times |
| 10 | Example | Schematic + 5-column BOM + "Procurement Status" bar |
| 11 | Guideline | **Maker Journey (1–2).** **Lab photos of team members (ID badges)**; joint mentor photo if attached; CAD UI feature tree; EDA rule-check log; FEA convergence; Drive/GitHub link with native files; timestamps audited; no embedded videos |
| 12 | Example | **Team photo** + "Stage 1 to Stage 2 Engineering Iterations" + "Institutional Sign-Off" bar |
| 13 | Guideline | **Safety (1).** Fail-safes, FMEA, standards |
| 14 | Guideline | **Roadmap (1).** 4-month fabrication plan; Stage 3 commitment |
| 15 | Example | FMEA table + months 1–2 / 3–4 panels |
| 16 | Guideline | **Technical Challenges (1).** Engineering bottlenecks |
| 17 | Guideline | **Solutions & Mitigation (1).** Backup solutions, fallback logic |
| 18 | Example | 3 cards (2 bottlenecks + standards) + "Empirical Verification" bar |
| 19 | References | "Mention the References and Sources used in your PPT" |
| 20 | Image sources | URL + source for every image |

## 3. Second read: what the template means for our deck (with the team's corrections)

1. **Slide 1 is basic details only:** the Application ID and the team members' names. No tagline, no evidence key, no track.
2. **Problem Context = 2 slides about the problem only.** No team photos there. Slide A defines the problem (what, for whom, why), with the Project Overview in the bottom bar exactly as in example page 4. Slide B shows why it is still unsolved: what exists, the gap, and what we will solve and why.
3. **User Journey = 2 slides, design-thinking style.**
   - **Who** is affected, with data.
   - A journey map before.
   - Quantified inefficiency in the template's four categories (time, material, cost, safety).
   - The after journey, with quantified (projected) efficiency.
4. **Team photos belong to Maker Journey** (pages 11–12): lab photos of team members with ID badges.
5. **Guideline and example pages are replaced** by our content in the same order. Section limits allow at most 1 + 2 + 2 + 2 + 2 + 2 + 2 + 1 + 1 + 1 + 1 + 1 + 1 = **19 slides**. The website gives no total slide count (it asks for a "PPT deck of design specifications").

## 4. Competition rules (primary sources, read 20 Oct)

| Item | Primary evidence | Status |
|---|---|---|
| Deadline | Organiser's email of 25 Sep 2026: "Deadline: 11:59 PM on 25th October 2026." | **Supported by the primary source**. Timezone not stated (IST likely). The secondary Internshala listing says 16 Oct. The form's open/closed state was **not checked** (no form link opened) |
| Format | Email: "Prepare your presentation using the given template … Submit it through the form". Website: "PPT deck". The team uploads a PDF | PDF exported from the PPTX |
| Criteria | Website FAQ: relevance, effectiveness, clarity, uniqueness, patentability (IP belongs to team members), commercial viability, fact check, ease of use | – |
| Rules | "Only work done during the program timeline will be evaluated"; working hardware required later. **No AI rule found** | – |

## 5. Slide-by-slide map: the plan

**Evidence classes:**
- **M** = measured (none exist)
- **V** = verified in a file, CAD or software test
- **C** = calculation
- **L** = published source
- **E** = estimate or quote
- **T** = target or projection
- **P** = planned or missing

| # | Section (limit) | Story purpose (non-specialist) | Evidence and source | Class | Visual | Missing / user input |
|---|---|---|---|---|---|---|
| 1 | Cover (1) | Who is submitting | Shortlist email: VK26-IITI-HT-0050; team names | – | Template cover | – |
| 2 | Problem Context 1/2 | **The problem:** a covered dressing hides the moment it is full | Refs 1, 2, 6, 14 (`2_research/literature.csv` L08, L28, L40; Dealey); geometry JSON for the to-scale figure | L | `fig_problem.png` + 4 cards; Project Overview in the bottom bar (as in example page 4) | – |
| 3 | Problem Context 2/2 | **Why it is unsolved:** what exists, what each misses, our focus | Refs 1, 4, 5, 7, 14; `research_gap.md` ("in our search") | L | **Native, editable comparison table** (approach × needs) + design question | – |
| 4 | User Journey 1/2 (before) | **Who** is affected and what a dressing week feels like | **New refs 16–20** (Indian prevalence, ICMR diabetes, DFU risk, pain survey) + refs 1, 13, 15 | L | **Native journey map** (persona labelled illustrative; 5 stages; pain points) + WHO cards + inefficiency (time, waste, cost, pain) | Indian nurse-time data (interviews not done) |
| 5 | User Journey 2/2 (after, intended) | How each person is helped, if it works | Firmware states; projections (up to 44.9 %, payback); BLE "designed" | T | **Native journey map** (after) + per-person benefit | Measured gains (E4) |
| 6 | Architecture 1/2 | How it senses, in three steps; specs with their basis | `sensor_selection.md`, `calc_readout_report.md`, `config.h`, geometry | V/C/P | `fig_howitworks.png` + spec table | – |
| 7 | Architecture 2/2 | What the reader decides and how it reports (LEDs, USB, Bluetooth) | `7_firmware/*`, tests 23 + 16 | V | `fig_dataflow.png` | Hardware test T0–T11 |
| 8 | CAD 1/2 | The clip-on clamp, designed and checked | `5_cad/*`, verify 99/0/5, hand calcs | V/C | Annotated exploded render + checks table | **FEA not done** (stated) |
| 9 | CAD 2/2 | The strip and how E2 will prove it | DXFs, 35/35 file checks, E2 package | V/P | `fig_strip.png` | E2 results |
| 10 | Electronics 1/2 | The circuit that reads each zone | Netlist, ERC 0, consistency 0 | V | Measurement path + KiCad sheet + pin map | Wiring |
| 11 | Electronics 2/2 | Cost and sourcing | `bom_v0_1.csv`, 3 quotes | E | BOM table + `fig_window.png` | Lead times |
| 12 | Maker Journey 1/2 | **The team at work** (photos) and why the work is real | git history, native files, AI-assistance statement | V | **Team / lab photo placeholders here** + names / roles + gallery | **Photos, roles, link (team)** |
| 13 | Maker Journey 2/2 | Stage 1 → 2: what changed and what we corrected | `decisions.md`, decision matrix, Stage 1 (private, not reproduced) | V/L | `fig_decision.png` | – |
| 14 | Safety (1) | Known risks, each with a check | FMEA, bench test, safety checklist | E/P | FMEA top-5 table | – |
| 15 | Roadmap (1) | What happens by the December video | Website dates, gates | P | `fig_roadmap.png` | – |
| 16 | Challenges (1) | Problems we found ourselves | verify_cad, FMEA F04, LaserCAD audit | V | `fig_challenges.png` | – |
| 17 | Solutions (1) | Every risk has a fix or fallback | Decisions, FMEA | V/P | Cards | – |
| 18 | References (1) | Sources and reading depth | 20 references | L | Text | – |
| 19 | Image sources (1) | All images are ours | Generators | V | Thumbnails | – |

**New sources for slides 4–5** (recorded in `new_sources.csv`; `2_research/literature.csv` is left untouched):
- **16:** Gupta N, Gupta SK, Shukla VK, Singh SP. *An Indian community-based epidemiological study of wounds.* J Wound Care 13(8):323–325 (2004), doi:10.12968/jowc.2004.13.8.26657. 6,917 people; 31 chronic wounds, i.e. **4.5 per 1,000**. Read as an abstract plus the citation in ref 17.
- **17:** Sharma A et al. *Epidemiological profile of chronic wounds in an Indian population.* Cureus 16(9):e68684 (2024), doi:10.7759/cureus.68684. Varanasi, 10,003 people; **1.9 per 1,000**; neglected trauma and diabetic foot ulcers each 36.8 % of chronic wounds. Full text (PMC).
- **18:** Anjana RM et al. *ICMR-INDIAB-17.* Lancet Diabetes Endocrinol 11(7):474–489 (2023). **101 million** Indians with diabetes (11.4 %). Abstract / summaries.
- **19:** Armstrong DG, Boulton AJM, Bus SA. *Diabetic foot ulcers and their recurrence.* N Engl J Med 376:2367–2375 (2017), doi:10.1056/NEJMra1615439. Lifetime foot-ulcer incidence **19–34 %**: a review estimate; **the upper bound is contested**. Summaries.
- **20:** Price PE et al. *Dressing-related pain in patients with chronic wounds: an international patient perspective.* Int Wound J 5(2):159–171 (2008), doi:10.1111/j.1742-481X.2008.00471.x. 2,018 patients, 15 countries: **40.3 %** said pain at dressing change is the worst part of living with a wound; about 80 % want to take part in their dressing changes. Abstract.

## 6. Rules for the build

- Built on the team's template copy.
- Output goes only to this folder. `FINAL_SUBMISSION/`, `1_presentation/` scripts and evidence files are not modified.
- New problem and journey visuals are **native, editable PowerPoint shapes and tables**.
- The persona is labelled "illustrative, built from the cited data; not a real patient or interview".
- No photos are generated. Placeholders are marked for *Change Picture*.
- `_private/` is never copied or quoted.
- No animations, videos, links or uploads.
