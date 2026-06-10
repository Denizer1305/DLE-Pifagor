from __future__ import annotations

from apps.materials.admin.shared import run_admin_service_action
from apps.materials.models import MaterialCategory
from apps.materials.services import (
    deactivate_material_category,
    restore_material_category,
)
from django.contrib import admin


class MaterialCategoryChildInline(admin.TabularInline):
    """
    Inline дочерних категорий материалов.
    """

    model = MaterialCategory
    fk_name = "parent"
    extra = 0
    show_change_link = True

    fields = (
        "name",
        "slug",
        "organization",
        "is_active",
    )
    raw_id_fields = ("organization",)


@admin.action(description="Деактивировать выбранные категории")
def deactivate_material_categories_action(modeladmin, request, queryset) -> None:
    """
    Деактивирует выбранные категории материалов.
    """

    run_admin_service_action(
        request=request,
        queryset=queryset,
        service=deactivate_material_category,
        object_kwarg="category",
        success_message="Деактивировано категорий материалов: {count}.",
    )


@admin.action(description="Восстановить выбранные категории")
def restore_material_categories_action(modeladmin, request, queryset) -> None:
    """
    Восстанавливает выбранные категории материалов.
    """

    run_admin_service_action(
        request=request,
        queryset=queryset,
        service=restore_material_category,
        object_kwarg="category",
        success_message="Восстановлено категорий материалов: {count}.",
    )


@admin.register(MaterialCategory)
class MaterialCategoryAdmin(admin.ModelAdmin):
    """
    Админка категорий учебных материалов.
    """

    list_display = (
        "name",
        "slug",
        "organization",
        "parent",
        "is_active",
        "materials_count",
        "children_count",
        "updated_at",
    )
    list_filter = (
        "is_active",
        "organization",
        "parent",
    )
    search_fields = (
        "name",
        "slug",
        "description",
        "organization__name",
        "organization__short_name",
        "organization__code",
        "parent__name",
        "parent__slug",
    )
    raw_id_fields = (
        "organization",
        "parent",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    ordering = (
        "organization_id",
        "parent_id",
        "name",
    )
    inlines = (MaterialCategoryChildInline,)
    actions = (
        deactivate_material_categories_action,
        restore_material_categories_action,
    )

    fieldsets = (
        (
            "Связи",
            {
                "fields": (
                    "organization",
                    "parent",
                )
            },
        ),
        (
            "Основная информация",
            {
                "fields": (
                    "name",
                    "slug",
                    "description",
                    "is_active",
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

    @admin.display(description="Материалов")
    def materials_count(self, obj: MaterialCategory) -> int:
        """
        Возвращает количество материалов категории.
        """

        return obj.materials.count()

    @admin.display(description="Подкатегорий")
    def children_count(self, obj: MaterialCategory) -> int:
        """
        Возвращает количество дочерних категорий.
        """

        return obj.children.count()
