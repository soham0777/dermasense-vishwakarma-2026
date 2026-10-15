# Design FMEA v0.1 (strip + clamp + bench reader)

**Status:** first draft (2026-10-14). The S/O/D ratings are engineering **estimates** made before any test data. Each line names the test that will replace its estimate. Full table: `fmea_v0_1.csv`. Regenerate it with `make_fmea.py`.

| Rank | ID | Failure mode | Effect | S | O | D | RPN | Action | Verified by |
|---|---|---|---|---|---|---|---|---|---|
| 1 | F04 | SENSE_C / SENSE_A lead: Crack or break | That zone reads open = dry forever: CHANGE missed, no alarm | 7 | 4 | 8 | **224** | v0.2 candidate: loop each SENSE lead to a second pad (6-pad strip) so its continuity is checked every scan | design v0.2 + T-MECH-01 |
| 2 | F07 | Sensing concept: Exudate front does not reach the windows as assumed | CHANGE late or never | 7 | 5 | 6 | **210** | Simulated-exudate test on real bordered foam dressings | E4 |
| 3 | F08 | Thresholds: Dry baseline of a humid dressing below 300 kohm | False wet | 6 | 5 | 5 | **150** | Measure dry baselines on dressings; adjust config.h with a written reason | E4 |
| 4 | F01 | Zone electrodes (LIG): Layer not conductive / Rs far higher than expected | Zones always read dry: CHANGE missed | 7 | 5 | 4 | **140** | Run E2; add a per-strip QC record (loop R, both zones dry > 1 Mohm) | E2 |
| 5 | F05 | Pogo-pin contact on LIG pad: High or unstable contact resistance | Readings drift high (towards dry) | 6 | 5 | 4 | **120** | Rounded-head pins; measure contact R vs clamp cycles | T-CON-01 |
| 6 | F15 | Strip material: LIG particles shed into the dressing | Foreign material near the wound | 8 | 3 | 5 | **120** | Literature and standards review of carbon/polyimide contact; shedding test on wet dressing | E2 tape test + E4 + review |
| 7 | F06 | Seal registration: Window shifted onto a lead | Wet lead read as wet zone: early CHANGE/CHECK | 5 | 4 | 5 | **100** | Seal jig using the 2 mm dowels; inspect each strip | E4 |
| 8 | F02 | Electrode gap: Carbon bridges the gap | Zone reads wet when dry: false CHANGE/CHECK | 6 | 4 | 3 | **72** | Set MIN_CLEAR from the E2 smallest isolating gap + growth | E2 |
| 9 | F12 | Fabrication: Operator exposed to polyimide fumes | Respiratory irritation | 8 | 3 | 2 | **48** | Checklist signed every session | E2 safety checklist |
| 10 | F11 | Strip placement: Strip inserted reversed or off-centre | Zones swapped: CHECK instead of OK/CHANGE | 5 | 3 | 3 | **45** | Orientation mark on the paddle; instructions | E4 |
| 11 | F03 | COM loop trace: Crack or break | FAULT shown (no wrong state) | 5 | 4 | 2 | **40** | Bend test of 1.0 mm lines at a 10 mm radius | T-MECH-01 |
| 12 | F13 | Fabrication: Fire in the laser | Injury, equipment damage | 9 | 2 | 2 | **36** | Checklist signed every session | E2 safety checklist |
| 13 | F09 | Readout: Wrong reading from ADC or reference drift | Wrong state | 7 | 2 | 2 | **28** | Bench test T2-T10 | BENCH_TEST |
| 14 | F14 | Bench reader: Mains-connected laptop coupled to a person | Electric shock path | 9 | 1 | 3 | **27** | Battery-only, isolated design before any human use (out of v0.1 scope) | design rule |
| 15 | F10 | Readout: DC current through wet electrodes | Electrode corrosion, drift | 4 | 2 | 3 | **24** | Bench test T8 (average DC < 5 mV) | BENCH_TEST |

**Highest risks:**
- **F07 / F04:** the sensing concept itself, and a broken sense lead that nothing detects.
- **F04 needs a design change** (v0.2: loop each sense lead), not just a test.
- F07 and F08 are retired only by E4 on real dressings.
