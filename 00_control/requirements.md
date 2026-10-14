# Requirements

**Status:** iteration 1, 2026-10-14.

Each line has an ID. `traceability.csv` links every ID to its design element and the test that proves it. User needs are **ASSUMED** until the Step 2 interviews confirm or change them.

---

## 1. Intended use: what we may and may not say

**Prototype (now):**

> A research prototype for **bench testing** on dressing materials and wound phantoms. It is **not a medical device**, makes **no diagnostic claims**, and is **not used on patients or volunteers' wounds.**

**Product hypothesis (to be proven, never claimed before evidence):**

> A disposable LIG sensor in the dressing plus a reusable pod that shows a nurse the *moisture state* and *temperature trend* of a wound without opening the dressing, to help decide **when** the dressing needs attention.

**Words we avoid until we have clinical evidence:** "detects infection", "diagnoses", "heals faster", "reduces dressing changes by X %".
**Words we use instead:** "indicates moisture state", "shows temperature trend", "designed to support".

---

## 2. User needs (UN): ASSUMED until Step 2

| ID | Need | Who | Evidence so far |
|---|---|---|---|
| UN-1 | Know whether a dressing needs changing **without removing it** | Nurse | `[LIT L08]`: 44.9 % of changes made at optimal moisture |
| UN-2 | Notice a wound **getting worse** between visits | Nurse, doctor | `[LIT L10, L11]`: temperature is a weak-to-fair indicator; `[LIT L12]`: pH |
| UN-3 | Fewer painful removals and clinic trips | Patient, family | Assumed |
| UN-4 | Affordable for Indian clinics | Hospital, patient | Assumed. Interviews should reveal what dressings cost now |
| UN-5 | Fits the existing routine: no extra step longer than about 1 minute | Nurse | Assumed |
| UN-6 | Patient data stays private | Everyone | Ethical/legal baseline |

---

## 3. Product requirements (PR)

| ID | Requirement | From |
|---|---|---|
| PR-1 | Indicate dressing moisture state (dry / optimal / wet) at least every 10 min | UN-1 |
| PR-2 | Report wound-area temperature and its trend | UN-2 |
| PR-3 | *(stretch)* Report wound-fluid pH, pH 5–9 | UN-2 |
| PR-4 | Show readings on a phone without opening the dressing | UN-1, UN-5 |
| PR-5 | Disposable sensor; reusable pod clips on and off in < 30 s without tools | UN-4, UN-5 |
| PR-6 | Disposable part materials ≤ ₹100 at prototype scale (target to revisit after interviews) | UN-4 |
| PR-7 | At least 7 days per charge | UN-5 |
| PR-8 | Skin side: no sharp edges; everything except the sensing area encapsulated; biocompatibility evaluated before any skin contact | Safety |
| PR-9 | Battery-only; measurement currents limited by design; no electrical stimulation in v1 | Safety |
| PR-10 | No personal identifiers on the device; BLE pairing required; data stored only on the phone in the prototype | UN-6 |

---

## 4. Engineering specifications (ES): measurable, each with a test

| ID | Specification | Verified by |
|---|---|---|
| ES-1 | LIG sheet resistance ≤ 100 Ω/sq (aim 20–60); coefficient of variation ≤ 20 % over 5 coupons on 2 days | T-LIG-01 (transmission-line method on test coupon) |
| ES-2 | S1: \|Z\| at 1 kHz differs by ≥ 3× between dry, optimal and wet bands; CV ≤ 15 % (3 sensors × 3 repeats) | T-S1-01 |
| ES-3 | S1: temperature effect characterised over 25–40 °C and corrected using S2 | T-S1-02 |
| ES-4 | S2: IC within ±0.2 °C of a reference thermometer over 25–42 °C | T-S2-01 |
| ES-5 | S2: LIG thermistor sensitivity (%/°C) measured with confidence interval; humidity effect measured | T-S2-02 |
| ES-6 | S3: slope ≥ 50 mV/pH, R² ≥ 0.99 over pH 5–9; drift ≤ 2 mV/h over 6 h; temperature effect measured | T-S3-01, T-S3-02 |
| ES-7 | Sensor: ΔR ≤ 10 % after 1,000 bends at 10 mm radius | T-MECH-01 |
| ES-8 | Pad contact resistance ≤ 5 Ω and stable over 50 connect/disconnect cycles | T-CON-01 |
| ES-9 | BLE: no lost readings over 1 h at 5 m | T-EL-02 |
| ES-10 | Average current ≤ 0.9 mA (150 mAh over 168 h) | T-EL-03 |
| ES-11 | Excitation through tissue-side electrodes is AC only, ≤ 10 µA and ≤ 100 mV rms, with DC blocked. This is below IEC 60601-1 patient-auxiliary-current limits `[SUPPORTED, check the standard text]` | T-EL-04 |

---

## 5. How each sensor gets validated (prototype level)

| | Controls | Calibration | Interference to test | Repeatability |
|---|---|---|---|---|
| **S1** | Bare polyimide (no LIG); commercial LCR meter as reference instrument; dry dressing | NaCl solutions of known conductivity | Temperature, salt concentration, partial wetting, dressing type, pressure, protein (BSA) fouling | 3 sensors × 3 runs; CV |
| **S2** | Reference thermometer; IC vs LIG side by side | 2–3 point (water bath) | Humidity, bending, ambient air temperature | 3 sensors; 24 h drift |
| **S3** | Commercial glass pH meter; bare LIG electrode (expected to respond poorly) | pH 4 / 7 / 9.2 buffers, before and after each run | Temperature, ionic strength, protein (BSA), ascorbic acid, light | 3 electrodes × 3 runs; 6 h drift; 1-week storage |

**Every test** is logged in `test_log.csv`. We report mean ± SD and n, and failures get a row too.

---

## 6. From research prototype to medical device: what it would take

We are at the **bench** stage. A real device would need:

1. **Bench validation** (us, now).
2. **Phantoms and wound models** (us, Stage 3).
3. **Biocompatibility**:
   - ISO 10993-5 cytotoxicity
   - ISO 10993-10 sensitisation
   - ISO 10993-23 irritation
   - these are done by an accredited lab
4. **Pre-clinical** work with partners.
5. **A clinical investigation** with ethics committee approval.
6. **Regulatory approval** in India under CDSCO's Medical Devices Rules 2017. Typical standards:
   - ISO 13485 (quality system)
   - ISO 14971 (risk)
   - IEC 60601-1 and -1-11 (electrical safety, home use)
   - IEC 62304 (software)
   - IEC 62366-1 (usability)
   - device classification still to be determined

None of this is needed to build the prototype. All of it must be named honestly in the deck as the road ahead.
