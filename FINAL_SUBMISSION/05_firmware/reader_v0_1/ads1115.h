// Minimal ADS1115 driver (single-shot, single-ended, auto-range). No external library needed.
// Register map and bit fields: TI ADS1115 datasheet (SBAS444), section 9.6.
#pragma once
#include <Arduino.h>
#include <Wire.h>

class ADS1115 {
 public:
  static constexpr float FSR[6] = {6.144f, 4.096f, 2.048f, 1.024f, 0.512f, 0.256f};  // PGA 0..5, volts

  bool begin(TwoWire& wire, uint8_t addr) {
    wire_ = &wire;
    addr_ = addr;
    wire_->beginTransmission(addr_);
    return wire_->endTransmission() == 0;
  }

  // One conversion of AINch vs GND at PGA index pga (0..5). Returns volts; ok = false on I2C error or timeout.
  float readSingle(uint8_t ch, uint8_t pga, bool& ok) {
    const uint16_t cfg = 0x8000                        // OS: start a single conversion
                         | (uint16_t)((4 + ch) << 12)  // MUX: AINch vs GND
                         | (uint16_t)(pga << 9)        // PGA
                         | 0x0100                      // MODE: single-shot
                         | (0x4 << 5)                  // DR: 128 SPS
                         | 0x0003;                     // comparator off
    ok = writeReg(0x01, cfg);
    if (!ok) return NAN;
    const uint32_t t0 = millis();
    uint16_t r = 0;
    do {                                               // OS reads 1 when the conversion is done
      delay(1);
      ok = readReg(0x01, r);
      if (!ok) return NAN;
    } while (!(r & 0x8000) && millis() - t0 < 30);
    if (!(r & 0x8000)) {
      ok = false;
      return NAN;
    }
    ok = readReg(0x00, r);
    return ok ? (int16_t)r * FSR[pga] / 32768.0f : NAN;
  }

  // Read at +/-4.096 V, then repeat at the smallest range that still holds the value (>= 10 % headroom).
  float readAuto(uint8_t ch, bool& ok, uint8_t* used_pga = nullptr) {
    uint8_t pga = 1;
    float v = readSingle(ch, pga, ok);
    if (!ok) return v;
    uint8_t best = 1;
    for (uint8_t i = 2; i < 6; ++i)
      if (fabsf(v) * 1.1f <= FSR[i]) best = i;
    if (best != pga) v = readSingle(ch, best, ok);
    if (used_pga) *used_pga = best;
    return v;
  }

 private:
  TwoWire* wire_ = nullptr;
  uint8_t addr_ = 0x48;

  bool writeReg(uint8_t reg, uint16_t val) {
    wire_->beginTransmission(addr_);
    wire_->write(reg);
    wire_->write((uint8_t)(val >> 8));
    wire_->write((uint8_t)(val & 0xFF));
    return wire_->endTransmission() == 0;
  }
  bool readReg(uint8_t reg, uint16_t& val) {
    wire_->beginTransmission(addr_);
    wire_->write(reg);
    if (wire_->endTransmission(false) != 0) return false;
    if (wire_->requestFrom((int)addr_, 2) != 2) return false;
    val = (uint16_t)(wire_->read() << 8);
    val |= (uint16_t)wire_->read();
    return true;
  }
};
