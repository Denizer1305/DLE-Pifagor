from __future__ import annotations

from apps.course.filters import CourseEnrollmentFilter
from apps.course.permissions import (
    CourseEnrollmentPermission,
    CourseEnrollmentStatusPermission,
)
from apps.course.selectors import course_enrollment_detail_queryset
from apps.course.serializers import (
    CourseEnrollmentReadSerializer,
    CourseEnrollmentStatusActionSerializer,
    CourseEnrollmentWriteSerializer,
)
from apps.course.services import (
    archive_course_enrollment,
    cancel_course_enrollment,
    complete_course_enrollment,
    start_course_enrollment,
)
from apps.course.views.shared import (
    CourseReadWriteViewSetMixin,
    filter_queryset_by_available_courses,
)
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class CourseEnrollmentViewSet(CourseReadWriteViewSetMixin):
    """
    API записей на курс.
    """

    permission_classes = (CourseEnrollmentPermission,)
    filterset_class = CourseEnrollmentFilter
    read_serializer_class = CourseEnrollmentReadSerializer
    write_serializer_class = CourseEnrollmentWriteSerializer
    serializer_action_classes = {
        "start": CourseEnrollmentStatusActionSerializer,
        "complete": CourseEnrollmentStatusActionSerializer,
        "cancel": CourseEnrollmentStatusActionSerializer,
        "archive": CourseEnrollmentStatusActionSerializer,
    }

    def get_permissions(self):
        """
        Возвращает ограничения доступа под действие.
        """

        if self.action in {
            "start",
            "complete",
            "cancel",
            "archive",
        }:
            return [CourseEnrollmentStatusPermission()]

        return super().get_permissions()

    def get_queryset(self):
        """
        Возвращает записи на доступные курсы.
        """

        return filter_queryset_by_available_courses(
            queryset=course_enrollment_detail_queryset(),
            user=self.request.user,
        )

    def destroy(self, request, *args, **kwargs) -> Response:
        """
        Вместо удаления архивирует запись.
        """

        enrollment = self.get_object()
        archive_course_enrollment(enrollment=enrollment)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=["post"],
        url_path="start",
    )
    def start(self, request, pk=None) -> Response:
        """
        Запускает прохождение курса.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        enrollment = self.get_object()
        enrollment = start_course_enrollment(enrollment=enrollment)

        return self.build_read_response(enrollment)

    @action(
        detail=True,
        methods=["post"],
        url_path="complete",
    )
    def complete(self, request, pk=None) -> Response:
        """
        Завершает прохождение курса.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        enrollment = self.get_object()
        enrollment = complete_course_enrollment(enrollment=enrollment)

        return self.build_read_response(enrollment)

    @action(
        detail=True,
        methods=["post"],
        url_path="cancel",
    )
    def cancel(self, request, pk=None) -> Response:
        """
        Отменяет запись на курс.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        enrollment = self.get_object()
        enrollment = cancel_course_enrollment(enrollment=enrollment)

        return self.build_read_response(enrollment)

    @action(
        detail=True,
        methods=["post"],
        url_path="archive",
    )
    def archive(self, request, pk=None) -> Response:
        """
        Архивирует запись на курс.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        enrollment = self.get_object()
        enrollment = archive_course_enrollment(enrollment=enrollment)

        return self.build_read_response(enrollment)
