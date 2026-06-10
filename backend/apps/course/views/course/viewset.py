from __future__ import annotations

from apps.course.filters import CourseFilter
from apps.course.models import Course
from apps.course.permissions import (
    CourseCreateWithPlanPermission,
    CourseDuplicatePermission,
    CoursePermission,
    CourseStatusPermission,
)
from apps.course.selectors import get_user_available_courses
from apps.course.serializers import (
    CourseCreateWithPlanSerializer,
    CourseDuplicateActionSerializer,
    CourseReadSerializer,
    CourseStatusActionSerializer,
    CourseWriteSerializer,
)
from apps.course.services import (
    archive_course,
    create_course_with_plan,
    duplicate_course,
    publish_course,
    restore_course,
)
from apps.course.views.shared import CourseReadWriteViewSetMixin
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


class CourseViewSet(CourseReadWriteViewSetMixin):
    """
    API курсов.
    """

    permission_classes = (CoursePermission,)
    filterset_class = CourseFilter
    read_serializer_class = CourseReadSerializer
    write_serializer_class = CourseWriteSerializer
    serializer_action_classes = {
        "publish": CourseStatusActionSerializer,
        "archive": CourseStatusActionSerializer,
        "restore": CourseStatusActionSerializer,
        "duplicate": CourseDuplicateActionSerializer,
        "create_with_plan": CourseCreateWithPlanSerializer,
    }

    def get_permissions(self):
        """
        Возвращает ограничения доступа под действие.
        """

        if self.action in {
            "publish",
            "archive",
            "restore",
        }:
            return [CourseStatusPermission()]

        if self.action == "duplicate":
            return [CourseDuplicatePermission()]

        if self.action == "create_with_plan":
            return [CourseCreateWithPlanPermission()]

        return super().get_permissions()

    def get_queryset(self):
        """
        Возвращает курсы, доступные пользователю.
        """

        return get_user_available_courses(
            user=self.request.user,
            is_active=None,
        )

    def destroy(self, request, *args, **kwargs) -> Response:
        """
        Вместо физического удаления архивирует курс.
        """

        course = self.get_object()
        archive_course(course=course)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=["post"],
        url_path="publish",
    )
    def publish(self, request, pk=None) -> Response:
        """
        Публикует курс.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        course = self.get_object()
        course = publish_course(course=course)

        return self.build_read_response(course)

    @action(
        detail=True,
        methods=["post"],
        url_path="archive",
    )
    def archive(self, request, pk=None) -> Response:
        """
        Архивирует курс.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        course = self.get_object()
        course = archive_course(course=course)

        return self.build_read_response(course)

    @action(
        detail=True,
        methods=["post"],
        url_path="restore",
    )
    def restore(self, request, pk=None) -> Response:
        """
        Восстанавливает курс.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        course = self.get_object()
        course = restore_course(course=course)

        return self.build_read_response(course)

    @action(
        detail=True,
        methods=["post"],
        url_path="duplicate",
    )
    def duplicate(self, request, pk=None) -> Response:
        """
        Создаёт копию курса.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        course = self.get_object()

        duplicated_course = duplicate_course(
            course=course,
            owner_teacher=request.user,
            title=serializer.validated_data.get("title") or None,
            code=serializer.validated_data.get("code") or None,
            slug=serializer.validated_data.get("slug") or None,
            copy_material_links=serializer.validated_data.get(
                "copy_material_links",
                True,
            ),
        )

        return self.build_read_response(
            duplicated_course,
            response_status=status.HTTP_201_CREATED,
        )

    @action(
        detail=False,
        methods=["post"],
        url_path="create-with-plan",
    )
    def create_with_plan(self, request) -> Response:
        """
        Создаёт курс вместе с КТП.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        course = create_course_with_plan(
            course_data=serializer.validated_data["course"],
            plan_data=serializer.validated_data["plan"],
        )

        return self.build_read_response(
            course,
            response_status=status.HTTP_201_CREATED,
        )


class PublicCourseViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Публичный API курсов.
    """

    permission_classes = (AllowAny,)
    serializer_class = CourseReadSerializer
    filter_backends = CourseReadWriteViewSetMixin.filter_backends
    filterset_class = CourseFilter

    def get_queryset(self):
        """
        Возвращает публичные опубликованные курсы.
        """

        return Course.objects.select_related(
            "owner_teacher",
            "organization",
            "subject",
            "academic_year",
            "period",
        ).filter(
            is_active=True,
            status=Course.StatusChoices.PUBLISHED,
            visibility__in=[
                "public",
                "public_link",
            ],
        )
