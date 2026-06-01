import enum
from decimal import Decimal


class UserRole(str, enum.Enum):
    ADMIN = "ADMIN"
    OPS_MANAGER = "OPS_MANAGER"
    SUPPORT = "SUPPORT"
    VIEWER = "VIEWER"


# Roles allowed to create/update resources (orders, inventory, etc.)
MUTATION_ROLES = {UserRole.ADMIN, UserRole.OPS_MANAGER}

# Roles allowed to manage users
USER_MANAGEMENT_ROLES = {UserRole.ADMIN}

# Roles that can view operational data
VIEW_ROLES = {UserRole.ADMIN, UserRole.OPS_MANAGER, UserRole.SUPPORT, UserRole.VIEWER}


class OrderStatus(str, enum.Enum):
    CREATED = "CREATED"
    INVENTORY_PENDING = "INVENTORY_PENDING"
    INVENTORY_RESERVED = "INVENTORY_RESERVED"
    PAYMENT_PENDING = "PAYMENT_PENDING"
    PAYMENT_CONFIRMED = "PAYMENT_CONFIRMED"
    PAYMENT_FAILED = "PAYMENT_FAILED"
    SHIPPING_PENDING = "SHIPPING_PENDING"
    SHIPPED = "SHIPPED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    FAILED = "FAILED"


class ReservationStatus(str, enum.Enum):
    PENDING = "PENDING"
    RESERVED = "RESERVED"
    FAILED = "FAILED"
    RELEASED = "RELEASED"


class PaymentStatus(str, enum.Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"


class ShipmentStatus(str, enum.Enum):
    PENDING = "PENDING"
    CREATED = "CREATED"
    SHIPPED = "SHIPPED"
    FAILED = "FAILED"


# RabbitMQ command queues
QUEUE_RESERVE_INVENTORY = "reserve_inventory"
QUEUE_PROCESS_PAYMENT = "process_payment"
QUEUE_CREATE_SHIPPING = "create_shipping"
QUEUE_SEND_NOTIFICATION = "send_notification"

# Demo payment failure threshold (deterministic for tests)
PAYMENT_FAILURE_THRESHOLD = Decimal("5000")


class CommandType(str, enum.Enum):
    RESERVE_INVENTORY = "reserve_inventory"
    PROCESS_PAYMENT = "process_payment"
    CREATE_SHIPPING = "create_shipping"
    SEND_NOTIFICATION = "send_notification"
