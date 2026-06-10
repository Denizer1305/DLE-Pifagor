from __future__ import annotations

GLOBAL_ADMIN_ROLE_CODES = frozenset(
    {
        "superadmin",
        "platform_admin",
        "admin",
    }
)

ORGANIZATION_ADMIN_ROLE_CODES = frozenset(
    {
        "org_admin",
        "director",
        "head_of_department",
    }
)

TEACHER_ROLE_CODES = frozenset(
    {
        "teacher",
    }
)

LEARNER_ROLE_CODES = frozenset(
    {
        "learner",
    }
)

EDUCATION_STAFF_ROLE_CODES = frozenset(
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
