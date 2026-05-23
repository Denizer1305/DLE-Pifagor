from __future__ import annotations

from apps.users.constants.lifecycle import UserStatus
from apps.users.models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """
    Административная панель для кастомной модели пользователя.

    Позволяет просматривать, фильтровать и управлять пользователями:
        - статусом аккаунта;
        - подтверждением email и телефона;
        - доступом к самостоятельному входу;
        - управляемыми аккаунтами детей младше 14 лет;
        - техническими правами Django.
    """

    list_display = (
        "id",
        "email",
        "phone",
        "full_name",
        "status",
        "is_active",
        "is_staff",
        "is_email_verified",
        "is_phone_verified",
        "is_login_allowed",
        "created_at",
    )
    list_filter = (
        "status",
        "is_active",
        "is_staff",
        "is_superuser",
        "is_email_verified",
        "is_phone_verified",
        "is_login_allowed",
        "created_at",
    )
    search_fields = (
        "email",
        "phone",
        "first_name",
        "last_name",
        "middle_name",
    )
    ordering = (
        "last_name",
        "first_name",
        "email",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
        "email_verified_at",
        "phone_verified_at",
        "login_activation_requested_at",
        "login_activated_at",
        "scheduled_for_deletion_at",
        "anonymized_at",
        "last_login",
    )
    filter_horizontal = (
        "groups",
        "user_permissions",
    )

    fieldsets = (
        (
            _("Учётные данные"),
            {
                "fields": (
                    "email",
                    "phone",
                    "password",
                )
            },
        ),
        (
            _("Персональные данные"),
            {
                "fields": (
                    "last_name",
                    "first_name",
                    "middle_name",
                    "birth_date",
                )
            },
        ),
        (
            _("Статус аккаунта"),
            {
                "fields": (
                    "status",
                    "is_active",
                    "is_login_allowed",
                    "account_managed_by",
                )
            },
        ),
        (
            _("Подтверждение контактов"),
            {
                "fields": (
                    "is_email_verified",
                    "email_verified_at",
                    "is_phone_verified",
                    "phone_verified_at",
                )
            },
        ),
        (
            _("Самостоятельный вход"),
            {
                "fields": (
                    "login_available_from",
                    "login_activation_requested_at",
                    "login_activated_at",
                )
            },
        ),
        (
            _("Права Django"),
            {
                "fields": (
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            _("Жизненный цикл"),
            {
                "fields": (
                    "archived_at",
                    "archived_by",
                    "archive_reason",
                    "deleted_at",
                    "deleted_by",
                    "delete_reason",
                    "scheduled_for_deletion_at",
                    "anonymized_at",
                )
            },
        ),
        (
            _("Служебные даты"),
            {
                "fields": (
                    "last_login",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    add_fieldsets = (
        (
            _("Создание пользователя"),
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "phone",
                    "last_name",
                    "first_name",
                    "middle_name",
                    "birth_date",
                    "password1",
                    "password2",
                    "status",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_email_verified",
                    "is_phone_verified",
                    "is_login_allowed",
                ),
            },
        ),
    )

    actions = (
        "activate_users",
        "block_users",
        "mark_email_verified",
        "mark_phone_verified",
    )

    @admin.display(description="ФИО")
    def full_name(self, obj: User) -> str:
        """
        Возвращает полное имя пользователя для отображения в списке.

        Args:
            obj:
                Пользователь.

        Returns:
            str: ФИО пользователя.
        """

        return obj.get_full_name()

    @admin.action(description="Активировать выбранных пользователей")
    def activate_users(self, request, queryset) -> None:
        """
        Активирует выбранных пользователей.

        Args:
            request:
                HTTP-запрос администратора.
            queryset:
                Выбранные пользователи.
        """

        queryset.update(
            status=UserStatus.ACTIVE,
            is_active=True,
        )

    @admin.action(description="Заблокировать выбранных пользователей")
    def block_users(self, request, queryset) -> None:
        """
        Блокирует выбранных пользователей.

        Args:
            request:
                HTTP-запрос администратора.
            queryset:
                Выбранные пользователи.
        """

        queryset.update(
            status=UserStatus.BLOCKED,
            is_active=False,
        )

    @admin.action(description="Отметить email как подтверждённый")
    def mark_email_verified(self, request, queryset) -> None:
        """
        Отмечает email выбранных пользователей как подтверждённый.

        Args:
            request:
                HTTP-запрос администратора.
            queryset:
                Выбранные пользователи.
        """

        for user in queryset:
            user.mark_email_verified(save=True)

    @admin.action(description="Отметить телефон как подтверждённый")
    def mark_phone_verified(self, request, queryset) -> None:
        """
        Отмечает телефон выбранных пользователей как подтверждённый.

        Args:
            request:
                HTTP-запрос администратора.
            queryset:
                Выбранные пользователи.
        """

        for user in queryset:
            user.mark_phone_verified(save=True)
