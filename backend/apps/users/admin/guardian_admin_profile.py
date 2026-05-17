from __future__ import annotations

from apps.users.constants.lifecycle import GuardianLearnerStatus, ProfileStatus
from apps.users.models import GuardianLearner, GuardianProfile
from django.contrib import admin
from django.utils import timezone


@admin.register(GuardianProfile)
class GuardianProfileAdmin(admin.ModelAdmin):
    """
    Административная панель профилей родителей и законных представителей.
    """

    list_display = (
        "id",
        "user",
        "status",
        "occupation",
        "work_place",
        "created_at",
    )
    list_filter = (
        "status",
        "created_at",
    )
    search_fields = (
        "user__email",
        "user__phone",
        "user__first_name",
        "user__last_name",
        "occupation",
        "work_place",
    )
    autocomplete_fields = ("user",)
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    actions = (
        "verify_profiles",
        "reject_profiles",
        "archive_profiles",
    )

    @admin.action(description="Подтвердить профили родителей")
    def verify_profiles(self, request, queryset) -> None:
        """
        Подтверждает выбранные профили родителей.

        Args:
            request:
                HTTP-запрос администратора.
            queryset:
                Выбранные профили родителей.
        """

        queryset.update(status=ProfileStatus.VERIFIED)

    @admin.action(description="Отклонить профили родителей")
    def reject_profiles(self, request, queryset) -> None:
        """
        Отклоняет выбранные профили родителей.

        Args:
            request:
                HTTP-запрос администратора.
            queryset:
                Выбранные профили родителей.
        """

        queryset.update(status=ProfileStatus.REJECTED)

    @admin.action(description="Архивировать профили родителей")
    def archive_profiles(self, request, queryset) -> None:
        """
        Архивирует выбранные профили родителей.

        Args:
            request:
                HTTP-запрос администратора.
            queryset:
                Выбранные профили родителей.
        """

        queryset.update(status=ProfileStatus.ARCHIVED)


@admin.register(GuardianLearner)
class GuardianLearnerAdmin(admin.ModelAdmin):
    """
    Административная панель связей родителей и учащихся.

    Связь используется для доступа родителя к данным ребёнка:
        - оценкам;
        - заданиям;
        - расписанию;
        - посещаемости;
        - уведомлениям.
    """

    list_display = (
        "id",
        "guardian",
        "learner",
        "relation_type",
        "status",
        "is_primary",
        "is_learner_consent_required",
        "approved_by",
        "approved_at",
        "created_at",
    )
    list_filter = (
        "status",
        "relation_type",
        "is_primary",
        "is_learner_consent_required",
        "created_at",
        "approved_at",
    )
    search_fields = (
        "guardian__email",
        "guardian__phone",
        "guardian__first_name",
        "guardian__last_name",
        "learner__email",
        "learner__phone",
        "learner__first_name",
        "learner__last_name",
    )
    autocomplete_fields = (
        "guardian",
        "learner",
        "requested_by",
        "approved_by",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
        "curator_code_verified_at",
        "learner_code_verified_at",
        "approved_at",
    )
    actions = (
        "approve_links",
        "reject_links",
        "revoke_links",
        "archive_links",
    )

    @admin.action(description="Подтвердить связи")
    def approve_links(self, request, queryset) -> None:
        """
        Подтверждает выбранные связи родителей и учащихся.

        Args:
            request:
                HTTP-запрос администратора.
            queryset:
                Выбранные связи.
        """

        queryset.update(
            status=GuardianLearnerStatus.ACTIVE,
            approved_by=request.user,
            approved_at=timezone.now(),
        )

    @admin.action(description="Отклонить связи")
    def reject_links(self, request, queryset) -> None:
        """
        Отклоняет выбранные связи родителей и учащихся.

        Args:
            request:
                HTTP-запрос администратора.
            queryset:
                Выбранные связи.
        """

        queryset.update(status=GuardianLearnerStatus.REJECTED)

    @admin.action(description="Отозвать связи")
    def revoke_links(self, request, queryset) -> None:
        """
        Отзывает выбранные связи родителей и учащихся.

        Args:
            request:
                HTTP-запрос администратора.
            queryset:
                Выбранные связи.
        """

        queryset.update(status=GuardianLearnerStatus.REVOKED)

    @admin.action(description="Архивировать связи")
    def archive_links(self, request, queryset) -> None:
        """
        Архивирует выбранные связи родителей и учащихся.

        Args:
            request:
                HTTP-запрос администратора.
            queryset:
                Выбранные связи.
        """

        queryset.update(status=GuardianLearnerStatus.ARCHIVED)
