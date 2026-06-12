from __future__ import annotations

from apps.testing.selectors.bank.base import (
    bank_item_base_queryset,
    bank_option_base_queryset,
)
from django.db.models import Q


def bank_item_list_queryset(
    *,
    search: str | None = None,
    organization_id: int | None = None,
    subject_id: int | None = None,
    owner_teacher_id: int | None = None,
    question_type: str | None = None,
    check_mode: str | None = None,
    difficulty: str | None = None,
    visibility: str | None = None,
    status: str | None = None,
    is_active: bool | None = None,
):
    """
    Возвращает список шаблонов вопросов с базовыми фильтрами.
    """

    queryset = bank_item_base_queryset()

    if search:
        queryset = queryset.filter(
            Q(title__icontains=search)
            | Q(text__icontains=search)
            | Q(explanation__icontains=search)
        )

    if organization_id is not None:
        queryset = queryset.filter(organization_id=organization_id)

    if subject_id is not None:
        queryset = queryset.filter(subject_id=subject_id)

    if owner_teacher_id is not None:
        queryset = queryset.filter(owner_teacher_id=owner_teacher_id)

    if question_type is not None:
        queryset = queryset.filter(question_type=question_type)

    if check_mode is not None:
        queryset = queryset.filter(check_mode=check_mode)

    if difficulty is not None:
        queryset = queryset.filter(difficulty=difficulty)

    if visibility is not None:
        queryset = queryset.filter(visibility=visibility)

    if status is not None:
        queryset = queryset.filter(status=status)

    if is_active is not None:
        queryset = queryset.filter(is_active=is_active)

    return queryset.order_by("-updated_at", "-id")


def reusable_bank_item_list_queryset(
    *,
    teacher_id: int,
    organization_id: int | None = None,
):
    """
    Возвращает шаблоны вопросов, доступные преподавателю для переиспользования.
    """

    return (
        bank_item_base_queryset()
        .reusable_for_teacher(
            teacher_id=teacher_id,
            organization_id=organization_id,
        )
        .order_by("-updated_at", "-id")
    )


def bank_option_list_queryset(
    *,
    bank_item_id: int | None = None,
    is_correct: bool | None = None,
    is_active: bool | None = None,
):
    """
    Возвращает список вариантов шаблонов вопросов.
    """

    queryset = bank_option_base_queryset()

    if bank_item_id is not None:
        queryset = queryset.filter(bank_item_id=bank_item_id)

    if is_correct is not None:
        queryset = queryset.filter(is_correct=is_correct)

    if is_active is not None:
        queryset = queryset.filter(is_active=is_active)

    return queryset.order_by("bank_item_id", "order", "id")
