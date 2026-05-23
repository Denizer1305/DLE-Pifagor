"""
Менеджеры приложения users.

Managers и QuerySets отвечают за удобные выборки и базовое создание объектов.

Важно:
    Сложные бизнес-сценарии не должны жить в managers.
    Для регистрации, подтверждения заявок, анонимизации и выдачи кодов
    используются сервисы из `users/services/`.
"""

from apps.users.managers.invite_code_manager import (
    InviteCodeManager,
    InviteCodeQuerySet,
)
from apps.users.managers.role_manager import (
    RoleManager,
    RoleQuerySet,
    UserRoleManager,
    UserRoleQuerySet,
)
from apps.users.managers.user_join_request_manager import (
    UserJoinRequestManager,
    UserJoinRequestQuerySet,
)
from apps.users.managers.user_manager import UserManager, UserQuerySet

__all__ = [
    "InviteCodeManager",
    "InviteCodeQuerySet",
    "RoleManager",
    "RoleQuerySet",
    "UserJoinRequestManager",
    "UserJoinRequestQuerySet",
    "UserManager",
    "UserQuerySet",
    "UserRoleManager",
    "UserRoleQuerySet",
]
