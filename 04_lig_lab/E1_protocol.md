# Experiment E1: Reproduce and bracket the "setting 12" observation

**Status:** PLANNED, not yet performed (2026-10-14). **Superseded:** carried out as Part A of E2 (`e2/E2_procedure.md`), with the same matrix and new sample IDs. Kept unchanged as the original plan.
**Question:** On *our* 100 W laser and *our* film, does the reference setting reliably produce a conductive, LIG-like layer? How much does the result change when power or speed moves a little, and from one day to the next?
**Evidence categories:** the earlier observation is `[A1]`. Everything this experiment produces is `[B]`. Literature values are `[C]` and are only for comparison.

---

## 1. Fixed conditions (identical for every coupon, recorded once per session)

- Same machine, same film roll/lot, same bed position (mark the corner with tape).
- Focus at the machine's normal focus (record how it was set). No defocus in E1.
- Scan (fill) mode, **interval 0.1 mm**, **1 pass**, air assist low, exhaust ON.
- Film wiped with isopropyl alcohol and taped flat on a flat plate, with no bubbles.
- Record room temperature and chiller water temperature at the start and end.

## 2. The reference condition

- **Power:** the setting "12", in whatever field it was originally set (Session 0 tells us which).
- **Speed (S_ref):** the speed used in the earlier trial.
  - **If nobody remembers it,** run coupon **E1-R** first: all six cells at setting 12, with speeds of 50 / 100 / 150 / 200 / 300 / 400 mm/s.
  - Choose S_ref as the **slowest speed that gives a continuous black layer without holes**.
  - Record why it was chosen.

## 3. The matrix: one factor at a time around the reference

Each test coupon (`lig_test_coupon.dxf`) has 6 colour cells. In LaserCAD each colour layer gets its own power and speed.

| Cell (colour) | Power setting | Speed | What it tests |
|---|---|---|---|
| RED | 10 | S_ref | Power −2 |
| YELLOW | 12 | 0.67 × S_ref | Speed −33 % |
| **GREEN** | **12** | **S_ref** | **Reference (replicate 1)** |
| CYAN | 12 | 1.5 × S_ref | Speed +50 % |
| BLUE | 14 | S_ref | Power +2 |
| **MAGENTA** | **12** | **S_ref** | **Reference (replicate 2)**, at the other end of the coupon |

**Replication:**
- 2 coupons on Day 1 and 2 coupons on Day 2 (different days, same settings), giving 4 coupons.
- The reference has **n = 8 cells** (4 per day); every other condition has n = 4.

**Engraving order:** keep the LaserCAD layer order the same on every coupon, and write down the order.

**If a cell burns through or shows nothing,** record it. Don't change settings mid-experiment; it is a result.

## 4. Sample labels

- **Cell:** `E1-D<day>-C<coupon>-<COLOUR>`, e.g. `E1-D1-C2-GREEN`.
- **Strip within a cell:** add `-L08`, `-L16` or `-L24`.
- Write the coupon ID on the film with a marker before lasing, and photograph it.

## 5. Controls

| Control | Purpose | Expected |
|---|---|---|
| Un-lased film strip (same film) | Proves conduction comes from laser treatment | Meter reads "OL" (open) |
| Two reference resistors (100 Ω and 10 kΩ, 1 %), measured each session with the same leads | Checks the meter and leads | Within the resistor tolerance plus meter accuracy |
| GREEN and MAGENTA cells on every coupon | Process drift and position effect | Similar values if the process is stable |

## 6. Measurements: what each one tells us, and its limits

| Measurement | Equipment | Tells us | Does NOT tell us |
|---|---|---|---|
| Visual grade 0–5 + macro photo with ruler | Phone + ruler or stereo microscope | Whether a continuous dark layer formed; burn-through | Whether it is graphene |
| Strip width at 3 positions | Optical microscope with scale, or a calibrated photo | Line growth vs the drawn 2.00 mm, which sets future gaps | Thickness or depth |
| **Resistance R** of each strip (8, 16, 24 mm), 3 readings each | Digital multimeter, 2-wire | Total resistance = strip + pads + contacts | Not a material property by itself |
| **Sheet resistance Rs** (from the 3 lengths) | Calculation: R = Rs·L/W + R₀ | A material property (Ω/sq) independent of length; R₀ = contact + pads | Bulk conductivity (needs LIG thickness, which we can't measure reliably yet) |
| Tape-peel test on the 8 mm strip (after electrical tests) | Scotch tape | Cohesion/adhesion: does it flake? | Mechanical durability under bending |

**Grade scale:**

| Grade | Meaning |
|---|---|
| 0 | No visible change |
| 1 | Brown/darkened, not continuous |
| 2 | Black but patchy |
| 3 | Continuous black |
| 4 | Black with flakes or ablation |
| 5 | Burn-through |

**Resistance method:**
1. Dab silver paint on each pad and let it dry (≥ 10 min). If you have none, press the probe tips firmly on the pad centres.
2. Take 3 readings per strip, lifting and re-placing the probes each time.
3. Write **all three** readings in `e1_resistance.csv`, with the meter model and range.

**Needs facilities we may not have (ask the mentor / IIT Indore SIC):**
- **Raman spectroscopy:** D, G and 2D bands. This is the only standard way to call it graphene-like carbon.
- **SEM:** porous morphology and cross-section thickness, which conductivity also needs.
- **Until then we report it as a "laser-carbonised conductive layer (LIG-like)".**

## 7. Pre-registered decision rules (set before testing)

- **"LIG-like conductive layer formed" (per cell):**
  - grade 3
  - R² ≥ 0.95 for R vs L
  - R(24 mm) < 1 MΩ
  - tape test pass
  - no burn-through
- **Process window:** the set of conditions where ≥ 3 of 4 cells meet the rule above.
- **Reproducibility of the reference** (coefficient of variation of Rs; reported within each day and between days):

| CV of Rs | Verdict |
|---|---|
| ≤ 20 % | Reproducible |
| 20–40 % | Marginal |
| > 40 % | Not reproducible: investigate tube current and focus before any sensor work |

- **Comparison to literature:** Rs of tens of Ω/sq would be in line with Lin et al. 2014 `[C1]`. **Much higher values are not a failure;** they are the honest number for our machine.

## 8. Data files (raw first; nothing averaged by hand)

| File | One row per |
|---|---|
| `e1_samples.csv` | Cell (fabrication record) |
| `e1_resistance.csv` | Single resistance reading |
| `e1_linewidth.csv` | Width reading |
| `e1_controls.csv` | Control reading |
| `e1_setting_current.csv` | Setting/current pair (Session 0) |
| `photos/` | Original files, never edited; edited copies go in `photos/edited/` |

Then run `python analyze_e1.py`, which writes `e1_summary.csv` and `e1_plots.png`.

## 9. Safety

- Burning polyimide releases irritating and potentially toxic gases. **Exhaust ON, lid closed, don't lean in, and wait for the smoke to clear before opening.**
- **Never leave the laser running unattended.** Keep a CO₂ extinguisher accessible; if there is flame, press stop.
- Use only settings in this plan, starting from the lowest power. Get the lab in-charge's permission for every session.
- Silver paint and isopropyl alcohol are flammable. Use them away from the laser, and wear gloves.

## 10. Time and cost

- **Time:**
  - Session 0: ~20 min
  - Each coupon: ~5 min of lasing
  - Measurements: ~45 min per coupon
- **Total:** two sessions of about 3 h.
- **Consumables:** film you already have; silver paint (~₹600–1,500, estimate); two resistors.
