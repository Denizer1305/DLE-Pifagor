from __future__ import annotations

from apps.course.filters import CourseSectionFilter
from apps.course.permissions import (
    CourseSectionPermission,
    CourseSectionStatusPermission,
)
from apps.course.selectors import course_section_detail_queryset
from apps.course.serializers import (
    CourseSectionReadSerializer,
    CourseSectionStatusActionSerializer,
    CourseSectionWriteSerializer,
)
from apps.course.services import archive_course_section, publish_course_section
from apps.course.views.shared import (
    CourseReadWriteViewSetMixin,
    filter_queryset_by_available_courses,
)
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class CourseSectionViewSet(CourseReadWriteViewSetMixin):
    """
    API разделов курса.
    """

    permission_classes = (CourseSectionPermission,)
    filterset_class = CourseSectionFilter
    read_serializer_class = CourseSectionReadSerializer
    write_serializer_class = CourseSectionWriteSerializer
    serializer_action_classes = {
        "publish": CourseSectionStatusActionSerializer,
        "archive": CourseSectionStatusActionSerializer,
    }

    def get_permissions(self):
        """
        Возвращает ограничения доступа под действие.
        """

        if self.action in {
            "publish",
            "archive",
        }:
            return [CourseSectionStatusPermission()]

        return super().get_permissions()

    def get_queryset(self):
        """
        Возвращает разделы доступных курсов.
        """

        return filter_queryset_by_available_courses(
            queryset=course_section_detail_queryset(),
            user=self.request.user,
        )

    def destroy(self, request, *args, **kwargs) -> Response:
        """
        Вместо удаления архивирует раздел.
        """

        section = self.get_object()
        archive_course_section(section=section)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=["post"],
        url_path="publish",
    )
    def publish(self, request, pk=None) -> Response:
        """
        Публикует раздел.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        section = self.get_object()
        section = publish_course_section(section=section)

        return self.build_read_response(section)

    @action(
        detail=True,
        methods=["post"],
        url_path="archive",
    )
    def archive(self, request, pk=None) -> Response:
        """
        Архивирует раздел.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        section = self.get_object()
        section = archive_course_section(section=section)

        return self.build_read_response(section)
