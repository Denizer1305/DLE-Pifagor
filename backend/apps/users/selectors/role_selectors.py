from __future__ import annotations

from apps.users.constants.lifecycle import UserRoleStatus
from apps.users.constants.roles import (
    GUARDIAN_REVIEWER_ROLE_CODES,
    LEARNER_REVIEWER_ROLE_CODES,
    ORGANIZATION_REVIEWER_ROLE_CODES,
    TEACHER_REVIEWER_ROLE_CODES,
    RoleCode,
)
from apps.users.models import Role, UserRole
from django.db.models import QuerySet


def get_roles_queryset() -> QuerySet:
    """
    Возвращает базовый QuerySet ролей.

    Returns:
        QuerySet: Роли.
    """

    return Role.objects.all()


def get_active_roles_queryset() -> QuerySet:
    """
    Возвращает активные роли.

    Returns:
        QuerySet: Активные роли.
    """

    return get_roles_queryset().filter(is_active=True)


def get_role_by_code(code: str):
    """
    Возвращает роль по коду.

    Args:
        code:
            Код роли.

    Returns:
        Role | None: Роль или None.
    """

    if not code:
        return None

    return get_roles_queryset().filter(code=code).first()


def get_user_roles_queryset() -> QuerySet:
    """
    Возвращает базовый QuerySet назначенных ролей пользователей.

    Returns:
        QuerySet: Назначенные роли пользователей.
    """

    return UserRole.objects.select_related(
        "user",
        "role",
        "organization",
        "department",
        "group",
    )


def get_active_user_roles_queryset() -> QuerySet:
    """
    Возвращает активные назначенные роли.

    Returns:
        QuerySet: Активные роли пользователей.
    """

    return get_user_roles_queryset().filter(status=UserRoleStatus.ACTIVE)


def get_user_active_roles(user) -> QuerySet:
    """
    Возвращает активные роли конкретного пользователя.

    Args:
        user:
            Пользователь.

    Returns:
        QuerySet: Активные роли пользователя.
    """

    if not user:
        return UserRole.objects.none()

    return get_active_user_roles_queryset().filter(user=user)


def get_user_active_role_codes(user) -> set[str]:
    """
    Возвращает коды активных ролей пользователя.

    Args:
        user:
            Пользователь.

    Returns:
        set[str]: Множество кодов активных ролей.
    """

    return set(
        get_user_active_roles(user).values_list(
            "role__code",
            flat=True,
        )
    )


def user_has_active_role(
    *,
    user,
    role_code: str,
    organization=None,
    department=None,
    group=None,
) -> bool:
    """
    Проверяет, есть ли у пользователя активная роль в заданном контексте.

    Args:
        user:
            Пользователь.
        role_code:
            Код роли.
        organization:
            Образовательная организация.
        department:
            Отделение.
        group:
            Группа.

    Returns:
        bool: True, если активная роль найдена.
    """

    if not user or not role_code:
        return False

    queryset = get_active_user_roles_queryset().filter(
        user=user,
        role__code=role_code,
    )

    if organization is not None:
        queryset = queryset.filter(organization=organization)

    if department is not None:
        queryset = queryset.filter(department=department)

    if group is not None:
        queryset = queryset.filter(group=group)

    return queryset.exists()


def user_is_superadmin(user) -> bool:
    """
    Проверяет, является ли пользователь суперадминистратором платформы.

    Args:
        user:
            Пользователь.

    Returns:
        bool: True, если у пользователя есть роль superadmin.
    """

    return user_has_active_role(
        user=user,
        role_code=RoleCode.SUPERADMIN,
    )


def get_organization_reviewers(organization) -> QuerySet:
    """
    Возвращает пользователей, которые могут рассматривать заявки организации.

    Args:
        organization:
            Образовательная организация.

    Returns:
        QuerySet: Активные роли проверяющих.
    """

    if not organization:
        return UserRole.objects.none()

    return get_active_user_roles_queryset().filter(
        organization=organization,
        role__code__in=ORGANIZATION_REVIEWER_ROLE_CODES,
    )


def get_teacher_reviewers(organization, department=None) -> QuerySet:
    """
    Возвращает проверяющих для заявки преподавателя.

    Проверяющими могут быть:
        - директор;
        - администратор организации;
        - заведующий отделением.

    Args:
        organization:
            Образовательная организация.
        department:
            Отделение.

    Returns:
        QuerySet: Активные роли проверяющих.
    """

    if not organization:
        return UserRole.objects.none()

    queryset = get_active_user_roles_queryset().filter(
        organization=organization,
        role__code__in=TEACHER_REVIEWER_ROLE_CODES,
    )

    if department is not None:
        queryset = queryset.filter(
            department__isnull=True,
        ) | queryset.filter(
            department=department,
        )

    return queryset.distinct()


def get_learner_reviewers(organization, group=None, department=None) -> QuerySet:
    """
    Возвращает проверяющих для заявки учащегося.

    Проверяющими могут быть:
        - куратор;
        - заведующий отделением;
        - администратор организации.

    Args:
        organization:
            Образовательная организация.
        group:
            Учебная группа.
        department:
            Отделение.

    Returns:
        QuerySet: Активные роли проверяющих.
    """

    if not organization:
        return UserRole.objects.none()

    queryset = get_active_user_roles_queryset().filter(
        organization=organization,
        role__code__in=LEARNER_REVIEWER_ROLE_CODES,
    )

    if group is not None:
        queryset = queryset.filter(group__isnull=True) | queryset.filter(group=group)

    if department is not None:
        queryset = queryset.filter(department__isnull=True) | queryset.filter(
            department=department
        )

    return queryset.distinct()


def get_guardian_reviewers(organization, group=None, department=None) -> QuerySet:
    """
    Возвращает проверяющих для связи родителя и учащегося.

    Проверяющими могут быть:
        - куратор;
        - заведующий отделением;
        - администратор организации.

    Args:
        organization:
            Образовательная организация.
        group:
            Учебная группа.
        department:
            Отделение.

    Returns:
        QuerySet: Активные роли проверяющих.
    """

    if not organization:
        return UserRole.objects.none()

    queryset = get_active_user_roles_queryset().filter(
        organization=organization,
        role__code__in=GUARDIAN_REVIEWER_ROLE_CODES,
    )

    if group is not None:
        queryset = queryset.filter(group__isnull=True) | queryset.filter(group=group)

    if department is not None:
        queryset = queryset.filter(department__isnull=True) | queryset.filter(
            department=department
        )

    return queryset.distinct()
