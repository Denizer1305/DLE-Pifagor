from __future__ import annotations

from apps.organizations.models import Organization
from apps.organizations.selectors.access_selectors import (
    get_actor_admin_organization_ids,
    is_authenticated_active_actor,
    is_superadmin_actor,
)
from apps.users.constants.lifecycle import ProfileStatus, UserRoleStatus
from django.db.models import QuerySet


def get_organizations_base_queryset() -> QuerySet:
    """
    Возвращает базовый QuerySet образовательных организаций.

    Returns:
        QuerySet: Организации.
    """

    return Organization.objects.all().order_by("name")


def get_active_organizations_queryset() -> QuerySet:
    """
    Возвращает активные образовательные организации.

    Returns:
        QuerySet: Активные организации.
    """

    return get_organizations_base_queryset().filter(
        is_active=True,
    )


def get_public_organizations_queryset() -> QuerySet:
    """
    Возвращает организации, доступные в публичной зоне.

    Returns:
        QuerySet: Публичные организации.
    """

    return get_active_organizations_queryset().filter(
        is_public=True,
    )


def get_default_public_organization() -> Organization | None:
    """
    Возвращает организацию по умолчанию для публичной зоны.

    Returns:
        Organization | None: Организация по умолчанию.
    """

    return get_public_organizations_queryset().filter(is_default_public=True).first()


def get_user_teacher_profile_organization(user) -> Organization | None:
    """
    Возвращает организацию из профиля преподавателя.

    Args:
        user:
            Пользователь.

    Returns:
        Organization | None: Организация преподавателя.
    """

    if not is_authenticated_active_actor(actor=user):
        return None

    teacher_profile = getattr(user, "teacher_profile", None)

    if not teacher_profile:
        return None

    if teacher_profile.status != ProfileStatus.VERIFIED:
        return None

    return teacher_profile.organization


def get_user_role_organization(user) -> Organization | None:
    """
    Возвращает первую организацию пользователя из активных ролей.

    Args:
        user:
            Пользователь.

    Returns:
        Organization | None: Организация из роли пользователя.
    """

    if not is_authenticated_active_actor(actor=user):
        return None

    user_role = (
        user.user_roles.select_related("organization")
        .filter(
            status=UserRoleStatus.ACTIVE,
            organization__isnull=False,
            organization__is_active=True,
        )
        .first()
    )

    if not user_role:
        return None

    return user_role.organization


def get_user_organization(user) -> Organization | None:
    """
    Возвращает основную организацию пользователя.

    Приоритет:
        1. TeacherProfile.organization;
        2. первая активная UserRole.organization.

    Args:
        user:
            Пользователь.

    Returns:
        Organization | None: Организация пользователя.
    """

    teacher_organization = get_user_teacher_profile_organization(user)

    if teacher_organization:
        return teacher_organization

    return get_user_role_organization(user)


def resolve_public_teachers_organization(user) -> Organization | None:
    """
    Определяет организацию для публичной страницы преподавателей.

    Для авторизованного пользователя используется его организация.
    Для анонимного пользователя используется организация по умолчанию.

    Args:
        user:
            Пользователь или None.

    Returns:
        Organization | None: Организация для публичной страницы.
    """

    user_organization = get_user_organization(user)

    if user_organization and user_organization.is_public:
        return user_organization

    return get_default_public_organization()


def get_admin_organizations_queryset_for_actor(*, actor) -> QuerySet:
    """
    Возвращает организации, доступные в административном разделе.

    Правила:
        - суперадминистратор видит все организации;
        - админ организации / директор видит свои организации;
        - остальные пользователи не видят список организаций.

    Args:
        actor:
            Пользователь, который выполняет административное действие.

    Returns:
        QuerySet: Доступные организации.
    """

    queryset = get_organizations_base_queryset()

    if not is_authenticated_active_actor(actor=actor):
        return Organization.objects.none()

    if is_superadmin_actor(actor=actor):
        return queryset

    organization_ids = get_actor_admin_organization_ids(actor=actor)

    if not organization_ids:
        return Organization.objects.none()

    return queryset.filter(id__in=organization_ids)
