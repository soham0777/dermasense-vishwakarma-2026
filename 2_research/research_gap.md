# Research gap: LIG on Kapton with an industrial 100 W CO₂ laser and low-cost characterisation

**Status:** analysis of 2026-10-14. It is based on targeted searches, not a full systematic review, so **no novelty is claimed** until the "evidence needed" column is satisfied.

**Labels:** `[C]` = published (IDs in `literature.csv` / `3_decisions/evidence_register.csv`) · `[A]` = our earlier observation · `[B]` = to be measured.

| # | Aspect | What the literature already establishes `[C]` | What is still unclear | Can *we* contribute with *our* resources? | Evidence needed before claiming anything |
|---|---|---|---|---|---|
| 1 | LIG forms on Kapton under a CO₂ laser in air | Yes: photothermal mechanism, thresholds, Rs < 35 Ω/sq (L01) | Nothing fundamental | **No.** Reproducing it is a *prerequisite*, not a contribution | E1 shows we can make it at all |
| 2 | Laser parameters → sheet resistance | Well studied: one-factor studies, design-of-experiments, ML prediction (L30, L31, L36); fluence 31–137 J/cm² → Rs 26–49 Ω/sq (L32) | Published windows are **machine- and film-specific** and don't transfer directly | **Locally useful, not novel:** "our machine's window" | E1 matrix |
| 3 | **Run-to-run and day-to-day reproducibility** (CV of Rs) | A desktop CO₂ unit was limited by speed control and thermal management; polyimide **brand** strongly changed quality (L30). The searches found **no reported CV / repeat-batch statistics** | How repeatable is LIG on an **industrial** tube used near the bottom of its power range? | **Yes, plausibly.** Replicated E1 (2 coupons × 2 days) with a pre-registered CV rule | E1 results **+ a deeper literature check** (keywords: "LIG repeatability", "coefficient of variation sheet resistance") before calling it a gap |
| 4 | **Low-PWM operation of a high-power glass tube** for LIG | Engineering measurements: tube current is spiky below ~25 % PWM and only roughly linear at mid range (L34, **not peer-reviewed**). Our "12" is in this range `[A1, C5]` | Whether tube-current instability at low PWM causes measurable LIG variability | **Yes, if the machine has a mA meter:** setting → current → Rs → CV | E1 Session 0 current data + E1 Rs scatter |
| 5 | Low-cost characterisation (multimeter transmission-line method, optical line width) | The transmission-line method is a standard technique; nothing new in it | n/a | **A documentation contribution only:** a reproducible protocol other labs can follow | n/a |
| 6 | Is it graphene? (D/G/2D, morphology) | Needs Raman / SEM (L01) | n/a | **Not without a facility.** Ask the mentor / IIT Indore SIC | Raman spectrum of our best cell |
| 7 | LIG sensors for **dressing** moisture | Wound moisture by impedance exists (WoundSense; McColl 2007 array: L08, L26). Patents on moisture maps (L27). Dressing makers' change rule is spatial (~2 cm from the edge, L28) | No *LIG* strip validated against the makers' change criterion was found in our searches | **Later (E2/E3)**, and only after E1 shows a reproducible process | E3 bench study + a patent search |
| 8 | Closed-loop electrotherapy bandage (Stage 1 idea) | Done at a much higher level (Jiang 2022, L03) | n/a | **No.** Not feasible or defensible with our resources | n/a |

## Conclusion (to be revised after E1)

1. **Most defensible near-term contribution (rows 3–4):**
   - A **quantified reproducibility study** of LIG on Kapton made with an *accessible industrial 100 W CO₂ laser at low power settings*.
   - It links the software setting, tube current and sheet-resistance variation, using only multimeter- and microscope-level measurements.
   - This is a **practical engineering contribution**, not a "first-ever" claim.
2. **Application path (row 7)** stays a **hypothesis** (H-APP1: an edge-alert moisture strip) until the process is shown to be reproducible.
3. **What would kill the contribution:**
   - E1 shows CV ≤ 20 % with no link to tube current, so the machine is simply fine. Then the contribution becomes "documented window + protocol" only.
   - Or the deeper literature check finds published repeatability statistics for comparable machines.
