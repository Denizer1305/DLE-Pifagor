from __future__ import annotations

from apps.education.admin.shared import (
    get_single_selected_object,
    run_admin_service_action,
)
from apps.education.services import (
    deactivate_academic_year,
    restore_academic_year,
    set_current_academic_year,
)
from django.contrib import admin


@admin.action(description="Сделать выбранный учебный год текущим")
def set_current_academic_year_action(modeladmin, request, queryset) -> None:
    """
    Делает выбранный учебный год текущим.
    """

    academic_year = get_single_selected_object(
        request=request,
        queryset=queryset,
    )

    if academic_year is None:
        return

    run_admin_service_action(
        request=request,
        queryset=queryset,
        service=set_current_academic_year,
        object_kwarg="academic_year",
        success_message="Текущий учебный год обновлён.",
    )


@admin.action(description="Деактивировать выбранные учебные годы")
def deactivate_academic_years_action(modeladmin, request, queryset) -> None:
    """
    Деактивирует учебные годы.
    """

    run_admin_service_action(
        request=request,
        queryset=queryset,
        service=deactivate_academic_year,
        object_kwarg="academic_year",
        success_message="Деактивировано учебных годов: {count}.",
    )


@admin.action(description="Восстановить выбранные учебные годы")
def restore_academic_years_action(modeladmin, request, queryset) -> None:
    """
    Восстанавливает учебные годы.
    """

    run_admin_service_action(
        request=request,
        queryset=queryset,
        service=restore_academic_year,
        object_kwarg="academic_year",
        success_message="Восстановлено учебных годов: {count}.",
    )
