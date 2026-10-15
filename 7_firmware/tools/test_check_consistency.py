"""
check_consistency.py must pass on the real files and must catch deliberately injected mistakes.
Run: python -m pytest test_check_consistency.py -q
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_consistency as cc  # noqa: E402


def real():
    nets, comps = cc.load_netlist()
    pins, nums, chans = cc.load_config()
    return nets, comps, pins, nums, chans


def test_real_design_is_consistent():
    assert cc.check(*real()) == []


def test_swapped_drive_pin_is_caught():
    nets, comps, pins, nums, chans = real()
    pins = dict(pins, PIN_DRV_C=pins["PIN_DRV_A"])
    assert any("PIN_DRV_C" in e for e in cc.check(nets, comps, pins, nums, chans))


def test_strapping_pin_is_caught():
    nets, comps, pins, nums, chans = real()
    pins = dict(pins, PIN_LED_G=8)
    assert any("not a usable" in e for e in cc.check(nets, comps, pins, nums, chans))


def test_wrong_reference_value_is_caught():
    nets, comps, pins, nums, chans = real()
    comps = dict(comps, R5="10k")
    assert any("R5" in e for e in cc.check(nets, comps, pins, nums, chans))


def test_wrong_adc_channel_is_caught():
    nets, comps, pins, nums, chans = real()
    chans = dict(chans, ADS_CH_NODE=2)
    assert any("ADS_CH_NODE" in e for e in cc.check(nets, comps, pins, nums, chans))


def test_missing_node_on_net_is_caught():
    nets, comps, pins, nums, chans = real()
    nets = dict(nets, N=nets["N"] - {("C1", "1")})
    assert any("net N" in e for e in cc.check(nets, comps, pins, nums, chans))
