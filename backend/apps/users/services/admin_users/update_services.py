from __future__ import annotations

from datetime import datetime
from typing import Any

from apps.users.constants.lifecycle import UserStatus
from apps.users.models import User
from apps.users.selectors.admin_user_selectors import actor_can_access_admin_user
from apps.users.services.admin_users.audit_services import (
    log_admin_user_email_changed,
    log_admin_user_updated,
)
from apps.users.tasks.email_tasks import send_email_verification_task
from django.db import IntegrityError, transaction
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from rest_framework.exceptions import PermissionDenied, ValidationError

ADMIN_USER_EDITABLE_FIELDS = [
    "first_name",
    "last_name",
    "middle_name",
    "birth_date",
    "phone",
    "backup_email",
    "is_login_allowed",
    "account_managed_by",
]
"""
Поля пользователя, которые можно редактировать через административный раздел.

Важно:
    status, роли, is_staff, is_superuser и lifecycle-поля здесь не меняются.
    Для них есть отдельные сервисы и endpoint'ы.
"""


def validate_admin_can_update_user(*, actor, target_user: User) -> None:
    """
    Проверяет, может ли администратор редактировать пользователя.

    Args:
        actor:
            Администратор, который выполняет действие.
        target_user:
            Пользователь, которого редактируют.

    Raises:
        PermissionDenied: Если пользователь недоступен администратору.
    """

    if not actor_can_access_admin_user(actor=actor, target_user=target_user):
        raise PermissionDenied(
            "Пользователь не найден или недоступен для текущего администратора."
        )


def validate_target_user_can_be_updated(*, target_user: User) -> None:
    """
    Проверяет, можно ли редактировать пользователя.

    Args:
        target_user:
            Пользователь, которого редактируют.

    Raises:
        ValidationError: Если пользователь находится в финальном состоянии.
    """

    if target_user.status == UserStatus.ANONYMIZED or target_user.anonymized_at:
        raise ValidationError(
            {
                "status": "Нельзя редактировать анонимизированного пользователя.",
            }
        )

    if (
        target_user.status == UserStatus.SCHEDULED_FOR_DELETION
        or target_user.scheduled_for_deletion_at
    ):
        raise ValidationError(
            {
                "status": (
                    "Нельзя редактировать пользователя, который запланирован "
                    "к удалению. Сначала восстановите пользователя."
                )
            }
        )


def validate_admin_user_expected_updated_at(
    *,
    target_user: User,
    expected_updated_at: str | datetime = "",
) -> None:
    """
    Проверяет optimistic locking по updated_at.

    Если frontend передал expected_updated_at и он не совпадает с текущим
    updated_at пользователя, значит запись уже изменил другой администратор.

    Args:
        target_user:
            Пользователь из базы данных.
        expected_updated_at:
            Значение updated_at, которое видел frontend.

    Raises:
        ValidationError: Если дата некорректна или пользователь уже изменён.
    """

    if not expected_updated_at:
        return

    parsed_expected_updated_at = (
        expected_updated_at
        if isinstance(expected_updated_at, datetime)
        else parse_datetime(expected_updated_at)
    )

    if parsed_expected_updated_at is None:
        raise ValidationError(
            {
                "expected_updated_at": "Некорректный формат даты обновления.",
            }
        )

    current_updated_at = target_user.updated_at

    if timezone.is_naive(parsed_expected_updated_at):
        parsed_expected_updated_at = timezone.make_aware(
            parsed_expected_updated_at,
            timezone.get_current_timezone(),
        )

    if timezone.is_naive(current_updated_at):
        current_updated_at = timezone.make_aware(
            current_updated_at,
            timezone.get_current_timezone(),
        )

    if current_updated_at != parsed_expected_updated_at:
        raise ValidationError(
            {
                "expected_updated_at": (
                    "Пользователь уже был изменён другим администратором. "
                    "Обновите страницу и повторите действие."
                )
            }
        )


def normalize_admin_user_update_data(*, data: dict[str, Any]) -> dict[str, Any]:
    """
    Очищает payload редактирования пользователя.

    Args:
        data:
            Данные из serializer'а или request.data.

    Returns:
        dict[str, Any]: Данные, разрешённые для обновления.
    """

    normalized_data = {}

    for field in ADMIN_USER_EDITABLE_FIELDS:
        if field in data:
            normalized_data[field] = data[field]

    if "email" in data:
        normalized_data["email"] = data["email"]

    return normalized_data


def apply_admin_user_regular_fields(
    *,
    target_user: User,
    data: dict[str, Any],
) -> list[str]:
    """
    Применяет обычные редактируемые поля пользователя.

    Args:
        target_user:
            Пользователь, которого редактируют.
        data:
            Очищенные данные обновления.

    Returns:
        list[str]: Список изменённых полей.
    """

    changed_fields = []

    for field in ADMIN_USER_EDITABLE_FIELDS:
        if field not in data:
            continue

        old_value = getattr(target_user, field)
        new_value = data[field]

        if old_value == new_value:
            continue

        setattr(target_user, field, new_value)
        changed_fields.append(field)

    return changed_fields


def apply_admin_user_email_change(
    *,
    target_user: User,
    new_email: str | None,
) -> tuple[bool, str, str]:
    """
    Применяет изменение email пользователя.

    После изменения email пользователь снова должен подтвердить почту.

    Args:
        target_user:
            Пользователь, которому меняют email.
        new_email:
            Новый email.

    Returns:
        tuple[bool, str, str]:
            changed, old_email, normalized_new_email.
    """

    if new_email is None:
        return False, "", ""

    normalized_new_email = new_email.strip().lower()
    old_email = target_user.email

    if old_email == normalized_new_email:
        return False, old_email, normalized_new_email

    target_user.email = normalized_new_email
    target_user.is_email_verified = False
    target_user.email_verified_at = None
    target_user.status = UserStatus.PENDING_EMAIL
    target_user.is_active = True

    return True, old_email, normalized_new_email


def get_admin_user_update_fields(
    *,
    changed_fields: list[str],
    email_changed: bool,
) -> list[str]:
    """
    Формирует список полей для user.save(update_fields=...).

    Args:
        changed_fields:
            Обычные изменённые поля.
        email_changed:
            Был ли изменён email.

    Returns:
        list[str]: Поля для сохранения.
    """

    update_fields = list(changed_fields)

    if email_changed:
        update_fields.extend(
            [
                "email",
                "is_email_verified",
                "email_verified_at",
                "status",
                "is_active",
            ]
        )

    if update_fields:
        update_fields.append("updated_at")

    return list(dict.fromkeys(update_fields))


def schedule_admin_email_verification_if_needed(
    *,
    target_user: User,
    email_changed: bool,
) -> None:
    """
    Планирует отправку письма подтверждения email после commit.

    Args:
        target_user:
            Пользователь.
        email_changed:
            Был ли изменён email.
    """

    if not email_changed:
        return

    transaction.on_commit(
        lambda: send_email_verification_task.delay(user_id=target_user.id)
    )


def save_admin_user_update(
    *,
    target_user: User,
    update_fields: list[str],
) -> None:
    """
    Валидирует и сохраняет пользователя.

    Args:
        target_user:
            Пользователь, которого нужно сохранить.
        update_fields:
            Список изменённых полей.

    Raises:
        ValidationError: Если модель не прошла валидацию или нарушена уникальность.
    """

    if not update_fields:
        return

    try:
        target_user.full_clean()
        target_user.save(update_fields=update_fields)
    except IntegrityError as error:
        raise ValidationError(
            {
                "detail": (
                    "Не удалось сохранить пользователя. Возможно, email или "
                    "телефон уже используются другим пользователем."
                )
            }
        ) from error


@transaction.atomic
def admin_update_user(
    *,
    actor,
    target_user: User,
    data: dict[str, Any],
    expected_updated_at: str = "",
    reason: str = "",
    request=None,
) -> User:
    """
    Обновляет пользователя из административного раздела.

    Этот сервис отвечает только за редактирование базовых данных пользователя.
    Статусы, роли, блокировка, архивирование и удаление меняются отдельными
    сервисами.

    Args:
        actor:
            Администратор, который редактирует пользователя.
        target_user:
            Пользователь, которого редактируют.
        data:
            Данные обновления.
        expected_updated_at:
            Значение updated_at для защиты от одновременного редактирования.
        reason:
            Причина изменения.
        request:
            HTTP-запрос.

    Returns:
        User: Обновлённый пользователь.

    Raises:
        PermissionDenied: Если нет прав.
        ValidationError: Если данные некорректны.
    """

    locked_user = User.objects.select_for_update().get(id=target_user.id)

    validate_admin_can_update_user(
        actor=actor,
        target_user=locked_user,
    )
    validate_target_user_can_be_updated(
        target_user=locked_user,
    )
    validate_admin_user_expected_updated_at(
        target_user=locked_user,
        expected_updated_at=expected_updated_at,
    )

    normalized_data = normalize_admin_user_update_data(data=data)

    email_changed, old_email, new_email = apply_admin_user_email_change(
        target_user=locked_user,
        new_email=normalized_data.get("email"),
    )
    changed_fields = apply_admin_user_regular_fields(
        target_user=locked_user,
        data=normalized_data,
    )

    update_fields = get_admin_user_update_fields(
        changed_fields=changed_fields,
        email_changed=email_changed,
    )

    save_admin_user_update(
        target_user=locked_user,
        update_fields=update_fields,
    )

    if changed_fields:
        log_admin_user_updated(
            actor=actor,
            target_user=locked_user,
            changed_fields=changed_fields,
            reason=reason,
            request=request,
        )

    if email_changed:
        log_admin_user_email_changed(
            actor=actor,
            target_user=locked_user,
            old_email=old_email,
            new_email=new_email,
            reason=reason,
            request=request,
        )

    schedule_admin_email_verification_if_needed(
        target_user=locked_user,
        email_changed=email_changed,
    )

    return locked_user
