"""
scanet — Unit Tests for OS Detection & Fingerprinting Engine
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../backend"))

from analyzers.os_fingerprint import OSFingerprintEngine


def test_ttl_linux_deduction():
    # Target observed with TTL 54 (initial 64 minus 10 hops)
    res = OSFingerprintEngine.deduce_os_from_ttl(54)
    assert "Linux" in res["family"]
    assert res["estimated_initial_ttl"] == 64
    assert res["estimated_network_hops"] == 10
    assert res["confidence"] >= 80


def test_ttl_windows_deduction():
    # Target observed with TTL 118 (initial 128 minus 10 hops)
    res = OSFingerprintEngine.deduce_os_from_ttl(118)
    assert res["family"] == "Windows"
    assert res["estimated_initial_ttl"] == 128
    assert res["estimated_network_hops"] == 10
    assert res["confidence"] >= 85


def test_ttl_cisco_network_deduction():
    # Target observed with TTL 248 (initial 255)
    res = OSFingerprintEngine.deduce_os_from_ttl(248)
    assert "Network" in res["family"]
    assert res["estimated_initial_ttl"] == 255


def test_ssh_banner_deduction():
    # Ubuntu SSH banner
    banner = "SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.1"
    res = OSFingerprintEngine.deduce_os_from_banners([banner])
    assert res is not None
    assert res["family"] == "Linux"
    assert "Ubuntu" in res["name"]
    assert res["confidence"] == 95


def test_http_iis_banner_deduction():
    # Microsoft IIS banner
    banner = "Microsoft-IIS/10.0"
    res = OSFingerprintEngine.deduce_os_from_banners([banner])
    assert res is not None
    assert res["family"] == "Windows"
    assert "IIS" in res["name"]


def test_port_profile_windows():
    # Characteristic Windows ports: 135, 445, 3389
    res = OSFingerprintEngine.deduce_os_from_ports([80, 135, 445, 3389])
    assert res["family"] == "Windows"
    assert 445 in res["indicative_ports"]


def test_composite_fingerprinting():
    # Composite case: TTL 54 + Ubuntu banner
    result = OSFingerprintEngine.fingerprint_target(
        ttl=54,
        banners=["SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.1"],
        open_ports=[22, 80]
    )
    assert result["os_family"] == "Linux"
    assert "Ubuntu" in result["os_name"]
    assert result["confidence_percent"] >= 95
