from __future__ import annotations

from apps.course.models import CourseEnrollment
from apps.testing.constants import TestStatus
from apps.testing.filters import TestQuestionFilter
from apps.testing.permissions import (
    QuestionOrderingPermission,
    TestQuestionPermission,
    is_learner,
    is_teacher,
    is_testing_admin,
)
from apps.testing.selectors import question_list_queryset
from apps.testing.serializers import (
    QuestionReorderSerializer,
    TestQuestionReadSerializer,
    TestQuestionWriteSerializer,
)
from apps.testing.services import create_question, reorder_questions, update_question
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


class TestQuestionViewSet(ModelViewSet):
    """
    ViewSet вопросов теста.
    """

    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
    )
    filterset_class = TestQuestionFilter
    permission_classes = (TestQuestionPermission,)
    ordering_fields = (
        "id",
        "test",
        "order",
        "score",
        "created_at",
        "updated_at",
    )
    ordering = (
        "test_id",
        "order",
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
        Возвращает вопросы с ограничением по роли.
        """

        queryset = question_list_queryset()
        user = self.request.user

        if is_testing_admin(user=user):
            return queryset

        if is_teacher(user=user):
            return queryset.filter(
                test__owner_teacher_id=user.id,
            )

        if is_learner(user=user):
            course_ids = CourseEnrollment.objects.filter(
                learner_id=user.id,
            ).values_list(
                "course_id",
                flat=True,
            )

            return queryset.filter(
                test__course_id__in=course_ids,
                test__status=TestStatus.PUBLISHED,
                test__is_active=True,
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
            return TestQuestionWriteSerializer

        if self.action == "reorder":
            return QuestionReorderSerializer

        return TestQuestionReadSerializer

    def create(self, request, *args, **kwargs):
        """
        Создаёт вопрос теста.
        """

        serializer = TestQuestionWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        question = create_question(data=serializer.validated_data)

        return Response(
            TestQuestionReadSerializer(question).data,
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        """
        Полностью обновляет вопрос.
        """

        return self._update_question(
            request=request,
            partial=False,
        )

    def partial_update(self, request, *args, **kwargs):
        """
        Частично обновляет вопрос.
        """

        return self._update_question(
            request=request,
            partial=True,
        )

    @action(
        detail=False,
        methods=("post",),
        permission_classes=(QuestionOrderingPermission,),
    )
    def reorder(self, request):
        """
        Переупорядочивает вопросы внутри теста.
        """

        serializer = QuestionReorderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        test_id = request.data.get("test_id")

        if test_id is None:
            return Response(
                {
                    "test_id": "Укажите идентификатор теста.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        reorder_questions(
            test_id=int(test_id),
            ordered_question_ids=serializer.validated_data["ordered_question_ids"],
        )

        return Response(status=status.HTTP_204_NO_CONTENT)

    def _update_question(
        self,
        *,
        request,
        partial: bool,
    ):
        """
        Общая логика обновления вопроса.
        """

        question = self.get_object()
        serializer = TestQuestionWriteSerializer(
            question,
            data=request.data,
            partial=partial,
        )
        serializer.is_valid(raise_exception=True)

        question = update_question(
            question=question,
            data=serializer.validated_data,
        )

        return Response(TestQuestionReadSerializer(question).data)
