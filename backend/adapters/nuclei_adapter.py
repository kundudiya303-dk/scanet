"""
scanet — Nuclei Tool Adapter
Template-Based Vulnerability & Misconfiguration Auditing (Tier 1 Extended).
"""
import json
from typing import List
from adapters.base import BaseToolAdapter, AdapterMeta


class NucleiAdapter(BaseToolAdapter):
    """
    Adapter for ProjectDiscovery Nuclei scanner.
    """

    @property
    def meta(self) -> AdapterMeta:
        return AdapterMeta(
            tool_name="nuclei",
            category="assessment",
            tier=1,
            description="Fast template-based scanner for known exposures, misconfigurations, and CVEs",
            requires_root=False,
            output_format="json"
        )

    def build_command_args(self, target: str, options: dict) -> List[str]:
        if options.get("use_builtin"):
            import sys
            return [sys.executable, "-m", "engine.builtin_tools", "nuclei", target]

        url = target if target.startswith(("http://", "https://")) else f"https://{target}"
        tags = options.get("tags", "misconfig,exposure,ssl,tech")
        severity = options.get("severity", "info,low,medium,high")
        rate_limit = int(options.get("rate_limit", 50))

        cmd = [
            "nuclei",
            "-target", url,
            "-tags", tags,
            "-severity", severity,
            "-rate-limit", str(rate_limit),
            "-silent",
            "-jsonl",
            "-no-color",
            "-duc"
        ]

        if options.get("templates"):
            cmd.extend(["-t", options["templates"]])

        return cmd

    def parse_output(self, raw_output: str, exit_code: int) -> dict:
        findings = []
        for line in raw_output.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                item = json.loads(line)
                info = item.get("info", {})
                classification = info.get("classification", {})
                cve_ids = classification.get("cve-id", [])
                if isinstance(cve_ids, str):
                    cve_ids = [cve_ids]

                findings.append({
                    "template_id": item.get("template-id"),
                    "name": info.get("name", item.get("template-id")),
                    "severity": info.get("severity", "info").lower(),
                    "description": info.get("description", ""),
                    "matched_at": item.get("matched-at"),
                    "cve_ids": cve_ids,
                    "cvss_score": classification.get("cvss-score", 0.0),
                    "remediation": info.get("remediation", "")
                })
            except json.JSONDecodeError:
                continue

        return {
            "findings": findings,
            "total_findings": len(findings),
            "exit_code": exit_code
        }
