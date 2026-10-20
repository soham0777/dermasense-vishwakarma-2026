# Decision log

One entry per decision: what we chose, what else we considered, why, and what evidence would change our mind.

**Status values:** PROPOSED (waiting for team approval) · DECIDED · REVISED.

---

### D-001: Restart from scratch; archive v1 (DECIDED, 2026-10-14)

- **Chosen:** all v1 files moved to `Desktop/MBF vishwakarma_ARCHIVE_v1_2026-10-14/`.
- **Why:** v1 contained unbacked results and unlabelled AI images (audit is in the archive).
- **Change if:** n/a.

### D-002: Sensor portfolio S1 moisture + S2 temperature now, S3 pH later (REVISED by D-012, 2026-10-14)

> **Superseded.** Stage 2 builds one sensor only: the two-zone moisture strip (D-012). Temperature and pH stay future scope.

- **Alternatives:** uric acid, sweat ions or glucose, respiration, strain, gas, ECG, and the foot insole (C9).
- **Why:** highest weighted scores, coherent use case, simplest builds. Details: the iteration-1 concept comparison (removed 16 Oct; in git tag `backup/pre-reorganize-6a467f3`).
- **Change if:** the interviews point to prevention (switch to C9), or S1 can't separate wetness bands (ES-2 fails).

### D-003: No electrical stimulation in v1 (DECIDED, 2026-10-14)

- **Why:**
  - It is therapy, so it carries electrode-safety and regulatory burden.
  - Strong prior art exists `[LIT L03]`.
  - DC on LIG electrodes generates H₂O₂ `[LIT L06]`.
- **Plan:** it stays on the roadmap as module 2.
- **Change if:** S1 and S2 are validated early and a mentor with an electrophysiology lab joins.

### D-004: MCU is ESP32-C3 for the bench phases; nRF52840 is the fallback (DECIDED, 2026-10-14)

- **Why:**
  - The team already uses ESP32, and the Arduino ESP32 core 3.3.12 is installed.
  - The precision analog work is done by a separate front end, so the MCU's ADC quality doesn't matter.
  - Boards are cheap and easy to buy.
- **Change if:** the measured average current (T-EL-03) misses ES-10 on our own board. Then move to nRF52840; the firmware is structured to make that easy.
- **Comparison:** the iteration-1 electronics architecture (removed 16 Oct; in git tag `backup/pre-reorganize-6a467f3`).

### D-005: Analog front end (REVISED, 2026-10-14)

> **Superseded for v0.1.** A two-zone strip only needs wet/dry resistance, so the reader is a bipolar divider into an ADS1115 (100 kΩ reference, check resistor, ratiometric 3V3; `6_electronics/kicad/`). No LCR meter, TMP117 or AD5941. The text below is kept as the original reasoning.

- **Phase A (bench):**
  - the lab LCR meter for S1
  - TMP117 plus an ADS1115 bridge for S2
  - a CMOS buffer plus ADS1115 for S3
- **Phase B (own PCB):** one AD5941 for S1, S3 and the LIG thermistor, plus TMP117.
- **Why:**
  - Phase A uses the lab instrument as the trusted reference while sensors are being characterised.
  - The AD5940 only comes as WLCSP (not hand-solderable); the AD5941 (LFCSP-48) can be assembled.
- **Change if:** we can't source AD5941 in time. Then use AD5933 for impedance plus a separate pH buffer.

### D-006: KiCad for schematics and PCB; SolidWorks for mechanics (DECIDED, 2026-10-14)

- **Why:**
  - SolidWorks Electrical (installed) is for wiring and harness diagrams, not PCB layout.
  - KiCad is free, and its STEP export lets the PCB be checked for fit in SolidWorks.
- **Done:** KiCad 10 installed and used for the reader schematic (`6_electronics/kicad/`).

### D-007: The uploaded Rezaei 2024 paper is not used as design evidence (DECIDED, 2026-10-14)

- **Why:** it is simulation only, and its reported shifts are physically implausible by about 10⁶ (see `2_research/rezaei2024_critique.md`).

### D-008: Differentiator — edge-alert strip (REVISED 2026-10-14 → hypothesis H-APP1)

- **Originally proposed:** in the iteration-1 differentiator note (removed 16 Oct; in git tag `backup/pre-reorganize-6a467f3`).
- **Now:** kept only as an **application hypothesis**.
- **Why:** the material process is unproven on our machine. No sensor claim until E1 passes (D-009).
- **Later the same day:** the hypothesis became the designed two-zone strip (D-012). It is still unvalidated: no sensing claim until E2 and E4.

### D-009: Process first; re-scope the Stage 2 entry (DECIDED by team brief, 2026-10-14)

- **Chosen:** Stage 2 presents a **reproducible LIG process on our 100 W laser** as the current work (Experiment E1).
  - The wound-dressing moisture strip is the target application, labelled as planned.
  - The Stage 1 closed-loop electrotherapy bandage is re-scoped.
- **Evidence:**
  - the earlier "setting 12" result is only a recollection `[A1]`
  - low-PWM tube instability is plausible `[C4]`
  - no reproducibility statistics were found in the literature `[C2, C3]`
- **Change if:** E1 shows CV ≤ 20 % quickly. Then move to E2/E3 (strip) sooner.
- **Revised later on 14 Oct:** E1 became Part A of **E2** (fabrication validation), and the strip itself was designed in parallel (D-012). Experiment names now in use: **E2** = laser fabrication, **reader bench test** = `7_firmware/BENCH_TEST.md`, **E4** = strips on real dressings with simulated exudate. (E3 was an early name for the dressing test; it is now E4.)

### D-010: Fill the official template in place (DECIDED, 2026-10-14)

- **What:**
  - `1_presentation/build_deck.py` fills the unchanged official template (`1_presentation/template/`; since 15 Oct the official **Template (2)**, MD5 c58ef4fe…).
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
- **Change if:** the organizers require the instruction slides to stay. The v1 builder is in git history (01f2d65).

### D-012: Primary sensor is the two-zone strip S2 (DECIDED, 2026-10-14)

- **Chosen:** zone **C** at the pad centre and zone **A** on the dressing maker's change line, read by a clip-on reader. States OK / CHANGE / CHECK / FAULT. Full reasoning: `sensor_selection.md`.
- **Alternatives (scored in `decision_matrix.md`):** S1 one zone at the change line (4.29), S3 four zones (3.96), S5 capacitive (3.46), S4 continuous locator (3.39). S2 scored 4.36.
- **Why:**
  - Only S2 and S3 have the **order check**: a real front wets C before A, so A-before-C is flagged as CHECK (leak, spill, misplaced strip).
  - S2 needs half the lanes and windows of S3, which matters while the laser's smallest reliable line is unknown.
  - It replaces the edge-alert idea of D-008 and the portfolio of D-002 with one buildable sensor.
- **Change if:** E2 shows sealing registration fails (fall back to S1), or E4 shows an early-warning zone changes a carer's decision (upgrade to S3).

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

### D-014: Roadmap follows the competition's own dates (DECIDED, 2026-10-19)

- **Found:** the deck's roadmap ran Nov → Feb, but the programme asks for a **3-minute working-prototype video + updated PPT in December** (Internshala listing: 4 Dec 2026). Health Tech semi-final interviews (virtual, 5-minute demo) are in **January**. The IIT Indore bootcamp and finale are **26 Jan – 1 Feb 2027** (vishwakarma-awards.org, read 19 Oct).
- **Chosen:** the plan is compressed to end of Oct → end of Jan. E2 runs first; then reader build and bench test; first wet demo on a dressing in time for the December video; repeatability and v0.2 strip before the January interview; finale demo at IIT Indore.
- **Change if:** the organisers announce different dates (check the WhatsApp group and email).

### D-015: Broadcast the reader state over Bluetooth LE (DECIDED, 2026-10-19)

- **Why:** our sub-theme is *Emergency Response & Remote Monitoring*, and the Stage 1 proposal promised BLE telemetry. The ESP32-C3 already has the radio, so remote viewing costs **no extra hardware**.
- **Chosen:** a broadcast (advertisement) rather than a connection: state, wet flags, scan number and both zone readings in 13 bytes (`7_firmware/reader_v0_1/ble_beacon.h`). A phone scanner app reads it; `7_firmware/tools/decode_beacon.py` decodes it. The USB CSV log stays the primary record.
- **Verified so far:** compiles (0 warnings); 4 compile-time payload tests; 6 PC decoder tests. **Not yet run on hardware** (bench test T11).
- **Limits (stated):** unencrypted, Bluetooth SIG test company ID, bench use only. A product needs pairing and encryption.
- **Change if:** BLE disturbs the measurement (compare T4 readings with BLE on and off), or a carer study asks for a different channel.
