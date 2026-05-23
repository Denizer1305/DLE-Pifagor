from __future__ import annotations

from apps.users.constants.onboarding import InviteCodePurpose
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_invite_code_required(raw_code: str) -> None:
    """
    Проверяет, что код приглашения передан.

    Args:
        raw_code:
            Открытый код приглашения.

    Raises:
        ValidationError: Если код не передан.
    """

    if not raw_code:
        raise ValidationError(_("Код приглашения обязателен."))


def validate_invite_code_purpose(purpose: str) -> None:
    """
    Проверяет назначение кода приглашения.

    Args:
        purpose:
            Назначение кода.

    Raises:
        ValidationError: Если назначение кода недопустимо.
    """

    if purpose not in InviteCodePurpose.values:
        raise ValidationError(_("Недопустимое назначение кода приглашения."))


def validate_invite_code_context(
    *,
    purpose: str,
    organization=None,
    group=None,
    target_user=None,
) -> None:
    """
    Проверяет минимальный контекст кода приглашения.

    Args:
        purpose:
            Назначение кода.
        organization:
            Образовательная организация.
        group:
            Учебная группа.
        target_user:
            Целевой пользователь.

    Raises:
        ValidationError: Если контекст кода некорректен.
    """

    validate_invite_code_purpose(purpose)

    if purpose == InviteCodePurpose.TEACHER_REGISTRATION and organization is None:
        raise ValidationError(
            _(
                "Для кода регистрации преподавателя требуется образовательная организация."
            )
        )

    if purpose == InviteCodePurpose.GUARDIAN_LINK_CURATOR and group is None:
        raise ValidationError(_("Для кода куратора требуется учебная группа."))

    if purpose == InviteCodePurpose.GUARDIAN_LINK_LEARNER and target_user is None:
        raise ValidationError(_("Для кода учащегося требуется целевой пользователь."))
