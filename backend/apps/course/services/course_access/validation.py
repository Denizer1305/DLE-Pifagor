from __future__ import annotations

from apps.course.models import CourseAccessRule, CourseEnrollment, CourseGroupAccess
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_course_group_access_can_be_saved(
    *,
    group_access: CourseGroupAccess,
) -> None:
    """
    Проверяет, что доступ группы к курсу можно сохранить.
    """

    errors: dict[str, str] = {}

    if group_access.group_subject_id:
        group_subject_group_id = getattr(
            group_access.group_subject,
            "group_id",
            None,
        )

        if (
            group_access.group_id
            and group_subject_group_id
            and group_subject_group_id != group_access.group_id
        ):
            errors["group_subject"] = _(
                "Предмет группы должен относиться к выбранной группе."
            )

    if group_access.teacher_group_subject_id:
        teacher_group_subject = group_access.teacher_group_subject

        subject_group_id = getattr(
            teacher_group_subject,
            "group_id",
            None,
        )
        group_subject_id = getattr(
            teacher_group_subject,
            "group_subject_id",
            None,
        )

        if (
            group_access.group_id
            and subject_group_id
            and subject_group_id != group_access.group_id
        ):
            errors["teacher_group_subject"] = _(
                "Назначение преподавателя должно относиться к выбранной группе."
            )

        if (
            group_access.group_subject_id
            and group_subject_id
            and group_subject_id != group_access.group_subject_id
        ):
            errors["teacher_group_subject"] = _(
                "Назначение преподавателя должно относиться к выбранному предмету группы."
            )

    if errors:
        raise ValidationError(errors)


def validate_course_access_rule_can_be_saved(
    *,
    access_rule: CourseAccessRule,
) -> None:
    """
    Проверяет, что правило доступа к курсу можно сохранить.
    """

    errors: dict[str, str] = {}

    if access_rule.access_type == CourseAccessRule.AccessTypeChoices.LEARNER:
        if not access_rule.learner_id:
            errors["learner"] = _("Для персонального доступа нужен обучающийся.")

    if access_rule.access_type == CourseAccessRule.AccessTypeChoices.ORGANIZATION:
        if not access_rule.organization_id:
            errors["organization"] = _(
                "Для доступа организации нужно указать организацию."
            )

    if access_rule.access_type in {
        CourseAccessRule.AccessTypeChoices.PUBLIC_LINK,
        CourseAccessRule.AccessTypeChoices.INVITE_CODE,
    }:
        if not access_rule.access_code:
            errors["access_code"] = _(
                "Для доступа по ссылке или коду нужен код доступа."
            )

    if errors:
        raise ValidationError(errors)


def validate_course_enrollment_can_be_saved(
    *,
    enrollment: CourseEnrollment,
) -> None:
    """
    Проверяет, что запись на курс можно сохранить.
    """

    errors: dict[str, str] = {}

    if enrollment.group_access_id:
        if enrollment.group_access.course_id != enrollment.course_id:
            errors["group_access"] = _(
                "Групповой доступ должен относиться к тому же курсу."
            )

    if enrollment.access_rule_id:
        if enrollment.access_rule.course_id != enrollment.course_id:
            errors["access_rule"] = _(
                "Правило доступа должно относиться к тому же курсу."
            )

    if enrollment.completed_at and enrollment.started_at:
        if enrollment.completed_at < enrollment.started_at:
            errors["completed_at"] = _(
                "Дата завершения не может быть раньше даты начала."
            )

    if errors:
        raise ValidationError(errors)
