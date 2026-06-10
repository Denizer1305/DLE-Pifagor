from __future__ import annotations

from apps.education.admin.shared import run_admin_service_action
from apps.education.services import deactivate_group_subject, restore_group_subject
from django.contrib import admin


@admin.action(description="Деактивировать выбранные предметы групп")
def deactivate_group_subjects_action(modeladmin, request, queryset) -> None:
    """
    Деактивирует предметы групп.
    """

    run_admin_service_action(
        request=request,
        queryset=queryset,
        service=deactivate_group_subject,
        object_kwarg="group_subject",
        success_message="Деактивировано предметов групп: {count}.",
    )


@admin.action(description="Восстановить выбранные предметы групп")
def restore_group_subjects_action(modeladmin, request, queryset) -> None:
    """
    Восстанавливает предметы групп.
    """

    run_admin_service_action(
        request=request,
        queryset=queryset,
        service=restore_group_subject,
        object_kwarg="group_subject",
        success_message="Восстановлено предметов групп: {count}.",
    )
