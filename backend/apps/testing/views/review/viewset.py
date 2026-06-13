from __future__ import annotations

from apps.testing.permissions import (
    TestReviewActionPermission,
    TestReviewQueuePermission,
)
from apps.testing.selectors import get_attempt_for_update
from apps.testing.serializers import (
    RecalculateAttemptScoreSerializer,
    ReviewQueueFilterSerializer,
    TeacherTestingSummarySerializer,
    TestAttemptReadSerializer,
    TestAttemptReviewQueueSerializer,
    TestReviewSummarySerializer,
)
from apps.testing.services.review.queue import get_teacher_review_queue
from apps.testing.services.review.recalculation import (
    recalculate_attempt_score_from_answers,
)
from apps.testing.services.review.summary import (
    build_teacher_testing_summary,
    build_test_review_summary,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


class TestReviewViewSet(ViewSet):
    """
    ViewSet очереди проверки и сводки по тестированию.
    """

    permission_classes = (TestReviewQueuePermission,)

    @action(
        detail=False,
        methods=("get",),
        url_path="queue",
    )
    def queue(self, request):
        """
        Возвращает очередь проверки преподавателя.
        """

        serializer = ReviewQueueFilterSerializer(
            data=request.query_params,
        )
        serializer.is_valid(raise_exception=True)

        test_id = serializer.validated_data.get("test_id")

        queryset = get_teacher_review_queue(
            teacher_id=request.user.id,
            test_id=test_id,
        )

        return Response(
            TestAttemptReviewQueueSerializer(queryset, many=True).data,
        )

    @action(
        detail=False,
        methods=("get",),
        url_path="teacher-summary",
    )
    def teacher_summary(self, request):
        """
        Возвращает общую сводку преподавателя по тестированию.
        """

        summary = build_teacher_testing_summary(
            teacher_id=request.user.id,
        )

        return Response(TeacherTestingSummarySerializer(summary).data)

    @action(
        detail=False,
        methods=("get",),
        url_path="test-summary",
    )
    def test_summary(self, request):
        """
        Возвращает сводку по конкретному тесту.
        """

        test_id = request.query_params.get("test_id")

        if test_id is None:
            return Response(
                {
                    "test_id": "Укажите идентификатор теста.",
                },
                status=400,
            )

        summary = build_test_review_summary(test_id=int(test_id))

        return Response(TestReviewSummarySerializer(summary).data)

    @action(
        detail=False,
        methods=("post",),
        url_path="recalculate-attempt",
        permission_classes=(TestReviewActionPermission,),
    )
    def recalculate_attempt(self, request):
        """
        Пересчитывает баллы попытки по ответам.
        """

        serializer = RecalculateAttemptScoreSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        attempt_id = request.data.get("attempt_id")

        if attempt_id is None:
            return Response(
                {
                    "attempt_id": "Укажите идентификатор попытки.",
                },
                status=400,
            )

        attempt = get_attempt_for_update(int(attempt_id))

        self.check_object_permissions(request, attempt)

        attempt = recalculate_attempt_score_from_answers(attempt=attempt)

        return Response(TestAttemptReadSerializer(attempt).data)
