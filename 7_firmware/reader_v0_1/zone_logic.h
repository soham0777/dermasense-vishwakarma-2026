// Pure measurement maths and the zone state machine (no Arduino calls, so it can be checked at compile time).
// Circuit: drive pin -R_PROT- electrode | fluid | electrode -R_PROT- N -R_REF- REF pin; ADC reads V(N).
//   phase + (drive = Vdd, REF = 0):  V_N = Vdd * Rref / (Rref + Rx)  ->  Rx = Rref * (Vdd / V_N - 1)
//   phase - (drive = 0, REF = Vdd):  V_N = Vdd * Rx / (Rref + Rx)    ->  Rx = Rref * V_N / (Vdd - V_N)
// The two phases carry equal and opposite current, so the strip sees no net DC; averaging them also cancels
// most of the ADC input-loading error.
#pragma once
#include <stdint.h>

namespace zl {
constexpr double INF = 1e12;   // "open circuit"

constexpr double rx_plus(double vn, double vdd, double rref, double vopen) {
  return vn <= vopen ? INF : rref * (vdd / vn - 1.0);
}
constexpr double rx_minus(double vn, double vdd, double rref, double vopen) {
  return (vdd - vn) <= vopen ? INF : rref * vn / (vdd - vn);
}
constexpr double combine(double a, double b) { return (a >= INF || b >= INF) ? INF : 0.5 * (a + b); }
constexpr double scale(double r, double k) { return r >= INF ? INF : r * k; }
constexpr double minus_series(double r, double rs) { return r >= INF ? INF : (r > rs ? r - rs : 0.0); }

enum class Wet : uint8_t { DRY = 0, WET = 1 };
struct Zone {
  Wet stable = Wet::DRY;   // debounced state
  Wet pending = Wet::DRY;  // candidate state
  uint8_t count = 0;       // consecutive scans supporting the candidate
};

// Hysteresis (wet below wet_ohm, dry above dry_ohm, otherwise no evidence) + persistence.
constexpr Zone step_zone(Zone z, double r, double wet_ohm, double dry_ohm, uint8_t persist) {
  const Wet raw = r < wet_ohm ? Wet::WET : (r > dry_ohm ? Wet::DRY : z.stable);
  if (raw == z.stable) {
    z.pending = raw;
    z.count = 0;
    return z;
  }
  if (raw == z.pending) {
    z.count = static_cast<uint8_t>(z.count + 1);
  } else {
    z.pending = raw;
    z.count = 1;
  }
  if (z.count >= persist) {
    z.stable = raw;
    z.count = 0;
  }
  return z;
}

// C = pad centre, A = maker's change line. Moisture spreading outward reaches A after C.
enum class State : uint8_t { Ok = 0, Change = 1, Check = 2, Fault = 3 };  // CamelCase: Arduino #defines CHANGE
constexpr State classify(Wet c, Wet a, bool fault) {
  return fault ? State::Fault
               : (a == Wet::WET ? (c == Wet::WET ? State::Change : State::Check) : State::Ok);
}
constexpr const char* state_name(State s) {
  return s == State::Ok ? "OK" : s == State::Change ? "CHANGE" : s == State::Check ? "CHECK" : "FAULT";
}
}  // namespace zl
