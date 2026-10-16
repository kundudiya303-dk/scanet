"""
scanet API — Results & Analytics Routes
Real implementation: queries normalized hosts, ports, endpoints, and findings from SQLite.
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.connection import get_db
from database.models import Host, Port, Endpoint, Finding, ScanJob
from analyzers.sarif_exporter import export_to_sarif

router = APIRouter()


@router.get("/hosts", summary="Query discovered hosts and ports")
async def get_hosts(job_id: str = None, db: AsyncSession = Depends(get_db)):
    """Returns normalized host and port data across all completed jobs (or filtered by job_id)."""
    query = select(Host)
    if job_id:
        query = query.where(Host.job_id == job_id)
    query = query.order_by(Host.created_at.desc())

    result = await db.execute(query)
    hosts = result.scalars().all()

    output = []
    for h in hosts:
        # Load associated ports
        ports_result = await db.execute(select(Port).where(Port.host_id == h.id))
        ports = ports_result.scalars().all()
        output.append({
            "id":             h.id,
            "job_id":         h.job_id,
            "ip_address":     h.ip_address,
            "hostname":       h.hostname,
            "os_fingerprint": h.os_fingerprint,
            "status":         h.status,
            "created_at":     h.created_at.isoformat() if h.created_at else None,
            "ports": [
                {
                    "port_number":  p.port_number,
                    "protocol":     p.protocol,
                    "state":        p.state,
                    "service_name": p.service_name,
                    "product":      p.product,
                    "version":      p.version,
                }
                for p in ports
            ]
        })
    return {"hosts": output, "total": len(output)}


@router.get("/endpoints", summary="Query discovered HTTP endpoints")
async def get_endpoints(job_id: str = None, db: AsyncSession = Depends(get_db)):
    """Returns discovered HTTP routes, status codes, and titles."""
    query = select(Endpoint)
    if job_id:
        query = query.where(Endpoint.job_id == job_id)
    query = query.order_by(Endpoint.created_at.desc())

    result = await db.execute(query)
    endpoints = result.scalars().all()

    return {
        "endpoints": [
            {
                "id":             e.id,
                "job_id":         e.job_id,
                "url":            e.url,
                "status_code":    e.status_code,
                "content_length": e.content_length,
                "title":          e.title,
                "tech_stack":     e.tech_stack,
                "created_at":     e.created_at.isoformat() if e.created_at else None,
            }
            for e in endpoints
        ],
        "total": len(endpoints)
    }


@router.get("/findings", summary="Query security findings")
async def get_findings(
    job_id: str = None,
    severity: str = None,
    db: AsyncSession = Depends(get_db)
):
    """Returns normalized security findings, optionally filtered by job_id or severity."""
    query = select(Finding)
    if job_id:
        query = query.where(Finding.job_id == job_id)
    if severity:
        query = query.where(Finding.severity == severity.lower())
    query = query.order_by(Finding.created_at.desc())

    result = await db.execute(query)
    findings = result.scalars().all()

    return {
        "findings": [
            {
                "id":          f.id,
                "job_id":      f.job_id,
                "target_id":   f.target_id,
                "category":    f.category,
                "severity":    f.severity,
                "title":       f.title,
                "description": f.description,
                "evidence":    f.evidence,
                "remediation": f.remediation,
                "created_at":  f.created_at.isoformat() if f.created_at else None,
            }
            for f in findings
        ],
        "total": len(findings)
    }


@router.get("/diff", summary="Compare results between two scan jobs")
async def diff_results(job_a: str, job_b: str, db: AsyncSession = Depends(get_db)):
    """
    Computes a structured diff between two historical scan jobs.
    Returns added, removed, and changed hosts/ports.
    """
    async def get_job_host_ports(job_id: str):
        hosts_result = await db.execute(select(Host).where(Host.job_id == job_id))
        hosts = hosts_result.scalars().all()
        data = {}
        for h in hosts:
            ports_result = await db.execute(select(Port).where(Port.host_id == h.id))
            ports = ports_result.scalars().all()
            data[h.ip_address] = {
                p.port_number for p in ports if p.state == "open"
            }
        return data

    hosts_a = await get_job_host_ports(job_a)
    hosts_b = await get_job_host_ports(job_b)

    added_hosts   = [ip for ip in hosts_b if ip not in hosts_a]
    removed_hosts = [ip for ip in hosts_a if ip not in hosts_b]
    changed = []

    for ip in hosts_a:
        if ip in hosts_b:
            new_ports = hosts_b[ip] - hosts_a[ip]
            closed_ports = hosts_a[ip] - hosts_b[ip]
            if new_ports or closed_ports:
                changed.append({
                    "ip":           ip,
                    "ports_added":  sorted(list(new_ports)),
                    "ports_closed": sorted(list(closed_ports)),
                })

    return {
        "job_a":         job_a,
        "job_b":         job_b,
        "added_hosts":   added_hosts,
        "removed_hosts": removed_hosts,
        "changed":       changed,
    }


@router.get("/export/{format}", summary="Export scan results")
async def export_results(
    format: str,
    job_id: str = None,
    db: AsyncSession = Depends(get_db)
):
    """Export results in: json | sarif | pptx | ppt"""
    supported = ["json", "sarif", "pptx", "ppt"]
    if format not in supported:
        raise HTTPException(status_code=400, detail=f"Unsupported format. Choose from: {supported}")

    # Gather findings
    query = select(Finding)
    if job_id:
        query = query.where(Finding.job_id == job_id)
    result = await db.execute(query)
    findings = result.scalars().all()

    findings_data = [
        {
            "id":          f.id,
            "template_id": f.category,
            "name":        f.title,
            "title":       f.title,
            "severity":    f.severity,
            "description": f.description,
            "matched_at":  f.evidence or "",
            "remediation": f.remediation or "",
        }
        for f in findings
    ]

    if format == "sarif":
        return export_to_sarif(
            job_id=job_id or "all",
            target="multiple",
            findings=findings_data,
        )

    if format in ["pptx", "ppt"]:
        from fastapi.responses import Response
        from analyzers.ppt_exporter import generate_scan_presentation

        # Gather hosts and ports
        hq = select(Host)
        if job_id:
            hq = hq.where(Host.job_id == job_id)
        h_res = await db.execute(hq)
        hosts = h_res.scalars().all()

        hosts_data = []
        for h in hosts:
            pq = select(Port).where(Port.host_id == h.id)
            p_res = await db.execute(pq)
            ports = p_res.scalars().all()
            hosts_data.append({
                "ip_address": h.ip_address,
                "hostname": h.hostname,
                "os_fingerprint": h.os_fingerprint,
                "ports": [
                    {
                        "port_number": p.port_number,
                        "protocol": p.protocol,
                        "service_name": p.service_name,
                        "product": p.product,
                        "version": p.version,
                    }
                    for p in ports
                ]
            })

        ppt_stream = generate_scan_presentation(
            target_name="Automated Network Assessment",
            hosts=hosts_data,
            findings=findings_data
        )

        return Response(
            content=ppt_stream.getvalue(),
            media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            headers={"Content-Disposition": "attachment; filename=scanet_security_report.pptx"}
        )

    return JSONResponse(content={"job_id": job_id, "findings": findings_data, "total": len(findings_data)})
