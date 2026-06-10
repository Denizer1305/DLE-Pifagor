from __future__ import annotations

from apps.testing.filters import TestLearnerResultFilter
from apps.testing.permissions import (
    TestLearnerResultPermission,
    TestResultPublicationPermission,
    is_learner,
    is_teacher,
    is_testing_admin,
)
from apps.testing.selectors import result_list_queryset
from apps.testing.serializers import TestLearnerResultReadSerializer
from apps.testing.services import hide_learner_result
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet


class TestLearnerResultViewSet(ReadOnlyModelViewSet):
    """
    ViewSet итоговых результатов тестов.
    """

    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = TestLearnerResultFilter
    permission_classes = (TestLearnerResultPermission,)
    serializer_class = TestLearnerResultReadSerializer
    ordering_fields = (
        "id",
        "average_score",
        "average_grade",
        "attempts_count",
        "updated_at",
    )
    ordering = ("-updated_at", "-id")

    def get_queryset(self):
        """
        Возвращает результаты с учётом роли пользователя.
        """

        queryset = result_list_queryset()
        user = self.request.user

        if is_testing_admin(user=user):
            return queryset

        if is_teacher(user=user):
            return queryset.filter(test__owner_teacher_id=user.id)

        if is_learner(user=user):
            return queryset.filter(
                learner_id=user.id,
                is_visible_to_learner=True,
            )

        return queryset.none()

    @action(
        detail=True,
        methods=("post",),
        permission_classes=(TestResultPublicationPermission,),
    )
    def hide(self, request, pk=None):
        """
        Скрывает итоговый результат от ученика и родителя.
        """

        result = self.get_object()
        hide_learner_result(result=result)

        return Response(TestLearnerResultReadSerializer(result).data)
