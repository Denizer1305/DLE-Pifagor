from __future__ import annotations

from apps.core.models import TimeStampedModel
from apps.users.constants.lifecycle import ProfileStatus
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class LearnerProfile(TimeStampedModel):
    """
    Профиль учащегося.

    Используется для школьников, студентов колледжей, студентов вузов
    и участников дополнительного образования.

    Важно:
        Для детей младше 14 лет аккаунт создаёт родитель,
        но учащийся всё равно получает отдельный User и LearnerProfile.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="learner_profile",
        verbose_name=_("Пользователь"),
    )

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.SET_NULL,
        related_name="learner_profiles",
        verbose_name=_("Образовательная организация"),
        blank=True,
        null=True,
    )
    department = models.ForeignKey(
        "organizations.Department",
        on_delete=models.SET_NULL,
        related_name="learner_profiles",
        verbose_name=_("Отделение"),
        blank=True,
        null=True,
    )
    group = models.ForeignKey(
        "organizations.StudyGroup",
        on_delete=models.SET_NULL,
        related_name="learner_profiles",
        verbose_name=_("Группа"),
        blank=True,
        null=True,
    )
    curator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="curated_learner_profiles",
        verbose_name=_("Куратор"),
        blank=True,
        null=True,
    )

    learner_code = models.CharField(
        _("Внутренний код учащегося"),
        max_length=64,
        blank=True,
        help_text=_("Например: ИСП-22-01 или иной код внутри организации."),
    )
    admission_year = models.PositiveSmallIntegerField(
        _("Год поступления"),
        blank=True,
        null=True,
    )
    admission_date = models.DateField(
        _("Дата зачисления"),
        blank=True,
        null=True,
    )
    graduation_date = models.DateField(
        _("Дата выпуска"),
        blank=True,
        null=True,
    )

    status = models.CharField(
        _("Статус профиля"),
        max_length=32,
        choices=ProfileStatus.choices,
        default=ProfileStatus.DRAFT,
        db_index=True,
    )

    is_minor = models.BooleanField(
        _("Учащийся младше 14 лет"),
        default=False,
    )
    created_by_guardian = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="created_learner_profiles",
        verbose_name=_("Создан родителем"),
        blank=True,
        null=True,
    )

    notes = models.TextField(
        _("Служебные заметки"),
        blank=True,
        default="",
    )
    verification_comment = models.TextField(
        _("Комментарий проверки"),
        blank=True,
    )

    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="verified_learner_profiles",
        verbose_name=_("Подтвердил"),
        blank=True,
        null=True,
    )
    verified_at = models.DateTimeField(
        _("Дата подтверждения"),
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "users_learner_profile"
        verbose_name = _("Профиль учащегося")
        verbose_name_plural = _("Профили учащихся")
        indexes = [
            models.Index(
                fields=["organization", "status"], name="users_lp_org_status_idx"
            ),
            models.Index(
                fields=["department", "status"], name="users_lp_dept_status_idx"
            ),
            models.Index(fields=["group", "status"], name="users_lp_group_status_idx"),
            models.Index(fields=["curator", "status"], name="users_lp_cur_status_idx"),
        ]

    def __str__(self) -> str:
        """
        Возвращает строковое представление профиля учащегося.

        Returns:
            str: Пользователь.
        """

        return f"Учащийся: {self.user}"

    def clean(self) -> None:
        """
        Проверяет согласованность организации, отделения и группы.
        """

        super().clean()

        if self.notes:
            self.notes = self.notes.strip()

        if self.verification_comment:
            self.verification_comment = self.verification_comment.strip()

        if (
            self.department
            and self.organization
            and self.department.organization_id != self.organization_id
        ):
            raise ValidationError(
                {
                    "department": _(
                        "Отделение должно принадлежать выбранной образовательной организации."
                    )
                }
            )

        if (
            self.group
            and self.organization
            and self.group.organization_id != self.organization_id
        ):
            raise ValidationError(
                {
                    "group": _(
                        "Группа должна принадлежать выбранной образовательной организации."
                    )
                }
            )

        if (
            self.group
            and self.department
            and getattr(self.group, "department_id", None)
            and self.group.department_id != self.department_id
        ):
            raise ValidationError(
                {"group": _("Группа должна принадлежать выбранному отделению.")}
            )

    def mark_verified(self, *, user=None, save: bool = True) -> None:
        """
        Подтверждает профиль учащегося.

        Args:
            user:
                Пользователь, который подтвердил профиль.
            save:
                Нужно ли сразу сохранить изменения.
        """

        from django.utils import timezone

        self.status = ProfileStatus.VERIFIED
        self.verified_by = user
        self.verified_at = timezone.now()

        if save:
            self.save(
                update_fields=[
                    "status",
                    "verified_by",
                    "verified_at",
                    "updated_at",
                ]
            )
