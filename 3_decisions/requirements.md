# Requirements and traceability: two-zone strip v0.1

**Status:** 16 Oct 2026. Replaces the iteration-1 list, which covered moisture, temperature and pH; that list is in git history. Each requirement shows the design element that meets it, the test that proves it, and where it stands today.

## Intended use

- **Now:** a research prototype for **bench testing** on dressings with simulated exudate.
  - Not a medical device.
  - Makes no diagnostic claims.
  - Not used on people.
- **Product hypothesis (to be proven, never claimed):** a disposable strip on the dressing pad plus a reusable reader that tells a carer when the exudate front reaches the dressing maker's change line, without lifting the dressing.
- **Words we avoid until there is clinical evidence:** "detects infection", "diagnoses", "heals faster", "reduces dressing changes by X %".

## User needs (assumed until the nurse interviews)

| ID | Need | Evidence so far |
|---|---|---|
| UN-1 | Know whether a dressing needs changing **without removing it** | Milne 2016: 44.9 % of changes made at optimal moisture (`2_research/literature.csv` L08) |
| UN-2 | Fit the existing routine: no extra step longer than about 1 minute | Assumed |
| UN-3 | Affordable for Indian clinics and home care | Assumed |
| UN-4 | Safe: nothing touches the wound bed; no electrical risk | Baseline |

## Requirements → design → test → status

| ID | Requirement | From | Design element | Verified by | Status (16 Oct) |
|---|---|---|---|---|---|
| R1 | Signal CHANGE when the front reaches the change line (zone A wet) | UN-1 | Zones C + A, wet < 100 kΩ, 3 scans (`7_firmware/reader_v0_1/config.h`) | E4: alert within ±10 % of the visible-front volume | Designed; logic verified in software |
| R2 | Flag CHECK when A wets before C (leak or misplaced strip) | UN-1 | `classify()` in `zone_logic.h` | 19 compile-time tests; bench test T6 | Software verified; hardware pending |
| R3 | Flag FAULT for a broken COM loop, a bad check resistor, wrong Vdd or ADC error | UN-4 | Loop path + 100 kΩ check resistor | Bench test T2, T9 | Designed |
| R3a | Detect a broken **sense** lead | UN-4 | **Not covered in v0.1** (FMEA F04) → v0.2 loops each lead | T-MECH-01 + v0.2 design | Open |
| R4 | No net DC on wet electrodes | UN-4 | Bipolar drive; idle pins high-Z | Bench test T8 (< 5 mV) | Designed |
| R5 | Strip never touches the wound bed | UN-4 | Strip on the pad's outer face; leads sealed | Design review; E4 | By design |
| R6 | Strip made by our laser in one pass, with 1.0 mm lines and gaps | UN-3 | `4_sensor_strip/strip_v0_1.dxf` (DRC pass) | E2: smallest reliable line, isolating gap, Rs CV ≤ 20 % | Pending E2 |
| R7 | Reader clips on without tools and aligns itself | UN-2 | Clamp with 4 pogo pins + 2 dowels (`5_cad`) | `verify_cad.py` (99 pass); contact test T-CON-01 | CAD verified; not built |
| R8 | Disposable part ≤ ₹100 at prototype scale | UN-3 | Film + laser carbon only (`6_electronics/bom_v0_1.csv`) | BOM with real prices | Target (estimate) |
| R9 | Every reading logged and validated | UN-1 | CSV over USB + `serial_logger.py` | 10 PC-side tests; bench test T10 | Software verified |
| R10 | The bench reader is never used on a person | UN-4 | USB-powered; labelled "not for patient use" | Lab rule | In force |
| R11 | The strip survives bending at the dressing edge | UN-4 | 0.125 mm polyimide; 0.62 % strain at 10 mm radius (calc) | T-MECH-01: ΔR ≤ 10 % after 1,000 bends | Calculated; untested |

## Road from prototype to device (named honestly, not needed now)

1. Bench validation: E2, the reader bench test, E4.
2. Wound phantoms (Stage 3).
3. Biocompatibility to ISO 10993, by an accredited lab.
4. Electrical safety of a battery-only reader to IEC 60601-1.
5. A clinical investigation with ethics approval.
6. CDSCO Medical Devices Rules 2017 (ISO 13485, ISO 14971).
