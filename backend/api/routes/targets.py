"""
scanet API — Target & Scope Management Routes
Handles CRUD operations for authorized scan targets.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import get_db

router = APIRouter()


@router.get("/", summary="List all authorized targets")
async def list_targets(db: AsyncSession = Depends(get_db)):
    """Returns all configured authorized scan targets."""
    # TODO: Implement target listing from database
    return {"targets": [], "total": 0}


@router.post("/", status_code=status.HTTP_201_CREATED, summary="Register a new target")
async def create_target(db: AsyncSession = Depends(get_db)):
    """
    Registers a new authorized scan target.
    Validates the target is within allowed private ranges.
    Blocks loopback, link-local, and cloud metadata addresses.
    """
    # TODO: Implement scope validation + target creation
    return {"message": "Target creation not yet implemented"}


@router.delete("/{target_id}", summary="Remove an authorized target")
async def delete_target(target_id: str, db: AsyncSession = Depends(get_db)):
    """De-registers an authorized target. All associated jobs remain for audit."""
    # TODO: Implement target deletion
    return {"message": f"Target {target_id} deletion not yet implemented"}
