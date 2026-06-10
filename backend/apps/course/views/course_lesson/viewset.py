from __future__ import annotations

from apps.course.filters import CourseLessonFilter
from apps.course.permissions import CourseLessonPermission, CourseLessonStatusPermission
from apps.course.selectors import course_lesson_detail_queryset
from apps.course.serializers import (
    CourseLessonReadSerializer,
    CourseLessonStatusActionSerializer,
    CourseLessonWriteSerializer,
)
from apps.course.services import archive_course_lesson, publish_course_lesson
from apps.course.views.shared import (
    CourseReadWriteViewSetMixin,
    filter_queryset_by_available_courses,
)
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class CourseLessonViewSet(CourseReadWriteViewSetMixin):
    """
    API уроков курса.
    """

    permission_classes = (CourseLessonPermission,)
    filterset_class = CourseLessonFilter
    read_serializer_class = CourseLessonReadSerializer
    write_serializer_class = CourseLessonWriteSerializer
    serializer_action_classes = {
        "publish": CourseLessonStatusActionSerializer,
        "archive": CourseLessonStatusActionSerializer,
    }

    def get_permissions(self):
        """
        Возвращает ограничения доступа под действие.
        """

        if self.action in {
            "publish",
            "archive",
        }:
            return [CourseLessonStatusPermission()]

        return super().get_permissions()

    def get_queryset(self):
        """
        Возвращает уроки доступных курсов.
        """

        return filter_queryset_by_available_courses(
            queryset=course_lesson_detail_queryset(),
            user=self.request.user,
        )

    def destroy(self, request, *args, **kwargs) -> Response:
        """
        Вместо удаления архивирует урок.
        """

        lesson = self.get_object()
        archive_course_lesson(lesson=lesson)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=["post"],
        url_path="publish",
    )
    def publish(self, request, pk=None) -> Response:
        """
        Публикует урок.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        lesson = self.get_object()
        lesson = publish_course_lesson(lesson=lesson)

        return self.build_read_response(lesson)

    @action(
        detail=True,
        methods=["post"],
        url_path="archive",
    )
    def archive(self, request, pk=None) -> Response:
        """
        Архивирует урок.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        lesson = self.get_object()
        lesson = archive_course_lesson(lesson=lesson)

        return self.build_read_response(lesson)
