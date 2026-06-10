from __future__ import annotations

from apps.organizations.filters import filter_study_groups_queryset
from apps.organizations.models import StudyGroup
from apps.organizations.permissions import (
    CanManageOrganizationCodes,
    CanManageStudyGroups,
)
from apps.organizations.selectors import get_admin_study_groups_queryset_for_actor
from apps.organizations.serializers import (
    GroupJoinCodeOutputSerializer,
    GroupJoinCodeSetSerializer,
    StudyGroupDetailSerializer,
    StudyGroupListSerializer,
    StudyGroupWriteSerializer,
)
from apps.organizations.services import (
    archive_study_group,
    clear_group_join_code,
    create_study_group,
    disable_group_join_code,
    restore_study_group,
    set_group_join_code,
    update_study_group,
)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class AdminStudyGroupViewSet(viewsets.ViewSet):
    """
    Административное управление учебными группами.
    """

    permission_classes = [CanManageStudyGroups]

    def get_queryset(self):
        """
        Возвращает учебные группы, доступные текущему пользователю.
        """

        return get_admin_study_groups_queryset_for_actor(
            actor=self.request.user,
        )

    def get_object(self) -> StudyGroup:
        """
        Возвращает учебную группу из доступного queryset.
        """

        return self.get_queryset().get(pk=self.kwargs["pk"])

    def list(self, request):
        """
        Возвращает список учебных групп.
        """

        queryset = filter_study_groups_queryset(
            queryset=self.get_queryset(),
            params=request.query_params,
        )

        serializer = StudyGroupListSerializer(
            queryset,
            many=True,
            context={
                "request": request,
            },
        )

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Возвращает детальную карточку учебной группы.
        """

        group = self.get_object()

        serializer = StudyGroupDetailSerializer(
            group,
            context={
                "request": request,
            },
        )

        return Response(serializer.data)

    def create(self, request):
        """
        Создаёт учебную группу.
        """

        serializer = StudyGroupWriteSerializer(
            data=request.data,
            context={
                "is_create": True,
            },
        )
        serializer.is_valid(raise_exception=True)

        group = create_study_group(
            actor=request.user,
            organization=serializer.validated_data["organization"],
            data=serializer.validated_data,
        )

        output_serializer = StudyGroupDetailSerializer(
            group,
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
        Частично обновляет учебную группу.
        """

        group = self.get_object()

        serializer = StudyGroupWriteSerializer(
            data=request.data,
            partial=True,
            context={
                "is_create": False,
            },
        )
        serializer.is_valid(raise_exception=True)

        group = update_study_group(
            actor=request.user,
            group=group,
            data=serializer.validated_data,
        )

        output_serializer = StudyGroupDetailSerializer(
            group,
            context={
                "request": request,
            },
        )

        return Response(output_serializer.data)

    def destroy(self, request, pk=None):
        """
        Архивирует учебную группу вместо физического удаления.
        """

        group = self.get_object()

        group = archive_study_group(
            actor=request.user,
            group=group,
        )

        serializer = StudyGroupDetailSerializer(
            group,
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
        Восстанавливает учебную группу из архива.
        """

        group = self.get_object()

        group = restore_study_group(
            actor=request.user,
            group=group,
        )

        serializer = StudyGroupDetailSerializer(
            group,
            context={
                "request": request,
            },
        )

        return Response(serializer.data)

    @action(
        detail=True,
        methods=["post"],
        url_path="set-join-code",
        permission_classes=[CanManageOrganizationCodes],
    )
    def set_join_code(self, request, pk=None):
        """
        Устанавливает код вступления в группу.
        """

        group = self.get_object()

        serializer = GroupJoinCodeSetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        group, raw_code = set_group_join_code(
            actor=request.user,
            group=group,
            raw_code=serializer.validated_data.get("raw_code", ""),
            expires_at=serializer.validated_data.get("expires_at"),
        )

        output_serializer = GroupJoinCodeOutputSerializer(
            {
                "group": group,
                "raw_code": raw_code,
            },
            context={
                "request": request,
            },
        )

        return Response(output_serializer.data)

    @action(
        detail=True,
        methods=["post"],
        url_path="disable-join-code",
        permission_classes=[CanManageOrganizationCodes],
    )
    def disable_join_code(self, request, pk=None):
        """
        Отключает код вступления в группу.
        """

        group = self.get_object()

        group = disable_group_join_code(
            actor=request.user,
            group=group,
        )

        serializer = StudyGroupDetailSerializer(
            group,
            context={
                "request": request,
            },
        )

        return Response(serializer.data)

    @action(
        detail=True,
        methods=["post"],
        url_path="clear-join-code",
        permission_classes=[CanManageOrganizationCodes],
    )
    def clear_join_code(self, request, pk=None):
        """
        Очищает код вступления в группу.
        """

        group = self.get_object()

        group = clear_group_join_code(
            actor=request.user,
            group=group,
        )

        serializer = StudyGroupDetailSerializer(
            group,
            context={
                "request": request,
            },
        )

        return Response(serializer.data)
