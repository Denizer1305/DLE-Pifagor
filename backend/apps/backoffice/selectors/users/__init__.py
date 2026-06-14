from __future__ import annotations

from .audit import (
    get_backoffice_user_audit_logs_for_actor,
    get_backoffice_user_audit_logs_for_target,
    get_backoffice_user_audit_logs_queryset,
    get_recent_backoffice_user_audit_logs_for_target,
)
from .base import (
    build_backoffice_users_scope_query_for_actor,
    get_actor_backoffice_admin_roles_queryset,
    get_backoffice_user_roles_prefetch_queryset,
    get_backoffice_users_base_queryset,
    get_backoffice_users_queryset_for_actor,
    is_backoffice_organization_admin_actor,
)
from .bulk import (
    actor_can_access_all_backoffice_users_for_bulk_action,
    get_accessible_backoffice_user_ids_for_bulk_action,
    get_backoffice_users_for_bulk_action,
)
from .detail import (
    actor_can_access_backoffice_user,
    actor_can_manage_backoffice_user,
    get_backoffice_user_by_id_for_actor,
    get_backoffice_user_detail_queryset_for_actor,
    get_required_backoffice_user_by_id_for_actor,
)
from .list import (
    get_backoffice_parents_queryset_for_actor,
    get_backoffice_students_queryset_for_actor,
    get_backoffice_teachers_queryset_for_actor,
    get_backoffice_users_list_queryset,
)
from .roles import (
    get_backoffice_active_user_roles_queryset,
    get_backoffice_role_by_code,
    get_backoffice_roles_queryset,
    get_backoffice_user_role_by_id,
    get_backoffice_user_roles_queryset,
    get_required_backoffice_role_by_code,
)

__all__ = [
    "actor_can_access_all_backoffice_users_for_bulk_action",
    "actor_can_access_backoffice_user",
    "actor_can_manage_backoffice_user",
    "build_backoffice_users_scope_query_for_actor",
    "get_accessible_backoffice_user_ids_for_bulk_action",
    "get_actor_backoffice_admin_roles_queryset",
    "get_backoffice_active_user_roles_queryset",
    "get_backoffice_parents_queryset_for_actor",
    "get_backoffice_role_by_code",
    "get_backoffice_roles_queryset",
    "get_backoffice_students_queryset_for_actor",
    "get_backoffice_teachers_queryset_for_actor",
    "get_backoffice_user_audit_logs_for_actor",
    "get_backoffice_user_audit_logs_for_target",
    "get_backoffice_user_audit_logs_queryset",
    "get_backoffice_user_by_id_for_actor",
    "get_backoffice_user_detail_queryset_for_actor",
    "get_backoffice_user_role_by_id",
    "get_backoffice_user_roles_prefetch_queryset",
    "get_backoffice_user_roles_queryset",
    "get_backoffice_users_base_queryset",
    "get_backoffice_users_for_bulk_action",
    "get_backoffice_users_list_queryset",
    "get_backoffice_users_queryset_for_actor",
    "get_recent_backoffice_user_audit_logs_for_target",
    "get_required_backoffice_role_by_code",
    "get_required_backoffice_user_by_id_for_actor",
    "is_backoffice_organization_admin_actor",
]
