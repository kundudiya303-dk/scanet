"""
scanet API — Reconnaissance Pipelines & Playbooks
Manages chained, multi-stage automated scanning workflows.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import get_db
from engine.pipeline_manager import PipelineManager, PIPELINE_PRESETS
from engine.tool_registry import ToolRegistry
from typing import List, Dict, Any

router = APIRouter()


@router.get("/presets", response_model=List[Dict[str, Any]])
async def list_pipeline_presets():
    """
    Returns pre-configured multi-stage scanning pipelines:
    - Full Attack Surface Reconnaissance
    - Web Application Security Audit
    - Network Routing & Port Diagnostics
    - Stealth Passive OSINT Intelligence
    """
    return list(PIPELINE_PRESETS.values())


@router.get("/presets/{preset_id}")
async def get_pipeline_preset(preset_id: str):
    """
    Returns detailed stages and tool sequence for a specific pipeline.
    """
    if preset_id not in PIPELINE_PRESETS:
        raise HTTPException(status_code=404, detail=f"Pipeline preset '{preset_id}' not found")
    return PIPELINE_PRESETS[preset_id]


@router.post("/execute/{preset_id}")
async def execute_pipeline(preset_id: str, payload: dict, db: AsyncSession = Depends(get_db)):
    """
    Launches an automated multi-stage pipeline run against an authorized target.
    """
    if preset_id not in PIPELINE_PRESETS:
        raise HTTPException(status_code=404, detail="Unknown pipeline preset")
    
    target_id = payload.get("target_id")
    if not target_id:
        raise HTTPException(status_code=400, detail="target_id is required")

    from sqlalchemy import select
    from database.models import Target
    target_res = await db.execute(select(Target).where(Target.id == target_id))
    target = target_res.scalar_one_or_none()
    if not target:
        raise HTTPException(status_code=404, detail="Target not found in database")

    preset = PIPELINE_PRESETS[preset_id]
    return {
        "status": "initiated",
        "pipeline_id": preset_id,
        "pipeline_name": preset["name"],
        "target_id": target_id,
        "total_stages": len(preset["stages"]),
        "current_stage": preset["stages"][0]["tool"]
    }
