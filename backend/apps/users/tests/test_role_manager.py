from __future__ import annotations

import pytest
from apps.users.constants.roles import RoleCode
from apps.users.models import Role


@pytest.mark.django_db
def test_ensure_system_roles_creates_roles() -> None:
    """
    Проверяет создание системных ролей через RoleManager.
    """

    roles = Role.objects.ensure_system_roles()

    assert len(roles) == len(RoleCode.choices)
    assert Role.objects.filter(code=RoleCode.LEARNER).exists()
    assert Role.objects.filter(code=RoleCode.TEACHER).exists()
    assert Role.objects.filter(code=RoleCode.SUPERADMIN).exists()


@pytest.mark.django_db
def test_get_by_code_returns_role() -> None:
    """
    Проверяет получение роли по коду.
    """

    Role.objects.ensure_system_roles()

    role = Role.objects.get_by_code(RoleCode.GUARDIAN)

    assert role.code == RoleCode.GUARDIAN
    assert role.is_active is True
