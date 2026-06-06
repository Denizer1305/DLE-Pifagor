from __future__ import annotations

from apps.core.models import TimeStampedModel
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class TeacherSubject(TimeStampedModel):
    """
    Предмет преподавателя.

    Модель хранит связь преподавателя с предметом.
    Проверка роли пользователя выполняется в service-слое через UserRole.
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
        related_name="teacher_subjects",
        verbose_name=_("Предмет"),
    )
    is_primary = models.BooleanField(
        _("Основной предмет"),
        default=False,
    )
    is_active = models.BooleanField(
        _("Активен"),
        default=True,
    )
    notes = models.TextField(
        _("Заметки"),
        blank=True,
    )

    class Meta:
        db_table = "organizations_teacher_subject"
        verbose_name = _("Предмет преподавателя")
        verbose_name_plural = _("Предметы преподавателей")
        ordering = ("teacher", "-is_primary", "subject")
        constraints = [
            models.UniqueConstraint(
                fields=["teacher", "subject"],
                name="organizations_teacher_subject_unique",
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
            models.Index(
                fields=["teacher", "is_primary"],
                name="org_ts_primary_idx",
            ),
        ]

    def __str__(self) -> str:
        """
        Возвращает строковое представление связи преподавателя и предмета.

        Returns:
            str: Преподаватель и предмет.
        """

        return f"{self.teacher} — {self.subject}"