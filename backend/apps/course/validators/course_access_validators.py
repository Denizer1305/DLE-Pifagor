from __future__ import annotations

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_access_date_range(
    *,
    starts_at,
    ends_at,
) -> None:
    """
    Проверяет даты действия доступа к курсу.
    """

    if starts_at and ends_at and ends_at < starts_at:
        raise ValidationError(
            {"ends_at": _("Дата окончания доступа не может быть раньше даты начала.")}
        )


def validate_course_group_access_relations(
    *,
    course,
    group,
    group_subject,
    teacher_group_subject,
) -> None:
    """
    Проверяет согласованность связи курса с учебной группой.
    """

    errors: dict[str, str] = {}

    if group_subject:
        if group and group_subject.group_id != group.id:
            errors["group_subject"] = _(
                "Предмет группы должен относиться к выбранной группе."
            )

        if course.subject_id and group_subject.subject_id != course.subject_id:
            errors["group_subject"] = _(
                "Предмет группы должен совпадать с предметом курса."
            )

        if (
            course.academic_year_id
            and group_subject.academic_year_id != course.academic_year_id
        ):
            errors["group_subject"] = _(
                "Учебный год предмета группы должен совпадать с учебным годом курса."
            )

    if teacher_group_subject:
        if group_subject and teacher_group_subject.group_subject_id != group_subject.id:
            errors["teacher_group_subject"] = _(
                "Назначение преподавателя должно относиться к выбранному предмету группы."
            )

        if teacher_group_subject.teacher_id != course.owner_teacher_id:
            errors["teacher_group_subject"] = _(
                "Назначение должно принадлежать владельцу курса."
            )

    if errors:
        raise ValidationError(errors)


def validate_course_access_rule_payload(
    *,
    access_type: str,
    learner,
    organization,
    access_code: str,
) -> None:
    """
    Проверяет наполнение правила доступа к курсу.
    """

    errors: dict[str, str] = {}

    if access_type == "learner" and learner is None:
        errors["learner"] = _("Для персонального доступа нужен обучающийся.")

    if access_type == "organization" and organization is None:
        errors["organization"] = _("Для доступа организации нужна организация.")

    if access_type in {"public_link", "invite_code"} and not access_code:
        errors["access_code"] = _("Для доступа по ссылке или коду нужен код доступа.")

    if access_type not in {"learner", "organization"} and learner is not None:
        errors["learner"] = _(
            "Обучающийся указывается только для персонального доступа."
        )

    if access_type != "organization" and organization is not None:
        errors["organization"] = _(
            "Организация указывается только для доступа организации."
        )

    if errors:
        raise ValidationError(errors)
