"""scanet — FFUF Adapter (Web Directory Discovery, Tier 1)"""
import json, os
from adapters.base import BaseToolAdapter, AdapterMeta
from typing import List
from config import settings


class FfufAdapter(BaseToolAdapter):

    @property
    def meta(self) -> AdapterMeta:
        return AdapterMeta(
            tool_name="ffuf",
            category="web_discovery",
            tier=1,
            description="High-speed web directory and file discovery with rate limiting",
            requires_root=False,
            output_format="json",
        )

    def build_command_args(self, target: str, options: dict) -> List[str]:
        if not self.has_native_binary():
            import sys
            return [sys.executable, "-m", "engine.builtin_tools", "ffuf", target]

        # Resolve wordlist path safely (must stay within allowed directory)
        wordlist_name = options.get("wordlist", "common.txt")
        wordlist_path = os.path.realpath(
            os.path.join(settings.WORDLIST_DIR, wordlist_name)
        )
        wordlist_base = os.path.realpath(settings.WORDLIST_DIR)
        if not wordlist_path.startswith(wordlist_base):
            wordlist_path = os.path.join(wordlist_base, "common.txt")

        args = [
            "ffuf",
            "-u", f"{target}/FUZZ",
            "-w", wordlist_path,
            "-o", "/dev/stdout",
            "-of", "json",
            "-s",                # Silent (no progress bar)
        ]

        # Rate limiting (enforce max 500 req/s)
        rate = int(options.get("rate", 50))
        rate = min(max(rate, 1), 500)
        args.extend(["-rate", str(rate)])

        # Filter by status codes
        match_codes = options.get("match_codes", "200,204,301,302,307,401,403")
        args.extend(["-mc", match_codes])

        # Extensions
        extensions = options.get("extensions", "")
        if extensions:
            args.extend(["-e", extensions])

        return args

    def parse_output(self, raw_output: str, exit_code: int) -> dict:
        result = {"endpoints": [], "total": 0, "tool": "ffuf"}
        try:
            data = json.loads(raw_output)
            for entry in data.get("results", []):
                result["endpoints"].append({
                    "url":            entry.get("url", ""),
                    "status_code":    entry.get("status", 0),
                    "content_length": entry.get("length", 0),
                    "words":          entry.get("words", 0),
                    "lines":          entry.get("lines", 0),
                })
            result["total"] = len(result["endpoints"])
        except Exception as e:
            result["parse_error"] = str(e)
        return result
