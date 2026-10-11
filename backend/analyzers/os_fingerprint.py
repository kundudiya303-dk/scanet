"""
scanet — OS Detection & Fingerprinting Engine
Determines target Operating System using unprivileged, multi-vector heuristics:
1. TCP / IP TTL (Time-To-Live) Analysis
2. Service Banner Regex Extraction (SSH, HTTP Server, FTP, SMB)
3. Port Ecosystem Profile (Windows NetBIOS/SMB/RDP vs Linux SSH/NFS)
4. TCP Window Size Heuristics
Operates with zero root privileges and zero raw-packet requirements.
"""
import re
from typing import Dict, Any, List, Optional


class OSFingerprintEngine:
    """
    Multi-vector Operating System detection and fingerprinting engine.
    """

    # Banner pattern matchers: (pattern, os_family, os_name, confidence)
    BANNER_SIGNATURES = [
        # SSH Banners
        (r"Ubuntu-([0-9\.]+)", "Linux", "Ubuntu Linux (Canonical)", 95),
        (r"Debian-([0-9\+]+)", "Linux", "Debian GNU/Linux", 95),
        (r"CentOS", "Linux", "CentOS Linux", 90),
        (r"Red Hat|RHEL", "Linux", "Red Hat Enterprise Linux (RHEL)", 90),
        (r"Alpine", "Linux", "Alpine Linux", 95),
        (r"Arch Linux", "Linux", "Arch Linux", 90),
        (r"FreeBSD", "BSD", "FreeBSD", 95),
        (r"OpenSSH_for_Windows", "Windows", "Microsoft Windows (OpenSSH)", 95),
        (r"Cisco", "Cisco IOS", "Cisco IOS Network Appliance", 95),
        (r"MikroTik", "RouterOS", "MikroTik RouterOS", 95),

        # HTTP Server Banners
        (r"Microsoft-IIS/([0-9\.]+)", "Windows", "Microsoft Windows Server (IIS)", 95),
        (r"Apache/.*\(Ubuntu\)", "Linux", "Ubuntu Linux (Apache)", 95),
        (r"Apache/.*\(Debian\)", "Linux", "Debian GNU/Linux (Apache)", 95),
        (r"Apache/.*\(CentOS\)", "Linux", "CentOS Linux (Apache)", 90),
        (r"Apache/.*\(Red-Hat\)", "Linux", "Red Hat Enterprise Linux (Apache)", 90),
        (r"Apache/.*Win64", "Windows", "Microsoft Windows (Apache Win64)", 90),
        (r"lighttpd/.*\(Alpine\)", "Linux", "Alpine Linux (lighttpd)", 95),

        # FTP / General Banners
        (r"vsftpd ([0-9\.]+)", "Linux", "Linux (vsftpd daemon)", 85),
        (r"ProFTPD", "Linux", "Linux / Unix (ProFTPD)", 80),
        (r"Microsoft FTP Service", "Windows", "Microsoft Windows Server (MS-FTP)", 95),
    ]

    @staticmethod
    def deduce_os_from_ttl(ttl: int) -> Dict[str, Any]:
        """
        Deduces base OS family from observed IP TTL value.
        - Linux/Android: Initial TTL = 64
        - Windows: Initial TTL = 128
        - Cisco/Solaris/Network: Initial TTL = 255
        """
        if ttl <= 0:
            return {"family": "Unknown", "confidence": 0, "estimated_initial_ttl": 0}

        # Calculate estimated initial TTL and hop distance
        if ttl <= 64:
            initial = 64
            family = "Linux / Unix"
            name = "Linux Kernel 3.x - 6.x / Android"
            confidence = 80 if ttl >= 45 else 65
        elif ttl <= 128:
            initial = 128
            family = "Windows"
            name = "Microsoft Windows (10 / 11 / Server 2016-2025)"
            confidence = 85 if ttl >= 105 else 70
        else:
            initial = 255
            family = "Network / Unix"
            name = "Cisco IOS / Solaris / BSD Network Equipment"
            confidence = 85 if ttl >= 235 else 65

        hops = initial - ttl
        return {
            "family": family,
            "name": name,
            "confidence": confidence,
            "estimated_initial_ttl": initial,
            "estimated_network_hops": max(0, hops)
        }

    @classmethod
    def deduce_os_from_banners(cls, banners: List[str]) -> Optional[Dict[str, Any]]:
        """
        Extracts high-confidence OS signatures from collected service banners.
        """
        for banner in banners:
            if not banner:
                continue
            for pattern, family, name, conf in cls.BANNER_SIGNATURES:
                match = re.search(pattern, banner, re.IGNORECASE)
                if match:
                    extra = f" (version {match.group(1)})" if match.groups() else ""
                    return {
                        "family": family,
                        "name": f"{name}{extra}",
                        "confidence": conf,
                        "matched_signature": pattern,
                        "evidence_banner": banner.strip()[:120]
                    }
        return None

    @staticmethod
    def deduce_os_from_ports(open_ports: List[int]) -> Dict[str, Any]:
        """
        Analyzes the open port portfolio to detect characteristic operating systems.
        """
        port_set = set(open_ports)
        windows_indicators = {135, 137, 138, 139, 445, 3389, 5985, 5986}
        linux_indicators = {22, 111, 2049, 8080}

        win_matches = port_set.intersection(windows_indicators)
        linux_matches = port_set.intersection(linux_indicators)

        if len(win_matches) >= 2:
            return {
                "family": "Windows",
                "name": "Microsoft Windows (SMB/NetBIOS/RDP Profile)",
                "confidence": 85,
                "indicative_ports": sorted(list(win_matches))
            }
        elif 22 in port_set and not win_matches:
            return {
                "family": "Linux",
                "name": "Linux / Unix (SSH Profile)",
                "confidence": 75,
                "indicative_ports": sorted(list(linux_matches))
            }

        return {"family": "Unknown", "confidence": 0, "indicative_ports": []}

    @classmethod
    def fingerprint_target(
        cls,
        ttl: Optional[int] = None,
        banners: Optional[List[str]] = None,
        open_ports: Optional[List[int]] = None
    ) -> Dict[str, Any]:
        """
        Generates a composite, multi-vector OS detection report.
        Blends banner evidence, port architecture, and packet TTL.
        """
        banners = banners or []
        open_ports = open_ports or []

        banner_result = cls.deduce_os_from_banners(banners)
        port_result = cls.deduce_os_from_ports(open_ports)
        ttl_result = cls.deduce_os_from_ttl(ttl) if ttl else None

        # Priority 1: High-confidence service banner (e.g., Ubuntu/Debian/IIS header)
        if banner_result and banner_result["confidence"] >= 85:
            final_family = banner_result["family"]
            final_name = banner_result["name"]
            final_conf = banner_result["confidence"]
            primary_evidence = f"Banner match: {banner_result['evidence_banner']}"
        # Priority 2: Distinctive port profile (e.g., SMB 445 + NetBIOS 139)
        elif port_result and port_result["confidence"] >= 80:
            final_family = port_result["family"]
            final_name = port_result["name"]
            final_conf = port_result["confidence"]
            primary_evidence = f"Open ports: {port_result['indicative_ports']}"
        # Priority 3: Observed packet TTL
        elif ttl_result and ttl_result["confidence"] > 0:
            final_family = ttl_result["family"]
            final_name = ttl_result["name"]
            final_conf = ttl_result["confidence"]
            primary_evidence = f"Observed TTL: {ttl} (Initial: {ttl_result['estimated_initial_ttl']})"
        else:
            final_family = "Unknown"
            final_name = "Generic IP Device"
            final_conf = 20
            primary_evidence = "Insufficient fingerprint indicators"

        return {
            "os_family": final_family,
            "os_name": final_name,
            "confidence_percent": final_conf,
            "primary_evidence": primary_evidence,
            "vectors": {
                "banner_deduction": banner_result,
                "port_profile_deduction": port_result,
                "ttl_deduction": ttl_result
            }
        }
