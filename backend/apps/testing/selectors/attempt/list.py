from __future__ import annotations

from apps.testing.selectors.attempt.base import attempt_base_queryset


def attempt_list_queryset(
    *,
    test_id: int | None = None,
    learner_id: int | None = None,
    status: str | None = None,
    check_status: str | None = None,
    reviewer_teacher_id: int | None = None,
    is_confirmed_by_teacher: bool | None = None,
    is_visible_to_learner: bool | None = None,
):
    """
    Возвращает список попыток теста с базовыми фильтрами.
    """

    queryset = attempt_base_queryset()

    if test_id is not None:
        queryset = queryset.filter(test_id=test_id)

    if learner_id is not None:
        queryset = queryset.filter(learner_id=learner_id)

    if status:
        queryset = queryset.filter(status=status)

    if check_status:
        queryset = queryset.filter(check_status=check_status)

    if reviewer_teacher_id is not None:
        queryset = queryset.filter(reviewer_teacher_id=reviewer_teacher_id)

    if is_confirmed_by_teacher is not None:
        queryset = queryset.filter(
            is_confirmed_by_teacher=is_confirmed_by_teacher,
        )

    if is_visible_to_learner is not None:
        queryset = queryset.filter(
            is_visible_to_learner=is_visible_to_learner,
        )

    return queryset


def learner_attempt_list_queryset(
    *,
    learner_id: int,
    is_visible_to_learner: bool | None = None,
):
    """
    Возвращает попытки конкретного обучающегося.
    """

    return attempt_list_queryset(
        learner_id=learner_id,
        is_visible_to_learner=is_visible_to_learner,
    )
