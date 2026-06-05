from apps.dashboard.views.admin_dashboard_views import AdminDashboardSummaryAPIView
from apps.dashboard.views.dashboard_item_views import (
    DashboardItemDetailAPIView,
    DashboardItemListCreateAPIView,
)
from apps.dashboard.views.parent_dashboard_views import ParentDashboardSummaryAPIView
from apps.dashboard.views.student_dashboard_views import StudentDashboardSummaryAPIView
from apps.dashboard.views.teacher_dashboard_views import TeacherDashboardSummaryAPIView

__all__ = [
    "AdminDashboardSummaryAPIView",
    "DashboardItemDetailAPIView",
    "DashboardItemListCreateAPIView",
    "ParentDashboardSummaryAPIView",
    "StudentDashboardSummaryAPIView",
    "TeacherDashboardSummaryAPIView",
]
