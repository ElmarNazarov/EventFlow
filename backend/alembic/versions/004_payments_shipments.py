"""payments and shipments tables

Revision ID: 004
Revises: 003
Create Date: 2026-06-02

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "004"
down_revision: Union[str, None] = "003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "payments",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("order_id", sa.Integer(), nullable=False),
        sa.Column("amount", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("currency", sa.String(length=3), nullable=False),
        sa.Column(
            "status",
            sa.Enum("PENDING", "CONFIRMED", "FAILED", "REFUNDED", name="payment_status", native_enum=False),
            nullable=False,
        ),
        sa.Column("provider", sa.String(length=50), nullable=False),
        sa.Column("provider_reference", sa.String(length=100), nullable=True),
        sa.Column("failure_reason", sa.Text(), nullable=True),
        sa.Column("processed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["order_id"], ["orders.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("order_id"),
    )
    op.create_index(op.f("ix_payments_order_id"), "payments", ["order_id"], unique=True)
    op.create_index(op.f("ix_payments_status"), "payments", ["status"], unique=False)

    op.create_table(
        "shipments",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("order_id", sa.Integer(), nullable=False),
        sa.Column(
            "status",
            sa.Enum("PENDING", "CREATED", "SHIPPED", "FAILED", name="shipment_status", native_enum=False),
            nullable=False,
        ),
        sa.Column("carrier", sa.String(length=100), nullable=False),
        sa.Column("tracking_number", sa.String(length=100), nullable=True),
        sa.Column("shipping_address", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["order_id"], ["orders.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("order_id"),
    )
    op.create_index(op.f("ix_shipments_order_id"), "shipments", ["order_id"], unique=True)
    op.create_index(op.f("ix_shipments_tracking_number"), "shipments", ["tracking_number"], unique=False)
    op.create_index(op.f("ix_shipments_status"), "shipments", ["status"], unique=False)


def downgrade() -> None:
    op.drop_table("shipments")
    op.drop_table("payments")
