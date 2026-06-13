from __future__ import annotations

from apps.testing.selectors import get_review_queue_count, review_queue_queryset


def get_teacher_review_queue(
    *,
    teacher_id: int,
    test_id: int | None = None,
):
    """
    Возвращает очередь проверки преподавателя.
    """

    return review_queue_queryset(
        teacher_id=teacher_id,
        test_id=test_id,
    )


def get_teacher_review_queue_count(
    *,
    teacher_id: int,
    test_id: int | None = None,
) -> int:
    """
    Возвращает количество попыток в очереди проверки преподавателя.
    """

    return get_review_queue_count(
        teacher_id=teacher_id,
        test_id=test_id,
    )
