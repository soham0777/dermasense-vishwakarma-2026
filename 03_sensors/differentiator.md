# Differentiator: what will our sensor do that existing approaches don't?

**Status:** PROPOSED (D-008), 2026-10-14. **Nothing below has been built or tested yet.**

**Labels:** `[LIT]` = literature (IDs in `02_research/literature.csv`) · `[CALC]` = our calculation · `[ASSUMED]` = to be checked · `[OURS]` = our measurement (none yet).

## 1. The specific problem

Nurses change a dressing when it is *full*, not merely when the wound is *wet*. A moist wound bed is the healing goal.

**Dressing makers define "full" spatially:**
- "Change when exudate … approaches 2 cm from the edge of the dressing" (several foam dressings) `[LIT L28]`.
- "Saturated when strike-through has reached 3 edges" (Mepilex Border Flex) `[LIT L28]`.

**Two ways this fails in practice:**
1. **Under compression bandages or opaque secondary dressings**, nobody can see the stain front, so changes happen on a fixed schedule or after leakage `[ASSUMED, check in interviews]`.
2. **A single moisture sensor at the wound** (WoundSense type `[LIT L08]`) reports wound-bed wetness. It reads "wet" early in a dressing's life, because the centre wets first. McColl et al. showed moisture inside dressings is very non-uniform (parts of foams stayed dry under constant injection) `[LIT L26]`. A single-point reading therefore can't tell how much absorbent capacity is left.

## 2. Candidate differentiators (prior art checked before scoring)

| | Differentiator | Prior art found | Novelty | Feasibility (our lab) | Measurable benefit | Cost | What proves it |
|---|---|---|---|---|---|---|---|
| D1 | Temperature-compensated moisture | Standard in conductivity meters (~2 %/°C); Jiang 2022 measured temperature + impedance `[LIT L03]` | **None** | High | **Small for our use.** Dry → wet changes resistance > 100×, so a 2 %/°C correction barely moves a wet/dry threshold `[CALC]` | ~₹450 (TMP117) | Threshold-crossing time with vs without correction, at 25 vs 35 °C |
| D2 | Spatial moisture map at the wound interface (multi-zone array) | McColl 2007, 8-point in-vitro array `[LIT L26]`; several US patents on moisture-map arrays `[LIT L27]` | **Low** (already done; patent-encumbered) | Medium | Moisture distribution; not linked to a change decision | Low | Map vs reference |
| D3 | Performance after repeated bending | Routine in LIG papers | **Low** | High | Durability number | ~0 | ΔR after 1,000 bends |
| D4 | Self-check: tell "dry" from "broken sensor" (continuity loop) | Same idea as ECG lead-off detection | **Low** | High | Removes a dangerous false "dry" reading | ~0 | Cut a trace: does the system flag it? |
| **D5** | **Edge-alert strip:** a narrow LIG strip on the **outer face of the absorbent pad** (never touching the wound), with zones placed at the dressing maker's own change line (2 cm from the edge), plus centre and edge zones | **No publication found** that measures the maker's change criterion electronically and reports **warning lead time vs a single-point sensor**. Moisture-map patents exist, so a **patent search is needed before any IP claim** | **Moderate, uncertain**: the contribution is the *measurand and its validation*, not "a sensor array" | High: pipette, balance, phone camera, our electronics | **Directly measurable:** alert timing vs the visual change criterion; how early a single centre sensor alarms; effect of the strip on the dressing's uptake | **₹** (one LIG strip + polyimide tape) | Experiment E01 |

**Why not "S1 + S2 = innovation"?** Combining sensors isn't a contribution unless the combination changes a decision. D1 alone changes almost nothing here, so we'll *measure* the temperature effect (as the brief asks) but not sell it.

## 3. Recommendation: D5, the edge-alert strip (D4's continuity loop as a built-in safety feature, not a claim)

**What we build:**
- A polyimide strip (15 mm wide in v0.1), laid from the centre of the absorbent pad out past its edge, with the LIG facing the pad.
- Four sensing windows:
  - **C**, centre: this is the single-point baseline
  - **M**, middle
  - **A**, *alert*, 2 cm inside the pad edge, which is the maker's change line
  - **E**, *edge*, 5 mm inside the edge, for leak warning
- All other traces are sealed under a second layer of polyimide tape, with windows cut by the same laser.
- The tail leaves the dressing to a clamp with spring contacts.
- One common electrode runs as a loop (two pads), so a cracked trace is detected (D4).

**What existing approaches don't do:**
- **Visual inspection:** impossible under bandages.
- **Single wound-interface sensor:** measures wound-bed moisture, not remaining capacity, and alarms too early.
- **Interface arrays:** sit in the wound (fouling, biocompatibility burden, occlusion) and output a moisture map, not the change decision.

**Our contribution, to be demonstrated, not assumed:**
1. A sensor that reads out the dressing maker's change criterion directly, without seeing or touching the dressing.
2. A quantified warning lead time, and a quantified early-alarm penalty for a single-point sensor, under controlled exudate loading.
3. Shown to cost ₹-level per strip with one CO₂ laser and no wound contact.

## 4. The experiment that proves or disproves it: E01 (full protocol in `09_experiments/E01_edge_alert/protocol.md`)

| | |
|---|---|
| **Set-up** | Simulated exudate (EN 13726-1 "Solution A": 142 mM Na⁺, 2.5 mM Ca²⁺ as chlorides `[LIT L29]`) fed at a fixed rate into the centre of a dressing on a test rig. |
| **Compared signals (same strip, same electronics)** | **Baseline:** centre zone C alone, i.e. what a single sensor would say. **Comparison:** alert zone A. |
| **Ground truth** | Time-lapse photo of the dyed stain front (the maker's visual criterion, 2 cm from the edge) and the dispensed volume. |

**The benefit is established if, in ≥ 8 of 10 runs across 2 dressing types:**
- zone A's alert falls within **±10 % of the volume** at which the stain visibly reaches the 2 cm line;
- zone C (single point) alerts at **≤ 50 % of that volume**, i.e. it alarms clearly early;
- the strip changes the dressing's uptake by **≤ 10 %** compared with a no-strip control.

**It is disproved if:**
- zone A's timing scatters more than the visual criterion itself (repeat photos), or
- the strip disturbs fluid spread (> 10 % uptake change, or visible channeling along the strip).
