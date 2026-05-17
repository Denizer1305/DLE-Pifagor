from __future__ import annotations

from apps.core.models import TimeStampedModel
from apps.users.constants.onboarding import JoinRequestStatus, JoinRequestType
from apps.users.managers import UserJoinRequestManager
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserJoinRequest(TimeStampedModel):
    """
    Заявка пользователя на присоединение.

    Используется для трёх основных сценариев:
        - преподаватель просится в образовательную организацию;
        - учащийся просится в группу;
        - родитель просит связь с учащимся.

    Заявка остаётся в ожидании, пока её не рассмотрит уполномоченный пользователь.
    Если заявка отклонена, пользователю отправляется сообщение,
    а аккаунт может быть запланирован к анонимизации через 7 дней.
    """

    objects = UserJoinRequestManager()

    request_type = models.CharField(
        _("Тип заявки"),
        max_length=64,
        choices=JoinRequestType.choices,
        db_index=True,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="join_requests",
        verbose_name=_("Пользователь"),
    )
    target_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="target_join_requests",
        verbose_name=_("Целевой пользователь"),
        blank=True,
        null=True,
        help_text=_("Используется для связи родителя с учащимся."),
    )

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="user_join_requests",
        verbose_name=_("Образовательная организация"),
        blank=True,
        null=True,
    )
    department = models.ForeignKey(
        "organizations.Department",
        on_delete=models.SET_NULL,
        related_name="user_join_requests",
        verbose_name=_("Отделение"),
        blank=True,
        null=True,
    )
    group = models.ForeignKey(
        "organizations.StudyGroup",
        on_delete=models.SET_NULL,
        related_name="user_join_requests",
        verbose_name=_("Группа"),
        blank=True,
        null=True,
    )

    status = models.CharField(
        _("Статус заявки"),
        max_length=32,
        choices=JoinRequestStatus.choices,
        default=JoinRequestStatus.PENDING,
        db_index=True,
    )

    message = models.TextField(
        _("Сообщение пользователя"),
        blank=True,
    )
    review_comment = models.TextField(
        _("Комментарий проверки"),
        blank=True,
    )

    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="reviewed_join_requests",
        verbose_name=_("Проверил"),
        blank=True,
        null=True,
    )
    reviewed_at = models.DateTimeField(
        _("Дата проверки"),
        blank=True,
        null=True,
    )

    expires_at = models.DateTimeField(
        _("Дата истечения заявки"),
        blank=True,
        null=True,
        help_text=_("Если пусто, заявка может ожидать проверки без автоистечения."),
    )

    class Meta:
        db_table = "users_join_request"
        verbose_name = _("Заявка пользователя")
        verbose_name_plural = _("Заявки пользователей")
        ordering = ("-created_at",)
        indexes = [
            models.Index(
                fields=["request_type", "status"], name="users_join_type_status_idx"
            ),
            models.Index(fields=["user", "status"], name="users_join_user_status_idx"),
            models.Index(
                fields=["organization", "status"], name="users_join_org_status_idx"
            ),
            models.Index(
                fields=["group", "status"], name="users_join_group_status_idx"
            ),
        ]

    def __str__(self) -> str:
        """
        Возвращает строковое представление заявки.

        Returns:
            str: Тип заявки и пользователь.
        """

        return f"{self.get_request_type_display()} — {self.user}"

    @property
    def is_pending(self) -> bool:
        """
        Проверяет, ожидает ли заявка рассмотрения.

        Returns:
            bool: True, если заявка ожидает проверки.
        """

        return self.status == JoinRequestStatus.PENDING

    def approve(self, *, user=None, comment: str = "", save: bool = True) -> None:
        """
        Подтверждает заявку.

        Args:
            user:
                Пользователь, который подтвердил заявку.
            comment:
                Комментарий проверяющего.
            save:
                Нужно ли сразу сохранить изменения.
        """

        self.status = JoinRequestStatus.APPROVED
        self.reviewed_by = user
        self.reviewed_at = timezone.now()
        self.review_comment = comment or ""

        if save:
            self.save(
                update_fields=[
                    "status",
                    "reviewed_by",
                    "reviewed_at",
                    "review_comment",
                    "updated_at",
                ]
            )

    def reject(self, *, user=None, comment: str = "", save: bool = True) -> None:
        """
        Отклоняет заявку.

        Args:
            user:
                Пользователь, который отклонил заявку.
            comment:
                Комментарий проверяющего.
            save:
                Нужно ли сразу сохранить изменения.
        """

        self.status = JoinRequestStatus.REJECTED
        self.reviewed_by = user
        self.reviewed_at = timezone.now()
        self.review_comment = comment or ""

        if save:
            self.save(
                update_fields=[
                    "status",
                    "reviewed_by",
                    "reviewed_at",
                    "review_comment",
                    "updated_at",
                ]
            )
