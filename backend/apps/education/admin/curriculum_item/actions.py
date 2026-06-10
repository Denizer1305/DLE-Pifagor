from __future__ import annotations

from apps.education.admin.shared import run_admin_service_action
from apps.education.services import deactivate_curriculum_item, restore_curriculum_item
from django.contrib import admin


@admin.action(description="Деактивировать выбранные элементы учебного плана")
def deactivate_curriculum_items_action(modeladmin, request, queryset) -> None:
    """
    Деактивирует элементы учебного плана.
    """

    run_admin_service_action(
        request=request,
        queryset=queryset,
        service=deactivate_curriculum_item,
        object_kwarg="curriculum_item",
        success_message="Деактивировано элементов учебного плана: {count}.",
    )


@admin.action(description="Восстановить выбранные элементы учебного плана")
def restore_curriculum_items_action(modeladmin, request, queryset) -> None:
    """
    Восстанавливает элементы учебного плана.
    """

    run_admin_service_action(
        request=request,
        queryset=queryset,
        service=restore_curriculum_item,
        object_kwarg="curriculum_item",
        success_message="Восстановлено элементов учебного плана: {count}.",
    )
