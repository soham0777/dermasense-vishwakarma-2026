# Electronics architecture

**Status:** PROPOSED, iteration 1 (2026-10-14). Decisions D-004, D-005 and D-006 are in `00_control/decisions.md`.

## 1. What the electronics must measure

| Channel | Signal | Range / resolution needed | Method |
|---|---|---|---|
| S1 moisture | Impedance between two LIG combs | \|Z\| from ~100 Ω (wet) to > 1 MΩ (dry) at ~1 kHz | Small AC excitation, read amplitude and phase |
| S2a temperature IC | Digital (I²C) | ±0.2 °C over 25–42 °C | Read the IC |
| S2b LIG thermistor | DC resistance, ~8 kΩ, −0.05 %/°C | ~40 µV per 0.1 °C on a 3.3 V bridge | Ratiometric bridge + 16-bit ADC |
| S3 pH | DC potential vs Ag/AgCl, no current | ±0.5 V, 0.5 mV resolution, input impedance > 10¹² Ω | High-impedance buffer + ADC |

## 2. Microcontroller: chosen on what this project needs

| Need | ESP32-C3 | nRF52840 | STM32 (WB55, or L4 + BLE module) |
|---|---|---|---|
| BLE to phone | Built in (BLE 5) `[LIT L25]` | Built in | WB55 built in; L4 needs a module |
| Sleep current | Chip 5 µA `[LIT L25]`; dev boards much more (~43 µA+) | Very low (check datasheet) | Very low |
| Radio current | **Measure** (T-EL-03) | Known to be low (check datasheet) | Low |
| ADC quality | Modest 12-bit SAR | 12-bit SAADC, differential | 12–16-bit |
| DAC | **None** | None (PWM) | Some parts |
| Does ADC/DAC quality matter here? | **No**: precision measurement happens in the front end (ADS1115 / AD5941) | No | No |
| Team experience / tools installed | **Yes**: Arduino ESP32 core 3.3.12, ESP32 libraries already used | No core installed | No tools installed |
| Boards in India | Many, cheap | XIAO nRF52840 ~₹1,150–1,300 (ThinkRobotics; out of stock when checked) | Fewer |
| **Verdict** | **Bench phases now** | **Fallback if the power test fails** | Not chosen: no advantage that outweighs a new toolchain |

**The deciding number is sleep current, not the chip brand.** Running `power_budget.py` with *assumed* currents gives:
- a lean custom board: ~29 days per 150 mAh at 1 reading every 5 minutes
- a dev board (USB chip + LED): ~4.4 days, which misses the 7-day target
- **T-EL-03** replaces these assumptions with measured currents

## 3. Analog front end in two phases

**Phase A: bench (Oct–Nov).** Uses modules and lab instruments, so each sensor can be characterised on its own:

```
S1 IDE  ──────────► Lab LCR meter (1 kHz)      ← reference instrument; no custom circuit yet
S2 IC   ──I²C────► ESP32-C3
S2 LIG  ──bridge─► ADS1115 (diff, ±0.256 V) ──I²C──► ESP32-C3 ──BLE──► phone
S3 pH   ──CMOS buffer (≤1 pA)─► ADS1115 ───────────┘
          (also checked against the lab glass pH meter)
```

**Phase B: our own PCB (Dec).** One chip does S1, S3 and the LIG thermistor:

```
Sensor pads ─pogo pins─► [DC-block caps on S1 drive] ─► AD5941 ─SPI─► ESP32-C3-MINI-1 ─BLE─► phone
                                                 TMP117 ─I²C─┘
LiPo 150–300 mAh ─► protection ─► low-Iq LDO 3.0–3.3 V      (MCP73831 charger: USB only when the pod is undocked)
```

## 4. Connecting the Kapton sensor to the electronics

- **Standard sensor tail.** Every coupon (S1, S2, S3) ends in the same tail:
  - a row of 4 × 4 mm pads at 5.08 mm pitch
  - two laser-cut alignment holes
  - one shared tail means one pod fits all sensors (modular)
- **Pads** are reinforced with silver paint, because bare porous LIG wears under spring contacts.
- **Pod contacts:** spring-loaded pogo pins press onto the pads. Two pins in the pod locate the alignment holes, and magnets or a snap latch hold the pod down.
- **Why not a ZIF/FPC connector:**
  - ZIF needs fine pitch and a precise tail thickness.
  - Our laser lines are ≥ 0.3 mm wide and LIG is porous.
  - This is a hypothesis to test (T-CON-01).
- **Strain relief:** the tail passes under a clamp bar in the pod *before* the pads, so tugging the dressing doesn't move the contacts.
- **Phase A bench wiring:** silver paint plus copper tape or crocodile clips.

## 5. Safety built into the circuit

- **Battery only.** The charge port is covered when the pod is docked on a patch, so it can't charge while worn.
- **S1:** AC excitation only (≤ 100 mV rms, ≤ 10 µA), with series DC-blocking capacitors (ES-11).
- **S3:** potential measurement only, with a series resistor (≥ 100 kΩ) on the input to limit fault current.
- **No stimulation hardware in v1** (D-003).

## 6. Firmware and phone (iteration 2 will detail)

- **Firmware:**
  - a scheduler wakes up, measures, sends, and goes back to sleep
  - each sensor driver sits behind a common interface, so moving to nRF52840 means swapping only the drivers
  - calibration constants are stored in flash
  - each record holds raw value, calibrated value, timestamp and sensor ID, with no personal data
- **Phone, in three stages:**
  1. the free **nRF Connect** app (no code)
  2. a **single-page Web Bluetooth app** (works in Chrome on Android), with a plot and CSV export
  3. a proper app only if the users ask for it

## 7. Preliminary BOM

See `bom_preliminary.csv`. All prices are **estimates** except the lines marked as checked listings.

| Phase | Covers | Estimated cost |
|---|---|---|
| A | Bench sensors + electronics | **₹3,000–7,000** (lab instruments and chemicals assumed available) |
| B | Own PCB + pod | **₹6,000–14,000** |

Verify every price on the supplier page before ordering.
