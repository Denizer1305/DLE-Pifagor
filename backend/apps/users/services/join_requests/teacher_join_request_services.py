from __future__ import annotations

from apps.users.constants.onboarding import JoinRequestType
from apps.users.models import UserJoinRequest
from apps.users.services.join_requests.base_join_request_services import (
    create_join_request,
)


def create_teacher_join_request(
    *,
    user,
    organization,
    department=None,
    message: str = "",
    request=None,
) -> UserJoinRequest:
    """
    Создаёт заявку преподавателя в образовательную организацию.

    Args:
        user:
            Пользователь преподавателя.
        organization:
            Образовательная организация.
        department:
            Отделение.
        message:
            Сообщение.
        request:
            HTTP-запрос.

    Returns:
        UserJoinRequest: Созданная заявка преподавателя.
    """

    return create_join_request(
        request_type=JoinRequestType.TEACHER_TO_ORGANIZATION,
        user=user,
        organization=organization,
        department=department,
        message=message,
        request=request,
    )
