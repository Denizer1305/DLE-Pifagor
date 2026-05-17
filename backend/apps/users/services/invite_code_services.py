from __future__ import annotations

from datetime import timedelta

from apps.core.exceptions import ConflictApplicationError, ValidationApplicationError
from apps.users.constants.audit import UserAuditAction
from apps.users.constants.onboarding import (
    DEFAULT_GUARDIAN_LINK_CODE_TTL_HOURS,
    DEFAULT_INVITE_CODE_LENGTH,
    DEFAULT_INVITE_CODE_TTL_HOURS,
    InviteCodePurpose,
)
from apps.users.models import InviteCode
from apps.users.selectors.invite_code_selectors import (
    get_available_invite_code_by_raw_code,
)
from apps.users.services.audit_services import create_user_audit_log
from django.db import transaction
from django.utils import timezone


def create_invite_code(
    *,
    purpose: str,
    created_by,
    organization=None,
    department=None,
    group=None,
    target_user=None,
    ttl_hours: int = DEFAULT_INVITE_CODE_TTL_HOURS,
    max_uses: int = 1,
    length: int = DEFAULT_INVITE_CODE_LENGTH,
    request=None,
) -> tuple[InviteCode, str]:
    """
    Создаёт временный код приглашения.

    В базе хранится только хеш кода.
    Открытый код возвращается из сервиса один раз и должен быть показан пользователю.

    Args:
        purpose:
            Назначение кода.
        created_by:
            Пользователь, создавший код.
        organization:
            Образовательная организация.
        department:
            Отделение.
        group:
            Учебная группа.
        target_user:
            Целевой пользователь.
        ttl_hours:
            Время жизни кода в часах.
        max_uses:
            Максимальное количество использований.
        length:
            Длина открытого кода.
        request:
            HTTP-запрос.

    Returns:
        tuple[InviteCode, str]: Созданный объект кода и открытый код.
    """

    raw_code = InviteCode.make_code(length=length)
    code_hash = InviteCode.make_hash(raw_code)

    invite_code = InviteCode.objects.create(
        code_hash=code_hash,
        purpose=purpose,
        organization=organization,
        department=department,
        group=group,
        created_by=created_by,
        target_user=target_user,
        expires_at=timezone.now() + timedelta(hours=ttl_hours),
        max_uses=max_uses,
        used_count=0,
        is_active=True,
    )

    create_user_audit_log(
        actor=created_by,
        target_user=target_user,
        action=UserAuditAction.INVITE_CODE_CREATED,
        message="Создан временный код приглашения.",
        metadata={
            "invite_code_id": invite_code.id,
            "purpose": purpose,
            "organization_id": getattr(organization, "id", None),
            "department_id": getattr(department, "id", None),
            "group_id": getattr(group, "id", None),
        },
        request=request,
    )

    return invite_code, raw_code


def validate_invite_code(
    *,
    raw_code: str,
    purpose: str | None = None,
    organization=None,
    department=None,
    group=None,
    target_user=None,
) -> InviteCode:
    """
    Проверяет временный код приглашения.

    Args:
        raw_code:
            Открытый код, введённый пользователем.
        purpose:
            Ожидаемое назначение кода.
        organization:
            Ожидаемая организация.
        department:
            Ожидаемое отделение.
        group:
            Ожидаемая группа.
        target_user:
            Ожидаемый целевой пользователь.

    Returns:
        InviteCode: Проверенный код.

    Raises:
        ValidationApplicationError: Если код не найден или не подходит.
    """

    invite_code = get_available_invite_code_by_raw_code(raw_code)

    if invite_code is None:
        raise ValidationApplicationError(
            "Код приглашения недействителен или истёк.",
            code="invalid_invite_code",
        )

    if purpose is not None and invite_code.purpose != purpose:
        raise ValidationApplicationError(
            "Код приглашения не подходит для этого действия.",
            code="invalid_invite_code_purpose",
        )

    if organization is not None and invite_code.organization_id != organization.id:
        raise ValidationApplicationError(
            "Код приглашения не относится к выбранной организации.",
            code="invalid_invite_code_organization",
        )

    if department is not None and invite_code.department_id != department.id:
        raise ValidationApplicationError(
            "Код приглашения не относится к выбранному отделению.",
            code="invalid_invite_code_department",
        )

    if group is not None and invite_code.group_id != group.id:
        raise ValidationApplicationError(
            "Код приглашения не относится к выбранной группе.",
            code="invalid_invite_code_group",
        )

    if target_user is not None and invite_code.target_user_id != target_user.id:
        raise ValidationApplicationError(
            "Код приглашения не относится к выбранному пользователю.",
            code="invalid_invite_code_target_user",
        )

    return invite_code


@transaction.atomic
def use_invite_code(
    *, invite_code: InviteCode, used_by=None, request=None
) -> InviteCode:
    """
    Отмечает код приглашения как использованный.

    Args:
        invite_code:
            Код приглашения.
        used_by:
            Пользователь, который использовал код.
        request:
            HTTP-запрос.

    Returns:
        InviteCode: Обновлённый код.

    Raises:
        ConflictApplicationError: Если код уже недоступен.
    """

    invite_code = InviteCode.objects.select_for_update().get(id=invite_code.id)

    if not invite_code.is_available:
        raise ConflictApplicationError(
            "Код приглашения уже недоступен.",
            code="invite_code_not_available",
        )

    invite_code.mark_used(save=True)

    create_user_audit_log(
        actor=used_by,
        target_user=used_by,
        action=UserAuditAction.INVITE_CODE_USED,
        message="Код приглашения использован.",
        metadata={
            "invite_code_id": invite_code.id,
            "purpose": invite_code.purpose,
        },
        request=request,
    )

    return invite_code


def create_teacher_registration_code(
    *,
    created_by,
    organization,
    department=None,
    ttl_hours: int = DEFAULT_INVITE_CODE_TTL_HOURS,
    request=None,
) -> tuple[InviteCode, str]:
    """
    Создаёт код регистрации преподавателя.

    Args:
        created_by:
            Пользователь, создавший код.
        organization:
            Организация.
        department:
            Отделение.
        ttl_hours:
            Время жизни кода в часах.
        request:
            HTTP-запрос.

    Returns:
        tuple[InviteCode, str]: Код приглашения и открытый код.
    """

    return create_invite_code(
        purpose=InviteCodePurpose.TEACHER_REGISTRATION,
        created_by=created_by,
        organization=organization,
        department=department,
        ttl_hours=ttl_hours,
        request=request,
    )


def create_guardian_curator_code(
    *,
    created_by,
    organization,
    group,
    ttl_hours: int = DEFAULT_GUARDIAN_LINK_CODE_TTL_HOURS,
    request=None,
) -> tuple[InviteCode, str]:
    """
    Создаёт код куратора для связи родителя и учащегося.

    Args:
        created_by:
            Куратор или администратор.
        organization:
            Организация.
        group:
            Учебная группа.
        ttl_hours:
            Время жизни кода.
        request:
            HTTP-запрос.

    Returns:
        tuple[InviteCode, str]: Код приглашения и открытый код.
    """

    return create_invite_code(
        purpose=InviteCodePurpose.GUARDIAN_LINK_CURATOR,
        created_by=created_by,
        organization=organization,
        group=group,
        ttl_hours=ttl_hours,
        request=request,
    )


def create_guardian_learner_code(
    *,
    created_by,
    learner,
    organization=None,
    group=None,
    ttl_hours: int = DEFAULT_GUARDIAN_LINK_CODE_TTL_HOURS,
    request=None,
) -> tuple[InviteCode, str]:
    """
    Создаёт код учащегося для подтверждения связи с родителем.

    Используется для учащихся старше 14 лет.

    Args:
        created_by:
            Пользователь, создавший код.
        learner:
            Учащийся.
        organization:
            Организация.
        group:
            Группа.
        ttl_hours:
            Время жизни кода.
        request:
            HTTP-запрос.

    Returns:
        tuple[InviteCode, str]: Код приглашения и открытый код.
    """

    return create_invite_code(
        purpose=InviteCodePurpose.GUARDIAN_LINK_LEARNER,
        created_by=created_by,
        target_user=learner,
        organization=organization,
        group=group,
        ttl_hours=ttl_hours,
        request=request,
    )
