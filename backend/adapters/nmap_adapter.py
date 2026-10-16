"""
scanet — Nmap Tool Adapter
Unprivileged TCP Connect scan (-sT) with XML output parsed via defusedxml.
Features seamless built-in native socket fallback when native Nmap binary is absent.
Tier 1 Core — Network Port & Service Discovery.
"""
import sys
import shutil
import subprocess

try:
    import defusedxml.ElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

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

    def is_installed(self) -> bool:
        """
        Nmap is always available in Scanet:
        - Uses native system nmap binary if present in PATH.
        - Seamlessly falls back to Scanet's built-in async socket scanner otherwise.
        """
        return True

    def get_version(self) -> str:
        """Returns version string from nmap binary, or built-in engine indicator."""
        if shutil.which("nmap"):
            try:
                res = subprocess.run(["nmap", "--version"], capture_output=True, text=True, timeout=5)
                out = res.stdout or res.stderr
                return out.splitlines()[0].strip() if out else "Nmap (installed)"
            except Exception:
                return "Nmap (installed)"
        return "Scanet Built-in Socket Engine v1.0 (Nmap-compatible)"

    def build_command_args(self, target: str, options: dict) -> List[str]:
        speed = str(options.get("speed", "3"))
        if speed not in ["1", "2", "3", "4"]:
            speed = "3"

        ports = options.get("ports", "top-100")

        # If system Nmap is installed, use native nmap
        if shutil.which("nmap"):
            args = ["nmap", "-sT", "-oX", "-", "--no-stylesheet"]
            args.extend(["-T", speed])

            if ports == "top-100":
                args.extend(["--top-ports", "100"])
            elif ports == "top-1000":
                args.extend(["--top-ports", "1000"])
            elif ports == "top-65535":
                args.extend(["-p-"])
            else:
                args.extend(["--top-ports", "100"])

            if options.get("service_detection", True):
                args.append("-sV")

            if options.get("script_scan", False):
                args.extend(["-sC"])

            args.append(target)
            return args

        # Otherwise use built-in engine
        return [
            sys.executable,
            "-m",
            "engine.builtin_scanner",
            target,
            "--ports",
            ports,
            "--speed",
            speed,
        ]

    def parse_output(self, raw_output: str, exit_code: int) -> dict:
        result = {"hosts": [], "open_ports_count": 0, "tool": "nmap"}
        if not raw_output:
            return {**result, "parse_error": "Empty output"}
        try:
            # Extract XML portion even if progress lines were printed before it
            xml_text = raw_output
            if "<nmaprun" in raw_output:
                start_idx = raw_output.index("<nmaprun")
                end_token = "</nmaprun>"
                if end_token in raw_output:
                    end_idx = raw_output.rindex(end_token) + len(end_token)
                    xml_text = raw_output[start_idx:end_idx]

            root = ET.fromstring(xml_text)
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
