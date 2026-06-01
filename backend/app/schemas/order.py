from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.constants import OrderStatus
from app.schemas.common import EmailStrLocal


class OrderItemCreate(BaseModel):
    sku: str = Field(min_length=1, max_length=100)
    quantity: int = Field(gt=0)
    unit_price: Decimal | None = Field(default=None, gt=0)


class OrderCreate(BaseModel):
    customer_name: str = Field(min_length=1, max_length=255)
    customer_email: EmailStrLocal
    currency: str = Field(default="USD", min_length=3, max_length=3)
    items: list[OrderItemCreate] = Field(min_length=1)

    @field_validator("currency")
    @classmethod
    def uppercase_currency(cls, value: str) -> str:
        return value.upper()


class OrderItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    sku: str
    product_name: str
    quantity: int
    unit_price: Decimal
    total_price: Decimal
    created_at: datetime


class OrderRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_number: str
    customer_name: str
    customer_email: str
    status: OrderStatus
    total_amount: Decimal
    currency: str
    created_by_id: int
    created_at: datetime
    updated_at: datetime
    items: list[OrderItemRead] = []


class OrderListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_number: str
    customer_name: str
    customer_email: str
    status: OrderStatus
    total_amount: Decimal
    currency: str
    created_at: datetime
    updated_at: datetime
