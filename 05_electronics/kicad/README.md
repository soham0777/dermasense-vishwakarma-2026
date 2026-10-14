# KiCad: two-zone reader v0.1 schematic

**Status:**
- ERC passes: 0 violations at every severity (KiCad 10.0.6).
- Netlist cross-checked against the firmware: 0 mismatches.
- No PCB yet. The bench reader is built on perfboard from modules (`07_firmware/WIRING.md`). A PCB is justified only after the bench test and E4.

| File | What it is |
|---|---|
| `make_reader_schematic.py` | Generates the schematic from real KiCad library symbols, runs ERC and exports. **Edit this, not the .kicad_sch** |
| `reader_v0_1.kicad_sch` / `.kicad_pro` | The schematic (opens in KiCad 10) |
| `sym-lib-table`, `fp-lib-table` | Project library tables (use KiCad's own `KICAD10_*_DIR` variables) |
| `out/reader_v0_1_schematic.pdf` | Printable schematic |
| `out/erc.json`, `out/erc.rpt` | ERC results |
| `out/reader_v0_1.net` | Netlist (read by `07_firmware/tools/check_consistency.py`) |
| `out/reader_v0_1_bom.csv` | Parts list from the schematic |

**Circuit in one line:** each zone is driven through 1 kΩ from a GPIO into node N, which returns through a 100 kΩ 0.1 % reference resistor. The ADS1115 reads N, and the polarity is swapped every scan, so the strip sees no net DC. A second 100 kΩ resistor checks the reader itself. The values are justified in `../calc_readout_report.md`.

**Regenerate:**

```bash
python make_reader_schematic.py
```
