from __future__ import annotations

from apps.users.constants.audit import UserAuditAction
from apps.users.constants.lifecycle import ProfileStatus
from apps.users.models import TeacherProfile
from apps.users.services.audit_services import create_user_audit_log
from django.db import transaction
from django.utils import timezone


def create_teacher_profile(
    *,
    user,
    organization=None,
    department=None,
    position: str = "",
    status: str = ProfileStatus.DRAFT,
) -> TeacherProfile:
    """
    Создаёт профиль преподавателя.

    Args:
        user:
            Пользователь преподавателя.
        organization:
            Образовательная организация.
        department:
            Отделение.
        position:
            Должность.
        status:
            Статус профиля.

    Returns:
        TeacherProfile: Созданный профиль преподавателя.
    """

    profile = TeacherProfile.objects.create(
        user=user,
        organization=organization,
        department=department,
        position=position,
        status=status,
    )
    profile.full_clean()
    profile.save()

    return profile


@transaction.atomic
def verify_teacher_profile(
    *, profile: TeacherProfile, verified_by, request=None
) -> TeacherProfile:
    """
    Подтверждает профиль преподавателя.

    Args:
        profile:
            Профиль преподавателя.
        verified_by:
            Пользователь, который подтвердил профиль.
        request:
            HTTP-запрос.

    Returns:
        TeacherProfile: Обновлённый профиль преподавателя.
    """

    profile.status = ProfileStatus.VERIFIED
    profile.verified_by = verified_by
    profile.verified_at = timezone.now()
    profile.save(
        update_fields=[
            "status",
            "verified_by",
            "verified_at",
            "updated_at",
        ]
    )

    create_user_audit_log(
        actor=verified_by,
        target_user=profile.user,
        action=UserAuditAction.PROFILE_VERIFIED,
        message="Профиль преподавателя подтверждён.",
        request=request,
    )

    return profile
