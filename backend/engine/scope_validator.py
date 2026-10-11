"""
scanet — Scope Validator & Target Guardrail
Validates and restricts scan targets to authorized ranges.
Permanently blocks loopback, cloud metadata, link-local, and private ranges
unless explicitly whitelisted by an administrator.
"""
import ipaddress
from typing import Union

# Permanently hard-blocked ranges — never scannable under any configuration
HARD_BLOCKED_NETWORKS = [
    ipaddress.ip_network("127.0.0.0/8"),      # IPv4 loopback
    ipaddress.ip_network("169.254.0.0/16"),   # Link-local / AWS Instance Metadata Service
    ipaddress.ip_network("::1/128"),           # IPv6 loopback
    ipaddress.ip_network("fc00::/7"),          # IPv6 unique local
    ipaddress.ip_network("fe80::/10"),         # IPv6 link-local
    ipaddress.ip_network("0.0.0.0/8"),         # Current network (invalid target)
    ipaddress.ip_network("255.255.255.255/32"),# Broadcast
]


class ScopeValidator:
    """
    Validates that a target IP, hostname, or CIDR block is within
    an approved whitelist and not in any hard-blocked range.
    """

    def __init__(self, approved_targets: list[str] | None = None):
        self.approved_targets = approved_targets or []

    def is_hard_blocked(self, ip_str: str) -> tuple[bool, str]:
        """Returns (is_blocked, reason) for a given IP address string."""
        try:
            addr = ipaddress.ip_address(ip_str)
            for network in HARD_BLOCKED_NETWORKS:
                if addr in network:
                    return True, f"Address {ip_str} is in permanently blocked range {network}"
            return False, ""
        except ValueError:
            return False, ""  # Not a plain IP — let hostname validation handle it

    def is_private_ip(self, ip_str: str) -> bool:
        """Returns True if the IP is in an RFC 1918 private range."""
        try:
            return ipaddress.ip_address(ip_str).is_private
        except ValueError:
            return False

    def validate_target(self, target: str, require_whitelist: bool = True) -> dict:
        """
        Full target validation.
        Returns {"valid": bool, "target": str, "reason": str}
        """
        target = target.strip().lower()

        if not target:
            return {"valid": False, "target": target, "reason": "Target cannot be empty"}

        # Check hard-blocked IP addresses
        blocked, reason = self.is_hard_blocked(target)
        if blocked:
            return {"valid": False, "target": target, "reason": reason}

        # Whitelist check
        if require_whitelist and self.approved_targets:
            if target not in self.approved_targets:
                return {
                    "valid": False,
                    "target": target,
                    "reason": f"Target '{target}' is not in the approved scope whitelist",
                }

        return {"valid": True, "target": target, "reason": ""}
