from __future__ import annotations

from apps.core.exceptions import ValidationApplicationError
from apps.users.constants.lifecycle import ProfileStatus, UserRoleStatus, UserStatus
from apps.users.constants.roles import RoleCode
from apps.users.models import User, UserRole
from apps.users.services.audit_services import log_user_registered
from apps.users.services.join_requests import create_learner_join_request
from apps.users.services.profiles import create_base_profile, create_learner_profile
from apps.users.services.registration.registration_helpers import get_required_role
from apps.users.services.user_settings_services import create_default_user_settings
from apps.users.tasks.email_tasks import send_email_verification_task
from django.db import transaction


@transaction.atomic
def register_learner(
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
    Регистрирует учащегося старше 14 лет.

    Args:
        email:
            Email учащегося.
        phone:
            Телефон учащегося.
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
        User: Созданный пользователь учащегося.
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
    create_learner_profile(
        user=user,
        status=ProfileStatus.DRAFT,
        is_minor=False,
    )
    create_default_user_settings(user=user)

    role = get_required_role(RoleCode.LEARNER)

    UserRole.objects.create(
        user=user,
        role=role,
        status=UserRoleStatus.PENDING,
    )

    log_user_registered(user=user, request=request)

    transaction.on_commit(lambda: send_email_verification_task.delay(user_id=user.id))

    return user


@transaction.atomic
def submit_learner_group_request(
    *,
    user,
    organization,
    department=None,
    group=None,
    curator=None,
    request=None,
):
    """
    Отправляет заявку учащегося в группу после заполнения профиля.

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
            Куратор.
        request:
            HTTP-запрос.

    Returns:
        UserJoinRequest: Созданная заявка.
    """

    profile = getattr(user, "learner_profile", None)

    if profile is None:
        raise ValidationApplicationError(
            "Профиль учащегося не найден.",
            code="learner_profile_not_found",
        )

    profile.organization = organization
    profile.department = department
    profile.group = group
    profile.curator = curator
    profile.status = ProfileStatus.PENDING_REVIEW
    profile.full_clean()
    profile.save(
        update_fields=[
            "organization",
            "department",
            "group",
            "curator",
            "status",
            "updated_at",
        ]
    )

    UserRole.objects.filter(
        user=user,
        role__code=RoleCode.LEARNER,
    ).update(
        organization=organization,
        department=department,
        group=group,
    )

    return create_learner_join_request(
        user=user,
        organization=organization,
        department=department,
        group=group,
        request=request,
    )
