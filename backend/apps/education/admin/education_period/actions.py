from __future__ import annotations

from apps.education.admin.shared import (
    get_single_selected_object,
    run_admin_service_action,
)
from apps.education.services import (
    deactivate_education_period,
    restore_education_period,
    set_current_education_period,
)
from django.contrib import admin


@admin.action(description="Сделать выбранный период текущим")
def set_current_education_period_action(modeladmin, request, queryset) -> None:
    """
    Делает выбранный учебный период текущим.
    """

    period = get_single_selected_object(
        request=request,
        queryset=queryset,
    )

    if period is None:
        return

    run_admin_service_action(
        request=request,
        queryset=queryset,
        service=set_current_education_period,
        object_kwarg="period",
        success_message="Текущий учебный период обновлён.",
    )


@admin.action(description="Деактивировать выбранные периоды")
def deactivate_education_periods_action(modeladmin, request, queryset) -> None:
    """
    Деактивирует учебные периоды.
    """

    run_admin_service_action(
        request=request,
        queryset=queryset,
        service=deactivate_education_period,
        object_kwarg="period",
        success_message="Деактивировано учебных периодов: {count}.",
    )


@admin.action(description="Восстановить выбранные периоды")
def restore_education_periods_action(modeladmin, request, queryset) -> None:
    """
    Восстанавливает учебные периоды.
    """

    run_admin_service_action(
        request=request,
        queryset=queryset,
        service=restore_education_period,
        object_kwarg="period",
        success_message="Восстановлено учебных периодов: {count}.",
    )
