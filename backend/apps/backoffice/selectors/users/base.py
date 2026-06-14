from __future__ import annotations

from apps.core.permissions import is_active_user, is_superadmin
from apps.users.constants.lifecycle import UserRoleStatus
from apps.users.constants.roles import ORGANIZATION_ADMIN_ROLE_CODES, RoleCode
from apps.users.models import User, UserRole
from django.db.models import Prefetch, Q, QuerySet


def get_backoffice_user_roles_prefetch_queryset() -> QuerySet:
    """
    Возвращает QuerySet ролей пользователя для prefetch_related.

    Используется в административном списке и детальной карточке,
    чтобы не получать N+1-запросы по ролям, организациям и группам.
    """

    return UserRole.objects.select_related(
        "role",
        "organization",
        "department",
        "group",
        "assigned_by",
        "revoked_by",
    ).order_by(
        "role__sort_order",
        "role__label",
    )


def get_backoffice_users_base_queryset() -> QuerySet:
    """
    Возвращает базовый QuerySet пользователей для backoffice.

    Важно:
        Этот QuerySet ещё не ограничивает область видимости администратора.
        Для API нужно использовать get_backoffice_users_queryset_for_actor().
    """

    return (
        User.objects.all()
        .select_related(
            "account_managed_by",
            "profile",
        )
        .prefetch_related(
            Prefetch(
                "user_roles",
                queryset=get_backoffice_user_roles_prefetch_queryset(),
            ),
        )
        .order_by(
            "last_name",
            "first_name",
            "email",
        )
    )


def get_actor_backoffice_admin_roles_queryset(*, actor) -> QuerySet:
    """
    Возвращает активные административные роли администратора.

    Эти роли определяют область видимости:
    - директор / администратор организации — организация;
    - заведующий отделением — отделение.
    """

    if not is_active_user(actor):
        return UserRole.objects.none()

    return get_backoffice_user_roles_prefetch_queryset().filter(
        user=actor,
        status=UserRoleStatus.ACTIVE,
        role__code__in=ORGANIZATION_ADMIN_ROLE_CODES,
    )


def is_backoffice_organization_admin_actor(*, actor) -> bool:
    """
    Проверяет, есть ли у пользователя административная роль организации.
    """

    return get_actor_backoffice_admin_roles_queryset(actor=actor).exists()


def build_backoffice_users_scope_query_for_actor(*, actor) -> Q:
    """
    Строит Q-условие области видимости пользователей для администратора.

    Правила:
    - директор и администратор организации видят пользователей своей организации;
    - заведующий отделением видит пользователей своего отделения;
    - superadmin обрабатывается выше и сюда обычно не попадает.
    """

    scope_query = Q(pk__in=[])

    for user_role in get_actor_backoffice_admin_roles_queryset(actor=actor):
        role_code = user_role.role.code

        if role_code in {RoleCode.DIRECTOR, RoleCode.ORG_ADMIN}:
            if user_role.organization_id:
                scope_query |= Q(
                    user_roles__status=UserRoleStatus.ACTIVE,
                    user_roles__organization_id=user_role.organization_id,
                )

        if role_code == RoleCode.DEPARTMENT_HEAD:
            if user_role.department_id:
                scope_query |= Q(
                    user_roles__status=UserRoleStatus.ACTIVE,
                    user_roles__department_id=user_role.department_id,
                )

    return scope_query


def get_backoffice_users_queryset_for_actor(*, actor) -> QuerySet:
    """
    Возвращает пользователей, доступных администратору.

    Правила:
    - superadmin / platform admin видит всех пользователей;
    - директор / org_admin видит пользователей своей организации;
    - заведующий отделением видит пользователей своего отделения;
    - обычный пользователь не видит административный список.
    """

    queryset = get_backoffice_users_base_queryset()

    if not is_active_user(actor):
        return User.objects.none()

    if is_superadmin(actor):
        return queryset

    if not is_backoffice_organization_admin_actor(actor=actor):
        return User.objects.none()

    scope_query = build_backoffice_users_scope_query_for_actor(actor=actor)

    return queryset.filter(scope_query).distinct()
