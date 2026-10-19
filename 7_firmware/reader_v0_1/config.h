// Dermasense two-zone reader v0.1 - configuration. PROVISIONAL until E2/E4 data exist.
// The pin map must match 6_electronics/kicad/reader_v0_1.kicad_sch; 7_firmware/tools/check_consistency.py
// checks it against the KiCad netlist. Values marked [PROV] are placeholders until measured.
#pragma once
#include <stdint.h>

namespace cfg {
constexpr const char* FW_VERSION = "reader_v0_1";

// ---- pins (ESP32-C3 SuperMini). GPIO2/8/9 are strapping pins and stay unused.
constexpr uint8_t PIN_DRV_C = 3;      // R1 -> J4.1 SENSE_C (zone C electrode)
constexpr uint8_t PIN_DRV_A = 4;      // R2 -> J4.2 SENSE_A (zone A electrode)
constexpr uint8_t PIN_DRV_LOOP = 5;   // R4 -> J4.4 COM_2 (COM loop continuity)
constexpr uint8_t PIN_DRV_REF = 10;   // R5 (Rref) -> node N
constexpr uint8_t PIN_DRV_CHK = 20;   // R6 (check resistor) -> node N
constexpr uint8_t PIN_SDA = 6;
constexpr uint8_t PIN_SCL = 7;
constexpr uint8_t PIN_LED_G = 0;      // OK
constexpr uint8_t PIN_LED_Y = 1;      // CHANGE
constexpr uint8_t PIN_LED_R = 21;     // CHECK (blinking) / FAULT (steady)
constexpr uint8_t ADS_ADDR = 0x48;    // ADDR to GND
constexpr uint8_t ADS_CH_NODE = 0;    // A0 = node N
constexpr uint8_t ADS_CH_VDD = 1;     // A1 = 3V3 rail

// ---- circuit values (schematic)
constexpr double R_REF = 100000.0;    // R5, 0.1 %
constexpr double R_CHECK = 100000.0;  // R6, 0.1 %
constexpr double R_PROT = 1000.0;     // R1..R4; a zone or loop path has two in series

// ---- decision thresholds (6_electronics/calc_readout.py) [PROV]
constexpr double WET_OHM = 100e3;     // below -> wet
constexpr double DRY_OHM = 300e3;     // above -> dry (hysteresis band in between)
constexpr uint8_t PERSIST = 3;        // consecutive scans before a zone changes state
constexpr double LOOP_MAX_OHM = 200e3;  // COM loop above this = broken strip/contact [PROV until E2 Rs]
constexpr double CHECK_TOL = 0.05;    // check resistor must read within +/-5 % else FAULT
constexpr double VDD_MIN = 3.0, VDD_MAX = 3.6;

// ---- Bluetooth LE broadcast (ble_beacon.h). Bench prototype: unencrypted, test company ID.
constexpr bool BLE_ENABLED = true;
constexpr const char* BLE_NAME = "Dermasense-R01";
constexpr uint16_t BLE_ADV_INTERVAL = 1600;   // x 0.625 ms = 1 s

// ---- timing
constexpr uint32_t SETTLE_MS = 10;    // >= 10 tau of node N (100 k x 10 nF = 1 ms)
constexpr uint32_t SCAN_PERIOD_MS = 2000;   // bench logging; a wearable would scan every ~60 s
constexpr double V_OPEN = 0.002;      // V: node voltage this close to a rail = open path
}  // namespace cfg
