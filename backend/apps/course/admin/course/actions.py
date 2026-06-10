from __future__ import annotations

from apps.course.admin.shared import run_admin_service_action
from apps.course.services import archive_course, publish_course, restore_course
from django.contrib import admin


@admin.action(description="Опубликовать выбранные курсы")
def publish_courses_action(modeladmin, request, queryset) -> None:
    """
    Публикует выбранные курсы.
    """

    run_admin_service_action(
        request=request,
        queryset=queryset,
        service=publish_course,
        object_kwarg="course",
        success_message="Опубликовано курсов: {count}.",
    )


@admin.action(description="Архивировать выбранные курсы")
def archive_courses_action(modeladmin, request, queryset) -> None:
    """
    Архивирует выбранные курсы.
    """

    run_admin_service_action(
        request=request,
        queryset=queryset,
        service=archive_course,
        object_kwarg="course",
        success_message="Архивировано курсов: {count}.",
    )


@admin.action(description="Восстановить выбранные курсы")
def restore_courses_action(modeladmin, request, queryset) -> None:
    """
    Восстанавливает выбранные курсы.
    """

    run_admin_service_action(
        request=request,
        queryset=queryset,
        service=restore_course,
        object_kwarg="course",
        success_message="Восстановлено курсов: {count}.",
    )
