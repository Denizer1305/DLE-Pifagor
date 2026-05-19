from __future__ import annotations

import re

from rest_framework.throttling import ScopedRateThrottle


class ContactFeedbackThrottle(ScopedRateThrottle):
    """
    Throttle для публичной формы обратной связи.

    Поддерживает стандартный DRF-формат:
        3/min
        100/hour

    И расширенный формат:
        3/10min
        3/10m
        5/30s
    """

    scope = "contact_feedback"

    def parse_rate(self, rate):
        """
        Преобразует rate-строку в количество запросов и длительность окна.

        Args:
            rate:
                Строка ограничения, например 3/10min.

        Returns:
            tuple[int | None, int | None]: Количество запросов и окно в секундах.
        """

        if rate is None:
            return None, None

        num, period = rate.split("/")
        num_requests = int(num)

        period = period.strip().lower()

        custom_period_match = re.fullmatch(
            r"(?P<amount>\d+)\s*(?P<unit>s|sec|second|seconds|m|min|minute|minutes|h|hour|hours|d|day|days)",
            period,
        )

        if custom_period_match:
            amount = int(custom_period_match.group("amount"))
            unit = custom_period_match.group("unit")

            unit_seconds = {
                "s": 1,
                "sec": 1,
                "second": 1,
                "seconds": 1,
                "m": 60,
                "min": 60,
                "minute": 60,
                "minutes": 60,
                "h": 3600,
                "hour": 3600,
                "hours": 3600,
                "d": 86400,
                "day": 86400,
                "days": 86400,
            }[unit]

            return num_requests, amount * unit_seconds

        duration = {
            "s": 1,
            "m": 60,
            "h": 3600,
            "d": 86400,
        }[period[0]]

        return num_requests, duration
