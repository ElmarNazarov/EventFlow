from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.core.constants import ReservationStatus


class InventoryItemCreate(BaseModel):
    sku: str = Field(min_length=1, max_length=100)
    name: str = Field(min_length=1, max_length=255)
    available_quantity: int = Field(ge=0)
    reorder_level: int = Field(default=0, ge=0)
    is_active: bool = True


class InventoryItemUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    available_quantity: int | None = Field(default=None, ge=0)
    reorder_level: int | None = Field(default=None, ge=0)
    is_active: bool | None = None


class InventoryItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    sku: str
    name: str
    available_quantity: int
    reserved_quantity: int
    reorder_level: int
    is_active: bool
    created_at: datetime
    updated_at: datetime


class InventoryReservationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_id: int
    sku: str
    quantity: int
    status: ReservationStatus
    created_at: datetime
    updated_at: datetime
