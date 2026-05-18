from __future__ import annotations

from apps.core.models import TimeStampedModel
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class TeacherSubject(TimeStampedModel):
    """
    Связь преподавателя с учебным предметом.

    Один преподаватель может вести несколько предметов.
    Один предмет может вести несколько преподавателей.
    """

    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="teacher_subjects",
        verbose_name=_("Преподаватель"),
    )
    subject = models.ForeignKey(
        "organizations.Subject",
        on_delete=models.CASCADE,
        related_name="teacher_links",
        verbose_name=_("Предмет"),
    )

    is_primary = models.BooleanField(
        _("Основной предмет"),
        default=False,
    )
    is_active = models.BooleanField(
        _("Активна"),
        default=True,
        db_index=True,
    )

    class Meta:
        db_table = "organizations_teacher_subject"
        verbose_name = _("Связь преподавателя с предметом")
        verbose_name_plural = _("Связи преподавателей с предметами")
        ordering = ("teacher", "-is_primary", "subject__name")
        constraints = [
            models.UniqueConstraint(
                fields=["teacher", "subject"],
                name="org_teacher_subject_unique",
            ),
        ]
        indexes = [
            models.Index(
                fields=["teacher", "is_active"],
                name="org_ts_teacher_idx",
            ),
            models.Index(
                fields=["subject", "is_active"],
                name="org_ts_subject_idx",
            ),
        ]

    def __str__(self) -> str:
        """
        Возвращает строковое представление связи.

        Returns:
            str: Преподаватель и предмет.
        """

        return f"{self.teacher} — {self.subject}"
