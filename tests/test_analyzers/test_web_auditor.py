"""
Tests for web_auditor analyzer module.
"""
from analyzers.web_auditor import (
    check_cookie_security,
    check_cors_policy,
    calculate_web_security_grade,
    SENSITIVE_PATHS
)
import re


def test_cookie_security_detection():
    # Headers with insecure cookies
    headers = {
        "Set-Cookie": "session_id=abc123xyz; Path=/; Domain=example.com"
    }
    result = check_cookie_security(headers)
    assert len(result["cookies"]) == 1
    assert result["cookies"][0]["http_only"] is False
    assert result["cookies"][0]["secure"] is False
    assert len(result["findings"]) >= 2

    # Headers with fully secure cookies
    secure_headers = {
        "Set-Cookie": "auth_token=tok456; Path=/; Secure; HttpOnly; SameSite=Strict"
    }
    secure_result = check_cookie_security(secure_headers)
    assert secure_result["cookies"][0]["http_only"] is True
    assert secure_result["cookies"][0]["secure"] is True
    assert secure_result["cookies"][0]["same_site"] == "Strict"
    assert len(secure_result["findings"]) == 0


def test_cors_misconfiguration_detection():
    # Wildcard with credentials
    vulnerable_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Credentials": "true"
    }
    cors_res = check_cors_policy("http://mock.local", vulnerable_headers)
    assert cors_res["is_misconfigured"] is True
    assert len(cors_res["findings"]) >= 1
    assert any("CORS" in f["title"] for f in cors_res["findings"])

    # Strict CORS
    safe_headers = {
        "Access-Control-Allow-Origin": "https://trusted.example.com",
        "Access-Control-Allow-Credentials": "true"
    }
    safe_res = check_cors_policy("http://mock.local", safe_headers)
    assert safe_res["is_misconfigured"] is False


def test_web_security_grade_calculation():
    # Clean finding set -> Grade A+
    clean_grade = calculate_web_security_grade([])
    assert clean_grade["score"] == 100
    assert clean_grade["grade"] == "A+"
    assert clean_grade["rating"] == "EXCELLENT"

    # Moderate findings
    mod_findings = [
        {"severity": "MEDIUM", "title": "Missing HttpOnly"},
        {"severity": "LOW", "title": "Missing Referrer-Policy"}
    ]
    mod_grade = calculate_web_security_grade(mod_findings)
    assert mod_grade["score"] == 89
    assert mod_grade["grade"] == "A"

    # Severe findings -> Grade F
    severe_findings = [
        {"severity": "CRITICAL", "title": "Exposed .env credentials"},
        {"severity": "CRITICAL", "title": "Exposed .git repo"},
        {"severity": "CRITICAL", "title": "Exposed database dump"},
        {"severity": "HIGH", "title": "CORS arbitrary reflection"}
    ]
    severe_grade = calculate_web_security_grade(severe_findings)
    assert severe_grade["score"] <= 20
    assert severe_grade["grade"] == "F"
    assert severe_grade["rating"] == "CRITICAL RISK"


def test_sensitive_endpoints_definitions():
    paths = [item["path"] for item in SENSITIVE_PATHS]
    assert "/.env" in paths
    assert "/.git/HEAD" in paths
    assert "/robots.txt" in paths
    assert "/sitemap.xml" in paths
    assert "/phpinfo.php" in paths
    assert "/backup.sql" in paths

    # Verify regex matches test body
    env_rule = next(r for r in SENSITIVE_PATHS if r["path"] == "/.env")
    sample_env = "APP_NAME=Scanet\nDB_PASSWORD=secret_password123\nPORT=8000"
    assert bool(re.search(env_rule["pattern"], sample_env, re.IGNORECASE)) is True
