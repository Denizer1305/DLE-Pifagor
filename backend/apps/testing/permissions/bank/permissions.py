from __future__ import annotations

from apps.testing.constants import BankItemStatus, BankItemVisibility
from apps.testing.permissions.shared import (
    is_authenticated_user,
    is_teacher,
    is_testing_admin,
)
from rest_framework.permissions import SAFE_METHODS, BasePermission


class QuestionBankItemPermission(BasePermission):
    """
    Ограничение доступа к шаблонам вопросов банка тестовых заданий.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет доступ к списку и созданию шаблонов.
        """

        user = request.user

        if not is_authenticated_user(user=user):
            return False

        if request.method in SAFE_METHODS:
            return True

        return is_testing_admin(user=user) or is_teacher(user=user)

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет доступ к конкретному шаблону вопроса.
        """

        user = request.user

        if request.method in SAFE_METHODS:
            return _user_can_read_bank_item(
                user=user,
                bank_item=obj,
            )

        return _user_can_manage_bank_item(
            user=user,
            bank_item=obj,
        )


class QuestionBankOptionPermission(BasePermission):
    """
    Ограничение доступа к вариантам шаблонов вопросов.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет доступ к списку и созданию вариантов.
        """

        user = request.user

        if not is_authenticated_user(user=user):
            return False

        if request.method in SAFE_METHODS:
            return True

        return is_testing_admin(user=user) or is_teacher(user=user)

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет доступ к конкретному варианту шаблона.
        """

        user = request.user

        if request.method in SAFE_METHODS:
            return _user_can_read_bank_item(
                user=user,
                bank_item=obj.bank_item,
            )

        return _user_can_manage_bank_item(
            user=user,
            bank_item=obj.bank_item,
        )


class QuestionBankStatusPermission(BasePermission):
    """
    Ограничение для публикации, архивации и восстановления шаблона.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет общий доступ к status actions.
        """

        user = request.user

        return is_testing_admin(user=user) or is_teacher(user=user)

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет право менять статус шаблона.
        """

        return _user_can_manage_bank_item(
            user=request.user,
            bank_item=obj,
        )


def _user_can_read_bank_item(*, user, bank_item) -> bool:
    """
    Проверяет, может ли пользователь читать шаблон вопроса.
    """

    if is_testing_admin(user=user):
        return True

    if bank_item.owner_teacher_id == user.id:
        return True

    if bank_item.status != BankItemStatus.PUBLISHED:
        return False

    if not bank_item.is_active:
        return False

    if bank_item.visibility == BankItemVisibility.PUBLIC:
        return True

    if bank_item.visibility == BankItemVisibility.ORGANIZATION:
        return _user_belongs_to_bank_item_organization(
            user=user,
            bank_item=bank_item,
        )

    return False


def _user_can_manage_bank_item(*, user, bank_item) -> bool:
    """
    Проверяет, может ли пользователь изменять шаблон вопроса.
    """

    if is_testing_admin(user=user):
        return True

    if not is_teacher(user=user):
        return False

    return bank_item.owner_teacher_id == user.id


def _user_belongs_to_bank_item_organization(*, user, bank_item) -> bool:
    """
    Проверяет совпадение организации пользователя и шаблона.

    Используем мягкую проверку, чтобы не завязаться жёстко
    на конкретную реализацию профиля пользователя.
    """

    user_organization_id = getattr(user, "organization_id", None)

    if user_organization_id is not None:
        return user_organization_id == bank_item.organization_id

    profile = getattr(user, "profile", None)

    if profile is None:
        return False

    profile_organization_id = getattr(profile, "organization_id", None)

    return profile_organization_id == bank_item.organization_id
