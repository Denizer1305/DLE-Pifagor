from __future__ import annotations

from apps.education.constants import EDUCATION_STAFF_ROLE_CODES, LEARNER_ROLE_CODES
from apps.education.selectors import (
    user_has_any_role,
    user_is_authenticated,
    user_is_global_admin,
    user_is_learner,
    user_is_organization_admin,
    user_is_teacher,
)
from django.contrib.auth import get_user_model

User = get_user_model()


def user_has_education_access(user: User) -> bool:
    """
    Проверяет, может ли пользователь в принципе работать
    с академическим модулем.

    Это не означает право на изменение. Это общий доступ
    к академическим данным с последующим объектным ограничением.
    """

    if not user_is_authenticated(user):
        return False

    return user_has_any_role(user, EDUCATION_STAFF_ROLE_CODES) or user_has_any_role(
        user, LEARNER_ROLE_CODES
    )


def user_can_manage_global_education(user: User) -> bool:
    """
    Проверяет право на управление глобальными академическими сущностями.

    Учебные годы и периоды не принадлежат конкретной организации,
    поэтому менять их может только глобальный администратор.
    """

    return user_is_global_admin(user)


def user_can_manage_scoped_education(user: User) -> bool:
    """
    Проверяет право на изменение академических сущностей,
    привязанных к организации / группе.
    """

    return user_is_global_admin(user) or user_is_organization_admin(user)


def user_can_read_teacher_education_data(user: User) -> bool:
    """
    Проверяет, может ли преподаватель читать свои академические данные.
    """

    return user_is_teacher(user)


def user_can_read_learner_education_data(user: User) -> bool:
    """
    Проверяет, может ли обучающийся читать свои академические данные.
    """

    return user_is_learner(user)
