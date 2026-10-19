// Compile-time tests of zone_logic.h: if any fails, the sketch does not compile.
// (There is no host C++ compiler on the team laptop; the ESP32 toolchain evaluates these during the build.)
#pragma once
#include "ble_beacon.h"
#include "zone_logic.h"

namespace zl_tests {
using namespace zl;

constexpr bool near(double a, double b, double rel) { return (a > b ? a - b : b - a) <= rel * (b > 0 ? b : -b); }

// --- divider maths: Rx = Rref gives V_N = Vdd/2 in both phases
static_assert(near(rx_plus(1.65, 3.3, 100e3, 0.002), 100e3, 1e-12), "phase + at Rx = Rref");
static_assert(near(rx_minus(1.65, 3.3, 100e3, 0.002), 100e3, 1e-12), "phase - at Rx = Rref");
// Rx = 10 k: V+ = 3.3 * 100/110 = 3.0 V, V- = 3.3 * 10/110 = 0.3 V
static_assert(near(rx_plus(3.0, 3.3, 100e3, 0.002), 10e3, 1e-9), "phase + at 10 k");
static_assert(near(rx_minus(0.3, 3.3, 100e3, 0.002), 10e3, 1e-9), "phase - at 10 k");
// open path: node pinned to the REF rail
static_assert(rx_plus(0.0005, 3.3, 100e3, 0.002) >= INF, "open in phase +");
static_assert(rx_minus(3.2995, 3.3, 100e3, 0.002) >= INF, "open in phase -");
static_assert(combine(10e3, 12e3) == 11e3 && combine(10e3, INF) >= INF, "combine");
static_assert(minus_series(12e3, 2e3) == 10e3 && minus_series(1e3, 2e3) == 0.0 && minus_series(INF, 2e3) >= INF, "series");
static_assert(near(scale(100e3, 1.02), 102e3, 1e-12) && scale(INF, 1.02) >= INF, "scale");

// --- zone state machine
constexpr Zone run(const double* r, int n) {
  Zone z{};
  for (int i = 0; i < n; ++i) z = step_zone(z, r[i], 100e3, 300e3, 3);
  return z;
}
constexpr double two_wet[] = {10e3, 10e3};
constexpr double three_wet[] = {10e3, 10e3, 10e3};
constexpr double glitch[] = {10e3, 10e3, 1e9, 10e3, 10e3};          // a dry glitch restarts the count
constexpr double band[] = {10e3, 10e3, 10e3, 200e3, 200e3, 200e3};  // 200 k is inside the band: stays wet
constexpr double dry_again[] = {10e3, 10e3, 10e3, 400e3, 400e3, 400e3};
static_assert(run(two_wet, 2).stable == Wet::DRY, "2 wet scans are not enough");
static_assert(run(three_wet, 3).stable == Wet::WET, "3 wet scans -> wet");
static_assert(run(glitch, 5).stable == Wet::DRY, "persistence must be consecutive");
static_assert(run(band, 6).stable == Wet::WET, "hysteresis band keeps the state");
static_assert(run(dry_again, 6).stable == Wet::DRY, "3 dry scans -> dry");

// --- classification
static_assert(classify(Wet::DRY, Wet::DRY, false) == State::Ok, "dry");
static_assert(classify(Wet::WET, Wet::DRY, false) == State::Ok, "exudate contained at the centre");
static_assert(classify(Wet::WET, Wet::WET, false) == State::Change, "front reached the change line");
static_assert(classify(Wet::DRY, Wet::WET, false) == State::Check, "A wet before C: leak or wrong placement");
static_assert(classify(Wet::WET, Wet::WET, true) == State::Fault, "fault overrides");

// --- BLE broadcast payload (ble_beacon.h)
static_assert(bb::r_code(12345.0) == 123 && bb::r_code(0.0) == 0, "resistance in 100-ohm steps");
static_assert(bb::r_code(INF) == bb::R_OPEN && bb::r_code(7e6) == bb::R_OPEN && bb::r_code(__builtin_nan("")) == bb::R_OPEN,
              "open, out of range and NaN all read as open");
constexpr bb::Payload change_pkt = bb::pack(State::Change, bb::F_C_WET | bb::F_A_WET, 0x10203, 4200.0, 15000.0);
static_assert(change_pkt.b[0] == 0xFF && change_pkt.b[1] == 0xFF && change_pkt.b[2] == 'D' && change_pkt.b[3] == 'S' &&
                  change_pkt.b[4] == bb::VERSION,
              "header: test company ID, magic, version");
static_assert(change_pkt.b[5] == 1 && change_pkt.b[6] == 3 && change_pkt.b[7] == 0x03 && change_pkt.b[8] == 0x02 &&
                  change_pkt.b[9] == 42 && change_pkt.b[10] == 0 && change_pkt.b[11] == 150 && change_pkt.b[12] == 0,
              "state, flags, scan (low 16 bits, little endian), zone resistances");
}  // namespace zl_tests
