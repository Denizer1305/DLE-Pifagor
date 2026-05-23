from __future__ import annotations

from apps.users.constants.lifecycle import ProfileStatus, UserRoleStatus, UserStatus
from apps.users.constants.roles import RoleCode
from apps.users.models import User, UserRole
from apps.users.services.audit_services import log_user_registered
from apps.users.services.profiles import create_base_profile, create_guardian_profile
from apps.users.services.registration.registration_helpers import get_required_role
from apps.users.services.user_settings_services import create_default_user_settings
from apps.users.tasks.email_tasks import send_email_verification_task
from django.db import transaction


@transaction.atomic
def register_guardian(
    *,
    email: str,
    phone: str,
    password: str,
    first_name: str,
    last_name: str,
    middle_name: str = "",
    birth_date=None,
    request=None,
) -> User:
    """
    Регистрирует родителя или законного представителя.

    Args:
        email:
            Email родителя.
        phone:
            Телефон родителя.
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
        request:
            HTTP-запрос.

    Returns:
        User: Созданный пользователь родителя.
    """

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

    create_base_profile(user=user)
    create_guardian_profile(
        user=user,
        status=ProfileStatus.DRAFT,
    )
    create_default_user_settings(user=user)

    role = get_required_role(RoleCode.GUARDIAN)

    UserRole.objects.create(
        user=user,
        role=role,
        status=UserRoleStatus.PENDING,
    )

    log_user_registered(user=user, request=request)

    transaction.on_commit(lambda: send_email_verification_task.delay(user_id=user.id))

    return user
