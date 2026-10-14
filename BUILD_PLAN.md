# Build plan

**How this works**

- Every step has a **check**. We don't move on until it passes, or until we've written down why it failed and what we're changing.
- After each step, send the results to Claude for review against the check.
- Steps 2 and 3 run **in parallel**: one person talks to people, the other works the laser.

**Proposed sensors** (details in `03_sensors/concept_comparison.md`; awaiting team approval, D-002):
- **S1** moisture (impedance)
- **S2** temperature (IC + LIG thermistor)
- **S3** pH, later

## Part 1: Stage 2 (deadline Sun 25 Oct, 23:59; we submit Sat 24)

| # | Step | Dates | Depends on |
|---|---|---|---|
| 1 | Write down our setup; approve sensor portfolio | Wed 14 Oct | none |
| 2 | Meet the people who dress wounds | Thu 15 – Sun 18 | 1 |
| 3 | First LIG on our laser | Thu 15 – Sat 17 | 1 |
| 4 | Confirm what v1 does | Mon 19 | 2, 3 |
| 5 | Bench-test S1 and S2 | Mon 19 – Wed 21 | 3, 4 |
| 6 | Electronics on a breadboard (Phase A) | Sun 18 – Thu 22 | 4 |
| 7 | Real design files (SolidWorks + KiCad) | Tue 20 – Fri 23 | 5, 6 |
| 8 | Build and submit the deck | Fri 23 – Sat 24 | all |

### Step 1: Our setup and portfolio approval (today)

**Do:**
- Fill in the "Our setup" section of `README.md`: laser access, film thickness, mentor.
- Read `03_sensors/concept_comparison.md` and answer its §6 questions.
- Install **KiCad**.

**Check:**
- Laser time is booked for 2 days this week.
- Film thickness is known.
- Each decision in `00_control/decisions.md` is marked DECIDED or changed.

### Step 2: Meet the people (Thu 15 – Sun 18)

**Do:**
- Use `01_people/interview_guide.md` with ≥ 3 nurses, 1 doctor and, if possible, 1–2 patients.
- Ask specifically about *when they decide to change a dressing* (S1), *how they spot infection* (S2/S3), and *foot-ulcer prevention* (the C9 pivot).

**Check:**
- ≥ 4 conversations written up.
- Top 3 problems, each backed by ≥ 2 people.
- ≥ 5 quotes.
- At least one finding that goes against our idea.

### Step 3: First LIG (Thu 15 – Sat 17)

**Do:** follow `04_lig_lab/README.md`.

**Check:**
- One recipe is black, conductive, passes the tape test and has no holes.
- Sheet resistance is below 100 Ω/sq.
- The same recipe on another day comes within ±20 % (ES-1, T-LIG-01).
- **Also measure the line width** (photo with a ruler or microscope); it sets the S1/S2 geometry.

### Step 4: Confirm v1 (Mon 19)

**Do:**
- Write `01_people/v1_decision.md`: who, which problem, what it measures, what it doesn't do, with an interview quote behind every requirement.
- Mark the UN rows in `00_control/requirements.md` as CONFIRMED or CHANGED.

**Check:** someone outside the team understands it in 2 minutes.

### Step 5: Bench-test S1 and S2 (Mon 19 – Wed 21)

**Do:**
- Claude generates the S1 comb and S2 thermistor coupons from the Step 3 line width.
- Then:
  - **T-S1-01:** saline on dressing samples; \|Z\| at 1 kHz with the LCR meter; 3 sensors × 3 repeats.
  - **T-S2-01 / 02:** IC and LIG thermistor against a reference thermometer, 25 → 45 °C, at two humidities.
  - **T-MECH-01:** 1,000 bends at 10 mm radius.

**Check:** ES-2, ES-4, ES-5 and ES-7 results logged in `00_control/test_log.csv`, pass or fail.

### Step 6: Electronics, Phase A (Sun 18 – Thu 22)

**Do:** follow `05_electronics/architecture.md` §3:
- ESP32-C3 + TMP117 + ADS1115 bridge, sending to a phone over BLE (nRF Connect).
- **T-EL-03:** measure the real currents, then rerun `power_budget.py`.

**Check:**
- Known resistors read within 5 %.
- Live phone data for 10 minutes.
- Current measurements recorded.

### Step 7: Real design files (Tue 20 – Fri 23)

**Do:**
- KiCad schematic of exactly what worked in Step 6.
- SolidWorks models P-01, P-03 and F-02 from `06_cad/cad_plan.md` (Claude provides macros or instructions).
- BOM prices checked on supplier pages.

**Check:** files open; schematic matches the breadboard photo; every BOM line has a source.

### Step 8: Deck (Fri 23 – Sat 24)

**Do:** official template, filled only with material from this repo. Any AI image is labelled "AI generated". Unfinished items are shown as *planned*, never as done.

**Check:** the "where's the proof?" test on every slide. **Submit Saturday.**

---

## Part 2: Engineering roadmap after Stage 2

| Phase | When | Goal | Acceptance |
|---|---|---|---|
| **A: bench sensors** | Oct – mid Nov | S1, S2 characterised; S3 pH first coupons | ES-1…ES-7 tested; S3 slope ≥ 50 mV/pH (ES-6) |
| **B: integrated pod** | mid Nov – Dec | AD5941 PCB, pod + patch in SolidWorks, firmware v1, Web Bluetooth app | Gate 2 checklist passed; ES-8…ES-11 |
| **C: phantom validation** | Jan | Gelatin/agar wound phantoms; repeatability n ≥ 3; nurse handling trial | Gate 3 checklist passed |
| **D: Stage 3 package** | Feb | Working-prototype video, honest results, roadmap to biocompatibility and clinical work | Every claim traced to `test_log.csv` |

### Top risks

| Risk | Effect | What we do |
|---|---|---|
| No laser access this week | Stage 2 with no real LIG | Book today; fall back to another maker lab |
| Film is thin tape (~25 µm) | Burn-through, fragile pads | Faster scans; buy ≥ 75 µm film for Phase A |
| LIG pads wear or contact is unstable | Noisy readings | Silver-paint pads; pogo-pin test T-CON-01 |
| S1 reading depends on dressing type | Can't give one "wet" threshold | Calibrate per dressing family; report bands, not absolutes |
| LIG thermistor is humidity-sensitive | S2b unreliable | Encapsulate; IC stays the trusted reading |
| PANi or reference drift (S3) | pH unusable | Keep as a stretch goal; report drift honestly |
| AD5941 sourcing delay | Phase B slips | Order early; AD5933 fallback (D-005) |
| Interviews don't support wound monitoring | Wrong product | C9 foot-insole pivot reuses S2 |

**Budget (estimate):**
- Phase A ≈ ₹3–7k
- Phase B ≈ ₹6–14k
- Within the ₹30k grant if we're among the finalists; before that, from our own funds.
