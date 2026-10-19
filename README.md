# Dermasense: start here

**Vishwakarma Awards 2026-27 · Stage 2 · Application ID VK26-IITI-HT-0050 · Health Tech**

A laser-written two-zone moisture strip that tells a carer when a wound dressing has reached its maker's "change line", read by a small clip-on reader without lifting the dressing.

## What we submit

**[`FINAL_SUBMISSION/`](FINAL_SUBMISSION/)** holds the deck (`.pptx`) and its PDF. Nothing else is uploaded.

**[`STAGE2_CHECKLIST.md`](STAGE2_CHECKLIST.md)**: what the organisers expect, how the jury scores, what we deliver, and the steps only the team can do before 25 Oct.

## Folder map

| Folder | What is inside |
|---|---|
| `1_presentation/` | How the deck is made: builder, QA, official template, figures and their scripts, claim and QA reports |
| `2_research/` | Literature (41 sources), research matrix, research gap, nurse interview guide, a paper critique |
| `3_decisions/` | Requirements, decision log, sensor selection and its scoring, FMEA, evidence register |
| `4_sensor_strip/` | The strip design and laser files; the E2 fabrication experiment (`e2_experiment/`) |
| `5_cad/` | SolidWorks models, drawings, STEP files, and the scripts that build and verify them |
| `6_electronics/` | Readout calculations, KiCad schematic, bill of materials |
| `7_firmware/` | Reader firmware (ESP32-C3), PC logger, wiring table, bench test |
| `LAB_NOTEBOOK.md` | A few lines after every work session |
| `_private/` | Application confirmation and the Stage 1 proposal. **Not in git**; never uploaded |

## Where the project stands (19 Oct 2026)

| Part | State |
|---|---|
| Deck | Final, 18 slides on the official template; roadmap on the programme's dates. **Needs the repository link on slide 11** |
| CAD | Frozen v0.1; independent check: 99 pass, 0 fail (5 wait for E2 data) |
| Laser files | 35/35 file checks pass; **not yet lased** |
| Reader | Schematic checks clean (0 errors); firmware (with a Bluetooth state broadcast) compiles and passes 23 + 16 software tests; **not yet built** |
| Experiments | E2 is ready to run; **no measurements yet** |

The layer is called **laser-carbonised (LIG-like)**; graphene is not confirmed.

**Next actions:** confirm the deadline, make the repository link and take the ID-badge photos (`STAGE2_CHECKLIST.md`, section 5); then book the laser and run E2 (`4_sensor_strip/e2_experiment/E2_procedure.md`).
