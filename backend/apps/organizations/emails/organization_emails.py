from __future__ import annotations

from apps.users.emails.base_email import send_templated_email
from apps.users.emails.email_context import get_base_email_context


def send_teacher_registration_code_created_email(
    *,
    user,
    code: str,
    organization_name: str = "",
    expires_at: str = "",
) -> int:
    context = get_base_email_context(
        user=user,
        title="Создан код регистрации преподавателя",
        preview_text="В ЦОС «Пифагор» создан код регистрации преподавателя.",
        action_url="/admin/organizations",
        action_label="Открыть организации",
        extra_context={
            "code": code,
            "organization_name": organization_name,
            "expires_at": expires_at,
        },
    )

    return send_templated_email(
        subject="Создан код регистрации преподавателя",
        to_email=user.email,
        template_base="emails/organizations/codes/teacher_registration_code_created",
        context=context,
    )


def send_group_join_code_created_email(
    *,
    user,
    code: str,
    group_name: str = "",
    organization_name: str = "",
    expires_at: str = "",
) -> int:
    context = get_base_email_context(
        user=user,
        title="Создан код присоединения к группе",
        preview_text="В ЦОС «Пифагор» создан код присоединения к учебной группе.",
        action_url="/admin/study-groups",
        action_label="Открыть группы",
        extra_context={
            "code": code,
            "group_name": group_name,
            "organization_name": organization_name,
            "expires_at": expires_at,
        },
    )

    return send_templated_email(
        subject="Создан код присоединения к группе",
        to_email=user.email,
        template_base="emails/organizations/codes/group_join_code_created",
        context=context,
    )


def send_organization_code_expiring_email(
    *,
    user,
    code: str,
    code_type: str = "",
    expires_at: str = "",
) -> int:
    context = get_base_email_context(
        user=user,
        title="Срок действия кода скоро истечёт",
        preview_text="Один из кодов ЦОС «Пифагор» скоро перестанет действовать.",
        action_url="/admin/organizations",
        action_label="Проверить коды",
        extra_context={
            "code": code,
            "code_type": code_type,
            "expires_at": expires_at,
        },
    )

    return send_templated_email(
        subject="Срок действия кода скоро истечёт",
        to_email=user.email,
        template_base="emails/organizations/codes/code_expiring",
        context=context,
    )


def send_teacher_subject_assigned_email(
    *,
    user,
    subject_name: str,
    organization_name: str = "",
) -> int:
    context = get_base_email_context(
        user=user,
        title="Назначен предмет",
        preview_text="В ЦОС «Пифагор» вам назначили предмет.",
        action_url="/teacher",
        action_label="Открыть кабинет преподавателя",
        extra_context={
            "subject_name": subject_name,
            "organization_name": organization_name,
        },
    )

    return send_templated_email(
        subject="Вам назначен предмет",
        to_email=user.email,
        template_base="emails/organizations/teacher_subjects/assigned",
        context=context,
    )


def send_teacher_subject_removed_email(
    *,
    user,
    subject_name: str,
    organization_name: str = "",
) -> int:
    context = get_base_email_context(
        user=user,
        title="Предмет снят с назначения",
        preview_text="В ЦОС «Пифагор» изменилось назначение предмета.",
        action_url="/teacher",
        action_label="Открыть кабинет преподавателя",
        extra_context={
            "subject_name": subject_name,
            "organization_name": organization_name,
        },
    )

    return send_templated_email(
        subject="Предмет снят с назначения",
        to_email=user.email,
        template_base="emails/organizations/teacher_subjects/removed",
        context=context,
    )


def send_group_curator_assigned_email(
    *,
    user,
    group_name: str,
    organization_name: str = "",
) -> int:
    context = get_base_email_context(
        user=user,
        title="Вы назначены куратором группы",
        preview_text="В ЦОС «Пифагор» вам назначили кураторство учебной группы.",
        action_url="/teacher",
        action_label="Открыть кабинет",
        extra_context={
            "group_name": group_name,
            "organization_name": organization_name,
        },
    )

    return send_templated_email(
        subject="Вы назначены куратором группы",
        to_email=user.email,
        template_base="emails/organizations/group_curators/assigned",
        context=context,
    )


def send_learner_group_changed_email(
    *,
    user,
    group_name: str,
    organization_name: str = "",
) -> int:
    context = get_base_email_context(
        user=user,
        title="Учебная группа изменена",
        preview_text="В ЦОС «Пифагор» изменилась учебная группа.",
        action_url="/profile",
        action_label="Открыть профиль",
        extra_context={
            "group_name": group_name,
            "organization_name": organization_name,
        },
    )

    return send_templated_email(
        subject="Учебная группа изменена",
        to_email=user.email,
        template_base="emails/organizations/study_groups/learner_group_changed",
        context=context,
    )
