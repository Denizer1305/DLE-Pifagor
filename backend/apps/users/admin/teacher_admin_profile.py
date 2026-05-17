from __future__ import annotations

from apps.users.constants.lifecycle import ProfileStatus
from apps.users.models import TeacherProfile
from django.contrib import admin
from django.utils import timezone


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    """
    Административная панель профилей преподавателей.

    Используется для просмотра и проверки преподавателей,
    а также управления отображением преподавателя на публичных страницах.
    """

    list_display = (
        "id",
        "user",
        "organization",
        "department",
        "position",
        "status",
        "is_public",
        "show_on_teachers_page",
        "created_at",
    )
    list_filter = (
        "status",
        "organization",
        "department",
        "is_public",
        "show_on_teachers_page",
        "created_at",
    )
    search_fields = (
        "user__email",
        "user__phone",
        "user__first_name",
        "user__last_name",
        "position",
        "public_title",
        "organization__name",
        "department__name",
    )
    autocomplete_fields = (
        "user",
        "organization",
        "department",
        "verified_by",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
        "code_verified_at",
        "verified_at",
    )
    actions = (
        "verify_profiles",
        "reject_profiles",
        "archive_profiles",
        "show_on_public_page",
        "hide_from_public_page",
    )

    @admin.action(description="Подтвердить профили преподавателей")
    def verify_profiles(self, request, queryset) -> None:
        """
        Подтверждает выбранные профили преподавателей.

        Args:
            request:
                HTTP-запрос администратора.
            queryset:
                Выбранные профили преподавателей.
        """

        queryset.update(
            status=ProfileStatus.VERIFIED,
            verified_by=request.user,
            verified_at=timezone.now(),
        )

    @admin.action(description="Отклонить профили преподавателей")
    def reject_profiles(self, request, queryset) -> None:
        """
        Отклоняет выбранные профили преподавателей.

        Args:
            request:
                HTTP-запрос администратора.
            queryset:
                Выбранные профили преподавателей.
        """

        queryset.update(status=ProfileStatus.REJECTED)

    @admin.action(description="Архивировать профили преподавателей")
    def archive_profiles(self, request, queryset) -> None:
        """
        Архивирует выбранные профили преподавателей.

        Args:
            request:
                HTTP-запрос администратора.
            queryset:
                Выбранные профили преподавателей.
        """

        queryset.update(status=ProfileStatus.ARCHIVED)

    @admin.action(description="Показывать на странице преподавателей")
    def show_on_public_page(self, request, queryset) -> None:
        """
        Включает показ выбранных преподавателей на публичной странице.

        Args:
            request:
                HTTP-запрос администратора.
            queryset:
                Выбранные профили преподавателей.
        """

        queryset.update(
            is_public=True,
            show_on_teachers_page=True,
        )

    @admin.action(description="Скрыть со страницы преподавателей")
    def hide_from_public_page(self, request, queryset) -> None:
        """
        Скрывает выбранных преподавателей с публичной страницы.

        Args:
            request:
                HTTP-запрос администратора.
            queryset:
                Выбранные профили преподавателей.
        """

        queryset.update(show_on_teachers_page=False)
