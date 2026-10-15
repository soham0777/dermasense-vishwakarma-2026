# Reader v0.1 bench test (known resistors in place of the strip)

**Status:** READY. The firmware compiles; it has **not yet run on hardware**. This test is what makes it a *working* reader.
**Time:** about 1.5 h once the board is wired. **Record in:** `bench_test.csv` (one row per step).

## You need

- The wired reader (see `WIRING.md`). Check every row of `WIRING.md` with the continuity beeper **before** powering up.
- A USB-C cable and a laptop with `python tools/serial_logger.py`.
- 1 % resistors: 1 k, 10 k (×3), 47 k, 100 k, 220 k, 470 k, 1 M.
- A DMM (the same one as E2).
- Crocodile leads or a breadboard to put resistors across the J4 pins. J4.1 = SENSE_C, J4.2 = SENSE_A, J4.3 = COM_1, J4.4 = COM_2.

**Zone C resistor:** J4.1 ↔ J4.3. **Zone A resistor:** J4.2 ↔ J4.3. **Loop resistor** (stands in for the strip's COM loop): J4.4 ↔ J4.3.

## Steps

| # | Do | Pass if |
|---|---|---|
| T0 | Measure every test resistor with the DMM and write the value down. These are the "true" values. | Within its 1 % tolerance |
| T1 | Flash: `arduino-cli compile --fqbn esp32:esp32:esp32c3:CDCOnBoot=cdc --upload -p COMx reader_v0_1`. Then start the logger: `python tools/serial_logger.py --port COMx`. | The banner shows `ADS1115 found`; the header is accepted |
| T2 | Nothing on J4. | `k_check` between 0.95 and 1.05; `rc`, `ra`, `rloop` = inf; state **FAULT**, flag `LOOP_OPEN` (red LED steady) |
| T3 | Loop resistor 10 k. | `rloop` within ±2 % of the DMM value; state **OK** (green); flags empty |
| T4 | Keep the loop at 10 k. Zone C = 1 k, 10 k, 47 k, 100 k, 220 k, 470 k, 1 M in turn, 5 scans each. | `rc` (median of 5) within ±2 % of the DMM value (or ±30 Ω at 1 k) for 1 k–220 k, and within ±5 % for 470 k–1 M |
| T5 | Repeat T4 for zone A. | Same limits for `ra` |
| T6 | State sequence (loop 10 k): (a) C open, A open → (b) C 10 k → (c) C 10 k + A 10 k → (d) C open, A 10 k. Note the scan number at each change. | (a) OK · (b) OK, `c_wet` becomes 1 after exactly 3 scans · (c) **CHANGE** (amber) after 3 scans · (d) **CHECK** (red blinking) after 3 scans |
| T7 | Hysteresis: zone C wet (10 k for ≥ 3 scans), then 220 k for 5 scans, then 470 k. | `c_wet` stays 1 at 220 k; drops to 0 after 3 scans at 470 k |
| T8 | **No net DC on the strip.** Zone C = 10 k. DMM on DC volts across J4.1–J4.3 for 30 s. | Average reading within ±5 mV (the drive is bipolar and idle pins are high-Z) |
| T9 | Remove the loop resistor during operation. | **FAULT** on the next scan; zones frozen (no state change while faulted) |
| T10 | Log 30 min with C 10 k, A 100 k, loop 10 k. | No bad lines in `.bad.txt`; `rc` drift (max − min) < 1 %; no resets |

**If a step fails:** don't change the firmware to make the numbers fit. Write down the result and look first for a wiring error (re-run `WIRING.md` with the beeper). Only change `config.h` with a written reason.

**What this does NOT test:**
- the real strip
- real dressings or fluid (E4)
- the pogo-pin contact (T-CON-01)
- battery operation

The reader runs on USB from a laptop. It is a bench tool, not for patient use.
