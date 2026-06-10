from __future__ import annotations

from apps.materials.filters import MaterialCategoryFilter
from apps.materials.permissions import MaterialCategoryPermission
from apps.materials.selectors import get_available_material_categories_for_user
from apps.materials.serializers import (
    MaterialCategoryReadSerializer,
    MaterialCategoryWriteSerializer,
)
from apps.materials.services import (
    deactivate_material_category,
    restore_material_category,
)
from apps.materials.views.shared import MaterialsReadWriteViewSetMixin
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class MaterialCategoryViewSet(MaterialsReadWriteViewSetMixin):
    """
    API категорий учебных материалов.
    """

    permission_classes = (MaterialCategoryPermission,)
    filterset_class = MaterialCategoryFilter
    read_serializer_class = MaterialCategoryReadSerializer
    write_serializer_class = MaterialCategoryWriteSerializer

    def get_queryset(self):
        """
        Возвращает категории материалов, доступные пользователю.
        """

        return get_available_material_categories_for_user(
            user=self.request.user,
            is_active=None,
        )

    def destroy(self, request, *args, **kwargs) -> Response:
        """
        Вместо физического удаления деактивирует категорию.
        """

        category = self.get_object()
        deactivate_material_category(category=category)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=["post"],
        url_path="deactivate",
    )
    def deactivate(self, request, pk=None) -> Response:
        """
        Деактивирует категорию материалов.
        """

        category = self.get_object()
        category = deactivate_material_category(category=category)

        return self.build_read_response(category)

    @action(
        detail=True,
        methods=["post"],
        url_path="restore",
    )
    def restore(self, request, pk=None) -> Response:
        """
        Восстанавливает категорию материалов.
        """

        category = self.get_object()
        category = restore_material_category(category=category)

        return self.build_read_response(category)
