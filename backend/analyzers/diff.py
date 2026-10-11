"""
scanet — Scan Diff Engine
Compares two scan results and identifies added, removed, and changed assets.
Zero external tool dependency.
"""
from typing import Any


def diff_hosts(old_result: dict, new_result: dict) -> dict:
    """
    Compares host/port data between two scan jobs.
    Returns structured diff with added, removed, and unchanged sets.
    """
    def build_port_map(hosts: list) -> dict:
        """Maps ip -> set of (port, protocol) tuples."""
        mapping = {}
        for host in hosts:
            ip    = host.get("ip", "unknown")
            ports = host.get("ports", [])
            mapping[ip] = set(
                (p.get("port"), p.get("protocol", "tcp"))
                for p in ports if p.get("state") == "open"
            )
        return mapping

    old_map = build_port_map(old_result.get("hosts", []))
    new_map = build_port_map(new_result.get("hosts", []))

    all_ips  = set(old_map.keys()) | set(new_map.keys())
    added_hosts    = []
    removed_hosts  = []
    changed_hosts  = []

    for ip in all_ips:
        old_ports = old_map.get(ip, set())
        new_ports = new_map.get(ip, set())

        if ip not in old_map:
            added_hosts.append({"ip": ip, "new_ports": list(new_ports)})
        elif ip not in new_map:
            removed_hosts.append({"ip": ip, "old_ports": list(old_ports)})
        else:
            added_ports   = new_ports - old_ports
            removed_ports = old_ports - new_ports
            if added_ports or removed_ports:
                changed_hosts.append({
                    "ip":             ip,
                    "added_ports":    [{"port": p[0], "protocol": p[1]} for p in added_ports],
                    "removed_ports":  [{"port": p[0], "protocol": p[1]} for p in removed_ports],
                })

    return {
        "summary": {
            "new_hosts":     len(added_hosts),
            "removed_hosts": len(removed_hosts),
            "changed_hosts": len(changed_hosts),
        },
        "added":   added_hosts,
        "removed": removed_hosts,
        "changed": changed_hosts,
    }
