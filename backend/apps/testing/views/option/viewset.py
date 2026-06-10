from __future__ import annotations

from apps.course.models import CourseEnrollment
from apps.testing.constants import TestStatus
from apps.testing.filters import TestQuestionOptionFilter
from apps.testing.permissions import (
    QuestionOrderingPermission,
    TestQuestionOptionPermission,
    is_learner,
    is_teacher,
    is_testing_admin,
)
from apps.testing.selectors import option_list_queryset
from apps.testing.serializers import (
    OptionReorderSerializer,
    TestQuestionOptionReadSerializer,
    TestQuestionOptionWriteSerializer,
)
from apps.testing.services import (
    create_question_option,
    reorder_question_options,
    update_question_option,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


class TestQuestionOptionViewSet(ModelViewSet):
    """
    ViewSet вариантов ответа на вопрос теста.
    """

    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
    )
    filterset_class = TestQuestionOptionFilter
    permission_classes = (TestQuestionOptionPermission,)
    ordering_fields = (
        "id",
        "question",
        "order",
        "score",
        "created_at",
        "updated_at",
    )
    ordering = (
        "question_id",
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
        Возвращает варианты ответа с ограничением по роли.
        """

        queryset = option_list_queryset()
        user = self.request.user

        if is_testing_admin(user=user):
            return queryset

        if is_teacher(user=user):
            return queryset.filter(
                question__test__owner_teacher_id=user.id,
            )

        if is_learner(user=user):
            course_ids = CourseEnrollment.objects.filter(
                learner_id=user.id,
            ).values_list(
                "course_id",
                flat=True,
            )

            return queryset.filter(
                question__test__course_id__in=course_ids,
                question__test__status=TestStatus.PUBLISHED,
                question__test__is_active=True,
                question__is_active=True,
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
            return TestQuestionOptionWriteSerializer

        if self.action == "reorder":
            return OptionReorderSerializer

        return TestQuestionOptionReadSerializer

    def create(self, request, *args, **kwargs):
        """
        Создаёт вариант ответа.
        """

        serializer = TestQuestionOptionWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        option = create_question_option(data=serializer.validated_data)

        return Response(
            TestQuestionOptionReadSerializer(option).data,
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        """
        Полностью обновляет вариант ответа.
        """

        return self._update_option(
            request=request,
            partial=False,
        )

    def partial_update(self, request, *args, **kwargs):
        """
        Частично обновляет вариант ответа.
        """

        return self._update_option(
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
        Переупорядочивает варианты ответа внутри вопроса.
        """

        serializer = OptionReorderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        question_id = request.data.get("question_id")

        if question_id is None:
            return Response(
                {
                    "question_id": "Укажите идентификатор вопроса.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        reorder_question_options(
            question_id=int(question_id),
            ordered_option_ids=serializer.validated_data["ordered_option_ids"],
        )

        return Response(status=status.HTTP_204_NO_CONTENT)

    def _update_option(
        self,
        *,
        request,
        partial: bool,
    ):
        """
        Общая логика обновления варианта ответа.
        """

        option = self.get_object()
        serializer = TestQuestionOptionWriteSerializer(
            option,
            data=request.data,
            partial=partial,
        )
        serializer.is_valid(raise_exception=True)

        option = update_question_option(
            option=option,
            data=serializer.validated_data,
        )

        return Response(TestQuestionOptionReadSerializer(option).data)
