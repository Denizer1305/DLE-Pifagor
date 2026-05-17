from __future__ import annotations

from apps.users.constants.onboarding import JoinRequestType
from apps.users.models import UserJoinRequest
from apps.users.services.join_requests.base_join_request_services import (
    create_join_request,
)


def create_guardian_join_request(
    *,
    guardian,
    learner,
    organization=None,
    department=None,
    group=None,
    message: str = "",
    request=None,
) -> UserJoinRequest:
    """
    Создаёт заявку родителя на связь с учащимся.

    Args:
        guardian:
            Родитель или законный представитель.
        learner:
            Учащийся.
        organization:
            Образовательная организация.
        department:
            Отделение.
        group:
            Учебная группа.
        message:
            Сообщение.
        request:
            HTTP-запрос.

    Returns:
        UserJoinRequest: Созданная заявка родителя.
    """

    return create_join_request(
        request_type=JoinRequestType.GUARDIAN_TO_LEARNER,
        user=guardian,
        target_user=learner,
        organization=organization,
        department=department,
        group=group,
        message=message,
        request=request,
    )
