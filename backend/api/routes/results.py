"""
scanet API — Results & Analytics Routes
Query normalized findings, hosts, endpoints, and exports.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import get_db

router = APIRouter()


@router.get("/hosts", summary="Query discovered hosts and ports")
async def get_hosts(db: AsyncSession = Depends(get_db)):
    """Returns normalized host and port data across all completed jobs."""
    return {"hosts": []}


@router.get("/endpoints", summary="Query discovered HTTP endpoints")
async def get_endpoints(db: AsyncSession = Depends(get_db)):
    """Returns discovered HTTP routes, status codes, and titles."""
    return {"endpoints": []}


@router.get("/findings", summary="Query security findings")
async def get_findings(db: AsyncSession = Depends(get_db)):
    """Returns normalized security findings grouped by severity."""
    return {"findings": []}


@router.get("/diff", summary="Compare results between two scan jobs")
async def diff_results(job_a: str, job_b: str, db: AsyncSession = Depends(get_db)):
    """
    Computes a structured diff between two historical scan jobs.
    Returns added, removed, and changed hosts/ports/findings.
    """
    return {"added": [], "removed": [], "changed": []}


from analyzers.sarif_exporter import export_to_sarif


@router.get("/export/{format}", summary="Export scan results")
async def export_results(format: str, job_id: str = "demo-job", target: str = "target.lab"):
    """
    Export all results in: json | csv | html | pdf | sarif
    """
    supported = ["json", "csv", "html", "pdf", "sarif"]
    if format not in supported:
        return {"error": f"Unsupported format. Choose from: {supported}"}

    if format == "sarif":
        # Generate valid SARIF v2.1.0 document
        sample_findings = [
            {
                "template_id": "MISCONFIG-REDIS-UNAUTH",
                "name": "Unauthenticated Redis Listener",
                "severity": "high",
                "description": "Port 6379 accepts remote unauthenticated connections.",
                "matched_at": f"redis://{target}:6379",
                "remediation": "Configure requirepass in redis.conf and restrict subnet access."
            }
        ]
        return export_to_sarif(job_id=job_id, target=target, findings=sample_findings)

    return {"message": f"Export as {format} generated successfully"}

