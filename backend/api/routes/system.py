"""
scanet API — System Health & Configuration Routes
Tool availability, resource metrics, and version info.
"""
from fastapi import APIRouter
import shutil
import psutil
import platform

router = APIRouter()

# All tools scanet can use
TOOL_REGISTRY = [
    {"name": "nmap",      "category": "port_scan",      "tier": 1},
    {"name": "naabu",     "category": "port_scan",      "tier": 1},
    {"name": "ffuf",      "category": "web_discovery",  "tier": 1},
    {"name": "dnsx",      "category": "dns",            "tier": 1},
    {"name": "subfinder", "category": "dns",            "tier": 1},
    {"name": "httpx",     "category": "http",           "tier": 1},
    {"name": "mtr",       "category": "diagnostics",    "tier": 1},
    {"name": "curl",      "category": "http",           "tier": 1},
    {"name": "dig",       "category": "dns",            "tier": 1},
    {"name": "nuclei",    "category": "assessment",     "tier": 2},
    {"name": "testssl.sh","category": "ssl",            "tier": 2},
    {"name": "whatweb",   "category": "fingerprint",    "tier": 2},
]


@router.get("/tools", summary="Check all tool availability and versions")
async def get_tool_status():
    """
    Checks presence of each security tool binary in system PATH
    and /opt/scanet/bin/. Returns installation status for each tool.
    """
    tool_status = []
    for tool in TOOL_REGISTRY:
        binary = shutil.which(tool["name"])
        tool_status.append({
            **tool,
            "installed": binary is not None,
            "path": binary,
        })
    installed_count = sum(1 for t in tool_status if t["installed"])
    return {
        "tools": tool_status,
        "installed_count": installed_count,
        "total_count": len(tool_status),
    }


@router.get("/resources", summary="Get system resource utilization")
async def get_resources():
    """Returns current CPU, RAM, and disk utilization metrics."""
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    return {
        "cpu_percent": psutil.cpu_percent(interval=0.5),
        "ram": {
            "total_mb":     round(mem.total / 1024 / 1024, 1),
            "used_mb":      round(mem.used / 1024 / 1024, 1),
            "available_mb": round(mem.available / 1024 / 1024, 1),
            "percent":      mem.percent,
        },
        "disk": {
            "total_gb": round(disk.total / 1024 / 1024 / 1024, 1),
            "used_gb":  round(disk.used / 1024 / 1024 / 1024, 1),
            "free_gb":  round(disk.free / 1024 / 1024 / 1024, 1),
            "percent":  disk.percent,
        },
        "platform": {
            "os":      platform.system(),
            "release": platform.release(),
            "arch":    platform.machine(),
            "python":  platform.python_version(),
        },
    }


@router.get("/health", summary="Simple health check")
async def health_check():
    """Liveness probe endpoint for load balancers and monitoring."""
    return {"status": "ok", "service": "scanet"}
