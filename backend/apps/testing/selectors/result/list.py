from __future__ import annotations

from apps.testing.selectors.result.base import result_base_queryset


def result_list_queryset(
    *,
    test_id: int | None = None,
    learner_id: int | None = None,
    status: str | None = None,
    is_blocked: bool | None = None,
    is_visible_to_learner: bool | None = None,
    is_visible_to_guardian: bool | None = None,
):
    """
    Возвращает список итоговых результатов с базовыми фильтрами.
    """

    queryset = result_base_queryset()

    if test_id is not None:
        queryset = queryset.filter(test_id=test_id)

    if learner_id is not None:
        queryset = queryset.filter(learner_id=learner_id)

    if status:
        queryset = queryset.filter(status=status)

    if is_blocked is not None:
        queryset = queryset.filter(is_blocked=is_blocked)

    if is_visible_to_learner is not None:
        queryset = queryset.filter(
            is_visible_to_learner=is_visible_to_learner,
        )

    if is_visible_to_guardian is not None:
        queryset = queryset.filter(
            is_visible_to_guardian=is_visible_to_guardian,
        )

    return queryset


def learner_result_list_queryset(
    *,
    learner_id: int,
    is_visible_to_learner: bool | None = None,
):
    """
    Возвращает итоговые результаты обучающегося.
    """

    return result_list_queryset(
        learner_id=learner_id,
        is_visible_to_learner=is_visible_to_learner,
    )


def visible_result_list_queryset(*, learner_id: int | None = None):
    """
    Возвращает результаты, видимые обучающимся.
    """

    return result_list_queryset(
        learner_id=learner_id,
        is_visible_to_learner=True,
    )
