from __future__ import annotations

from apps.users.constants.onboarding import JoinRequestType
from apps.users.models import UserJoinRequest
from apps.users.services.join_requests.base_join_request_services import (
    create_join_request,
)


def create_learner_join_request(
    *,
    user,
    organization,
    department=None,
    group=None,
    message: str = "",
    request=None,
) -> UserJoinRequest:
    """
    Создаёт заявку учащегося в группу.

    Args:
        user:
            Пользователь учащегося.
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
        UserJoinRequest: Созданная заявка учащегося.
    """

    return create_join_request(
        request_type=JoinRequestType.LEARNER_TO_GROUP,
        user=user,
        organization=organization,
        department=department,
        group=group,
        message=message,
        request=request,
    )
