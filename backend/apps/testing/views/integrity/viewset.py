from __future__ import annotations

from apps.testing.filters import TestAttemptIntegrityReportFilter
from apps.testing.permissions import TestAttemptIntegrityReportPermission
from apps.testing.selectors import integrity_report_list_queryset
from apps.testing.serializers import TestAttemptIntegrityReportReadSerializer
from apps.testing.tasks import build_and_save_attempt_integrity_report_task
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet


class TestAttemptIntegrityReportViewSet(ReadOnlyModelViewSet):
    """
    ViewSet сохранённых отчётов добросовестности попыток.
    """

    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
    )
    filterset_class = TestAttemptIntegrityReportFilter
    permission_classes = (TestAttemptIntegrityReportPermission,)
    serializer_class = TestAttemptIntegrityReportReadSerializer
    ordering_fields = (
        "id",
        "score",
        "risk_level",
        "checked_at",
        "created_at",
        "updated_at",
    )
    ordering = (
        "-checked_at",
        "-id",
    )

    def get_queryset(self):
        """
        Возвращает отчёты с ограничением по роли.
        """

        queryset = integrity_report_list_queryset()
        user = self.request.user

        from apps.testing.permissions import is_teacher, is_testing_admin

        if is_testing_admin(user=user):
            return queryset

        if is_teacher(user=user):
            return queryset.filter(
                attempt__test__owner_teacher_id=user.id,
            )

        return queryset.none()

    @action(
        detail=False,
        methods=("post",),
        url_path="build",
    )
    def build(self, request):
        """
        Формирует и сохраняет отчёт добросовестности по попытке.
        """

        attempt_id = request.data.get("attempt_id")

        if attempt_id is None:
            return Response(
                {
                    "attempt_id": "Укажите идентификатор попытки.",
                },
                status=400,
            )

        report = build_and_save_attempt_integrity_report_task(
            attempt_id=int(attempt_id),
        )

        self.check_object_permissions(request, report)

        return Response(
            TestAttemptIntegrityReportReadSerializer(report).data,
        )
