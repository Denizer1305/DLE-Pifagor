from __future__ import annotations

from apps.users.filters import RoleFilter, UserRoleFilter
from apps.users.models import Role, UserRole
from apps.users.permissions import CanManageSystemRoles, CanViewRoles, CanViewUserRole
from apps.users.serializers import RoleSerializer, UserRoleSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets


class RoleViewSet(viewsets.ModelViewSet):
    """
    ViewSet системных ролей.
    """

    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    filterset_class = RoleFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = [
        "code",
        "label",
        "description",
    ]
    ordering_fields = [
        "id",
        "code",
        "label",
        "sort_order",
    ]
    ordering = [
        "sort_order",
        "label",
    ]

    def get_permissions(self):
        """
        Возвращает permissions.

        Returns:
            list: Permissions.
        """

        if self.action in {"create", "update", "partial_update", "destroy"}:
            return [CanManageSystemRoles()]

        return [CanViewRoles()]


class UserRoleViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet назначенных ролей пользователей.
    """

    queryset = UserRole.objects.select_related(
        "user",
        "role",
        "organization",
        "department",
        "group",
    )
    serializer_class = UserRoleSerializer
    filterset_class = UserRoleFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    ordering_fields = [
        "id",
        "assigned_at",
        "created_at",
    ]
    ordering = [
        "-assigned_at",
    ]

    def get_permissions(self):
        """
        Возвращает permissions.

        Returns:
            list: Permissions.
        """

        return [CanViewUserRole()]

    def get_queryset(self):
        """
        Ограничивает список назначенных ролей.

        Returns:
            QuerySet: Роли пользователей.
        """

        user = self.request.user

        if not user.is_authenticated:
            return UserRole.objects.none()

        if user.is_superuser:
            return self.queryset

        return self.queryset.filter(user=user)
