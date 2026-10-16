"""
scanet — RustScan Tool Adapter
Ultra-Fast Port Discovery Engine (Tier 2).
"""
import re
from typing import List
from adapters.base import BaseToolAdapter, AdapterMeta


class RustScanAdapter(BaseToolAdapter):
    """
    Adapter for RustScan port scanner.
    """

    @property
    def meta(self) -> AdapterMeta:
        return AdapterMeta(
            tool_name="rustscan",
            category="port_scan",
            tier=2,
            description="High-speed port scanner written in Rust with adaptive timeout algorithm",
            requires_root=False,
            output_format="text"
        )

    def build_command_args(self, target: str, options: dict) -> List[str]:
        if not self.has_native_binary():
            import sys
            return [sys.executable, "-m", "engine.builtin_tools", "rustscan", target]

        ports = options.get("ports", "1-1000")
        batch_size = str(options.get("batch_size", 4500))

        cmd = [
            "rustscan",
            "-a", target,
            "-r", ports,
            "-b", batch_size,
            "--accessible",
            "--no-nmap"
        ]

        return cmd

    def parse_output(self, raw_output: str, exit_code: int) -> dict:
        open_ports = []
        for line in raw_output.splitlines():
            bracket_match = re.search(r"\[([0-9,\s]+)\]", line)
            if bracket_match:
                port_strs = bracket_match.group(1).split(",")
                for p in port_strs:
                    p = p.strip()
                    if p.isdigit():
                        open_ports.append(int(p))
            else:
                match = re.search(r"Open\s+(?:[\d\.]+):(\d+)", line)
                if match:
                    open_ports.append(int(match.group(1)))

        unique_ports = sorted(list(set(open_ports)))
        return {
            "open_ports": unique_ports,
            "total_open": len(unique_ports),
            "exit_code": exit_code
        }
