# 07_firmware: minimum two-zone reader v0.1

**Status:**
- Compiles for ESP32-C3 with 0 warnings; its 19 compile-time logic tests pass.
- **Not yet run on hardware.** Next is `BENCH_TEST.md` with known resistors.
- Wired logging over USB only (no radio yet).

| File | What it is |
|---|---|
| `reader_v0_1/reader_v0_1.ino` | Scan loop: check resistor → zone C → zone A → COM loop, then one CSV line per scan; LEDs |
| `reader_v0_1/config.h` | Pins, circuit values and thresholds (`[PROV]` = placeholder until measured) |
| `reader_v0_1/zone_logic.h` | Pure maths and the state machine: bipolar divider, hysteresis, 3-scan persistence, OK / CHANGE / CHECK / FAULT |
| `reader_v0_1/zone_logic_tests.h` | 19 `static_assert` tests. A wrong result stops the build (proved with a deliberately false assert) |
| `reader_v0_1/ads1115.h` | Minimal ADS1115 driver (single-shot, auto-range; no external library) |
| `tools/serial_logger.py` | PC logger: validates the header and every row, adds PC time, keeps bad lines separately |
| `tools/check_consistency.py` | Cross-checks KiCad netlist ↔ `config.h` ↔ strip pad order, and writes `WIRING.md` |
| `tools/test_*.py` | 10 tests: logger over `loop://`, header contract, deliberately injected design mistakes |
| `WIRING.md` | Point-to-point wiring for perfboard (generated from the schematic) |
| `BENCH_TEST.md`, `bench_test.csv` | Acceptance test with known resistors, and its record |

## Build and flash

```bash
arduino-cli compile --fqbn esp32:esp32:esp32c3:CDCOnBoot=cdc reader_v0_1
```

```bash
arduino-cli upload --fqbn esp32:esp32:esp32c3:CDCOnBoot=cdc -p COM5 reader_v0_1
```

```bash
python tools/serial_logger.py --port COM5 --minutes 30
```

`CDCOnBoot=cdc` is needed because the SuperMini's USB-C is the chip's native USB.

## States

| C (pad centre) | A (change line) | State | LED |
|---|---|---|---|
| dry | dry | OK | green |
| wet | dry | OK (exudate contained) | green |
| wet | wet | **CHANGE** | amber |
| dry | wet | **CHECK**: A wet before C (edge leak or misplaced strip) | red blinking |
| any | any | **FAULT**: loop open, check resistor off by more than ±5 %, Vdd out of range, or ADC error | red steady |

- **Wet** means below 100 kΩ, and **dry** means above 300 kΩ. A zone only changes after 3 consecutive scans.
- These thresholds come from calculation (`05_electronics/calc_readout.py`), not from measurement. E4 must confirm them on real dressings.
