"""
scanet API — Operating System Detection & Fingerprinting Routes
Provides unprivileged OS identification via TTL, banners, and port profiles.
"""
from fastapi import APIRouter, HTTPException
from analyzers.os_fingerprint import OSFingerprintEngine
from typing import Dict, Any, List, Optional

router = APIRouter()


@router.post("/fingerprint")
async def fingerprint_os(payload: dict):
    """
    Fingerprints target OS from available observables:
    - ttl: int (observed Time-To-Live)
    - banners: list[str] (HTTP, SSH, FTP banner strings)
    - open_ports: list[int] (detected open TCP ports)
    """
    ttl = payload.get("ttl")
    banners = payload.get("banners", [])
    open_ports = payload.get("open_ports", [])

    result = OSFingerprintEngine.fingerprint_target(
        ttl=ttl,
        banners=banners,
        open_ports=open_ports
    )
    return {
        "status": "success",
        "fingerprint": result
    }


@router.get("/signatures")
async def list_os_signatures():
    """
    Returns the supported operating system signature categories.
    """
    return {
        "total_signatures": len(OSFingerprintEngine.BANNER_SIGNATURES),
        "supported_families": ["Linux", "Windows", "BSD", "Cisco IOS", "RouterOS"],
        "ttl_heuristics": {
            "64": "Linux / Android / Unix",
            "128": "Microsoft Windows (10/11/Server)",
            "255": "Cisco IOS / Network Equipment / Solaris"
        }
    }
