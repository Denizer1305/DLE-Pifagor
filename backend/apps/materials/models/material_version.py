from __future__ import annotations

from apps.materials.constants import (
    DEFAULT_MATERIAL_VERSION_NUMBER,
    MATERIAL_EXTERNAL_URL_MAX_LENGTH,
    MATERIAL_FILE_UPLOAD_TO,
    MATERIAL_ORIGINAL_FILENAME_MAX_LENGTH,
    MATERIAL_VERSION_CHANGE_LOG_MAX_LENGTH,
    MATERIAL_VERSION_CHECKSUM_MAX_LENGTH,
    MATERIAL_VERSION_MIME_TYPE_MAX_LENGTH,
    MATERIAL_VERSION_STATUS_ARCHIVED,
    MATERIAL_VERSION_STATUS_CURRENT,
    MATERIAL_VERSION_STATUS_DRAFT,
    MATERIAL_VERSION_STATUS_MAX_LENGTH,
)
from apps.materials.managers import MaterialVersionManager
from apps.materials.validators import (
    validate_current_version_flags,
    validate_material_file_size,
    validate_material_version_number,
    validate_material_version_payload,
)
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class MaterialVersion(models.Model):
    """
    Версия учебного материала.

    Версионность позволяет обновлять файл, ссылку или текст материала
    без потери истории изменений.
    """

    class StatusChoices(models.TextChoices):
        DRAFT = MATERIAL_VERSION_STATUS_DRAFT, _("Черновик")
        CURRENT = MATERIAL_VERSION_STATUS_CURRENT, _("Текущая")
        ARCHIVED = MATERIAL_VERSION_STATUS_ARCHIVED, _("Архивная")

    material = models.ForeignKey(
        "materials.Material",
        on_delete=models.CASCADE,
        related_name="versions",
        verbose_name=_("Материал"),
    )
    version_number = models.PositiveIntegerField(
        _("Номер версии"),
        default=DEFAULT_MATERIAL_VERSION_NUMBER,
        validators=[validate_material_version_number],
    )
    status = models.CharField(
        _("Статус версии"),
        max_length=MATERIAL_VERSION_STATUS_MAX_LENGTH,
        choices=StatusChoices.choices,
        default=StatusChoices.DRAFT,
    )

    file = models.FileField(
        _("Файл"),
        upload_to=MATERIAL_FILE_UPLOAD_TO,
        validators=[validate_material_file_size],
        blank=True,
        null=True,
    )
    external_url = models.URLField(
        _("Внешняя ссылка"),
        max_length=MATERIAL_EXTERNAL_URL_MAX_LENGTH,
        blank=True,
    )
    content = models.TextField(
        _("Текстовое содержимое"),
        blank=True,
    )

    original_filename = models.CharField(
        _("Исходное имя файла"),
        max_length=MATERIAL_ORIGINAL_FILENAME_MAX_LENGTH,
        blank=True,
    )
    mime_type = models.CharField(
        _("MIME-тип"),
        max_length=MATERIAL_VERSION_MIME_TYPE_MAX_LENGTH,
        blank=True,
    )
    file_size_bytes = models.PositiveBigIntegerField(
        _("Размер файла, байт"),
        blank=True,
        null=True,
    )
    checksum = models.CharField(
        _("Контрольная сумма"),
        max_length=MATERIAL_VERSION_CHECKSUM_MAX_LENGTH,
        blank=True,
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="created_material_versions",
        verbose_name=_("Кем создана версия"),
        blank=True,
        null=True,
    )
    change_log = models.CharField(
        _("Описание изменений"),
        max_length=MATERIAL_VERSION_CHANGE_LOG_MAX_LENGTH,
        blank=True,
    )
    is_current = models.BooleanField(
        _("Текущая версия"),
        default=False,
    )

    created_at = models.DateTimeField(
        _("Дата создания"),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        _("Дата обновления"),
        auto_now=True,
    )

    objects = MaterialVersionManager()

    class Meta:
        db_table = "materials_version"
        verbose_name = _("Версия материала")
        verbose_name_plural = _("Версии материалов")
        ordering = (
            "material_id",
            "-version_number",
            "-created_at",
        )
        constraints = [
            models.UniqueConstraint(
                fields=(
                    "material",
                    "version_number",
                ),
                name="mat_ver_unique_number",
            ),
            models.UniqueConstraint(
                fields=("material",),
                condition=models.Q(is_current=True),
                name="mat_ver_unique_current",
            ),
        ]
        indexes = [
            models.Index(
                fields=("material",),
                name="mat_version_material_idx",
            ),
            models.Index(
                fields=("status",),
                name="mat_version_status_idx",
            ),
            models.Index(
                fields=("is_current",),
                name="mat_version_current_idx",
            ),
            models.Index(
                fields=("created_by",),
                name="mat_version_creator_idx",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.material} v{self.version_number}"

    def clean(self) -> None:
        """
        Проверяет версию материала.
        """

        super().clean()

        errors: dict[str, str] = {}

        try:
            validate_material_version_payload(
                material_type=self.material.material_type,
                file=self.file,
                external_url=self.external_url,
                content=self.content,
            )
        except ValidationError as error:
            errors.update(error.message_dict)

        try:
            validate_current_version_flags(
                is_current=self.is_current,
                status=self.status,
            )
        except ValidationError as error:
            errors.update(error.message_dict)

        if self.file:
            if not self.original_filename:
                self.original_filename = self.file.name

            file_size = getattr(self.file, "size", None)

            if file_size is not None:
                self.file_size_bytes = file_size

        if self.is_current and self.status != self.StatusChoices.CURRENT:
            self.status = self.StatusChoices.CURRENT

        if self.status == self.StatusChoices.CURRENT:
            self.is_current = True

        if errors:
            raise ValidationError(errors)
