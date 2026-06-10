from __future__ import annotations

from apps.testing.services import (
    hide_learner_result,
    publish_learner_result,
    recalculate_learner_result,
)
from django.contrib import messages
from django.core.exceptions import ValidationError


def recalculate_results(modeladmin, request, queryset) -> None:
    """
    Пересчитывает выбранные итоговые результаты.
    """

    updated_count = 0

    for result in queryset:
        recalculate_learner_result(
            test=result.test,
            learner=result.learner,
        )
        updated_count += 1

    modeladmin.message_user(
        request,
        f"Пересчитано результатов: {updated_count}.",
        level=messages.SUCCESS,
    )


def publish_results(modeladmin, request, queryset) -> None:
    """
    Делает выбранные результаты видимыми ученику и родителю.
    """

    published_count = 0
    failed_count = 0

    for result in queryset:
        try:
            publish_learner_result(result=result)
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
                f"{failed_count}. Проверьте наличие оценки."
            ),
            level=messages.WARNING,
        )


def hide_results(modeladmin, request, queryset) -> None:
    """
    Скрывает выбранные результаты от ученика и родителя.
    """

    hidden_count = 0

    for result in queryset:
        hide_learner_result(result=result)
        hidden_count += 1

    modeladmin.message_user(
        request,
        f"Скрыто результатов: {hidden_count}.",
        level=messages.SUCCESS,
    )


recalculate_results.short_description = "Пересчитать итоговые результаты"
publish_results.short_description = "Опубликовать результаты"
hide_results.short_description = "Скрыть результаты"
