from __future__ import annotations

from apps.organizations.selectors import (
    actor_has_department_admin_access,
    actor_has_organization_admin_access,
    is_authenticated_active_actor,
    is_superadmin_actor,
)
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsActiveAuthenticatedUser(BasePermission):
    """
    Разрешает доступ только активному авторизованному пользователю.
    """

    message = "Необходимо быть авторизованным активным пользователем."

    def has_permission(self, request, view) -> bool:
        """
        Проверяет доступ к endpoint'у.

        Args:
            request:
                DRF request.
            view:
                DRF view.

        Returns:
            bool: True, если доступ разрешён.
        """

        return is_authenticated_active_actor(actor=request.user)


class CanAccessOrganizationsAdmin(BasePermission):
    """
    Базовое право доступа к административному разделу организаций.

    Подходит для list/retrieve административных endpoint'ов.
    """

    message = "Нет доступа к административному разделу организаций."

    def has_permission(self, request, view) -> bool:
        """
        Проверяет общий доступ к админке организаций.
        """

        user = request.user

        if not is_authenticated_active_actor(actor=user):
            return False

        if is_superadmin_actor(actor=user):
            return True

        return (
            actor_has_organization_admin_access(actor=user)
            or actor_has_department_admin_access(actor=user)
        )


class CanManageOrganizations(BasePermission):
    """
    Право управления образовательными организациями.

    Создание и изменение организаций разрешаем только суперадмину
    и администраторам организаций.
    """

    message = "Нет прав на управление образовательными организациями."

    def has_permission(self, request, view) -> bool:
        """
        Проверяет доступ к управлению организациями.
        """

        user = request.user

        if not is_authenticated_active_actor(actor=user):
            return False

        if request.method in SAFE_METHODS:
            return CanAccessOrganizationsAdmin().has_permission(request, view)

        return actor_has_organization_admin_access(actor=user)


class CanManageDepartments(BasePermission):
    """
    Право управления отделениями.
    """

    message = "Нет прав на управление отделениями."

    def has_permission(self, request, view) -> bool:
        """
        Проверяет доступ к управлению отделениями.
        """

        user = request.user

        if not is_authenticated_active_actor(actor=user):
            return False

        if request.method in SAFE_METHODS:
            return CanAccessOrganizationsAdmin().has_permission(request, view)

        return (
            actor_has_organization_admin_access(actor=user)
            or actor_has_department_admin_access(actor=user)
        )


class CanManageStudyGroups(BasePermission):
    """
    Право управления учебными группами.
    """

    message = "Нет прав на управление учебными группами."

    def has_permission(self, request, view) -> bool:
        """
        Проверяет доступ к управлению учебными группами.
        """

        user = request.user

        if not is_authenticated_active_actor(actor=user):
            return False

        if request.method in SAFE_METHODS:
            return CanAccessOrganizationsAdmin().has_permission(request, view)

        return (
            actor_has_organization_admin_access(actor=user)
            or actor_has_department_admin_access(actor=user)
        )


class CanManageTeacherOrganizations(BasePermission):
    """
    Право управления связями преподавателей с организациями.
    """

    message = "Нет прав на управление преподавателями организации."

    def has_permission(self, request, view) -> bool:
        """
        Проверяет доступ к управлению преподавателями организации.
        """

        user = request.user

        if not is_authenticated_active_actor(actor=user):
            return False

        if request.method in SAFE_METHODS:
            return CanAccessOrganizationsAdmin().has_permission(request, view)

        return actor_has_organization_admin_access(actor=user)


class CanManageGroupCurators(BasePermission):
    """
    Право управления кураторами учебных групп.
    """

    message = "Нет прав на управление кураторами групп."

    def has_permission(self, request, view) -> bool:
        """
        Проверяет доступ к управлению кураторами групп.
        """

        user = request.user

        if not is_authenticated_active_actor(actor=user):
            return False

        if request.method in SAFE_METHODS:
            return CanAccessOrganizationsAdmin().has_permission(request, view)

        return (
            actor_has_organization_admin_access(actor=user)
            or actor_has_department_admin_access(actor=user)
        )


class CanManageOrganizationCodes(BasePermission):
    """
    Право управления кодами организации и групп.

    Сюда относятся:
        - код регистрации преподавателя;
        - код вступления в группу.
    """

    message = "Нет прав на управление кодами организации или группы."

    def has_permission(self, request, view) -> bool:
        """
        Проверяет доступ к управлению кодами.
        """

        user = request.user

        if not is_authenticated_active_actor(actor=user):
            return False

        return (
            actor_has_organization_admin_access(actor=user)
            or actor_has_department_admin_access(actor=user)
        )

class CanManageSubjects(BasePermission):
    """
    Право управления справочником учебных предметов.

    Предметы являются глобальным справочником, поэтому управлять ими
    могут суперадминистратор, администратор организации и директор.
    """

    message = "Нет прав на управление учебными предметами."

    def has_permission(self, request, view) -> bool:
        """
        Проверяет доступ к управлению учебными предметами.

        Args:
            request:
                DRF request.
            view:
                DRF view.

        Returns:
            bool: True, если доступ разрешён.
        """

        user = request.user

        if not is_authenticated_active_actor(actor=user):
            return False

        if request.method in SAFE_METHODS:
            return CanAccessOrganizationsAdmin().has_permission(request, view)

        return actor_has_organization_admin_access(actor=user)


class CanManageTeacherSubjects(BasePermission):
    """
    Право управления предметами преподавателей.

    Связи преподавателей с предметами могут менять суперадминистратор,
    администратор организации и директор.
    """

    message = "Нет прав на управление предметами преподавателей."

    def has_permission(self, request, view) -> bool:
        """
        Проверяет доступ к управлению предметами преподавателей.

        Args:
            request:
                DRF request.
            view:
                DRF view.

        Returns:
            bool: True, если доступ разрешён.
        """

        user = request.user

        if not is_authenticated_active_actor(actor=user):
            return False

        if request.method in SAFE_METHODS:
            return CanAccessOrganizationsAdmin().has_permission(request, view)

        return actor_has_organization_admin_access(actor=user)