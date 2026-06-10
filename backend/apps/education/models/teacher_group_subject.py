from __future__ import annotations

from apps.education.managers import TeacherGroupSubjectManager
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _


class TeacherGroupSubject(models.Model):
    """
    Назначение преподавателя на предмет группы.

    Показывает, какой преподаватель ведёт конкретный предмет
    у конкретной группы в рамках учебного периода.
    """

    class RoleChoices(models.TextChoices):
        PRIMARY = "primary", _("Основной преподаватель")
        ASSISTANT = "assistant", _("Ассистент")
        SUBSTITUTE = "substitute", _("Замещающий преподаватель")
        OTHER = "other", _("Иная роль")

    teacher = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="teacher_group_subjects",
        verbose_name=_("Преподаватель"),
    )
    group_subject = models.ForeignKey(
        "education.GroupSubject",
        on_delete=models.CASCADE,
        related_name="teacher_assignments",
        verbose_name=_("Предмет группы"),
    )

    role = models.CharField(
        _("Роль преподавателя"),
        max_length=32,
        choices=RoleChoices.choices,
        default=RoleChoices.PRIMARY,
    )
    is_primary = models.BooleanField(
        _("Основной преподаватель"),
        default=True,
    )
    is_active = models.BooleanField(
        _("Активно"),
        default=True,
    )

    planned_hours = models.PositiveIntegerField(
        _("Плановые часы преподавателя"),
        default=0,
    )

    starts_at = models.DateField(
        _("Дата начала"),
        blank=True,
        null=True,
    )
    ends_at = models.DateField(
        _("Дата окончания"),
        blank=True,
        null=True,
    )

    notes = models.TextField(
        _("Примечание"),
        blank=True,
    )

    created_at = models.DateTimeField(
        _("Дата создания"),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        _("Дата обновления"),
        auto_now=True,
    )

    objects = TeacherGroupSubjectManager()

    class Meta:
        db_table = "education_teacher_group_subject"
        verbose_name = _("Назначение преподавателя на предмет группы")
        verbose_name_plural = _("Назначения преподавателей на предметы групп")
        ordering = ("group_subject", "-is_primary", "teacher")
        constraints = [
            models.UniqueConstraint(
                fields=("teacher", "group_subject"),
                name="education_unique_teacher_group_subject",
            ),
            models.UniqueConstraint(
                fields=("group_subject", "is_primary"),
                condition=Q(is_primary=True),
                name="education_unique_primary_teacher_per_group_subject",
            ),
        ]

    def __str__(self) -> str:
        full_name = getattr(self.teacher, "full_name", str(self.teacher))

        return f"{full_name} — {self.group_subject}"

    def clean(self) -> None:
        """
        Проверяет согласованность назначения преподавателя.
        """

        super().clean()

        errors: dict[str, str] = {}

        if self.ends_at and self.starts_at and self.ends_at < self.starts_at:
            errors["ends_at"] = _("Дата окончания не может быть раньше даты начала.")

        if self.group_subject_id:
            period = self.group_subject.period
            group = self.group_subject.group
            subject = self.group_subject.subject

            if self.starts_at and self.starts_at < period.start_date:
                errors["starts_at"] = _(
                    "Дата начала не может быть раньше начала учебного периода."
                )

            if self.ends_at and self.ends_at > period.end_date:
                errors["ends_at"] = _(
                    "Дата окончания не может быть позже окончания учебного периода."
                )

            if self.planned_hours > self.group_subject.planned_hours:
                errors["planned_hours"] = _(
                    "Плановые часы преподавателя не могут превышать плановые часы предмета группы."
                )

            if self.teacher_id:
                teacher_organizations = getattr(
                    self.teacher,
                    "teacher_organizations",
                    None,
                )

                if teacher_organizations is not None:
                    active_org_qs = teacher_organizations.filter(
                        organization=group.organization,
                        is_active=True,
                    )

                    if hasattr(active_org_qs.model, "starts_at"):
                        active_org_qs = active_org_qs.filter(
                            Q(starts_at__isnull=True)
                            | Q(starts_at__lte=period.end_date),
                            Q(ends_at__isnull=True) | Q(ends_at__gte=period.start_date),
                        )

                    if not active_org_qs.exists():
                        errors["teacher"] = _(
                            "Преподаватель не имеет активной связи с организацией группы."
                        )

                teacher_subjects = getattr(self.teacher, "teacher_subjects", None)

                if teacher_subjects is not None:
                    active_subject_qs = teacher_subjects.filter(is_active=True)

                    if active_subject_qs.exists():
                        has_required_subject = active_subject_qs.filter(
                            subject=subject,
                        ).exists()

                        if not has_required_subject:
                            errors["teacher"] = _(
                                "Преподаватель не закреплён за этим предметом."
                            )

        if self.is_primary and self.role == self.RoleChoices.ASSISTANT:
            errors["role"] = _(
                "Ассистент не может быть отмечен как основной преподаватель."
            )

        if errors:
            raise ValidationError(errors)
