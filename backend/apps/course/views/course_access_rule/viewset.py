from __future__ import annotations

from apps.course.filters import CourseAccessRuleFilter
from apps.course.permissions import (
    CourseAccessRulePermission,
    CourseAccessRuleStatusPermission,
)
from apps.course.selectors import course_access_rule_detail_queryset
from apps.course.serializers import (
    CourseAccessRuleReadSerializer,
    CourseAccessRuleStatusActionSerializer,
    CourseAccessRuleWriteSerializer,
)
from apps.course.services import (
    deactivate_course_access_rule,
    restore_course_access_rule,
)
from apps.course.views.shared import (
    CourseReadWriteViewSetMixin,
    filter_queryset_by_available_courses,
)
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class CourseAccessRuleViewSet(CourseReadWriteViewSetMixin):
    """
    API правил доступа к курсам.
    """

    permission_classes = (CourseAccessRulePermission,)
    filterset_class = CourseAccessRuleFilter
    read_serializer_class = CourseAccessRuleReadSerializer
    write_serializer_class = CourseAccessRuleWriteSerializer
    serializer_action_classes = {
        "deactivate": CourseAccessRuleStatusActionSerializer,
        "restore": CourseAccessRuleStatusActionSerializer,
    }

    def get_permissions(self):
        """
        Возвращает ограничения доступа под действие.
        """

        if self.action in {
            "deactivate",
            "restore",
        }:
            return [CourseAccessRuleStatusPermission()]

        return super().get_permissions()

    def get_queryset(self):
        """
        Возвращает правила доступа доступных курсов.
        """

        return filter_queryset_by_available_courses(
            queryset=course_access_rule_detail_queryset(),
            user=self.request.user,
        )

    def destroy(self, request, *args, **kwargs) -> Response:
        """
        Вместо удаления деактивирует правило доступа.
        """

        access_rule = self.get_object()
        deactivate_course_access_rule(access_rule=access_rule)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=["post"],
        url_path="deactivate",
    )
    def deactivate(self, request, pk=None) -> Response:
        """
        Деактивирует правило доступа.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        access_rule = self.get_object()
        access_rule = deactivate_course_access_rule(access_rule=access_rule)

        return self.build_read_response(access_rule)

    @action(
        detail=True,
        methods=["post"],
        url_path="restore",
    )
    def restore(self, request, pk=None) -> Response:
        """
        Восстанавливает правило доступа.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        access_rule = self.get_object()
        access_rule = restore_course_access_rule(access_rule=access_rule)

        return self.build_read_response(access_rule)
