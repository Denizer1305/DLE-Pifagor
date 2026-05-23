from __future__ import annotations

from apps.users.constants.lifecycle import ProfileStatus
from apps.users.models import LearnerProfile
from django.contrib import admin
from django.utils import timezone


@admin.register(LearnerProfile)
class LearnerProfileAdmin(admin.ModelAdmin):
    """
    Административная панель профилей учащихся.

    Используется для просмотра и проверки учащихся:
        - школьников;
        - студентов колледжей;
        - студентов вузов;
        - учащихся дополнительного образования.
    """

    list_display = (
        "id",
        "user",
        "organization",
        "department",
        "group",
        "curator",
        "status",
        "is_minor",
        "admission_year",
        "created_at",
    )
    list_filter = (
        "status",
        "is_minor",
        "organization",
        "department",
        "group",
        "admission_year",
        "created_at",
    )
    search_fields = (
        "user__email",
        "user__phone",
        "user__first_name",
        "user__last_name",
        "learner_code",
        "organization__name",
        "department__name",
        "group__name",
    )
    autocomplete_fields = (
        "user",
        "organization",
        "department",
        "group",
        "curator",
        "created_by_guardian",
        "verified_by",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
        "verified_at",
    )
    actions = (
        "verify_profiles",
        "reject_profiles",
        "archive_profiles",
    )

    @admin.action(description="Подтвердить профили учащихся")
    def verify_profiles(self, request, queryset) -> None:
        """
        Подтверждает выбранные профили учащихся.

        Args:
            request:
                HTTP-запрос администратора.
            queryset:
                Выбранные профили учащихся.
        """

        queryset.update(
            status=ProfileStatus.VERIFIED,
            verified_by=request.user,
            verified_at=timezone.now(),
        )

    @admin.action(description="Отклонить профили учащихся")
    def reject_profiles(self, request, queryset) -> None:
        """
        Отклоняет выбранные профили учащихся.

        Args:
            request:
                HTTP-запрос администратора.
            queryset:
                Выбранные профили учащихся.
        """

        queryset.update(status=ProfileStatus.REJECTED)

    @admin.action(description="Архивировать профили учащихся")
    def archive_profiles(self, request, queryset) -> None:
        """
        Архивирует выбранные профили учащихся.

        Args:
            request:
                HTTP-запрос администратора.
            queryset:
                Выбранные профили учащихся.
        """

        queryset.update(status=ProfileStatus.ARCHIVED)
