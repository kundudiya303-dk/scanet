"""
scanet — Tool Registry
Central registry mapping tool names to their adapter instances.
"""
from adapters.nmap_adapter      import NmapAdapter
from adapters.naabu_adapter     import NaabuAdapter
from adapters.ffuf_adapter      import FfufAdapter
from adapters.dnsx_adapter      import DnsxAdapter
from adapters.subfinder_adapter import SubfinderAdapter
from adapters.httpx_adapter     import HttpxAdapter
from adapters.mtr_adapter       import MtrAdapter
from adapters.katana_adapter    import KatanaAdapter
from adapters.nuclei_adapter    import NucleiAdapter
from adapters.gobuster_adapter  import GobusterAdapter
from adapters.rustscan_adapter  import RustScanAdapter
from adapters.osint_adapter     import OsintAdapter

TOOL_ADAPTERS = {
    "nmap":      NmapAdapter(),
    "naabu":     NaabuAdapter(),
    "ffuf":      FfufAdapter(),
    "dnsx":      DnsxAdapter(),
    "subfinder": SubfinderAdapter(),
    "httpx":     HttpxAdapter(),
    "mtr":       MtrAdapter(),
    "katana":    KatanaAdapter(),
    "nuclei":    NucleiAdapter(),
    "gobuster":  GobusterAdapter(),
    "rustscan":  RustScanAdapter(),
    "osint":     OsintAdapter(),
}



def get_adapter(tool_name: str):
    """Returns the adapter instance for a given tool name."""
    return TOOL_ADAPTERS.get(tool_name)


def list_all_adapters() -> list[dict]:
    """Returns metadata for all registered adapters."""
    return [
        {
            **adapter.meta.__dict__,
            "installed": adapter.is_installed(),
            "version":   adapter.get_version() if adapter.is_installed() else "N/A",
        }
        for adapter in TOOL_ADAPTERS.values()
    ]


class ToolRegistry:
    @staticmethod
    def get(tool_name: str):
        return get_adapter(tool_name)

    @staticmethod
    def list_all():
        return list_all_adapters()

