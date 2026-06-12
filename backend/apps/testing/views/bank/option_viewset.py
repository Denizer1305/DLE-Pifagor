from __future__ import annotations

from apps.testing.filters import QuestionBankOptionFilter
from apps.testing.permissions import (
    QuestionBankOptionPermission,
    is_teacher,
    is_testing_admin,
)
from apps.testing.selectors import bank_option_list_queryset
from apps.testing.serializers import (
    QuestionBankOptionReadSerializer,
    QuestionBankOptionWriteSerializer,
)
from apps.testing.services.bank.mutations import create_bank_option, update_bank_option
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


class QuestionBankOptionViewSet(ModelViewSet):
    """
    ViewSet вариантов ответа шаблонов вопросов.
    """

    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
    )
    filterset_class = QuestionBankOptionFilter
    permission_classes = (QuestionBankOptionPermission,)
    ordering_fields = (
        "id",
        "bank_item",
        "order",
        "is_correct",
        "score",
        "created_at",
        "updated_at",
    )
    ordering = (
        "bank_item_id",
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

        queryset = bank_option_list_queryset()
        user = self.request.user

        if is_testing_admin(user=user):
            return queryset

        if is_teacher(user=user):
            return queryset.filter(bank_item__owner_teacher_id=user.id)

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
            return QuestionBankOptionWriteSerializer

        return QuestionBankOptionReadSerializer

    def create(self, request, *args, **kwargs):
        """
        Создаёт вариант ответа шаблона.
        """

        serializer = QuestionBankOptionWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        option = create_bank_option(data=serializer.validated_data)

        return Response(
            QuestionBankOptionReadSerializer(option).data,
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        """
        Полностью обновляет вариант ответа шаблона.
        """

        return self._update_option(
            request=request,
            partial=False,
        )

    def partial_update(self, request, *args, **kwargs):
        """
        Частично обновляет вариант ответа шаблона.
        """

        return self._update_option(
            request=request,
            partial=True,
        )

    def _update_option(
        self,
        *,
        request,
        partial: bool,
    ):
        """
        Общая логика обновления варианта ответа шаблона.
        """

        option = self.get_object()
        serializer = QuestionBankOptionWriteSerializer(
            option,
            data=request.data,
            partial=partial,
        )
        serializer.is_valid(raise_exception=True)

        option = update_bank_option(
            option=option,
            data=serializer.validated_data,
        )

        return Response(QuestionBankOptionReadSerializer(option).data)
