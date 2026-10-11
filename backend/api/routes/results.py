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


@router.get("/export/{format}", summary="Export scan results")
async def export_results(format: str):
    """
    Export all results in: json | csv | html | pdf | sarif
    """
    supported = ["json", "csv", "html", "pdf", "sarif"]
    if format not in supported:
        return {"error": f"Unsupported format. Choose from: {supported}"}
    # TODO: Implement multi-format report generation
    return {"message": f"Export as {format} not yet implemented"}
