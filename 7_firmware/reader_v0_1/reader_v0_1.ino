// Dermasense two-zone reader v0.1 (bench). ESP32-C3 SuperMini + ADS1115.
// Every scan measures zone C, zone A, the COM loop and the on-board check resistor, then prints one CSV line over USB.
// Wired logging first: no radio. Build: arduino-cli compile --fqbn esp32:esp32:esp32c3:CDCOnBoot=cdc reader_v0_1
// Bench test with known resistors: 7_firmware/BENCH_TEST.md. Log on a PC: python ../tools/serial_logger.py --port COMx
#include <Wire.h>

#include "ads1115.h"
#include "config.h"
#include "zone_logic.h"
#include "zone_logic_tests.h"   // compile-time tests

// The PC logger checks this exact header (7_firmware/tools/serial_logger.py EXPECTED_HEADER).
static const char* CSV_HEADER =
    "ms,scan,vdd_V,rc_ohm,ra_ohm,rloop_ohm,rcheck_ohm,k_check,c_wet,a_wet,state,flags";

static const uint8_t DRIVE_PINS[] = {cfg::PIN_DRV_C, cfg::PIN_DRV_A, cfg::PIN_DRV_LOOP, cfg::PIN_DRV_REF, cfg::PIN_DRV_CHK};

ADS1115 adc;
zl::Zone zone_c, zone_a;
uint32_t scan_no = 0, last_scan = 0, last_blink = 0;
zl::State state = zl::State::Ok;
bool adc_present = false, blink_on = false;

struct Path {
  double r = zl::INF;   // series resistance between the drive pin and node N (ohm)
  double vdd = NAN;     // measured 3V3 rail (V)
  bool ok = false;      // ADC conversions succeeded
};

static void release_all() {   // every drive pin high-Z: no current through the strip between scans
  for (uint8_t p : DRIVE_PINS) pinMode(p, INPUT);
}

static void drive(uint8_t pin, bool high) {
  pinMode(pin, OUTPUT);
  digitalWrite(pin, high ? HIGH : LOW);
}

// Bipolar measurement of one path (drive pin vs the reference resistor). Both phases take the same time.
static Path measure(uint8_t drv) {
  Path out;
  bool ok1, ok2, ok3, ok4;
  release_all();
  drive(drv, true);
  drive(cfg::PIN_DRV_REF, false);
  delay(cfg::SETTLE_MS);
  const float vdd_p = adc.readSingle(cfg::ADS_CH_VDD, 1, ok1);
  const float vn_p = adc.readAuto(cfg::ADS_CH_NODE, ok2);
  drive(drv, false);
  drive(cfg::PIN_DRV_REF, true);
  delay(cfg::SETTLE_MS);
  const float vdd_m = adc.readSingle(cfg::ADS_CH_VDD, 1, ok3);
  const float vn_m = adc.readAuto(cfg::ADS_CH_NODE, ok4);
  release_all();
  out.ok = ok1 && ok2 && ok3 && ok4;
  if (!out.ok) return out;
  out.vdd = 0.5 * (vdd_p + vdd_m);
  out.r = zl::combine(zl::rx_plus(vn_p, out.vdd, cfg::R_REF, cfg::V_OPEN),
                      zl::rx_minus(vn_m, out.vdd, cfg::R_REF, cfg::V_OPEN));
  return out;
}

static void print_r(double r) {
  if (r >= zl::INF) Serial.print("inf");
  else Serial.print(r, 0);
}

static void set_leds() {
  digitalWrite(cfg::PIN_LED_G, state == zl::State::Ok ? HIGH : LOW);
  digitalWrite(cfg::PIN_LED_Y, state == zl::State::Change ? HIGH : LOW);
  const bool red = state == zl::State::Fault || (state == zl::State::Check && blink_on);
  digitalWrite(cfg::PIN_LED_R, red ? HIGH : LOW);
}

static void scan() {
  String flags;
  const Path chk = measure(cfg::PIN_DRV_CHK);
  const Path pc = measure(cfg::PIN_DRV_C);
  const Path pa = measure(cfg::PIN_DRV_A);
  const Path pl = measure(cfg::PIN_DRV_LOOP);
  const bool adc_ok = chk.ok && pc.ok && pa.ok && pl.ok;
  // Gain/loading correction from the known check resistor (valid near 100 k, i.e. near the thresholds).
  double k = (chk.ok && chk.r < zl::INF && chk.r > 0) ? cfg::R_CHECK / chk.r : NAN;
  const bool k_ok = !isnan(k) && fabs(k - 1.0) <= cfg::CHECK_TOL;
  if (!k_ok) k = 1.0;
  const double two_rp = 2.0 * cfg::R_PROT;
  const double rc = zl::minus_series(zl::scale(pc.r, k), two_rp);
  const double ra = zl::minus_series(zl::scale(pa.r, k), two_rp);
  const double rl = zl::minus_series(zl::scale(pl.r, k), two_rp);
  const double vdd = chk.vdd;
  const bool vdd_ok = !isnan(vdd) && vdd >= cfg::VDD_MIN && vdd <= cfg::VDD_MAX;

  if (!adc_present || !adc_ok) flags += "ADC;";
  if (!k_ok) flags += "CHECK_R;";
  if (!vdd_ok) flags += "VDD;";
  if (rl > cfg::LOOP_MAX_OHM) flags += "LOOP_OPEN;";
  const bool fault = flags.length() > 0;
  if (!fault) {   // only update the zones from trustworthy readings
    zone_c = zl::step_zone(zone_c, rc, cfg::WET_OHM, cfg::DRY_OHM, cfg::PERSIST);
    zone_a = zl::step_zone(zone_a, ra, cfg::WET_OHM, cfg::DRY_OHM, cfg::PERSIST);
  }
  state = zl::classify(zone_c.stable, zone_a.stable, fault);

  Serial.print(millis()); Serial.print(',');
  Serial.print(++scan_no); Serial.print(',');
  Serial.print(vdd, 4); Serial.print(',');
  print_r(rc); Serial.print(',');
  print_r(ra); Serial.print(',');
  print_r(rl); Serial.print(',');
  print_r(chk.r); Serial.print(',');
  Serial.print(k, 5); Serial.print(',');
  Serial.print((int)zone_c.stable); Serial.print(',');
  Serial.print((int)zone_a.stable); Serial.print(',');
  Serial.print(zl::state_name(state)); Serial.print(',');
  Serial.println(flags);
}

void setup() {
  release_all();
  for (uint8_t p : {cfg::PIN_LED_G, cfg::PIN_LED_Y, cfg::PIN_LED_R}) {
    pinMode(p, OUTPUT);
    digitalWrite(p, LOW);
  }
  Serial.begin(115200);
  const uint32_t t0 = millis();
  while (!Serial && millis() - t0 < 3000) delay(10);   // wait briefly for the USB serial port
  Wire.begin(cfg::PIN_SDA, cfg::PIN_SCL);
  Wire.setClock(100000);
  adc_present = adc.begin(Wire, cfg::ADS_ADDR);
  Serial.printf("# %s | Rref %.0f | Rcheck %.0f | Rprot %.0f | wet<%.0f dry>%.0f persist %u | loop max %.0f | ADS1115 %s\n",
                cfg::FW_VERSION, cfg::R_REF, cfg::R_CHECK, cfg::R_PROT, cfg::WET_OHM, cfg::DRY_OHM, cfg::PERSIST,
                cfg::LOOP_MAX_OHM, adc_present ? "found" : "NOT FOUND");
  Serial.println(CSV_HEADER);
}

void loop() {
  const uint32_t now = millis();
  if (now - last_scan >= cfg::SCAN_PERIOD_MS || scan_no == 0) {
    last_scan = now;
    scan();
  }
  if (now - last_blink >= 500) {
    last_blink = now;
    blink_on = !blink_on;
  }
  set_leds();
  delay(5);
}
