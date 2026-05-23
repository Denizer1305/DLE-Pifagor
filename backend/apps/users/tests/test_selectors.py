from __future__ import annotations

import pytest
from apps.users.constants.lifecycle import UserRoleStatus, UserStatus
from apps.users.constants.roles import RoleCode
from apps.users.models import UserRole
from apps.users.selectors import (
    get_active_users_queryset,
    get_user_active_role_codes,
    get_user_by_email,
    get_user_by_phone,
    user_email_exists,
    user_has_active_role,
    user_phone_exists,
)
from apps.users.tests.factories import make_role, make_user


@pytest.mark.django_db
def test_get_user_by_email_returns_user() -> None:
    """
    Проверяет поиск пользователя по email.
    """

    user = make_user(email="selector@example.com")

    found_user = get_user_by_email("SELECTOR@example.com")

    assert found_user == user


@pytest.mark.django_db
def test_get_user_by_phone_returns_user() -> None:
    """
    Проверяет поиск пользователя по телефону.
    """

    user = make_user(phone="+79007770001")

    found_user = get_user_by_phone("+79007770001")

    assert found_user == user


@pytest.mark.django_db
def test_user_email_exists() -> None:
    """
    Проверяет проверку существования email.
    """

    make_user(email="exists@example.com")

    assert user_email_exists("exists@example.com") is True
    assert user_email_exists("missing@example.com") is False


@pytest.mark.django_db
def test_user_phone_exists() -> None:
    """
    Проверяет проверку существования телефона.
    """

    make_user(phone="+79007770002")

    assert user_phone_exists("+79007770002") is True
    assert user_phone_exists("+79007770003") is False


@pytest.mark.django_db
def test_get_active_users_queryset_returns_only_active_users() -> None:
    """
    Проверяет выборку активных пользователей.
    """

    active_user = make_user(
        email="active@example.com",
        status=UserStatus.ACTIVE,
        is_active=True,
    )
    make_user(
        email="blocked@example.com",
        status=UserStatus.BLOCKED,
        is_active=False,
    )

    users = list(get_active_users_queryset())

    assert active_user in users
    assert len(users) == 1


@pytest.mark.django_db
def test_user_has_active_role() -> None:
    """
    Проверяет наличие активной роли у пользователя.
    """

    user = make_user(email="role-user@example.com")
    role = make_role(code=RoleCode.LEARNER)

    UserRole.objects.create(
        user=user,
        role=role,
        status=UserRoleStatus.ACTIVE,
    )

    assert user_has_active_role(user=user, role_code=RoleCode.LEARNER) is True
    assert user_has_active_role(user=user, role_code=RoleCode.TEACHER) is False


@pytest.mark.django_db
def test_get_user_active_role_codes() -> None:
    """
    Проверяет получение кодов активных ролей пользователя.
    """

    user = make_user(email="role-codes@example.com")
    learner_role = make_role(code=RoleCode.LEARNER)
    teacher_role = make_role(code=RoleCode.TEACHER)

    UserRole.objects.create(
        user=user,
        role=learner_role,
        status=UserRoleStatus.ACTIVE,
    )
    UserRole.objects.create(
        user=user,
        role=teacher_role,
        status=UserRoleStatus.PENDING,
    )

    role_codes = get_user_active_role_codes(user)

    assert role_codes == {RoleCode.LEARNER}
