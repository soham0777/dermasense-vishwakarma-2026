"""
Decode the reader's Bluetooth LE broadcast (layout in reader_v0_1/ble_beacon.h).

A phone scanner app (e.g. nRF Connect) shows the advertisement's manufacturer data as hex, for example
    0xFFFF44530101030302 2A00 9600
Paste it here to read the state:
    python decode_beacon.py FFFF44530101030302 2A009600
Used in bench test T11 (7_firmware/BENCH_TEST.md).
"""
import sys

STATES = ["OK", "CHANGE", "CHECK", "FAULT"]
FLAGS = ["C_WET", "A_WET", "ADC", "CHECK_R", "VDD", "LOOP_OPEN"]
R_OPEN = 0xFFFF


def decode(hex_text):
    raw = bytes.fromhex(hex_text.replace("0x", "").replace(" ", "").replace("-", ""))
    if len(raw) != 13:
        raise ValueError(f"expected 13 bytes, got {len(raw)}")
    if raw[0:2] != b"\xff\xff" or raw[2:4] != b"DS":
        raise ValueError("not a Dermasense payload (company ID 0xFFFF + 'DS' expected)")
    if raw[4] != 1:
        raise ValueError(f"unknown payload version {raw[4]}")
    if raw[5] >= len(STATES):
        raise ValueError(f"unknown state code {raw[5]}")

    def ohm(lo, hi):
        code = raw[lo] | raw[hi] << 8
        return None if code == R_OPEN else code * 100

    return {"state": STATES[raw[5]],
            "flags": [name for bit, name in enumerate(FLAGS) if raw[6] >> bit & 1],
            "scan": raw[7] | raw[8] << 8,
            "rc_ohm": ohm(9, 10),
            "ra_ohm": ohm(11, 12)}


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    d = decode("".join(argv[1:]))
    fmt = lambda r: "open" if r is None else f"{r:,} ohm"
    print(f"state {d['state']} | scan {d['scan']} | C {fmt(d['rc_ohm'])} | A {fmt(d['ra_ohm'])} | "
          f"flags {' '.join(d['flags']) or '-'}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
