from __future__ import annotations

from apps.course.admin.shared import run_admin_service_action
from apps.course.services import (
    archive_course_enrollment,
    archive_course_group_access,
    cancel_course_enrollment,
    complete_course_enrollment,
    deactivate_course_access_rule,
    hide_course_for_group,
    restore_course_access_rule,
    show_course_for_group,
    start_course_enrollment,
)
from django.contrib import admin


@admin.action(description="Показать курс выбранным группам")
def show_course_for_groups_action(modeladmin, request, queryset) -> None:
    """
    Показывает курс выбранным группам.
    """

    run_admin_service_action(
        request=request,
        queryset=queryset,
        service=show_course_for_group,
        object_kwarg="group_access",
        success_message="Курс показан группам: {count}.",
    )


@admin.action(description="Скрыть курс от выбранных групп")
def hide_course_for_groups_action(modeladmin, request, queryset) -> None:
    """
    Скрывает курс от выбранных групп.
    """

    run_admin_service_action(
        request=request,
        queryset=queryset,
        service=hide_course_for_group,
        object_kwarg="group_access",
        success_message="Курс скрыт от групп: {count}.",
    )


@admin.action(description="Архивировать выбранные групповые доступы")
def archive_course_group_accesses_action(modeladmin, request, queryset) -> None:
    """
    Архивирует выбранные групповые доступы.
    """

    run_admin_service_action(
        request=request,
        queryset=queryset,
        service=archive_course_group_access,
        object_kwarg="group_access",
        success_message="Архивировано групповых доступов: {count}.",
    )


@admin.action(description="Деактивировать выбранные правила доступа")
def deactivate_course_access_rules_action(modeladmin, request, queryset) -> None:
    """
    Деактивирует выбранные правила доступа.
    """

    run_admin_service_action(
        request=request,
        queryset=queryset,
        service=deactivate_course_access_rule,
        object_kwarg="access_rule",
        success_message="Деактивировано правил доступа: {count}.",
    )


@admin.action(description="Восстановить выбранные правила доступа")
def restore_course_access_rules_action(modeladmin, request, queryset) -> None:
    """
    Восстанавливает выбранные правила доступа.
    """

    run_admin_service_action(
        request=request,
        queryset=queryset,
        service=restore_course_access_rule,
        object_kwarg="access_rule",
        success_message="Восстановлено правил доступа: {count}.",
    )


@admin.action(description="Начать выбранные прохождения курса")
def start_course_enrollments_action(modeladmin, request, queryset) -> None:
    """
    Запускает выбранные записи на курс.
    """

    run_admin_service_action(
        request=request,
        queryset=queryset,
        service=start_course_enrollment,
        object_kwarg="enrollment",
        success_message="Запущено прохождений курса: {count}.",
    )


@admin.action(description="Завершить выбранные прохождения курса")
def complete_course_enrollments_action(modeladmin, request, queryset) -> None:
    """
    Завершает выбранные записи на курс.
    """

    run_admin_service_action(
        request=request,
        queryset=queryset,
        service=complete_course_enrollment,
        object_kwarg="enrollment",
        success_message="Завершено прохождений курса: {count}.",
    )


@admin.action(description="Отменить выбранные записи на курс")
def cancel_course_enrollments_action(modeladmin, request, queryset) -> None:
    """
    Отменяет выбранные записи на курс.
    """

    run_admin_service_action(
        request=request,
        queryset=queryset,
        service=cancel_course_enrollment,
        object_kwarg="enrollment",
        success_message="Отменено записей на курс: {count}.",
    )


@admin.action(description="Архивировать выбранные записи на курс")
def archive_course_enrollments_action(modeladmin, request, queryset) -> None:
    """
    Архивирует выбранные записи на курс.
    """

    run_admin_service_action(
        request=request,
        queryset=queryset,
        service=archive_course_enrollment,
        object_kwarg="enrollment",
        success_message="Архивировано записей на курс: {count}.",
    )
