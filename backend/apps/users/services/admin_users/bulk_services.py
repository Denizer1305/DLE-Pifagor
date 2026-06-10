from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from uuid import uuid4

from apps.users.models import User
from apps.users.selectors.admin_user_selectors import get_admin_users_queryset_for_actor
from apps.users.services.admin_users.delete_services import admin_schedule_user_deletion
from apps.users.services.admin_users.role_services import admin_change_user_roles
from apps.users.services.admin_users.status_services import (
    admin_archive_user,
    admin_block_user,
    admin_restore_user,
    admin_unblock_user,
)
from django.db import transaction
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from rest_framework.exceptions import PermissionDenied, ValidationError


class AdminUserBulkAction:
    """
    Действия массового управления пользователями.

    Используется сервисным слоем и будущим serializer'ом.
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


@dataclass
class AdminUserBulkItemResult:
    """
    Результат обработки одного пользователя в bulk-операции.

    Attributes:
        user_id:
            ID пользователя.
        success:
            Успешно ли выполнено действие.
        message:
            Человекочитаемое сообщение.
        error_code:
            Машинный код ошибки.
    """

    user_id: int
    success: bool
    message: str = ""
    error_code: str = ""


@dataclass
class AdminUserBulkResult:
    """
    Итог массового административного действия.

    Attributes:
        bulk_action_id:
            ID массовой операции.
        action:
            Код выполненного действия.
        total_count:
            Сколько пользователей было передано.
        success_count:
            Сколько пользователей успешно обработано.
        failed_count:
            Сколько пользователей не удалось обработать.
        items:
            Результаты по каждому пользователю.
    """

    bulk_action_id: str
    action: str
    total_count: int
    success_count: int
    failed_count: int
    items: list[AdminUserBulkItemResult]

    def to_dict(self) -> dict:
        """
        Преобразует результат bulk-операции в словарь.

        Returns:
            dict: Сериализуемый результат bulk-операции.
        """

        return {
            "bulk_action_id": self.bulk_action_id,
            "action": self.action,
            "total_count": self.total_count,
            "success_count": self.success_count,
            "failed_count": self.failed_count,
            "items": [asdict(item) for item in self.items],
        }


def validate_bulk_action(*, action: str) -> None:
    """
    Проверяет, поддерживается ли массовое действие.

    Args:
        action:
            Код массового действия.

    Raises:
        ValidationError: Если действие не поддерживается.
    """

    if action not in AdminUserBulkAction.CHOICES:
        raise ValidationError(
            {
                "action": "Неподдерживаемое массовое действие.",
            }
        )


def normalize_bulk_user_ids(*, user_ids: list[int]) -> list[int]:
    """
    Нормализует список ID пользователей для массовой операции.

    Args:
        user_ids:
            Список ID пользователей.

    Returns:
        list[int]: Уникальные ID пользователей с сохранением порядка.

    Raises:
        ValidationError: Если список пустой.
    """

    normalized_user_ids = []
    seen_user_ids = set()

    for user_id in user_ids or []:
        if not user_id:
            continue

        if user_id in seen_user_ids:
            continue

        seen_user_ids.add(user_id)
        normalized_user_ids.append(user_id)

    if not normalized_user_ids:
        raise ValidationError(
            {
                "user_ids": "Необходимо выбрать хотя бы одного пользователя.",
            }
        )

    return normalized_user_ids


def get_expected_updated_at_for_user(
    *,
    expected_updated_at_by_user_id: dict | None,
    user_id: int,
) -> str:
    """
    Возвращает ожидаемый updated_at для конкретного пользователя.

    Args:
        expected_updated_at_by_user_id:
            Словарь вида {user_id: expected_updated_at}.
        user_id:
            ID пользователя.

    Returns:
        str: Ожидаемая дата обновления или пустая строка.
    """

    if not expected_updated_at_by_user_id:
        return ""

    return (
        expected_updated_at_by_user_id.get(user_id)
        or expected_updated_at_by_user_id.get(str(user_id))
        or ""
    )


def validate_expected_updated_at(
    *,
    user: User,
    expected_updated_at: str | datetime = "",
) -> None:
    """
    Проверяет optimistic locking по updated_at.

    Если frontend передал expected_updated_at и он не совпадает с текущим
    user.updated_at, значит пользователя уже изменил другой администратор.

    Args:
        user:
            Пользователь из базы.
        expected_updated_at:
            Значение updated_at, которое видел frontend.

    Raises:
        ValidationError: Если пользователь был изменён другим администратором.
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

    current_updated_at = user.updated_at

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
                ),
            }
        )


def get_locked_admin_user_for_bulk_action(
    *,
    actor,
    user_id: int,
) -> User:
    """
    Возвращает пользователя с блокировкой строки в БД.

    Args:
        actor:
            Администратор, который выполняет массовое действие.
        user_id:
            ID целевого пользователя.

    Returns:
        User: Заблокированная строка пользователя.

    Raises:
        PermissionDenied: Если пользователь недоступен администратору.
    """

    user = (
        get_admin_users_queryset_for_actor(actor=actor)
        .select_for_update()
        .filter(id=user_id)
        .first()
    )

    if user is None:
        raise PermissionDenied(
            "Пользователь не найден или недоступен для текущего администратора."
        )

    return user


def perform_admin_user_bulk_item_action(
    *,
    action: str,
    actor,
    target_user: User,
    reason: str = "",
    role_payload: dict | None = None,
    bulk_action_id: str = "",
    request=None,
) -> User:
    """
    Выполняет массовое действие над одним пользователем.

    Args:
        action:
            Код массового действия.
        actor:
            Администратор.
        target_user:
            Целевой пользователь.
        reason:
            Причина действия.
        role_payload:
            Данные для изменения ролей.
        bulk_action_id:
            ID массовой операции.
        request:
            HTTP-запрос.

    Returns:
        User: Обновлённый пользователь.

    Raises:
        ValidationError: Если действие невозможно выполнить.
    """

    role_payload = role_payload or {}

    if action == AdminUserBulkAction.BLOCK:
        return admin_block_user(
            actor=actor,
            target_user=target_user,
            reason=reason,
            bulk_action_id=bulk_action_id,
            request=request,
        )

    if action == AdminUserBulkAction.UNBLOCK:
        return admin_unblock_user(
            actor=actor,
            target_user=target_user,
            reason=reason,
            bulk_action_id=bulk_action_id,
            request=request,
        )

    if action == AdminUserBulkAction.ARCHIVE:
        return admin_archive_user(
            actor=actor,
            target_user=target_user,
            reason=reason,
            bulk_action_id=bulk_action_id,
            request=request,
        )

    if action == AdminUserBulkAction.RESTORE:
        return admin_restore_user(
            actor=actor,
            target_user=target_user,
            reason=reason,
            bulk_action_id=bulk_action_id,
            request=request,
        )

    if action == AdminUserBulkAction.DELETE:
        return admin_schedule_user_deletion(
            actor=actor,
            target_user=target_user,
            reason=reason,
            bulk_action_id=bulk_action_id,
            request=request,
        )

    if action == AdminUserBulkAction.CHANGE_ROLES:
        admin_change_user_roles(
            actor=actor,
            target_user=target_user,
            assigned_roles=role_payload.get("assigned_roles", []),
            revoked_user_role_ids=role_payload.get("revoked_user_role_ids", []),
            reason=reason,
            bulk_action_id=bulk_action_id,
            request=request,
        )

        return target_user

    raise ValidationError(
        {
            "action": "Неподдерживаемое массовое действие.",
        }
    )


def execute_admin_user_bulk_item(
    *,
    action: str,
    actor,
    user_id: int,
    reason: str = "",
    role_payload: dict | None = None,
    expected_updated_at: str = "",
    bulk_action_id: str = "",
    request=None,
) -> AdminUserBulkItemResult:
    """
    Выполняет bulk-действие над одним пользователем.

    Каждая запись обрабатывается в отдельной транзакции, чтобы ошибка по одному
    пользователю не откатывала всю массовую операцию.

    Args:
        action:
            Код массового действия.
        actor:
            Администратор.
        user_id:
            ID целевого пользователя.
        reason:
            Причина действия.
        role_payload:
            Данные для изменения ролей.
        expected_updated_at:
            Значение updated_at для optimistic locking.
        bulk_action_id:
            ID массовой операции.
        request:
            HTTP-запрос.

    Returns:
        AdminUserBulkItemResult: Результат обработки одного пользователя.
    """

    try:
        with transaction.atomic():
            target_user = get_locked_admin_user_for_bulk_action(
                actor=actor,
                user_id=user_id,
            )

            validate_expected_updated_at(
                user=target_user,
                expected_updated_at=expected_updated_at,
            )

            perform_admin_user_bulk_item_action(
                action=action,
                actor=actor,
                target_user=target_user,
                reason=reason,
                role_payload=role_payload,
                bulk_action_id=bulk_action_id,
                request=request,
            )

        return AdminUserBulkItemResult(
            user_id=user_id,
            success=True,
            message="Действие выполнено.",
        )

    except PermissionDenied as error:
        return AdminUserBulkItemResult(
            user_id=user_id,
            success=False,
            message=str(error.detail if hasattr(error, "detail") else error),
            error_code="permission_denied",
        )

    except ValidationError as error:
        return AdminUserBulkItemResult(
            user_id=user_id,
            success=False,
            message=str(error.detail if hasattr(error, "detail") else error),
            error_code="validation_error",
        )

    except Exception as error:
        return AdminUserBulkItemResult(
            user_id=user_id,
            success=False,
            message=str(error),
            error_code="unknown_error",
        )


def execute_admin_users_bulk_action(
    *,
    action: str,
    actor,
    user_ids: list[int],
    reason: str = "",
    role_payload: dict | None = None,
    expected_updated_at_by_user_id: dict | None = None,
    request=None,
) -> AdminUserBulkResult:
    """
    Выполняет массовое административное действие над пользователями.

    Поддерживаемые действия:
        - block;
        - unblock;
        - archive;
        - restore;
        - delete;
        - change_roles.

    Args:
        action:
            Код массового действия.
        actor:
            Администратор, который выполняет действие.
        user_ids:
            Список ID пользователей.
        reason:
            Причина массового действия.
        role_payload:
            Данные для массового изменения ролей.
        expected_updated_at_by_user_id:
            Словарь optimistic locking вида {user_id: updated_at}.
        request:
            HTTP-запрос.

    Returns:
        AdminUserBulkResult: Итог массового действия.

    Raises:
        ValidationError: Если action или user_ids некорректны.
    """

    validate_bulk_action(action=action)

    normalized_user_ids = normalize_bulk_user_ids(
        user_ids=user_ids,
    )

    bulk_action_id = str(uuid4())
    items = []

    for user_id in normalized_user_ids:
        expected_updated_at = get_expected_updated_at_for_user(
            expected_updated_at_by_user_id=expected_updated_at_by_user_id,
            user_id=user_id,
        )

        item_result = execute_admin_user_bulk_item(
            action=action,
            actor=actor,
            user_id=user_id,
            reason=reason,
            role_payload=role_payload,
            expected_updated_at=expected_updated_at,
            bulk_action_id=bulk_action_id,
            request=request,
        )

        items.append(item_result)

    success_count = sum(1 for item in items if item.success)
    failed_count = len(items) - success_count

    return AdminUserBulkResult(
        bulk_action_id=bulk_action_id,
        action=action,
        total_count=len(items),
        success_count=success_count,
        failed_count=failed_count,
        items=items,
    )
