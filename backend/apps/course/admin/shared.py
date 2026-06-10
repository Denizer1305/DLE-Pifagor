from __future__ import annotations

from collections.abc import Callable
from typing import Any

from django.contrib import messages
from django.core.exceptions import ValidationError


def format_validation_error(error: ValidationError) -> str:
    """
    Форматирует ValidationError для вывода в Django admin.
    """

    if hasattr(error, "message_dict"):
        return "; ".join(
            f"{field}: {', '.join(messages_list)}"
            for field, messages_list in error.message_dict.items()
        )

    return "; ".join(error.messages)


def run_admin_service_action(
    *,
    request,
    queryset,
    service: Callable[..., Any],
    object_kwarg: str,
    success_message: str,
) -> None:
    """
    Выполняет сервисное действие для набора объектов.
    """

    updated_count = 0

    for obj in queryset:
        try:
            service(**{object_kwarg: obj})
            updated_count += 1
        except ValidationError as error:
            messages.error(
                request,
                f"{obj}: {format_validation_error(error)}",
            )

    if updated_count:
        messages.success(
            request,
            success_message.format(count=updated_count),
        )


def get_single_selected_object(
    *,
    request,
    queryset,
):
    """
    Возвращает один выбранный объект или пишет ошибку.
    """

    selected_count = queryset.count()

    if selected_count != 1:
        messages.error(
            request,
            "Выберите ровно одну запись для выполнения действия.",
        )
        return None

    return queryset.first()
