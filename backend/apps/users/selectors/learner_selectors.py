from __future__ import annotations

from apps.users.constants.lifecycle import ProfileStatus
from apps.users.models import LearnerProfile
from django.db.models import QuerySet


def get_learner_profiles_queryset() -> QuerySet:
    """
    Возвращает базовый QuerySet профилей учащихся.

    Returns:
        QuerySet: Профили учащихся.
    """

    return LearnerProfile.objects.select_related(
        "user",
        "organization",
        "department",
        "group",
        "curator",
        "created_by_guardian",
        "verified_by",
    )


def get_learner_profile_by_user(user):
    """
    Возвращает профиль учащегося по пользователю.

    Args:
        user:
            Пользователь.

    Returns:
        LearnerProfile | None: Профиль учащегося или None.
    """

    if not user:
        return None

    return get_learner_profiles_queryset().filter(user=user).first()


def get_learner_profile_by_id(profile_id: int):
    """
    Возвращает профиль учащегося по ID.

    Args:
        profile_id:
            ID профиля учащегося.

    Returns:
        LearnerProfile | None: Профиль учащегося или None.
    """

    if not profile_id:
        return None

    return get_learner_profiles_queryset().filter(id=profile_id).first()


def get_verified_learner_profiles_queryset() -> QuerySet:
    """
    Возвращает подтверждённые профили учащихся.

    Returns:
        QuerySet: Подтверждённые профили учащихся.
    """

    return get_learner_profiles_queryset().filter(status=ProfileStatus.VERIFIED)


def get_pending_learner_profiles_queryset() -> QuerySet:
    """
    Возвращает профили учащихся, ожидающие проверки.

    Returns:
        QuerySet: Профили учащихся на проверке.
    """

    return get_learner_profiles_queryset().filter(status=ProfileStatus.PENDING_REVIEW)


def get_learners_by_organization(organization) -> QuerySet:
    """
    Возвращает учащихся образовательной организации.

    Args:
        organization:
            Образовательная организация.

    Returns:
        QuerySet: Профили учащихся организации.
    """

    if not organization:
        return LearnerProfile.objects.none()

    return get_learner_profiles_queryset().filter(organization=organization)


def get_learners_by_department(department) -> QuerySet:
    """
    Возвращает учащихся отделения.

    Args:
        department:
            Отделение.

    Returns:
        QuerySet: Профили учащихся отделения.
    """

    if not department:
        return LearnerProfile.objects.none()

    return get_learner_profiles_queryset().filter(department=department)


def get_learners_by_group(group) -> QuerySet:
    """
    Возвращает учащихся группы.

    Args:
        group:
            Учебная группа.

    Returns:
        QuerySet: Профили учащихся группы.
    """

    if not group:
        return LearnerProfile.objects.none()

    return get_learner_profiles_queryset().filter(group=group)


def get_learners_by_curator(curator) -> QuerySet:
    """
    Возвращает учащихся, закреплённых за куратором.

    Args:
        curator:
            Куратор.

    Returns:
        QuerySet: Профили учащихся куратора.
    """

    if not curator:
        return LearnerProfile.objects.none()

    return get_learner_profiles_queryset().filter(curator=curator)


def get_minor_learners_created_by_guardian(guardian) -> QuerySet:
    """
    Возвращает несовершеннолетних учащихся, созданных родителем.

    Args:
        guardian:
            Родитель или законный представитель.

    Returns:
        QuerySet: Профили учащихся младше 14 лет.
    """

    if not guardian:
        return LearnerProfile.objects.none()

    return get_learner_profiles_queryset().filter(
        created_by_guardian=guardian,
        is_minor=True,
    )
