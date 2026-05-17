from __future__ import annotations

from apps.core.utils import hash_value
from apps.users.constants.onboarding import InviteCodePurpose
from apps.users.models import InviteCode
from django.db.models import QuerySet


def get_invite_codes_queryset() -> QuerySet:
    """
    Возвращает базовый QuerySet кодов приглашения.

    Returns:
        QuerySet: Коды приглашения.
    """

    return InviteCode.objects.select_related(
        "organization",
        "department",
        "group",
        "created_by",
        "target_user",
    )


def get_active_invite_codes_queryset() -> QuerySet:
    """
    Возвращает активные коды приглашения.

    Returns:
        QuerySet: Активные коды.
    """

    return get_invite_codes_queryset().filter(is_active=True)


def get_available_invite_codes_queryset() -> QuerySet:
    """
    Возвращает коды, доступные для использования.

    Returns:
        QuerySet: Доступные коды.
    """

    return InviteCode.objects.available().select_related(
        "organization",
        "department",
        "group",
        "created_by",
        "target_user",
    )


def get_invite_code_by_hash(code_hash: str):
    """
    Возвращает код приглашения по хешу.

    Args:
        code_hash:
            Хеш кода.

    Returns:
        InviteCode | None: Код приглашения или None.
    """

    if not code_hash:
        return None

    return get_invite_codes_queryset().filter(code_hash=code_hash).first()


def get_available_invite_code_by_raw_code(raw_code: str):
    """
    Возвращает доступный код приглашения по открытому коду.

    Args:
        raw_code:
            Открытый код, введённый пользователем.

    Returns:
        InviteCode | None: Доступный код приглашения или None.
    """

    if not raw_code:
        return None

    code_hash = hash_value(raw_code)

    return get_available_invite_codes_queryset().filter(code_hash=code_hash).first()


def get_teacher_registration_codes_for_organization(organization) -> QuerySet:
    """
    Возвращает коды регистрации преподавателей для организации.

    Args:
        organization:
            Образовательная организация.

    Returns:
        QuerySet: Коды регистрации преподавателей.
    """

    if not organization:
        return InviteCode.objects.none()

    return get_invite_codes_queryset().filter(
        organization=organization,
        purpose=InviteCodePurpose.TEACHER_REGISTRATION,
    )


def get_guardian_curator_codes_for_group(group) -> QuerySet:
    """
    Возвращает коды куратора для подтверждения связи родителя и учащегося.

    Args:
        group:
            Учебная группа.

    Returns:
        QuerySet: Коды куратора для группы.
    """

    if not group:
        return InviteCode.objects.none()

    return get_invite_codes_queryset().filter(
        group=group,
        purpose=InviteCodePurpose.GUARDIAN_LINK_CURATOR,
    )


def get_guardian_learner_codes_for_user(user) -> QuerySet:
    """
    Возвращает коды учащегося для подтверждения связи с родителем.

    Args:
        user:
            Учащийся.

    Returns:
        QuerySet: Коды учащегося.
    """

    if not user:
        return InviteCode.objects.none()

    return get_invite_codes_queryset().filter(
        target_user=user,
        purpose=InviteCodePurpose.GUARDIAN_LINK_LEARNER,
    )
