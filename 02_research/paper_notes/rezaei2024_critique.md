# Critique: Rezaei et al. 2024, "Wearable Kapton graphene biosensor for detection of toxic gases"

*J. Hazard. Mater. Adv.* 15:100452, doi:10.1016/j.hazadv.2024.100452 (the paper uploaded with the brief; full text read).

## What it actually is

- A **computer simulation** (CST Studio, 2023) of a 2.29 × 1.9 mm graphene patch antenna on 125 µm Kapton, resonating at about 80 GHz (scanned 76–86 GHz).
- Gas is modelled as a dielectric layer over the patch, and "detection" is the resonant-frequency shift.
- **No device was made, no gas was tested, and no laser-induced graphene is involved.** The graphene is an idealised sheet described by its theoretical conductivity.

## Does the physics hold? (our check: WRONG)

- At room conditions, gases have a relative permittivity of about **1.0005–1.001** (air ≈ 1.0006). Differences between gases are therefore around 10⁻⁴.
- At **20 ppm**, swapping a little air for CO changes the permittivity by roughly 20×10⁻⁶ × 10⁻⁴ ≈ **10⁻⁹–10⁻⁸**.
- A resonator's frequency shift is at most about half the permittivity change, so we'd expect a relative shift of **≤10⁻⁸**.
- The paper reports relative shifts of **0.12–2.4 %** (Table 1) and "sensitivity above 5 %" at 20 ppm.
- That is **about six orders of magnitude** larger than physics allows.
- Even the paper's own **pure nitrogen** case (N₂ is 78 % of air) shows the *largest* shift (2.4 %), which cannot be right.

## Other problems

- N₂ is listed as a "toxic gas", and "fluorine azide (F₂N)" is not a standard compound name.
- The gas list changes between the abstract, the text and Table 1.
- Running at 76–86 GHz needs millimetre-wave hardware (VNA, waveguide probes), far beyond a wearable or our lab.
- The comparison table (Table 2) sets ppm-level measured results from other papers against simulated ones.

## What we take from it

- **Nothing as evidence of feasibility.** We cite it only as an example of why we test claims experimentally.
- One idea is reusable: modelling a sensor as an equivalent R-L-C circuit. That is standard practice anyway, and we'll use it for our moisture-sensor impedance (electrode + solution model).
- Gas sensing as a whole stays **rejected** for this project (see `03_sensors/concept_comparison.md`, C10).
