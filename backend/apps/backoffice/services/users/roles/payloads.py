from __future__ import annotations

from dataclasses import dataclass

from rest_framework.exceptions import ValidationError


@dataclass(frozen=True, slots=True)
class BackofficeRoleAssignmentPayload:
    """
    Нормализованный payload назначения роли пользователю.
    """

    role_id: int
    organization_id: int | None = None
    department_id: int | None = None
    group_id: int | None = None


def normalize_backoffice_role_assignment_payload(
    raw_payload: dict,
) -> BackofficeRoleAssignmentPayload:
    """
    Нормализует payload назначения роли.
    """

    role_id = raw_payload.get("role_id") or raw_payload.get("role")

    if not role_id:
        raise ValidationError(
            {
                "role_id": "Необходимо указать роль.",
            }
        )

    return BackofficeRoleAssignmentPayload(
        role_id=int(role_id),
        organization_id=(
            raw_payload.get("organization_id") or raw_payload.get("organization")
        ),
        department_id=(
            raw_payload.get("department_id") or raw_payload.get("department")
        ),
        group_id=raw_payload.get("group_id") or raw_payload.get("group"),
    )


# Совместимые alias'ы на время переноса старой admin-user логики.
AdminRoleAssignmentPayload = BackofficeRoleAssignmentPayload
normalize_role_assignment_payload = normalize_backoffice_role_assignment_payload
