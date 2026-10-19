# Slide-by-slide plan and changelog

**Date:** 19 Oct 2026.

**Rule for this refinement:** *simplify the explanation, not the invention.* Every slide should give:
1. a one-sentence takeaway in plain English;
2. one genuine primary visual;
3. only the annotations needed to read that visual;
4. a visible evidence line (source, test or status).

Speaker notes repeat details for the presenter, but nothing a judge must see is hidden in them.

**Gap types:** MISSING (content) · UNSUPPORTED (claim) · OUTDATED · VISUAL (poor communication) · REPEATED · EVIDENCE (missing engineering evidence) · HUMAN (needs team input) · VALIDATION (incomplete).

## Part A: plan, written before any edit

| New # (old #) | Section | Takeaway for a judge | Gaps found | Plan | Must stay | Checks after editing |
|---|---|---|---|---|---|---|
| 1 (1) | Cover | Dermasense, VK26-IITI-HT-0050, Health Tech / Remote Monitoring | UNSUPPORTED: "a strip **that reads**" | "designed to read"; add Sanjivani University | ID, names, track, evidence key | ID matches the email; names spelled right |
| 2 (new) | Problem Context 1/2: Project Overview & Team | Who we are, the idea in one line, and what Stage 2 produced | MISSING: Project Overview slide (template T2); HUMAN: photos, roles | New slide from the template's own Problem Context design. Left: 2 photo placeholders (pictures the team can swap with *Change Picture*) with names, institution and role fields. Right: "What we built in Stage 2" (counts from `PROJECT_AUDIT.md`). Cards: ID, track, institution, stage. Bar: core innovation | Placeholders clearly marked | Placeholders easy to replace; flagged in remaining actions |
| 3 (2) | Problem Context 2/2 | Carers can't see when a covered dressing is full | – | Keep | 4 cited cards, "in our search" | – |
| 4 (3) | User Journey: Before | Today's checks are guesses that cost time and dressings | – | Keep; label the survey "UK" on its card | Cited numbers | – |
| 5 (4) | User Journey: After | Same routine, a clear signal, no unwrapping (intended) | UNSUPPORTED: "the state **is** broadcast"; payback leaves out the reader | "designed to broadcast … (hardware test pending)"; "strip only; the reader is reused" | Projections labelled | Present tense used only for things that exist |
| 6 (5) | Architecture 1: How it works | A wet pad bridges a 1 mm gap; the reader sees the resistance drop and says CHANGE | VISUAL + EVIDENCE: the block diagram shows only status ticks, never the mechanism; spec table lost its "basis" column in the 16 Oct declutter | New `fig_howitworks.png` (layers → dry vs wet gap → signal path with real part names); spec table gets a short basis column | All spec values; status of each block | Values match `config.h`, `calc_readout_report.md` and the geometry |
| 7 (6) | Architecture 2: Firmware & remote view | The reader decides by rules a judge can check; the result goes to LEDs, USB and Bluetooth | UNSUPPORTED risk: "phone" may suggest an app; MISSING: what "remote" means today | Bullets say "any Bluetooth scanner app (no custom app yet), nearby"; keep the test counts | 23 + 16 tests, not on hardware | Counts match the files |
| 8 (7) | CAD 1: Mechanical | A clip-on clamp holds the strip on 4 spring pins; designed and checked in SolidWorks | VISUAL: 4 small images, part names unreadable; EVIDENCE: numbers and material reasons removed in the declutter; UNSUPPORTED: "99 pass" without the 5 blocked | New annotated exploded render (numbered parts) + assembled view; compact "key checks" table (calc vs tool); FEA gap stated | D-013 iteration, 99 / 0 / 5 | Callouts point at the right parts |
| 9 (8) | CAD 2: Strip & laser | The strip is drawn for our laser; E2 will fix its real sizes | – | Keep; state that 35/35 are file checks | E2 plan and pass rules | – |
| 10 (9) | Electronics 1: Schematic | One circuit measures each zone and checks itself on every scan | VISUAL: the full KiCad sheet is unreadable at slide size; EVIDENCE: pin table removed in the declutter | New figure: the measurement path drawn from the netlist (same reference designators) + the real KiCad sheet; restore the pin/net table | ERC 0, 0 mismatches | Every pin matches `config.h` / `WIRING.md` |
| 11 (10) | Electronics 2: BOM | It is cheap; key parts are quoted and in stock in India | EVIDENCE: SKUs only in the notes | Put SKUs in the table; note that the reader is reused | Quoted vs estimate | Total = builder sum |
| 12 (11) | Maker Journey 1 | Real, dated, re-checkable work; honest about photos and AI help | VISUAL: dark terminal boxes; HUMAN: lab photo, repository link; UNSUPPORTED (slide 19): "produced by the team" | New evidence gallery of 6 real artifacts; lab-photo placeholder; one honest line on AI-assisted scripting; link placeholder | Native files, checks, git, "no staged photos" | Gallery tiles are real files |
| 13 (12) | Maker Journey 2 | Why the project changed and what we corrected | UNSUPPORTED risk: "Kept: Bluetooth telemetry" without status | Add "(compiled; hardware test pending)" | Pivot, corrections, prior art | – |
| 14 (13) | Safety | Known risks, each with a check | EVIDENCE: FMEA cut to 3 rows without effects | Restore the top 5 with effects | Fail-safes, standards "considered, not claimed" | RPNs match `fmea_v0_1.csv` |
| 15 (14) | Roadmap | What happens before the December video and the finale | VISUAL: Gantt labels small | Larger Gantt labels | Real programme dates, gates | – |
| 16 (15) | Challenges | Problems we found ourselves | – | Keep | Evidence for each | – |
| 17 (16) | Solutions | Every risk has a fix or a fallback | – | Product line mentions the BLE broadcast correctly | – | – |
| 18 (17) | References | Every number is sourced | – | Keep 15 | Reading depth | Superscripts match |
| 19 (18) | Image sources | All images are ours | UNSUPPORTED: "produced by the team… no AI-generated images" | Reword; add the new figures | – | Every image listed |

**Slide count:** 18 → 19, the maximum the template's section limits allow. No animations, videos or hidden content.

## Part B: what changed (filled in after the edit)

**Backup before editing:** git tag `backup/pre-refine-9626ef0`. **Builder:** `build_deck.py`. **Figures:** `make_figures.py`. The template is unchanged (MD5 `c58ef4fe…`).

| # | What changed | Evidence kept or restored |
|---|---|---|
| 1 | "designed to read"; Sanjivani University added | ID, names, track, evidence key |
| 2 | **New Project Overview & Team slide** (template T2), built from the template's own Problem Context design. Two photo placeholders (*Change Picture*, or drop files in `team_photos/`); role fields for the team; "What we built in Stage 2" with counts; 3 real thumbnails (SolidWorks, laser file, KiCad); core-innovation bar | Counts re-checked 19 Oct (`PROJECT_AUDIT.md`) |
| 3 | No change | 4 cited cards |
| 4 | Survey card labelled "(UK)" | 44.9 %, 18 min, ₹240–510, exudate range |
| 5 | Remote bullet: "designed to broadcast … (hardware test pending)"; payback: "strip only; the reader is reused" | Projections still labelled |
| 6 | Status-only block diagram **replaced by `fig_howitworks.png`**: dressing layers → dry vs wet gap → reader chain with real part names. Spec table regains a **Basis** column (decision, calc, datasheet, E2) and a self-test row | All spec values (from `config.h`, calc report, geometry) |
| 7 | "Output" bullet names the channels honestly (any scanner app, no custom app); new "Why remote" bullet (to be bench-tested) | 23 + 16 tests; "not yet run on a wired board" |
| 8 | 4 small images **replaced by an annotated exploded render** (9 numbered parts with materials) + assembled view + clamp close-up. Bullets replaced by a **Check / Result / Basis table** restoring pin force, lid bending, alignment, strip strain, CAD checks 99/0/5 and the FEA gap | D-013 iteration bar |
| 9 | Bar: "files only; nothing lased yet" | E2 plan, pass rules, "LIG-like" |
| 10 | Unreadable full KiCad sheet **replaced by the zone-C measurement path drawn from the netlist** (R1, R3, R5, R6, C1, U2, pins) above the real KiCad sheet; the **pin & net table is restored** (10 rows) | ERC 0, 0 mismatches |
| 11 | Shop SKUs visible in the BOM table; "the reader is reused; only the strip is consumed" | Quoted vs estimated; total |
| 12 | Dark terminal boxes **replaced by an evidence gallery** of 6 real artifacts (SolidWorks UI, A3 drawing, KiCad sheet, firmware excerpt checked against the source, laser file, E2 bench sheet) + today's tool output. **Two lab-photo placeholders**. One honest line on AI-assisted scripting. The link placeholder no longer quotes a file count that could drift | "No staged photos" |
| 13 | "Kept" bullet: "(compiled; hardware test pending)"; figure footnote no longer quotes an old commit range | Pivot, corrections, prior art |
| 14 | FMEA table **restored to the top 5 with effects** (F04, F07, F08, F01, F05); fail-safes regain the T8 DC check, sealed leads and the laser safety checklist | Standards "considered, not claimed" |
| 15 | Larger Gantt labels; Stage 3 line no longer assumes a finale place | Programme dates, gates G1–G4 |
| 16–18 | No change | – |
| 19 | Wording corrected: images are "from our own project files … plots drawn by our scripts (written with AI assistance) … no AI image generators"; 3-column layout; new figure listed; unused `fig_block.png` removed | Origin of every image |

**Slide count:** 18 → 19 (template maximum).

**Word count on content slides 2–17:** about 128 per slide (it was 104). The increase is restored evidence (tables and annotations), not paragraphs. The densest slide is Safety (template T15 combines FMEA, fail-safes and standards).
