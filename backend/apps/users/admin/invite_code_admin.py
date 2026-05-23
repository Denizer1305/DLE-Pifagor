from __future__ import annotations

from apps.users.models import InviteCode
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


@admin.register(InviteCode)
class InviteCodeAdmin(admin.ModelAdmin):
    """
    Административная панель временных кодов приглашения.

    Важно:
        Открытый код не хранится в базе данных.
        В админке отображается только хеш кода.
    """

    list_display = (
        "id",
        "purpose",
        "organization",
        "department",
        "group",
        "target_user",
        "is_active",
        "used_count",
        "max_uses",
        "expires_at",
        "last_used_at",
        "created_at",
    )
    list_filter = (
        "purpose",
        "is_active",
        "organization",
        "department",
        "group",
        "expires_at",
        "created_at",
    )
    search_fields = (
        "code_hash",
        "organization__name",
        "department__name",
        "group__name",
        "target_user__email",
        "target_user__phone",
    )
    autocomplete_fields = (
        "organization",
        "department",
        "group",
        "created_by",
        "target_user",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
        "last_used_at",
        "code_hash_preview",
        "is_expired_display",
        "is_available_display",
    )
    ordering = ("-created_at",)
    actions = (
        "activate_codes",
        "deactivate_codes",
    )

    fieldsets = (
        (
            _("Код"),
            {
                "fields": (
                    "code_hash",
                    "code_hash_preview",
                    "purpose",
                    "is_active",
                )
            },
        ),
        (
            _("Контекст"),
            {
                "fields": (
                    "organization",
                    "department",
                    "group",
                    "target_user",
                )
            },
        ),
        (
            _("Использование"),
            {
                "fields": (
                    "expires_at",
                    "max_uses",
                    "used_count",
                    "last_used_at",
                    "is_expired_display",
                    "is_available_display",
                )
            },
        ),
        (
            _("Создание"),
            {
                "fields": (
                    "created_by",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    @admin.display(description="Хеш кода")
    def code_hash_preview(self, obj: InviteCode) -> str:
        """
        Возвращает короткое отображение хеша кода.

        Args:
            obj:
                Код приглашения.

        Returns:
            str: Усечённый хеш.
        """

        if not obj.code_hash:
            return ""

        return f"{obj.code_hash[:12]}..."

    @admin.display(description="Истёк")
    def is_expired_display(self, obj: InviteCode) -> bool:
        """
        Проверяет, истёк ли код.

        Args:
            obj:
                Код приглашения.

        Returns:
            bool: True, если код истёк.
        """

        return obj.is_expired

    @admin.display(description="Доступен")
    def is_available_display(self, obj: InviteCode) -> bool:
        """
        Проверяет, доступен ли код.

        Args:
            obj:
                Код приглашения.

        Returns:
            bool: True, если код можно использовать.
        """

        return obj.is_available

    @admin.action(description="Активировать выбранные коды")
    def activate_codes(self, request, queryset) -> None:
        """
        Активирует выбранные коды приглашения.

        Args:
            request:
                HTTP-запрос администратора.
            queryset:
                Выбранные коды.
        """

        queryset.update(is_active=True)

    @admin.action(description="Отключить выбранные коды")
    def deactivate_codes(self, request, queryset) -> None:
        """
        Отключает выбранные коды приглашения.

        Args:
            request:
                HTTP-запрос администратора.
            queryset:
                Выбранные коды.
        """

        queryset.update(is_active=False)
