from __future__ import annotations

from apps.core.exceptions import ValidationApplicationError
from apps.users.models import Role
from apps.users.selectors.role_selectors import get_role_by_code


def get_required_role(role_code: str) -> Role:
    """
    Возвращает обязательную системную роль.

    Args:
        role_code:
            Код роли.

    Returns:
        Role: Найденная роль.

    Raises:
        ValidationApplicationError: Если роль не создана.
    """

    role = get_role_by_code(role_code)

    if role is None:
        raise ValidationApplicationError(
            f"Системная роль {role_code} не создана.",
            code="role_not_found",
        )

    return role
