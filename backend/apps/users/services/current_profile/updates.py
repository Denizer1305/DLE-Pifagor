from __future__ import annotations

from apps.users.constants.audit import UserAuditAction
from apps.users.constants.roles import RoleCode
from apps.users.selectors.current_profile_selectors import (
    get_active_role_code_for_user,
    get_current_role_profile,
    get_or_create_profile_for_user,
)
from apps.users.services.audit_services import create_user_audit_log
from apps.users.services.current_profile.payloads import build_current_profile_payload
from apps.users.services.current_profile.role_profiles import TEACHER_ROLE_CODES
from django.db import transaction


@transaction.atomic
def update_current_profile(*, user, data: dict, request=None) -> dict:
    """
    Обновляет текущий профиль пользователя.
    """

    profile = get_or_create_profile_for_user(user)

    update_user_fields(user=user, data=data)
    update_base_profile_fields(profile=profile, data=data)

    role_code = get_active_role_code_for_user(user)
    role_profile = get_current_role_profile(user, role_code)

    update_role_profile_fields(
        role_code=role_code,
        role_profile=role_profile,
        data=data.get("role_profile") or {},
    )

    create_user_audit_log(
        actor=user,
        target_user=user,
        action=UserAuditAction.PROFILE_UPDATED,
        message="Пользователь обновил данные профиля.",
        request=request,
    )

    return build_current_profile_payload(user=user)


def update_user_fields(*, user, data: dict) -> None:
    """
    Обновляет поля модели User.
    """

    fields = []

    for field in [
        "first_name",
        "last_name",
        "middle_name",
        "birth_date",
        "phone",
        "backup_email",
    ]:
        if field in data:
            setattr(user, field, data[field])
            fields.append(field)

    if fields:
        user.full_clean()
        user.save(update_fields=[*fields, "updated_at"])


def update_base_profile_fields(*, profile, data: dict) -> None:
    """
    Обновляет поля базового профиля.
    """

    mapping = {
        "gender": "gender",
        "city": "city",
        "about": "about",
        "vk_url": "social_link_vk",
        "max_url": "social_link_max",
        "preferred_contact_method": "preferred_contact_method",
        "show_email": "show_email",
        "show_phone": "show_phone",
        "email_notifications": "email_notifications",
        "push_notifications": "push_notifications",
    }

    fields = []

    for input_field, model_field in mapping.items():
        if input_field in data:
            setattr(profile, model_field, data[input_field])
            fields.append(model_field)

    if fields:
        profile.full_clean()
        profile.save(update_fields=[*fields, "updated_at"])


def update_role_profile_fields(*, role_code: str, role_profile, data: dict) -> None:
    """
    Обновляет ролевой профиль.

    Организацию, группу, отделение и статус пользователь сам менять не должен.
    """

    if not role_profile or not data:
        return

    if role_code in TEACHER_ROLE_CODES:
        update_teacher_role_profile(profile=role_profile, data=data)
        return

    if role_code == RoleCode.GUARDIAN:
        update_guardian_role_profile(profile=role_profile, data=data)


def update_teacher_role_profile(*, profile, data: dict) -> None:
    """
    Обновляет безопасные поля профиля преподавателя.
    """

    fields = []

    for field in [
        "position",
        "public_title",
        "short_bio",
        "bio",
        "education",
        "experience_years",
        "achievements",
        "is_public",
        "show_on_teachers_page",
    ]:
        if field in data:
            setattr(profile, field, data[field])
            fields.append(field)

    if fields:
        profile.full_clean()
        profile.save(update_fields=[*fields, "updated_at"])


def update_guardian_role_profile(*, profile, data: dict) -> None:
    """
    Обновляет безопасные поля профиля родителя.
    """

    fields = []

    for field in [
        "occupation",
        "work_place",
        "emergency_contact_phone",
        "notes",
    ]:
        if field in data:
            setattr(profile, field, data[field])
            fields.append(field)

    if fields:
        profile.full_clean()
        profile.save(update_fields=[*fields, "updated_at"])
