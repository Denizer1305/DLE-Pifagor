from __future__ import annotations

from apps.materials.filters import MaterialUsageLogFilter
from apps.materials.models import Material, MaterialUsageLog
from apps.materials.permissions import MaterialUsageLogPermission
from apps.materials.selectors import (
    limit_materials_queryset_by_user,
    material_usage_log_base_queryset,
)
from apps.materials.serializers import (
    MaterialUsageLogReadSerializer,
    MaterialUsageLogWriteSerializer,
)
from apps.materials.views.shared import MaterialsReadWriteViewSetMixin
from django.db.models import Q


class MaterialUsageLogViewSet(MaterialsReadWriteViewSetMixin):
    """
    API журнала использования учебных материалов.
    """

    permission_classes = (MaterialUsageLogPermission,)
    filterset_class = MaterialUsageLogFilter
    read_serializer_class = MaterialUsageLogReadSerializer
    write_serializer_class = MaterialUsageLogWriteSerializer

    def get_queryset(self):
        """
        Возвращает события использования материалов с учётом доступа.
        """

        user = self.request.user

        if not user or not user.is_authenticated:
            return MaterialUsageLog.objects.none()

        if getattr(user, "is_superuser", False):
            return material_usage_log_base_queryset()

        available_materials = limit_materials_queryset_by_user(
            Material.objects.all(),
            user,
        )

        return material_usage_log_base_queryset().filter(
            Q(user=user) | Q(material__in=available_materials),
        )
