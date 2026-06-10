from __future__ import annotations

from apps.education.models import LearnerGroupEnrollment
from django.db.models import Q, QuerySet


def learner_group_enrollment_base_queryset() -> QuerySet:
    """
    Базовый queryset академических зачислений обучающихся.
    """

    return LearnerGroupEnrollment.objects.select_related(
        "learner",
        "group",
        "group__organization",
        "group__department",
        "academic_year",
    )


def learner_group_enrollment_list_queryset(
    *,
    search: str = "",
    learner_id: int | None = None,
    organization_id: int | None = None,
    department_id: int | None = None,
    group_id: int | None = None,
    academic_year_id: int | None = None,
    status: str = "",
    is_primary: bool | None = None,
) -> QuerySet:
    """
    Возвращает список академических зачислений с фильтрами.
    """

    queryset = learner_group_enrollment_base_queryset()

    if search:
        queryset = queryset.filter(
            Q(learner__email__icontains=search)
            | Q(learner__first_name__icontains=search)
            | Q(learner__last_name__icontains=search)
            | Q(group__name__icontains=search)
            | Q(group__code__icontains=search)
            | Q(academic_year__name__icontains=search)
        )

    if learner_id:
        queryset = queryset.filter(learner_id=learner_id)

    if organization_id:
        queryset = queryset.filter(group__organization_id=organization_id)

    if department_id:
        queryset = queryset.filter(group__department_id=department_id)

    if group_id:
        queryset = queryset.filter(group_id=group_id)

    if academic_year_id:
        queryset = queryset.filter(academic_year_id=academic_year_id)

    if status:
        queryset = queryset.filter(status=status)

    if is_primary is not None:
        queryset = queryset.filter(is_primary=is_primary)

    return queryset


def learner_group_enrollment_detail_queryset() -> QuerySet:
    """
    Queryset для детальной карточки академического зачисления.
    """

    return learner_group_enrollment_base_queryset()


def get_learner_group_enrollment_by_id(
    enrollment_id: int,
) -> LearnerGroupEnrollment:
    """
    Возвращает академическое зачисление по идентификатору.
    """

    return learner_group_enrollment_detail_queryset().get(id=enrollment_id)


def get_active_enrollments_for_learner(
    learner_id: int,
    *,
    academic_year_id: int | None = None,
) -> QuerySet:
    """
    Возвращает активные зачисления обучающегося.
    """

    queryset = learner_group_enrollment_base_queryset().filter(
        learner_id=learner_id,
        status=LearnerGroupEnrollment.StatusChoices.ACTIVE,
    )

    if academic_year_id:
        queryset = queryset.filter(academic_year_id=academic_year_id)

    return queryset


def get_primary_enrollment_for_learner(
    learner_id: int,
    *,
    academic_year_id: int,
) -> LearnerGroupEnrollment | None:
    """
    Возвращает основное зачисление обучающегося на учебный год.
    """

    return (
        learner_group_enrollment_base_queryset()
        .filter(
            learner_id=learner_id,
            academic_year_id=academic_year_id,
            is_primary=True,
        )
        .first()
    )
