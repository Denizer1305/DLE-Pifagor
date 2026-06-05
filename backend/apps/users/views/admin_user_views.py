from __future__ import annotations

from apps.users.filters.admin_user_filters import AdminUserFilter
from apps.users.models import Role, UserAuditLog
from apps.users.permissions.admin_user_permissions import (
    CanAccessAdminUsers,
    CanBulkManageAdminUsers,
    CanManageAdminUser,
    CanManageAdminUserRoles,
    CanManageAdminUserStatus,
)
from apps.users.selectors.admin_user_selectors import (
    filter_admin_users_by_role_group,
    get_admin_user_detail_queryset_for_actor,
    get_admin_users_queryset_for_actor,
)
from apps.users.serializers.admin_user_serializers import (
    AdminUserAuditLogListSerializer,
    AdminUserAvailableRoleSerializer,
    AdminUserBulkResultSerializer,
    AdminUserBulkSerializer,
    AdminUserChangeRolesSerializer,
    AdminUserDeleteSerializer,
    AdminUserDetailSerializer,
    AdminUserListSerializer,
    AdminUserStatusActionSerializer,
    AdminUserUpdateSerializer,
)
from apps.users.services.admin_users.bulk_services import (
    execute_admin_users_bulk_action,
)
from apps.users.services.admin_users.delete_services import admin_schedule_user_deletion
from apps.users.services.admin_users.role_services import admin_change_user_roles
from apps.users.services.admin_users.status_services import (
    admin_archive_user,
    admin_block_user,
    admin_restore_user,
    admin_unblock_user,
)
from apps.users.services.admin_users.update_services import admin_update_user
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response


class AdminUserViewSet(viewsets.ModelViewSet):
    """
    ViewSet административного управления пользователями.

    Endpoint'ы:
        GET    /api/v1/users/admin/users/
        GET    /api/v1/users/admin/users/{id}/
        PATCH  /api/v1/users/admin/users/{id}/
        POST   /api/v1/users/admin/users/{id}/block/
        POST   /api/v1/users/admin/users/{id}/unblock/
        POST   /api/v1/users/admin/users/{id}/archive/
        POST   /api/v1/users/admin/users/{id}/restore/
        POST   /api/v1/users/admin/users/{id}/change-roles/
        DELETE /api/v1/users/admin/users/{id}/
        POST   /api/v1/users/admin/users/bulk/
    """

    http_method_names = [
        "get",
        "patch",
        "post",
        "delete",
        "head",
        "options",
    ]
    permission_classes = [CanAccessAdminUsers]
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]
    filterset_class = AdminUserFilter
    search_fields = [
        "email",
        "phone",
        "first_name",
        "last_name",
        "middle_name",
    ]
    ordering_fields = [
        "id",
        "email",
        "first_name",
        "last_name",
        "status",
        "created_at",
        "updated_at",
        "scheduled_for_deletion_at",
    ]
    ordering = [
        "last_name",
        "first_name",
        "email",
    ]

    def get_queryset(self):
        """
        Возвращает QuerySet пользователей с учётом прав администратора.

        Query parameter role_group дополнительно ограничивает список:
            - students;
            - teachers;
            - parents.

        Returns:
            QuerySet: Доступные пользователи.
        """

        queryset = get_admin_users_queryset_for_actor(
            actor=self.request.user,
        )

        role_group = self.request.query_params.get("role_group")

        if role_group:
            queryset = filter_admin_users_by_role_group(
                queryset=queryset,
                role_group=role_group,
            )

        return queryset

    def get_object(self):
        """
        Возвращает объект пользователя с учётом административной области доступа.

        Returns:
            User: Целевой пользователь.
        """

        queryset = get_admin_user_detail_queryset_for_actor(
            actor=self.request.user,
        )

        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        lookup_value = self.kwargs[lookup_url_kwarg]

        obj = queryset.get(**{self.lookup_field: lookup_value})
        self.check_object_permissions(self.request, obj)

        return obj

    def get_permissions(self):
        """
        Возвращает permissions в зависимости от action.

        Returns:
            list: Список permission-классов.
        """

        if self.action in {"partial_update", "update"}:
            permission_classes = [CanManageAdminUser]
        elif self.action in {
            "block",
            "unblock",
            "archive",
            "restore",
            "destroy",
        }:
            permission_classes = [CanManageAdminUserStatus]
        elif self.action == "change_roles":
            permission_classes = [CanManageAdminUserRoles]
        elif self.action == "bulk":
            permission_classes = [CanBulkManageAdminUsers]
        else:
            permission_classes = [CanAccessAdminUsers]

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """
        Возвращает serializer-класс для текущего action.

        Returns:
            type[Serializer]: Класс serializer'а.
        """

        if self.action == "list":
            return AdminUserListSerializer

        if self.action == "retrieve":
            return AdminUserDetailSerializer

        if self.action in {"partial_update", "update"}:
            return AdminUserUpdateSerializer

        if self.action in {"block", "unblock", "archive", "restore"}:
            return AdminUserStatusActionSerializer

        if self.action == "destroy":
            return AdminUserDeleteSerializer

        if self.action == "change_roles":
            return AdminUserChangeRolesSerializer

        if self.action == "bulk":
            return AdminUserBulkSerializer

        if self.action == "available_roles":
            return AdminUserAvailableRoleSerializer

        if self.action == "audit_logs":
            return AdminUserAuditLogListSerializer

        return AdminUserDetailSerializer

    def get_serializer_context(self):
        """
        Возвращает context для serializer'ов.

        Returns:
            dict: Контекст serializer'а.
        """

        context = super().get_serializer_context()
        context["actor"] = self.request.user

        return context

    def get_expected_updated_at(self, serializer):
        """
        Возвращает expected_updated_at из serializer'а в строковом формате.

        Сервисы используют строку ISO-формата, чтобы одинаково работать
        с данными из одиночных и массовых действий.

        Args:
            serializer:
                Валидированный serializer.

        Returns:
            str: expected_updated_at или пустая строка.
        """

        expected_updated_at = serializer.validated_data.get("expected_updated_at")

        return expected_updated_at or ""

    def list(self, request, *args, **kwargs):
        """
        Возвращает страницу административного списка пользователей.

        Args:
            request:
                HTTP-запрос.

        Returns:
            Response: Список пользователей.
        """

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = AdminUserListSerializer(
                page,
                many=True,
                context=self.get_serializer_context(),
            )

            return self.get_paginated_response(serializer.data)

        serializer = AdminUserListSerializer(
            queryset,
            many=True,
            context=self.get_serializer_context(),
        )

        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """
        Возвращает детальную карточку пользователя.

        Args:
            request:
                HTTP-запрос.

        Returns:
            Response: Данные пользователя.
        """

        target_user = self.get_object()
        serializer = AdminUserDetailSerializer(
            target_user,
            context=self.get_serializer_context(),
        )

        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        """
        Обновляет базовые данные пользователя из административного раздела.

        Args:
            request:
                HTTP-запрос.

        Returns:
            Response: Обновлённая детальная карточка пользователя.
        """

        target_user = self.get_object()
        serializer = AdminUserUpdateSerializer(
            data=request.data,
            context=self.get_serializer_context(),
        )
        serializer.is_valid(raise_exception=True)

        updated_user = admin_update_user(
            actor=request.user,
            target_user=target_user,
            data=serializer.get_service_payload(),
            expected_updated_at=self.get_expected_updated_at(serializer),
            reason=serializer.validated_data.get("reason", ""),
            request=request,
        )

        output_serializer = AdminUserDetailSerializer(
            updated_user,
            context=self.get_serializer_context(),
        )

        return Response(output_serializer.data)

    def update(self, request, *args, **kwargs):
        """
        Полное обновление пользователя в админке отключено.

        Для административного редактирования используется PATCH, чтобы случайно
        не стереть поля пользователя неполным payload'ом.

        Args:
            request:
                HTTP-запрос.

        Returns:
            Response: Ошибка метода.
        """

        return Response(
            {
                "detail": "Используйте PATCH для редактирования пользователя.",
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def destroy(self, request, *args, **kwargs):
        """
        Планирует удаление пользователя.

        Физическое удаление не выполняется сразу. Пользователь переводится
        в статус SCHEDULED_FOR_DELETION.

        Args:
            request:
                HTTP-запрос.

        Returns:
            Response: Обновлённая детальная карточка пользователя.
        """

        target_user = self.get_object()
        serializer = AdminUserDeleteSerializer(
            data=request.data,
            context=self.get_serializer_context(),
        )
        serializer.is_valid(raise_exception=True)

        updated_user = admin_schedule_user_deletion(
            actor=request.user,
            target_user=target_user,
            when=serializer.validated_data.get("scheduled_for_deletion_at"),
            reason=serializer.validated_data.get("reason", ""),
            request=request,
        )

        output_serializer = AdminUserDetailSerializer(
            updated_user,
            context=self.get_serializer_context(),
        )

        return Response(
            output_serializer.data,
            status=status.HTTP_202_ACCEPTED,
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="block",
        permission_classes=[CanManageAdminUserStatus],
    )
    def block(self, request, *args, **kwargs):
        """
        Блокирует пользователя.

        Args:
            request:
                HTTP-запрос.

        Returns:
            Response: Обновлённая детальная карточка пользователя.
        """

        target_user = self.get_object()
        serializer = AdminUserStatusActionSerializer(
            data=request.data,
            context=self.get_serializer_context(),
        )
        serializer.is_valid(raise_exception=True)

        updated_user = admin_block_user(
            actor=request.user,
            target_user=target_user,
            reason=serializer.validated_data.get("reason", ""),
            request=request,
        )

        output_serializer = AdminUserDetailSerializer(
            updated_user,
            context=self.get_serializer_context(),
        )

        return Response(output_serializer.data)

    @action(
        detail=True,
        methods=["post"],
        url_path="unblock",
        permission_classes=[CanManageAdminUserStatus],
    )
    def unblock(self, request, *args, **kwargs):
        """
        Разблокирует пользователя.

        Args:
            request:
                HTTP-запрос.

        Returns:
            Response: Обновлённая детальная карточка пользователя.
        """

        target_user = self.get_object()
        serializer = AdminUserStatusActionSerializer(
            data=request.data,
            context=self.get_serializer_context(),
        )
        serializer.is_valid(raise_exception=True)

        updated_user = admin_unblock_user(
            actor=request.user,
            target_user=target_user,
            reason=serializer.validated_data.get("reason", ""),
            request=request,
        )

        output_serializer = AdminUserDetailSerializer(
            updated_user,
            context=self.get_serializer_context(),
        )

        return Response(output_serializer.data)

    @action(
        detail=True,
        methods=["post"],
        url_path="archive",
        permission_classes=[CanManageAdminUserStatus],
    )
    def archive(self, request, *args, **kwargs):
        """
        Архивирует пользователя.

        Args:
            request:
                HTTP-запрос.

        Returns:
            Response: Обновлённая детальная карточка пользователя.
        """

        target_user = self.get_object()
        serializer = AdminUserStatusActionSerializer(
            data=request.data,
            context=self.get_serializer_context(),
        )
        serializer.is_valid(raise_exception=True)

        updated_user = admin_archive_user(
            actor=request.user,
            target_user=target_user,
            reason=serializer.validated_data.get("reason", ""),
            request=request,
        )

        output_serializer = AdminUserDetailSerializer(
            updated_user,
            context=self.get_serializer_context(),
        )

        return Response(output_serializer.data)

    @action(
        detail=True,
        methods=["post"],
        url_path="restore",
        permission_classes=[CanManageAdminUserStatus],
    )
    def restore(self, request, *args, **kwargs):
        """
        Восстанавливает пользователя.

        Args:
            request:
                HTTP-запрос.

        Returns:
            Response: Обновлённая детальная карточка пользователя.
        """

        target_user = self.get_object()
        serializer = AdminUserStatusActionSerializer(
            data=request.data,
            context=self.get_serializer_context(),
        )
        serializer.is_valid(raise_exception=True)

        updated_user = admin_restore_user(
            actor=request.user,
            target_user=target_user,
            reason=serializer.validated_data.get("reason", ""),
            request=request,
        )

        output_serializer = AdminUserDetailSerializer(
            updated_user,
            context=self.get_serializer_context(),
        )

        return Response(output_serializer.data)

    @action(
        detail=True,
        methods=["post"],
        url_path="change-roles",
        permission_classes=[CanManageAdminUserRoles],
    )
    def change_roles(self, request, *args, **kwargs):
        """
        Изменяет роли пользователя.

        Args:
            request:
                HTTP-запрос.

        Returns:
            Response: Обновлённая детальная карточка пользователя.
        """

        target_user = self.get_object()
        serializer = AdminUserChangeRolesSerializer(
            data=request.data,
            context=self.get_serializer_context(),
        )
        serializer.is_valid(raise_exception=True)

        admin_change_user_roles(
            actor=request.user,
            target_user=target_user,
            assigned_roles=serializer.validated_data.get("assigned_roles", []),
            revoked_user_role_ids=serializer.validated_data.get(
                "revoked_user_role_ids",
                [],
            ),
            reason=serializer.validated_data.get("reason", ""),
            request=request,
        )

        target_user.refresh_from_db()

        output_serializer = AdminUserDetailSerializer(
            target_user,
            context=self.get_serializer_context(),
        )

        return Response(output_serializer.data)

    @action(
        detail=False,
        methods=["post"],
        url_path="bulk",
        permission_classes=[CanBulkManageAdminUsers],
    )
    def bulk(self, request, *args, **kwargs):
        """
        Выполняет массовое действие над пользователями.

        Args:
            request:
                HTTP-запрос.

        Returns:
            Response: Результат массового действия.
        """

        serializer = AdminUserBulkSerializer(
            data=request.data,
            context=self.get_serializer_context(),
        )
        serializer.is_valid(raise_exception=True)

        bulk_result = execute_admin_users_bulk_action(
            action=serializer.validated_data["action"],
            actor=request.user,
            user_ids=serializer.validated_data["user_ids"],
            reason=serializer.validated_data.get("reason", ""),
            role_payload=serializer.validated_data.get("role_payload", {}),
            expected_updated_at_by_user_id=serializer.validated_data.get(
                "expected_updated_at_by_user_id",
                {},
            ),
            request=request,
        )

        output_serializer = AdminUserBulkResultSerializer(
            bulk_result.to_dict(),
        )

        return Response(
            output_serializer.data,
            status=status.HTTP_200_OK,
        )

    @action(
        detail=False,
        methods=["get"],
        url_path="available-roles",
        permission_classes=[CanAccessAdminUsers],
    )
    def available_roles(self, request, *args, **kwargs):
        """
        Возвращает список активных ролей для интерфейса назначения ролей.

        Важно:
            Ограничения, какую роль реально можно назначить, всё равно
            проверяются в role_services.py.

        Args:
            request:
                HTTP-запрос.

        Returns:
            Response: Список ролей.
        """

        queryset = Role.objects.filter(
            is_active=True,
        ).order_by(
            "sort_order",
            "label",
        )

        serializer = AdminUserAvailableRoleSerializer(
            queryset,
            many=True,
            context=self.get_serializer_context(),
        )

        return Response(serializer.data)

    @action(
        detail=True,
        methods=["get"],
        url_path="audit-logs",
        permission_classes=[CanAccessAdminUsers],
    )
    def audit_logs(self, request, *args, **kwargs):
        """
        Возвращает историю действий по пользователю.

        Args:
            request:
                HTTP-запрос.

        Returns:
            Response: Список записей аудита.
        """

        target_user = self.get_object()

        queryset = (
            UserAuditLog.objects.select_related(
                "actor",
                "target_user",
            )
            .filter(
                target_user=target_user,
            )
            .order_by(
                "-created_at",
            )
        )

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = AdminUserAuditLogListSerializer(
                page,
                many=True,
                context=self.get_serializer_context(),
            )

            return self.get_paginated_response(serializer.data)

        serializer = AdminUserAuditLogListSerializer(
            queryset,
            many=True,
            context=self.get_serializer_context(),
        )

        return Response(serializer.data)
