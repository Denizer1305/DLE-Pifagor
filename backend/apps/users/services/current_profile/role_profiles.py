from __future__ import annotations

from apps.users.constants.roles import RoleCode

TEACHER_ROLE_CODES = {
    RoleCode.TEACHER,
    RoleCode.CURATOR,
    RoleCode.METHODIST,
    RoleCode.ORGANIZER,
    RoleCode.MENTOR,
}


def build_role_profile_payload(*, role_code: str, role_profile) -> dict:
    """
    Собирает ролевой профиль для активной роли.
    """

    if not role_profile:
        return {}

    if role_code in TEACHER_ROLE_CODES:
        return build_teacher_role_payload(role_profile)

    if role_code == RoleCode.LEARNER:
        return build_learner_role_payload(role_profile)

    if role_code == RoleCode.GUARDIAN:
        return build_guardian_role_payload(role_profile)

    return {}


def build_teacher_role_payload(profile) -> dict:
    """
    Собирает данные преподавательского профиля.
    """

    return {
        "status": profile.status,
        "organization": profile.organization.short_name if profile.organization else "",
        "department": profile.department.name if profile.department else "",
        "position": profile.position or "",
        "public_title": profile.public_title or "",
        "short_bio": profile.short_bio or "",
        "bio": profile.bio or "",
        "education": profile.education or "",
        "experience_years": profile.experience_years,
        "achievements": profile.achievements or "",
        "is_public": profile.is_public,
        "show_on_teachers_page": profile.show_on_teachers_page,
        "hired_at": profile.hired_at,
        "dismissed_at": profile.dismissed_at,
    }


def build_learner_role_payload(profile) -> dict:
    """
    Собирает данные профиля учащегося.
    """

    return {
        "status": profile.status,
        "organization": profile.organization.short_name if profile.organization else "",
        "department": profile.department.name if profile.department else "",
        "group": profile.group.name if profile.group else "",
        "curator": profile.curator.get_full_name() if profile.curator else "",
        "learner_code": profile.learner_code or "",
        "admission_year": profile.admission_year,
        "admission_date": profile.admission_date,
        "graduation_date": profile.graduation_date,
        "is_minor": profile.is_minor,
    }


def build_guardian_role_payload(profile) -> dict:
    """
    Собирает данные профиля родителя.
    """

    return {
        "status": profile.status,
        "occupation": profile.occupation or "",
        "work_place": profile.work_place or "",
        "emergency_contact_phone": profile.emergency_contact_phone or "",
        "notes": profile.notes or "",
    }
