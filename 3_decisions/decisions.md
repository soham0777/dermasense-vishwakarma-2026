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
- **Why:** highest weighted scores, coherent use case, simplest builds. Details: the iteration-1 concept comparison (removed 16 Oct; in git tag `backup/pre-reorganize-a5e776f`).
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
- **Comparison:** the iteration-1 electronics architecture (removed 16 Oct; in git tag `backup/pre-reorganize-a5e776f`).

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

- **Why:** it is simulation only, and its reported shifts are physically implausible by about 10⁶ (see `2_research/rezaei2024_critique.md`).

### D-008: Differentiator — edge-alert strip (REVISED 2026-10-14 → hypothesis H-APP1)

- **Originally proposed:** in the iteration-1 differentiator note (removed 16 Oct; in git tag `backup/pre-reorganize-a5e776f`).
- **Now:** kept only as an **application hypothesis**.
- **Why:** the material process is unproven on our machine. No sensor claim until E1 passes (D-009).

### D-009: Process first; re-scope the Stage 2 entry (DECIDED by team brief, 2026-10-14)

- **Chosen:** Stage 2 presents a **reproducible LIG process on our 100 W laser** as the current work (Experiment E1).
  - The wound-dressing moisture strip is the target application, labelled as planned.
  - The Stage 1 closed-loop electrotherapy bandage is re-scoped.
- **Evidence:**
  - the earlier "setting 12" result is only a recollection `[A1]`
  - low-PWM tube instability is plausible `[C4]`
  - no reproducibility statistics were found in the literature `[C2, C3]`
- **Change if:** E1 shows CV ≤ 20 % quickly. Then move to E2/E3 (strip) sooner.

### D-010: Fill the official template in place (DECIDED, 2026-10-14)

- **What:**
  - `1_presentation/build_deck.py` fills the unchanged official template (`1_presentation/template/`, MD5 4d96244a…).
  - It keeps the order, layouts, cards and tables.
  - It removes only the TerraWeed example content and badges, the "Example:" prefixes and the "(1-2 Slides)" hints.
  - All figures are generated from project files.
- **Why:** the brief requires the original template; every number in the deck traces to the evidence register.

### D-011: Deck v2, one strong slide per template section (DECIDED by team, 2026-10-15)

- **Team feedback on v1:**
  - it looked empty and unfinished
  - it had too many [A]/[B]/[C] tags and "planned" labels
  - the story wasn't convincing
  - the visuals were weak
- **Chosen:**
  - **Instruction slides removed.** The template's own content-slide designs are kept, in the template's section order (11 slides). The Problem-Context design is duplicated so User Journey gets its own slide.
  - **One story:** the dressing maker's "change line" → a strip that reads it from outside the wound → reproducible laser graphene as the foundation.
  - **Honesty kept, but quieter:**
    - numbered citations instead of tags
    - concept drawings labelled as concepts
    - targets called targets
    - the bottom strip of each slide says what is done vs next
  - **Visuals:** figures enlarged to fill the left column. The empty photo box was replaced by a panel of real files (E1 data sheet + LaserCAD config).
- **Change if:** the organizers require the instruction slides to stay. The v1 builder is in git history (fd3a8fd).

### D-013: Seal tape starts outside the contact clamp; CAD v0.1 frozen pending E2 (DECIDED, 2026-10-14)

- **Found by:** `5_cad/verify_cad.py` interference detection. The 0.09 mm seal started at x = 12 mm, while the clamp base reaches x = 22 mm. That trapped 9.0 mm³ of tape between the strip and the clamp, which would lift the strip off the pogo pins.
- **Chosen:**
  - The seal now starts at x = 23 mm (`make_strip.py` SEAL_X0). The traces from 11 to 23 mm sit inside the dry clamp, 17 mm before the dressing edge, so they need no moisture seal. DRC PASS.
  - The verification now reports 99 PASS, 0 FAIL, 5 BLOCKED. The 5 blocked checks are the comparisons with E2 measurements.
- **Also fixed in the same freeze:**
  - first-angle A3 drawings with every dimension shown once
  - 3-decimal film thicknesses
  - Material field filled in
  - assembly drawing: BOM + balloons
  - assembly and STEP files in millimetres (the assembly had been exported in cm)
- **Change if:** E2 shows line growth or isolation that breaks the 0.95 mm clearance, or a laser-cut hole outside 2.00–2.10 mm. Then update `make_strip.py`, rebuild the CAD and re-run `verify_cad.py`.
