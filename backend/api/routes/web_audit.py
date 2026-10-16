"""
scanet — Web Security & Misconfiguration API Routes
Endpoints for running Nikto/OWASP ZAP style web audits and subdomain takeover checks.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

from analyzers.web_auditor import run_full_web_audit, SENSITIVE_PATHS
from analyzers.subdomain_takeover import check_subdomain_takeover, check_dns_zone_transfer, TAKEOVER_SIGNATURES
from engine.scope_validator import ScopeValidator

router = APIRouter()


class WebAuditRequest(BaseModel):
    target_url: str = Field(..., example="http://example.com")


class TakeoverRequest(BaseModel):
    domain: str = Field(..., example="sub.example.com")
    cname: Optional[str] = Field(None, example="example.github.io")


class ZoneTransferRequest(BaseModel):
    domain: str = Field(..., example="example.com")
    nameserver: Optional[str] = Field(None, example="ns1.example.com")


@router.post("/scan")
async def scan_web_security(req: WebAuditRequest):
    """
    Run comprehensive web security and misconfiguration audit on target URL.
    Checks HTTP methods, sensitive file leaks, cookies, and CORS policies.
    """
    # Scope validation (allows loopback for local testing of web services)
    is_valid, reason = ScopeValidator.validate(req.target_url, allow_loopback=True)
    if not is_valid:
        raise HTTPException(status_code=400, detail=f"Target rejected by Scope Guard: {reason}")

    try:
        results = run_full_web_audit(req.target_url)
        return {
            "success": True,
            "data": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Web audit execution failed: {str(e)}")


@router.post("/takeover")
async def check_takeover(req: TakeoverRequest):
    """
    Check if a subdomain has a dangling CNAME record vulnerable to takeover.
    """
    is_valid, reason = ScopeValidator.validate(req.domain)
    if not is_valid:
        raise HTTPException(status_code=400, detail=f"Target rejected by Scope Guard: {reason}")

    try:
        result = check_subdomain_takeover(req.domain, req.cname)
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Takeover check failed: {str(e)}")


@router.post("/zone-transfer")
async def check_axfr(req: ZoneTransferRequest):
    """
    Check if a target nameserver permits unauthorized DNS AXFR zone transfers.
    """
    is_valid, reason = ScopeValidator.validate(req.domain)
    if not is_valid:
        raise HTTPException(status_code=400, detail=f"Target rejected by Scope Guard: {reason}")

    try:
        result = check_dns_zone_transfer(req.domain, req.nameserver)
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Zone transfer check failed: {str(e)}")


@router.get("/rules")
async def get_audit_rules():
    """
    Return all active audit rules, probed sensitive paths, and cloud takeover signatures.
    """
    return {
        "sensitive_paths": [
            {"path": p["path"], "name": p["name"], "severity": p["severity"], "risk": p["risk"]}
            for p in SENSITIVE_PATHS
        ],
        "takeover_providers": [
            {"provider": s["provider"], "severity": s["severity"], "domains": s["cname_regex"]}
            for s in TAKEOVER_SIGNATURES
        ],
        "methods_audited": ["OPTIONS", "TRACE", "PUT", "DELETE", "GET", "POST", "HEAD"]
    }
