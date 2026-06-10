from apps.dashboard.views import (
    AdminDashboardSummaryAPIView,
    DashboardItemDetailAPIView,
    DashboardItemListCreateAPIView,
    ParentDashboardSummaryAPIView,
    StudentDashboardSummaryAPIView,
    TeacherDashboardSummaryAPIView,
)
from django.urls import path

app_name = "dashboard"

urlpatterns = [
    path(
        "me/items/",
        DashboardItemListCreateAPIView.as_view(),
        name="dashboard-item-list-create",
    ),
    path(
        "me/items/<int:item_id>/",
        DashboardItemDetailAPIView.as_view(),
        name="dashboard-item-detail",
    ),
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
    path(
        "parent/summary/",
        ParentDashboardSummaryAPIView.as_view(),
        name="parent-dashboard-summary",
    ),
]
