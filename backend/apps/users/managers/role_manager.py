from __future__ import annotations

from apps.users.constants.lifecycle import UserRoleStatus
from apps.users.constants.roles import ROLE_LABELS, ROLE_SORT_ORDER, RoleCode
from django.db import models


class RoleQuerySet(models.QuerySet):
    """
    QuerySet для справочника ролей.
    """

    def active(self):
        """
        Возвращает активные роли.

        Returns:
            QuerySet: Активные роли.
        """

        return self.filter(is_active=True)

    def system(self):
        """
        Возвращает системные роли.

        Returns:
            QuerySet: Системные роли.
        """

        return self.filter(is_system=True)

    def by_code(self, code: str):
        """
        Ищет роль по системному коду.

        Args:
            code:
                Код роли.

        Returns:
            QuerySet: Роль с указанным кодом.
        """

        if not code:
            return self.none()

        return self.filter(code=code)


class RoleManager(models.Manager.from_queryset(RoleQuerySet)):
    """
    Менеджер справочника ролей.

    Содержит вспомогательные методы для создания и синхронизации
    системных ролей проекта.
    """

    def get_by_code(self, code: str):
        """
        Возвращает роль по коду.

        Args:
            code:
                Код роли.

        Returns:
            Role: Найденная роль.
        """

        return self.get(code=code)

    def ensure_system_roles(self) -> list:
        """
        Создаёт или обновляет системные роли из RoleCode.

        Используется в management command или data migration,
        чтобы справочник ролей всегда соответствовал коду.

        Returns:
            list: Список созданных или обновлённых ролей.
        """

        synced_roles = []

        for role_code, role_label in RoleCode.choices:
            role, _created = self.update_or_create(
                code=role_code,
                defaults={
                    "label": ROLE_LABELS.get(role_code, role_label),
                    "is_system": True,
                    "is_active": True,
                    "sort_order": ROLE_SORT_ORDER.get(role_code, 100),
                },
            )
            synced_roles.append(role)

        return synced_roles


class UserRoleQuerySet(models.QuerySet):
    """
    QuerySet для назначенных ролей пользователей.
    """

    def active(self):
        """
        Возвращает активные назначенные роли.

        Returns:
            QuerySet: Активные роли пользователей.
        """

        return self.filter(status=UserRoleStatus.ACTIVE)

    def pending(self):
        """
        Возвращает роли, ожидающие подтверждения.

        Returns:
            QuerySet: Роли со статусом pending.
        """

        return self.filter(status=UserRoleStatus.PENDING)

    def rejected(self):
        """
        Возвращает отклонённые роли.

        Returns:
            QuerySet: Роли со статусом rejected.
        """

        return self.filter(status=UserRoleStatus.REJECTED)

    def revoked(self):
        """
        Возвращает отозванные роли.

        Returns:
            QuerySet: Роли со статусом revoked.
        """

        return self.filter(status=UserRoleStatus.REVOKED)

    def archived(self):
        """
        Возвращает архивные роли.

        Returns:
            QuerySet: Роли со статусом archived.
        """

        return self.filter(status=UserRoleStatus.ARCHIVED)

    def for_user(self, user):
        """
        Возвращает роли конкретного пользователя.

        Args:
            user:
                Пользователь.

        Returns:
            QuerySet: Роли пользователя.
        """

        return self.filter(user=user)

    def for_organization(self, organization):
        """
        Возвращает роли в рамках образовательной организации.

        Args:
            organization:
                Образовательная организация.

        Returns:
            QuerySet: Роли пользователей в организации.
        """

        return self.filter(organization=organization)

    def for_department(self, department):
        """
        Возвращает роли в рамках отделения.

        Args:
            department:
                Отделение.

        Returns:
            QuerySet: Роли пользователей в отделении.
        """

        return self.filter(department=department)

    def for_group(self, group):
        """
        Возвращает роли в рамках группы.

        Args:
            group:
                Учебная группа.

        Returns:
            QuerySet: Роли пользователей в группе.
        """

        return self.filter(group=group)

    def with_role_code(self, role_code: str):
        """
        Возвращает назначенные роли по коду роли.

        Args:
            role_code:
                Код роли.

        Returns:
            QuerySet: Назначенные роли с указанным кодом.
        """

        return self.filter(role__code=role_code)

    def reviewers_for_organization(self, organization):
        """
        Возвращает пользователей, которые могут рассматривать заявки организации.

        Args:
            organization:
                Образовательная организация.

        Returns:
            QuerySet: Активные роли проверяющих в организации.
        """

        from apps.users.constants.roles import ORGANIZATION_REVIEWER_ROLE_CODES

        return self.active().filter(
            organization=organization,
            role__code__in=ORGANIZATION_REVIEWER_ROLE_CODES,
        )


class UserRoleManager(models.Manager.from_queryset(UserRoleQuerySet)):
    """
    Менеджер назначенных ролей пользователей.
    """

    def user_has_active_role(
        self,
        *,
        user,
        role_code: str,
        organization=None,
        department=None,
        group=None,
    ) -> bool:
        """
        Проверяет, есть ли у пользователя активная роль в заданном контексте.

        Args:
            user:
                Пользователь.
            role_code:
                Код роли.
            organization:
                Образовательная организация.
            department:
                Отделение.
            group:
                Группа.

        Returns:
            bool: True, если активная роль найдена.
        """

        queryset = (
            self.get_queryset()
            .active()
            .filter(
                user=user,
                role__code=role_code,
            )
        )

        if organization is not None:
            queryset = queryset.filter(organization=organization)

        if department is not None:
            queryset = queryset.filter(department=department)

        if group is not None:
            queryset = queryset.filter(group=group)

        return queryset.exists()
