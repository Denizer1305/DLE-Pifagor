from __future__ import annotations

from apps.organizations.filters import filter_group_curators_queryset
from apps.organizations.models import GroupCurator
from apps.organizations.permissions import CanManageGroupCurators
from apps.organizations.selectors import get_group_curators_base_queryset
from apps.organizations.serializers import (
    GroupCuratorDetailSerializer,
    GroupCuratorListSerializer,
    GroupCuratorWriteSerializer,
)
from apps.organizations.services import (
    assign_group_curator,
    remove_group_curator,
    set_primary_group_curator,
    update_group_curator,
)
from apps.organizations.selectors import get_admin_group_curators_queryset_for_actor
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class AdminGroupCuratorViewSet(viewsets.ViewSet):
    """
    Административное управление кураторами учебных групп.
    """

    permission_classes = [CanManageGroupCurators]

    def get_queryset(self):
        """
        Возвращает кураторов групп, доступных текущему пользователю.
        """

        return get_admin_group_curators_queryset_for_actor(
            actor=self.request.user,
        )

    def get_object(self) -> GroupCurator:
        """
        Возвращает связь куратора с группой.
        """

        return self.get_queryset().get(pk=self.kwargs["pk"])

    def list(self, request):
        """
        Возвращает список кураторов групп.
        """

        queryset = filter_group_curators_queryset(
            queryset=self.get_queryset(),
            params=request.query_params,
        )

        serializer = GroupCuratorListSerializer(
            queryset,
            many=True,
            context={
                "request": request,
            },
        )

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Возвращает детальную карточку куратора группы.
        """

        group_curator = self.get_object()

        serializer = GroupCuratorDetailSerializer(
            group_curator,
            context={
                "request": request,
            },
        )

        return Response(serializer.data)

    def create(self, request):
        """
        Назначает куратора учебной группы.
        """

        serializer = GroupCuratorWriteSerializer(
            data=request.data,
            context={
                "is_create": True,
            },
        )
        serializer.is_valid(raise_exception=True)

        group_curator = assign_group_curator(
            actor=request.user,
            group=serializer.validated_data["group"],
            teacher=serializer.validated_data["teacher"],
            data=serializer.validated_data,
        )

        output_serializer = GroupCuratorDetailSerializer(
            group_curator,
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
        Частично обновляет связь куратора с группой.
        """

        group_curator = self.get_object()

        serializer = GroupCuratorWriteSerializer(
            data=request.data,
            partial=True,
            context={
                "is_create": False,
            },
        )
        serializer.is_valid(raise_exception=True)

        group_curator = update_group_curator(
            actor=request.user,
            group_curator=group_curator,
            data=serializer.validated_data,
        )

        output_serializer = GroupCuratorDetailSerializer(
            group_curator,
            context={
                "request": request,
            },
        )

        return Response(output_serializer.data)

    def destroy(self, request, pk=None):
        """
        Деактивирует куратора группы.
        """

        group_curator = self.get_object()

        group_curator = remove_group_curator(
            actor=request.user,
            group_curator=group_curator,
        )

        serializer = GroupCuratorDetailSerializer(
            group_curator,
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
        Делает куратора основным для группы.
        """

        group_curator = self.get_object()

        group_curator = set_primary_group_curator(
            actor=request.user,
            group_curator=group_curator,
        )

        serializer = GroupCuratorDetailSerializer(
            group_curator,
            context={
                "request": request,
            },
        )

        return Response(serializer.data)