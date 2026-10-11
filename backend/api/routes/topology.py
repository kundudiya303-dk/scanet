"""
scanet API — Interactive Attack Surface Topology Graph
Builds graph nodes and edges for Cytoscape.js / D3 force-directed visualization:
Target -> Subdomains -> Hosts -> Open Ports -> CVE Findings.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import get_db
from typing import Dict, Any, List

router = APIRouter()


@router.get("/graph/{target_id}")
async def get_target_topology_graph(target_id: str):
    """
    Returns graph elements (nodes and edges) formatted for Cytoscape.js / D3:
    - Root Target Node
    - Host IP Nodes
    - Service / Port Nodes (color-coded by risk)
    - Vulnerability / Alert Nodes
    """
    # Sample structured graph model
    nodes = [
        {"data": {"id": f"target_{target_id}", "label": "Target Root", "type": "target", "color": "#6366f1"}},
        {"data": {"id": "sub_api", "label": "api.target.lab", "type": "subdomain", "color": "#06b6d4"}},
        {"data": {"id": "sub_web", "label": "www.target.lab", "type": "subdomain", "color": "#06b6d4"}},
        {"data": {"id": "host_1", "label": "192.168.1.100", "type": "host", "color": "#10b981"}},
        {"data": {"id": "port_80", "label": "Port 80/tcp (http)", "type": "port", "color": "#3b82f6"}},
        {"data": {"id": "port_443", "label": "Port 443/tcp (https)", "type": "port", "color": "#3b82f6"}},
        {"data": {"id": "port_6379", "label": "Port 6379/tcp (redis)", "type": "port_critical", "color": "#ef4444"}},
        {"data": {"id": "vuln_redis", "label": "Unauthenticated Redis", "type": "finding", "color": "#dc2626"}}
    ]

    edges = [
        {"data": {"source": f"target_{target_id}", "target": "sub_api"}},
        {"data": {"source": f"target_{target_id}", "target": "sub_web"}},
        {"data": {"source": "sub_api", "target": "host_1"}},
        {"data": {"source": "sub_web", "target": "host_1"}},
        {"data": {"source": "host_1", "target": "port_80"}},
        {"data": {"source": "host_1", "target": "port_443"}},
        {"data": {"source": "host_1", "target": "port_6379"}},
        {"data": {"source": "port_6379", "target": "vuln_redis"}}
    ]

    return {
        "target_id": target_id,
        "total_nodes": len(nodes),
        "total_edges": len(edges),
        "elements": {
            "nodes": nodes,
            "edges": edges
        }
    }
