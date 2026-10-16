"""
scanet — Katana Tool Adapter
Modern Web Crawling, Spidering, and Endpoint Discovery (Tier 1 Extended).
"""
import json
from typing import List
from adapters.base import BaseToolAdapter, AdapterMeta


class KatanaAdapter(BaseToolAdapter):
    """
    Adapter for ProjectDiscovery Katana crawler.
    Executes non-destructive discovery of web application surface area.
    """

    @property
    def meta(self) -> AdapterMeta:
        return AdapterMeta(
            tool_name="katana",
            category="web_discovery",
            tier=1,
            description="Next-generation web crawler for endpoint, API route, and parameter discovery",
            requires_root=False,
            output_format="json"
        )

    def build_command_args(self, target: str, options: dict) -> List[str]:
        if not self.has_native_binary():
            import sys
            return [sys.executable, "-m", "engine.builtin_tools", "katana", target]

        url = target if target.startswith(("http://", "https://")) else f"https://{target}"
        depth = int(options.get("depth", 2))
        max_duration = options.get("crawl_duration", "3m")
        concurrency = int(options.get("concurrency", 10))

        cmd = [
            "katana",
            "-u", url,
            "-jc",
            "-depth", str(depth),
            "-concurrency", str(concurrency),
            "-crawl-duration", max_duration,
            "-silent",
            "-no-color"
        ]

        if options.get("crawl_scope") == "subdomains":
            cmd.append("-crawl-subdomains")

        return cmd

    def parse_output(self, raw_output: str, exit_code: int) -> dict:
        endpoints = []
        for line in raw_output.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                url = data.get("request", {}).get("endpoint") or data.get("endpoint")
                if url:
                    endpoints.append({
                        "url": url,
                        "method": data.get("request", {}).get("method", "GET"),
                        "source": data.get("source", "crawler")
                    })
            except json.JSONDecodeError:
                if line.startswith("http"):
                    endpoints.append({
                        "url": line,
                        "method": "GET",
                        "source": "crawler"
                    })

        return {
            "endpoints": endpoints,
            "total_discovered": len(endpoints),
            "exit_code": exit_code
        }
