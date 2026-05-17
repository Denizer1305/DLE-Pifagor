from __future__ import annotations

from apps.core.models import TimeStampedModel
from apps.users.constants.lifecycle import GuardianLearnerStatus
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class GuardianLearner(TimeStampedModel):
    """
    Связь родителя или законного представителя с учащимся.

    Для учащегося старше 14 лет связь может подтверждаться двумя частями кода:
        - код куратора;
        - код учащегося.

    Для учащегося младше 14 лет связь создаётся родителем и подтверждается
    куратором, администратором организации или заведующим отделением.
    """

    class RelationType(models.TextChoices):
        """
        Тип родства или представительства.
        """

        MOTHER = "mother", _("Мать")
        FATHER = "father", _("Отец")
        GUARDIAN = "guardian", _("Опекун")
        REPRESENTATIVE = "representative", _("Законный представитель")
        OTHER = "other", _("Иное")

    guardian = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="guardian_learner_links",
        verbose_name=_("Родитель"),
    )
    learner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="learner_guardian_links",
        verbose_name=_("Учащийся"),
    )

    relation_type = models.CharField(
        _("Тип связи"),
        max_length=32,
        choices=RelationType.choices,
        default=RelationType.OTHER,
    )
    status = models.CharField(
        _("Статус связи"),
        max_length=32,
        choices=GuardianLearnerStatus.choices,
        default=GuardianLearnerStatus.PENDING,
        db_index=True,
    )

    is_primary = models.BooleanField(
        _("Основной представитель"),
        default=False,
    )
    is_learner_consent_required = models.BooleanField(
        _("Требуется согласие учащегося"),
        default=False,
    )

    curator_code_verified_at = models.DateTimeField(
        _("Дата подтверждения кода куратора"),
        blank=True,
        null=True,
    )
    learner_code_verified_at = models.DateTimeField(
        _("Дата подтверждения кода учащегося"),
        blank=True,
        null=True,
    )

    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="requested_guardian_learner_links",
        verbose_name=_("Инициатор запроса"),
        blank=True,
        null=True,
    )
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="approved_guardian_learner_links",
        verbose_name=_("Подтвердил"),
        blank=True,
        null=True,
    )
    approved_at = models.DateTimeField(
        _("Дата подтверждения"),
        blank=True,
        null=True,
    )

    comment = models.TextField(
        _("Комментарий"),
        blank=True,
    )

    class Meta:
        db_table = "users_guardian_learner"
        verbose_name = _("Связь родителя и учащегося")
        verbose_name_plural = _("Связи родителей и учащихся")
        ordering = ("-is_primary", "-created_at")
        constraints = [
            models.UniqueConstraint(
                fields=["guardian", "learner"],
                name="users_guardian_learner_unique",
            ),
            models.UniqueConstraint(
                fields=["learner"],
                condition=models.Q(is_primary=True),
                name="users_guardian_learner_one_primary",
            ),
        ]
        indexes = [
            models.Index(
                fields=["guardian", "status"], name="users_gl_guardian_status_idx"
            ),
            models.Index(
                fields=["learner", "status"], name="users_gl_learner_status_idx"
            ),
        ]

    def __str__(self) -> str:
        """
        Возвращает строковое представление связи.

        Returns:
            str: Родитель и учащийся.
        """

        return f"{self.guardian} → {self.learner}"

    def clean(self) -> None:
        """
        Проверяет корректность связи родителя и учащегося.
        """

        super().clean()

        if self.guardian_id and self.learner_id and self.guardian_id == self.learner_id:
            raise ValidationError(_("Нельзя создать связь пользователя с самим собой."))

        if self.comment:
            self.comment = self.comment.strip()

    def approve(self, *, user=None, save: bool = True) -> None:
        """
        Подтверждает связь родителя и учащегося.

        Args:
            user:
                Пользователь, который подтвердил связь.
            save:
                Нужно ли сразу сохранить изменения.
        """

        self.status = GuardianLearnerStatus.ACTIVE
        self.approved_by = user
        self.approved_at = timezone.now()

        if save:
            self.save(
                update_fields=[
                    "status",
                    "approved_by",
                    "approved_at",
                    "updated_at",
                ]
            )

    def reject(self, *, save: bool = True) -> None:
        """
        Отклоняет связь родителя и учащегося.

        Args:
            save:
                Нужно ли сразу сохранить изменения.
        """

        self.status = GuardianLearnerStatus.REJECTED

        if save:
            self.save(update_fields=["status", "updated_at"])
