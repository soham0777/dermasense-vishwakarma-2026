# Baseline audit, 2026-10-14

- **Branch:** `dev/stage2-rebuild` (from `master` @ 5e7d08d).
- **Method:** inspected the repository, git history, the archive folder, Downloads, the LaserCAD install, installed applications and both template copies; rendered every slide of the current deck.
- **Status words:** CONFIRMED = seen in a file or run here · CLAIMED = stated by the team, no record · PROPOSED = designed or written but not built · NOT DONE.

## 1. Confirmed facts (with evidence)

| Fact | Evidence (path / command) |
|---|---|
| Stage 2 is due 25 Oct 2026, 23:59; ID VK26-IITI-HT-0050; Health Tech track | `Desktop/MBF vishwakarma_ARCHIVE_v1_2026-10-14/01_Competition_Submissions/Gmail - Congratulations…pdf` |
| Official template has 20 pages: 1 ID page, 11 guideline pages, 8 TerraWeed example pages | Rendered: `08_submission/template/…Template.pptx` and `Downloads/…Template (2).pptx` (same content, re-exported: media renumbered, fonts re-embedded) |
| Template rules include: lab photos with institutional ID badges, a raw repository link (.STEP, .SLDPRT, .kicad_sch), file timestamps audited, no embedded videos | Template Maker Journey guideline page (slide 11) |
| Organizer clarifications: prototype not required for Stage 2, but work-in-progress photos are expected; AI images must be labelled; Stage 3 needs a working-prototype video | `Downloads/Group 1_Vishwakarma 26-27 Stage 2 Participants/chat.txt` (lines ~514–686) |
| Laser software: LaserCAD V8.28 (AWC controller family), installed 2026-07-20 | `C:\LaserCAD\` file timestamps |
| Machine config: X 1200 mm, Y 900 mm, MaxSpeed 500/400 mm/s, PWMFreq 20000, MaxPower 98, LaserMode 0 | `C:\LaserCAD\AWCCfg\SysCfg.ini` |
| SolidWorks 2019 (27.4.0) is licensed and scriptable from Python (a sketch → extrude → `.SLDPRT` saved) | Probe run 2026-10-14 (scratch file; not kept) |
| Toolchain: Arduino CLI 1.5.1 + esp32 core 3.3.12 (ESP32-C3 targets); Python 3.14.4 (pytest, ezdxf, shapely, schemdraw, pywin32); git 2.55; PowerPoint 16 | Commands run 2026-10-14 |
| KiCad: not installed at audit start; official KiCad 10.0.6 installation started via winget | `winget install KiCad.KiCad` |
| No host C/C++ compiler (gcc, clang and cl absent) | `command -v` checks |
| Disk free: 98 GB | `df -h` |

## 2. Existing project files

| Area | Files | Status |
|---|---|---|
| Control | `00_control/` requirements, traceability, decisions D-001…D-011, evidence register, test log (empty), review checklist | Documents |
| Research | `02_research/literature.csv` (L01–L36), `research_gap.md`, Rezaei critique | Documents |
| Laser | `04_lig_lab/make_test_pattern.py` → `lig_test_coupon.dxf`; E1 protocol; machine record form; pre-filled `e1_samples.csv`; `analyze_e1.py` | DXF + scripts real; **no fabrication, no data** |
| Electronics | `05_electronics/architecture.md`, `bom_preliminary.csv`, `power_budget.py` | PROPOSED; no schematic file, nothing built |
| CAD | `06_cad/cad_plan.md` | **No CAD files exist** |
| Firmware | `07_firmware/` | **Empty** |
| Deck | `08_submission/…Dermasense.pptx` (v2, 11 slides) | Uses concept drawings; combines Safety+Roadmap and Challenges+Mitigation |
| Archive | `Desktop/MBF vishwakarma_ARCHIVE_v1_2026-10-14/` (v1 deck, proposal, 21 PDFs) | Kept unchanged |

## 3. Research status

- **Established:**
  - LIG forms on Kapton under a 10.6 µm CO₂ laser in air; Rs < 35 Ω/sq at threshold (Lin 2014).
  - LIG made in air is superhydrophilic (Li 2017).
  - Wetness detection with disposable electrode strips plus clip-on detectors is old prior art in absorbent products: US 5,469,145; US 5,838,240; US 9,291,589; US 10,928,344.
- **Unresolved (scientific):**
  - Does *our* machine make conductive, repeatable LIG, and in what window?
  - Is it graphene? Raman is not available yet.
  - How does simulated exudate spread through the specific dressings we'll test?
  - Is the strip readable through the dressing's outer face, and does it disturb uptake?
  - Do sweat or condensation trigger false alerts?

## 4. Proposed but not built

- Zone strip.
- Contact clamp.
- Reader electronics.
- Firmware.
- Phone or BLE interface.
- Every CAD part.
- Test rigs.

## 5. Experiments not conducted

| ID | Experiment |
|---|---|
| E1 | Laser window and repeatability |
| E2 | Line width, isolation and encapsulation |
| E3 | Dressing bench test |
| — | Bending test |
| — | Raman |
| — | Nurse interviews |

## 6. Missing (needed from the team or institution)

| Type | Item |
|---|---|
| Permissions | Laser time; lab in-charge approval; mentor confirmation; access to a Raman/SEM facility |
| Data | Earlier "12" trial parameters/photos; machine nameplate; tube rating; whether there is a mA meter; Kapton grade/thickness |
| Hardware | Silver paint or alternative; pogo pins; ESP32-C3 board; ADS1115; resistors; simulated-exudate salts; dressings; balance; syringe or pipette |
| Expertise | Wound-care professional input (interviews) |
| Photos | Every authentic lab photo (none exist) |

## 7. Conflicts, unsupported claims and risks

- **Unsupported claims:**
  - The 2026-10-14 v2 deck tile "≤ ₹100 per strip" is a *target* with no cost model behind it. It will be computed in `08_bom/cost_model.py`.
  - "4 zones" and the OK/SOON/CHANGE/LEAK states are *proposed*; whether they are measurable is unverified.
- **Novelty conflict:** previous documents implied the strip-plus-reader architecture was new. It is not (diaper prior art). The only defensible angle is the application-specific change-line placement plus a LIG process validated on our machine.
- **Compliance conflict:** v2 merged Safety with Roadmap and Challenges with Mitigation. The template asks for 1 slide each. **To be fixed.**
- **Critical risks:**
  1. No laser access or data before the deadline.
  2. Unstable low-power operation of the tube.
  3. KiCad install blocked.
  4. Dressing experiment not possible without consumables.
