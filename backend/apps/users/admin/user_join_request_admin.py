from __future__ import annotations

from apps.users.constants.onboarding import JoinRequestStatus
from apps.users.models import UserJoinRequest
from django.contrib import admin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


@admin.register(UserJoinRequest)
class UserJoinRequestAdmin(admin.ModelAdmin):
    """
    Административная панель заявок пользователей.

    Заявки используются для:
        - принятия преподавателя в организацию;
        - принятия учащегося в группу;
        - подтверждения связи родителя и учащегося.
    """

    list_display = (
        "id",
        "request_type",
        "user",
        "target_user",
        "organization",
        "department",
        "group",
        "status",
        "reviewed_by",
        "reviewed_at",
        "created_at",
    )
    list_filter = (
        "request_type",
        "status",
        "organization",
        "department",
        "group",
        "reviewed_at",
        "created_at",
    )
    search_fields = (
        "user__email",
        "user__phone",
        "user__first_name",
        "user__last_name",
        "target_user__email",
        "target_user__phone",
        "organization__name",
        "department__name",
        "group__name",
        "message",
        "review_comment",
    )
    autocomplete_fields = (
        "user",
        "target_user",
        "organization",
        "department",
        "group",
        "reviewed_by",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
        "reviewed_at",
    )
    ordering = ("-created_at",)
    actions = (
        "approve_requests",
        "reject_requests",
        "cancel_requests",
        "expire_requests",
    )

    fieldsets = (
        (
            _("Основное"),
            {
                "fields": (
                    "request_type",
                    "status",
                    "user",
                    "target_user",
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
                )
            },
        ),
        (
            _("Сообщения"),
            {
                "fields": (
                    "message",
                    "review_comment",
                )
            },
        ),
        (
            _("Проверка"),
            {
                "fields": (
                    "reviewed_by",
                    "reviewed_at",
                    "expires_at",
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

    @admin.action(description="Подтвердить выбранные заявки")
    def approve_requests(self, request, queryset) -> None:
        """
        Подтверждает выбранные заявки.

        Args:
            request:
                HTTP-запрос администратора.
            queryset:
                Выбранные заявки.
        """

        queryset.update(
            status=JoinRequestStatus.APPROVED,
            reviewed_by=request.user,
            reviewed_at=timezone.now(),
        )

    @admin.action(description="Отклонить выбранные заявки")
    def reject_requests(self, request, queryset) -> None:
        """
        Отклоняет выбранные заявки.

        Args:
            request:
                HTTP-запрос администратора.
            queryset:
                Выбранные заявки.
        """

        queryset.update(
            status=JoinRequestStatus.REJECTED,
            reviewed_by=request.user,
            reviewed_at=timezone.now(),
        )

    @admin.action(description="Отменить выбранные заявки")
    def cancel_requests(self, request, queryset) -> None:
        """
        Отменяет выбранные заявки.

        Args:
            request:
                HTTP-запрос администратора.
            queryset:
                Выбранные заявки.
        """

        queryset.update(
            status=JoinRequestStatus.CANCELLED,
            reviewed_by=request.user,
            reviewed_at=timezone.now(),
        )

    @admin.action(description="Пометить выбранные заявки как истёкшие")
    def expire_requests(self, request, queryset) -> None:
        """
        Помечает выбранные заявки как истёкшие.

        Args:
            request:
                HTTP-запрос администратора.
            queryset:
                Выбранные заявки.
        """

        queryset.update(
            status=JoinRequestStatus.EXPIRED,
            reviewed_by=request.user,
            reviewed_at=timezone.now(),
        )
