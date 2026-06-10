from __future__ import annotations

from apps.education.filters import GroupSubjectFilter
from apps.education.permissions import GroupSubjectPermission
from apps.education.selectors import (
    group_subject_detail_queryset,
    limit_queryset_by_user_groups,
)
from apps.education.serializers import (
    GroupSubjectReadSerializer,
    GroupSubjectWriteSerializer,
)
from apps.education.services import deactivate_group_subject, restore_group_subject
from apps.education.tasks import sync_group_subjects_from_curriculum
from apps.education.views.shared import EducationReadWriteViewSetMixin
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response


class SyncGroupSubjectsSerializer(serializers.Serializer):
    """
    Сериализатор синхронизации предметов группы из учебного плана.
    """

    curriculum_id = serializers.IntegerField(min_value=1)
    group_id = serializers.IntegerField(min_value=1)


class GroupSubjectViewSet(EducationReadWriteViewSetMixin):
    """
    Административный API предметов учебных групп.
    """

    permission_classes = (GroupSubjectPermission,)
    filterset_class = GroupSubjectFilter
    read_serializer_class = GroupSubjectReadSerializer
    write_serializer_class = GroupSubjectWriteSerializer

    def get_queryset(self):
        """
        Возвращает queryset предметов групп.
        """

        queryset = group_subject_detail_queryset()

        return limit_queryset_by_user_groups(
            queryset,
            self.request.user,
            group_field="group_id",
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="deactivate",
    )
    def deactivate(self, request, pk=None) -> Response:
        """
        Деактивирует предмет группы.
        """

        group_subject = self.get_object()
        group_subject = deactivate_group_subject(group_subject=group_subject)

        return self.build_read_response(group_subject)

    @action(
        detail=True,
        methods=["post"],
        url_path="restore",
    )
    def restore(self, request, pk=None) -> Response:
        """
        Восстанавливает предмет группы.
        """

        group_subject = self.get_object()
        group_subject = restore_group_subject(group_subject=group_subject)

        return self.build_read_response(group_subject)

    @action(
        detail=False,
        methods=["post"],
        url_path="sync-from-curriculum",
    )
    def sync_from_curriculum(self, request) -> Response:
        """
        Создаёт предметы группы по элементам учебного плана.
        """

        serializer = SyncGroupSubjectsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = sync_group_subjects_from_curriculum(
            curriculum_id=serializer.validated_data["curriculum_id"],
            group_id=serializer.validated_data["group_id"],
        )

        return Response(
            result,
            status=status.HTTP_200_OK,
        )
