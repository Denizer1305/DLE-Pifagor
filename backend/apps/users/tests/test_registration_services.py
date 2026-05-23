from __future__ import annotations

from datetime import date

import pytest
from apps.users.constants.lifecycle import ProfileStatus, UserRoleStatus, UserStatus
from apps.users.constants.roles import RoleCode
from apps.users.models import LearnerProfile, UserRole
from apps.users.services.registration import register_guardian, register_learner
from apps.users.tests.factories import make_role


@pytest.mark.django_db
def test_register_learner_creates_user_profile_role_and_settings() -> None:
    """
    Проверяет регистрацию учащегося старше 14 лет.

    Тест не затрагивает organization/group, потому что organizations/
    будет финализирован отдельно.
    """

    make_role(code=RoleCode.LEARNER)

    user = register_learner(
        email="learner@example.com",
        phone="+79007771001",
        password="StrongPassword123",
        first_name="Иван",
        last_name="Иванов",
        birth_date=date(2005, 1, 1),
    )

    assert user.status == UserStatus.PENDING_EMAIL
    assert hasattr(user, "profile")
    assert hasattr(user, "learner_profile")
    assert hasattr(user, "settings")

    learner_profile = LearnerProfile.objects.get(user=user)

    assert learner_profile.status == ProfileStatus.DRAFT
    assert learner_profile.is_minor is False

    user_role = UserRole.objects.get(user=user)

    assert user_role.role.code == RoleCode.LEARNER
    assert user_role.status == UserRoleStatus.PENDING


@pytest.mark.django_db
def test_register_guardian_creates_user_profile_role_and_settings() -> None:
    """
    Проверяет регистрацию родителя.
    """

    make_role(code=RoleCode.GUARDIAN)

    user = register_guardian(
        email="guardian-registration@example.com",
        phone="+79007771002",
        password="StrongPassword123",
        first_name="Мария",
        last_name="Петрова",
        birth_date=date(1985, 1, 1),
    )

    assert user.status == UserStatus.PENDING_EMAIL
    assert hasattr(user, "profile")
    assert hasattr(user, "guardian_profile")
    assert hasattr(user, "settings")

    user_role = UserRole.objects.get(user=user)

    assert user_role.role.code == RoleCode.GUARDIAN
    assert user_role.status == UserRoleStatus.PENDING
