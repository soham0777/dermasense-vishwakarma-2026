# CAD plan: what gets modelled where

**Status:** iteration 1 (2026-10-14). Model building starts in iteration 2, once Step 3 gives us the measured line width, film thickness and alignment-hole accuracy. Until then no dimension below is final.

## 1. Which tool does what

| Work | Tool | Why |
|---|---|---|
| LIG electrode patterns (2D) | **Python + ezdxf** (`04_lig_lab/`) | Parametric and regenerated from *measured* line width; the same DXF goes to LaserCAD **and** into SolidWorks as a sketch |
| Pod, clamp, fixtures, patch stack-up, drawings | **SolidWorks 2019** (installed) | 3D fit, tolerances, drawings, exploded views, 3D-print files |
| Schematic + PCB | **KiCad** (to install, D-006) | Free PCB tool; STEP export goes into SolidWorks to check fit |
| Wiring/harness diagrams (if needed) | SolidWorks Electrical (installed) | Only for cable or harness documentation |
| Power budget, TLM, IDE cell constant, Nernst correction, tolerance stack-ups | **Python scripts** in this repo | Reproducible; rerun with measured values |
| Sensor performance | **Lab experiments only** | No simulation stands in for a measurement |
| Snap-fit / clip strain (optional) | SolidWorks Simulation, *if licensed* | Hand calculation is enough for v1 |

## 2. SolidWorks models planned

| ID | Part / assembly | Key parameters (to be measured or set) | Purpose |
|---|---|---|---|
| P-01 | Sensor coupon (S1 / S2 / S3), sheet body with the electrode sketch imported from DXF | Film thickness (Step 1), pad size 4 × 4 mm, pad pitch 5.08 mm, alignment holes Ø (measured laser-cut size) | Drawings; fit with the pod |
| P-02 | Patch stack-up (thin bodies): skin-side layer → sensor film → encapsulation tape → adhesive border | Thicknesses from datasheets or micrometer | Shows the layers honestly; total thickness; bending check |
| P-03 | Pod base / contact carrier: pogo-pin holes, 2 alignment pins, magnet pockets, **clamp bar for strain relief** | Pogo-pin press-fit Ø (datasheet), magnet Ø + 0.2 mm, pin Ø = hole Ø − 0.1 mm | Reliable, repeatable contact (T-CON-01) |
| P-04 | Pod top shell: PCB standoffs, battery pocket, USB opening with cover, snap fits | From the KiCad STEP and the real battery size | Housing |
| A-01 | Pod + patch assembly, exploded view, drawing with tolerances | FDM ±0.2 mm; resin ±0.1 mm | Fit, interference check, Stage 2 / 3 drawings |
| F-01 | **Laser alignment plate**: registration pins so film always sits in the same place | Bed reference corner | Repeatable LIG (process control) |
| F-02 | **Bending jig**: 20 mm mandrel (10 mm radius) + clamp | | T-MECH-01 |
| F-03 | **S1 wetting cell**: a well over the IDE that holds a known volume | Well volume 50–200 µL | T-S1-01 |

## 3. How Claude Code will help with SolidWorks (iteration 2)

- **One parameter file:** all key dimensions live in `06_cad/cad_parameters.csv`, so changing a number updates everything.
- **Automation:**
  - Claude writes **SolidWorks macros** (VBA, or Python via `pywin32`, which isn't installed yet) that build or update P-01…P-04 from the parameter file.
  - SolidWorks 2019's API supports this. Each macro is tested on this PC before we say it works.
- **Where automation isn't practical** (fillets, final cosmetics): step-by-step modelling instructions with exact sketch dimensions.
- **Real files only:** native `.SLDPRT`/`.SLDASM` plus STEP/STL exports are committed to the repo. Timestamps then show genuine progress, as the template asks.
