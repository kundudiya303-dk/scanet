"""
scanet — Nmap Tool Adapter
Unprivileged TCP Connect scan (-sT) with XML output parsed via defusedxml.
Tier 1 Core — Network Port & Service Discovery.
"""
import defusedxml.ElementTree as ET
from adapters.base import BaseToolAdapter, AdapterMeta, ToolResult
from typing import List


class NmapAdapter(BaseToolAdapter):

    @property
    def meta(self) -> AdapterMeta:
        return AdapterMeta(
            tool_name="nmap",
            category="port_scan",
            tier=1,
            description="Network port scanner with service and version detection",
            requires_root=False,  # Uses -sT (unprivileged TCP Connect)
            output_format="xml",
        )

    def build_command_args(self, target: str, options: dict) -> List[str]:
        args = ["nmap", "-sT", "-oX", "-", "--no-stylesheet"]

        # Timing/Speed: T1-T4 only (never T5 — too aggressive for lab networks)
        speed = str(options.get("speed", "3"))
        if speed in ["1", "2", "3", "4"]:
            args.extend(["-T", speed])
        else:
            args.extend(["-T", "3"])

        # Port profile
        ports = options.get("ports", "top-100")
        if ports == "top-100":
            args.extend(["--top-ports", "100"])
        elif ports == "top-1000":
            args.extend(["--top-ports", "1000"])
        elif ports == "top-65535":
            args.extend(["-p-"])
        else:
            args.extend(["--top-ports", "100"])  # Safe default

        # Service/Version detection
        if options.get("service_detection", True):
            args.append("-sV")

        # Script scan (default safe scripts)
        if options.get("script_scan", False):
            args.extend(["-sC"])

        args.append(target)
        return args

    def parse_output(self, raw_output: str, exit_code: int) -> dict:
        result = {"hosts": [], "open_ports_count": 0, "tool": "nmap"}
        if not raw_output:
            return {**result, "parse_error": "Empty output"}
        try:
            root = ET.fromstring(raw_output)
            for host_el in root.findall("host"):
                addr_el = host_el.find("address")
                if addr_el is None:
                    continue
                ip = addr_el.get("addr", "unknown")

                hostname = None
                hostnames_el = host_el.find("hostnames")
                if hostnames_el is not None:
                    hn = hostnames_el.find("hostname")
                    if hn is not None:
                        hostname = hn.get("name")

                ports = []
                ports_el = host_el.find("ports")
                if ports_el is not None:
                    for p in ports_el.findall("port"):
                        state_el = p.find("state")
                        if state_el is None or state_el.get("state") != "open":
                            continue
                        svc = p.find("service")
                        ports.append({
                            "port":     int(p.get("portid", 0)),
                            "protocol": p.get("protocol", "tcp"),
                            "state":    "open",
                            "service":  svc.get("name", "unknown") if svc is not None else "unknown",
                            "product":  svc.get("product", "") if svc is not None else "",
                            "version":  svc.get("version", "") if svc is not None else "",
                        })

                result["hosts"].append({
                    "ip":       ip,
                    "hostname": hostname,
                    "ports":    ports,
                })
                result["open_ports_count"] += len(ports)
        except Exception as e:
            result["parse_error"] = str(e)
        return result
