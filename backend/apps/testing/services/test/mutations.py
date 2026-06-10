from __future__ import annotations

from typing import Any

from apps.testing.models import Test
from apps.testing.services.test.payloads import apply_test_payload
from django.db import transaction


@transaction.atomic
def create_test(*, data: dict[str, Any]) -> Test:
    """
    Создаёт тест.
    """

    test = Test()

    apply_test_payload(
        test=test,
        data=data,
    )

    test.full_clean()
    test.save()

    return test


@transaction.atomic
def update_test(
    *,
    test: Test,
    data: dict[str, Any],
) -> Test:
    """
    Обновляет тест.
    """

    apply_test_payload(
        test=test,
        data=data,
    )

    test.full_clean()
    test.save()

    return test
