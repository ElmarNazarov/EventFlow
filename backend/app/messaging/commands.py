import uuid
from typing import Any

from pydantic import BaseModel, Field

from app.core.constants import CommandType


class CommandMessage(BaseModel):
    command_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    command_type: CommandType
    order_id: int
    retry_count: int = 0
    metadata: dict[str, Any] = Field(default_factory=dict)

    def to_json(self) -> bytes:
        return self.model_dump_json().encode("utf-8")

    @classmethod
    def from_json(cls, data: bytes) -> "CommandMessage":
        return cls.model_validate_json(data)


def build_reserve_inventory_command(order_id: int, retry_count: int = 0) -> CommandMessage:
    return CommandMessage(
        command_type=CommandType.RESERVE_INVENTORY,
        order_id=order_id,
        retry_count=retry_count,
    )


def build_process_payment_command(order_id: int, retry_count: int = 0) -> CommandMessage:
    return CommandMessage(
        command_type=CommandType.PROCESS_PAYMENT,
        order_id=order_id,
        retry_count=retry_count,
    )


def build_create_shipping_command(order_id: int, retry_count: int = 0) -> CommandMessage:
    return CommandMessage(
        command_type=CommandType.CREATE_SHIPPING,
        order_id=order_id,
        retry_count=retry_count,
    )
