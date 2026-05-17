from __future__ import annotations

from apps.core.models import TimeStampedModel
from apps.core.validators import validate_image_extension
from apps.users.constants.lifecycle import ProfileStatus
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class TeacherProfile(TimeStampedModel):
    """
    Профиль преподавателя.

    Содержит данные, связанные с публичным и служебным профилем преподавателя:
        - организация;
        - отделение;
        - должность;
        - публичный заголовок;
        - описание;
        - образование;
        - стаж;
        - достижения;
        - настройки показа на публичной странице.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="teacher_profile",
        verbose_name=_("Пользователь"),
    )

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.SET_NULL,
        related_name="teacher_profiles",
        verbose_name=_("Образовательная организация"),
        blank=True,
        null=True,
    )
    department = models.ForeignKey(
        "organizations.Department",
        on_delete=models.SET_NULL,
        related_name="teacher_profiles",
        verbose_name=_("Отделение"),
        blank=True,
        null=True,
    )

    position = models.CharField(
        _("Должность"),
        max_length=255,
        blank=True,
    )
    public_title = models.CharField(
        _("Публичный заголовок"),
        max_length=255,
        blank=True,
        help_text=_('Например: "Преподаватель математики".'),
    )
    short_bio = models.CharField(
        _("Краткое описание"),
        max_length=255,
        blank=True,
    )
    bio = models.TextField(
        _("Описание"),
        blank=True,
    )
    education = models.TextField(
        _("Образование"),
        blank=True,
    )
    experience_years = models.PositiveSmallIntegerField(
        _("Стаж, лет"),
        blank=True,
        null=True,
    )
    achievements = models.TextField(
        _("Достижения и награды"),
        blank=True,
    )

    cover_image = models.ImageField(
        _("Обложка карточки преподавателя"),
        upload_to="users/teachers/covers/%Y/%m/",
        validators=[validate_image_extension],
        blank=True,
        null=True,
    )

    is_public = models.BooleanField(
        _("Публичный профиль"),
        default=True,
    )
    show_on_teachers_page = models.BooleanField(
        _("Показывать на странице преподавателей"),
        default=True,
    )

    status = models.CharField(
        _("Статус профиля"),
        max_length=32,
        choices=ProfileStatus.choices,
        default=ProfileStatus.DRAFT,
        db_index=True,
    )

    code_verified_at = models.DateTimeField(
        _("Дата подтверждения регистрационного кода"),
        blank=True,
        null=True,
    )
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="verified_teacher_profiles",
        verbose_name=_("Подтвердил"),
        blank=True,
        null=True,
    )
    verified_at = models.DateTimeField(
        _("Дата подтверждения"),
        blank=True,
        null=True,
    )
    verification_comment = models.TextField(
        _("Комментарий проверки"),
        blank=True,
    )

    hired_at = models.DateField(
        _("Дата начала работы"),
        blank=True,
        null=True,
    )
    dismissed_at = models.DateField(
        _("Дата увольнения"),
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "users_teacher_profile"
        verbose_name = _("Профиль преподавателя")
        verbose_name_plural = _("Профили преподавателей")
        indexes = [
            models.Index(
                fields=["organization", "status"], name="users_tp_org_status_idx"
            ),
            models.Index(
                fields=["department", "status"], name="users_tp_dept_status_idx"
            ),
            models.Index(fields=["show_on_teachers_page"], name="users_tp_show_idx"),
        ]

    def __str__(self) -> str:
        """
        Возвращает строковое представление профиля преподавателя.

        Returns:
            str: Пользователь.
        """

        return f"Преподаватель: {self.user}"

    def clean(self) -> None:
        """
        Проверяет согласованность организации и отделения.
        """

        super().clean()

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
