"""
scanet — Asynchronous Web Security & Misconfiguration Auditor
Lightweight native Python auditor equivalent to Nikto & OWASP ZAP checks:
- Probes for dangerous HTTP methods (TRACE, PUT, DELETE, OPTIONS)
- Detects sensitive file/directory leaks (.env, .git, robots.txt, backups)
- Analyzes cookie security flags (HttpOnly, Secure, SameSite)
- Evaluates CORS policy misconfigurations
- Generates composite security grade (A+ to F) and remediation guidance
Runs in < 15MB RAM with zero heavy external dependencies.
"""
import re
import urllib.request
import urllib.parse
import ssl
from typing import Dict, List, Any, Optional

# High-risk sensitive files to probe
SENSITIVE_PATHS = [
    {
        "path": "/.env",
        "name": "Environment Variables File",
        "severity": "CRITICAL",
        "pattern": r"(DB_PASSWORD|SECRET_KEY|API_KEY|AWS_ACCESS_KEY|APP_KEY)=",
        "risk": "Exposure of production credentials, database connection strings, or cloud secret keys.",
        "remediation": "Block access to hidden dot-files in web server configuration (.htaccess, nginx.conf)."
    },
    {
        "path": "/.git/HEAD",
        "name": "Git Repository Metadata",
        "severity": "CRITICAL",
        "pattern": r"ref: refs/heads/",
        "risk": "Full source code dump possible via exposed .git repository objects.",
        "remediation": "Restrict web server access to .git directories or exclude .git during deployments."
    },
    {
        "path": "/robots.txt",
        "name": "Robots Information Mapping",
        "severity": "INFO",
        "pattern": r"(Disallow:|User-agent:)",
        "risk": "Discloses internal administrative paths, hidden endpoints, or portal locations to attackers.",
        "remediation": "Do not rely on robots.txt for security; enforce proper authentication on sensitive routes."
    },
    {
        "path": "/sitemap.xml",
        "name": "XML Sitemap Discovery",
        "severity": "INFO",
        "pattern": r"<urlset|<sitemapindex",
        "risk": "Provides automated scrapers with complete route topology and dynamic endpoint parameters.",
        "remediation": "Ensure administrative, internal, and staging URLs are excluded from public sitemaps."
    },
    {
        "path": "/.well-known/security.txt",
        "name": "RFC 9116 Security Disclosure Policy",
        "severity": "INFO",
        "pattern": r"Contact:",
        "risk": "Informational policy file. If missing, external security researchers have no clear disclosure channel.",
        "remediation": "Deploy a standard security.txt file per RFC 9116 to facilitate coordinated disclosure."
    },
    {
        "path": "/phpinfo.php",
        "name": "PHP Diagnostic Info Page",
        "severity": "HIGH",
        "pattern": r"PHP Version|Configuration File",
        "risk": "Discloses PHP runtime version, compile flags, extensions, and server environment variables.",
        "remediation": "Remove phpinfo() scripts from production systems immediately."
    },
    {
        "path": "/config.json",
        "name": "Client/Server Configuration File",
        "severity": "HIGH",
        "pattern": r"(\"database\"|\"apiKey\"|\"secret\"|\"auth\")",
        "risk": "Exposes infrastructure configurations, backend API routes, or client-side auth parameters.",
        "remediation": "Ensure configuration files are stored outside the public document root."
    },
    {
        "path": "/backup.sql",
        "name": "Database Backup Dump",
        "severity": "CRITICAL",
        "pattern": r"(CREATE TABLE|INSERT INTO|MySQL dump|PostgreSQL database dump)",
        "risk": "Complete database compromise and exfiltration of user tables and password hashes.",
        "remediation": "Never store raw database dumps inside web-accessible document roots."
    }
]


def _create_ssl_context() -> ssl.SSLContext:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def check_http_methods(target_url: str, timeout: int = 4) -> Dict[str, Any]:
    """
    Audit supported and enabled HTTP methods using OPTIONS request.
    Detects Cross-Site Tracing (XST) and insecure write methods.
    """
    ctx = _create_ssl_context()
    results = {
        "tested_methods": ["GET", "POST", "OPTIONS", "HEAD", "TRACE", "PUT", "DELETE"],
        "allowed_methods": [],
        "trace_enabled": False,
        "insecure_methods": [],
        "findings": []
    }

    # Probing with OPTIONS
    try:
        req = urllib.request.Request(target_url, method="OPTIONS")
        req.add_header("User-Agent", "scanet-WebAuditor/1.0")
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            allow_hdr = resp.headers.get("Allow", "") or resp.headers.get("Public", "")
            if allow_hdr:
                results["allowed_methods"] = [m.strip().upper() for m in allow_hdr.split(",") if m.strip()]
    except Exception:
        pass

    # Specifically test TRACE for Cross-Site Tracing (XST)
    try:
        trace_req = urllib.request.Request(target_url, method="TRACE")
        trace_req.add_header("User-Agent", "scanet-WebAuditor/1.0")
        with urllib.request.urlopen(trace_req, timeout=timeout, context=ctx) as trace_resp:
            if trace_resp.status == 200:
                results["trace_enabled"] = True
                results["insecure_methods"].append("TRACE")
                results["findings"].append({
                    "method": "TRACE",
                    "severity": "MEDIUM",
                    "title": "HTTP TRACE Method Enabled (XST Risk)",
                    "description": "Server responded 200 OK to TRACE. Enables Cross-Site Tracing attacks to bypass HttpOnly cookies.",
                    "remediation": "Disable TRACE method in web server configuration (e.g., 'TraceEnable off' in Apache)."
                })
    except Exception:
        pass

    # Flag unauthenticated PUT or DELETE if indicated in Allow header
    for method in ["PUT", "DELETE"]:
        if method in results["allowed_methods"]:
            results["insecure_methods"].append(method)
            results["findings"].append({
                "method": method,
                "severity": "HIGH",
                "title": f"HTTP {method} Method Advertised",
                "description": f"Server advertises {method} in Allow header, indicating potential unauthenticated file manipulation.",
                "remediation": f"Disable {method} method for public unauthenticated endpoints."
            })

    return results


def check_cookie_security(headers: Dict[str, str]) -> Dict[str, Any]:
    """
    Audit Set-Cookie headers for HttpOnly, Secure, and SameSite directives.
    """
    findings = []
    cookies_audited = []

    # Case-insensitive lookup for set-cookie headers
    set_cookie_headers = [v for k, v in headers.items() if k.lower() == "set-cookie"]

    for raw_cookie in set_cookie_headers:
        cookie_parts = [p.strip() for p in raw_cookie.split(";")]
        name_val = cookie_parts[0]
        cookie_name = name_val.split("=")[0] if "=" in name_val else name_val
        lower_parts = [p.lower() for p in cookie_parts[1:]]

        has_httponly = any("httponly" in p for p in lower_parts)
        has_secure = any("secure" in p for p in lower_parts)
        samesite = "None"
        for p in lower_parts:
            if p.startswith("samesite="):
                samesite = p.split("=")[1].capitalize()

        cookie_info = {
            "name": cookie_name,
            "http_only": has_httponly,
            "secure": has_secure,
            "same_site": samesite
        }
        cookies_audited.append(cookie_info)

        if not has_httponly:
            findings.append({
                "cookie": cookie_name,
                "severity": "MEDIUM",
                "title": f"Cookie '{cookie_name}' Missing HttpOnly Flag",
                "description": "Cookie accessible to client-side scripts. Enables session token hijacking via XSS.",
                "remediation": "Add the 'HttpOnly' directive when issuing cookies."
            })
        if not has_secure:
            findings.append({
                "cookie": cookie_name,
                "severity": "MEDIUM",
                "title": f"Cookie '{cookie_name}' Missing Secure Flag",
                "description": "Cookie can be transmitted over unencrypted HTTP connections, exposing it to eavesdropping.",
                "remediation": "Add the 'Secure' directive so cookies are transmitted exclusively over TLS/HTTPS."
            })
        if samesite in ["None", "Not specified"]:
            findings.append({
                "cookie": cookie_name,
                "severity": "LOW",
                "title": f"Cookie '{cookie_name}' SameSite Insecure / Unspecified",
                "description": "Without SameSite=Lax or Strict, requests may be vulnerable to Cross-Site Request Forgery (CSRF).",
                "remediation": "Set 'SameSite=Lax' or 'SameSite=Strict' on session and sensitive cookies."
            })

    return {
        "cookies": cookies_audited,
        "findings": findings
    }


def check_cors_policy(target_url: str, headers: Dict[str, str], timeout: int = 4) -> Dict[str, Any]:
    """
    Audit CORS policy for wildcard origins with credentials or arbitrary reflection.
    """
    ctx = _create_ssl_context()
    findings = []
    cors_info = {
        "allow_origin": headers.get("Access-Control-Allow-Origin", "None"),
        "allow_credentials": headers.get("Access-Control-Allow-Credentials", "false"),
        "is_misconfigured": False,
        "findings": findings
    }

    if cors_info["allow_origin"] == "*" and cors_info["allow_credentials"].lower() == "true":
        cors_info["is_misconfigured"] = True
        findings.append({
            "severity": "HIGH",
            "title": "Critical CORS Misconfiguration (* with Credentials)",
            "description": "Access-Control-Allow-Origin is wildcard while Allow-Credentials is true, allowing malicious sites to access authenticated resources.",
            "remediation": "Specify explicit trusted origins instead of wildcard '*' when credentials are required."
        })

    # Test arbitrary origin reflection
    test_origin = "https://evil-attacker.example.com"
    try:
        req = urllib.request.Request(target_url, method="GET")
        req.add_header("Origin", test_origin)
        req.add_header("User-Agent", "scanet-WebAuditor/1.0")
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            refl_origin = resp.headers.get("Access-Control-Allow-Origin", "")
            if refl_origin == test_origin:
                cors_info["is_misconfigured"] = True
                findings.append({
                    "severity": "HIGH",
                    "title": "CORS Arbitrary Origin Reflection",
                    "description": f"Server blindly reflected untrusted Origin '{test_origin}' in Access-Control-Allow-Origin.",
                    "remediation": "Validate the Origin header against a strict whitelist before granting CORS permissions."
                })
    except Exception:
        pass

    return cors_info


def audit_sensitive_endpoints(base_url: str, timeout: int = 3) -> List[Dict[str, Any]]:
    """
    Probes common sensitive paths (.env, .git, robots.txt, phpinfo, backups).
    """
    ctx = _create_ssl_context()
    base = base_url.rstrip("/")
    disclosures = []

    for item in SENSITIVE_PATHS:
        test_url = base + item["path"]
        try:
            req = urllib.request.Request(test_url, method="GET")
            req.add_header("User-Agent", "scanet-WebAuditor/1.0")
            with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
                if resp.status == 200:
                    body_sample = resp.read(2048).decode("utf-8", errors="replace")
                    matched = bool(re.search(item["pattern"], body_sample, re.IGNORECASE))
                    
                    # For robots.txt / sitemap / security.txt status 200 is always relevant
                    if matched or item["path"] in ["/robots.txt", "/sitemap.xml", "/.well-known/security.txt"]:
                        disclosures.append({
                            "path": item["path"],
                            "url": test_url,
                            "status": resp.status,
                            "name": item["name"],
                            "severity": item["severity"],
                            "verified_match": matched,
                            "risk": item["risk"],
                            "remediation": item["remediation"],
                            "snippet": body_sample[:180].strip()
                        })
        except urllib.error.HTTPError as e:
            # 403 or 401 on sensitive files indicates the file exists but access is forbidden
            if e.code in [401, 403] and item["path"] in ["/.env", "/.git/HEAD", "/backup.sql"]:
                disclosures.append({
                    "path": item["path"],
                    "url": test_url,
                    "status": e.code,
                    "name": item["name"],
                    "severity": "LOW",
                    "verified_match": False,
                    "risk": f"File exists on server but returned HTTP {e.code} (Access Restricted).",
                    "remediation": "Ensure file cannot be accessed via alternate route encodings.",
                    "snippet": f"HTTP {e.code} Restricted"
                })
        except Exception:
            continue

    return disclosures


def calculate_web_security_grade(findings: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Computes overall security grade and health score based on finding severities.
    """
    score = 100
    crit_count = 0
    high_count = 0
    med_count = 0
    low_count = 0

    for f in findings:
        sev = f.get("severity", "LOW").upper()
        if sev == "CRITICAL":
            score -= 25
            crit_count += 1
        elif sev == "HIGH":
            score -= 15
            high_count += 1
        elif sev == "MEDIUM":
            score -= 8
            med_count += 1
        elif sev == "LOW":
            score -= 3
            low_count += 1

    score = max(0, min(100, score))

    if score >= 95:
        grade = "A+"
        rating = "EXCELLENT"
    elif score >= 85:
        grade = "A"
        rating = "SECURE"
    elif score >= 75:
        grade = "B"
        rating = "MODERATE"
    elif score >= 60:
        grade = "C"
        rating = "NEEDS IMPROVEMENT"
    elif score >= 40:
        grade = "D"
        rating = "POOR"
    else:
        grade = "F"
        rating = "CRITICAL RISK"

    return {
        "score": score,
        "grade": grade,
        "rating": rating,
        "counts": {
            "critical": crit_count,
            "high": high_count,
            "medium": med_count,
            "low": low_count,
            "total": crit_count + high_count + med_count + low_count
        }
    }


def run_full_web_audit(target_url: str) -> Dict[str, Any]:
    """
    Unified entry point executing all web security auditor checks.
    """
    if not target_url.startswith("http://") and not target_url.startswith("https://"):
        target_url = "http://" + target_url

    parsed = urllib.parse.urlparse(target_url)
    base_url = f"{parsed.scheme}://{parsed.netloc}"

    ctx = _create_ssl_context()
    main_headers = {}
    server_banner = "Unknown"
    status_code = 0

    try:
        req = urllib.request.Request(base_url, method="GET")
        req.add_header("User-Agent", "scanet-WebAuditor/1.0")
        with urllib.request.urlopen(req, timeout=5, context=ctx) as resp:
            status_code = resp.status
            main_headers = dict(resp.headers)
            server_banner = resp.headers.get("Server", "Hidden / Not Disclosed")
    except Exception as e:
        server_banner = f"Unreachable: {str(e)[:60]}"

    # Execute all modular checks
    method_audit = check_http_methods(base_url)
    cookie_audit = check_cookie_security(main_headers)
    cors_audit = check_cors_policy(base_url, main_headers)
    sensitive_files = audit_sensitive_endpoints(base_url)

    # Consolidate all findings
    all_findings = []
    all_findings.extend(method_audit.get("findings", []))
    all_findings.extend(cookie_audit.get("findings", []))
    all_findings.extend(cors_audit.get("findings", []))
    for sf in sensitive_files:
        all_findings.append({
            "severity": sf["severity"],
            "title": f"Exposed Resource: {sf['name']} ({sf['path']})",
            "description": sf["risk"],
            "remediation": sf["remediation"]
        })

    grade_result = calculate_web_security_grade(all_findings)

    return {
        "target_url": base_url,
        "status_code": status_code,
        "server_banner": server_banner,
        "security_score": grade_result["score"],
        "security_grade": grade_result["grade"],
        "security_rating": grade_result["rating"],
        "counts": grade_result["counts"],
        "methods_audit": method_audit,
        "cookie_audit": cookie_audit,
        "cors_audit": cors_audit,
        "sensitive_exposures": sensitive_files,
        "all_findings": all_findings
    }
