from __future__ import annotations

from apps.users.constants.moderation import ModerationStatus
from apps.users.models import Profile
from django.contrib import admin


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Административная панель базовых профилей пользователей.

    Базовый профиль хранит общие пользовательские данные:
        - аватар;
        - город;
        - описание;
        - часовой пояс;
        - ссылки на социальные профили;
        - статусы модерации.
    """

    list_display = (
        "id",
        "user",
        "city",
        "timezone",
        "avatar_moderation_status",
        "profile_moderation_status",
        "created_at",
    )
    list_filter = (
        "gender",
        "avatar_moderation_status",
        "profile_moderation_status",
        "timezone",
        "created_at",
    )
    search_fields = (
        "user__email",
        "user__phone",
        "user__first_name",
        "user__last_name",
        "city",
        "about",
    )
    autocomplete_fields = ("user",)
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    actions = (
        "approve_avatar",
        "reject_avatar",
        "approve_profile",
        "reject_profile",
    )

    @admin.action(description="Одобрить аватары")
    def approve_avatar(self, request, queryset) -> None:
        """
        Одобряет аватары выбранных профилей.

        Args:
            request:
                HTTP-запрос администратора.
            queryset:
                Выбранные профили.
        """

        queryset.update(avatar_moderation_status=ModerationStatus.APPROVED)

    @admin.action(description="Отклонить аватары")
    def reject_avatar(self, request, queryset) -> None:
        """
        Отклоняет аватары выбранных профилей.

        Args:
            request:
                HTTP-запрос администратора.
            queryset:
                Выбранные профили.
        """

        queryset.update(avatar_moderation_status=ModerationStatus.REJECTED)

    @admin.action(description="Одобрить профили")
    def approve_profile(self, request, queryset) -> None:
        """
        Одобряет публичные данные выбранных профилей.

        Args:
            request:
                HTTP-запрос администратора.
            queryset:
                Выбранные профили.
        """

        queryset.update(profile_moderation_status=ModerationStatus.APPROVED)

    @admin.action(description="Отклонить профили")
    def reject_profile(self, request, queryset) -> None:
        """
        Отклоняет публичные данные выбранных профилей.

        Args:
            request:
                HTTP-запрос администратора.
            queryset:
                Выбранные профили.
        """

        queryset.update(profile_moderation_status=ModerationStatus.REJECTED)
