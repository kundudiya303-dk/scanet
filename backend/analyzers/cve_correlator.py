"""
scanet — CVE & Threat Intelligence Correlator
Maps detected software versions to known CVEs, CISA KEV status, and EPSS scores.
Runs locally with zero external network dependencies required.
"""
from typing import List, Dict, Any


# Built-in high-impact CVE database curated for educational labs and common audit exposures
CVE_KNOWLEDGE_BASE = [
    {
        "product": "openssh",
        "min_version": "8.5p1",
        "max_version": "9.7p1",
        "cve_id": "CVE-2024-6387",
        "name": "regreSSHion: Remote Unauthenticated Code Execution",
        "cvss": 8.1,
        "severity": "HIGH",
        "cisa_kev": True,
        "epss": 0.88,
        "mitre_attack": "T1190 - Exploit Public-Facing Application",
        "remediation": "Upgrade OpenSSH to version 9.8p1 or newer, or set LoginGraceTime 0 in sshd_config."
    },
    {
        "product": "apache",
        "min_version": "2.4.49",
        "max_version": "2.4.50",
        "cve_id": "CVE-2021-41773",
        "name": "Apache HTTP Server Path Traversal & RCE",
        "cvss": 9.8,
        "severity": "CRITICAL",
        "cisa_kev": True,
        "epss": 0.97,
        "mitre_attack": "T1006 - Direct Volume Access / T1190",
        "remediation": "Immediately upgrade Apache HTTP Server to version 2.4.51 or higher."
    },
    {
        "product": "vsftpd",
        "min_version": "2.3.4",
        "max_version": "2.3.4",
        "cve_id": "CVE-2011-2523",
        "name": "vsftpd Smile Backdoor Remote Code Execution",
        "cvss": 9.8,
        "severity": "CRITICAL",
        "cisa_kev": False,
        "epss": 0.94,
        "mitre_attack": "T1190 - Exploit Public-Facing Application",
        "remediation": "Common in Metasploitable 2. Replace compromised vsftpd binary with a verified release."
    },
    {
        "product": "redis",
        "min_version": "1.0",
        "max_version": "7.0",
        "cve_id": "MISCONFIG-REDIS-UNAUTH",
        "name": "Redis Insecure Unauthenticated Remote Access",
        "cvss": 9.0,
        "severity": "CRITICAL",
        "cisa_kev": True,
        "epss": 0.91,
        "mitre_attack": "T1078 - Valid Accounts / Unauthenticated Execution",
        "remediation": "Enable requirepass in redis.conf, bind to 127.0.0.1, or place behind an encrypted tunnel."
    },
    {
        "product": "tomcat",
        "min_version": "7.0.0",
        "max_version": "9.0.30",
        "cve_id": "CVE-2020-1938",
        "name": "Ghostcat: Apache Tomcat AJP Insecure File Read/Inclusion",
        "cvss": 9.8,
        "severity": "CRITICAL",
        "cisa_kev": True,
        "epss": 0.95,
        "mitre_attack": "T1190 - Exploit Public-Facing Application",
        "remediation": "Disable AJP Connector on port 8009 if not required, or set secretRequired='true'."
    },
    {
        "product": "nginx",
        "min_version": "1.20.0",
        "max_version": "1.21.4",
        "cve_id": "CVE-2021-23017",
        "name": "1-Byte Memory Overwrite in DNS Resolver",
        "cvss": 7.7,
        "severity": "HIGH",
        "cisa_kev": False,
        "epss": 0.42,
        "mitre_attack": "T1190 - Exploit Public-Facing Application",
        "remediation": "Update Nginx to 1.20.1 / 1.21.0 or newer."
    }
]


import re


def _parse_version(v_str: str) -> tuple:
    parts = re.findall(r"\d+", v_str)
    return tuple(map(int, parts)) if parts else (0,)


def correlate_service_cves(product: str, version: str) -> List[Dict[str, Any]]:
    """
    Correlates a service product name and version string against the CVE knowledge base.
    """
    if not product:
        return []

    product_clean = product.lower().strip()
    matched_cves = []

    for entry in CVE_KNOWLEDGE_BASE:
        target_prod = entry["product"]
        if target_prod in product_clean:
            if version:
                ver_clean = version.lower().strip()
                v_num = _parse_version(ver_clean)
                min_v = _parse_version(entry["min_version"])
                max_v = _parse_version(entry["max_version"])
                if min_v <= v_num <= max_v:
                    matched_cves.append(entry)
            else:
                entry_copy = dict(entry)
                entry_copy["severity"] = "MEDIUM (Potential)"
                matched_cves.append(entry_copy)


    return matched_cves
