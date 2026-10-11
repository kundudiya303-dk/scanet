"""
scanet — Gobuster Tool Adapter
Academic Web Directory and Virtual Host Enumeration (Tier 1 Extended).
"""
import os
import re
from typing import List
from adapters.base import BaseToolAdapter, AdapterMeta
from config import settings


class GobusterAdapter(BaseToolAdapter):
    """
    Adapter for Gobuster.
    """

    @property
    def meta(self) -> AdapterMeta:
        return AdapterMeta(
            tool_name="gobuster",
            category="web_discovery",
            tier=1,
            description="Classic high-speed directory, file, and DNS subdomain bruteforcing utility",
            requires_root=False,
            output_format="text"
        )

    def build_command_args(self, target: str, options: dict) -> List[str]:
        url = target if target.startswith(("http://", "https://")) else f"http://{target}"
        mode = options.get("mode", "dir")
        
        wordlist_name = options.get("wordlist", "common.txt")
        wordlist_path = os.path.realpath(os.path.join(settings.WORDLISTS_DIR, wordlist_name))
        allowed_dir = os.path.realpath(settings.WORDLISTS_DIR)
        
        if not wordlist_path.startswith(allowed_dir) or not os.path.exists(wordlist_path):
            wordlist_path = os.path.join(allowed_dir, "common.txt")

        threads = min(int(options.get("threads", 10)), 30)

        cmd = [
            "gobuster",
            mode,
            "-u", url,
            "-w", wordlist_path,
            "-t", str(threads),
            "--no-color",
            "-q"
        ]

        if options.get("extensions"):
            cmd.extend(["-x", options["extensions"]])

        return cmd

    def parse_output(self, raw_output: str, exit_code: int) -> dict:
        endpoints = []
        pattern = re.compile(r"^(\S+)\s+\(Status:\s*(\d+)\)(?:\s+\[Size:\s*(\d+)\])?")

        for line in raw_output.splitlines():
            line = line.strip()
            match = pattern.match(line)
            if match:
                path = match.group(1)
                status = int(match.group(2))
                size = int(match.group(3)) if match.group(3) else 0
                endpoints.append({
                    "path": path,
                    "status_code": status,
                    "size": size
                })

        return {
            "endpoints": endpoints,
            "total_discovered": len(endpoints),
            "exit_code": exit_code
        }
