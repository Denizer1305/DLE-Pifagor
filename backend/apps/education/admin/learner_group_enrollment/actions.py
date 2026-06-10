from __future__ import annotations

from apps.education.admin.shared import (
    get_single_selected_object,
    run_admin_service_action,
)
from apps.education.services import (
    archive_learner_group_enrollment,
    set_primary_learner_group_enrollment,
)
from django.contrib import admin
from django.utils import timezone


@admin.action(description="Сделать выбранное зачисление основным")
def set_primary_learner_enrollment_action(modeladmin, request, queryset) -> None:
    """
    Делает выбранное зачисление основным.
    """

    enrollment = get_single_selected_object(
        request=request,
        queryset=queryset,
    )

    if enrollment is None:
        return

    run_admin_service_action(
        request=request,
        queryset=queryset,
        service=set_primary_learner_group_enrollment,
        object_kwarg="enrollment",
        success_message="Основное зачисление обновлено.",
    )


@admin.action(description="Архивировать выбранные зачисления")
def archive_learner_enrollments_action(modeladmin, request, queryset) -> None:
    """
    Архивирует академические зачисления.

    Дату завершения подбирает безопасно внутри границ учебного года.
    """

    updated_count = 0

    for enrollment in queryset:
        current_date = timezone.localdate()
        completion_date = current_date

        if completion_date < enrollment.enrollment_date:
            completion_date = enrollment.enrollment_date

        if completion_date > enrollment.academic_year.end_date:
            completion_date = enrollment.academic_year.end_date

        archive_learner_group_enrollment(
            enrollment=enrollment,
            completion_date=completion_date,
        )
        updated_count += 1

    if updated_count:
        modeladmin.message_user(
            request,
            f"Архивировано зачислений: {updated_count}.",
        )
