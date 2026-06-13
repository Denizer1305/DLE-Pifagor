from __future__ import annotations

from apps.testing.filters import TestAttemptFilter
from apps.testing.permissions import (
    TestAttemptLifecyclePermission,
    TestAttemptPermission,
    TestAttemptReviewPermission,
    is_learner,
    is_teacher,
    is_testing_admin,
)
from apps.testing.selectors import attempt_list_queryset, get_test_by_id
from apps.testing.serializers import (
    ConfirmAttemptResultSerializer,
    StartTestAttemptSerializer,
    SubmitTestAttemptSerializer,
    TestAttemptReadSerializer,
    TestAttemptWriteSerializer,
)
from apps.testing.services import (
    cancel_test_attempt,
    confirm_attempt_result,
    start_test_attempt,
    submit_test_attempt,
    update_test_attempt,
)
from apps.testing.tasks import (
    auto_check_attempt_task,
    build_attempt_integrity_report_task,
    publish_attempt_result_task,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


class TestAttemptViewSet(ModelViewSet):
    """
    ViewSet попыток прохождения теста.
    """

    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = TestAttemptFilter
    permission_classes = (TestAttemptPermission,)
    ordering_fields = (
        "id",
        "attempt_number",
        "status",
        "started_at",
        "submitted_at",
        "updated_at",
    )
    ordering = ("-created_at", "-id")
    http_method_names = ("get", "post", "patch", "delete", "head", "options")

    def get_queryset(self):
        """
        Возвращает попытки с ограничением по роли.
        """

        queryset = attempt_list_queryset()
        user = self.request.user

        if is_testing_admin(user=user):
            return queryset

        if is_teacher(user=user):
            return queryset.filter(test__owner_teacher_id=user.id)

        if is_learner(user=user):
            return queryset.filter(learner_id=user.id)

        return queryset.none()

    def get_serializer_class(self):
        """
        Возвращает serializer под действие.
        """

        if self.action in {"create", "update", "partial_update"}:
            return TestAttemptWriteSerializer

        if self.action == "start":
            return StartTestAttemptSerializer

        if self.action == "submit":
            return SubmitTestAttemptSerializer

        if self.action == "confirm_result":
            return ConfirmAttemptResultSerializer

        return TestAttemptReadSerializer

    def create(self, request, *args, **kwargs):
        """
        Создаёт попытку напрямую.
        """

        serializer = TestAttemptWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        from apps.testing.models import TestAttempt

        attempt = TestAttempt()
        attempt = update_test_attempt(
            attempt=attempt,
            data=serializer.validated_data,
        )

        return Response(
            TestAttemptReadSerializer(attempt).data,
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        """
        Полностью обновляет попытку.
        """

        return self._update_attempt(request=request, partial=False)

    def partial_update(self, request, *args, **kwargs):
        """
        Частично обновляет попытку.
        """

        return self._update_attempt(request=request, partial=True)

    def perform_destroy(self, instance) -> None:
        """
        Вместо удаления отменяет попытку.
        """

        cancel_test_attempt(attempt=instance)

    @action(
        detail=False,
        methods=("post",),
        permission_classes=(TestAttemptLifecyclePermission,),
    )
    def start(self, request):
        """
        Начинает новую попытку прохождения теста.
        """

        serializer = StartTestAttemptSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        test = get_test_by_id(serializer.validated_data["test_id"])
        attempt = start_test_attempt(test=test, learner=request.user)

        return Response(
            TestAttemptReadSerializer(attempt).data,
            status=status.HTTP_201_CREATED,
        )

    @action(
        detail=True,
        methods=("post",),
        permission_classes=(TestAttemptLifecyclePermission,),
    )
    def submit(self, request, pk=None):
        """
        Отправляет попытку и запускает автопроверку.
        """

        serializer = SubmitTestAttemptSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        attempt = submit_test_attempt(attempt=self.get_object())
        attempt = auto_check_attempt_task(attempt_id=attempt.id)

        return Response(TestAttemptReadSerializer(attempt).data)

    @action(
        detail=True,
        methods=("post",),
        permission_classes=(TestAttemptReviewPermission,),
        url_path="confirm-result",
    )
    def confirm_result(self, request, pk=None):
        """
        Подтверждает итоговую оценку преподавателем.
        """

        serializer = ConfirmAttemptResultSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        attempt = confirm_attempt_result(
            attempt=self.get_object(),
            reviewer_teacher=request.user,
            **serializer.validated_data,
        )

        return Response(TestAttemptReadSerializer(attempt).data)

    @action(
        detail=True,
        methods=("post",),
        permission_classes=(TestAttemptReviewPermission,),
        url_path="publish-result",
    )
    def publish_result(self, request, pk=None):
        """
        Публикует подтверждённый результат ученику и родителю.
        """

        attempt = publish_attempt_result_task(attempt_id=self.get_object().id)

        return Response(TestAttemptReadSerializer(attempt).data)

    @action(
        detail=True,
        methods=("get",),
        permission_classes=(TestAttemptReviewPermission,),
        url_path="integrity-report",
    )
    def integrity_report(self, request, pk=None):
        """
        Возвращает отчёт о признаках возможного списывания.
        """

        report = build_attempt_integrity_report_task(
            attempt_id=self.get_object().id,
        )
        report.setdefault("flags", report.get("flags_data", []))

        return Response(report)

    def _update_attempt(self, *, request, partial: bool):
        """
        Общая логика обновления попытки.
        """

        attempt = self.get_object()
        serializer = TestAttemptWriteSerializer(
            attempt,
            data=request.data,
            partial=partial,
        )
        serializer.is_valid(raise_exception=True)

        attempt = update_test_attempt(
            attempt=attempt,
            data=serializer.validated_data,
        )

        return Response(TestAttemptReadSerializer(attempt).data)
