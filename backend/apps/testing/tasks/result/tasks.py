from __future__ import annotations

from apps.testing.selectors import get_attempt_for_update, get_test_by_id
from apps.testing.services import publish_attempt_result, recalculate_learner_result
from django.contrib.auth import get_user_model
from django.db import transaction
from django.shortcuts import get_object_or_404

User = get_user_model()


@transaction.atomic
def publish_attempt_result_task(*, attempt_id: int):
    """
    Публикует подтверждённый результат попытки.

    После публикации результат становится доступен ученику и родителю,
    а агрегированный результат ученика по тесту пересчитывается сервисом.
    """

    attempt = get_attempt_for_update(attempt_id)

    return publish_attempt_result(attempt=attempt)


@transaction.atomic
def recalculate_learner_result_task(
    *,
    test_id: int,
    learner_id: int,
):
    """
    Пересчитывает итоговый результат обучающегося по тесту.
    """

    test = get_test_by_id(test_id)
    learner = get_object_or_404(
        User.objects.all(),
        id=learner_id,
    )

    return recalculate_learner_result(
        test=test,
        learner=learner,
    )
