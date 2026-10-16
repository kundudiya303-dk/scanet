"""
scanet API — Interactive Attack Surface Topology Graph
Builds graph nodes and edges from real scan DB data for Cytoscape.js visualization:
Target -> Hosts -> Open Ports -> Findings.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.connection import get_db
from database.models import Target, Host, Port, Finding, ScanJob
from typing import Dict, Any, List

router = APIRouter()


@router.get("/graph/{target_id}")
async def get_target_topology_graph(target_id: str, db: AsyncSession = Depends(get_db)):
    """
    Returns graph elements (nodes and edges) formatted for Cytoscape.js / D3.
    Builds topology from real scan result data in the database.
    - Root Target Node
    - Host IP Nodes (from completed scan jobs)
    - Service/Port Nodes (color-coded by risk)
    - Finding/Alert Nodes
    """
    # Verify target exists
    result = await db.execute(select(Target).where(Target.id == target_id))
    target = result.scalar_one_or_none()
    if not target:
        raise HTTPException(status_code=404, detail=f"Target '{target_id}' not found.")

    nodes = []
    edges = []

    # Root target node
    nodes.append({
        "data": {
            "id":    f"target_{target_id}",
            "label": target.name or target.value,
            "type":  "target",
            "color": "#6366f1",
            "value": target.value,
        }
    })

    # Get all hosts from scan jobs for this target
    hosts_result = await db.execute(
        select(Host)
        .join(ScanJob, Host.job_id == ScanJob.id)
        .where(ScanJob.target_id == target_id)
    )
    hosts = hosts_result.scalars().all()

    seen_ips = set()
    for h in hosts:
        if h.ip_address in seen_ips:
            continue
        seen_ips.add(h.ip_address)

        host_node_id = f"host_{h.id}"
        nodes.append({
            "data": {
                "id":       host_node_id,
                "label":    h.hostname or h.ip_address,
                "type":     "host",
                "color":    "#10b981",
                "ip":       h.ip_address,
                "os":       h.os_fingerprint or "Unknown",
            }
        })
        edges.append({"data": {"source": f"target_{target_id}", "target": host_node_id}})

        # Get ports for this host
        ports_result = await db.execute(select(Port).where(Port.host_id == h.id))
        ports = ports_result.scalars().all()

        for p in ports:
            port_node_id = f"port_{h.id}_{p.port_number}"
            risk_color = _port_risk_color(p.port_number)
            nodes.append({
                "data": {
                    "id":      port_node_id,
                    "label":   f"Port {p.port_number}/{p.protocol} ({p.service_name or 'unknown'})",
                    "type":    "port_critical" if risk_color == "#ef4444" else "port",
                    "color":   risk_color,
                    "port":    p.port_number,
                    "service": p.service_name,
                    "version": p.version,
                }
            })
            edges.append({"data": {"source": host_node_id, "target": port_node_id}})

    # Get findings for this target
    findings_result = await db.execute(select(Finding).where(Finding.target_id == target_id))
    findings = findings_result.scalars().all()

    for f in findings:
        finding_node_id = f"finding_{f.id}"
        sev_color = {"critical": "#dc2626", "high": "#ef4444", "medium": "#f59e0b", "low": "#3b82f6", "info": "#6b7280"}.get(f.severity, "#6b7280")
        nodes.append({
            "data": {
                "id":       finding_node_id,
                "label":    f.title[:40] + ("…" if len(f.title) > 40 else ""),
                "type":     "finding",
                "color":    sev_color,
                "severity": f.severity,
                "category": f.category,
            }
        })
        edges.append({"data": {"source": f"target_{target_id}", "target": finding_node_id}})

    # Fallback: if no scan data yet, return an informative empty graph
    if len(nodes) == 1:
        nodes.append({
            "data": {
                "id":    "no_data",
                "label": "No scan data yet. Run a scan job first.",
                "type":  "info",
                "color": "#6b7280",
            }
        })
        edges.append({"data": {"source": f"target_{target_id}", "target": "no_data"}})

    return {
        "target_id":   target_id,
        "target_name": target.name,
        "total_nodes": len(nodes),
        "total_edges": len(edges),
        "elements": {
            "nodes": nodes,
            "edges": edges,
        }
    }


def _port_risk_color(port: int) -> str:
    """Returns a risk color based on port number."""
    critical = {21, 23, 445, 3389, 6379, 5900, 2375, 27017, 11211}
    high     = {22, 3306, 5432, 1433, 8080, 8443, 9200}
    if port in critical:
        return "#ef4444"
    if port in high:
        return "#f59e0b"
    return "#3b82f6"
