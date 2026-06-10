from __future__ import annotations

from collections.abc import Callable

from apps.testing.services import archive_test, publish_test, restore_test
from django.contrib import messages


def messages_action(success_message: str) -> Callable:
    """
    Оборачивает admin action и показывает сообщение об успехе.
    """

    def decorator(action_func: Callable) -> Callable:
        def wrapper(modeladmin, request, queryset) -> None:
            action_func(modeladmin, request, queryset)
            modeladmin.message_user(
                request,
                success_message,
                level=messages.SUCCESS,
            )

        wrapper.__name__ = action_func.__name__
        wrapper.__doc__ = action_func.__doc__
        wrapper.short_description = success_message

        return wrapper

    return decorator


@messages_action("Тесты опубликованы.")
def publish_tests(modeladmin, request, queryset) -> None:
    """
    Публикует выбранные тесты.
    """

    for test in queryset:
        publish_test(test=test)


@messages_action("Тесты архивированы.")
def archive_tests(modeladmin, request, queryset) -> None:
    """
    Архивирует выбранные тесты.
    """

    for test in queryset:
        archive_test(test=test)


@messages_action("Тесты восстановлены в черновик.")
def restore_tests(modeladmin, request, queryset) -> None:
    """
    Восстанавливает выбранные тесты.
    """

    for test in queryset:
        restore_test(test=test)
