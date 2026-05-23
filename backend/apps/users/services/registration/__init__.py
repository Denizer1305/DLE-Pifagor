"""
Сервисы регистрации пользователей.

Пакет содержит отдельные сценарии регистрации:
    - преподаватель;
    - учащийся старше 14 лет;
    - родитель;
    - ребёнок младше 14 лет через родителя.
"""

from apps.users.services.registration.guardian_registration_services import (
    register_guardian,
)
from apps.users.services.registration.learner_registration_services import (
    register_learner,
    submit_learner_group_request,
)
from apps.users.services.registration.minor_learner_registration_services import (
    register_minor_learner_by_guardian,
)
from apps.users.services.registration.teacher_registration_services import (
    register_teacher,
)

__all__ = [
    "register_guardian",
    "register_learner",
    "register_minor_learner_by_guardian",
    "register_teacher",
    "submit_learner_group_request",
]
