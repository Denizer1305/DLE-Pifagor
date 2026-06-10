from __future__ import annotations

GLOBAL_COURSE_ADMIN_ROLE_CODES = frozenset(
    {
        "superadmin",
        "platform_admin",
        "admin",
    }
)

COURSE_ORGANIZATION_ADMIN_ROLE_CODES = frozenset(
    {
        "org_admin",
        "director",
        "head_of_department",
    }
)

COURSE_TEACHER_ROLE_CODES = frozenset(
    {
        "teacher",
    }
)

COURSE_LEARNER_ROLE_CODES = frozenset(
    {
        "learner",
    }
)

COURSE_CURATOR_ROLE_CODES = frozenset(
    {
        "curator",
    }
)

COURSE_STAFF_ROLE_CODES = frozenset(
    {
        "superadmin",
        "platform_admin",
        "admin",
        "org_admin",
        "director",
        "head_of_department",
        "teacher",
        "curator",
    }
)

COURSE_READONLY_ROLE_CODES = frozenset(
    {
        "learner",
        "guardian",
    }
)

COURSE_EDITOR_ROLE_CODES = frozenset(
    {
        "superadmin",
        "platform_admin",
        "admin",
        "org_admin",
        "director",
        "head_of_department",
        "teacher",
    }
)
