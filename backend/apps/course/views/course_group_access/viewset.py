from __future__ import annotations

from apps.course.filters import CourseGroupAccessFilter
from apps.course.permissions import (
    CourseGroupAccessPermission,
    CourseGroupAccessVisibilityPermission,
)
from apps.course.selectors import course_group_access_detail_queryset
from apps.course.serializers import (
    CourseGroupAccessReadSerializer,
    CourseGroupAccessVisibilityActionSerializer,
    CourseGroupAccessWriteSerializer,
)
from apps.course.services import (
    archive_course_group_access,
    hide_course_for_group,
    show_course_for_group,
)
from apps.course.views.shared import (
    CourseReadWriteViewSetMixin,
    filter_queryset_by_available_courses,
)
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class CourseGroupAccessViewSet(CourseReadWriteViewSetMixin):
    """
    API группового доступа к курсам.
    """

    permission_classes = (CourseGroupAccessPermission,)
    filterset_class = CourseGroupAccessFilter
    read_serializer_class = CourseGroupAccessReadSerializer
    write_serializer_class = CourseGroupAccessWriteSerializer
    serializer_action_classes = {
        "show": CourseGroupAccessVisibilityActionSerializer,
        "hide": CourseGroupAccessVisibilityActionSerializer,
        "archive": CourseGroupAccessVisibilityActionSerializer,
    }

    def get_permissions(self):
        """
        Возвращает ограничения доступа под действие.
        """

        if self.action in {
            "show",
            "hide",
            "archive",
        }:
            return [CourseGroupAccessVisibilityPermission()]

        return super().get_permissions()

    def get_queryset(self):
        """
        Возвращает групповые доступы доступных курсов.
        """

        return filter_queryset_by_available_courses(
            queryset=course_group_access_detail_queryset(),
            user=self.request.user,
        )

    def destroy(self, request, *args, **kwargs) -> Response:
        """
        Вместо удаления архивирует групповой доступ.
        """

        group_access = self.get_object()
        archive_course_group_access(group_access=group_access)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=["post"],
        url_path="show",
    )
    def show(self, request, pk=None) -> Response:
        """
        Показывает курс группе.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        group_access = self.get_object()
        group_access = show_course_for_group(group_access=group_access)

        return self.build_read_response(group_access)

    @action(
        detail=True,
        methods=["post"],
        url_path="hide",
    )
    def hide(self, request, pk=None) -> Response:
        """
        Скрывает курс от группы.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        group_access = self.get_object()
        group_access = hide_course_for_group(group_access=group_access)

        return self.build_read_response(group_access)

    @action(
        detail=True,
        methods=["post"],
        url_path="archive",
    )
    def archive(self, request, pk=None) -> Response:
        """
        Архивирует групповой доступ.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        group_access = self.get_object()
        group_access = archive_course_group_access(group_access=group_access)

        return self.build_read_response(group_access)
