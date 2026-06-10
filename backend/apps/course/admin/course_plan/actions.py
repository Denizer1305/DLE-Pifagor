from __future__ import annotations

from apps.course.admin.shared import run_admin_service_action
from apps.course.services import (
    approve_course_plan,
    archive_course_plan,
    mark_course_plan_reviewed,
)
from django.contrib import admin


@admin.action(description="Пометить выбранные КТП как проверенные")
def review_course_plans_action(modeladmin, request, queryset) -> None:
    """
    Помечает выбранные КТП как проверенные.
    """

    run_admin_service_action(
        request=request,
        queryset=queryset,
        service=mark_course_plan_reviewed,
        object_kwarg="plan",
        success_message="Проверено КТП: {count}.",
    )


@admin.action(description="Утвердить выбранные КТП")
def approve_course_plans_action(modeladmin, request, queryset) -> None:
    """
    Утверждает выбранные КТП.
    """

    run_admin_service_action(
        request=request,
        queryset=queryset,
        service=approve_course_plan,
        object_kwarg="plan",
        success_message="Утверждено КТП: {count}.",
    )


@admin.action(description="Архивировать выбранные КТП")
def archive_course_plans_action(modeladmin, request, queryset) -> None:
    """
    Архивирует выбранные КТП.
    """

    run_admin_service_action(
        request=request,
        queryset=queryset,
        service=archive_course_plan,
        object_kwarg="plan",
        success_message="Архивировано КТП: {count}.",
    )
