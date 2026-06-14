from __future__ import annotations

BACKOFFICE_USER_EDITABLE_FIELDS = {
    "email",
    "backup_email",
    "phone",
    "first_name",
    "last_name",
    "middle_name",
    "birth_date",
    "is_login_allowed",
    "account_managed_by",
}
"""Поля пользователя, которые можно менять через backoffice update."""

BACKOFFICE_USER_SERVICE_ONLY_FIELDS = {
    "expected_updated_at",
    "reason",
}
"""Служебные поля serializer, которые не пишутся напрямую в User."""

BACKOFFICE_USER_LOCKING_FIELD = "expected_updated_at"
"""Поле optimistic locking для защиты от одновременного редактирования."""

BACKOFFICE_USER_REASON_FIELD = "reason"
"""Поле причины административного действия."""

BACKOFFICE_USER_LIST_SEARCH_FIELDS = (
    "email",
    "first_name",
    "last_name",
    "middle_name",
    "phone",
)
"""Поля поиска в административном списке пользователей."""

BACKOFFICE_USER_DEFAULT_ORDERING = (
    "-created_at",
    "-id",
)
"""Сортировка пользователей по умолчанию в backoffice."""

BACKOFFICE_USER_AUDIT_LIMIT = 20
"""Количество последних audit-записей пользователя в detail serializer."""

BACKOFFICE_USER_BULK_MAX_ITEMS = 100
"""Максимальное количество пользователей в одной bulk-операции."""
