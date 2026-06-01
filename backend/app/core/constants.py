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
