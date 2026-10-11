"""
scanet — AI Security Advisory & Copilot Engine
Provides automated, heuristic and LLM-assisted threat explanations,
MITRE ATT&CK mapping, and student-focused remediation advice.
Runs completely offline with zero mandatory API dependencies.
"""
from typing import List, Dict, Any, Optional


# Port-specific heuristics & MITRE ATT&CK mappings
PORT_RISK_KNOWLEDGE = {
    21: {
        "service": "FTP",
        "risk_level": "HIGH",
        "title": "Cleartext File Transfer Protocol Exposed",
        "explanation": "FTP transmits credentials and payload data in plaintext, exposing authentication sessions to sniffing and man-in-the-middle attacks.",
        "mitre_attack": "T1040 - Network Sniffing",
        "remediation": "Replace FTP with SFTP (SSH File Transfer Protocol) or FTPS with enforced TLS 1.3 encryption."
    },
    22: {
        "service": "SSH",
        "risk_level": "LOW",
        "title": "Secure Shell Port Exposed",
        "explanation": "Standard administrative entrypoint. Exposure to public subnets invites automated password bruteforce attacks.",
        "mitre_attack": "T1110 - Brute Force / Password Guessing",
        "remediation": "Disable root login (`PermitRootLogin no`), enforce SSH public key authentication, and deploy Fail2ban."
    },
    23: {
        "service": "Telnet",
        "risk_level": "CRITICAL",
        "title": "Insecure Legacy Telnet Daemon",
        "explanation": "Telnet is an obsolete unencrypted protocol. All usernames, passwords, and terminal keystrokes are transmitted in cleartext.",
        "mitre_attack": "T1040 - Network Sniffing / T1078 - Valid Accounts",
        "remediation": "Immediately terminate telnetd service and replace with OpenSSH (`sshd`)."
    },
    445: {
        "service": "SMB",
        "risk_level": "CRITICAL",
        "title": "Microsoft Server Message Block (SMB) Exposed",
        "explanation": "Direct SMB exposure to untrusted subnets has historically enabled worm propagation (EternalBlue / WannaCry) and NTLM relay attacks.",
        "mitre_attack": "T1021.002 - Remote Services: SMB/Windows Admin Shares",
        "remediation": "Block TCP port 445 at firewall perimeter. Isolate internal file shares behind an encrypted VPN."
    },
    3389: {
        "service": "RDP",
        "risk_level": "HIGH",
        "title": "Remote Desktop Protocol (RDP) Exposed",
        "explanation": "Public RDP listeners are primary targets for ransomware syndicates using credential stuffing and BlueKeep vulnerabilities.",
        "mitre_attack": "T1021.001 - Remote Desktop Protocol",
        "remediation": "Place RDP behind a secure VPN gateway or RD Gateway with Multi-Factor Authentication (MFA)."
    },
    6379: {
        "service": "Redis",
        "risk_level": "CRITICAL",
        "title": "In-Memory Redis Cache Exposed",
        "explanation": "Redis instances frequently lack authentication by default, allowing remote attackers to write SSH authorized_keys or cron jobs for immediate RCE.",
        "mitre_attack": "T1059 - Command and Scripting Interpreter",
        "remediation": "Set `bind 127.0.0.1` in redis.conf, require strong authentication with `requirepass`, and block port 6379."
    },
    8080: {
        "service": "HTTP-Proxy / Alt-HTTP",
        "risk_level": "MEDIUM",
        "title": "Alternative HTTP Port (Common Admin / Dev Interface)",
        "explanation": "Port 8080 often hosts unauthenticated developer dashboards, Jenkins, Tomcat manager, or staging APIs with default credentials.",
        "mitre_attack": "T1190 - Exploit Public-Facing Application",
        "remediation": "Verify authentication requirements, audit exposed administrative paths, and disable debug endpoints."
    }
}


class AISecurityAdvisor:
    """
    Expert heuristic security advisor with optional LLM integration.
    """

    def analyze_findings(self, scan_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyzes normalized scan results and outputs prioritized advisory insights,
        MITRE ATT&CK associations, and concrete remediation instructions.
        """
        advisories: List[Dict[str, Any]] = []
        mitre_tactics: set = set()
        overall_risk_score = 100 # Starts at 100 (clean) and deducts points

        # 1. Analyze Open Ports
        ports = scan_results.get("ports", [])
        for p in ports:
            port_num = p.get("port_number")
            service = p.get("service_name", "")
            
            if port_num in PORT_RISK_KNOWLEDGE:
                info = PORT_RISK_KNOWLEDGE[port_num]
                risk = info["risk_level"]
                
                # Penalty calculation
                deduction = 25 if risk == "CRITICAL" else (15 if risk == "HIGH" else 5)
                overall_risk_score = max(0, overall_risk_score - deduction)
                mitre_tactics.add(info["mitre_attack"])

                advisories.append({
                    "category": "port_exposure",
                    "target_port": port_num,
                    "service": service or info["service"],
                    "risk_level": risk,
                    "title": info["title"],
                    "explanation": info["explanation"],
                    "mitre_attack": info["mitre_attack"],
                    "remediation": info["remediation"]
                })

        # 2. Analyze HTTP Security Headers
        header_grade = scan_results.get("header_grade")
        if header_grade and header_grade in ["D", "F"]:
            overall_risk_score = max(0, overall_risk_score - 15)
            mitre_tactics.add("T1190 - Exploit Public-Facing Application")
            advisories.append({
                "category": "http_misconfiguration",
                "risk_level": "MEDIUM",
                "title": f"Poor HTTP Security Header Posture (Grade {header_grade})",
                "explanation": "Target web server is missing critical defensive headers (Content-Security-Policy, HSTS, or X-Frame-Options), leaving users vulnerable to Clickjacking and Cross-Site Scripting (XSS).",
                "mitre_attack": "T1189 - Drive-by Compromise",
                "remediation": "Deploy standard OWASP-recommended headers: Strict-Transport-Security, Content-Security-Policy: default-src 'self', and X-Content-Type-Options: nosniff."
            })

        # Sort advisories by severity
        severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "INFO": 4}
        advisories.sort(key=lambda a: severity_order.get(a.get("risk_level", "INFO"), 5))

        return {
            "hygiene_score": overall_risk_score,
            "grade": "A" if overall_risk_score >= 85 else ("B" if overall_risk_score >= 70 else ("C" if overall_risk_score >= 50 else "F")),
            "total_advisories": len(advisories),
            "critical_count": sum(1 for a in advisories if a["risk_level"] == "CRITICAL"),
            "high_count": sum(1 for a in advisories if a["risk_level"] == "HIGH"),
            "mitre_techniques": sorted(list(mitre_tactics)),
            "advisories": advisories
        }
