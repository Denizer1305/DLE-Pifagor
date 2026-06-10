from __future__ import annotations

GLOBAL_MATERIAL_ADMIN_ROLE_CODES = frozenset(
    {
        "superadmin",
        "platform_admin",
        "admin",
    }
)

MATERIAL_ORGANIZATION_ADMIN_ROLE_CODES = frozenset(
    {
        "org_admin",
        "director",
        "head_of_department",
    }
)

MATERIAL_TEACHER_ROLE_CODES = frozenset(
    {
        "teacher",
    }
)

MATERIAL_LEARNER_ROLE_CODES = frozenset(
    {
        "learner",
    }
)

MATERIAL_GUARDIAN_ROLE_CODES = frozenset(
    {
        "guardian",
    }
)

MATERIAL_CURATOR_ROLE_CODES = frozenset(
    {
        "curator",
    }
)

MATERIAL_STAFF_ROLE_CODES = frozenset(
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

MATERIAL_EDITOR_ROLE_CODES = frozenset(
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

MATERIAL_READONLY_ROLE_CODES = frozenset(
    {
        "learner",
        "guardian",
    }
)
