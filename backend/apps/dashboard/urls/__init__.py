from apps.dashboard.views import (
    AdminDashboardSummaryAPIView,
    StudentDashboardSummaryAPIView,
    TeacherDashboardSummaryAPIView,
)
from django.urls import path

app_name = "dashboard"

urlpatterns = [
    path(
        "admin/summary/",
        AdminDashboardSummaryAPIView.as_view(),
        name="admin-dashboard-summary",
    ),
    path(
        "teacher/summary/",
        TeacherDashboardSummaryAPIView.as_view(),
        name="teacher-dashboard-summary",
    ),
    path(
        "student/summary/",
        StudentDashboardSummaryAPIView.as_view(),
        name="student-dashboard-summary",
    ),
]
