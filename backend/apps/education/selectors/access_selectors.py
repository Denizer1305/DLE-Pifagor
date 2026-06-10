from __future__ import annotations

from collections.abc import Iterable

from apps.education.constants import (
    GLOBAL_ADMIN_ROLE_CODES,
    LEARNER_ROLE_CODES,
    ORGANIZATION_ADMIN_ROLE_CODES,
    TEACHER_ROLE_CODES,
)
from apps.education.models import LearnerGroupEnrollment
from apps.organizations.models import Organization, StudyGroup
from django.contrib.auth import get_user_model
from django.db.models import QuerySet

User = get_user_model()


def user_is_authenticated(user: User | None) -> bool:
    """
    Проверяет, что пользователь авторизован.
    """

    return bool(user and user.is_authenticated)


def get_user_role_codes(user: User) -> set[str]:
    """
    Возвращает коды активных ролей пользователя.

    Функция написана устойчиво к разным вариантам related_name,
    потому что users уже развивался отдельно и не должен ломать
    селекторы education при изменении внутренней реализации ролей.
    """

    if not user_is_authenticated(user):
        return set()

    role_codes: set[str] = set()

    direct_role = getattr(user, "role", None)
    direct_role_code = getattr(direct_role, "code", None)

    if direct_role_code:
        role_codes.add(str(direct_role_code))

    for relation_name in (
        "roles",
        "user_roles",
        "role_assignments",
    ):
        relation = getattr(user, relation_name, None)

        if relation is None:
            continue

        try:
            role_items = relation.all()
        except TypeError:
            continue

        for role_item in role_items:
            status = getattr(role_item, "status", "active")

            if status != "active":
                continue

            code = getattr(role_item, "code", None)
            role = getattr(role_item, "role", None)

            if code:
                role_codes.add(str(code))
                continue

            role_code = getattr(role, "code", None)

            if role_code:
                role_codes.add(str(role_code))

    return role_codes


def user_has_any_role(user: User, role_codes: Iterable[str]) -> bool:
    """
    Проверяет наличие хотя бы одной роли из списка.
    """

    return bool(get_user_role_codes(user).intersection(set(role_codes)))


def user_is_global_admin(user: User) -> bool:
    """
    Проверяет, имеет ли пользователь глобальный административный доступ.
    """

    return user_has_any_role(user, GLOBAL_ADMIN_ROLE_CODES)


def user_is_organization_admin(user: User) -> bool:
    """
    Проверяет, имеет ли пользователь административный доступ
    на уровне организации или отделения.
    """

    return user_has_any_role(user, ORGANIZATION_ADMIN_ROLE_CODES)


def user_is_teacher(user: User) -> bool:
    """
    Проверяет роль преподавателя.
    """

    return user_has_any_role(user, TEACHER_ROLE_CODES)


def user_is_learner(user: User) -> bool:
    """
    Проверяет роль обучающегося.
    """

    return user_has_any_role(user, LEARNER_ROLE_CODES)


def get_user_profile_organization_ids(user: User) -> set[int]:
    """
    Возвращает организации из профильных связей пользователя,
    если такие поля есть в текущей реализации users.
    """

    organization_ids: set[int] = set()

    for profile_name in (
        "profile",
        "admin_profile",
        "teacher_profile",
        "learner_profile",
        "guardian_profile",
    ):
        profile = getattr(user, profile_name, None)

        if profile is None:
            continue

        organization_id = getattr(profile, "organization_id", None)

        if organization_id:
            organization_ids.add(organization_id)

    return organization_ids


def get_user_teacher_organization_ids(user: User) -> set[int]:
    """
    Возвращает организации, где пользователь активен как преподаватель.
    """

    relation = getattr(user, "teacher_organizations", None)

    if relation is None:
        return set()

    return set(
        relation.filter(is_active=True).values_list(
            "organization_id",
            flat=True,
        )
    )


def get_user_learner_organization_ids(user: User) -> set[int]:
    """
    Возвращает организации через активные академические зачисления.
    """

    return set(
        LearnerGroupEnrollment.objects.filter(
            learner=user,
            status=LearnerGroupEnrollment.StatusChoices.ACTIVE,
        ).values_list(
            "group__organization_id",
            flat=True,
        )
    )


def get_user_available_organization_ids(user: User) -> set[int]:
    """
    Возвращает организации, доступные пользователю в education.
    """

    if not user_is_authenticated(user):
        return set()

    if user_is_global_admin(user):
        return set(Organization.objects.values_list("id", flat=True))

    organization_ids = set()

    organization_ids.update(get_user_profile_organization_ids(user))
    organization_ids.update(get_user_teacher_organization_ids(user))
    organization_ids.update(get_user_learner_organization_ids(user))

    return organization_ids


def get_user_available_group_ids(user: User) -> set[int]:
    """
    Возвращает учебные группы, доступные пользователю.
    """

    if not user_is_authenticated(user):
        return set()

    if user_is_global_admin(user):
        return set(StudyGroup.objects.values_list("id", flat=True))

    organization_ids = get_user_available_organization_ids(user)

    group_ids = set(
        StudyGroup.objects.filter(
            organization_id__in=organization_ids,
        ).values_list("id", flat=True)
    )

    learner_group_ids = set(
        LearnerGroupEnrollment.objects.filter(
            learner=user,
            status=LearnerGroupEnrollment.StatusChoices.ACTIVE,
        ).values_list("group_id", flat=True)
    )

    group_ids.update(learner_group_ids)

    return group_ids


def limit_queryset_by_user_organizations(
    queryset: QuerySet,
    user: User,
    organization_field: str = "organization_id",
) -> QuerySet:
    """
    Ограничивает queryset организациями пользователя.
    """

    if user_is_global_admin(user):
        return queryset

    organization_ids = get_user_available_organization_ids(user)

    return queryset.filter(**{f"{organization_field}__in": organization_ids})


def limit_queryset_by_user_groups(
    queryset: QuerySet,
    user: User,
    group_field: str = "group_id",
) -> QuerySet:
    """
    Ограничивает queryset учебными группами пользователя.
    """

    if user_is_global_admin(user):
        return queryset

    group_ids = get_user_available_group_ids(user)

    return queryset.filter(**{f"{group_field}__in": group_ids})
