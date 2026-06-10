from __future__ import annotations

from apps.materials.filters import MaterialVersionFilter
from apps.materials.models import Material
from apps.materials.permissions import (
    MaterialVersionPermission,
    MaterialVersionSetCurrentPermission,
)
from apps.materials.selectors import (
    limit_materials_queryset_by_user,
    material_version_detail_queryset,
)
from apps.materials.serializers import (
    MaterialVersionReadSerializer,
    MaterialVersionSetCurrentSerializer,
    MaterialVersionWriteSerializer,
)
from apps.materials.services import (
    archive_material_version,
    set_current_material_version,
)
from apps.materials.views.shared import MaterialsReadWriteViewSetMixin
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class MaterialVersionViewSet(MaterialsReadWriteViewSetMixin):
    """
    API версий учебных материалов.
    """

    permission_classes = (MaterialVersionPermission,)
    filterset_class = MaterialVersionFilter
    read_serializer_class = MaterialVersionReadSerializer
    write_serializer_class = MaterialVersionWriteSerializer
    serializer_action_classes = {
        "set_current": MaterialVersionSetCurrentSerializer,
    }

    def get_permissions(self):
        """
        Возвращает ограничения доступа под действие.
        """

        if self.action == "set_current":
            return [MaterialVersionSetCurrentPermission()]

        return super().get_permissions()

    def get_queryset(self):
        """
        Возвращает версии материалов, доступные пользователю.
        """

        available_materials = limit_materials_queryset_by_user(
            Material.objects.all(),
            self.request.user,
        )

        return material_version_detail_queryset().filter(
            material__in=available_materials,
        )

    def destroy(self, request, *args, **kwargs) -> Response:
        """
        Вместо физического удаления архивирует версию материала.
        """

        version = self.get_object()
        archive_material_version(version=version)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=["post"],
        url_path="set-current",
    )
    def set_current(self, request, pk=None) -> Response:
        """
        Делает версию текущей для материала.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        version = self.get_object()
        version = set_current_material_version(version=version)

        return self.build_read_response(version)

    @action(
        detail=True,
        methods=["post"],
        url_path="archive",
    )
    def archive(self, request, pk=None) -> Response:
        """
        Архивирует версию материала.
        """

        version = self.get_object()
        version = archive_material_version(version=version)

        return self.build_read_response(version)
