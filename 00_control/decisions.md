# Decision log

One entry per decision: what we chose, what else we considered, why, and what evidence would change our mind.

**Status values:** PROPOSED (waiting for team approval) · DECIDED · REVISED.

---

### D-001: Restart from scratch; archive v1 (DECIDED, 2026-10-14)

- **Chosen:** all v1 files moved to `Desktop/MBF vishwakarma_ARCHIVE_v1_2026-10-14/`.
- **Why:** v1 contained unbacked results and unlabelled AI images (audit is in the archive).
- **Change if:** n/a.

### D-002: Sensor portfolio S1 moisture + S2 temperature now, S3 pH later (PROPOSED, 2026-10-14)

- **Alternatives:** uric acid, sweat ions or glucose, respiration, strain, gas, ECG, and the foot insole (C9).
- **Why:** highest weighted scores, coherent use case, simplest builds. Details in `03_sensors/concept_comparison.md`.
- **Change if:** the interviews point to prevention (switch to C9), or S1 can't separate wetness bands (ES-2 fails).

### D-003: No electrical stimulation in v1 (PROPOSED, 2026-10-14)

- **Why:**
  - It is therapy, so it carries electrode-safety and regulatory burden.
  - Strong prior art exists `[LIT L03]`.
  - DC on LIG electrodes generates H₂O₂ `[LIT L06]`.
- **Plan:** it stays on the roadmap as module 2.
- **Change if:** S1 and S2 are validated early and a mentor with an electrophysiology lab joins.

### D-004: MCU is ESP32-C3 for the bench phases; nRF52840 is the fallback (PROPOSED, 2026-10-14)

- **Why:**
  - The team already uses ESP32, and the Arduino ESP32 core 3.3.12 is installed.
  - The precision analog work is done by a separate front end, so the MCU's ADC quality doesn't matter.
  - Boards are cheap and easy to buy.
- **Change if:** the measured average current (T-EL-03) misses ES-10 on our own board. Then move to nRF52840; the firmware is structured to make that easy.
- **Comparison:** `05_electronics/architecture.md`.

### D-005: Analog front end (PROPOSED, 2026-10-14)

- **Phase A (bench):**
  - the lab LCR meter for S1
  - TMP117 plus an ADS1115 bridge for S2
  - a CMOS buffer plus ADS1115 for S3
- **Phase B (own PCB):** one AD5941 for S1, S3 and the LIG thermistor, plus TMP117.
- **Why:**
  - Phase A uses the lab instrument as the trusted reference while sensors are being characterised.
  - The AD5940 only comes as WLCSP (not hand-solderable); the AD5941 (LFCSP-48) can be assembled.
- **Change if:** we can't source AD5941 in time. Then use AD5933 for impedance plus a separate pH buffer.

### D-006: KiCad for schematics and PCB; SolidWorks for mechanics (PROPOSED, 2026-10-14)

- **Why:**
  - SolidWorks Electrical (installed) is for wiring and harness diagrams, not PCB layout.
  - KiCad is free, and its STEP export lets the PCB be checked for fit in SolidWorks.
- **Action:** install KiCad.

### D-007: The uploaded Rezaei 2024 paper is not used as design evidence (DECIDED, 2026-10-14)

- **Why:** it is simulation only, and its reported shifts are physically implausible by about 10⁶ (see `02_research/paper_notes/rezaei2024_critique.md`).
