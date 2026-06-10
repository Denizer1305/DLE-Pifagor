from __future__ import annotations

from apps.education.views import (
    AcademicYearViewSet,
    CurriculumItemViewSet,
    CurriculumViewSet,
    EducationPeriodViewSet,
    GroupSubjectViewSet,
    LearnerGroupEnrollmentViewSet,
    TeacherGroupSubjectViewSet,
)
from rest_framework.routers import DefaultRouter

admin_router = DefaultRouter()

admin_router.register(
    "academic-years",
    AcademicYearViewSet,
    basename="education-admin-academic-years",
)
admin_router.register(
    "periods",
    EducationPeriodViewSet,
    basename="education-admin-periods",
)
admin_router.register(
    "curricula",
    CurriculumViewSet,
    basename="education-admin-curricula",
)
admin_router.register(
    "curriculum-items",
    CurriculumItemViewSet,
    basename="education-admin-curriculum-items",
)
admin_router.register(
    "group-subjects",
    GroupSubjectViewSet,
    basename="education-admin-group-subjects",
)
admin_router.register(
    "teacher-group-subjects",
    TeacherGroupSubjectViewSet,
    basename="education-admin-teacher-group-subjects",
)
admin_router.register(
    "learner-enrollments",
    LearnerGroupEnrollmentViewSet,
    basename="education-admin-learner-enrollments",
)
