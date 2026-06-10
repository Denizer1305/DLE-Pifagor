from __future__ import annotations

from apps.course.filters import CoursePlanImportFilter
from apps.course.permissions import (
    CoursePlanImportPermission,
    CoursePlanImportStatusPermission,
)
from apps.course.selectors import course_plan_import_detail_queryset
from apps.course.serializers import (
    CoursePlanImportReadSerializer,
    CoursePlanImportStatusActionSerializer,
    CoursePlanImportWriteSerializer,
)
from apps.course.services import (
    mark_course_plan_import_applied,
    mark_course_plan_import_failed,
    mark_course_plan_import_parsed,
)
from apps.course.views.shared import (
    CourseReadWriteViewSetMixin,
    filter_queryset_by_available_courses,
)
from rest_framework.decorators import action


class CoursePlanImportViewSet(CourseReadWriteViewSetMixin):
    """
    API импортов КТП.
    """

    permission_classes = (CoursePlanImportPermission,)
    filterset_class = CoursePlanImportFilter
    read_serializer_class = CoursePlanImportReadSerializer
    write_serializer_class = CoursePlanImportWriteSerializer
    serializer_action_classes = {
        "mark_parsed": CoursePlanImportStatusActionSerializer,
        "mark_failed": CoursePlanImportStatusActionSerializer,
        "mark_applied": CoursePlanImportStatusActionSerializer,
    }

    def get_permissions(self):
        """
        Возвращает ограничения доступа под действие.
        """

        if self.action in {
            "mark_parsed",
            "mark_failed",
            "mark_applied",
        }:
            return [CoursePlanImportStatusPermission()]

        return super().get_permissions()

    def get_queryset(self):
        """
        Возвращает импорты КТП доступных курсов.
        """

        return filter_queryset_by_available_courses(
            queryset=course_plan_import_detail_queryset(),
            user=self.request.user,
            course_field_path="course_plan__course",
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="mark-parsed",
    )
    def mark_parsed(self, request, pk=None):
        """
        Помечает импорт как разобранный.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        plan_import = self.get_object()
        plan_import = mark_course_plan_import_parsed(
            plan_import=plan_import,
            parsed_payload=serializer.validated_data.get("parsed_payload", {}),
            parser_version=serializer.validated_data.get("parser_version", ""),
        )

        return self.build_read_response(plan_import)

    @action(
        detail=True,
        methods=["post"],
        url_path="mark-failed",
    )
    def mark_failed(self, request, pk=None):
        """
        Помечает импорт как ошибочный.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        plan_import = self.get_object()
        plan_import = mark_course_plan_import_failed(
            plan_import=plan_import,
            errors=serializer.validated_data.get("errors", []),
        )

        return self.build_read_response(plan_import)

    @action(
        detail=True,
        methods=["post"],
        url_path="mark-applied",
    )
    def mark_applied(self, request, pk=None):
        """
        Помечает импорт как применённый.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        plan_import = self.get_object()
        plan_import = mark_course_plan_import_applied(
            plan_import=plan_import,
        )

        return self.build_read_response(plan_import)
