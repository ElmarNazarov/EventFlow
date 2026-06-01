import enum


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
