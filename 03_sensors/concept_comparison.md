# Sensor concepts: comparison and recommended portfolio

**Status:** PROPOSED, iteration 1 (2026-10-14). It needs the team's approval and a check against the nurse interviews (BUILD_PLAN Step 2).

**Labels:** `[LIT]` literature (IDs refer to `02_research/literature.csv`) · `[AI]` Claude's engineering judgment · `[OURS]` our measurements (none yet).

---

## 1. Ground rule: what bare LIG can and can't measure

LIG is a porous, conductive carbon. Many claimed "LIG sensors" depend on a coating or other extra parts. We keep the two apart.

| Measurement | Bare LIG enough? | What else is needed |
|---|---|---|
| Its own resistance changing with **bending/strain** | Yes, strongly | Encapsulation to block humidity |
| Its own resistance changing with **temperature** | Yes, but weakly (≈ −0.05 %/°C) `[LIT L21]` | Good ADC or bridge; encapsulation; a reference thermometer for calibration |
| **Conductivity/impedance of a liquid touching two LIG electrodes** (wetness, exudate) | Yes: LIG is just the electrode `[LIT L08 principle]` | AC readout, calibration solutions, temperature correction |
| **Humidity** of air | Weak on its own | A hygroscopic coating such as graphene oxide `[LIT L14]` |
| **pH** | No: bare LIG is sub-Nernstian `[LIT L15]` | A pH-sensitive coating (PANi) **and** a reference electrode (Ag/AgCl) `[LIT L05, L16]` |
| **Uric acid, dopamine** (direct oxidation) | Partly: oxidises on bare LIG `[LIT L05, L07]` | Potentiostat, reference electrode, interference handling (ascorbate) |
| **Na⁺, K⁺** | No | Ion-selective membrane (ionophore + PVC), reference electrode |
| **Glucose, lactate** | No | Enzyme + mediator layer; stability, pH and temperature correction |
| **Proteins, cytokines** | No | Antibody or aptamer surface chemistry `[LIT L05]` |
| **Gases** (NO₂, CO…) | Weak and humidity-dominated `[LIT L18]` | Coatings or encapsulation, often heating |

**Rule for this project:** every claim we make names its row in this table.

---

## 2. Screening: 11 candidate concepts

| # | Concept | LIG role | Clinical / real-world evidence | Verdict |
|---|---|---|---|---|
| C1 | **Wound moisture/exudate** (impedance between LIG electrodes) | Electrodes only | Moisture-based dressing decisions: 44.9 % of changes happened at optimal moisture `[LIT L08]` | **Shortlist** |
| C2 | **Wound-area temperature** (reference IC + LIG thermistor) | Weak thermistor; IC is the reference | Periwound warmth is linked to infection `[LIT L10]`, but correlation is only fair (r ≈ 0.32) `[LIT L11]` | **Shortlist** |
| C3 | **Wound pH** (PANi-LIG + Ag/AgCl) | Electrode substrate with a coating | Chronic wounds tend to be alkaline `[LIT L12, L13]`; PANi-LIG ≈ 55 mV/pH `[LIT L05, L16]` | **Shortlist (stretch)** |
| C4 | Wound uric acid (bare LIG, voltammetry) | Electrode | Used as a severity marker `[LIT L04]` | Defer: needs a potentiostat; ascorbate interference |
| C5 | Sweat Na⁺/K⁺ | Substrate + membrane | Sweat electrolytes are relevant | Defer: different product; needs sweat induction and microfluidics |
| C6 | Sweat glucose/lactate | Substrate + enzyme | No simple sweat–blood glucose correlation `[LIT L19]` | **Reject** |
| C7 | Respiration (LIG humidity sensor in a mask) | Electrodes + GO | Shown in the literature `[LIT L14]` | Defer: feasible but a separate product, low novelty |
| C8 | Strain/motion | Piezoresistor | Very well explored | Defer: could later flag "dressing disturbed" |
| C9 | **Diabetic-foot temperature insole** (left/right asymmetry) | Thermistor array | RCT: ulcers 12.2 % → 4.7 % with home temperature monitoring `[LIT L09]` | **Pivot option** (see §4) |
| C10 | Toxic gases (the uploaded paper's approach) | Antenna (simulated) | Physically implausible `[LIT L20]`; humidity dominates LIG gas sensors `[LIT L18]` | **Reject** |
| C11 | ECG/biopotential dry electrodes | Electrode | Mature market | Reject: low novelty |

---

## 3. Scored comparison of the five strongest concepts `[AI]`

- **Scale:** 1 (poor) to 5 (good). For cost, power, fabrication and calibration, 5 means *easier or cheaper*.
- **Weights** are in brackets.
- **These are engineering judgments**, written down so they can be argued with. They will be re-scored after Step 3 (our LIG) and Step 2 (interviews).

| Criterion (weight) | C1 Moisture | C2 Temperature | C9 Foot insole | C3 pH | C4 Uric acid |
|---|---|---|---|---|---|
| Clinical relevance (3) | 4 | 3 | 5 | 4 | 3 |
| Unmet need (3) | 4 | 3 | 4 | 3 | 2 |
| Feasibility in our lab (3) | 5 | 5 | 4 | 3 | 3 |
| Fabrication simplicity (2) | 5 | 4 | 4 | 2 | 4 |
| Low cost (2) | 5 | 4 | 4 | 3 | 4 |
| Low power (1) | 4 | 5 | 4 | 4 | 3 |
| Sensitivity (2) | 4 | 5* | 3 | 4 | 3 |
| Selectivity (2) | 2 | 3 | 2 | 3 | 2 |
| Response time (1) | 4 | 3 | 3 | 4 | 4 |
| Repeatability (2) | 3 | 5* | 3 | 2 | 2 |
| Low calibration burden (2) | 3 | 4 | 3 | 2 | 2 |
| Novelty (2) | 2 | 1 | 3 | 3 | 3 |
| Market potential (2) | 3 | 3 | 4 | 3 | 2 |
| Material compatibility (1) | 4 | 4 | 3 | 3 | 4 |
| **Weighted score (out of 5)** | **3.75** | **3.68** | **3.61** | **3.04** | **2.82** |

\* C2 scores well because the *IC* does the accurate measurement. The LIG thermistor alone would score around 2.

**Main weaknesses:**
- **C1, selectivity:** impedance responds to wetness *and* to salt concentration, temperature (~2 %/°C) and how much of the electrode is covered. It indicates *moisture state*, not exudate chemistry.
- **C1, novelty:** WoundSense already does moisture by impedance `[LIT L08]`. Our difference would be **continuous, wireless, LIG-printed, much cheaper**, and that has to be shown, not claimed.
- **C3:** the reference electrode drifts and the PANi film varies from batch to batch. It needs buffer calibration.

---

## 4. Recommended portfolio

**Recommendation: build S1 and S2 now; S3 after S1 passes.** All three measure the same wound bed, share one set of electronics, and come from the same laser process, which makes a coherent product. Each is built on **its own Kapton test coupon** with the same pad layout, so it can be tested alone before integration.

| ID | Sensor | Why it's in | What decides success |
|---|---|---|---|
| **S1** | **Moisture/exudate, impedance IDE** | Strongest need (unnecessary dressing changes), simplest build, intrinsic LIG | Separates dry / optimal / wet reliably on dressing samples |
| **S2** | **Temperature: digital IC (reference) + LIG thermistor (research element)** | Needed anyway to correct S1 and S3 for temperature; the infection link is plausible but weak, so it is presented as *trend* information only | IC within ±0.2 °C of a reference thermometer; LIG thermistor sensitivity measured |
| **S3** | **pH, PANi-LIG + Ag/AgCl** (stretch, Phase A after Stage 2) | Clinically meaningful; shows the "LIG + functional coating" path honestly | ≥ 50 mV/pH, R² ≥ 0.99 (pH 5–9), drift ≤ 2 mV/h |

**Not in v1:**
- **Electrical stimulation:** it is therapy, with electrode-safety and regulatory work, and the Stanford prior art is strong `[LIT L03]`. It stays on the roadmap as module 2.
- **C4–C8, C10, C11:** reasons in §2.

**Pivot option C9 (diabetic-foot insole).** It scores close to C1 and has the strongest clinical trial behind it `[LIT L09]`. It reuses the **same S2 technology** (LIG thermistors + IC + same electronics). If the interviews show nurses care more about *preventing* foot ulcers than *monitoring* them, we switch, and almost nothing is wasted.

---

## 5. Each selected sensor in brief

Geometry here is a **starting hypothesis**. Final dimensions wait for Step 3, because line width and sheet resistance depend on our laser.

### S1: Moisture / exudate (impedance)

- **Principle.** Two interdigitated LIG combs with the dressing or wound fluid between them.
  - Dry: very high, mostly capacitive impedance.
  - Wet with exudate (≈ saline-like conductivity): low, mostly resistive impedance.
  - Measured at ~1 kHz AC, which avoids the polarisation that DC causes on wet electrodes.
- **Starting geometry** `[AI]`:
  - active area 10 × 10 mm
  - finger width 0.6 mm
  - three gap variants (0.6 / 1.0 / 1.5 mm) to test
  - 4–6 fingers per side
  - leads 1.5 mm wide and covered by encapsulation
  - pads 4 × 4 mm
- **Also needed:**
  - encapsulation over leads (polyimide tape overlay or thin PDMS)
  - calibration with NaCl solutions of known conductivity
  - temperature correction from S2
- **Key risks:**
  - the LIG surface may flake when wet and rubbed
  - readings depend on dressing type
  - contact resistance at the pads
- **First experiment (Step 5):** drop known volumes of 0.9 % NaCl onto a dressing piece over the IDE and read |Z| at 1 kHz with the lab LCR meter. Three sensors, three repeats each.

### S2: Temperature

- **Principle.**
  - A digital temperature IC (e.g. TMP117, ±0.1 °C class; datasheet to verify) next to the wound area gives the trusted reading.
  - A LIG serpentine thermistor gives a research comparison.
  - Example LIG thermistor: a 0.5 mm line at 1 mm pitch gives about a 100 mm path in 10 × 10 mm; at 40 Ω/sq that's about 8 kΩ.
- **Expected LIG sensitivity:**
  - 0.1 °C ≈ 0.005 % ΔR, about 40 µV on a 3.3 V divider. That is marginal with a 16-bit ADC (ADS1115).
  - 1 °C is easy to resolve.
- **Hypothesis to test:** covering the thermistor with polyimide tape makes it far less sensitive to humidity.
- **First experiment:** hotplate or water bath (in a sealed bag) from 25 to 45 °C, against a reference thermometer, then repeated at two humidities.

### S3: pH (stretch)

- **Principle.** Polyaniline on LIG changes its potential with pH, at about 55 mV per pH unit `[LIT L05, L16]`. We measure it against an Ag/AgCl reference electrode with a very high-impedance input (no current flows).
- **Starting geometry:** LIG working electrode Ø 3 mm; Ag/AgCl reference Ø 2 mm, 3 mm away.
- **Fabrication options:**
  1. Electropolymerise aniline. This needs a potentiostat.
  2. Chemically polymerise it with ammonium persulfate and drop-cast. No potentiostat is needed, but the film is less uniform.
  - **Safety:** aniline is toxic. Use a fume hood, gloves, and chemistry-lab supervision.
- **Reference electrode:** chlorided silver (silver wire or paint in bleach) as a first version.
- **Calibration and correction:**
  - pH 4 / 7 / 9.2 buffers before and after each use
  - temperature correction from S2: the Nernst slope changes about 0.2 mV per pH per °C
- **Key risks:** reference drift; PANi stability in alkaline, protein-rich fluid `[UNCERTAIN]`.

---

## 6. Decisions the team needs to make now

1. Approve **S1 + S2 now, S3 later**, or change it.
2. Do we keep **wound monitoring** as the product, or keep **C9 (foot insole)** open until the interviews are done? Recommendation: keep it open until 19 Oct.
3. Confirm **electrical stimulation moves to module 2.** The Stage 2 deck can still show it on the roadmap.
