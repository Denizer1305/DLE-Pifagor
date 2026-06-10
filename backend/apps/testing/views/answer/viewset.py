from __future__ import annotations

from apps.testing.filters import TestAttemptAnswerFilter
from apps.testing.permissions import (
    TestAttemptAnswerPermission,
    TestAttemptAnswerReviewPermission,
    is_learner,
    is_teacher,
    is_testing_admin,
    user_can_manage_attempt_object,
    user_can_track_attempt_object,
)
from apps.testing.selectors import answer_list_queryset, get_attempt_by_id
from apps.testing.serializers import (
    ReviewAttemptAnswerSerializer,
    SaveAttemptAnswersSerializer,
    TestAttemptAnswerReadSerializer,
    TestAttemptAnswerWriteSerializer,
)
from apps.testing.services import (
    review_attempt_answer,
    save_attempt_answer,
    save_attempt_answers,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


class TestAttemptAnswerViewSet(ModelViewSet):
    """
    ViewSet ответов на вопросы теста.
    """

    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
    )
    filterset_class = TestAttemptAnswerFilter
    permission_classes = (TestAttemptAnswerPermission,)
    ordering_fields = (
        "id",
        "attempt",
        "question",
        "auto_score",
        "final_score",
        "updated_at",
    )
    ordering = (
        "attempt_id",
        "question_id",
        "id",
    )
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
        Возвращает ответы с ограничением по роли.
        """

        queryset = answer_list_queryset()
        user = self.request.user

        if is_testing_admin(user=user):
            return queryset

        if is_teacher(user=user):
            return queryset.filter(
                attempt__test__owner_teacher_id=user.id,
            )

        if is_learner(user=user):
            return queryset.filter(
                attempt__learner_id=user.id,
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
            return TestAttemptAnswerWriteSerializer

        if self.action == "save_bulk":
            return SaveAttemptAnswersSerializer

        if self.action == "review":
            return ReviewAttemptAnswerSerializer

        return TestAttemptAnswerReadSerializer

    def create(self, request, *args, **kwargs):
        """
        Сохраняет один ответ попытки.
        """

        serializer = TestAttemptAnswerWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        payload = serializer.validated_data
        attempt = payload["attempt"]

        self._check_attempt_write_access(
            request=request,
            attempt=attempt,
        )

        answer = save_attempt_answer(
            attempt=attempt,
            data=_build_answer_payload(payload=payload),
        )

        return Response(
            TestAttemptAnswerReadSerializer(answer).data,
            status=status.HTTP_201_CREATED,
        )

    @action(
        detail=False,
        methods=("post",),
        url_path="save-bulk",
    )
    def save_bulk(self, request):
        """
        Сохраняет набор ответов внутри попытки.
        """

        serializer = SaveAttemptAnswersSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        attempt_id = request.data.get("attempt_id")

        if attempt_id is None:
            return Response(
                {
                    "attempt_id": "Укажите идентификатор попытки.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        attempt = get_attempt_by_id(int(attempt_id))

        self._check_attempt_write_access(
            request=request,
            attempt=attempt,
        )

        answers = save_attempt_answers(
            attempt=attempt,
            answers_data=serializer.validated_data["answers"],
        )

        return Response(
            TestAttemptAnswerReadSerializer(answers, many=True).data,
            status=status.HTTP_200_OK,
        )

    @action(
        detail=True,
        methods=("post",),
        permission_classes=(TestAttemptAnswerReviewPermission,),
    )
    def review(self, request, pk=None):
        """
        Выполняет ручную проверку ответа.
        """

        serializer = ReviewAttemptAnswerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        answer = review_attempt_answer(
            answer=self.get_object(),
            **serializer.validated_data,
        )

        return Response(TestAttemptAnswerReadSerializer(answer).data)

    def _check_attempt_write_access(
        self,
        *,
        request,
        attempt,
    ) -> None:
        """
        Проверяет право сохранять ответы в попытке.
        """

        if is_learner(user=request.user):
            if user_can_track_attempt_object(
                user=request.user,
                attempt=attempt,
            ):
                return

            self.permission_denied(
                request,
                message="Нет доступа к этой попытке.",
            )

        if user_can_manage_attempt_object(
            user=request.user,
            attempt=attempt,
        ):
            return

        self.permission_denied(
            request,
            message="Нет доступа к этой попытке.",
        )


def _build_answer_payload(*, payload: dict) -> dict:
    """
    Преобразует serializer payload в payload сервисов.
    """

    question = payload["question"]
    selected_option = payload.get("selected_option")

    return {
        "question_id": question.id,
        "selected_option_id": (
            selected_option.id if selected_option is not None else None
        ),
        "selected_options_data": payload.get("selected_options_data", []),
        "text_answer": payload.get("text_answer", ""),
        "number_answer": payload.get("number_answer"),
    }
