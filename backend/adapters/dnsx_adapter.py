"""scanet — dnsx Adapter (DNS Analysis & Resolution, Tier 1)"""
import json
from adapters.base import BaseToolAdapter, AdapterMeta
from typing import List


class DnsxAdapter(BaseToolAdapter):

    @property
    def meta(self) -> AdapterMeta:
        return AdapterMeta(
            tool_name="dnsx",
            category="dns",
            tier=1,
            description="Multi-record DNS resolution and active query engine",
            requires_root=False,
            output_format="json",
        )

    def build_command_args(self, target: str, options: dict) -> List[str]:
        if not self.has_native_binary():
            import sys
            return [sys.executable, "-m", "engine.builtin_tools", "dnsx", target]

        record_types = options.get("record_types", ["a", "cname", "mx", "txt"])
        safe_types = {"a", "aaaa", "cname", "mx", "txt", "ns", "ptr", "soa"}
        filtered_types = [r for r in record_types if r.lower() in safe_types]
        if not filtered_types:
            filtered_types = ["a"]

        args = ["dnsx", "-d", target, "-json", "-silent"]
        for rtype in filtered_types:
            args.extend([f"-{rtype}"])
        return args

    def parse_output(self, raw_output: str, exit_code: int) -> dict:
        result = {"records": [], "total": 0, "tool": "dnsx"}
        for line in raw_output.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                result["records"].append(entry)
            except json.JSONDecodeError:
                continue
        result["total"] = len(result["records"])
        return result
