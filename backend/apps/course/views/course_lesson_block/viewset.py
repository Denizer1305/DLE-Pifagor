from __future__ import annotations

from apps.course.permissions import (
    CourseLessonBlockPermission,
    CourseLessonBlockVisibilityPermission,
)
from apps.course.selectors import course_lesson_block_detail_queryset
from apps.course.serializers import (
    CourseLessonBlockReadSerializer,
    CourseLessonBlockVisibilityActionSerializer,
    CourseLessonBlockWriteSerializer,
)
from apps.course.services import hide_course_lesson_block, show_course_lesson_block
from apps.course.views.shared import (
    CourseReadWriteViewSetMixin,
    filter_queryset_by_available_courses,
)
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class CourseLessonBlockViewSet(CourseReadWriteViewSetMixin):
    """
    API блоков урока.
    """

    permission_classes = (CourseLessonBlockPermission,)
    filterset_fields = (
        "lesson_id",
        "block_type",
        "material_id",
        "is_visible",
    )
    read_serializer_class = CourseLessonBlockReadSerializer
    write_serializer_class = CourseLessonBlockWriteSerializer
    serializer_action_classes = {
        "show": CourseLessonBlockVisibilityActionSerializer,
        "hide": CourseLessonBlockVisibilityActionSerializer,
    }

    def get_permissions(self):
        """
        Возвращает ограничения доступа под действие.
        """

        if self.action in {
            "show",
            "hide",
        }:
            return [CourseLessonBlockVisibilityPermission()]

        return super().get_permissions()

    def get_queryset(self):
        """
        Возвращает блоки уроков доступных курсов.
        """

        return filter_queryset_by_available_courses(
            queryset=course_lesson_block_detail_queryset(),
            user=self.request.user,
            course_field_path="lesson__course",
        )

    def destroy(self, request, *args, **kwargs) -> Response:
        """
        Вместо удаления скрывает блок урока.
        """

        block = self.get_object()
        hide_course_lesson_block(block=block)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=["post"],
        url_path="show",
    )
    def show(self, request, pk=None) -> Response:
        """
        Показывает блок урока.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        block = self.get_object()
        block = show_course_lesson_block(block=block)

        return self.build_read_response(block)

    @action(
        detail=True,
        methods=["post"],
        url_path="hide",
    )
    def hide(self, request, pk=None) -> Response:
        """
        Скрывает блок урока.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        block = self.get_object()
        block = hide_course_lesson_block(block=block)

        return self.build_read_response(block)
