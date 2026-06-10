from __future__ import annotations

from apps.course.filters import CoursePlanFilter
from apps.course.permissions import CoursePlanPermission, CoursePlanStatusPermission
from apps.course.selectors import course_plan_detail_queryset
from apps.course.serializers import (
    CoursePlanReadSerializer,
    CoursePlanStatusActionSerializer,
    CoursePlanWriteSerializer,
)
from apps.course.services import (
    approve_course_plan,
    archive_course_plan,
    mark_course_plan_reviewed,
)
from apps.course.views.shared import (
    CourseReadWriteViewSetMixin,
    filter_queryset_by_available_courses,
)
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class CoursePlanViewSet(CourseReadWriteViewSetMixin):
    """
    API КТП курса.
    """

    permission_classes = (CoursePlanPermission,)
    filterset_class = CoursePlanFilter
    read_serializer_class = CoursePlanReadSerializer
    write_serializer_class = CoursePlanWriteSerializer
    serializer_action_classes = {
        "review": CoursePlanStatusActionSerializer,
        "approve": CoursePlanStatusActionSerializer,
        "archive": CoursePlanStatusActionSerializer,
    }

    def get_permissions(self):
        """
        Возвращает ограничения доступа под действие.
        """

        if self.action in {
            "review",
            "approve",
            "archive",
        }:
            return [CoursePlanStatusPermission()]

        return super().get_permissions()

    def get_queryset(self):
        """
        Возвращает КТП доступных курсов.
        """

        return filter_queryset_by_available_courses(
            queryset=course_plan_detail_queryset(),
            user=self.request.user,
        )

    def destroy(self, request, *args, **kwargs) -> Response:
        """
        Вместо удаления архивирует КТП.
        """

        plan = self.get_object()
        archive_course_plan(plan=plan)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=["post"],
        url_path="review",
    )
    def review(self, request, pk=None) -> Response:
        """
        Помечает КТП как проверенный.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        plan = self.get_object()
        plan = mark_course_plan_reviewed(plan=plan)

        return self.build_read_response(plan)

    @action(
        detail=True,
        methods=["post"],
        url_path="approve",
    )
    def approve(self, request, pk=None) -> Response:
        """
        Утверждает КТП.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        plan = self.get_object()
        plan = approve_course_plan(plan=plan)

        return self.build_read_response(plan)

    @action(
        detail=True,
        methods=["post"],
        url_path="archive",
    )
    def archive(self, request, pk=None) -> Response:
        """
        Архивирует КТП.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        plan = self.get_object()
        plan = archive_course_plan(plan=plan)

        return self.build_read_response(plan)
