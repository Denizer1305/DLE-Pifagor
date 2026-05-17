from __future__ import annotations

from apps.users.constants.audit import UserAuditAction
from apps.users.constants.lifecycle import ProfileStatus, UserRoleStatus, UserStatus
from apps.users.constants.roles import RoleCode
from apps.users.models import User, UserRole
from apps.users.services.audit_services import create_user_audit_log
from apps.users.services.join_requests import create_learner_join_request
from apps.users.services.profiles import (
    create_base_profile,
    create_guardian_learner_link,
    create_learner_profile,
)
from apps.users.services.registration.registration_helpers import get_required_role
from apps.users.services.user_settings_services import create_default_user_settings
from django.db import transaction


@transaction.atomic
def register_minor_learner_by_guardian(
    *,
    guardian,
    email: str,
    phone: str,
    password: str,
    first_name: str,
    last_name: str,
    middle_name: str = "",
    birth_date=None,
    organization=None,
    department=None,
    group=None,
    curator=None,
    relation_type=None,
    request=None,
) -> User:
    """
    Регистрирует ребёнка младше 14 лет от имени родителя.

    Args:
        guardian:
            Родитель или законный представитель.
        email:
            Email ребёнка.
        phone:
            Телефон ребёнка.
        password:
            Пароль ребёнка.
        first_name:
            Имя ребёнка.
        last_name:
            Фамилия ребёнка.
        middle_name:
            Отчество ребёнка.
        birth_date:
            Дата рождения.
        organization:
            Образовательная организация.
        department:
            Отделение.
        group:
            Учебная группа.
        curator:
            Куратор.
        relation_type:
            Тип связи родителя и ребёнка.
        request:
            HTTP-запрос.

    Returns:
        User: Созданный пользователь ребёнка.
    """

    learner = User.objects.create_managed_child_user(
        email=email,
        phone=phone,
        password=password,
        account_managed_by=guardian,
        first_name=first_name,
        last_name=last_name,
        middle_name=middle_name,
        birth_date=birth_date,
        status=UserStatus.PENDING_REVIEW,
    )

    create_base_profile(user=learner)
    create_learner_profile(
        user=learner,
        organization=organization,
        department=department,
        group=group,
        curator=curator,
        is_minor=True,
        created_by_guardian=guardian,
        status=ProfileStatus.PENDING_REVIEW,
    )
    create_default_user_settings(user=learner)

    role = get_required_role(RoleCode.LEARNER)

    UserRole.objects.create(
        user=learner,
        role=role,
        organization=organization,
        department=department,
        group=group,
        status=UserRoleStatus.PENDING,
    )

    create_guardian_learner_link(
        guardian=guardian,
        learner=learner,
        relation_type=relation_type or "other",
        is_primary=True,
        is_learner_consent_required=False,
        requested_by=guardian,
    )

    create_learner_join_request(
        user=learner,
        organization=organization,
        department=department,
        group=group,
        request=request,
    )

    create_user_audit_log(
        actor=guardian,
        target_user=learner,
        action=UserAuditAction.USER_REGISTERED,
        message="Родитель зарегистрировал аккаунт ребёнка младше 14 лет.",
        request=request,
    )

    return learner
