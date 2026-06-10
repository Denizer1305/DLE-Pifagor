from __future__ import annotations

from apps.organizations.views import (
    AdminDepartmentViewSet,
    AdminGroupCuratorViewSet,
    AdminOrganizationViewSet,
    AdminStudyGroupViewSet,
    AdminSubjectViewSet,
    AdminTeacherOrganizationViewSet,
    AdminTeacherSubjectViewSet,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(
    r"admin/organizations",
    AdminOrganizationViewSet,
    basename="admin-organizations",
)
router.register(
    r"admin/departments",
    AdminDepartmentViewSet,
    basename="admin-departments",
)
router.register(
    r"admin/study-groups",
    AdminStudyGroupViewSet,
    basename="admin-study-groups",
)
router.register(
    r"admin/teacher-organizations",
    AdminTeacherOrganizationViewSet,
    basename="admin-teacher-organizations",
)
router.register(
    r"admin/group-curators",
    AdminGroupCuratorViewSet,
    basename="admin-group-curators",
)
router.register(
    r"admin/subjects",
    AdminSubjectViewSet,
    basename="admin-subjects",
)
router.register(
    r"admin/teacher-subjects",
    AdminTeacherSubjectViewSet,
    basename="admin-teacher-subjects",
)

urlpatterns = router.urls
