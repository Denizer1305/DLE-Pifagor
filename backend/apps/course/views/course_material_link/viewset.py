from __future__ import annotations

from apps.course.permissions import (
    CourseMaterialLinkPermission,
    CourseMaterialLinkVisibilityPermission,
)
from apps.course.selectors import course_material_link_detail_queryset
from apps.course.serializers import (
    CourseMaterialLinkReadSerializer,
    CourseMaterialLinkVisibilityActionSerializer,
    CourseMaterialLinkWriteSerializer,
)
from apps.course.services import hide_course_material_link, show_course_material_link
from apps.course.views.shared import (
    CourseReadWriteViewSetMixin,
    filter_queryset_by_available_courses,
)
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class CourseMaterialLinkViewSet(CourseReadWriteViewSetMixin):
    """
    API связей курса с материалами.
    """

    permission_classes = (CourseMaterialLinkPermission,)
    filterset_fields = (
        "course_id",
        "section_id",
        "lesson_id",
        "material_id",
        "placement",
        "is_required",
        "is_visible",
    )
    read_serializer_class = CourseMaterialLinkReadSerializer
    write_serializer_class = CourseMaterialLinkWriteSerializer
    serializer_action_classes = {
        "show": CourseMaterialLinkVisibilityActionSerializer,
        "hide": CourseMaterialLinkVisibilityActionSerializer,
    }

    def get_permissions(self):
        """
        Возвращает ограничения доступа под действие.
        """

        if self.action in {
            "show",
            "hide",
        }:
            return [CourseMaterialLinkVisibilityPermission()]

        return super().get_permissions()

    def get_queryset(self):
        """
        Возвращает связи с материалами доступных курсов.
        """

        return filter_queryset_by_available_courses(
            queryset=course_material_link_detail_queryset(),
            user=self.request.user,
        )

    def destroy(self, request, *args, **kwargs) -> Response:
        """
        Вместо удаления скрывает материал курса.
        """

        link = self.get_object()
        hide_course_material_link(link=link)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=["post"],
        url_path="show",
    )
    def show(self, request, pk=None) -> Response:
        """
        Показывает материал курса.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        link = self.get_object()
        link = show_course_material_link(link=link)

        return self.build_read_response(link)

    @action(
        detail=True,
        methods=["post"],
        url_path="hide",
    )
    def hide(self, request, pk=None) -> Response:
        """
        Скрывает материал курса.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        link = self.get_object()
        link = hide_course_material_link(link=link)

        return self.build_read_response(link)
