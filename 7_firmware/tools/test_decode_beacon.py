"""The PC decoder must read the same bytes the firmware's compile-time test packs (zone_logic_tests.h change_pkt)."""
import pytest

from decode_beacon import decode

# bb::pack(State::Change, C_WET | A_WET, scan 0x10203, 4200 ohm, 15000 ohm)
CHANGE_PKT = "FF FF 44 53 01 01 03 03 02 2A 00 96 00"


def test_decodes_the_firmware_test_packet():
    d = decode(CHANGE_PKT)
    assert d == {"state": "CHANGE", "flags": ["C_WET", "A_WET"], "scan": 0x0203, "rc_ohm": 4200, "ra_ohm": 15000}


def test_open_zone_and_fault_flags():
    d = decode("0xFFFF 4453 01 03 20 0000 FFFF FFFF")
    assert d["state"] == "FAULT" and d["flags"] == ["LOOP_OPEN"] and d["rc_ohm"] is None and d["ra_ohm"] is None


@pytest.mark.parametrize("bad", ["FFFF44530101", "0000445301010303022A009600", "FFFF44530201030302 2A009600",
                                 "FFFF44530109030302 2A009600"])
def test_rejects_wrong_length_id_version_or_state(bad):
    with pytest.raises(ValueError):
        decode(bad)
