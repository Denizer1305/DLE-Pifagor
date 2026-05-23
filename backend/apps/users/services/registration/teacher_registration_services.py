from __future__ import annotations

from apps.core.exceptions import ValidationApplicationError
from apps.users.constants.lifecycle import ProfileStatus, UserRoleStatus, UserStatus
from apps.users.constants.onboarding import InviteCodePurpose, RegistrationAttemptStatus
from apps.users.constants.roles import RoleCode
from apps.users.models import User, UserRole
from apps.users.services.audit_services import (
    create_registration_attempt_log,
    log_user_registered,
)
from apps.users.services.invite_code_services import (
    use_invite_code,
    validate_invite_code,
)
from apps.users.services.join_requests import create_teacher_join_request
from apps.users.services.profiles import create_base_profile, create_teacher_profile
from apps.users.services.registration.registration_helpers import get_required_role
from apps.users.services.user_settings_services import create_default_user_settings
from apps.users.tasks.email_tasks import (
    send_email_verification_task,
    send_teacher_registration_pending_task,
)
from django.db import transaction


@transaction.atomic
def register_teacher(
    *,
    email: str,
    phone: str,
    password: str,
    first_name: str,
    last_name: str,
    middle_name: str = "",
    birth_date=None,
    invite_code: str,
    position: str = "",
    request=None,
) -> User:
    """
    Регистрирует преподавателя через временный код организации.

    Args:
        email:
            Email преподавателя.
        phone:
            Телефон преподавателя.
        password:
            Пароль.
        first_name:
            Имя.
        last_name:
            Фамилия.
        middle_name:
            Отчество.
        birth_date:
            Дата рождения.
        invite_code:
            Код регистрации преподавателя.
        position:
            Должность.
        request:
            HTTP-запрос.

    Returns:
        User: Созданный пользователь преподавателя.
    """

    try:
        checked_code = validate_invite_code(
            raw_code=invite_code,
            purpose=InviteCodePurpose.TEACHER_REGISTRATION,
        )
    except ValidationApplicationError as exc:
        create_registration_attempt_log(
            email=email,
            phone=phone,
            role_code=RoleCode.TEACHER,
            status=RegistrationAttemptStatus.FAILED,
            failure_reason=exc.code,
            request=request,
        )
        raise

    user = User.objects.create_user(
        email=email,
        phone=phone,
        password=password,
        first_name=first_name,
        last_name=last_name,
        middle_name=middle_name,
        birth_date=birth_date,
        status=UserStatus.PENDING_EMAIL,
    )

    role = get_required_role(RoleCode.TEACHER)

    create_base_profile(user=user)
    create_teacher_profile(
        user=user,
        organization=checked_code.organization,
        department=checked_code.department,
        position=position,
        status=ProfileStatus.PENDING_REVIEW,
    )
    create_default_user_settings(user=user)

    UserRole.objects.create(
        user=user,
        role=role,
        organization=checked_code.organization,
        department=checked_code.department,
        status=UserRoleStatus.PENDING,
    )

    create_teacher_join_request(
        user=user,
        organization=checked_code.organization,
        department=checked_code.department,
        request=request,
    )

    use_invite_code(
        invite_code=checked_code,
        used_by=user,
        request=request,
    )

    log_user_registered(user=user, request=request)

    transaction.on_commit(lambda: send_email_verification_task.delay(user_id=user.id))

    transaction.on_commit(
        lambda: send_teacher_registration_pending_task.delay(user_id=user.id)
    )

    return user
