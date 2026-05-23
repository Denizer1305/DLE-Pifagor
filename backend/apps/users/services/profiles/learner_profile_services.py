from __future__ import annotations

from apps.users.constants.audit import UserAuditAction
from apps.users.constants.lifecycle import ProfileStatus
from apps.users.models import LearnerProfile
from apps.users.services.audit_services import create_user_audit_log
from django.db import transaction
from django.utils import timezone


def create_learner_profile(
    *,
    user,
    organization=None,
    department=None,
    group=None,
    curator=None,
    is_minor: bool = False,
    created_by_guardian=None,
    status: str = ProfileStatus.DRAFT,
) -> LearnerProfile:
    """
    Создаёт профиль учащегося.

    Args:
        user:
            Пользователь учащегося.
        organization:
            Образовательная организация.
        department:
            Отделение.
        group:
            Учебная группа.
        curator:
            Куратор группы.
        is_minor:
            Является ли учащийся ребёнком младше 14 лет.
        created_by_guardian:
            Родитель, который создал профиль ребёнка.
        status:
            Статус профиля.

    Returns:
        LearnerProfile: Созданный профиль учащегося.
    """

    profile = LearnerProfile.objects.create(
        user=user,
        organization=organization,
        department=department,
        group=group,
        curator=curator,
        is_minor=is_minor,
        created_by_guardian=created_by_guardian,
        status=status,
    )
    profile.full_clean()
    profile.save()

    return profile


@transaction.atomic
def verify_learner_profile(
    *, profile: LearnerProfile, verified_by, request=None
) -> LearnerProfile:
    """
    Подтверждает профиль учащегося.

    Args:
        profile:
            Профиль учащегося.
        verified_by:
            Пользователь, который подтвердил профиль.
        request:
            HTTP-запрос.

    Returns:
        LearnerProfile: Обновлённый профиль учащегося.
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
        message="Профиль учащегося подтверждён.",
        request=request,
    )

    return profile
