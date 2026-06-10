from __future__ import annotations

from apps.education.filters import EducationPeriodFilter
from apps.education.permissions import EducationPeriodPermission
from apps.education.selectors import education_period_detail_queryset
from apps.education.serializers import (
    EducationPeriodReadSerializer,
    EducationPeriodWriteSerializer,
)
from apps.education.services import (
    deactivate_education_period,
    restore_education_period,
    set_current_education_period,
)
from apps.education.views.shared import EducationReadWriteViewSetMixin
from rest_framework.decorators import action
from rest_framework.response import Response


class EducationPeriodViewSet(EducationReadWriteViewSetMixin):
    """
    Административный API учебных периодов.
    """

    permission_classes = (EducationPeriodPermission,)
    filterset_class = EducationPeriodFilter
    read_serializer_class = EducationPeriodReadSerializer
    write_serializer_class = EducationPeriodWriteSerializer

    def get_queryset(self):
        """
        Возвращает queryset учебных периодов.
        """

        return education_period_detail_queryset()

    @action(
        detail=True,
        methods=["post"],
        url_path="set-current",
    )
    def set_current(self, request, pk=None) -> Response:
        """
        Делает учебный период текущим.
        """

        period = self.get_object()
        period = set_current_education_period(period=period)

        return self.build_read_response(period)

    @action(
        detail=True,
        methods=["post"],
        url_path="deactivate",
    )
    def deactivate(self, request, pk=None) -> Response:
        """
        Деактивирует учебный период.
        """

        period = self.get_object()
        period = deactivate_education_period(period=period)

        return self.build_read_response(period)

    @action(
        detail=True,
        methods=["post"],
        url_path="restore",
    )
    def restore(self, request, pk=None) -> Response:
        """
        Восстанавливает учебный период.
        """

        period = self.get_object()
        period = restore_education_period(period=period)

        return self.build_read_response(period)
