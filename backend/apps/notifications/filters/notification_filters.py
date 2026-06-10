"""
Фильтры уведомлений.

Файл содержит функции фильтрации queryset уведомлений по query-параметрам API.
Фильтры вынесены отдельно, чтобы views оставались тонкими.
"""

from __future__ import annotations


def apply_notification_filters(*, queryset, filters: dict):
    """
    Применяет фильтры к queryset уведомлений.

    Поддерживаемые фильтры:
    - unread_only;
    - status;
    - level;
    - category;
    - notification_type;
    - source_type;
    - source_id.
    """

    queryset = apply_unread_filter(
        queryset=queryset,
        unread_only=filters.get("unread_only", False),
    )
    queryset = apply_status_filter(
        queryset=queryset,
        status=filters.get("status", ""),
    )
    queryset = apply_level_filter(
        queryset=queryset,
        level=filters.get("level", ""),
    )
    queryset = apply_category_filter(
        queryset=queryset,
        category=filters.get("category", ""),
    )
    queryset = apply_type_filter(
        queryset=queryset,
        notification_type=filters.get("notification_type", ""),
    )
    queryset = apply_source_filter(
        queryset=queryset,
        source_type=filters.get("source_type", ""),
        source_id=filters.get("source_id", ""),
    )

    return queryset


def apply_unread_filter(*, queryset, unread_only: bool):
    """
    Фильтрует queryset только по непрочитанным уведомлениям.
    """

    if not unread_only:
        return queryset

    return queryset.unread()


def apply_status_filter(*, queryset, status: str):
    """
    Фильтрует queryset по статусу уведомления.
    """

    if not status:
        return queryset

    return queryset.by_status(status)


def apply_level_filter(*, queryset, level: str):
    """
    Фильтрует queryset по уровню важности.
    """

    if not level:
        return queryset

    return queryset.by_level(level)


def apply_category_filter(*, queryset, category: str):
    """
    Фильтрует queryset по категории уведомления.
    """

    if not category:
        return queryset

    return queryset.by_category(category)


def apply_type_filter(*, queryset, notification_type: str):
    """
    Фильтрует queryset по типу уведомления.
    """

    if not notification_type:
        return queryset

    return queryset.by_type(notification_type)


def apply_source_filter(
    *,
    queryset,
    source_type: str,
    source_id: str,
):
    """
    Фильтрует queryset по источнику уведомления.
    """

    if not source_type and not source_id:
        return queryset

    return queryset.by_source(
        source_type=source_type,
        source_id=source_id,
    )
