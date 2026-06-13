from __future__ import annotations

from apps.testing.services.bank.status import (
    archive_bank_item,
    publish_bank_item,
    restore_bank_item,
)
from django.contrib import messages
from django.core.exceptions import ValidationError


def publish_bank_items(modeladmin, request, queryset) -> None:
    """
    Публикует выбранные шаблоны вопросов.
    """

    success_count, failed_count = _process_bank_items(
        queryset=queryset,
        action=publish_bank_item,
    )

    _show_result_message(
        modeladmin=modeladmin,
        request=request,
        success_count=success_count,
        failed_count=failed_count,
        success_message="Опубликовано шаблонов",
        failed_message="Не удалось опубликовать шаблонов",
    )


def archive_bank_items(modeladmin, request, queryset) -> None:
    """
    Архивирует выбранные шаблоны вопросов.
    """

    success_count, failed_count = _process_bank_items(
        queryset=queryset,
        action=archive_bank_item,
    )

    _show_result_message(
        modeladmin=modeladmin,
        request=request,
        success_count=success_count,
        failed_count=failed_count,
        success_message="Архивировано шаблонов",
        failed_message="Не удалось архивировать шаблонов",
    )


def restore_bank_items(modeladmin, request, queryset) -> None:
    """
    Восстанавливает выбранные шаблоны вопросов.
    """

    success_count, failed_count = _process_bank_items(
        queryset=queryset,
        action=restore_bank_item,
    )

    _show_result_message(
        modeladmin=modeladmin,
        request=request,
        success_count=success_count,
        failed_count=failed_count,
        success_message="Восстановлено шаблонов",
        failed_message="Не удалось восстановить шаблонов",
    )


def _process_bank_items(*, queryset, action) -> tuple[int, int]:
    """
    Выполняет действие над набором шаблонов.
    """

    success_count = 0
    failed_count = 0

    for bank_item in queryset:
        try:
            action(bank_item=bank_item)
            success_count += 1
        except ValidationError:
            failed_count += 1

    return success_count, failed_count


def _show_result_message(
    *,
    modeladmin,
    request,
    success_count: int,
    failed_count: int,
    success_message: str,
    failed_message: str,
) -> None:
    """
    Показывает результат выполнения admin action.
    """

    if success_count:
        modeladmin.message_user(
            request,
            f"{success_message}: {success_count}.",
            level=messages.SUCCESS,
        )

    if failed_count:
        modeladmin.message_user(
            request,
            f"{failed_message}: {failed_count}.",
            level=messages.WARNING,
        )


publish_bank_items.short_description = "Опубликовать шаблоны вопросов"
archive_bank_items.short_description = "Архивировать шаблоны вопросов"
restore_bank_items.short_description = "Восстановить шаблоны вопросов"
