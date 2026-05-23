from __future__ import annotations

from apps.users.models import RegistrationAttemptLog, UserAuditLog
from django.contrib import admin


@admin.register(UserAuditLog)
class UserAuditLogAdmin(admin.ModelAdmin):
    """
    Административная панель аудита действий пользователей.

    Аудит должен быть доступен для просмотра, но не для ручного редактирования.
    """

    list_display = (
        "id",
        "action",
        "actor",
        "actor_type",
        "target_user",
        "ip_address",
        "created_at",
    )
    list_filter = (
        "action",
        "actor_type",
        "created_at",
    )
    search_fields = (
        "actor__email",
        "actor__phone",
        "target_user__email",
        "target_user__phone",
        "message",
        "ip_address",
        "user_agent",
    )
    autocomplete_fields = (
        "actor",
        "target_user",
    )
    readonly_fields = (
        "actor",
        "actor_type",
        "target_user",
        "action",
        "message",
        "metadata",
        "ip_address",
        "user_agent",
        "created_at",
        "updated_at",
    )
    ordering = ("-created_at",)

    def has_add_permission(self, request) -> bool:
        """
        Запрещает ручное создание записей аудита.

        Args:
            request:
                HTTP-запрос администратора.

        Returns:
            bool: False.
        """

        return False

    def has_change_permission(self, request, obj=None) -> bool:
        """
        Запрещает ручное изменение записей аудита.

        Args:
            request:
                HTTP-запрос администратора.
            obj:
                Запись аудита.

        Returns:
            bool: False для конкретного объекта, иначе стандартное право просмотра списка.
        """

        if obj is not None:
            return False

        return super().has_change_permission(request, obj=obj)

    def has_delete_permission(self, request, obj=None) -> bool:
        """
        Запрещает ручное удаление записей аудита.

        Args:
            request:
                HTTP-запрос администратора.
            obj:
                Запись аудита.

        Returns:
            bool: False.
        """

        return False


@admin.register(RegistrationAttemptLog)
class RegistrationAttemptLogAdmin(admin.ModelAdmin):
    """
    Административная панель попыток регистрации.

    Используется для анализа неудачных регистраций и попыток подбора кодов.
    """

    list_display = (
        "id",
        "status",
        "role_code",
        "failure_reason",
        "ip_address",
        "created_at",
    )
    list_filter = (
        "status",
        "role_code",
        "failure_reason",
        "created_at",
    )
    search_fields = (
        "email_hash",
        "phone_hash",
        "role_code",
        "failure_reason",
        "ip_address",
        "user_agent",
    )
    readonly_fields = (
        "email_hash",
        "phone_hash",
        "role_code",
        "status",
        "failure_reason",
        "ip_address",
        "user_agent",
        "metadata",
        "created_at",
        "updated_at",
    )
    ordering = ("-created_at",)

    def has_add_permission(self, request) -> bool:
        """
        Запрещает ручное создание попыток регистрации.

        Args:
            request:
                HTTP-запрос администратора.

        Returns:
            bool: False.
        """

        return False

    def has_change_permission(self, request, obj=None) -> bool:
        """
        Запрещает ручное изменение попыток регистрации.

        Args:
            request:
                HTTP-запрос администратора.
            obj:
                Запись попытки регистрации.

        Returns:
            bool: False для конкретного объекта, иначе стандартное право просмотра списка.
        """

        if obj is not None:
            return False

        return super().has_change_permission(request, obj=obj)

    def has_delete_permission(self, request, obj=None) -> bool:
        """
        Запрещает ручное удаление попыток регистрации.

        Args:
            request:
                HTTP-запрос администратора.
            obj:
                Запись попытки регистрации.

        Returns:
            bool: False.
        """

        return False
