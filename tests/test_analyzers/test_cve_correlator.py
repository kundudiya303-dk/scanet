"""
scanet — Unit Tests for CVE & CISA KEV Correlator
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../backend"))

from analyzers.cve_correlator import correlate_service_cves


def test_correlate_openssh_regresshion():
    matches = correlate_service_cves("OpenSSH", "8.9p1")
    assert len(matches) > 0
    cve_ids = [m["cve_id"] for m in matches]
    assert "CVE-2024-6387" in cve_ids


def test_correlate_apache_path_traversal():
    matches = correlate_service_cves("Apache", "2.4.49")
    assert len(matches) > 0
    assert any("CVE-2021-41773" == m["cve_id"] for m in matches)


def test_correlate_unknown_service():
    matches = correlate_service_cves("custom_internal_daemon", "1.0.0")
    assert len(matches) == 0
