"""scanet — HTTPX Adapter (HTTP Inspection & Tech Fingerprinting, Tier 1)"""
import json
from adapters.base import BaseToolAdapter, AdapterMeta
from typing import List


class HttpxAdapter(BaseToolAdapter):

    @property
    def meta(self) -> AdapterMeta:
        return AdapterMeta(
            tool_name="httpx",
            category="http",
            tier=1,
            description="HTTP probing: status codes, redirects, TLS, titles, and tech detection",
            requires_root=False,
            output_format="json",
        )

    def build_command_args(self, target: str, options: dict) -> List[str]:
        args = [
            "httpx",
            "-u", target,
            "-json",
            "-silent",
            "-follow-redirects",
            "-title",
            "-tech-detect",
            "-status-code",
            "-content-length",
            "-tls-grab",
            "-timeout", "10",
        ]
        if options.get("include_cdn", False):
            args.append("-cdn")
        return args

    def parse_output(self, raw_output: str, exit_code: int) -> dict:
        result = {"endpoints": [], "total": 0, "tool": "httpx"}
        for line in raw_output.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                result["endpoints"].append({
                    "url":            entry.get("url", ""),
                    "status_code":    entry.get("status_code", 0),
                    "title":          entry.get("title", ""),
                    "content_length": entry.get("content_length", 0),
                    "tech":           entry.get("tech", []),
                    "tls":            entry.get("tls", {}),
                    "webserver":      entry.get("webserver", ""),
                })
            except json.JSONDecodeError:
                continue
        result["total"] = len(result["endpoints"])
        return result
