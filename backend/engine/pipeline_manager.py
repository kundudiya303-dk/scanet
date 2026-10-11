"""
scanet — Pipeline Orchestration Engine
Executes automated sequential multi-tool reconnaissance playbooks.
Chains tool outputs: e.g., Subdomain Discovery -> Port Screening -> Service Versioning -> Vulnerability Scan.
"""
from typing import List, Dict, Any, Callable
from engine.tool_registry import ToolRegistry


PIPELINE_PRESETS = {
    "full_recon": {
        "id": "full_recon",
        "name": "Full Attack Surface Reconnaissance",
        "description": "Comprehensive pipeline: Passive Subdomains -> Active DNS -> Fast Port Sweep -> Nmap Services -> HTTP Surface -> Nuclei Audit.",
        "stages": [
            {"tool": "subfinder", "params": {}},
            {"tool": "dnsx", "params": {}},
            {"tool": "naabu", "params": {"top_ports": 100}},
            {"tool": "nmap", "params": {"timing": 3, "service_version": True}},
            {"tool": "httpx", "params": {}},
            {"tool": "nuclei", "params": {"severity": "info,low,medium,high"}}
        ]
    },
    "web_security": {
        "id": "web_security",
        "name": "Web Application Security Audit",
        "description": "Web surface pipeline: Katana Crawler -> FFUF Path Discovery -> HTTPX TLS/Headers -> Nuclei Misconfiguration Check.",
        "stages": [
            {"tool": "katana", "params": {"depth": 2}},
            {"tool": "ffuf", "params": {"wordlist": "common.txt", "rate": 50}},
            {"tool": "httpx", "params": {}},
            {"tool": "nuclei", "params": {"tags": "misconfig,exposure"}}
        ]
    },
    "network_diagnostic": {
        "id": "network_diagnostic",
        "name": "Network Routing & Port Diagnostics",
        "description": "Network infrastructure pipeline: MTR Hop Analysis -> Naabu Port Screening -> Nmap OS & Service Audit.",
        "stages": [
            {"tool": "mtr", "params": {"report_cycles": 5}},
            {"tool": "naabu", "params": {"top_ports": 1000}},
            {"tool": "nmap", "params": {"timing": 3, "service_version": True}}
        ]
    },
    "passive_osint": {
        "id": "passive_osint",
        "name": "Stealth Passive OSINT Intelligence",
        "description": "100% passive pipeline: Subfinder -> OSINT Geolocation & ASN -> crt.sh Cert Transparency. Zero direct target traffic.",
        "stages": [
            {"tool": "subfinder", "params": {}},
            {"tool": "osint", "params": {}}
        ]
    }
}


class PipelineManager:
    """
    Manages and coordinates execution of sequential multi-stage pipelines.
    """

    def __init__(self, registry: ToolRegistry):
        self.registry = registry

    def get_presets(self) -> List[Dict[str, Any]]:
        return list(PIPELINE_PRESETS.values())

    def get_preset(self, preset_id: str) -> Dict[str, Any]:
        return PIPELINE_PRESETS.get(preset_id, {})
