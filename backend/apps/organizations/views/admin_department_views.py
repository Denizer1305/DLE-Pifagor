from __future__ import annotations

from apps.organizations.filters import filter_departments_queryset
from apps.organizations.models import Department
from apps.organizations.permissions import CanManageDepartments
from apps.organizations.selectors import get_admin_departments_queryset_for_actor
from apps.organizations.serializers import (
    DepartmentDetailSerializer,
    DepartmentListSerializer,
    DepartmentWriteSerializer,
)
from apps.organizations.services import (
    create_department,
    deactivate_department,
    restore_department,
    update_department,
)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class AdminDepartmentViewSet(viewsets.ViewSet):
    """
    Административное управление отделениями.
    """

    permission_classes = [CanManageDepartments]

    def get_queryset(self):
        """
        Возвращает отделения, доступные текущему пользователю.
        """

        return get_admin_departments_queryset_for_actor(
            actor=self.request.user,
        )

    def get_object(self) -> Department:
        """
        Возвращает отделение из доступного queryset.
        """

        return self.get_queryset().get(pk=self.kwargs["pk"])

    def list(self, request):
        """
        Возвращает список отделений.
        """

        queryset = filter_departments_queryset(
            queryset=self.get_queryset(),
            params=request.query_params,
        )

        serializer = DepartmentListSerializer(
            queryset,
            many=True,
            context={
                "request": request,
            },
        )

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Возвращает детальную карточку отделения.
        """

        department = self.get_object()

        serializer = DepartmentDetailSerializer(
            department,
            context={
                "request": request,
            },
        )

        return Response(serializer.data)

    def create(self, request):
        """
        Создаёт отделение.
        """

        serializer = DepartmentWriteSerializer(
            data=request.data,
            context={
                "is_create": True,
            },
        )
        serializer.is_valid(raise_exception=True)

        department = create_department(
            actor=request.user,
            organization=serializer.validated_data["organization"],
            data=serializer.validated_data,
        )

        output_serializer = DepartmentDetailSerializer(
            department,
            context={
                "request": request,
            },
        )

        return Response(
            output_serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def partial_update(self, request, pk=None):
        """
        Частично обновляет отделение.
        """

        department = self.get_object()

        serializer = DepartmentWriteSerializer(
            data=request.data,
            partial=True,
            context={
                "is_create": False,
            },
        )
        serializer.is_valid(raise_exception=True)

        department = update_department(
            actor=request.user,
            department=department,
            data=serializer.validated_data,
        )

        output_serializer = DepartmentDetailSerializer(
            department,
            context={
                "request": request,
            },
        )

        return Response(output_serializer.data)

    def destroy(self, request, pk=None):
        """
        Деактивирует отделение вместо физического удаления.
        """

        department = self.get_object()

        department = deactivate_department(
            actor=request.user,
            department=department,
        )

        serializer = DepartmentDetailSerializer(
            department,
            context={
                "request": request,
            },
        )

        return Response(serializer.data)

    @action(
        detail=True,
        methods=["post"],
        url_path="restore",
    )
    def restore(self, request, pk=None):
        """
        Восстанавливает отделение.
        """

        department = self.get_object()

        department = restore_department(
            actor=request.user,
            department=department,
        )

        serializer = DepartmentDetailSerializer(
            department,
            context={
                "request": request,
            },
        )

        return Response(serializer.data)
