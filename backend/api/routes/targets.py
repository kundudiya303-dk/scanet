"""
scanet API — Target & Scope Management Routes
Real CRUD implementation with SQLite persistence and scope validation.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from database.connection import get_db
from database.models import Target, new_uuid
from engine.scope_validator import ScopeValidator
from pydantic import BaseModel
from typing import Optional
import json

router = APIRouter()


class TargetCreateRequest(BaseModel):
    name: str
    value: str                      # IP, CIDR, or domain
    target_type: str                # 'ip', 'cidr', 'domain'
    notes: Optional[str] = None
    created_by: Optional[str] = "admin"


@router.get("/", summary="List all authorized targets")
async def list_targets(db: AsyncSession = Depends(get_db)):
    """Returns all configured authorized scan targets from the database."""
    result = await db.execute(select(Target).order_by(Target.created_at.desc()))
    targets = result.scalars().all()
    return {
        "targets": [
            {
                "id":          t.id,
                "name":        t.name,
                "value":       t.value,
                "target_type": t.target_type,
                "is_approved": t.is_approved,
                "notes":       t.notes,
                "created_by":  t.created_by,
                "created_at":  t.created_at.isoformat() if t.created_at else None,
            }
            for t in targets
        ],
        "total": len(targets)
    }


@router.post("/", status_code=status.HTTP_201_CREATED, summary="Register a new target")
async def create_target(body: TargetCreateRequest, db: AsyncSession = Depends(get_db)):
    """
    Registers a new authorized scan target.
    Validates the target against hard-blocked ranges before persisting.
    """
    # Scope validation
    valid, reason = ScopeValidator.validate(body.value)
    if not valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Scope validation failed: {reason}"
        )

    # Check for duplicates
    existing = await db.execute(select(Target).where(Target.value == body.value.strip().lower()))
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Target '{body.value}' is already registered."
        )

    target = Target(
        id=new_uuid(),
        name=body.name,
        value=body.value.strip().lower(),
        target_type=body.target_type,
        notes=body.notes,
        created_by=body.created_by or "admin",
        is_approved=True,
    )
    db.add(target)
    await db.commit()
    await db.refresh(target)

    return {
        "message":     "Target registered successfully.",
        "target_id":   target.id,
        "name":        target.name,
        "value":       target.value,
        "target_type": target.target_type,
        "is_approved": target.is_approved,
        "created_at":  target.created_at.isoformat() if target.created_at else None,
    }


@router.delete("/{target_id}", summary="Remove an authorized target")
async def delete_target(target_id: str, db: AsyncSession = Depends(get_db)):
    """De-registers an authorized target. All associated jobs remain for audit history."""
    result = await db.execute(select(Target).where(Target.id == target_id))
    target = result.scalar_one_or_none()
    if not target:
        raise HTTPException(status_code=404, detail=f"Target '{target_id}' not found.")

    await db.execute(delete(Target).where(Target.id == target_id))
    await db.commit()
    return {"message": f"Target '{target.name}' ({target.value}) removed successfully."}


@router.get("/{target_id}", summary="Get a single target by ID")
async def get_target(target_id: str, db: AsyncSession = Depends(get_db)):
    """Returns metadata for a single target."""
    result = await db.execute(select(Target).where(Target.id == target_id))
    target = result.scalar_one_or_none()
    if not target:
        raise HTTPException(status_code=404, detail=f"Target '{target_id}' not found.")
    return {
        "id":          target.id,
        "name":        target.name,
        "value":       target.value,
        "target_type": target.target_type,
        "is_approved": target.is_approved,
        "notes":       target.notes,
        "created_by":  target.created_by,
        "created_at":  target.created_at.isoformat() if target.created_at else None,
    }
