"""
scanet — Unit Tests for AI Security Advisor & MITRE ATT&CK Copilot
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../backend"))

from analyzers.ai_advisor import AISecurityAdvisor


def test_ai_advisor_port_exposure():
    advisor = AISecurityAdvisor()
    sample_scan = {
        "ports": [
            {"port_number": 6379, "service_name": "redis"},
            {"port_number": 21, "service_name": "ftp"}
        ],
        "header_grade": "F"
    }

    result = advisor.analyze_findings(sample_scan)
    assert result["hygiene_score"] < 70
    assert result["critical_count"] >= 1
    assert "T1040 - Network Sniffing" in result["mitre_techniques"]
    assert any("Redis" in a["title"] for a in result["advisories"])


def test_ai_advisor_clean_target():
    advisor = AISecurityAdvisor()
    sample_scan = {
        "ports": [
            {"port_number": 443, "service_name": "https"}
        ],
        "header_grade": "A"
    }

    result = advisor.analyze_findings(sample_scan)
    assert result["hygiene_score"] == 100
    assert result["critical_count"] == 0
    assert result["grade"] == "A"
