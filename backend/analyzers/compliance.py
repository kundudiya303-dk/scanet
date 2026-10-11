"""
scanet — Compliance & Governance Framework Mapper
Maps discovered findings, exposed ports, and missing headers to:
- OWASP Top 10 (2021)
- CIS Critical Security Controls v8
- NIST Cybersecurity Framework (CSF 2.0)
"""
from typing import Dict, Any, List


COMPLIANCE_MAPPINGS = {
    "A01:2021-Broken Access Control": {
        "framework": "OWASP Top 10",
        "description": "Restrictions on what authenticated users can do are not properly enforced.",
        "checks": ["exposed_admin_paths", "directory_listing", "unauth_redis"]
    },
    "A02:2021-Cryptographic Failures": {
        "framework": "OWASP Top 10",
        "description": "Sensitive data transmitted over cleartext HTTP, outdated TLS, or weak cipher suites.",
        "checks": ["missing_hsts", "cleartext_http", "tls_1_0_detected", "expiring_cert"]
    },
    "A05:2021-Security Misconfiguration": {
        "framework": "OWASP Top 10",
        "description": "Default configurations, unpatched flaws, verbose error pages, or missing security headers.",
        "checks": ["missing_csp", "missing_xfo", "default_banner", "debug_endpoints"]
    },
    "CIS-Control-04: Secure Configuration of Enterprise Assets and Software": {
        "framework": "CIS Controls v8",
        "description": "Establish and maintain the secure configuration of enterprise assets and software.",
        "checks": ["hardened_services", "unnecessary_ports_closed", "service_versioning"]
    },
    "CIS-Control-07: Continuous Vulnerability Management": {
        "framework": "CIS Controls v8",
        "description": "Develop a plan to continuously assess and track vulnerabilities on all enterprise assets.",
        "checks": ["cve_detection", "automated_scans", "patch_verification"]
    },
    "NIST-PR.IP-01: Baseline Configuration": {
        "framework": "NIST CSF",
        "description": "A baseline configuration of information technology and other systems is created and maintained.",
        "checks": ["scan_diff_verification", "scope_enforcement"]
    }
}


def map_findings_to_compliance(findings: List[Dict[str, Any]], header_grade: str = "A") -> Dict[str, Any]:
    """
    Evaluates findings and returns a structured compliance audit matrix.
    """
    compliance_report = {
        "owasp_top_10": [],
        "cis_controls": [],
        "nist_csf": []
    }

    # Evaluate Header Grade
    if header_grade in ["D", "F"]:
        compliance_report["owasp_top_10"].append({
            "category": "A05:2021-Security Misconfiguration",
            "status": "NON_COMPLIANT",
            "evidence": f"Missing critical browser defense headers (Grade {header_grade})"
        })
        compliance_report["owasp_top_10"].append({
            "category": "A02:2021-Cryptographic Failures",
            "status": "ATTENTION_REQUIRED",
            "evidence": "Strict-Transport-Security (HSTS) header is missing or unverified."
        })

    # Evaluate Port & CVE Findings
    for f in findings:
        severity = f.get("severity", "LOW")
        name = f.get("name", "")
        if severity in ["HIGH", "CRITICAL"]:
            compliance_report["cis_controls"].append({
                "control": "CIS-Control-07: Continuous Vulnerability Management",
                "status": "FAILED",
                "evidence": f"High risk finding: {name} requires remediation."
            })

    return compliance_report
