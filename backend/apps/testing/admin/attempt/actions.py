from __future__ import annotations

from apps.testing.admin.test.actions import messages_action
from apps.testing.services import publish_attempt_result
from apps.testing.tasks import auto_check_attempt_task
from django.contrib import messages
from django.core.exceptions import ValidationError


@messages_action("Выбранные попытки отправлены на автопроверку.")
def auto_check_attempts(modeladmin, request, queryset) -> None:
    """
    Запускает автопроверку выбранных попыток.
    """

    for attempt in queryset:
        auto_check_attempt_task(attempt_id=attempt.id)


def publish_attempt_results(modeladmin, request, queryset) -> None:
    """
    Публикует подтверждённые результаты попыток.
    """

    published_count = 0
    failed_count = 0

    for attempt in queryset:
        try:
            publish_attempt_result(attempt=attempt)
            published_count += 1
        except ValidationError:
            failed_count += 1

    if published_count:
        modeladmin.message_user(
            request,
            f"Опубликовано результатов: {published_count}.",
            level=messages.SUCCESS,
        )

    if failed_count:
        modeladmin.message_user(
            request,
            (
                "Не удалось опубликовать результатов: "
                f"{failed_count}. Проверьте подтверждение оценок."
            ),
            level=messages.WARNING,
        )


publish_attempt_results.short_description = "Опубликовать подтверждённые результаты"
