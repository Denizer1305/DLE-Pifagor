from __future__ import annotations

from apps.education.admin.shared import (
    get_single_selected_object,
    run_admin_service_action,
)
from apps.education.services import (
    deactivate_teacher_group_subject,
    restore_teacher_group_subject,
    set_primary_teacher_group_subject,
)
from django.contrib import admin


@admin.action(description="Сделать выбранное назначение основным")
def set_primary_teacher_group_subject_action(modeladmin, request, queryset) -> None:
    """
    Делает выбранное назначение основным.
    """

    assignment = get_single_selected_object(
        request=request,
        queryset=queryset,
    )

    if assignment is None:
        return

    run_admin_service_action(
        request=request,
        queryset=queryset,
        service=set_primary_teacher_group_subject,
        object_kwarg="assignment",
        success_message="Основное назначение преподавателя обновлено.",
    )


@admin.action(description="Деактивировать выбранные назначения")
def deactivate_teacher_group_subjects_action(modeladmin, request, queryset) -> None:
    """
    Деактивирует назначения преподавателей.
    """

    run_admin_service_action(
        request=request,
        queryset=queryset,
        service=deactivate_teacher_group_subject,
        object_kwarg="assignment",
        success_message="Деактивировано назначений преподавателей: {count}.",
    )


@admin.action(description="Восстановить выбранные назначения")
def restore_teacher_group_subjects_action(modeladmin, request, queryset) -> None:
    """
    Восстанавливает назначения преподавателей.
    """

    run_admin_service_action(
        request=request,
        queryset=queryset,
        service=restore_teacher_group_subject,
        object_kwarg="assignment",
        success_message="Восстановлено назначений преподавателей: {count}.",
    )
