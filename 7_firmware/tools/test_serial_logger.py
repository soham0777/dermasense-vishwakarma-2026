"""
Test serial_logger.py through pyserial's loop:// port (what is written is read back), plus the header contract
with the firmware source. The lines below imitate the firmware format; they are test strings, not measurements.
Run: python -m pytest test_serial_logger.py -q
"""
import csv
import re
import shutil
import sys
import tempfile
from pathlib import Path

import serial

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import serial_logger as sl  # noqa: E402

LINES = [
    "# reader_v0_1 | Rref 100000 | ... | ADS1115 found",
    sl.EXPECTED_HEADER,
    "2003,1,3.2981,8123,inf,9050,100210,0.99790,0,0,OK,",
    "4005,2,3.2979,7990,inf,9011,100190,0.99810,0,0,OK,",
    "6011,3,3.2980,8010,85000,9030,100200,0.99800,1,1,CHANGE,",
    "8013,4,3.2980,garbage,,,",                                        # corrupted line
    "10015,5,nan,inf,inf,inf,inf,1.00000,0,0,FAULT,ADC;VDD;LOOP_OPEN;",
]


def test_loopback_logging():
    d = Path(tempfile.mkdtemp(prefix="logger_"))
    try:
        port = serial.serial_for_url("loop://", timeout=0.2)
        port.write(("\n".join(LINES) + "\n").encode())
        stats = sl.run(port, d / "run.csv", max_lines=len(LINES), echo=False)
        port.close()
        assert stats == {"rows": 4, "bad": 1, "meta": 1, "header_ok": True}, stats
        rows = list(csv.DictReader(open(d / "run.csv", encoding="utf-8")))
        assert [r["state"] for r in rows] == ["OK", "OK", "CHANGE", "FAULT"]
        assert rows[0]["ra_ohm"] == "inf" and float(rows[0]["ra_ohm"]) == float("inf")
        assert rows[3]["flags"] == "ADC;VDD;LOOP_OPEN;"
        assert all(r["pc_time"] for r in rows)
        assert "garbage" in (d / "run.bad.txt").read_text()
        assert "ADS1115 found" in (d / "run.meta.txt").read_text()
    finally:
        shutil.rmtree(d, ignore_errors=True)


def test_header_mismatch_detected():
    d = Path(tempfile.mkdtemp(prefix="logger_"))
    try:
        port = serial.serial_for_url("loop://", timeout=0.2)
        port.write(b"ms,scan,vdd_V,rc_ohm\n")
        stats = sl.run(port, d / "run.csv", max_lines=1, echo=False)
        assert stats["header_ok"] is False
    finally:
        shutil.rmtree(d, ignore_errors=True)


def test_header_matches_firmware_source():
    ino = (HERE.parent / "reader_v0_1" / "reader_v0_1.ino").read_text(encoding="utf-8")
    m = re.search(r'CSV_HEADER\s*=\s*\n?\s*"([^"]+)"', ino)
    assert m and m.group(1) == sl.EXPECTED_HEADER


def test_firmware_state_names_match():
    zl = (HERE.parent / "reader_v0_1" / "zone_logic.h").read_text(encoding="utf-8")
    names = set(re.findall(r'"(OK|CHANGE|CHECK|FAULT)"', zl))
    assert names == sl.STATES
