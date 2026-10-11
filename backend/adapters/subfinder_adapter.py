"""scanet — Subfinder Adapter (Passive Subdomain Discovery, Tier 1)"""
import json
from adapters.base import BaseToolAdapter, AdapterMeta
from typing import List


class SubfinderAdapter(BaseToolAdapter):

    @property
    def meta(self) -> AdapterMeta:
        return AdapterMeta(
            tool_name="subfinder",
            category="dns",
            tier=1,
            description="Passive subdomain discovery using public intelligence sources",
            requires_root=False,
            output_format="json",
        )

    def build_command_args(self, target: str, options: dict) -> List[str]:
        return ["subfinder", "-d", target, "-json", "-silent"]

    def parse_output(self, raw_output: str, exit_code: int) -> dict:
        result = {"subdomains": [], "total": 0, "tool": "subfinder"}
        for line in raw_output.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                result["subdomains"].append({
                    "subdomain": entry.get("host", ""),
                    "source":    entry.get("source", "unknown"),
                })
            except json.JSONDecodeError:
                result["subdomains"].append({"subdomain": line, "source": "unknown"})
        result["total"] = len(result["subdomains"])
        return result
