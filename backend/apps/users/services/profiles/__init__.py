"""
Сервисы профилей пользователей.

Пакет содержит операции с базовым профилем,
профилями учащихся, родителей, преподавателей и модерацией.
"""

from apps.users.services.current_profile import (
    build_current_profile_payload,
    delete_current_profile_avatar,
    update_current_profile,
    update_current_profile_avatar,
)
from apps.users.services.profiles.base_profile_services import create_base_profile
from apps.users.services.profiles.guardian_profile_services import (
    create_guardian_learner_link,
    create_guardian_profile,
)
from apps.users.services.profiles.learner_profile_services import (
    create_learner_profile,
    verify_learner_profile,
)
from apps.users.services.profiles.profile_moderation_services import (
    moderate_avatar,
    reject_profile,
    submit_avatar_for_moderation,
)
from apps.users.services.profiles.teacher_profile_services import (
    create_teacher_profile,
    verify_teacher_profile,
)

__all__ = [
    "create_base_profile",
    "create_guardian_learner_link",
    "create_guardian_profile",
    "create_learner_profile",
    "create_teacher_profile",
    "moderate_avatar",
    "reject_profile",
    "submit_avatar_for_moderation",
    "verify_learner_profile",
    "verify_teacher_profile",
    "build_current_profile_payload",
    "delete_current_profile_avatar",
    "update_current_profile",
    "update_current_profile_avatar",
]
