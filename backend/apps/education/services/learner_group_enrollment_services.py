from __future__ import annotations

from typing import Any

from apps.education.constants import LEARNER_ROLE_CODES
from apps.education.models import LearnerGroupEnrollment
from apps.education.selectors import get_learner_group_enrollment_by_id
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils.translation import gettext_lazy as _

LEARNER_GROUP_ENROLLMENT_MUTABLE_FIELDS = {
    "learner",
    "learner_id",
    "group",
    "group_id",
    "academic_year",
    "academic_year_id",
    "enrollment_date",
    "completion_date",
    "status",
    "is_primary",
    "journal_number",
    "notes",
}


@transaction.atomic
def create_learner_group_enrollment(
    *,
    data: dict[str, Any],
) -> LearnerGroupEnrollment:
    """
    Создаёт академическое зачисление обучающегося.
    """

    enrollment = LearnerGroupEnrollment()

    _apply_learner_group_enrollment_data(
        enrollment=enrollment,
        data=data,
    )

    _validate_learner_can_be_enrolled(enrollment=enrollment)

    if enrollment.is_primary:
        _unset_other_primary_enrollments(
            learner_id=enrollment.learner_id,
            academic_year_id=enrollment.academic_year_id,
        )

    enrollment.full_clean()
    enrollment.save()

    return enrollment


@transaction.atomic
def update_learner_group_enrollment(
    *,
    enrollment: LearnerGroupEnrollment,
    data: dict[str, Any],
) -> LearnerGroupEnrollment:
    """
    Обновляет академическое зачисление обучающегося.
    """

    _apply_learner_group_enrollment_data(
        enrollment=enrollment,
        data=data,
    )

    _validate_learner_can_be_enrolled(enrollment=enrollment)

    if enrollment.is_primary:
        _unset_other_primary_enrollments(
            learner_id=enrollment.learner_id,
            academic_year_id=enrollment.academic_year_id,
            exclude_id=enrollment.id,
        )

    enrollment.full_clean()
    enrollment.save()

    return enrollment


@transaction.atomic
def update_learner_group_enrollment_by_id(
    *,
    enrollment_id: int,
    data: dict[str, Any],
) -> LearnerGroupEnrollment:
    """
    Обновляет академическое зачисление по идентификатору.
    """

    enrollment = get_learner_group_enrollment_by_id(enrollment_id)

    return update_learner_group_enrollment(
        enrollment=enrollment,
        data=data,
    )


@transaction.atomic
def set_primary_learner_group_enrollment(
    *,
    enrollment: LearnerGroupEnrollment,
) -> LearnerGroupEnrollment:
    """
    Делает зачисление основным для обучающегося в учебном году.
    """

    _unset_other_primary_enrollments(
        learner_id=enrollment.learner_id,
        academic_year_id=enrollment.academic_year_id,
        exclude_id=enrollment.id,
    )

    enrollment.is_primary = True
    enrollment.full_clean()
    enrollment.save(
        update_fields=[
            "is_primary",
            "updated_at",
        ],
    )

    return enrollment


@transaction.atomic
def set_primary_learner_group_enrollment_by_id(
    *,
    enrollment_id: int,
) -> LearnerGroupEnrollment:
    """
    Делает зачисление основным по идентификатору.
    """

    enrollment = get_learner_group_enrollment_by_id(enrollment_id)

    return set_primary_learner_group_enrollment(enrollment=enrollment)


@transaction.atomic
def complete_learner_group_enrollment(
    *,
    enrollment: LearnerGroupEnrollment,
    completion_date,
    status: str = LearnerGroupEnrollment.StatusChoices.GRADUATED,
) -> LearnerGroupEnrollment:
    """
    Завершает академическое зачисление.
    """

    enrollment.status = status
    enrollment.completion_date = completion_date
    enrollment.is_primary = False
    enrollment.full_clean()
    enrollment.save(
        update_fields=[
            "status",
            "completion_date",
            "is_primary",
            "updated_at",
        ],
    )

    return enrollment


@transaction.atomic
def complete_learner_group_enrollment_by_id(
    *,
    enrollment_id: int,
    completion_date,
    status: str = LearnerGroupEnrollment.StatusChoices.GRADUATED,
) -> LearnerGroupEnrollment:
    """
    Завершает академическое зачисление по идентификатору.
    """

    enrollment = get_learner_group_enrollment_by_id(enrollment_id)

    return complete_learner_group_enrollment(
        enrollment=enrollment,
        completion_date=completion_date,
        status=status,
    )


@transaction.atomic
def archive_learner_group_enrollment(
    *,
    enrollment: LearnerGroupEnrollment,
    completion_date,
) -> LearnerGroupEnrollment:
    """
    Архивирует академическое зачисление.
    """

    return complete_learner_group_enrollment(
        enrollment=enrollment,
        completion_date=completion_date,
        status=LearnerGroupEnrollment.StatusChoices.ARCHIVED,
    )


@transaction.atomic
def archive_learner_group_enrollment_by_id(
    *,
    enrollment_id: int,
    completion_date,
) -> LearnerGroupEnrollment:
    """
    Архивирует академическое зачисление по идентификатору.
    """

    enrollment = get_learner_group_enrollment_by_id(enrollment_id)

    return archive_learner_group_enrollment(
        enrollment=enrollment,
        completion_date=completion_date,
    )


def _apply_learner_group_enrollment_data(
    *,
    enrollment: LearnerGroupEnrollment,
    data: dict[str, Any],
) -> None:
    """
    Применяет входные данные к академическому зачислению.
    """

    for field_name in LEARNER_GROUP_ENROLLMENT_MUTABLE_FIELDS:
        if field_name in data:
            setattr(enrollment, field_name, data[field_name])


def _validate_learner_can_be_enrolled(
    *,
    enrollment: LearnerGroupEnrollment,
) -> None:
    """
    Проверяет, что пользователь может быть зачислен как обучающийся.

    Проверка сделана устойчивой к текущей реализации users:
    если у пользователя есть role/user_roles, проверяем роль learner;
    если роль-связи недоступны, не блокируем создание на уровне сервиса,
    чтобы не ломать модуль до подключения permissions.
    """

    if not enrollment.learner_id:
        return

    role_codes = set()

    direct_role = getattr(enrollment.learner, "role", None)
    direct_role_code = getattr(direct_role, "code", None)

    if direct_role_code:
        role_codes.add(str(direct_role_code))

    user_roles = getattr(enrollment.learner, "user_roles", None)

    if user_roles is not None:
        for user_role in user_roles.all():
            status = getattr(user_role, "status", "active")

            if status != "active":
                continue

            role = getattr(user_role, "role", None)
            role_code = getattr(role, "code", None)

            if role_code:
                role_codes.add(str(role_code))

    if role_codes and not role_codes.intersection(LEARNER_ROLE_CODES):
        raise ValidationError(
            {"learner": _("Пользователь должен иметь активную роль обучающегося.")}
        )


def _unset_other_primary_enrollments(
    *,
    learner_id: int,
    academic_year_id: int,
    exclude_id: int | None = None,
) -> None:
    """
    Снимает флаг основного зачисления с остальных зачислений обучающегося.
    """

    queryset = LearnerGroupEnrollment.objects.filter(
        learner_id=learner_id,
        academic_year_id=academic_year_id,
        is_primary=True,
    )

    if exclude_id:
        queryset = queryset.exclude(id=exclude_id)

    queryset.update(is_primary=False)
