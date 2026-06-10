from __future__ import annotations

from apps.course.filters import LessonProgressFilter
from apps.course.models import CourseEnrollment, CourseLesson
from apps.course.permissions import (
    LessonProgressPermission,
    LessonProgressStatusPermission,
)
from apps.course.selectors import lesson_progress_detail_queryset
from apps.course.serializers import (
    LessonProgressReadSerializer,
    LessonProgressStatusActionSerializer,
    LessonProgressTrackActionSerializer,
    LessonProgressWriteSerializer,
)
from apps.course.services import (
    complete_lesson_progress,
    reset_lesson_progress,
    start_lesson_progress,
    track_lesson_completed,
    track_lesson_opened,
)
from apps.course.views.shared import (
    CourseReadWriteViewSetMixin,
    filter_queryset_by_available_courses,
)
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class LessonProgressViewSet(CourseReadWriteViewSetMixin):
    """
    API прогресса уроков.
    """

    permission_classes = (LessonProgressPermission,)
    filterset_class = LessonProgressFilter
    read_serializer_class = LessonProgressReadSerializer
    write_serializer_class = LessonProgressWriteSerializer
    serializer_action_classes = {
        "start": LessonProgressStatusActionSerializer,
        "complete": LessonProgressStatusActionSerializer,
        "reset": LessonProgressStatusActionSerializer,
        "track_opened": LessonProgressTrackActionSerializer,
        "track_completed": LessonProgressTrackActionSerializer,
    }

    def get_permissions(self):
        """
        Возвращает ограничения доступа под действие.
        """

        if self.action in {
            "start",
            "complete",
            "reset",
            "track_opened",
            "track_completed",
        }:
            return [LessonProgressStatusPermission()]

        return super().get_permissions()

    def get_queryset(self):
        """
        Возвращает прогресс уроков доступных курсов.
        """

        return filter_queryset_by_available_courses(
            queryset=lesson_progress_detail_queryset(),
            user=self.request.user,
            course_field_path="enrollment__course",
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="start",
    )
    def start(self, request, pk=None) -> Response:
        """
        Запускает прогресс урока.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        progress = self.get_object()
        progress = start_lesson_progress(lesson_progress=progress)

        return self.build_read_response(progress)

    @action(
        detail=True,
        methods=["post"],
        url_path="complete",
    )
    def complete(self, request, pk=None) -> Response:
        """
        Завершает прогресс урока.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        progress = self.get_object()
        progress = complete_lesson_progress(lesson_progress=progress)

        return self.build_read_response(progress)

    @action(
        detail=True,
        methods=["post"],
        url_path="reset",
    )
    def reset(self, request, pk=None) -> Response:
        """
        Сбрасывает прогресс урока.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        progress = self.get_object()
        progress = reset_lesson_progress(lesson_progress=progress)

        return self.build_read_response(progress)

    @action(
        detail=False,
        methods=["post"],
        url_path="track-opened",
    )
    def track_opened(self, request) -> Response:
        """
        Фиксирует открытие урока.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = track_lesson_opened(
            enrollment=CourseEnrollment.objects.get(
                id=serializer.validated_data["enrollment_id"],
            ),
            lesson=CourseLesson.objects.get(
                id=serializer.validated_data["lesson_id"],
            ),
        )

        read_serializer = self.read_serializer_class(
            result["lesson_progress"],
            context=self.get_serializer_context(),
        )

        return Response(
            read_serializer.data,
            status=status.HTTP_200_OK,
        )

    @action(
        detail=False,
        methods=["post"],
        url_path="track-completed",
    )
    def track_completed(self, request) -> Response:
        """
        Фиксирует завершение урока.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = track_lesson_completed(
            enrollment=CourseEnrollment.objects.get(
                id=serializer.validated_data["enrollment_id"],
            ),
            lesson=CourseLesson.objects.get(
                id=serializer.validated_data["lesson_id"],
            ),
        )

        read_serializer = self.read_serializer_class(
            result["lesson_progress"],
            context=self.get_serializer_context(),
        )

        return Response(
            read_serializer.data,
            status=status.HTTP_200_OK,
        )
