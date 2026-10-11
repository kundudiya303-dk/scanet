"""
scanet — SARIF v2.1.0 Exporter
Generates OASIS Static Analysis Results Interchange Format (SARIF) JSON.
Enables native ingestion into GitHub Code Scanning, GitLab CI, and DefectDojo.
"""
from typing import Dict, Any, List


def export_to_sarif(job_id: str, target: str, findings: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Translates scan findings into standard SARIF v2.1.0 schema.
    """
    sarif_results = []
    rules = []
    seen_rule_ids = set()

    severity_map = {
        "critical": "error",
        "high": "error",
        "medium": "warning",
        "low": "note",
        "info": "note"
    }

    for f in findings:
        rule_id = f.get("template_id") or f.get("cve_id") or f.get("name", "SCANET-FINDING")
        rule_name = f.get("name", "Security Finding")
        severity = f.get("severity", "medium").lower()
        level = severity_map.get(severity, "warning")

        if rule_id not in seen_rule_ids:
            seen_rule_ids.add(rule_id)
            rules.append({
                "id": rule_id,
                "name": rule_name,
                "shortDescription": {"text": rule_name},
                "fullDescription": {"text": f.get("description", rule_name)},
                "help": {"text": f.get("remediation", "Remediate according to vendor guidelines.")},
                "properties": {
                    "tags": ["security", "recon", "scanet"],
                    "cvss": f.get("cvss_score", 0.0)
                }
            })

        sarif_results.append({
            "ruleId": rule_id,
            "level": level,
            "message": {
                "text": f"{rule_name} detected at {f.get('matched_at', target)}"
            },
            "locations": [{
                "physicalLocation": {
                    "artifactLocation": {
                        "uri": f.get("matched_at", target)
                    }
                }
            }]
        })

    sarif_doc = {
        "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
        "version": "2.1.0",
        "runs": [{
            "tool": {
                "driver": {
                    "name": "scanet",
                    "version": "1.0.0",
                    "informationUri": "https://github.com/mjishaan59-cell/scanet",
                    "rules": rules
                }
            },
            "invocations": [{
                "executionSuccessful": True,
                "arguments": [f"target: {target}", f"job_id: {job_id}"]
            }],
            "results": sarif_results
        }]
    }

    return sarif_doc
