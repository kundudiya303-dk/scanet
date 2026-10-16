"""
scanet API — Scan Job Orchestration Routes
Real implementation: queues jobs to the process job manager, persists to DB,
streams live output via SSE, and supports cancellation.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.connection import get_db
from database.models import ScanJob, Target, Host, Port, new_uuid
from engine.job_manager import job_manager
from engine.scope_validator import ScopeValidator
from engine.tool_registry import get_adapter
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone
import asyncio
import json

router = APIRouter()

# In-memory SSE output buffers: job_id -> list of output lines
_output_buffers: dict[str, list[str]] = {}
_job_done: dict[str, asyncio.Event] = {}


class JobCreateRequest(BaseModel):
    target_id: str
    tool_name: str
    profile_name: Optional[str] = "default"
    parameters: Optional[dict] = {}


@router.post("/", status_code=status.HTTP_201_CREATED, summary="Queue a new scan job")
async def create_job(body: JobCreateRequest, db: AsyncSession = Depends(get_db)):
    """
    Queues a new scan job for an approved target.
    Validates target scope, then dispatches to the process job manager as an async background task.
    """
    # 1. Load target from DB
    result = await db.execute(select(Target).where(Target.id == body.target_id))
    target = result.scalar_one_or_none()
    if not target:
        raise HTTPException(status_code=404, detail=f"Target '{body.target_id}' not found.")

    if not target.is_approved:
        raise HTTPException(status_code=403, detail="Target is not approved for scanning.")

    # 2. Scope re-validation
    valid, reason = ScopeValidator.validate(target.value)
    if not valid:
        raise HTTPException(status_code=400, detail=f"Scope validation failed: {reason}")

    # 3. Get tool adapter
    adapter = get_adapter(body.tool_name)
    if not adapter:
        raise HTTPException(status_code=400, detail=f"Unknown tool '{body.tool_name}'.")

    if not adapter.is_installed():
        raise HTTPException(
            status_code=503,
            detail=f"Tool '{body.tool_name}' is not installed on this system. Install it first."
        )

    # 4. Build command args
    params = body.parameters or {}
    cmd_args = adapter.build_command_args(target.value, params)

    # 5. Create DB job record
    job_id = new_uuid()
    job = ScanJob(
        id=job_id,
        target_id=target.id,
        tool_name=body.tool_name,
        profile_name=body.profile_name or "default",
        status="running",
        parameters=json.dumps(params),
        started_at=datetime.now(timezone.utc).replace(tzinfo=None),
    )
    db.add(job)
    await db.commit()

    # 6. Initialize SSE output buffer
    _output_buffers[job_id] = []
    done_event = asyncio.Event()
    _job_done[job_id] = done_event

    # 7. Dispatch in background (non-blocking)
    asyncio.create_task(
        _run_job_background(job_id, target.id, cmd_args, adapter, body.tool_name, done_event)
    )

    return {
        "message":    f"Scan job queued successfully.",
        "job_id":     job_id,
        "target":     target.value,
        "tool":       body.tool_name,
        "status":     "running",
        "command":    " ".join(cmd_args),
        "started_at": job.started_at.isoformat(),
    }


async def _run_job_background(
    job_id: str,
    target_id: str,
    cmd_args: list,
    adapter,
    tool_name: str,
    done_event: asyncio.Event,
):
    """Background coroutine: runs job, streams output, updates DB on finish."""
    from database.connection import AsyncSessionLocal
    buf = _output_buffers[job_id]

    async def on_line(line: str):
        buf.append(line)

    exit_code, full_output = await job_manager.execute_job(
        job_id=job_id,
        cmd_args=cmd_args,
        output_callback=on_line,
        timeout_seconds=600,
    )

    # Parse output and store results
    parsed = adapter.parse_output(full_output, exit_code)

    async with AsyncSessionLocal() as db:
        # Update job record
        result = await db.execute(select(ScanJob).where(ScanJob.id == job_id))
        job = result.scalar_one_or_none()
        if job:
            job.status = "completed" if exit_code == 0 else "failed"
            job.completed_at = datetime.now(timezone.utc).replace(tzinfo=None)
            job.exit_code = exit_code
            if exit_code != 0:
                job.error_message = f"Exit code {exit_code}"

            # Persist parsed hosts/ports for nmap-like adapters
            if tool_name == "nmap" and "hosts" in parsed:
                for h in parsed.get("hosts", []):
                    host_id = new_uuid()
                    host = Host(
                        id=host_id,
                        job_id=job_id,
                        ip_address=h.get("ip", "unknown"),
                        hostname=h.get("hostname"),
                        status="up",
                    )
                    db.add(host)
                    for p in h.get("ports", []):
                        db.add(Port(
                            id=new_uuid(),
                            host_id=host_id,
                            port_number=p.get("port", 0),
                            protocol=p.get("protocol", "tcp"),
                            state=p.get("state", "open"),
                            service_name=p.get("service", ""),
                            product=p.get("product", ""),
                            version=p.get("version", ""),
                        ))

            await db.commit()

    buf.append(f"[scanet-engine] Job {job_id} finished. Exit code: {exit_code}\n")
    done_event.set()
    _job_done.pop(job_id, None)


@router.get("/", summary="List all scan jobs")
async def list_jobs(db: AsyncSession = Depends(get_db)):
    """Returns all job history with status, tool name, and timing info."""
    result = await db.execute(
        select(ScanJob, Target.value, Target.name)
        .join(Target, ScanJob.target_id == Target.id, isouter=True)
        .order_by(ScanJob.started_at.desc())
    )
    rows = result.all()
    jobs = []
    for job, target_value, target_name in rows:
        jobs.append({
            "id":           job.id,
            "target_id":    job.target_id,
            "target_value": target_value,
            "target_name":  target_name,
            "tool_name":    job.tool_name,
            "profile_name": job.profile_name,
            "status":       job.status,
            "pid":          job.pid,
            "started_at":   job.started_at.isoformat() if job.started_at else None,
            "completed_at": job.completed_at.isoformat() if job.completed_at else None,
            "exit_code":    job.exit_code,
            "error_message":job.error_message,
        })
    return {"jobs": jobs, "total": len(jobs)}


@router.get("/{job_id}", summary="Get job details")
async def get_job(job_id: str, db: AsyncSession = Depends(get_db)):
    """Returns detailed status and metadata for a specific job."""
    result = await db.execute(
        select(ScanJob, Target.value, Target.name)
        .join(Target, ScanJob.target_id == Target.id, isouter=True)
        .where(ScanJob.id == job_id)
    )
    row = result.first()
    if not row:
        raise HTTPException(status_code=404, detail=f"Job '{job_id}' not found.")
    job, target_value, target_name = row
    return {
        "id":           job.id,
        "target_id":    job.target_id,
        "target_value": target_value,
        "target_name":  target_name,
        "tool_name":    job.tool_name,
        "profile_name": job.profile_name,
        "status":       job.status,
        "parameters":   json.loads(job.parameters) if job.parameters else {},
        "pid":          job.pid,
        "started_at":   job.started_at.isoformat() if job.started_at else None,
        "completed_at": job.completed_at.isoformat() if job.completed_at else None,
        "exit_code":    job.exit_code,
        "error_message":job.error_message,
    }


@router.post("/{job_id}/cancel", summary="Cancel a running job")
async def cancel_job(job_id: str, db: AsyncSession = Depends(get_db)):
    """
    Sends SIGTERM to the job's process group.
    Falls back to SIGKILL if the process does not terminate within 1 second.
    """
    cancelled = await job_manager.cancel_job(job_id)
    if not cancelled:
        # Mark as cancelled even if process was already done
        result = await db.execute(select(ScanJob).where(ScanJob.id == job_id))
        job = result.scalar_one_or_none()
        if not job:
            raise HTTPException(status_code=404, detail=f"Job '{job_id}' not found.")
        return {"message": f"Job '{job_id}' was not running or already finished.", "status": job.status}

    # Update DB status to cancelled
    result = await db.execute(select(ScanJob).where(ScanJob.id == job_id))
    job = result.scalar_one_or_none()
    if job:
        job.status = "cancelled"
        job.completed_at = datetime.now(timezone.utc).replace(tzinfo=None)
        await db.commit()

    return {"message": f"Job '{job_id}' cancelled successfully.", "status": "cancelled"}


@router.get("/{job_id}/stream", summary="Stream live job output (SSE)")
async def stream_job_output(job_id: str):
    """
    Server-Sent Events (SSE) endpoint.
    Streams real-time console output from the running scan process.
    Sends buffered lines first, then tails live output until job completes.
    """
    async def event_generator():
        sent = 0
        # Check if job exists in buffer
        if job_id not in _output_buffers:
            yield f"data: [scanet-engine] Job {job_id} not found or already completed. Check /api/v1/jobs/{job_id} for status.\n\n"
            return

        buf = _output_buffers[job_id]
        done_event = _job_done.get(job_id)

        while True:
            # Drain any new lines
            while sent < len(buf):
                line = buf[sent].rstrip("\n")
                yield f"data: {line}\n\n"
                sent += 1

            # If job is done and buffer fully drained, close stream
            if done_event and done_event.is_set() and sent >= len(buf):
                yield f"data: [scanet-engine] Stream complete.\n\n"
                break

            await asyncio.sleep(0.3)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )
