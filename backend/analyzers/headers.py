"""
scanet — HTTP Security Header Analyzer
Inspects HTTP response headers and grades security posture A+ to F.
Zero external tool dependency — uses Python httpx directly.
"""
try:
    import httpx
except ImportError:
    httpx = None

from typing import Optional


SECURITY_HEADERS = {
    "strict-transport-security": {
        "description": "HTTP Strict Transport Security (HSTS)",
        "severity":    "high",
        "remediation": "Add: Strict-Transport-Security: max-age=31536000; includeSubDomains",
    },
    "content-security-policy": {
        "description": "Content Security Policy (CSP)",
        "severity":    "high",
        "remediation": "Define a strict CSP policy preventing XSS and injection attacks.",
    },
    "x-frame-options": {
        "description": "Clickjacking Protection (X-Frame-Options)",
        "severity":    "medium",
        "remediation": "Add: X-Frame-Options: DENY or SAMEORIGIN",
    },
    "x-content-type-options": {
        "description": "MIME-Sniffing Protection",
        "severity":    "low",
        "remediation": "Add: X-Content-Type-Options: nosniff",
    },
    "referrer-policy": {
        "description": "Referrer Policy",
        "severity":    "low",
        "remediation": "Add: Referrer-Policy: strict-origin-when-cross-origin",
    },
    "permissions-policy": {
        "description": "Permissions Policy (Feature Policy)",
        "severity":    "low",
        "remediation": "Define Permissions-Policy to restrict browser features.",
    },
}


def grade_from_score(score: int, max_score: int) -> str:
    """Convert a numeric score to an A+, A, B, C, D, F letter grade."""
    ratio = score / max_score if max_score > 0 else 0
    if ratio >= 0.95: return "A+"
    if ratio >= 0.85: return "A"
    if ratio >= 0.70: return "B"
    if ratio >= 0.55: return "C"
    if ratio >= 0.40: return "D"
    return "F"


async def analyze_headers(url: str, timeout: int = 10) -> dict:
    """
    Fetches HTTP headers for the given URL and grades security posture.
    Returns a structured report with grade, findings, and remediations.
    """
    result = {
        "url":      url,
        "grade":    "F",
        "score":    0,
        "max_score": len(SECURITY_HEADERS),
        "present_headers":  [],
        "missing_headers":  [],
        "server_info":      {},
        "error": None,
    }
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=timeout, verify=False) as client:
            response = await client.head(url)
            headers = {k.lower(): v for k, v in response.headers.items()}

            result["server_info"] = {
                "server":        headers.get("server", "Not disclosed"),
                "x-powered-by":  headers.get("x-powered-by", "Not disclosed"),
                "status_code":   response.status_code,
                "final_url":     str(response.url),
            }

            score = 0
            for header_name, meta in SECURITY_HEADERS.items():
                if header_name in headers:
                    score += 1
                    result["present_headers"].append({
                        "header":      header_name,
                        "value":       headers[header_name],
                        "description": meta["description"],
                    })
                else:
                    result["missing_headers"].append({
                        "header":      header_name,
                        "description": meta["description"],
                        "severity":    meta["severity"],
                        "remediation": meta["remediation"],
                    })

            result["score"] = score
            result["grade"] = grade_from_score(score, len(SECURITY_HEADERS))

    except Exception as e:
        result["error"] = str(e)

    return result
