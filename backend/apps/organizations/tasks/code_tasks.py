from __future__ import annotations

from apps.organizations.models import Organization, StudyGroup
from django.utils import timezone


def disable_expired_teacher_registration_codes() -> int:
    """
    Отключает истёкшие коды регистрации преподавателей.

    Returns:
        int: Количество обновлённых организаций.
    """

    now = timezone.now()

    updated_count = Organization.objects.filter(
        teacher_registration_code_is_active=True,
        teacher_registration_code_expires_at__isnull=False,
        teacher_registration_code_expires_at__lte=now,
    ).update(
        teacher_registration_code_is_active=False,
        updated_at=now,
    )

    return updated_count


def disable_expired_group_join_codes() -> int:
    """
    Отключает истёкшие коды вступления в группы.

    Returns:
        int: Количество обновлённых групп.
    """

    now = timezone.now()

    updated_count = StudyGroup.objects.filter(
        join_code_is_active=True,
        join_code_expires_at__isnull=False,
        join_code_expires_at__lte=now,
    ).update(
        join_code_is_active=False,
        updated_at=now,
    )

    return updated_count


def disable_expired_organization_codes() -> dict[str, int]:
    """
    Отключает все истёкшие коды модуля organizations.

    Returns:
        dict[str, int]: Статистика обновлений.
    """

    teacher_codes_count = disable_expired_teacher_registration_codes()
    group_codes_count = disable_expired_group_join_codes()

    return {
        "teacher_registration_codes": teacher_codes_count,
        "group_join_codes": group_codes_count,
    }