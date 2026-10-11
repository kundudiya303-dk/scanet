"""
scanet — Subnet & CIDR Calculator
Native Python module for IP address and network math.
Zero external tool dependency — uses Python's built-in ipaddress module.
"""
import ipaddress
from typing import Union


def calculate_subnet(cidr: str) -> dict:
    """
    Calculates subnet details for a given CIDR block.
    Example: calculate_subnet("192.168.1.0/24")
    """
    try:
        network = ipaddress.ip_network(cidr, strict=False)
        hosts   = list(network.hosts())
        return {
            "cidr":             str(network),
            "network_address":  str(network.network_address),
            "broadcast":        str(network.broadcast_address),
            "netmask":          str(network.netmask),
            "wildcard":         str(network.hostmask),
            "prefix_length":    network.prefixlen,
            "total_addresses":  network.num_addresses,
            "usable_hosts":     len(hosts),
            "first_host":       str(hosts[0]) if hosts else "N/A",
            "last_host":        str(hosts[-1]) if hosts else "N/A",
            "ip_version":       network.version,
            "is_private":       network.is_private,
            "is_multicast":     network.is_multicast,
            "error":            None,
        }
    except ValueError as e:
        return {"error": str(e), "cidr": cidr}


def is_ip_in_range(ip: str, cidr: str) -> dict:
    """Returns whether a given IP address falls within the CIDR range."""
    try:
        addr    = ipaddress.ip_address(ip)
        network = ipaddress.ip_network(cidr, strict=False)
        return {"ip": ip, "cidr": cidr, "in_range": addr in network}
    except ValueError as e:
        return {"error": str(e)}
