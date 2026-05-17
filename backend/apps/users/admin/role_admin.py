from __future__ import annotations

from apps.users.constants.lifecycle import UserRoleStatus
from apps.users.models import Role, UserRole
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """
    Административная панель справочника ролей.

    Роли используются для бизнес-доступа внутри ЦОС «Пифагор».
    """

    list_display = (
        "id",
        "label",
        "code",
        "is_system",
        "is_active",
        "sort_order",
        "created_at",
    )
    list_filter = (
        "is_system",
        "is_active",
        "created_at",
    )
    search_fields = (
        "code",
        "label",
        "description",
    )
    ordering = (
        "sort_order",
        "label",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    """
    Административная панель назначенных ролей пользователей.

    Позволяет видеть роль пользователя в контексте:
        - платформы;
        - организации;
        - отделения;
        - группы.
    """

    list_display = (
        "id",
        "user",
        "role",
        "status",
        "organization",
        "department",
        "group",
        "assigned_by",
        "assigned_at",
    )
    list_filter = (
        "status",
        "role",
        "organization",
        "department",
        "group",
        "assigned_at",
        "revoked_at",
    )
    search_fields = (
        "user__email",
        "user__phone",
        "user__first_name",
        "user__last_name",
        "role__code",
        "role__label",
        "organization__name",
        "department__name",
        "group__name",
    )
    autocomplete_fields = (
        "user",
        "role",
        "organization",
        "department",
        "group",
        "assigned_by",
        "revoked_by",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
        "assigned_at",
        "revoked_at",
    )
    ordering = (
        "user",
        "role",
    )
    actions = (
        "approve_roles",
        "reject_roles",
        "archive_roles",
    )

    fieldsets = (
        (
            _("Основное"),
            {
                "fields": (
                    "user",
                    "role",
                    "status",
                )
            },
        ),
        (
            _("Контекст роли"),
            {
                "fields": (
                    "organization",
                    "department",
                    "group",
                )
            },
        ),
        (
            _("Назначение"),
            {
                "fields": (
                    "assigned_by",
                    "assigned_at",
                )
            },
        ),
        (
            _("Отзыв роли"),
            {
                "fields": (
                    "revoked_by",
                    "revoked_at",
                    "revoke_reason",
                )
            },
        ),
        (
            _("Служебные даты"),
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    @admin.action(description="Подтвердить выбранные роли")
    def approve_roles(self, request, queryset) -> None:
        """
        Подтверждает выбранные роли пользователей.

        Args:
            request:
                HTTP-запрос администратора.
            queryset:
                Выбранные роли пользователей.
        """

        queryset.update(status=UserRoleStatus.ACTIVE)

    @admin.action(description="Отклонить выбранные роли")
    def reject_roles(self, request, queryset) -> None:
        """
        Отклоняет выбранные роли пользователей.

        Args:
            request:
                HTTP-запрос администратора.
            queryset:
                Выбранные роли пользователей.
        """

        queryset.update(status=UserRoleStatus.REJECTED)

    @admin.action(description="Архивировать выбранные роли")
    def archive_roles(self, request, queryset) -> None:
        """
        Архивирует выбранные роли пользователей.

        Args:
            request:
                HTTP-запрос администратора.
            queryset:
                Выбранные роли пользователей.
        """

        queryset.update(status=UserRoleStatus.ARCHIVED)
