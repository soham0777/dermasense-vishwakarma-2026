# 09_procurement: bill of materials v0.1 (bench prototype)

`bom_v0_1.csv`: 23 lines. Each line traces to the file that needs it (`requirement_source`).

| Needed for | Estimated cost (₹) |
|---|---|
| E2 fabrication validation (includes borrowing or buying a ≥ 20 MΩ DMM) | 1,120 – 6,720 |
| Reader (electronics) | 610 – 1,520 |
| Contact clamp | 110 – 600 |
| Bench rig | 40 – 720 |
| Strip seal tape | 200 – 500 |
| E4 dressings (later) | 300 – 900 |
| **Total** | **≈ 2,400 – 11,000** |

**Every price is an estimate (`price_status`).** Check the supplier page and write the real price and date into the CSV before ordering. Fill in `have_it_YN` first, because many items may already be in the lab.

**Order first** (they block E2 and the reader bench test):
- silver paint (P02)
- the 1 % resistor set (P03)
- 0.1 % 100 kΩ resistors (R03)
- ADS1115 (R02)
- ESP32-C3 SuperMini (R01)
- a ≥ 20 MΩ multimeter if the lab has none (P08)

`../05_electronics/bom_preliminary.csv` is the iteration-1 multi-sensor list. It is kept for the upgrade path; it is not the v0.1 build.
