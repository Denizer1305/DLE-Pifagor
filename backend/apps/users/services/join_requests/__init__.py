"""
Сервисы заявок пользователей.

Пакет содержит создание и обработку заявок:
    - преподавателя в организацию;
    - учащегося в группу;
    - родителя к учащемуся.
"""

from apps.users.services.join_requests.base_join_request_services import (
    create_join_request,
)
from apps.users.services.join_requests.guardian_join_request_services import (
    create_guardian_join_request,
)
from apps.users.services.join_requests.learner_join_request_services import (
    create_learner_join_request,
)
from apps.users.services.join_requests.review_join_request_services import (
    approve_join_request,
    reject_join_request,
)
from apps.users.services.join_requests.teacher_join_request_services import (
    create_teacher_join_request,
)

__all__ = [
    "approve_join_request",
    "create_guardian_join_request",
    "create_join_request",
    "create_learner_join_request",
    "create_teacher_join_request",
    "reject_join_request",
]
