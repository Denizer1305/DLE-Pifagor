from __future__ import annotations

from apps.education.filters import TeacherGroupSubjectFilter
from apps.education.permissions import TeacherGroupSubjectPermission
from apps.education.selectors import (
    get_user_available_group_ids,
    teacher_group_subject_detail_queryset,
    user_is_global_admin,
    user_is_learner,
    user_is_organization_admin,
    user_is_teacher,
)
from apps.education.serializers import (
    TeacherGroupSubjectReadSerializer,
    TeacherGroupSubjectWriteSerializer,
)
from apps.education.services import (
    deactivate_teacher_group_subject,
    restore_teacher_group_subject,
    set_primary_teacher_group_subject,
)
from apps.education.views.shared import EducationReadWriteViewSetMixin
from rest_framework.decorators import action
from rest_framework.response import Response


class TeacherGroupSubjectViewSet(EducationReadWriteViewSetMixin):
    """
    Административный API назначений преподавателей на предметы групп.
    """

    permission_classes = (TeacherGroupSubjectPermission,)
    filterset_class = TeacherGroupSubjectFilter
    read_serializer_class = TeacherGroupSubjectReadSerializer
    write_serializer_class = TeacherGroupSubjectWriteSerializer

    def get_queryset(self):
        """
        Возвращает queryset назначений преподавателей.
        """

        queryset = teacher_group_subject_detail_queryset()
        user = self.request.user

        if user_is_global_admin(user):
            return queryset

        if user_is_organization_admin(user):
            group_ids = get_user_available_group_ids(user)

            return queryset.filter(
                group_subject__group_id__in=group_ids,
            )

        if user_is_teacher(user):
            return queryset.filter(teacher=user)

        if user_is_learner(user):
            group_ids = get_user_available_group_ids(user)

            return queryset.filter(
                group_subject__group_id__in=group_ids,
            )

        return queryset.none()

    @action(
        detail=True,
        methods=["post"],
        url_path="set-primary",
    )
    def set_primary(self, request, pk=None) -> Response:
        """
        Делает назначение основным преподавателем предмета группы.
        """

        assignment = self.get_object()
        assignment = set_primary_teacher_group_subject(assignment=assignment)

        return self.build_read_response(assignment)

    @action(
        detail=True,
        methods=["post"],
        url_path="deactivate",
    )
    def deactivate(self, request, pk=None) -> Response:
        """
        Деактивирует назначение преподавателя.
        """

        assignment = self.get_object()
        assignment = deactivate_teacher_group_subject(assignment=assignment)

        return self.build_read_response(assignment)

    @action(
        detail=True,
        methods=["post"],
        url_path="restore",
    )
    def restore(self, request, pk=None) -> Response:
        """
        Восстанавливает назначение преподавателя.
        """

        assignment = self.get_object()
        assignment = restore_teacher_group_subject(assignment=assignment)

        return self.build_read_response(assignment)
