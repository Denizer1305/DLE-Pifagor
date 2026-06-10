"""
Selectors источников уведомлений.

Здесь будут функции, которые получают данные из других приложений:
задания, расписание, календарь, заметки, тесты, обращения и события.
"""

from __future__ import annotations

from apps.dashboard.selectors.dashboard_item_selectors import (
    get_calendar_items_for_date,
    get_note_items_in_period,
)


def get_today_schedule_items_for_user(*, user, target_date):
    """
    Возвращает занятия пользователя на указанную дату.

    Реальная интеграция с schedule будет добавлена после согласования
    моделей расписания.
    """

    return []


def get_assignment_deadlines_for_user(*, user, target_date):
    """
    Возвращает дедлайны заданий пользователя на указанную дату.

    Реальная интеграция с assignments будет добавлена после анализа моделей.
    """

    return []


def get_calendar_events_for_user(*, user, target_date):
    """
    Возвращает события пользовательского календаря на указанную дату.

    Возвращает сохранённые пользователем события личного календаря.
    """

    return get_calendar_items_for_date(user=user, target_date=target_date)


def get_note_reminders_for_user(*, user, starts_at, ends_at):
    """
    Возвращает напоминания заметок пользователя за период.

    Возвращает пользовательские заметки в указанном периоде.
    """

    return get_note_items_in_period(
        user=user,
        starts_at=starts_at,
        ends_at=ends_at,
    )


def get_work_to_check_for_teacher(*, user, target_date):
    """
    Возвращает работы, ожидающие проверки преподавателем.

    Реальная интеграция с assignments/journal будет добавлена позже.
    """

    return []


def get_moderation_requests_for_admin(*, user, target_date):
    """
    Возвращает заявки на модерацию для администратора.

    Реальная интеграция будет добавлена после согласования источников модерации.
    """

    return []


def get_support_requests_for_admin(*, user, target_date):
    """
    Возвращает обращения поддержки для администратора.

    Реальная интеграция с feedback/support будет добавлена позже.
    """

    return []
