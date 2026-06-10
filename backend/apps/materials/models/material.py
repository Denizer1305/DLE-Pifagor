from __future__ import annotations

import uuid

from apps.materials.constants import (
    MATERIAL_PREVIEW_UPLOAD_TO,
    MATERIAL_SHORT_DESCRIPTION_MAX_LENGTH,
    MATERIAL_SLUG_MAX_LENGTH,
    MATERIAL_SOURCE_COURSE,
    MATERIAL_SOURCE_EXTERNAL,
    MATERIAL_SOURCE_IMPORT,
    MATERIAL_SOURCE_MANUAL,
    MATERIAL_SOURCE_MAX_LENGTH,
    MATERIAL_SOURCE_UPLOAD,
    MATERIAL_STATUS_ARCHIVED,
    MATERIAL_STATUS_DRAFT,
    MATERIAL_STATUS_MAX_LENGTH,
    MATERIAL_STATUS_PUBLISHED,
    MATERIAL_TITLE_MAX_LENGTH,
    MATERIAL_TYPE_ARCHIVE,
    MATERIAL_TYPE_CODE,
    MATERIAL_TYPE_DOCUMENT,
    MATERIAL_TYPE_EMBED,
    MATERIAL_TYPE_FILE,
    MATERIAL_TYPE_IMAGE,
    MATERIAL_TYPE_LINK,
    MATERIAL_TYPE_MAX_LENGTH,
    MATERIAL_TYPE_OTHER,
    MATERIAL_TYPE_PRESENTATION,
    MATERIAL_TYPE_SPREADSHEET,
    MATERIAL_TYPE_TEXT,
    MATERIAL_TYPE_VIDEO,
    MATERIAL_VISIBILITY_ASSIGNED_ONLY,
    MATERIAL_VISIBILITY_MAX_LENGTH,
    MATERIAL_VISIBILITY_ORGANIZATION,
    MATERIAL_VISIBILITY_PRIVATE,
    MATERIAL_VISIBILITY_PUBLIC,
)
from apps.materials.managers import MaterialManager
from apps.materials.validators import (
    validate_material_publish_dates,
    validate_material_slug,
    validate_material_tags,
    validate_material_visibility_scope,
)
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Material(models.Model):
    """
    Учебный материал.

    Материал является самостоятельной библиотечной сущностью.
    Курсы, уроки и будущие задания подключают материал через связи,
    но сам модуль materials не зависит от course или assignments.
    """

    class MaterialTypeChoices(models.TextChoices):
        FILE = MATERIAL_TYPE_FILE, _("Файл")
        LINK = MATERIAL_TYPE_LINK, _("Ссылка")
        TEXT = MATERIAL_TYPE_TEXT, _("Текст")
        VIDEO = MATERIAL_TYPE_VIDEO, _("Видео")
        IMAGE = MATERIAL_TYPE_IMAGE, _("Изображение")
        PRESENTATION = MATERIAL_TYPE_PRESENTATION, _("Презентация")
        DOCUMENT = MATERIAL_TYPE_DOCUMENT, _("Документ")
        SPREADSHEET = MATERIAL_TYPE_SPREADSHEET, _("Таблица")
        ARCHIVE = MATERIAL_TYPE_ARCHIVE, _("Архив")
        CODE = MATERIAL_TYPE_CODE, _("Код")
        EMBED = MATERIAL_TYPE_EMBED, _("Встраиваемый материал")
        OTHER = MATERIAL_TYPE_OTHER, _("Другое")

    class StatusChoices(models.TextChoices):
        DRAFT = MATERIAL_STATUS_DRAFT, _("Черновик")
        PUBLISHED = MATERIAL_STATUS_PUBLISHED, _("Опубликован")
        ARCHIVED = MATERIAL_STATUS_ARCHIVED, _("Архивирован")

    class VisibilityChoices(models.TextChoices):
        PRIVATE = MATERIAL_VISIBILITY_PRIVATE, _("Приватный")
        ORGANIZATION = MATERIAL_VISIBILITY_ORGANIZATION, _("Внутри организации")
        ASSIGNED_ONLY = MATERIAL_VISIBILITY_ASSIGNED_ONLY, _("Только назначенным")
        PUBLIC = MATERIAL_VISIBILITY_PUBLIC, _("Публичный")

    class SourceChoices(models.TextChoices):
        MANUAL = MATERIAL_SOURCE_MANUAL, _("Создан вручную")
        UPLOAD = MATERIAL_SOURCE_UPLOAD, _("Загружен")
        IMPORT = MATERIAL_SOURCE_IMPORT, _("Импортирован")
        EXTERNAL = MATERIAL_SOURCE_EXTERNAL, _("Внешний источник")
        COURSE = MATERIAL_SOURCE_COURSE, _("Создан из курса")

    uid = models.UUIDField(
        _("Публичный идентификатор"),
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )
    title = models.CharField(
        _("Название"),
        max_length=MATERIAL_TITLE_MAX_LENGTH,
    )
    slug = models.SlugField(
        _("Slug"),
        max_length=MATERIAL_SLUG_MAX_LENGTH,
        unique=True,
        validators=[validate_material_slug],
    )

    short_description = models.CharField(
        _("Краткое описание"),
        max_length=MATERIAL_SHORT_DESCRIPTION_MAX_LENGTH,
        blank=True,
    )
    description = models.TextField(
        _("Описание"),
        blank=True,
    )

    material_type = models.CharField(
        _("Тип материала"),
        max_length=MATERIAL_TYPE_MAX_LENGTH,
        choices=MaterialTypeChoices.choices,
        default=MaterialTypeChoices.FILE,
    )
    status = models.CharField(
        _("Статус"),
        max_length=MATERIAL_STATUS_MAX_LENGTH,
        choices=StatusChoices.choices,
        default=StatusChoices.DRAFT,
    )
    visibility = models.CharField(
        _("Видимость"),
        max_length=MATERIAL_VISIBILITY_MAX_LENGTH,
        choices=VisibilityChoices.choices,
        default=VisibilityChoices.PRIVATE,
    )
    source = models.CharField(
        _("Источник"),
        max_length=MATERIAL_SOURCE_MAX_LENGTH,
        choices=SourceChoices.choices,
        default=SourceChoices.MANUAL,
    )

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="materials",
        verbose_name=_("Организация"),
        blank=True,
        null=True,
    )
    subject = models.ForeignKey(
        "organizations.Subject",
        on_delete=models.PROTECT,
        related_name="materials",
        verbose_name=_("Предмет"),
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        "materials.MaterialCategory",
        on_delete=models.SET_NULL,
        related_name="materials",
        verbose_name=_("Категория"),
        blank=True,
        null=True,
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="owned_materials",
        verbose_name=_("Владелец"),
        blank=True,
        null=True,
    )

    current_version = models.ForeignKey(
        "materials.MaterialVersion",
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Текущая версия"),
        blank=True,
        null=True,
    )

    tags = models.JSONField(
        _("Теги"),
        default=list,
        blank=True,
        validators=[validate_material_tags],
    )
    preview_image = models.FileField(
        _("Изображение предпросмотра"),
        upload_to=MATERIAL_PREVIEW_UPLOAD_TO,
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(
        _("Активен"),
        default=True,
    )
    published_at = models.DateTimeField(
        _("Дата публикации"),
        blank=True,
        null=True,
    )
    archived_at = models.DateTimeField(
        _("Дата архивации"),
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        _("Дата создания"),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        _("Дата обновления"),
        auto_now=True,
    )

    objects = MaterialManager()

    class Meta:
        db_table = "materials_material"
        verbose_name = _("Учебный материал")
        verbose_name_plural = _("Учебные материалы")
        ordering = (
            "organization_id",
            "category_id",
            "-updated_at",
            "title",
        )
        indexes = [
            models.Index(
                fields=("slug",),
                name="mat_material_slug_idx",
            ),
            models.Index(
                fields=("material_type",),
                name="mat_material_type_idx",
            ),
            models.Index(
                fields=("status",),
                name="mat_material_status_idx",
            ),
            models.Index(
                fields=("visibility",),
                name="mat_material_vis_idx",
            ),
            models.Index(
                fields=("source",),
                name="mat_material_source_idx",
            ),
            models.Index(
                fields=("organization",),
                name="mat_material_org_idx",
            ),
            models.Index(
                fields=("subject",),
                name="mat_material_subject_idx",
            ),
            models.Index(
                fields=("category",),
                name="mat_material_category_idx",
            ),
            models.Index(
                fields=("owner",),
                name="mat_material_owner_idx",
            ),
            models.Index(
                fields=("is_active",),
                name="mat_material_active_idx",
            ),
        ]

    def __str__(self) -> str:
        return self.title

    def clean(self) -> None:
        """
        Проверяет материал.
        """

        super().clean()

        errors: dict[str, str] = {}

        try:
            validate_material_visibility_scope(
                visibility=self.visibility,
                organization=self.organization,
            )
        except ValidationError as error:
            errors.update(error.message_dict)

        try:
            validate_material_publish_dates(
                published_at=self.published_at,
                archived_at=self.archived_at,
            )
        except ValidationError as error:
            errors.update(error.message_dict)

        if self.category_id:
            if self.category.organization_id and self.organization_id:
                if self.category.organization_id != self.organization_id:
                    errors["category"] = _(
                        "Категория должна относиться к той же организации."
                    )

            if self.category.organization_id and not self.organization_id:
                errors["organization"] = _(
                    "Для материала в организационной категории нужна организация."
                )

        if self.current_version_id and self.pk:
            if self.current_version.material_id != self.pk:
                errors["current_version"] = _(
                    "Текущая версия должна относиться к этому материалу."
                )

        if self.status == self.StatusChoices.PUBLISHED and not self.published_at:
            self.published_at = timezone.now()

        if self.status == self.StatusChoices.ARCHIVED:
            self.is_active = False

            if not self.archived_at:
                self.archived_at = timezone.now()

        if errors:
            raise ValidationError(errors)
