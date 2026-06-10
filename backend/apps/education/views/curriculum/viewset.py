from __future__ import annotations

from apps.education.filters import CurriculumFilter
from apps.education.permissions import CurriculumPermission
from apps.education.selectors import (
    curriculum_detail_queryset,
    limit_queryset_by_user_organizations,
)
from apps.education.serializers import (
    CurriculumReadSerializer,
    CurriculumWriteSerializer,
)
from apps.education.services import (
    activate_curriculum,
    archive_curriculum,
    restore_curriculum,
)
from apps.education.views.shared import EducationReadWriteViewSetMixin
from rest_framework.decorators import action
from rest_framework.response import Response


class CurriculumViewSet(EducationReadWriteViewSetMixin):
    """
    Административный API учебных планов.
    """

    permission_classes = (CurriculumPermission,)
    filterset_class = CurriculumFilter
    read_serializer_class = CurriculumReadSerializer
    write_serializer_class = CurriculumWriteSerializer

    def get_queryset(self):
        """
        Возвращает queryset учебных планов с ограничением по организациям.
        """

        queryset = curriculum_detail_queryset()

        return limit_queryset_by_user_organizations(
            queryset,
            self.request.user,
            organization_field="organization_id",
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="activate",
    )
    def activate(self, request, pk=None) -> Response:
        """
        Активирует учебный план.
        """

        curriculum = self.get_object()
        curriculum = activate_curriculum(curriculum=curriculum)

        return self.build_read_response(curriculum)

    @action(
        detail=True,
        methods=["post"],
        url_path="archive",
    )
    def archive(self, request, pk=None) -> Response:
        """
        Архивирует учебный план.
        """

        curriculum = self.get_object()
        curriculum = archive_curriculum(curriculum=curriculum)

        return self.build_read_response(curriculum)

    @action(
        detail=True,
        methods=["post"],
        url_path="restore",
    )
    def restore(self, request, pk=None) -> Response:
        """
        Восстанавливает учебный план.
        """

        curriculum = self.get_object()
        curriculum = restore_curriculum(curriculum=curriculum)

        return self.build_read_response(curriculum)
