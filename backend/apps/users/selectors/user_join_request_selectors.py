from __future__ import annotations

from apps.organizations.selectors.access_selectors import (
    get_actor_admin_department_ids,
    get_actor_admin_organization_ids,
    get_actor_group_ids,
    is_authenticated_active_actor,
    is_superadmin_actor,
)
from apps.users.constants.onboarding import JoinRequestStatus, JoinRequestType
from apps.users.models import UserJoinRequest
from django.db.models import Q, QuerySet


def get_join_requests_queryset() -> QuerySet:
    """
    Возвращает базовый QuerySet заявок пользователей.

    Returns:
        QuerySet: Заявки пользователей.
    """

    return (
        UserJoinRequest.objects.select_related(
            "user",
            "target_user",
            "organization",
            "department",
            "group",
            "reviewed_by",
        )
        .all()
        .order_by("-created_at")
    )


def get_pending_join_requests_queryset() -> QuerySet:
    """
    Возвращает заявки, ожидающие проверки.

    Returns:
        QuerySet: Ожидающие заявки.
    """

    return get_join_requests_queryset().filter(
        status=JoinRequestStatus.PENDING,
    )


def get_join_request_by_id(request_id: int | None) -> UserJoinRequest | None:
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

    return (
        get_join_requests_queryset()
        .filter(
            id=request_id,
        )
        .first()
    )


def get_user_join_requests_queryset(*, user) -> QuerySet:
    """
    Возвращает заявки, связанные с пользователем.

    Пользователь может быть:
        - автором заявки;
        - целевым пользователем заявки, например учащимся
          в заявке родителя на связь.

    Args:
        user:
            Пользователь.

    Returns:
        QuerySet: Заявки пользователя.
    """

    if not user:
        return UserJoinRequest.objects.none()

    return (
        get_join_requests_queryset()
        .filter(
            Q(user=user) | Q(target_user=user),
        )
        .distinct()
    )


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

    return (
        get_pending_join_requests_queryset()
        .filter(
            Q(user=user) | Q(target_user=user),
        )
        .distinct()
    )


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

    Этот selector оставлен для обратной совместимости старых сервисов.
    Для API админки лучше использовать get_reviewable_join_requests_queryset_for_actor().

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
        queryset = queryset.filter(
            organization=organization,
        )

    if department is not None:
        queryset = queryset.filter(
            department=department,
        )

    if group is not None:
        queryset = queryset.filter(
            group=group,
        )

    return queryset


def get_reviewer_scope_query_for_actor(*, actor) -> Q:
    """
    Возвращает Q-условие области проверки заявок для пользователя.

    Правила:
        - админ организации / директор видит заявки своей организации;
        - заведующий отделением видит заявки своего отделения;
        - куратор видит заявки своей группы;
        - обычный пользователь не получает reviewer scope.

    Args:
        actor:
            Пользователь-проверяющий.

    Returns:
        Q: Условие области проверки.
    """

    organization_ids = get_actor_admin_organization_ids(actor=actor)
    department_ids = get_actor_admin_department_ids(actor=actor)
    group_ids = get_actor_group_ids(actor=actor)

    scope_query = Q()

    if organization_ids:
        scope_query |= Q(organization_id__in=organization_ids)

    if department_ids:
        scope_query |= Q(department_id__in=department_ids)
        scope_query |= Q(group__department_id__in=department_ids)

    if group_ids:
        scope_query |= Q(group_id__in=group_ids)

    return scope_query


def get_reviewable_join_requests_queryset_for_actor(*, actor) -> QuerySet:
    """
    Возвращает заявки, которые пользователь может рассматривать.

    Args:
        actor:
            Проверяющий пользователь.

    Returns:
        QuerySet: Заявки, доступные для рассмотрения.
    """

    if not is_authenticated_active_actor(actor=actor):
        return UserJoinRequest.objects.none()

    if is_superadmin_actor(actor=actor):
        return get_join_requests_queryset()

    scope_query = get_reviewer_scope_query_for_actor(actor=actor)

    if not scope_query:
        return UserJoinRequest.objects.none()

    return get_join_requests_queryset().filter(scope_query).distinct()


def get_pending_reviewable_join_requests_queryset_for_actor(*, actor) -> QuerySet:
    """
    Возвращает ожидающие заявки, которые пользователь может рассматривать.

    Args:
        actor:
            Проверяющий пользователь.

    Returns:
        QuerySet: Ожидающие заявки, доступные для рассмотрения.
    """

    return get_reviewable_join_requests_queryset_for_actor(actor=actor).filter(
        status=JoinRequestStatus.PENDING,
    )


def get_join_requests_queryset_for_actor(*, actor) -> QuerySet:
    """
    Возвращает заявки, доступные пользователю.

    Правила:
        - суперадминистратор видит все заявки;
        - проверяющий видит входящие заявки в своей области;
        - пользователь видит собственные заявки;
        - целевой пользователь видит заявки, связанные с ним.

    Args:
        actor:
            Текущий пользователь.

    Returns:
        QuerySet: Доступные заявки.
    """

    if not is_authenticated_active_actor(actor=actor):
        return UserJoinRequest.objects.none()

    if is_superadmin_actor(actor=actor):
        return get_join_requests_queryset()

    own_query = Q(user=actor) | Q(target_user=actor)
    scope_query = get_reviewer_scope_query_for_actor(actor=actor)

    access_query = own_query

    if scope_query:
        access_query |= scope_query

    return get_join_requests_queryset().filter(access_query).distinct()


def get_pending_join_requests_queryset_for_actor(*, actor) -> QuerySet:
    """
    Возвращает ожидающие заявки, доступные пользователю.

    Args:
        actor:
            Текущий пользователь.

    Returns:
        QuerySet: Доступные ожидающие заявки.
    """

    return get_join_requests_queryset_for_actor(actor=actor).filter(
        status=JoinRequestStatus.PENDING,
    )


def get_join_request_by_id_for_actor(
    *,
    actor,
    request_id: int | None,
) -> UserJoinRequest | None:
    """
    Возвращает заявку по ID с учётом доступа пользователя.

    Args:
        actor:
            Текущий пользователь.
        request_id:
            ID заявки.

    Returns:
        UserJoinRequest | None: Заявка или None.
    """

    if not request_id:
        return None

    return (
        get_join_requests_queryset_for_actor(actor=actor)
        .filter(
            id=request_id,
        )
        .first()
    )


def get_reviewable_join_request_by_id_for_actor(
    *,
    actor,
    request_id: int | None,
) -> UserJoinRequest | None:
    """
    Возвращает заявку по ID, если пользователь может её рассматривать.

    Args:
        actor:
            Проверяющий пользователь.
        request_id:
            ID заявки.

    Returns:
        UserJoinRequest | None: Заявка или None.
    """

    if not request_id:
        return None

    return (
        get_reviewable_join_requests_queryset_for_actor(actor=actor)
        .filter(
            id=request_id,
        )
        .first()
    )


def actor_can_access_join_request(
    *,
    actor,
    join_request: UserJoinRequest | None,
) -> bool:
    """
    Проверяет, может ли пользователь видеть заявку.

    Args:
        actor:
            Текущий пользователь.
        join_request:
            Заявка.

    Returns:
        bool: True, если заявка доступна.
    """

    if join_request is None:
        return False

    if is_superadmin_actor(actor=actor):
        return True

    return (
        get_join_requests_queryset_for_actor(actor=actor)
        .filter(
            id=join_request.id,
        )
        .exists()
    )


def actor_can_review_join_request(
    *,
    actor,
    join_request: UserJoinRequest | None,
) -> bool:
    """
    Проверяет, может ли пользователь рассмотреть заявку.

    Важно:
        Пользователь не должен подтверждать собственную заявку,
        кроме суперадминистратора.

    Args:
        actor:
            Проверяющий пользователь.
        join_request:
            Заявка.

    Returns:
        bool: True, если пользователь может рассмотреть заявку.
    """

    if join_request is None:
        return False

    if not is_authenticated_active_actor(actor=actor):
        return False

    if is_superadmin_actor(actor=actor):
        return True

    if join_request.user_id == getattr(actor, "id", None):
        return False

    return (
        get_reviewable_join_requests_queryset_for_actor(actor=actor)
        .filter(
            id=join_request.id,
        )
        .exists()
    )


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
        queryset = queryset.filter(
            organization=organization,
        )

    if department is not None:
        queryset = queryset.filter(
            department=department,
        )

    if group is not None:
        queryset = queryset.filter(
            group=group,
        )

    if target_user is not None:
        queryset = queryset.filter(
            target_user=target_user,
        )

    return queryset.exists()
