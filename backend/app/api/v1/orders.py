from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user, get_db, require_mutation_role
from app.core.constants import OrderStatus
from app.core.pagination import PaginatedResponse, PaginationParams
from app.models.user import User
from app.schemas.order import OrderCreate, OrderListItem, OrderRead
from app.services.order_service import OrderService

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("", response_model=PaginatedResponse[OrderListItem])
async def list_orders(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: OrderStatus | None = None,
    search: str | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    ordering: str = Query("-created_at"),
) -> PaginatedResponse[OrderListItem]:
    _ = current_user
    service = OrderService(db)
    return await service.list_orders(
        PaginationParams(page=page, page_size=page_size),
        status=status,
        search=search,
        date_from=date_from,
        date_to=date_to,
        ordering=ordering,
    )


@router.post("", response_model=OrderRead, status_code=201)
async def create_order(
    data: OrderCreate,
    current_user: Annotated[User, Depends(require_mutation_role)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> OrderRead:
    service = OrderService(db)
    return await service.create_order(data, current_user)


@router.get("/{order_id}", response_model=OrderRead)
async def get_order(
    order_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> OrderRead:
    _ = current_user
    service = OrderService(db)
    return await service.get_order(order_id)
