from __future__ import annotations


class BackofficeUserAction:
    """
    Action-имена административного ViewSet управления пользователями.

    Эти значения совпадают с DRF action names и используются
    для выбора serializer, permissions и логики viewset.
    """

    LIST = "list"
    RETRIEVE = "retrieve"
    CREATE = "create"
    UPDATE = "update"
    PARTIAL_UPDATE = "partial_update"
    DESTROY = "destroy"

    BLOCK = "block"
    UNBLOCK = "unblock"
    ARCHIVE = "archive"
    RESTORE = "restore"
    CHANGE_ROLES = "change_roles"
    BULK = "bulk"
    AVAILABLE_ROLES = "available_roles"
    AUDIT_LOGS = "audit_logs"


BACKOFFICE_USER_DETAIL_ACTIONS = {
    BackofficeUserAction.RETRIEVE,
    BackofficeUserAction.UPDATE,
    BackofficeUserAction.PARTIAL_UPDATE,
    BackofficeUserAction.DESTROY,
}
"""Actions, которые работают с конкретным пользователем."""


BACKOFFICE_USER_STATUS_ACTIONS = {
    BackofficeUserAction.BLOCK,
    BackofficeUserAction.UNBLOCK,
    BackofficeUserAction.ARCHIVE,
    BackofficeUserAction.RESTORE,
}
"""Actions изменения статуса пользователя."""


BACKOFFICE_USER_ROLE_ACTIONS = {
    BackofficeUserAction.CHANGE_ROLES,
    BackofficeUserAction.AVAILABLE_ROLES,
}
"""Actions управления ролями пользователя."""


BACKOFFICE_USER_READ_ACTIONS = {
    BackofficeUserAction.LIST,
    BackofficeUserAction.RETRIEVE,
    BackofficeUserAction.AVAILABLE_ROLES,
    BackofficeUserAction.AUDIT_LOGS,
}
"""Actions чтения в административном контуре пользователей."""


class BackofficeUserBulkAction:
    """
    Действия массового управления пользователями.
    """

    BLOCK = "block"
    UNBLOCK = "unblock"
    ARCHIVE = "archive"
    RESTORE = "restore"
    DELETE = "delete"
    CHANGE_ROLES = "change_roles"

    CHOICES = {
        BLOCK,
        UNBLOCK,
        ARCHIVE,
        RESTORE,
        DELETE,
        CHANGE_ROLES,
    }


BACKOFFICE_USER_BULK_ACTION_CHOICES = (
    (BackofficeUserBulkAction.BLOCK, "Заблокировать"),
    (BackofficeUserBulkAction.UNBLOCK, "Разблокировать"),
    (BackofficeUserBulkAction.ARCHIVE, "Архивировать"),
    (BackofficeUserBulkAction.RESTORE, "Восстановить"),
    (BackofficeUserBulkAction.DELETE, "Удалить"),
    (BackofficeUserBulkAction.CHANGE_ROLES, "Изменить роли"),
)
"""Choices для serializer массового управления пользователями."""


# Временный совместимый alias для переноса старого AdminUserBulkAction.
AdminUserBulkAction = BackofficeUserBulkAction
