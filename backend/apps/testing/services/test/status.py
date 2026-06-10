from __future__ import annotations

from apps.testing.constants import TestStatus
from apps.testing.models import Test
from apps.testing.services.test.validation import (
    validate_test_can_be_archived,
    validate_test_can_be_published,
    validate_test_can_be_restored,
)
from django.db import transaction
from django.utils import timezone


@transaction.atomic
def publish_test(*, test: Test) -> Test:
    """
    Публикует тест.
    """

    validate_test_can_be_published(test=test)

    now = timezone.now()

    test.status = TestStatus.PUBLISHED
    test.is_active = True
    test.published_at = now
    test.archived_at = None

    test.full_clean()
    test.save(
        update_fields=[
            "status",
            "is_active",
            "published_at",
            "archived_at",
            "updated_at",
        ]
    )

    return test


@transaction.atomic
def archive_test(*, test: Test) -> Test:
    """
    Архивирует тест.
    """

    validate_test_can_be_archived(test=test)

    test.status = TestStatus.ARCHIVED
    test.is_active = False
    test.archived_at = timezone.now()

    test.full_clean()
    test.save(
        update_fields=[
            "status",
            "is_active",
            "archived_at",
            "updated_at",
        ]
    )

    return test


@transaction.atomic
def restore_test(*, test: Test) -> Test:
    """
    Восстанавливает тест в черновик.
    """

    validate_test_can_be_restored(test=test)

    test.status = TestStatus.DRAFT
    test.is_active = True
    test.archived_at = None

    test.full_clean()
    test.save(
        update_fields=[
            "status",
            "is_active",
            "archived_at",
            "updated_at",
        ]
    )

    return test
