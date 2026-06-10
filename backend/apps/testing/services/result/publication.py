from __future__ import annotations

from apps.testing.constants import TestAttemptStatus
from apps.testing.models import TestAttempt
from apps.testing.services.result.aggregation import recalculate_learner_result
from apps.testing.services.result.notifications import (
    notify_guardian_about_test_result,
    notify_learner_about_test_result,
)
from apps.testing.validators import validate_attempt_can_be_published
from django.db import transaction
from django.utils import timezone


@transaction.atomic
def publish_attempt_result(
    *,
    attempt: TestAttempt,
) -> TestAttempt:
    """
    Публикует подтверждённый результат попытки ученику и родителю.
    """

    validate_attempt_can_be_published(attempt=attempt)

    attempt.status = TestAttemptStatus.PUBLISHED
    attempt.is_visible_to_learner = True
    attempt.is_visible_to_guardian = True
    attempt.published_at = timezone.now()

    attempt.full_clean()
    attempt.save(
        update_fields=[
            "status",
            "is_visible_to_learner",
            "is_visible_to_guardian",
            "published_at",
            "updated_at",
        ]
    )

    result = recalculate_learner_result(
        test=attempt.test,
        learner=attempt.learner,
    )
    publish_learner_result(result=result)

    notify_learner_about_test_result(attempt=attempt)
    notify_guardian_about_test_result(attempt=attempt)

    return attempt


@transaction.atomic
def publish_learner_result(*, result) -> None:
    """
    Делает агрегированный результат видимым ученику и родителю.
    """

    result.is_visible_to_learner = True
    result.is_visible_to_guardian = True

    result.full_clean()
    result.save(
        update_fields=[
            "is_visible_to_learner",
            "is_visible_to_guardian",
            "updated_at",
        ]
    )


@transaction.atomic
def hide_learner_result(*, result) -> None:
    """
    Скрывает агрегированный результат от ученика и родителя.
    """

    result.is_visible_to_learner = False
    result.is_visible_to_guardian = False

    result.full_clean()
    result.save(
        update_fields=[
            "is_visible_to_learner",
            "is_visible_to_guardian",
            "updated_at",
        ]
    )
