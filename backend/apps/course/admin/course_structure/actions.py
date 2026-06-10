from __future__ import annotations

from apps.course.admin.shared import run_admin_service_action
from apps.course.services import (
    archive_course_lesson,
    archive_course_section,
    hide_course_lesson_block,
    hide_course_material_link,
    publish_course_lesson,
    publish_course_section,
    show_course_lesson_block,
    show_course_material_link,
)
from django.contrib import admin


@admin.action(description="Опубликовать выбранные разделы")
def publish_course_sections_action(modeladmin, request, queryset) -> None:
    """
    Публикует выбранные разделы.
    """

    run_admin_service_action(
        request=request,
        queryset=queryset,
        service=publish_course_section,
        object_kwarg="section",
        success_message="Опубликовано разделов: {count}.",
    )


@admin.action(description="Архивировать выбранные разделы")
def archive_course_sections_action(modeladmin, request, queryset) -> None:
    """
    Архивирует выбранные разделы.
    """

    run_admin_service_action(
        request=request,
        queryset=queryset,
        service=archive_course_section,
        object_kwarg="section",
        success_message="Архивировано разделов: {count}.",
    )


@admin.action(description="Опубликовать выбранные уроки")
def publish_course_lessons_action(modeladmin, request, queryset) -> None:
    """
    Публикует выбранные уроки.
    """

    run_admin_service_action(
        request=request,
        queryset=queryset,
        service=publish_course_lesson,
        object_kwarg="lesson",
        success_message="Опубликовано уроков: {count}.",
    )


@admin.action(description="Архивировать выбранные уроки")
def archive_course_lessons_action(modeladmin, request, queryset) -> None:
    """
    Архивирует выбранные уроки.
    """

    run_admin_service_action(
        request=request,
        queryset=queryset,
        service=archive_course_lesson,
        object_kwarg="lesson",
        success_message="Архивировано уроков: {count}.",
    )


@admin.action(description="Показать выбранные блоки уроков")
def show_course_lesson_blocks_action(modeladmin, request, queryset) -> None:
    """
    Показывает выбранные блоки уроков.
    """

    run_admin_service_action(
        request=request,
        queryset=queryset,
        service=show_course_lesson_block,
        object_kwarg="block",
        success_message="Показано блоков уроков: {count}.",
    )


@admin.action(description="Скрыть выбранные блоки уроков")
def hide_course_lesson_blocks_action(modeladmin, request, queryset) -> None:
    """
    Скрывает выбранные блоки уроков.
    """

    run_admin_service_action(
        request=request,
        queryset=queryset,
        service=hide_course_lesson_block,
        object_kwarg="block",
        success_message="Скрыто блоков уроков: {count}.",
    )


@admin.action(description="Показать выбранные материалы курса")
def show_course_material_links_action(modeladmin, request, queryset) -> None:
    """
    Показывает выбранные материалы курса.
    """

    run_admin_service_action(
        request=request,
        queryset=queryset,
        service=show_course_material_link,
        object_kwarg="link",
        success_message="Показано материалов курса: {count}.",
    )


@admin.action(description="Скрыть выбранные материалы курса")
def hide_course_material_links_action(modeladmin, request, queryset) -> None:
    """
    Скрывает выбранные материалы курса.
    """

    run_admin_service_action(
        request=request,
        queryset=queryset,
        service=hide_course_material_link,
        object_kwarg="link",
        success_message="Скрыто материалов курса: {count}.",
    )
