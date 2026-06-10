from __future__ import annotations

from apps.education.filters import CurriculumItemFilter
from apps.education.permissions import CurriculumItemPermission
from apps.education.selectors import (
    curriculum_item_detail_queryset,
    limit_queryset_by_user_organizations,
)
from apps.education.serializers import (
    CurriculumItemReadSerializer,
    CurriculumItemWriteSerializer,
)
from apps.education.services import deactivate_curriculum_item, restore_curriculum_item
from apps.education.views.shared import EducationReadWriteViewSetMixin
from rest_framework.decorators import action
from rest_framework.response import Response


class CurriculumItemViewSet(EducationReadWriteViewSetMixin):
    """
    Административный API элементов учебного плана.
    """

    permission_classes = (CurriculumItemPermission,)
    filterset_class = CurriculumItemFilter
    read_serializer_class = CurriculumItemReadSerializer
    write_serializer_class = CurriculumItemWriteSerializer

    def get_queryset(self):
        """
        Возвращает queryset элементов учебного плана.
        """

        queryset = curriculum_item_detail_queryset()

        return limit_queryset_by_user_organizations(
            queryset,
            self.request.user,
            organization_field="curriculum__organization_id",
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="deactivate",
    )
    def deactivate(self, request, pk=None) -> Response:
        """
        Деактивирует элемент учебного плана.
        """

        curriculum_item = self.get_object()
        curriculum_item = deactivate_curriculum_item(
            curriculum_item=curriculum_item,
        )

        return self.build_read_response(curriculum_item)

    @action(
        detail=True,
        methods=["post"],
        url_path="restore",
    )
    def restore(self, request, pk=None) -> Response:
        """
        Восстанавливает элемент учебного плана.
        """

        curriculum_item = self.get_object()
        curriculum_item = restore_curriculum_item(
            curriculum_item=curriculum_item,
        )

        return self.build_read_response(curriculum_item)
