from __future__ import annotations

from datetime import timedelta

from django.utils import timezone


def now_plus_days(days: int):
    """
    Возвращает дату и время через указанное количество дней.
    """

    return timezone.now() + timedelta(days=days)