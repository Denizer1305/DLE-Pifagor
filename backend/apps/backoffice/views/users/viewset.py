from __future__ import annotations

from apps.backoffice.constants import (
    BACKOFFICE_USER_DEFAULT_ORDERING,
    BACKOFFICE_USER_LIST_SEARCH_FIELDS,
    BackofficeUserAction,
)
from apps.backoffice.filters import BackofficeUserFilter
from apps.backoffice.permissions import (
    CanAccessBackofficeUsers,
    CanBulkManageBackofficeUsers,
    CanDeleteBackofficeUser,
    CanManageBackofficeUser,
    CanManageBackofficeUserRoles,
    CanManageBackofficeUserStatus,
    CanViewBackofficeUserAudit,
)
from apps.backoffice.selectors.users import get_backoffice_users_list_queryset
from apps.backoffice.serializers.users import (
    BackofficeUserAuditLogListSerializer,
    BackofficeUserAvailableRoleSerializer,
    BackofficeUserBulkSerializer,
    BackofficeUserChangeRolesSerializer,
    BackofficeUserDeleteSerializer,
    BackofficeUserDetailSerializer,
    BackofficeUserListSerializer,
    BackofficeUserStatusActionSerializer,
    BackofficeUserUpdateSerializer,
)
from apps.backoffice.views.users.audit_actions import BackofficeUserAuditActionsMixin
from apps.backoffice.views.users.bulk_actions import BackofficeUserBulkActionsMixin
from apps.backoffice.views.users.mutations import BackofficeUserMutationActionsMixin
from apps.backoffice.views.users.responses import BackofficeUserResponseMixin
from apps.backoffice.views.users.role_actions import BackofficeUserRoleActionsMixin
from apps.backoffice.views.users.status_actions import BackofficeUserStatusActionsMixin
from apps.core.mixins import PermissionByActionMixin, SerializerByActionMixin
from apps.core.pagination import DefaultPageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter


class BackofficeUserViewSet(
    SerializerByActionMixin,
    PermissionByActionMixin,
    BackofficeUserResponseMixin,
    BackofficeUserMutationActionsMixin,
    BackofficeUserStatusActionsMixin,
    BackofficeUserRoleActionsMixin,
    BackofficeUserBulkActionsMixin,
    BackofficeUserAuditActionsMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    ViewSet административного управления пользователями.
    """

    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    filterset_class = BackofficeUserFilter
    pagination_class = DefaultPageNumberPagination
    search_fields = BACKOFFICE_USER_LIST_SEARCH_FIELDS
    ordering = BACKOFFICE_USER_DEFAULT_ORDERING
    ordering_fields = (
        "id",
        "email",
        "first_name",
        "last_name",
        "status",
        "is_active",
        "created_at",
        "updated_at",
        "scheduled_for_deletion_at",
    )

    serializer_class = BackofficeUserDetailSerializer
    serializer_action_classes = {
        BackofficeUserAction.LIST: BackofficeUserListSerializer,
        BackofficeUserAction.RETRIEVE: BackofficeUserDetailSerializer,
        BackofficeUserAction.UPDATE: BackofficeUserUpdateSerializer,
        BackofficeUserAction.PARTIAL_UPDATE: BackofficeUserUpdateSerializer,
        BackofficeUserAction.DESTROY: BackofficeUserDeleteSerializer,
        BackofficeUserAction.BLOCK: BackofficeUserStatusActionSerializer,
        BackofficeUserAction.UNBLOCK: BackofficeUserStatusActionSerializer,
        BackofficeUserAction.ARCHIVE: BackofficeUserStatusActionSerializer,
        BackofficeUserAction.RESTORE: BackofficeUserStatusActionSerializer,
        BackofficeUserAction.CHANGE_ROLES: BackofficeUserChangeRolesSerializer,
        BackofficeUserAction.BULK: BackofficeUserBulkSerializer,
        BackofficeUserAction.AVAILABLE_ROLES: (BackofficeUserAvailableRoleSerializer),
        BackofficeUserAction.AUDIT_LOGS: BackofficeUserAuditLogListSerializer,
    }

    permission_classes = (CanAccessBackofficeUsers,)
    permission_action_classes = {
        BackofficeUserAction.LIST: (CanAccessBackofficeUsers,),
        BackofficeUserAction.RETRIEVE: (CanAccessBackofficeUsers,),
        BackofficeUserAction.UPDATE: (CanManageBackofficeUser,),
        BackofficeUserAction.PARTIAL_UPDATE: (CanManageBackofficeUser,),
        BackofficeUserAction.DESTROY: (CanDeleteBackofficeUser,),
        BackofficeUserAction.BLOCK: (CanManageBackofficeUserStatus,),
        BackofficeUserAction.UNBLOCK: (CanManageBackofficeUserStatus,),
        BackofficeUserAction.ARCHIVE: (CanManageBackofficeUserStatus,),
        BackofficeUserAction.RESTORE: (CanManageBackofficeUserStatus,),
        BackofficeUserAction.CHANGE_ROLES: (CanManageBackofficeUserRoles,),
        BackofficeUserAction.BULK: (CanBulkManageBackofficeUsers,),
        BackofficeUserAction.AVAILABLE_ROLES: (CanAccessBackofficeUsers,),
        BackofficeUserAction.AUDIT_LOGS: (CanViewBackofficeUserAudit,),
    }

    def get_queryset(self):
        """
        Возвращает пользователей, доступных текущему администратору.
        """

        return get_backoffice_users_list_queryset(
            actor=self.request.user,
        )
