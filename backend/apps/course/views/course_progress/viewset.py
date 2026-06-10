from __future__ import annotations

from apps.course.filters import CourseProgressFilter
from apps.course.permissions import (
    CourseProgressPermission,
    CourseProgressRecalculatePermission,
)
from apps.course.selectors import course_progress_detail_queryset
from apps.course.serializers import (
    CourseProgressEnsureActionSerializer,
    CourseProgressReadSerializer,
    CourseProgressRecalculateActionSerializer,
    CourseProgressWriteSerializer,
)
from apps.course.services import ensure_course_progress, recalculate_course_progress
from apps.course.views.shared import (
    CourseReadWriteViewSetMixin,
    filter_queryset_by_available_courses,
)
from rest_framework.decorators import action


class CourseProgressViewSet(CourseReadWriteViewSetMixin):
    """
    API общего прогресса курса.
    """

    permission_classes = (CourseProgressPermission,)
    filterset_class = CourseProgressFilter
    read_serializer_class = CourseProgressReadSerializer
    write_serializer_class = CourseProgressWriteSerializer
    serializer_action_classes = {
        "ensure": CourseProgressEnsureActionSerializer,
        "recalculate": CourseProgressRecalculateActionSerializer,
    }

    def get_permissions(self):
        """
        Возвращает ограничения доступа под действие.
        """

        if self.action in {
            "ensure",
            "recalculate",
        }:
            return [CourseProgressRecalculatePermission()]

        return super().get_permissions()

    def get_queryset(self):
        """
        Возвращает прогресс доступных курсов.
        """

        return filter_queryset_by_available_courses(
            queryset=course_progress_detail_queryset(),
            user=self.request.user,
            course_field_path="enrollment__course",
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="ensure",
    )
    def ensure(self, request, pk=None):
        """
        Гарантирует наличие прогресса курса.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        progress = self.get_object()
        progress = ensure_course_progress(enrollment=progress.enrollment)

        return self.build_read_response(progress)

    @action(
        detail=True,
        methods=["post"],
        url_path="recalculate",
    )
    def recalculate(self, request, pk=None):
        """
        Пересчитывает прогресс курса.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        progress = self.get_object()
        progress = recalculate_course_progress(enrollment=progress.enrollment)

        return self.build_read_response(progress)
