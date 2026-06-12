from __future__ import annotations

from apps.testing.permissions import TestTakingPermission
from apps.testing.selectors import (
    get_active_attempt_for_taking,
    get_taking_attempt_by_id,
    get_taking_test_by_id,
)
from apps.testing.serializers import (
    TestAttemptReadSerializer,
    TestTakingPayloadSerializer,
    TestTakingSaveAnswersSerializer,
    TestTakingSubmitSerializer,
)
from apps.testing.services.attempt.answers import save_attempt_answers
from apps.testing.services.attempt.lifecycle import (
    start_test_attempt,
    submit_test_attempt,
)
from apps.testing.services.taking.access import (
    ensure_learner_can_continue_attempt,
    ensure_learner_can_take_test,
)
from apps.testing.services.taking.payloads import build_taking_test_payload
from apps.testing.tasks import (
    auto_check_attempt_task,
    build_and_save_attempt_integrity_report_task,
)
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


class TestTakingViewSet(ViewSet):
    """
    ViewSet безопасного прохождения теста обучающимся.
    """

    permission_classes = (TestTakingPermission,)

    @action(
        detail=False,
        methods=("post",),
        url_path="start",
    )
    def start(self, request):
        """
        Начинает или возвращает активную попытку прохождения теста.
        """

        test_id = request.data.get("test_id")

        if test_id is None:
            return Response(
                {
                    "test_id": "Укажите идентификатор теста.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        test = get_taking_test_by_id(int(test_id))

        ensure_learner_can_take_test(
            test=test,
            learner=request.user,
        )

        attempt = get_active_attempt_for_taking(
            test_id=test.id,
            learner_id=request.user.id,
        )

        if attempt is None:
            attempt = start_test_attempt(
                test=test,
                learner=request.user,
            )

        payload = build_taking_test_payload(
            test=test,
            attempt=attempt,
        )

        return Response(
            TestTakingPayloadSerializer(payload).data,
            status=status.HTTP_200_OK,
        )

    @action(
        detail=False,
        methods=("get",),
        url_path="active",
    )
    def active(self, request):
        """
        Возвращает активный payload прохождения теста.
        """

        test_id = request.query_params.get("test_id")

        if test_id is None:
            return Response(
                {
                    "test_id": "Укажите идентификатор теста.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        test = get_taking_test_by_id(int(test_id))

        ensure_learner_can_take_test(
            test=test,
            learner=request.user,
        )

        attempt = get_active_attempt_for_taking(
            test_id=test.id,
            learner_id=request.user.id,
        )

        if attempt is None:
            return Response(
                {
                    "attempt": "Активная попытка не найдена.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        payload = build_taking_test_payload(
            test=test,
            attempt=attempt,
        )

        return Response(TestTakingPayloadSerializer(payload).data)

    @action(
        detail=False,
        methods=("post",),
        url_path="save-answers",
    )
    def save_answers(self, request):
        """
        Сохраняет ответы обучающегося.
        """

        serializer = TestTakingSaveAnswersSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        attempt = get_taking_attempt_by_id(
            attempt_id=serializer.validated_data["attempt_id"],
            learner_id=request.user.id,
        )

        ensure_learner_can_continue_attempt(
            attempt=attempt,
            learner=request.user,
        )

        answers = save_attempt_answers(
            attempt=attempt,
            answers_data=serializer.validated_data["answers"],
        )

        return Response(
            {
                "saved_count": len(answers),
            },
            status=status.HTTP_200_OK,
        )

    @action(
        detail=False,
        methods=("post",),
        url_path="submit",
    )
    def submit(self, request):
        """
        Отправляет попытку на проверку и запускает автопроверку.
        """

        serializer = TestTakingSubmitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        attempt_id = request.data.get("attempt_id")

        if attempt_id is None:
            return Response(
                {
                    "attempt_id": "Укажите идентификатор попытки.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        attempt = get_taking_attempt_by_id(
            attempt_id=int(attempt_id),
            learner_id=request.user.id,
        )

        ensure_learner_can_continue_attempt(
            attempt=attempt,
            learner=request.user,
        )

        attempt = submit_test_attempt(attempt=attempt)
        attempt = auto_check_attempt_task(attempt_id=attempt.id)

        build_and_save_attempt_integrity_report_task(
            attempt_id=attempt.id,
        )

        return Response(TestAttemptReadSerializer(attempt).data)
