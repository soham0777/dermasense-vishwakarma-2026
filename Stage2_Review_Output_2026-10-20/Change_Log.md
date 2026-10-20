# Change log: Vishwakarma_Stage2_Refined (20 Oct 2026)

## Inputs (version identifiers)

| Input | Identifier |
|---|---|
| Official template (team's file) | `Vishwakarma Awards 2026-27 Stage 2 Submission Template.pptx`, MD5 `4d96244a04c6be5a3a952b42eb965679` (copy in `build/template_source/`) |
| Previous deck (left untouched) | `FINAL_SUBMISSION/Vishwakarma_Stage2_Final.pptx`, commit `1e7ab17`, 19 slides |
| Reused slide code (imported, not modified) | `1_presentation/build_deck.py`, `qa_deck.py`; figures in `1_presentation/figures/` |
| Organiser email | Downloads `.eml` of 25 Sep 2026 (deadline line only) |
| New sources | `new_sources.csv` (refs 16–20) |

**Rebuild:** run `python build/build_refined.py`, then `python build/qa_refined.py`.

## Why this version exists

**Team feedback (20 Oct):**
1. Slide 1 needs only the ID and the team names.
2. Team photos on a Problem Context slide were the wrong place.
3. Problem Context (up to 2 slides) must make the problem clear: what it is, what we solve, why.
4. User Journey must show **who** is affected, with data, the way design thinking would.

The team also asked for the template to be read page by page before rebuilding.

## Slide by slide (previous 19 Oct deck → this deck)

| New | Was | Change | Reason |
|---|---|---|---|
| 1 | 1 | Only "Vishwakarma Application ID", the ID and "Team: Soham Prabhakar Kadu · Bhakti Ajay Kadam". Tagline, track, institution and evidence key removed | Template page 1 + team instruction |
| 2 | 3 | Problem Context 1/2: same figure; problem / result / who / we will; **Project Overview moved into the bottom bar** (as in template example page 4). Cards: 44.9 %, ≈ 2 cm · 75 %, 1 point, > 10× | Template page 2 + example page 4 |
| 3 | **new** | Problem Context 2/2: **editable comparison table** of 7 options × "without lifting? / maker's rule? / what limits it"; public search disclosure; why now; "not our goal: diagnosis or therapy"; design question | Problem must be clear before the solution |
| 4 | 4 | User Journey before: **WHO cards** (1.9–4.5 per 1,000 chronic wounds in India; 101 million with diabetes; 19–34 % foot-ulcer risk; 40.3 % pain) + **native journey map** (illustrative persona, 5 stages, pain points) + quantified inefficiency (time, waste, cost, safety) + insight | Team instruction; template page 3 |
| 5 | 5 | User Journey after: **native journey map** (5 stages, gains) + how each person is helped + projected efficiency cards (labelled) | Template page 3 |
| 6–11 | 6–11 | Unchanged (how it works, firmware, CAD, strip, circuit, BOM) | Already checked; team did not object |
| 12 | 12 | Maker Journey: **team photo + lab photo placeholders**, names with role fields, evidence gallery, link field | Template pages 11–12 |
| 13–17 | 13–17 | Unchanged | – |
| 18 | 18 | 20 references (5 new) at 8.6 pt | New data on slides 4–5 |
| 19 | 19 | Wording: team photos on "slide 12" | Photos moved |
| – | 2 | **Removed:** "Project Overview & Team" slide with team portraits | Wrong place for photos (team); its project-overview content is now the slide 2 bar, and its photos moved to slide 12 |

## Content moved or omitted (with justification)

- **"What we built in Stage 2" list and thumbnails (old slide 2):** omitted. The same evidence is on slides 8–12 (CAD, circuit, firmware, laser files, gallery), so nothing is lost.
- **Old journey images** (`fig_journey_before.png`, `fig_journey_after.png`): replaced by editable native maps. The images remain in `1_presentation/figures/`.
- **Nothing was deleted, renamed or moved in the project.** `literature.csv` was not edited; the new sources are listed here instead.
