from __future__ import annotations

from apps.organizations.filters import filter_organizations_queryset
from apps.organizations.models import Organization
from apps.organizations.permissions import (
    CanManageOrganizationCodes,
    CanManageOrganizations,
)
from apps.organizations.selectors import get_admin_organizations_queryset_for_actor
from apps.organizations.serializers import (
    OrganizationDetailSerializer,
    OrganizationListSerializer,
    OrganizationWriteSerializer,
    TeacherRegistrationCodeOutputSerializer,
    TeacherRegistrationCodeSetSerializer,
)
from apps.organizations.services import (
    clear_teacher_registration_code,
    create_organization,
    deactivate_organization,
    disable_teacher_registration_code,
    restore_organization,
    set_teacher_registration_code,
    update_organization,
)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class AdminOrganizationViewSet(viewsets.ViewSet):
    """
    Административное управление образовательными организациями.
    """

    permission_classes = [CanManageOrganizations]

    def get_queryset(self):
        """
        Возвращает организации, доступные текущему пользователю.
        """

        return get_admin_organizations_queryset_for_actor(
            actor=self.request.user,
        )

    def get_object(self) -> Organization:
        """
        Возвращает организацию из доступного queryset.
        """

        return self.get_queryset().get(pk=self.kwargs["pk"])

    def list(self, request):
        """
        Возвращает список организаций.
        """

        queryset = filter_organizations_queryset(
            queryset=self.get_queryset(),
            params=request.query_params,
        )

        serializer = OrganizationListSerializer(
            queryset,
            many=True,
            context={"request": request},
        )

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Возвращает детальную карточку организации.
        """

        organization = self.get_object()

        serializer = OrganizationDetailSerializer(
            organization,
            context={"request": request},
        )

        return Response(serializer.data)

    def create(self, request):
        """
        Создаёт организацию.
        """

        serializer = OrganizationWriteSerializer(
            data=request.data,
            context={"is_create": True},
        )
        serializer.is_valid(raise_exception=True)

        organization = create_organization(
            actor=request.user,
            data=serializer.validated_data,
        )

        output_serializer = OrganizationDetailSerializer(
            organization,
            context={"request": request},
        )

        return Response(
            output_serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def partial_update(self, request, pk=None):
        """
        Частично обновляет организацию.
        """

        organization = self.get_object()

        serializer = OrganizationWriteSerializer(
            data=request.data,
            partial=True,
            context={"is_create": False},
        )
        serializer.is_valid(raise_exception=True)

        organization = update_organization(
            actor=request.user,
            organization=organization,
            data=serializer.validated_data,
        )

        output_serializer = OrganizationDetailSerializer(
            organization,
            context={"request": request},
        )

        return Response(output_serializer.data)

    def destroy(self, request, pk=None):
        """
        Деактивирует организацию вместо физического удаления.
        """

        organization = self.get_object()

        organization = deactivate_organization(
            actor=request.user,
            organization=organization,
        )

        serializer = OrganizationDetailSerializer(
            organization,
            context={"request": request},
        )

        return Response(serializer.data)

    @action(
        detail=True,
        methods=["post"],
        url_path="restore",
    )
    def restore(self, request, pk=None):
        """
        Восстанавливает организацию.
        """

        organization = self.get_object()

        organization = restore_organization(
            actor=request.user,
            organization=organization,
        )

        serializer = OrganizationDetailSerializer(
            organization,
            context={"request": request},
        )

        return Response(serializer.data)

    @action(
        detail=True,
        methods=["post"],
        url_path="set-teacher-registration-code",
        permission_classes=[CanManageOrganizationCodes],
    )
    def set_teacher_code(self, request, pk=None):
        """
        Устанавливает код регистрации преподавателя.
        """

        organization = self.get_object()

        serializer = TeacherRegistrationCodeSetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        organization, raw_code = set_teacher_registration_code(
            actor=request.user,
            organization=organization,
            raw_code=serializer.validated_data.get("raw_code", ""),
            expires_at=serializer.validated_data.get("expires_at"),
        )

        output_serializer = TeacherRegistrationCodeOutputSerializer(
            {
                "organization": organization,
                "raw_code": raw_code,
            },
            context={"request": request},
        )

        return Response(output_serializer.data)

    @action(
        detail=True,
        methods=["post"],
        url_path="disable-teacher-registration-code",
        permission_classes=[CanManageOrganizationCodes],
    )
    def disable_teacher_code(self, request, pk=None):
        """
        Отключает код регистрации преподавателя.
        """

        organization = self.get_object()

        organization = disable_teacher_registration_code(
            actor=request.user,
            organization=organization,
        )

        serializer = OrganizationDetailSerializer(
            organization,
            context={"request": request},
        )

        return Response(serializer.data)

    @action(
        detail=True,
        methods=["post"],
        url_path="clear-teacher-registration-code",
        permission_classes=[CanManageOrganizationCodes],
    )
    def clear_teacher_code(self, request, pk=None):
        """
        Очищает код регистрации преподавателя.
        """

        organization = self.get_object()

        organization = clear_teacher_registration_code(
            actor=request.user,
            organization=organization,
        )

        serializer = OrganizationDetailSerializer(
            organization,
            context={"request": request},
        )

        return Response(serializer.data)