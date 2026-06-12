from __future__ import annotations

from apps.testing.filters import QuestionBankItemFilter
from apps.testing.permissions import (
    QuestionBankItemPermission,
    QuestionBankStatusPermission,
    is_teacher,
    is_testing_admin,
)
from apps.testing.selectors import bank_item_list_queryset
from apps.testing.serializers import (
    BankItemStatusActionSerializer,
    CopyBankItemToTestSerializer,
    DuplicateBankItemSerializer,
    QuestionBankItemReadSerializer,
    QuestionBankItemWriteSerializer,
    TestQuestionReadSerializer,
)
from apps.testing.services.bank.mutations import create_bank_item, update_bank_item
from apps.testing.tasks import (
    archive_bank_item_task,
    copy_bank_item_to_test_task,
    duplicate_bank_item_task,
    publish_bank_item_task,
    restore_bank_item_task,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


class QuestionBankItemViewSet(ModelViewSet):
    """
    ViewSet шаблонов вопросов банка тестовых заданий.
    """

    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
    )
    filterset_class = QuestionBankItemFilter
    permission_classes = (QuestionBankItemPermission,)
    ordering_fields = (
        "id",
        "title",
        "question_type",
        "difficulty",
        "visibility",
        "status",
        "created_at",
        "updated_at",
    )
    ordering = (
        "-updated_at",
        "-id",
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
        Возвращает шаблоны вопросов с ограничением по роли.
        """

        queryset = bank_item_list_queryset()
        user = self.request.user

        if is_testing_admin(user=user):
            return queryset

        if is_teacher(user=user):
            organization_id = _get_user_organization_id(user=user)

            reusable_queryset = queryset.reusable_for_teacher(
                teacher_id=user.id,
                organization_id=organization_id,
            )
            own_queryset = queryset.filter(owner_teacher_id=user.id)

            return (own_queryset | reusable_queryset).distinct()

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
            return QuestionBankItemWriteSerializer

        if self.action in {
            "publish",
            "archive",
            "restore",
        }:
            return BankItemStatusActionSerializer

        if self.action == "duplicate":
            return DuplicateBankItemSerializer

        if self.action == "copy_to_test":
            return CopyBankItemToTestSerializer

        return QuestionBankItemReadSerializer

    def create(self, request, *args, **kwargs):
        """
        Создаёт шаблон вопроса.
        """

        serializer = QuestionBankItemWriteSerializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)

        bank_item = create_bank_item(data=serializer.validated_data)

        return Response(
            QuestionBankItemReadSerializer(bank_item).data,
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        """
        Полностью обновляет шаблон вопроса.
        """

        return self._update_bank_item(
            request=request,
            partial=False,
        )

    def partial_update(self, request, *args, **kwargs):
        """
        Частично обновляет шаблон вопроса.
        """

        return self._update_bank_item(
            request=request,
            partial=True,
        )

    def perform_destroy(self, instance) -> None:
        """
        Вместо удаления архивирует шаблон.
        """

        archive_bank_item_task(bank_item_id=instance.id)

    @action(
        detail=True,
        methods=("post",),
        permission_classes=(QuestionBankStatusPermission,),
    )
    def publish(self, request, pk=None):
        """
        Публикует шаблон вопроса.
        """

        serializer = BankItemStatusActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        bank_item = publish_bank_item_task(bank_item_id=self.get_object().id)

        return Response(QuestionBankItemReadSerializer(bank_item).data)

    @action(
        detail=True,
        methods=("post",),
        permission_classes=(QuestionBankStatusPermission,),
    )
    def archive(self, request, pk=None):
        """
        Архивирует шаблон вопроса.
        """

        serializer = BankItemStatusActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        bank_item = archive_bank_item_task(bank_item_id=self.get_object().id)

        return Response(QuestionBankItemReadSerializer(bank_item).data)

    @action(
        detail=True,
        methods=("post",),
        permission_classes=(QuestionBankStatusPermission,),
    )
    def restore(self, request, pk=None):
        """
        Восстанавливает шаблон вопроса в черновик.
        """

        serializer = BankItemStatusActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        bank_item = restore_bank_item_task(bank_item_id=self.get_object().id)

        return Response(QuestionBankItemReadSerializer(bank_item).data)

    @action(
        detail=True,
        methods=("post",),
        permission_classes=(QuestionBankStatusPermission,),
    )
    def duplicate(self, request, pk=None):
        """
        Создаёт копию шаблона вопроса.
        """

        serializer = DuplicateBankItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        bank_item = duplicate_bank_item_task(
            bank_item_id=self.get_object().id,
            owner_teacher=request.user,
        )

        custom_title = serializer.validated_data.get("title")

        if custom_title:
            bank_item = update_bank_item(
                bank_item=bank_item,
                data={"title": custom_title},
            )

        return Response(
            QuestionBankItemReadSerializer(bank_item).data,
            status=status.HTTP_201_CREATED,
        )

    @action(
        detail=True,
        methods=("post",),
        url_path="copy-to-test",
        permission_classes=(QuestionBankStatusPermission,),
    )
    def copy_to_test(self, request, pk=None):
        """
        Копирует шаблон вопроса в конкретный тест.
        """

        serializer = CopyBankItemToTestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        question = copy_bank_item_to_test_task(
            bank_item_id=self.get_object().id,
            test_id=serializer.validated_data["test"].id,
            order=serializer.validated_data.get("order"),
        )

        return Response(
            TestQuestionReadSerializer(question).data,
            status=status.HTTP_201_CREATED,
        )

    def _update_bank_item(
        self,
        *,
        request,
        partial: bool,
    ):
        """
        Общая логика обновления шаблона вопроса.
        """

        bank_item = self.get_object()
        serializer = QuestionBankItemWriteSerializer(
            bank_item,
            data=request.data,
            partial=partial,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)

        bank_item = update_bank_item(
            bank_item=bank_item,
            data=serializer.validated_data,
        )

        return Response(QuestionBankItemReadSerializer(bank_item).data)


def _get_user_organization_id(*, user) -> int | None:
    """
    Возвращает организацию пользователя мягким способом.
    """

    user_organization_id = getattr(user, "organization_id", None)

    if user_organization_id is not None:
        return user_organization_id

    profile = getattr(user, "profile", None)

    if profile is None:
        return None

    return getattr(profile, "organization_id", None)
