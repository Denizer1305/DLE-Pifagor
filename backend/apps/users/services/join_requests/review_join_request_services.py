from __future__ import annotations

from apps.core.exceptions import ConflictApplicationError, ValidationApplicationError
from apps.users.constants.lifecycle import ProfileStatus, UserRoleStatus
from apps.users.constants.onboarding import JoinRequestStatus, JoinRequestType
from apps.users.constants.roles import RoleCode
from apps.users.models import UserJoinRequest, UserRole
from apps.users.selectors.guardian_selectors import get_guardian_link
from apps.users.selectors.learner_selectors import get_learner_profile_by_user
from apps.users.selectors.teacher_selectors import get_teacher_profile_by_user
from apps.users.services.audit_services import (
    log_join_request_approved,
    log_join_request_rejected,
)
from apps.users.services.user_lifecycle_services import (
    activate_user,
    schedule_user_deletion_after_rejection,
)
from django.db import transaction


@transaction.atomic
def approve_join_request(
    *, join_request: UserJoinRequest, reviewer, comment: str = "", request=None
) -> UserJoinRequest:
    """
    Подтверждает заявку пользователя и применяет связанные изменения.

    Args:
        join_request:
            Заявка пользователя.
        reviewer:
            Проверяющий пользователь.
        comment:
            Комментарий проверки.
        request:
            HTTP-запрос.

    Returns:
        UserJoinRequest: Обновлённая заявка.
    """

    join_request = UserJoinRequest.objects.select_for_update().get(id=join_request.id)

    if join_request.status != JoinRequestStatus.PENDING:
        raise ConflictApplicationError(
            "Можно подтвердить только заявку в ожидании.",
            code="join_request_not_pending",
        )

    join_request.approve(user=reviewer, comment=comment, save=True)

    if join_request.request_type == JoinRequestType.TEACHER_TO_ORGANIZATION:
        _approve_teacher_request(join_request=join_request, reviewer=reviewer)
    elif join_request.request_type == JoinRequestType.LEARNER_TO_GROUP:
        _approve_learner_request(join_request=join_request, reviewer=reviewer)
    elif join_request.request_type == JoinRequestType.GUARDIAN_TO_LEARNER:
        _approve_guardian_request(join_request=join_request, reviewer=reviewer)
    else:
        raise ValidationApplicationError(
            "Неизвестный тип заявки.",
            code="unknown_join_request_type",
        )

    activate_user(user=join_request.user, request=request)

    log_join_request_approved(
        actor=reviewer,
        target_user=join_request.user,
        join_request=join_request,
        request=request,
    )

    return join_request


@transaction.atomic
def reject_join_request(
    *, join_request: UserJoinRequest, reviewer, comment: str = "", request=None
) -> UserJoinRequest:
    """
    Отклоняет заявку пользователя.

    Args:
        join_request:
            Заявка пользователя.
        reviewer:
            Проверяющий пользователь.
        comment:
            Комментарий проверки.
        request:
            HTTP-запрос.

    Returns:
        UserJoinRequest: Обновлённая заявка.
    """

    join_request = UserJoinRequest.objects.select_for_update().get(id=join_request.id)

    if join_request.status != JoinRequestStatus.PENDING:
        raise ConflictApplicationError(
            "Можно отклонить только заявку в ожидании.",
            code="join_request_not_pending",
        )

    join_request.reject(user=reviewer, comment=comment, save=True)

    schedule_user_deletion_after_rejection(
        user=join_request.user,
        actor=reviewer,
        reason=comment or "Заявка пользователя отклонена.",
        request=request,
    )

    log_join_request_rejected(
        actor=reviewer,
        target_user=join_request.user,
        join_request=join_request,
        request=request,
    )

    return join_request


def _approve_teacher_request(*, join_request: UserJoinRequest, reviewer) -> None:
    """
    Применяет подтверждение заявки преподавателя.

    Args:
        join_request:
            Заявка преподавателя.
        reviewer:
            Проверяющий пользователь.
    """

    profile = get_teacher_profile_by_user(join_request.user)

    if profile:
        profile.status = ProfileStatus.VERIFIED
        profile.verified_by = reviewer
        profile.verified_at = join_request.reviewed_at
        profile.save(
            update_fields=["status", "verified_by", "verified_at", "updated_at"]
        )

    UserRole.objects.filter(
        user=join_request.user,
        role__code=RoleCode.TEACHER,
        organization=join_request.organization,
        department=join_request.department,
        status=UserRoleStatus.PENDING,
    ).update(status=UserRoleStatus.ACTIVE)


def _approve_learner_request(*, join_request: UserJoinRequest, reviewer) -> None:
    """
    Применяет подтверждение заявки учащегося.

    Args:
        join_request:
            Заявка учащегося.
        reviewer:
            Проверяющий пользователь.
    """

    profile = get_learner_profile_by_user(join_request.user)

    if profile:
        profile.status = ProfileStatus.VERIFIED
        profile.verified_by = reviewer
        profile.verified_at = join_request.reviewed_at
        profile.save(
            update_fields=["status", "verified_by", "verified_at", "updated_at"]
        )

    UserRole.objects.filter(
        user=join_request.user,
        role__code=RoleCode.LEARNER,
        organization=join_request.organization,
        department=join_request.department,
        group=join_request.group,
        status=UserRoleStatus.PENDING,
    ).update(status=UserRoleStatus.ACTIVE)


def _approve_guardian_request(*, join_request: UserJoinRequest, reviewer) -> None:
    """
    Применяет подтверждение заявки родителя.

    Args:
        join_request:
            Заявка родителя.
        reviewer:
            Проверяющий пользователь.
    """

    link = get_guardian_link(join_request.user, join_request.target_user)

    if link:
        link.approve(user=reviewer, save=True)

    UserRole.objects.filter(
        user=join_request.user,
        role__code=RoleCode.GUARDIAN,
        organization=join_request.organization,
        status=UserRoleStatus.PENDING,
    ).update(status=UserRoleStatus.ACTIVE)
