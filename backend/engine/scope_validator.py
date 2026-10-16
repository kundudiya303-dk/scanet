"""
scanet — Scope Validator & Target Guardrail
Validates and restricts scan targets to authorized ranges.
Permanently blocks cloud metadata (IMDS), link-local, and broadcast ranges.
Permits local laboratory/educational targets (RFC 1918 subnets, Metasploitable VMs, lab domains).
Allows loopback for authorized local web audits when explicitly requested.
"""
import ipaddress
from typing import Union

# Permanently hard-blocked ranges — strictly forbidden for cloud security & network safety
HARD_BLOCKED_NETWORKS = [
    ipaddress.ip_network("127.0.0.0/8"),      # IPv4 loopback (blocked by default, overridable for local web audit)
    ipaddress.ip_network("169.254.0.0/16"),   # Link-local / AWS Instance Metadata Service (IMDS)
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

    @classmethod
    def validate(cls, target: str, allow_loopback: bool = False) -> tuple[bool, str]:
        """Convenience classmethod for rapid target validation."""
        cleaned = target.strip().lower()
        if "://" in cleaned:
            cleaned = cleaned.split("://")[1].split("/")[0].split(":")[0]
        else:
            cleaned = cleaned.split("/")[0].split(":")[0]
        validator = cls()
        res = validator.validate_target(cleaned, require_whitelist=False, allow_loopback=allow_loopback)
        return res["valid"], res["reason"]

    def is_hard_blocked(self, ip_str: str, allow_loopback: bool = False) -> tuple[bool, str]:
        """Returns (is_blocked, reason) for a given IP address string."""
        if allow_loopback and ip_str in ("127.0.0.1", "localhost", "::1"):
            return False, ""
        try:
            addr = ipaddress.ip_address(ip_str)
            if allow_loopback and addr.is_loopback:
                return False, ""
            for network in HARD_BLOCKED_NETWORKS:
                if addr in network:
                    return True, f"Address {ip_str} is in permanently blocked range {network}"
            return False, ""
        except ValueError:
            return False, ""  # Hostname (e.g. juiceshop.lab, metasploitable.local)

    def is_private_ip(self, ip_str: str) -> bool:
        """Returns True if the IP is in an RFC 1918 private range."""
        try:
            return ipaddress.ip_address(ip_str).is_private
        except ValueError:
            return False

    def validate_target(self, target: str, require_whitelist: bool = True, allow_loopback: bool = False) -> dict:
        """
        Full target validation.
        Returns {"valid": bool, "target": str, "reason": str}
        """
        target = target.strip().lower()

        if not target:
            return {"valid": False, "target": target, "reason": "Target cannot be empty"}

        # Check hard-blocked IP addresses
        blocked, reason = self.is_hard_blocked(target, allow_loopback=allow_loopback)
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
