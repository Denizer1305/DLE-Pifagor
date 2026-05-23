from __future__ import annotations

from datetime import date, timedelta

from django.utils import timezone

MONTH_NAMES = [
    "",
    "Январь",
    "Февраль",
    "Март",
    "Апрель",
    "Май",
    "Июнь",
    "Июль",
    "Август",
    "Сентябрь",
    "Октябрь",
    "Ноябрь",
    "Декабрь",
]

ADMIN_CALENDAR_NOTES = {
    1: (
        "Проверка новых регистраций",
        "Проверить корректность новых регистраций преподавателей и учащихся.",
    ),
    3: (
        "Проверка обращений",
        "Разобрать новые сообщения от пользователей и распределить обращения.",
    ),
    7: (
        "Мониторинг системы",
        "Проверить стабильность платформы и основные системные показатели.",
    ),
    14: (
        "Контроль платформы и обращения",
        "Проверить обращения пользователей, статус системы и новые регистрации.",
    ),
    21: (
        "Обновление пользователей",
        "Сверить списки преподавателей, студентов и родителей.",
    ),
    30: (
        "Закрытие месяца",
        "Подготовить итоговую административную сводку.",
    ),
}

DEFAULT_ADMIN_CALENDAR_NOTE = (
    "Административный день",
    "Плановая проверка данных, доступов и активности платформы.",
)


def get_month_label(target_date: date) -> str:
    """
    Возвращает название месяца для календаря dashboard.
    """

    return f"{MONTH_NAMES[target_date.month]} {target_date.year}"


def get_calendar_start_date(first_day: date) -> date:
    """
    Возвращает дату первой ячейки календарной сетки.

    Календарь начинается с понедельника.
    """

    weekday_offset = first_day.weekday()

    return first_day - timedelta(days=weekday_offset)


def get_admin_calendar_note(day: int) -> tuple[str, str]:
    """
    Возвращает подсказку для дня календаря администратора.
    """

    return ADMIN_CALENDAR_NOTES.get(day, DEFAULT_ADMIN_CALENDAR_NOTE)


def build_admin_calendar_day_payload(
    *,
    current_date: date,
    first_day: date,
    selected_date: date,
    today: date,
) -> dict:
    """
    Формирует одну ячейку календаря администратора.
    """

    day_title, day_text = get_admin_calendar_note(current_date.day)

    return {
        "date": current_date.isoformat(),
        "day": current_date.day,
        "is_today": current_date == today,
        "is_selected": current_date == selected_date,
        "is_muted": current_date.month != first_day.month,
        "is_weekend": current_date.weekday() >= 5,
        "title": day_title,
        "text": day_text,
    }


def build_admin_calendar_payload(target_date: date | None = None) -> dict:
    """
    Формирует календарь для dashboard.

    Сейчас это общий календарный виджет с системными подсказками.
    Позже сюда можно подключить отдельное приложение календаря/расписания.
    """

    today = timezone.localdate()
    selected_date = target_date or today
    first_day = selected_date.replace(day=1)
    calendar_start = get_calendar_start_date(first_day)

    # Оставляем стабильные 42 ячейки, чтобы frontend-сетка не прыгала.
    total_days = 42

    days = [
        build_admin_calendar_day_payload(
            current_date=calendar_start + timedelta(days=index),
            first_day=first_day,
            selected_date=selected_date,
            today=today,
        )
        for index in range(total_days)
    ]

    return {
        "month_label": get_month_label(first_day),
        "selected_date": selected_date.isoformat(),
        "days": days,
    }
