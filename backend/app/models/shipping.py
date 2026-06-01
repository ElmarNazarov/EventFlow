from sqlalchemy import Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.constants import ShipmentStatus
from app.models.base import Base, TimestampMixin


class Shipment(Base, TimestampMixin):
    __tablename__ = "shipments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"), unique=True, index=True
    )
    status: Mapped[ShipmentStatus] = mapped_column(
        Enum(ShipmentStatus, name="shipment_status", native_enum=False),
        nullable=False,
        default=ShipmentStatus.PENDING,
        index=True,
    )
    carrier: Mapped[str] = mapped_column(String(100), nullable=False, default="EventFlow Logistics")
    tracking_number: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    shipping_address: Mapped[str] = mapped_column(Text, nullable=False, default="")
