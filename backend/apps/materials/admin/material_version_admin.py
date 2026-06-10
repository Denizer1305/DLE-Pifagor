from __future__ import annotations

from apps.materials.admin.shared import (
    get_single_selected_object,
    run_admin_service_action,
)
from apps.materials.models import MaterialVersion
from apps.materials.services import (
    archive_material_version,
    set_current_material_version,
)
from django.contrib import admin


@admin.action(description="Сделать выбранную версию текущей")
def set_current_material_version_action(modeladmin, request, queryset) -> None:
    """
    Делает выбранную версию текущей.
    """

    version = get_single_selected_object(
        request=request,
        queryset=queryset,
    )

    if version is None:
        return

    run_admin_service_action(
        request=request,
        queryset=queryset,
        service=set_current_material_version,
        object_kwarg="version",
        success_message="Текущая версия материала обновлена.",
    )


@admin.action(description="Архивировать выбранные версии")
def archive_material_versions_action(modeladmin, request, queryset) -> None:
    """
    Архивирует выбранные версии материалов.
    """

    run_admin_service_action(
        request=request,
        queryset=queryset,
        service=archive_material_version,
        object_kwarg="version",
        success_message="Архивировано версий материалов: {count}.",
    )


@admin.register(MaterialVersion)
class MaterialVersionAdmin(admin.ModelAdmin):
    """
    Админка версий учебных материалов.
    """

    list_display = (
        "material",
        "version_number",
        "status",
        "is_current",
        "original_filename",
        "mime_type",
        "file_size_bytes",
        "created_by",
        "created_at",
    )
    list_filter = (
        "status",
        "is_current",
        "material__material_type",
        "material__status",
        "material__visibility",
        "material__organization",
    )
    search_fields = (
        "material__title",
        "material__slug",
        "original_filename",
        "mime_type",
        "checksum",
        "change_log",
        "external_url",
        "created_by__email",
        "created_by__first_name",
        "created_by__last_name",
    )
    raw_id_fields = (
        "material",
        "created_by",
    )
    readonly_fields = (
        "original_filename",
        "file_size_bytes",
        "created_at",
        "updated_at",
    )
    ordering = (
        "material_id",
        "-version_number",
        "-created_at",
    )
    date_hierarchy = "created_at"
    actions = (
        set_current_material_version_action,
        archive_material_versions_action,
    )

    fieldsets = (
        (
            "Материал",
            {
                "fields": (
                    "material",
                    "version_number",
                    "status",
                    "is_current",
                )
            },
        ),
        (
            "Содержимое версии",
            {
                "fields": (
                    "file",
                    "external_url",
                    "content",
                )
            },
        ),
        (
            "Технические данные",
            {
                "fields": (
                    "original_filename",
                    "mime_type",
                    "file_size_bytes",
                    "checksum",
                )
            },
        ),
        (
            "История",
            {
                "fields": (
                    "created_by",
                    "change_log",
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

    def get_queryset(self, request):
        """
        Оптимизирует queryset списка версий.
        """

        return (
            super()
            .get_queryset(request)
            .select_related(
                "material",
                "created_by",
                "material__organization",
                "material__subject",
                "material__category",
            )
        )
