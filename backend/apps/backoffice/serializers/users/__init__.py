from __future__ import annotations

from .audit import BackofficeUserAuditLogListSerializer
from .bulk import (
    BackofficeUserBulkItemResultSerializer,
    BackofficeUserBulkResultSerializer,
    BackofficeUserBulkSerializer,
)
from .delete import BackofficeUserDeleteSerializer
from .detail import BackofficeUserDetailSerializer
from .list import BackofficeUserListSerializer
from .related import (
    BackofficeUserRoleSerializer,
    build_backoffice_related_object_payload,
    get_active_user_roles,
)
from .roles import (
    BackofficeUserAvailableRoleSerializer,
    BackofficeUserChangeRolesSerializer,
    BackofficeUserRoleAssignmentSerializer,
)
from .status import BackofficeUserStatusActionSerializer
from .write import BackofficeUserUpdateSerializer

# Совместимые alias'ы на время переноса старой admin-user логики.
AdminUserAuditLogListSerializer = BackofficeUserAuditLogListSerializer
AdminUserAvailableRoleSerializer = BackofficeUserAvailableRoleSerializer
AdminUserBulkItemResultSerializer = BackofficeUserBulkItemResultSerializer
AdminUserBulkResultSerializer = BackofficeUserBulkResultSerializer
AdminUserBulkSerializer = BackofficeUserBulkSerializer
AdminUserChangeRolesSerializer = BackofficeUserChangeRolesSerializer
AdminUserDeleteSerializer = BackofficeUserDeleteSerializer
AdminUserDetailSerializer = BackofficeUserDetailSerializer
AdminUserListSerializer = BackofficeUserListSerializer
AdminUserRoleAssignmentSerializer = BackofficeUserRoleAssignmentSerializer
AdminUserRoleSerializer = BackofficeUserRoleSerializer
AdminUserStatusActionSerializer = BackofficeUserStatusActionSerializer
AdminUserUpdateSerializer = BackofficeUserUpdateSerializer
build_admin_related_object_payload = build_backoffice_related_object_payload

__all__ = [
    "AdminUserAuditLogListSerializer",
    "AdminUserAvailableRoleSerializer",
    "AdminUserBulkItemResultSerializer",
    "AdminUserBulkResultSerializer",
    "AdminUserBulkSerializer",
    "AdminUserChangeRolesSerializer",
    "AdminUserDeleteSerializer",
    "AdminUserDetailSerializer",
    "AdminUserListSerializer",
    "AdminUserRoleAssignmentSerializer",
    "AdminUserRoleSerializer",
    "AdminUserStatusActionSerializer",
    "AdminUserUpdateSerializer",
    "BackofficeUserAuditLogListSerializer",
    "BackofficeUserAvailableRoleSerializer",
    "BackofficeUserBulkItemResultSerializer",
    "BackofficeUserBulkResultSerializer",
    "BackofficeUserBulkSerializer",
    "BackofficeUserChangeRolesSerializer",
    "BackofficeUserDeleteSerializer",
    "BackofficeUserDetailSerializer",
    "BackofficeUserListSerializer",
    "BackofficeUserRoleAssignmentSerializer",
    "BackofficeUserRoleSerializer",
    "BackofficeUserStatusActionSerializer",
    "BackofficeUserUpdateSerializer",
    "build_admin_related_object_payload",
    "build_backoffice_related_object_payload",
    "get_active_user_roles",
]
