from __future__ import annotations

from apps.users.constants.roles import (
    GUARDIAN_ROLE_CODES,
    LEARNER_ROLE_CODES,
    STAFF_ROLE_CODES,
)


class BackofficeUserRoleGroup:
    """
    Группы ролей для административного фильтра пользователей.
    """

    STUDENTS = "students"
    TEACHERS = "teachers"
    PARENTS = "parents"


BACKOFFICE_USER_ROLE_GROUP_CHOICES = (
    (BackofficeUserRoleGroup.STUDENTS, "Учащиеся"),
    (BackofficeUserRoleGroup.TEACHERS, "Преподаватели и сотрудники"),
    (BackofficeUserRoleGroup.PARENTS, "Родители"),
)
"""Choices групп ролей для фильтра пользователей."""


BACKOFFICE_USER_ROLE_GROUPS = {
    BackofficeUserRoleGroup.STUDENTS: LEARNER_ROLE_CODES,
    BackofficeUserRoleGroup.TEACHERS: STAFF_ROLE_CODES,
    BackofficeUserRoleGroup.PARENTS: GUARDIAN_ROLE_CODES,
}
"""Соответствие группы пользователей и набора role_code."""
