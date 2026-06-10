from __future__ import annotations

from apps.education.admin.shared import run_admin_service_action
from apps.education.services import (
    activate_curriculum,
    archive_curriculum,
    restore_curriculum,
)
from django.contrib import admin


@admin.action(description="Активировать выбранные учебные планы")
def activate_curricula_action(modeladmin, request, queryset) -> None:
    """
    Активирует учебные планы.
    """

    run_admin_service_action(
        request=request,
        queryset=queryset,
        service=activate_curriculum,
        object_kwarg="curriculum",
        success_message="Активировано учебных планов: {count}.",
    )


@admin.action(description="Архивировать выбранные учебные планы")
def archive_curricula_action(modeladmin, request, queryset) -> None:
    """
    Архивирует учебные планы.
    """

    run_admin_service_action(
        request=request,
        queryset=queryset,
        service=archive_curriculum,
        object_kwarg="curriculum",
        success_message="Архивировано учебных планов: {count}.",
    )


@admin.action(description="Восстановить выбранные учебные планы")
def restore_curricula_action(modeladmin, request, queryset) -> None:
    """
    Восстанавливает учебные планы.
    """

    run_admin_service_action(
        request=request,
        queryset=queryset,
        service=restore_curriculum,
        object_kwarg="curriculum",
        success_message="Восстановлено учебных планов: {count}.",
    )
