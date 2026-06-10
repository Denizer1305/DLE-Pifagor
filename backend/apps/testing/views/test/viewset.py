from __future__ import annotations

from apps.course.models import CourseEnrollment
from apps.testing.constants import TestStatus
from apps.testing.filters import TestFilter
from apps.testing.permissions import (
    TestPermission,
    TestStatusPermission,
    is_learner,
    is_teacher,
    is_testing_admin,
)
from apps.testing.selectors import test_list_queryset
from apps.testing.serializers import (
    TestReadSerializer,
    TestStatusActionSerializer,
    TestWriteSerializer,
)
from apps.testing.services import (
    archive_test,
    create_test,
    publish_test,
    restore_test,
    update_test,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


class TestViewSet(ModelViewSet):
    """
    ViewSet тестов.

    Используется в admin/teacher/learner пространствах.
    QuerySet дополнительно ограничивается по роли пользователя.
    """

    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
    )
    filterset_class = TestFilter
    permission_classes = (TestPermission,)
    ordering_fields = (
        "id",
        "title",
        "status",
        "published_at",
        "created_at",
        "updated_at",
    )
    ordering = ("-updated_at", "-id")
    http_method_names = (
        "get",
        "post",
        "patch",
        "delete",
        "head",
        "options",
    )

    def get_queryset(self):
        """
        Возвращает тесты с учётом роли пользователя.
        """

        queryset = test_list_queryset()
        user = self.request.user

        if is_testing_admin(user=user):
            return queryset

        if is_teacher(user=user):
            return queryset.filter(owner_teacher_id=user.id)

        if is_learner(user=user):
            course_ids = CourseEnrollment.objects.filter(
                learner_id=user.id,
            ).values_list(
                "course_id",
                flat=True,
            )

            return queryset.filter(
                course_id__in=course_ids,
                status=TestStatus.PUBLISHED,
                is_active=True,
            )

        return queryset.none()

    def get_serializer_class(self):
        """
        Возвращает serializer под действие.
        """

        if self.action in {
            "create",
            "update",
            "partial_update",
        }:
            return TestWriteSerializer

        if self.action in {
            "publish",
            "archive",
            "restore",
        }:
            return TestStatusActionSerializer

        return TestReadSerializer

    def create(self, request, *args, **kwargs):
        """
        Создаёт тест через сервисный слой.
        """

        serializer = TestWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        test = create_test(data=serializer.validated_data)

        return Response(
            TestReadSerializer(test).data,
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        """
        Полностью обновляет тест через сервисный слой.
        """

        return self._update_test(
            request=request,
            partial=False,
        )

    def partial_update(self, request, *args, **kwargs):
        """
        Частично обновляет тест через сервисный слой.
        """

        return self._update_test(
            request=request,
            partial=True,
        )

    def perform_destroy(self, instance) -> None:
        """
        Вместо физического удаления архивирует тест.
        """

        archive_test(test=instance)

    @action(
        detail=True,
        methods=("post",),
        permission_classes=(TestStatusPermission,),
    )
    def publish(self, request, pk=None):
        """
        Публикует тест.
        """

        test = publish_test(test=self.get_object())

        return Response(TestReadSerializer(test).data)

    @action(
        detail=True,
        methods=("post",),
        permission_classes=(TestStatusPermission,),
    )
    def archive(self, request, pk=None):
        """
        Архивирует тест.
        """

        test = archive_test(test=self.get_object())

        return Response(TestReadSerializer(test).data)

    @action(
        detail=True,
        methods=("post",),
        permission_classes=(TestStatusPermission,),
    )
    def restore(self, request, pk=None):
        """
        Восстанавливает тест в черновик.
        """

        test = restore_test(test=self.get_object())

        return Response(TestReadSerializer(test).data)

    def _update_test(
        self,
        *,
        request,
        partial: bool,
    ):
        """
        Общая логика обновления теста.
        """

        test = self.get_object()
        serializer = TestWriteSerializer(
            test,
            data=request.data,
            partial=partial,
        )
        serializer.is_valid(raise_exception=True)

        test = update_test(
            test=test,
            data=serializer.validated_data,
        )

        return Response(TestReadSerializer(test).data)
