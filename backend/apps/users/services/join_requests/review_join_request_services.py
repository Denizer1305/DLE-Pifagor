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
from django.utils import timezone


@transaction.atomic
def approve_join_request(
    *,
    join_request: UserJoinRequest,
    reviewer,
    comment: str = "",
    request=None,
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

    join_request = UserJoinRequest.objects.select_for_update().get(
        id=join_request.id,
    )

    if join_request.status != JoinRequestStatus.PENDING:
        raise ConflictApplicationError(
            "Можно подтвердить только заявку в ожидании.",
            code="join_request_not_pending",
        )

    _validate_join_request_can_be_approved(join_request=join_request)

    join_request.approve(
        user=reviewer,
        comment=comment,
        save=True,
    )

    if join_request.request_type == JoinRequestType.TEACHER_TO_ORGANIZATION:
        _approve_teacher_request(
            join_request=join_request,
            reviewer=reviewer,
        )
    elif join_request.request_type == JoinRequestType.LEARNER_TO_GROUP:
        _approve_learner_request(
            join_request=join_request,
            reviewer=reviewer,
        )
    elif join_request.request_type == JoinRequestType.GUARDIAN_TO_LEARNER:
        _approve_guardian_request(
            join_request=join_request,
            reviewer=reviewer,
        )
    else:
        raise ValidationApplicationError(
            "Неизвестный тип заявки.",
            code="unknown_join_request_type",
        )

    activate_user(
        user=join_request.user,
        request=request,
    )

    log_join_request_approved(
        actor=reviewer,
        target_user=join_request.user,
        join_request=join_request,
        request=request,
    )

    return join_request


@transaction.atomic
def reject_join_request(
    *,
    join_request: UserJoinRequest,
    reviewer,
    comment: str = "",
    request=None,
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

    join_request = UserJoinRequest.objects.select_for_update().get(
        id=join_request.id,
    )

    if join_request.status != JoinRequestStatus.PENDING:
        raise ConflictApplicationError(
            "Можно отклонить только заявку в ожидании.",
            code="join_request_not_pending",
        )

    join_request.reject(
        user=reviewer,
        comment=comment,
        save=True,
    )

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


def _validate_join_request_can_be_approved(
    *,
    join_request: UserJoinRequest,
) -> None:
    """
    Проверяет, что заявка содержит обязательные целевые сущности.

    Args:
        join_request:
            Заявка пользователя.

    Raises:
        ValidationApplicationError: Если заявка неполная.
    """

    if join_request.request_type == JoinRequestType.TEACHER_TO_ORGANIZATION:
        if join_request.organization is None:
            raise ValidationApplicationError(
                "В заявке преподавателя не указана организация.",
                code="teacher_join_request_without_organization",
            )

        return

    if join_request.request_type == JoinRequestType.LEARNER_TO_GROUP:
        if join_request.organization is None:
            raise ValidationApplicationError(
                "В заявке учащегося не указана организация.",
                code="learner_join_request_without_organization",
            )

        if join_request.group is None:
            raise ValidationApplicationError(
                "В заявке учащегося не указана учебная группа.",
                code="learner_join_request_without_group",
            )

        return

    if join_request.request_type == JoinRequestType.GUARDIAN_TO_LEARNER:
        if join_request.target_user is None:
            raise ValidationApplicationError(
                "В заявке родителя не указан учащийся.",
                code="guardian_join_request_without_target_user",
            )

        return

    raise ValidationApplicationError(
        "Неизвестный тип заявки.",
        code="unknown_join_request_type",
    )


def _approve_teacher_request(
    *,
    join_request: UserJoinRequest,
    reviewer,
) -> None:
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
            update_fields=[
                "status",
                "verified_by",
                "verified_at",
                "updated_at",
            ]
        )

    _activate_pending_role(
        user=join_request.user,
        role_code=RoleCode.TEACHER,
        organization=join_request.organization,
    )

    _ensure_teacher_organization_link(
        join_request=join_request,
        profile=profile,
    )


def _approve_learner_request(
    *,
    join_request: UserJoinRequest,
    reviewer,
) -> None:
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
            update_fields=[
                "status",
                "verified_by",
                "verified_at",
                "updated_at",
            ]
        )

    _activate_pending_role(
        user=join_request.user,
        role_code=RoleCode.LEARNER,
        organization=join_request.organization,
        department=join_request.department,
        group=join_request.group,
    )


def _approve_guardian_request(
    *,
    join_request: UserJoinRequest,
    reviewer,
) -> None:
    """
    Применяет подтверждение заявки родителя.

    Args:
        join_request:
            Заявка родителя.
        reviewer:
            Проверяющий пользователь.
    """

    link = get_guardian_link(
        join_request.user,
        join_request.target_user,
    )

    if link:
        link.approve(
            user=reviewer,
            save=True,
        )

    _activate_pending_role(
        user=join_request.user,
        role_code=RoleCode.GUARDIAN,
        organization=join_request.organization,
    )


def _activate_pending_role(
    *,
    user,
    role_code: str,
    organization=None,
    department=None,
    group=None,
) -> int:
    """
    Активирует ожидающую роль пользователя.

    Args:
        user:
            Пользователь.
        role_code:
            Код роли.
        organization:
            Организация роли.
        department:
            Отделение роли.
        group:
            Группа роли.

    Returns:
        int: Количество обновлённых ролей.
    """

    filters = {
        "user": user,
        "role__code": role_code,
        "organization": organization,
        "department": department,
        "group": group,
        "status": UserRoleStatus.PENDING,
    }

    return UserRole.objects.filter(**filters).update(
        status=UserRoleStatus.ACTIVE,
    )


def _ensure_teacher_organization_link(
    *,
    join_request: UserJoinRequest,
    profile,
) -> None:
    """
    Создаёт или восстанавливает связь преподавателя с организацией.

    Args:
        join_request:
            Подтверждённая заявка преподавателя.
        profile:
            Профиль преподавателя.
    """

    from apps.organizations.models import TeacherOrganization

    teacher = join_request.user
    organization = join_request.organization

    if organization is None:
        raise ValidationApplicationError(
            "Нельзя создать связь преподавателя без организации.",
            code="teacher_organization_required",
        )

    has_other_primary_link = (
        TeacherOrganization.objects.filter(
            teacher=teacher,
            is_primary=True,
            is_active=True,
        )
        .exclude(
            organization=organization,
        )
        .exists()
    )

    position = ""

    if profile:
        position = profile.position or profile.public_title or ""

    teacher_organization, created = TeacherOrganization.objects.get_or_create(
        teacher=teacher,
        organization=organization,
        defaults={
            "position": position,
            "is_primary": not has_other_primary_link,
            "is_active": True,
            "starts_at": timezone.localdate(),
        },
    )

    if created:
        return

    update_fields = []

    if not teacher_organization.is_active:
        teacher_organization.is_active = True
        update_fields.append("is_active")

    if not teacher_organization.starts_at:
        teacher_organization.starts_at = timezone.localdate()
        update_fields.append("starts_at")

    if not teacher_organization.position and position:
        teacher_organization.position = position
        update_fields.append("position")

    if not has_other_primary_link and not teacher_organization.is_primary:
        teacher_organization.is_primary = True
        update_fields.append("is_primary")

    if update_fields:
        update_fields.append("updated_at")
        teacher_organization.save(
            update_fields=update_fields,
        )
