from __future__ import annotations

from apps.materials.filters import MaterialFilter
from apps.materials.models import MaterialUsageLog
from apps.materials.permissions import MaterialPermission, MaterialStatusPermission
from apps.materials.selectors import (
    get_published_public_materials,
    get_user_available_materials,
)
from apps.materials.serializers import (
    MaterialReadSerializer,
    MaterialStatusActionSerializer,
    MaterialUsageLogCreateSerializer,
    MaterialUsageLogReadSerializer,
    MaterialWriteSerializer,
)
from apps.materials.services import (
    archive_material,
    log_material_usage,
    publish_material,
    restore_material,
)
from apps.materials.views.shared import MaterialsReadWriteViewSetMixin
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class MaterialViewSet(MaterialsReadWriteViewSetMixin):
    """
    API учебных материалов.
    """

    permission_classes = (MaterialPermission,)
    filterset_class = MaterialFilter
    read_serializer_class = MaterialReadSerializer
    write_serializer_class = MaterialWriteSerializer
    serializer_action_classes = {
        "publish": MaterialStatusActionSerializer,
        "archive": MaterialStatusActionSerializer,
        "restore": MaterialStatusActionSerializer,
        "log_usage": MaterialUsageLogCreateSerializer,
    }

    def get_permissions(self):
        """
        Возвращает ограничения доступа под действие.
        """

        if self.action in {
            "publish",
            "archive",
            "restore",
        }:
            return [MaterialStatusPermission()]

        return super().get_permissions()

    def get_queryset(self):
        """
        Возвращает материалы, доступные пользователю.
        """

        return get_user_available_materials(
            user=self.request.user,
            is_active=None,
        )

    def destroy(self, request, *args, **kwargs) -> Response:
        """
        Вместо физического удаления архивирует материал.
        """

        material = self.get_object()
        archive_material(material=material)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=["post"],
        url_path="publish",
    )
    def publish(self, request, pk=None) -> Response:
        """
        Публикует учебный материал.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        material = self.get_object()
        material = publish_material(material=material)

        log_material_usage(
            material=material,
            action=MaterialUsageLog.ActionChoices.PUBLISH,
            context=MaterialUsageLog.ContextChoices.ADMIN,
            request=request,
            metadata={
                "source": "material_api_publish",
            },
        )

        return self.build_read_response(material)

    @action(
        detail=True,
        methods=["post"],
        url_path="archive",
    )
    def archive(self, request, pk=None) -> Response:
        """
        Архивирует учебный материал.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        material = self.get_object()
        material = archive_material(material=material)

        log_material_usage(
            material=material,
            action=MaterialUsageLog.ActionChoices.ARCHIVE,
            context=MaterialUsageLog.ContextChoices.ADMIN,
            request=request,
            metadata={
                "source": "material_api_archive",
            },
        )

        return self.build_read_response(material)

    @action(
        detail=True,
        methods=["post"],
        url_path="restore",
    )
    def restore(self, request, pk=None) -> Response:
        """
        Восстанавливает учебный материал в черновик.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        material = self.get_object()
        material = restore_material(material=material)

        return self.build_read_response(material)

    @action(
        detail=True,
        methods=["post"],
        url_path="log-usage",
    )
    def log_usage(self, request, pk=None) -> Response:
        """
        Логирует использование материала.
        """

        material = self.get_object()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        usage_log = log_material_usage(
            material=material,
            action=serializer.validated_data["action"],
            context=serializer.validated_data.get(
                "context",
                MaterialUsageLog.ContextChoices.LIBRARY,
            ),
            context_object_id=serializer.validated_data.get(
                "context_object_id",
            ),
            request=request,
            metadata=serializer.validated_data.get("metadata"),
        )

        read_serializer = MaterialUsageLogReadSerializer(
            usage_log,
            context=self.get_serializer_context(),
        )

        return Response(
            read_serializer.data,
            status=status.HTTP_201_CREATED,
        )


class PublicMaterialViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Публичный API учебных материалов.
    """

    serializer_class = MaterialReadSerializer
    filter_backends = MaterialViewSet.filter_backends
    filterset_class = MaterialFilter

    def get_queryset(self):
        """
        Возвращает публичные опубликованные материалы.
        """

        return get_published_public_materials()
