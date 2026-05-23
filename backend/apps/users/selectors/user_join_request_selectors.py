from __future__ import annotations

from apps.users.constants.onboarding import JoinRequestStatus, JoinRequestType
from apps.users.models import UserJoinRequest
from django.db.models import QuerySet


def get_join_requests_queryset() -> QuerySet:
    """
    Возвращает базовый QuerySet заявок пользователей.

    Returns:
        QuerySet: Заявки пользователей.
    """

    return UserJoinRequest.objects.select_related(
        "user",
        "target_user",
        "organization",
        "department",
        "group",
        "reviewed_by",
    )


def get_pending_join_requests_queryset() -> QuerySet:
    """
    Возвращает заявки, ожидающие проверки.

    Returns:
        QuerySet: Ожидающие заявки.
    """

    return get_join_requests_queryset().filter(status=JoinRequestStatus.PENDING)


def get_join_request_by_id(request_id: int):
    """
    Возвращает заявку по ID.

    Args:
        request_id:
            ID заявки.

    Returns:
        UserJoinRequest | None: Заявка или None.
    """

    if not request_id:
        return None

    return get_join_requests_queryset().filter(id=request_id).first()


def get_user_pending_join_requests(user) -> QuerySet:
    """
    Возвращает ожидающие заявки пользователя.

    Args:
        user:
            Пользователь.

    Returns:
        QuerySet: Ожидающие заявки пользователя.
    """

    if not user:
        return UserJoinRequest.objects.none()

    return get_pending_join_requests_queryset().filter(user=user)


def get_pending_teacher_requests_for_organization(organization) -> QuerySet:
    """
    Возвращает ожидающие заявки преподавателей в организацию.

    Args:
        organization:
            Образовательная организация.

    Returns:
        QuerySet: Заявки преподавателей.
    """

    if not organization:
        return UserJoinRequest.objects.none()

    return get_pending_join_requests_queryset().filter(
        organization=organization,
        request_type=JoinRequestType.TEACHER_TO_ORGANIZATION,
    )


def get_pending_learner_requests_for_group(group) -> QuerySet:
    """
    Возвращает ожидающие заявки учащихся в группу.

    Args:
        group:
            Учебная группа.

    Returns:
        QuerySet: Заявки учащихся.
    """

    if not group:
        return UserJoinRequest.objects.none()

    return get_pending_join_requests_queryset().filter(
        group=group,
        request_type=JoinRequestType.LEARNER_TO_GROUP,
    )


def get_pending_guardian_requests_for_learner(learner) -> QuerySet:
    """
    Возвращает ожидающие заявки родителей к учащемуся.

    Args:
        learner:
            Учащийся.

    Returns:
        QuerySet: Заявки родителей.
    """

    if not learner:
        return UserJoinRequest.objects.none()

    return get_pending_join_requests_queryset().filter(
        target_user=learner,
        request_type=JoinRequestType.GUARDIAN_TO_LEARNER,
    )


def get_pending_join_requests_for_reviewer(
    *,
    organization=None,
    department=None,
    group=None,
) -> QuerySet:
    """
    Возвращает ожидающие заявки в контексте проверяющего.

    Args:
        organization:
            Образовательная организация.
        department:
            Отделение.
        group:
            Учебная группа.

    Returns:
        QuerySet: Ожидающие заявки.
    """

    queryset = get_pending_join_requests_queryset()

    if organization is not None:
        queryset = queryset.filter(organization=organization)

    if department is not None:
        queryset = queryset.filter(department=department)

    if group is not None:
        queryset = queryset.filter(group=group)

    return queryset


def user_has_pending_join_request(
    *,
    user,
    request_type: str,
    organization=None,
    department=None,
    group=None,
    target_user=None,
) -> bool:
    """
    Проверяет, есть ли у пользователя ожидающая заявка.

    Args:
        user:
            Пользователь.
        request_type:
            Тип заявки.
        organization:
            Образовательная организация.
        department:
            Отделение.
        group:
            Учебная группа.
        target_user:
            Целевой пользователь.

    Returns:
        bool: True, если ожидающая заявка уже существует.
    """

    if not user or not request_type:
        return False

    queryset = get_pending_join_requests_queryset().filter(
        user=user,
        request_type=request_type,
    )

    if organization is not None:
        queryset = queryset.filter(organization=organization)

    if department is not None:
        queryset = queryset.filter(department=department)

    if group is not None:
        queryset = queryset.filter(group=group)

    if target_user is not None:
        queryset = queryset.filter(target_user=target_user)

    return queryset.exists()
