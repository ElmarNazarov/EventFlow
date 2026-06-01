from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user, get_db, require_mutation_role
from app.core.pagination import PaginatedResponse, PaginationParams
from app.models.user import User
from app.schemas.inventory import InventoryItemCreate, InventoryItemRead, InventoryItemUpdate
from app.services.inventory_service import InventoryService

router = APIRouter(prefix="/inventory", tags=["inventory"])


@router.get("", response_model=PaginatedResponse[InventoryItemRead])
async def list_inventory(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = None,
    active_only: bool = False,
) -> PaginatedResponse[InventoryItemRead]:
    _ = current_user
    service = InventoryService(db)
    return await service.list_items(
        PaginationParams(page=page, page_size=page_size),
        search=search,
        active_only=active_only,
    )


@router.post("", response_model=InventoryItemRead, status_code=201)
async def create_inventory_item(
    data: InventoryItemCreate,
    current_user: Annotated[User, Depends(require_mutation_role)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> InventoryItemRead:
    _ = current_user
    service = InventoryService(db)
    return await service.create_item(data)


@router.patch("/{inventory_id}", response_model=InventoryItemRead)
async def update_inventory_item(
    inventory_id: int,
    data: InventoryItemUpdate,
    current_user: Annotated[User, Depends(require_mutation_role)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> InventoryItemRead:
    _ = current_user
    service = InventoryService(db)
    return await service.update_item(inventory_id, data)
