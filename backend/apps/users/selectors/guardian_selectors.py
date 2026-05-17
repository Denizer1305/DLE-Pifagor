from __future__ import annotations

from apps.users.constants.lifecycle import GuardianLearnerStatus, ProfileStatus
from apps.users.models import GuardianLearner, GuardianProfile
from django.db.models import QuerySet


def get_guardian_profiles_queryset() -> QuerySet:
    """
    Возвращает базовый QuerySet профилей родителей.

    Returns:
        QuerySet: Профили родителей.
    """

    return GuardianProfile.objects.select_related("user")


def get_guardian_profile_by_user(user):
    """
    Возвращает профиль родителя по пользователю.

    Args:
        user:
            Пользователь.

    Returns:
        GuardianProfile | None: Профиль родителя или None.
    """

    if not user:
        return None

    return get_guardian_profiles_queryset().filter(user=user).first()


def get_verified_guardian_profiles_queryset() -> QuerySet:
    """
    Возвращает подтверждённые профили родителей.

    Returns:
        QuerySet: Подтверждённые профили родителей.
    """

    return get_guardian_profiles_queryset().filter(status=ProfileStatus.VERIFIED)


def get_guardian_learner_links_queryset() -> QuerySet:
    """
    Возвращает базовый QuerySet связей родителей и учащихся.

    Returns:
        QuerySet: Связи родителей и учащихся.
    """

    return GuardianLearner.objects.select_related(
        "guardian",
        "learner",
        "requested_by",
        "approved_by",
    )


def get_active_guardian_learner_links_queryset() -> QuerySet:
    """
    Возвращает активные связи родителей и учащихся.

    Returns:
        QuerySet: Активные связи.
    """

    return get_guardian_learner_links_queryset().filter(
        status=GuardianLearnerStatus.ACTIVE,
    )


def get_guardian_link(guardian, learner):
    """
    Возвращает связь конкретного родителя и учащегося.

    Args:
        guardian:
            Родитель или законный представитель.
        learner:
            Учащийся.

    Returns:
        GuardianLearner | None: Связь или None.
    """

    if not guardian or not learner:
        return None

    return (
        get_guardian_learner_links_queryset()
        .filter(
            guardian=guardian,
            learner=learner,
        )
        .first()
    )


def get_active_guardian_link(guardian, learner):
    """
    Возвращает активную связь конкретного родителя и учащегося.

    Args:
        guardian:
            Родитель или законный представитель.
        learner:
            Учащийся.

    Returns:
        GuardianLearner | None: Активная связь или None.
    """

    if not guardian or not learner:
        return None

    return (
        get_active_guardian_learner_links_queryset()
        .filter(
            guardian=guardian,
            learner=learner,
        )
        .first()
    )


def get_learners_for_guardian(guardian) -> QuerySet:
    """
    Возвращает учащихся, доступных родителю.

    Args:
        guardian:
            Родитель или законный представитель.

    Returns:
        QuerySet: Активные связи родителя с учащимися.
    """

    if not guardian:
        return GuardianLearner.objects.none()

    return get_active_guardian_learner_links_queryset().filter(guardian=guardian)


def get_guardians_for_learner(learner) -> QuerySet:
    """
    Возвращает родителей, связанных с учащимся.

    Args:
        learner:
            Учащийся.

    Returns:
        QuerySet: Активные связи учащегося с родителями.
    """

    if not learner:
        return GuardianLearner.objects.none()

    return get_active_guardian_learner_links_queryset().filter(learner=learner)


def guardian_has_access_to_learner(guardian, learner) -> bool:
    """
    Проверяет, есть ли у родителя доступ к данным учащегося.

    Args:
        guardian:
            Родитель или законный представитель.
        learner:
            Учащийся.

    Returns:
        bool: True, если активная связь существует.
    """

    return get_active_guardian_link(guardian, learner) is not None


def get_primary_guardian_for_learner(learner):
    """
    Возвращает основного представителя учащегося.

    Args:
        learner:
            Учащийся.

    Returns:
        GuardianLearner | None: Основная активная связь или None.
    """

    if not learner:
        return None

    return (
        get_active_guardian_learner_links_queryset()
        .filter(
            learner=learner,
            is_primary=True,
        )
        .first()
    )
