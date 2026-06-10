from __future__ import annotations

from apps.users.constants.lifecycle import UserRoleStatus
from apps.users.constants.roles import (
    GUARDIAN_ROLE_CODES,
    LEARNER_ROLE_CODES,
    ORGANIZATION_ADMIN_ROLE_CODES,
    PLATFORM_ADMIN_ROLE_CODES,
    STAFF_ROLE_CODES,
    RoleCode,
)
from apps.users.models import User, UserRole
from django.db.models import Prefetch, Q, QuerySet

ADMIN_USER_ROLE_GROUPS = {
    "students": LEARNER_ROLE_CODES,
    "teachers": STAFF_ROLE_CODES,
    "parents": GUARDIAN_ROLE_CODES,
}
"""
Группы ролей для административных страниц пользователей.

Используется для страниц:
    - /admin/users/students;
    - /admin/users/teachers;
    - /admin/users/parents.
"""


def is_authenticated_active_admin_actor(*, actor) -> bool:
    """
    Проверяет, что пользователь авторизован и активен.

    Args:
        actor:
            Пользователь, который выполняет административное действие.

    Returns:
        bool: True, если пользователь авторизован и активен.
    """

    return bool(actor and actor.is_authenticated and actor.is_active)


def is_superadmin_actor(*, actor) -> bool:
    """
    Проверяет, является ли пользователь суперадминистратором.

    Args:
        actor:
            Пользователь, который выполняет действие.

    Returns:
        bool: True, если пользователь является суперадминистратором.
    """

    return bool(
        is_authenticated_active_admin_actor(actor=actor)
        and (
            actor.is_superuser
            or UserRole.objects.filter(
                user=actor,
                status=UserRoleStatus.ACTIVE,
                role__code__in=PLATFORM_ADMIN_ROLE_CODES,
            ).exists()
        )
    )


def get_admin_user_roles_prefetch_queryset() -> QuerySet:
    """
    Возвращает QuerySet ролей пользователя для prefetch_related.

    Роли заранее подгружаются вместе с ролью, организацией, отделением и группой,
    чтобы административный список пользователей не создавал N+1-запросы.

    Returns:
        QuerySet: QuerySet назначенных ролей пользователей.
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


def get_admin_users_base_queryset() -> QuerySet:
    """
    Возвращает базовый QuerySet пользователей для административного раздела.

    Важно:
        Этот QuerySet ещё не проверяет права текущего администратора.
        Для endpoint'ов админки нужно использовать
        get_admin_users_queryset_for_actor().

    Returns:
        QuerySet: Базовый QuerySet пользователей.
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
                queryset=get_admin_user_roles_prefetch_queryset(),
            ),
        )
        .order_by(
            "last_name",
            "first_name",
            "email",
        )
    )


def get_actor_admin_roles_queryset(*, actor) -> QuerySet:
    """
    Возвращает активные административные роли текущего пользователя.

    Args:
        actor:
            Пользователь, который выполняет административное действие.

    Returns:
        QuerySet: Активные административные роли пользователя.
    """

    if not is_authenticated_active_admin_actor(actor=actor):
        return UserRole.objects.none()

    return get_admin_user_roles_prefetch_queryset().filter(
        user=actor,
        status=UserRoleStatus.ACTIVE,
        role__code__in=ORGANIZATION_ADMIN_ROLE_CODES,
    )


def is_organization_admin_actor(*, actor) -> bool:
    """
    Проверяет, есть ли у пользователя административная роль организации.

    Args:
        actor:
            Пользователь, который выполняет действие.

    Returns:
        bool: True, если пользователь имеет административную роль организации.
    """

    return get_actor_admin_roles_queryset(actor=actor).exists()


def build_admin_users_scope_query_for_actor(*, actor) -> Q:
    """
    Строит Q-условие области видимости пользователей для администратора.

    Правила:
        - директор и администратор организации видят пользователей своей организации;
        - заведующий отделением видит пользователей только своего отделения;
        - суперадминистратор обрабатывается выше и в этот метод обычно не попадает.

    Args:
        actor:
            Пользователь, который выполняет административное действие.

    Returns:
        Q: Условие для ограничения QuerySet.
    """

    scope_query = Q(pk__in=[])

    for user_role in get_actor_admin_roles_queryset(actor=actor):
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


def get_admin_users_queryset_for_actor(*, actor) -> QuerySet:
    """
    Возвращает пользователей, доступных администратору.

    Правила:
        - суперадминистратор видит всех пользователей;
        - администратор организации видит пользователей своей организации;
        - директор видит пользователей своей организации;
        - заведующий отделением видит пользователей своего отделения;
        - обычный пользователь не видит административный список.

    Args:
        actor:
            Пользователь, который выполняет административное действие.

    Returns:
        QuerySet: Пользователи, доступные текущему администратору.
    """

    queryset = get_admin_users_base_queryset()

    if not is_authenticated_active_admin_actor(actor=actor):
        return User.objects.none()

    if is_superadmin_actor(actor=actor):
        return queryset

    if not is_organization_admin_actor(actor=actor):
        return User.objects.none()

    scope_query = build_admin_users_scope_query_for_actor(actor=actor)

    return queryset.filter(scope_query).distinct()


def filter_admin_users_by_role_group(
    *,
    queryset: QuerySet,
    role_group: str,
) -> QuerySet:
    """
    Фильтрует административный список пользователей по группе ролей.

    Args:
        queryset:
            Исходный QuerySet пользователей.
        role_group:
            Группа ролей: students, teachers или parents.

    Returns:
        QuerySet: Отфильтрованный QuerySet пользователей.
    """

    role_codes = ADMIN_USER_ROLE_GROUPS.get(role_group)

    if not role_codes:
        return queryset

    return queryset.filter(
        user_roles__status=UserRoleStatus.ACTIVE,
        user_roles__role__code__in=role_codes,
    ).distinct()


def get_admin_students_queryset_for_actor(*, actor) -> QuerySet:
    """
    Возвращает учащихся, доступных администратору.

    Args:
        actor:
            Пользователь, который выполняет административное действие.

    Returns:
        QuerySet: Доступные учащиеся.
    """

    return filter_admin_users_by_role_group(
        queryset=get_admin_users_queryset_for_actor(actor=actor),
        role_group="students",
    )


def get_admin_teachers_queryset_for_actor(*, actor) -> QuerySet:
    """
    Возвращает пользователей с преподавательскими и сотрудническими ролями.

    Args:
        actor:
            Пользователь, который выполняет административное действие.

    Returns:
        QuerySet: Доступные сотрудники и преподаватели.
    """

    return filter_admin_users_by_role_group(
        queryset=get_admin_users_queryset_for_actor(actor=actor),
        role_group="teachers",
    )


def get_admin_parents_queryset_for_actor(*, actor) -> QuerySet:
    """
    Возвращает родителей и законных представителей, доступных администратору.

    Args:
        actor:
            Пользователь, который выполняет административное действие.

    Returns:
        QuerySet: Доступные родители и законные представители.
    """

    return filter_admin_users_by_role_group(
        queryset=get_admin_users_queryset_for_actor(actor=actor),
        role_group="parents",
    )


def get_admin_user_detail_queryset_for_actor(*, actor) -> QuerySet:
    """
    Возвращает QuerySet для детальной карточки пользователя в админке.

    Args:
        actor:
            Пользователь, который открывает карточку.

    Returns:
        QuerySet: Доступные пользователи с подгруженными связями.
    """

    return get_admin_users_queryset_for_actor(actor=actor)


def get_admin_user_by_id_for_actor(*, actor, user_id: int):
    """
    Возвращает пользователя по ID с учётом прав администратора.

    Args:
        actor:
            Пользователь, который выполняет административное действие.
        user_id:
            ID целевого пользователя.

    Returns:
        User | None: Пользователь или None.
    """

    if not user_id:
        return None

    return (
        get_admin_user_detail_queryset_for_actor(actor=actor).filter(id=user_id).first()
    )


def actor_can_access_admin_user(*, actor, target_user) -> bool:
    """
    Проверяет, может ли администратор получить доступ к пользователю.

    Args:
        actor:
            Пользователь, который выполняет действие.
        target_user:
            Целевой пользователь.

    Returns:
        bool: True, если доступ разрешён.
    """

    if not actor or not target_user:
        return False

    if is_superadmin_actor(actor=actor):
        return True

    return (
        get_admin_users_queryset_for_actor(actor=actor)
        .filter(
            id=target_user.id,
        )
        .exists()
    )
