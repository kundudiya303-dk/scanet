"""scanet — Naabu Adapter (Fast Port Discovery, Tier 1)"""
import json
from adapters.base import BaseToolAdapter, AdapterMeta, ToolResult
from typing import List


class NaabuAdapter(BaseToolAdapter):

    @property
    def meta(self) -> AdapterMeta:
        return AdapterMeta(
            tool_name="naabu",
            category="port_scan",
            tier=1,
            description="High-speed port discovery with JSON output",
            requires_root=False,
            output_format="json",
        )

    def build_command_args(self, target: str, options: dict) -> List[str]:
        args = ["naabu", "-host", target, "-json", "-silent"]
        rate = int(options.get("rate", 1000))
        rate = min(max(rate, 100), 5000)  # Enforce 100–5000 pps range
        args.extend(["-rate", str(rate)])
        top_ports = options.get("top_ports", "100")
        if top_ports in ["100", "1000"]:
            args.extend(["-top-ports", top_ports])
        return args

    def parse_output(self, raw_output: str, exit_code: int) -> dict:
        result = {"hosts": {}, "open_ports_count": 0, "tool": "naabu"}
        for line in raw_output.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                ip = entry.get("ip", "unknown")
                port = entry.get("port", 0)
                if ip not in result["hosts"]:
                    result["hosts"][ip] = []
                result["hosts"][ip].append({"port": port, "protocol": "tcp", "state": "open"})
                result["open_ports_count"] += 1
            except json.JSONDecodeError:
                continue
        result["hosts"] = [{"ip": ip, "ports": ports} for ip, ports in result["hosts"].items()]
        return result
