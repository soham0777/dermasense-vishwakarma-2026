"""
Log the reader's CSV stream from USB serial to a file, adding the PC time to every row.

Checks every line: the header must match EXPECTED_HEADER (the same string as CSV_HEADER in reader_v0_1.ino),
and every row must have the right number of fields with numbers where numbers belong. Bad lines are counted and
kept in a separate file, never silently dropped or "fixed". Lines starting with '#' (firmware info) go to the
.meta.txt file.
Usage:  python serial_logger.py --port COM5 [--minutes 30] [--out ../../04_lig_lab/e4/run1.csv]
        python serial_logger.py --list            (show serial ports)
"""
import argparse
import datetime as dt
import sys
import time
from pathlib import Path

EXPECTED_HEADER = "ms,scan,vdd_V,rc_ohm,ra_ohm,rloop_ohm,rcheck_ohm,k_check,c_wet,a_wet,state,flags"
NUMERIC = ("ms", "scan", "vdd_V", "rc_ohm", "ra_ohm", "rloop_ohm", "rcheck_ohm", "k_check", "c_wet", "a_wet")
STATES = {"OK", "CHANGE", "CHECK", "FAULT"}


def check_row(line):
    """Return the list of fields if the row is valid, else None."""
    f = line.split(",")
    cols = EXPECTED_HEADER.split(",")
    if len(f) != len(cols):
        return None
    row = dict(zip(cols, f))
    try:
        for c in NUMERIC:
            float(row[c])          # 'inf' is valid (open circuit)
    except ValueError:
        return None
    return f if row["state"] in STATES else None


def run(ser, out_path, duration_s=None, max_lines=None, echo=True):
    """Read from any object with readline() (a pyserial port, or loop:// in the tests)."""
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    stats = {"rows": 0, "bad": 0, "meta": 0, "header_ok": None}
    t_end = time.time() + duration_s if duration_s else None
    seen = 0
    with open(out_path, "w", newline="", encoding="utf-8") as fo, \
            open(out_path.with_suffix(".bad.txt"), "w", encoding="utf-8") as fb, \
            open(out_path.with_suffix(".meta.txt"), "w", encoding="utf-8") as fm:
        fo.write("pc_time," + EXPECTED_HEADER + "\n")
        while (t_end is None or time.time() < t_end) and (max_lines is None or seen < max_lines):
            raw = ser.readline()
            if not raw:
                if max_lines is not None and t_end is None:
                    break                          # test mode: nothing more to read
                continue
            seen += 1
            line = raw.decode("utf-8", errors="replace").strip()
            now = dt.datetime.now().isoformat(timespec="milliseconds")
            if not line:
                continue
            if line.startswith("#"):
                fm.write(f"{now} {line}\n")
                stats["meta"] += 1
            elif line.startswith("ms,"):
                stats["header_ok"] = line == EXPECTED_HEADER
                if not stats["header_ok"]:
                    fb.write(f"{now} HEADER MISMATCH: {line}\n")
            elif check_row(line) is not None:
                fo.write(f"{now},{line}\n")
                fo.flush()
                stats["rows"] += 1
                if echo:
                    print(line)
            else:
                fb.write(f"{now} {line}\n")
                stats["bad"] += 1
    return stats


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--port", help="COM port (e.g. COM5) or a pyserial URL")
    ap.add_argument("--baud", type=int, default=115200)
    ap.add_argument("--minutes", type=float, default=None, help="stop after this many minutes (default: Ctrl+C)")
    ap.add_argument("--out", default=None, help="output CSV (default: logs/reader_<date_time>.csv)")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    import serial
    import serial.tools.list_ports
    if a.list or not a.port:
        for p in serial.tools.list_ports.comports():
            print(p.device, "-", p.description)
        return
    out = a.out or Path(__file__).resolve().parent / "logs" / f"reader_{dt.datetime.now():%Y%m%d_%H%M%S}.csv"
    ser = serial.serial_for_url(a.port, a.baud, timeout=1)
    try:
        stats = run(ser, out, duration_s=a.minutes * 60 if a.minutes else None)
    except KeyboardInterrupt:
        stats = "stopped by user"
    finally:
        ser.close()
    print(f"saved {out}: {stats}")
    if isinstance(stats, dict) and stats["header_ok"] is False:
        sys.exit("Header mismatch: firmware and logger versions differ.")


if __name__ == "__main__":
    main()
