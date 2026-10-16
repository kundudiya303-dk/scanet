"""scanet — MTR Adapter (Network Hop Diagnostics, Tier 1)"""
import json
from adapters.base import BaseToolAdapter, AdapterMeta
from typing import List


class MtrAdapter(BaseToolAdapter):

    @property
    def meta(self) -> AdapterMeta:
        return AdapterMeta(
            tool_name="mtr",
            category="diagnostics",
            tier=1,
            description="Hop-by-hop network path analysis with latency and packet loss",
            requires_root=False,
            output_format="json",
        )

    def build_command_args(self, target: str, options: dict) -> List[str]:
        if not self.has_native_binary():
            import sys
            return [sys.executable, "-m", "engine.builtin_tools", "mtr", target]

        cycles = int(options.get("cycles", 5))
        cycles = min(max(cycles, 1), 20)  # 1–20 cycles max
        return [
            "mtr",
            "--json",
            "--report",
            "--report-cycles", str(cycles),
            "--no-dns",
            target,
        ]

    def parse_output(self, raw_output: str, exit_code: int) -> dict:
        result = {"hops": [], "destination": "", "tool": "mtr"}
        try:
            data = json.loads(raw_output)
            report = data.get("report", {})
            result["destination"] = report.get("mtr", {}).get("dst", "")
            for hub in report.get("hubs", []):
                result["hops"].append({
                    "count":   hub.get("count", 0),
                    "host":    hub.get("host", "???"),
                    "loss%":   hub.get("Loss%", 0),
                    "avg_ms":  hub.get("Avg", 0),
                    "best_ms": hub.get("Best", 0),
                    "worst_ms":hub.get("Wrst", 0),
                    "stdev":   hub.get("StDev", 0),
                })
        except Exception as e:
            result["parse_error"] = str(e)
        return result
