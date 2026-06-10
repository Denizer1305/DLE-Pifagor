from __future__ import annotations

from apps.materials.admin.shared import run_admin_service_action
from apps.materials.models import Material, MaterialUsageLog, MaterialVersion
from apps.materials.services import archive_material, publish_material, restore_material
from django.contrib import admin


class MaterialVersionInline(admin.TabularInline):
    """
    Inline версий материала.
    """

    model = MaterialVersion
    extra = 0
    show_change_link = True

    fields = (
        "version_number",
        "status",
        "is_current",
        "original_filename",
        "mime_type",
        "file_size_bytes",
        "created_by",
        "created_at",
    )
    readonly_fields = (
        "original_filename",
        "mime_type",
        "file_size_bytes",
        "created_at",
    )
    raw_id_fields = ("created_by",)
    ordering = (
        "-version_number",
        "-created_at",
    )


class MaterialUsageLogInline(admin.TabularInline):
    """
    Inline журнала использования материала.
    """

    model = MaterialUsageLog
    extra = 0
    show_change_link = True
    can_delete = False

    fields = (
        "user",
        "action",
        "context",
        "context_object_id",
        "ip_address",
        "created_at",
    )
    readonly_fields = (
        "user",
        "action",
        "context",
        "context_object_id",
        "ip_address",
        "created_at",
    )
    ordering = (
        "-created_at",
        "-id",
    )

    def has_add_permission(self, request, obj=None) -> bool:
        """
        Запрещает ручное добавление событий журнала из inline.
        """

        return False

    def has_change_permission(self, request, obj=None) -> bool:
        """
        Запрещает ручное изменение событий журнала из inline.
        """

        return False


@admin.action(description="Опубликовать выбранные материалы")
def publish_materials_action(modeladmin, request, queryset) -> None:
    """
    Публикует выбранные материалы.
    """

    run_admin_service_action(
        request=request,
        queryset=queryset,
        service=publish_material,
        object_kwarg="material",
        success_message="Опубликовано материалов: {count}.",
    )


@admin.action(description="Архивировать выбранные материалы")
def archive_materials_action(modeladmin, request, queryset) -> None:
    """
    Архивирует выбранные материалы.
    """

    run_admin_service_action(
        request=request,
        queryset=queryset,
        service=archive_material,
        object_kwarg="material",
        success_message="Архивировано материалов: {count}.",
    )


@admin.action(description="Восстановить выбранные материалы")
def restore_materials_action(modeladmin, request, queryset) -> None:
    """
    Восстанавливает выбранные материалы в черновики.
    """

    run_admin_service_action(
        request=request,
        queryset=queryset,
        service=restore_material,
        object_kwarg="material",
        success_message="Восстановлено материалов: {count}.",
    )


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    """
    Админка учебных материалов.
    """

    list_display = (
        "title",
        "material_type",
        "status",
        "visibility",
        "organization",
        "subject",
        "category",
        "owner",
        "current_version_number",
        "is_active",
        "updated_at",
    )
    list_filter = (
        "material_type",
        "status",
        "visibility",
        "source",
        "is_active",
        "organization",
        "subject",
        "category",
    )
    search_fields = (
        "title",
        "slug",
        "short_description",
        "description",
        "organization__name",
        "organization__short_name",
        "organization__code",
        "subject__name",
        "subject__short_name",
        "subject__code",
        "category__name",
        "category__slug",
        "owner__email",
        "owner__first_name",
        "owner__last_name",
    )
    raw_id_fields = (
        "organization",
        "subject",
        "category",
        "owner",
        "current_version",
    )
    readonly_fields = (
        "uid",
        "published_at",
        "archived_at",
        "created_at",
        "updated_at",
    )
    ordering = (
        "organization_id",
        "category_id",
        "-updated_at",
        "title",
    )
    date_hierarchy = "created_at"
    inlines = (
        MaterialVersionInline,
        MaterialUsageLogInline,
    )
    actions = (
        publish_materials_action,
        archive_materials_action,
        restore_materials_action,
    )

    fieldsets = (
        (
            "Основная информация",
            {
                "fields": (
                    "uid",
                    "title",
                    "slug",
                    "short_description",
                    "description",
                )
            },
        ),
        (
            "Классификация",
            {
                "fields": (
                    "material_type",
                    "status",
                    "visibility",
                    "source",
                    "tags",
                )
            },
        ),
        (
            "Связи",
            {
                "fields": (
                    "organization",
                    "subject",
                    "category",
                    "owner",
                    "current_version",
                )
            },
        ),
        (
            "Медиа",
            {"fields": ("preview_image",)},
        ),
        (
            "Статусы и даты",
            {
                "fields": (
                    "is_active",
                    "published_at",
                    "archived_at",
                )
            },
        ),
        (
            "Служебная информация",
            {
                "classes": ("collapse",),
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )

    @admin.display(description="Текущая версия")
    def current_version_number(self, obj: Material) -> str:
        """
        Возвращает номер текущей версии материала.
        """

        if not obj.current_version_id:
            return "—"

        return f"v{obj.current_version.version_number}"

    def get_queryset(self, request):
        """
        Оптимизирует queryset списка материалов.
        """

        return (
            super()
            .get_queryset(request)
            .select_related(
                "organization",
                "subject",
                "category",
                "owner",
                "current_version",
            )
        )
