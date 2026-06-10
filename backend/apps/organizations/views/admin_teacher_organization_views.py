from __future__ import annotations

from apps.organizations.filters import filter_teacher_organizations_queryset
from apps.organizations.models import TeacherOrganization
from apps.organizations.permissions import CanManageTeacherOrganizations
from apps.organizations.selectors import (
    get_admin_teacher_organizations_queryset_for_actor,
)
from apps.organizations.serializers import (
    TeacherOrganizationDetailSerializer,
    TeacherOrganizationListSerializer,
    TeacherOrganizationWriteSerializer,
)
from apps.organizations.services import (
    attach_teacher_to_organization,
    detach_teacher_from_organization,
    set_primary_teacher_organization,
    update_teacher_organization,
)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class AdminTeacherOrganizationViewSet(viewsets.ViewSet):
    """
    Административное управление связями преподавателей с организациями.
    """

    permission_classes = [CanManageTeacherOrganizations]

    def get_queryset(self):
        """
        Возвращает связи преподавателей с организациями,
        доступные текущему пользователю.
        """

        return get_admin_teacher_organizations_queryset_for_actor(
            actor=self.request.user,
        )

    def get_object(self) -> TeacherOrganization:
        """
        Возвращает связь преподавателя с организацией из доступного queryset.
        """

        return self.get_queryset().get(pk=self.kwargs["pk"])

    def list(self, request):
        """
        Возвращает список связей преподавателей с организациями.
        """

        queryset = filter_teacher_organizations_queryset(
            queryset=self.get_queryset(),
            params=request.query_params,
        )

        serializer = TeacherOrganizationListSerializer(
            queryset,
            many=True,
            context={
                "request": request,
            },
        )

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Возвращает детальную карточку связи преподавателя с организацией.
        """

        teacher_organization = self.get_object()

        serializer = TeacherOrganizationDetailSerializer(
            teacher_organization,
            context={
                "request": request,
            },
        )

        return Response(serializer.data)

    def create(self, request):
        """
        Привязывает преподавателя к образовательной организации.
        """

        serializer = TeacherOrganizationWriteSerializer(
            data=request.data,
            context={
                "is_create": True,
            },
        )
        serializer.is_valid(raise_exception=True)

        teacher_organization = attach_teacher_to_organization(
            actor=request.user,
            teacher=serializer.validated_data["teacher"],
            organization=serializer.validated_data["organization"],
            data=serializer.validated_data,
        )

        output_serializer = TeacherOrganizationDetailSerializer(
            teacher_organization,
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
        Частично обновляет связь преподавателя с организацией.
        """

        teacher_organization = self.get_object()

        serializer = TeacherOrganizationWriteSerializer(
            data=request.data,
            partial=True,
            context={
                "is_create": False,
            },
        )
        serializer.is_valid(raise_exception=True)

        teacher_organization = update_teacher_organization(
            actor=request.user,
            teacher_organization=teacher_organization,
            data=serializer.validated_data,
        )

        output_serializer = TeacherOrganizationDetailSerializer(
            teacher_organization,
            context={
                "request": request,
            },
        )

        return Response(output_serializer.data)

    def destroy(self, request, pk=None):
        """
        Деактивирует связь преподавателя с организацией.
        """

        teacher_organization = self.get_object()

        teacher_organization = detach_teacher_from_organization(
            actor=request.user,
            teacher_organization=teacher_organization,
        )

        serializer = TeacherOrganizationDetailSerializer(
            teacher_organization,
            context={
                "request": request,
            },
        )

        return Response(serializer.data)

    @action(
        detail=True,
        methods=["post"],
        url_path="set-primary",
    )
    def set_primary(self, request, pk=None):
        """
        Делает организацию основной для преподавателя.
        """

        teacher_organization = self.get_object()

        teacher_organization = set_primary_teacher_organization(
            actor=request.user,
            teacher_organization=teacher_organization,
        )

        serializer = TeacherOrganizationDetailSerializer(
            teacher_organization,
            context={
                "request": request,
            },
        )

        return Response(serializer.data)
