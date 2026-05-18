from __future__ import annotations

from apps.organizations.models import Organization
from django.contrib.auth.models import AnonymousUser
from django.db.models import QuerySet


def get_public_organizations_queryset() -> QuerySet[Organization]:
    """
    Возвращает публичные активные образовательные организации.

    Returns:
        QuerySet[Organization]: QuerySet организаций.
    """

    return Organization.objects.filter(
        is_active=True,
        is_public=True,
    ).order_by("name")


def get_default_public_organization() -> Organization | None:
    """
    Возвращает системную организацию по умолчанию для публичной зоны.

    Returns:
        Organization | None: Организация по умолчанию.
    """

    return (
        Organization.objects.filter(
            is_active=True,
            is_public=True,
            is_default_public=True,
        )
        .order_by("name")
        .first()
    )


def get_user_organization(user) -> Organization | None:
    """
    Определяет образовательную организацию пользователя.

    Приоритет:
        1. teacher_profile.organization;
        2. learner_profile.organization;
        3. user_roles.organization;
        4. организация учащегося для родителя;
        5. None.

    Args:
        user:
            Пользователь.

    Returns:
        Organization | None: Организация пользователя.
    """

    if not user or isinstance(user, AnonymousUser) or not user.is_authenticated:
        return None

    teacher_profile = getattr(user, "teacher_profile", None)

    if teacher_profile and teacher_profile.organization_id:
        return teacher_profile.organization

    learner_profile = getattr(user, "learner_profile", None)

    if learner_profile and learner_profile.organization_id:
        return learner_profile.organization

    user_role = (
        user.user_roles.filter(
            organization__isnull=False,
            organization__is_active=True,
        )
        .select_related("organization")
        .order_by("-created_at")
        .first()
    )

    if user_role and user_role.organization_id:
        return user_role.organization

    guardian_link = (
        user.guardian_learner_links.filter(
            learner__learner_profile__organization__isnull=False,
            learner__learner_profile__organization__is_active=True,
        )
        .select_related("learner__learner_profile__organization")
        .order_by("-is_primary", "-created_at")
        .first()
    )

    if guardian_link:
        return guardian_link.learner.learner_profile.organization

    return None


def resolve_public_teachers_organization(user) -> Organization | None:
    """
    Возвращает организацию для публичной страницы преподавателей.

    Для авторизованного пользователя используется его организация.
    Для гостя используется организация по умолчанию.

    Args:
        user:
            Пользователь.

    Returns:
        Organization | None: Организация.
    """

    user_organization = get_user_organization(user)

    if user_organization and user_organization.is_active:
        return user_organization

    return get_default_public_organization()
