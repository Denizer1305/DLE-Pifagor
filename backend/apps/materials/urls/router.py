from __future__ import annotations

from apps.materials.views import (
    MaterialCategoryViewSet,
    MaterialUsageLogViewSet,
    MaterialVersionViewSet,
    MaterialViewSet,
    PublicMaterialViewSet,
)
from rest_framework.routers import DefaultRouter

admin_router = DefaultRouter()
teacher_router = DefaultRouter()
learner_router = DefaultRouter()
public_router = DefaultRouter()


admin_router.register(
    "categories",
    MaterialCategoryViewSet,
    basename="materials-admin-categories",
)
admin_router.register(
    "materials",
    MaterialViewSet,
    basename="materials-admin-materials",
)
admin_router.register(
    "versions",
    MaterialVersionViewSet,
    basename="materials-admin-versions",
)
admin_router.register(
    "usage-logs",
    MaterialUsageLogViewSet,
    basename="materials-admin-usage-logs",
)


teacher_router.register(
    "categories",
    MaterialCategoryViewSet,
    basename="materials-teacher-categories",
)
teacher_router.register(
    "materials",
    MaterialViewSet,
    basename="materials-teacher-materials",
)
teacher_router.register(
    "versions",
    MaterialVersionViewSet,
    basename="materials-teacher-versions",
)
teacher_router.register(
    "usage-logs",
    MaterialUsageLogViewSet,
    basename="materials-teacher-usage-logs",
)


learner_router.register(
    "categories",
    MaterialCategoryViewSet,
    basename="materials-learner-categories",
)
learner_router.register(
    "materials",
    MaterialViewSet,
    basename="materials-learner-materials",
)
learner_router.register(
    "usage-logs",
    MaterialUsageLogViewSet,
    basename="materials-learner-usage-logs",
)


public_router.register(
    "materials",
    PublicMaterialViewSet,
    basename="materials-public-materials",
)
