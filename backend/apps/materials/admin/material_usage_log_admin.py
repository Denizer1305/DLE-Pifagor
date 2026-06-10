from __future__ import annotations

from apps.materials.models import MaterialUsageLog
from django.contrib import admin


@admin.register(MaterialUsageLog)
class MaterialUsageLogAdmin(admin.ModelAdmin):
    """
    Админка журнала использования учебных материалов.
    """

    list_display = (
        "material",
        "user",
        "action",
        "context",
        "context_object_id",
        "ip_address",
        "created_at",
    )
    list_filter = (
        "action",
        "context",
        "created_at",
        "material__material_type",
        "material__status",
        "material__organization",
    )
    search_fields = (
        "material__title",
        "material__slug",
        "user__email",
        "user__first_name",
        "user__last_name",
        "ip_address",
        "user_agent",
    )
    raw_id_fields = (
        "material",
        "user",
    )
    readonly_fields = (
        "material",
        "user",
        "action",
        "context",
        "context_object_id",
        "ip_address",
        "user_agent",
        "metadata",
        "created_at",
    )
    ordering = (
        "-created_at",
        "-id",
    )
    date_hierarchy = "created_at"

    fieldsets = (
        (
            "Событие",
            {
                "fields": (
                    "material",
                    "user",
                    "action",
                    "context",
                    "context_object_id",
                )
            },
        ),
        (
            "Технические данные",
            {
                "fields": (
                    "ip_address",
                    "user_agent",
                    "metadata",
                )
            },
        ),
        (
            "Служебная информация",
            {"fields": ("created_at",)},
        ),
    )

    def has_add_permission(self, request) -> bool:
        """
        Запрещает ручное создание событий журнала.
        """

        return False

    def has_change_permission(self, request, obj=None) -> bool:
        """
        Запрещает ручное изменение событий журнала.
        """

        return False

    def get_queryset(self, request):
        """
        Оптимизирует queryset журнала использования.
        """

        return (
            super()
            .get_queryset(request)
            .select_related(
                "material",
                "user",
                "material__organization",
                "material__subject",
                "material__category",
            )
        )
