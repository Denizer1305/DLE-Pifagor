from __future__ import annotations

from apps.education.filters import AcademicYearFilter
from apps.education.permissions import AcademicYearPermission
from apps.education.selectors import academic_year_detail_queryset
from apps.education.serializers import (
    AcademicYearReadSerializer,
    AcademicYearWriteSerializer,
)
from apps.education.services import (
    deactivate_academic_year,
    restore_academic_year,
    set_current_academic_year,
)
from apps.education.views.shared import EducationReadWriteViewSetMixin
from rest_framework.decorators import action
from rest_framework.response import Response


class AcademicYearViewSet(EducationReadWriteViewSetMixin):
    """
    Административный API учебных годов.
    """

    permission_classes = (AcademicYearPermission,)
    filterset_class = AcademicYearFilter
    read_serializer_class = AcademicYearReadSerializer
    write_serializer_class = AcademicYearWriteSerializer

    def get_queryset(self):
        """
        Возвращает queryset учебных годов.
        """

        return academic_year_detail_queryset()

    @action(
        detail=True,
        methods=["post"],
        url_path="set-current",
    )
    def set_current(self, request, pk=None) -> Response:
        """
        Делает учебный год текущим.
        """

        academic_year = self.get_object()
        academic_year = set_current_academic_year(academic_year=academic_year)

        return self.build_read_response(academic_year)

    @action(
        detail=True,
        methods=["post"],
        url_path="deactivate",
    )
    def deactivate(self, request, pk=None) -> Response:
        """
        Деактивирует учебный год.
        """

        academic_year = self.get_object()
        academic_year = deactivate_academic_year(academic_year=academic_year)

        return self.build_read_response(academic_year)

    @action(
        detail=True,
        methods=["post"],
        url_path="restore",
    )
    def restore(self, request, pk=None) -> Response:
        """
        Восстанавливает учебный год.
        """

        academic_year = self.get_object()
        academic_year = restore_academic_year(academic_year=academic_year)

        return self.build_read_response(academic_year)
