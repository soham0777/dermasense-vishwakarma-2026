# Dermasense: start here

We are building a low-cost smart wound patch. The sensor is laser-written graphene (LIG) on Kapton film, and a small reusable electronics pod reads it.

**Working goal, to be confirmed with nurses in Step 2:** let a nurse know how a chronic wound is doing without opening the dressing.

We started again from zero on 14 Oct 2026. The old version is in `Desktop/MBF vishwakarma_ARCHIVE_v1_2026-10-14/`. It is kept only as a record, so nothing from it gets reused without being re-checked.

---

## Where we are now

**Submission state:** see [FINAL_SUBMISSION/SUBMISSION_READINESS_REPORT.md](FINAL_SUBMISSION/SUBMISSION_READINESS_REPORT.md) (rebuilt by `python 00_control/assemble_submission.py`).

| Part | State |
|---|---|
| CAD v0.1 (SolidWorks) | Frozen. `06_cad/verify_cad.py`: 99 PASS / 0 FAIL / 5 BLOCKED (waiting for E2 data) |
| Laser files | 35/35 file checks pass (`04_lig_lab/verify_laser_files.py`) |
| **E2 fabrication validation** | **Ready to run, not performed.** [04_lig_lab/e2/E2_procedure.md](04_lig_lab/e2/E2_procedure.md). It replaces E1 as Part A |
| Reader schematic (KiCad) | ERC 0 violations: [05_electronics/kicad](05_electronics/kicad/README.md) |
| Reader firmware | Compiles, 22 compile-time tests; **not yet run on hardware** ([07_firmware/BENCH_TEST.md](07_firmware/BENCH_TEST.md)) |
| BOM / FMEA | [09_procurement](09_procurement/README.md) (estimated prices) · [00_control/fmea_v0_1.md](00_control/fmea_v0_1.md) |

No measurement exists yet. The layer is a laser-carbonised conductive layer (LIG-like); graphene is not confirmed.

**Evidence register:** `00_control/evidence_register.csv`, with categories A (our records), B (planned measurements), C (literature) and X (excluded claims).

## Folder map

| Folder | What goes in it |
|---|---|
| `00_control/` | Requirements, traceability matrix, test log, decision log, review checklist |
| `01_people/` | Interviews, observations, real quotes from nurses, doctors and patients |
| `02_research/` | `literature.csv` (every paper, with how it was verified) and paper notes |
| `03_sensors/` | Sensor concepts, the comparison, the chosen portfolio (S1, S2, S3) |
| `04_lig_lab/` | Laser test files, the laser log, photos, measurements |
| `05_electronics/` | Architecture, readout calculations, KiCad schematic of the reader (`kicad/`) |
| `06_cad/` | SolidWorks plan, parameters, models and drawings |
| `07_firmware/` | ESP32-C3 reader firmware, PC logger, wiring table, bench test |
| `08_submission/` | Stage 2/3 decks, the official template(s) and their source material |
| `09_procurement/` | Bill of materials v0.1 |
| `FINAL_SUBMISSION/` | Verified copies for submission. Generated; never edit there |
| `LAB_NOTEBOOK.md` | Five lines after every work session |

## How we keep track (version control)

- This folder is a **git repository**, so every change has a date and a reason.
- After a work session, commit with a message saying what you did (e.g. `Run R2: 300 mm/s power sweep, best 42 ohm/sq`).
- **Don't commit** temporary files: SolidWorks `~$` files, `__pycache__`. These are ignored automatically.
- **IDs link everything:**
  - requirements `PR-x` / `ES-x`
  - tests `T-…`
  - decisions `D-…`
  - papers `L..`
- **Backup:** the folder sits in OneDrive. Git and OneDrive can occasionally clash on `.git` files, so also push to a **private** GitHub repo. Create it yourself, then Claude can connect it.

## Our rules

1. **Real data only.** Every number we show is either something we measured (and we say how) or labelled as a *target*.
2. **Keep original photos.** Don't crop or filter the originals; the phone's timestamps are our proof of work. Make edited copies only when needed.
3. **Label anything AI-made**, every time, as the organizers require.
4. **If a test fails, write it down.** A failed test with a reason is worth more than a pretty slide.

## Our setup (fill this in during Step 1)

- **Laser:** 100 W industrial CO₂ (team statement). LaserCAD V8.28 config on the laptop shows a 1200 × 900 mm bed, 500/400 mm/s max axis speed, 20 kHz PWM and MaxPower 98 % `[A3]`. Still unknown: make/model, controller, tube brand, and whether there is a mA meter. Fill in `04_lig_lab/machine_record.md`.
- **Lens / focus distance:**
- **Film:** the Stage 1 proposal says 100 µm Kapton HN `[A5, unverified]`. Measure the thickness and photograph the label.
- **Instruments we can use:** multimeter / LCR meter / potentiostat / oscilloscope / hotplate / micrometer / Raman / SEM:
- **Mentor (confirmed?):**
- **Who does what:** Soham: · Bhakti:
- **Software on this PC (checked 14 Oct):**
  - SolidWorks 2019 (incl. Electrical, CAM, Composer)
  - Arduino IDE with the ESP32 core 3.3.12
  - VS Code, git 2.55
  - Python 3.14 with ezdxf, numpy, scipy, pandas, matplotlib, pyserial, python-docx, python-pptx
  - **Missing:** KiCad (install it); `pywin32` (needed for SolidWorks automation from Python)
- **Budget before the grant:**

## Things we already know (checked, with sources)

- **LIG is a proven process.** A CO₂ laser (10.6 µm) on Kapton makes conductive porous graphene in air. The first paper (Lin et al. 2014, *Nat Commun* 5:5714) got below 35 Ω/sq at the threshold power and below 15 Ω/sq at its best setting.
- **The old idea already exists in a top lab.** Stanford built a wireless bandage that senses impedance and temperature and gives electrical stimulation, with a gel that releases at 40 °C (Jiang et al. 2022, *Nat Biotechnol*, doi:10.1038/s41587-022-01528-3). Our difference has to come from somewhere else, such as cost, the LIG process, or what nurses actually need.
- **LIG wound sensors with an ESP32 and a phone app exist too.** WoundMx (Asgharian et al. 2025) is lab-only, with no therapy.
- **LIG is a weak thermometer.** Its resistance changes only about 0.05 % per °C, and moisture and bending affect it as well, so use a proper temperature IC for real readings.
- **The ESP32-C3 has no DAC,** and its ADC can't do impedance up to 100 kHz. Use an impedance chip such as the AD5940 or AD5933.
- **Pluronic F-127 gels when warm and turns liquid when cold,** the opposite of what the old deck said.
- **Kapton is not "medical grade".** DuPont publishes a medical-use caution for it, so say "polyimide film" instead.

The full audit of the old version is in the archive at `00_Project_Control/CURRENT_STATE_ASSESSMENT.md`.
