// Bluetooth LE broadcast of the reader state (remote view without lifting the dressing or plugging in a cable).
// Pure packing only (no Arduino calls), so zone_logic_tests.h can check it at compile time.
// The reader advertises this payload as manufacturer data; any phone BLE scanner (e.g. nRF Connect) shows it.
// Bench prototype only: the broadcast is NOT encrypted and the 0xFFFF company ID is the Bluetooth SIG test value.
// A product would need pairing/encryption and its own company ID.
//
// Byte  Meaning
// 0-1   company ID 0xFFFF (little endian)
// 2-3   'D' 'S' (Dermasense)
// 4     payload version (1)
// 5     state: 0 OK, 1 CHANGE, 2 CHECK, 3 FAULT  (zl::State)
// 6     flags: bit0 C wet, bit1 A wet, bit2 ADC, bit3 CHECK_R, bit4 VDD, bit5 LOOP_OPEN
// 7-8   scan number (uint16, wraps)
// 9-10  zone C resistance in 100-ohm steps (uint16); 0xFFFF = open or above 6.55 Mohm
// 11-12 zone A resistance, same coding
#pragma once
#include <stdint.h>

#include "zone_logic.h"

namespace bb {
constexpr uint16_t COMPANY_ID = 0xFFFF;
constexpr uint8_t VERSION = 1;
constexpr uint8_t LEN = 13;
constexpr uint8_t F_C_WET = 1, F_A_WET = 2, F_ADC = 4, F_CHECK_R = 8, F_VDD = 16, F_LOOP_OPEN = 32;
constexpr uint16_t R_OPEN = 0xFFFF;

struct Payload {
  uint8_t b[LEN] = {};
};

constexpr uint16_t r_code(double ohm) {   // NaN, open and > 6.55 Mohm all read as R_OPEN
  return !(ohm >= 0.0) || ohm >= 65534.5 * 100.0 ? R_OPEN : static_cast<uint16_t>(ohm / 100.0 + 0.5);
}

constexpr Payload pack(zl::State s, uint8_t flags, uint32_t scan, double rc, double ra) {
  Payload p{};
  const uint16_t n = static_cast<uint16_t>(scan & 0xFFFF), c = r_code(rc), a = r_code(ra);
  p.b[0] = COMPANY_ID & 0xFF;
  p.b[1] = COMPANY_ID >> 8;
  p.b[2] = 'D';
  p.b[3] = 'S';
  p.b[4] = VERSION;
  p.b[5] = static_cast<uint8_t>(s);
  p.b[6] = flags;
  p.b[7] = n & 0xFF;
  p.b[8] = n >> 8;
  p.b[9] = c & 0xFF;
  p.b[10] = c >> 8;
  p.b[11] = a & 0xFF;
  p.b[12] = a >> 8;
  return p;
}
}  // namespace bb
