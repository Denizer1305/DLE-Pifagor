from __future__ import annotations

from apps.dashboard.permissions import IsTeacherDashboardUser
from apps.dashboard.selectors.teacher_dashboard_selectors import (
    get_teacher_dashboard_summary,
)
from apps.dashboard.serializers import TeacherDashboardSummarySerializer
from rest_framework.response import Response
from rest_framework.views import APIView


class TeacherDashboardSummaryAPIView(APIView):
    permission_classes = (IsTeacherDashboardUser,)

    def get(self, request):
        payload = get_teacher_dashboard_summary(
            user=request.user,
            request=request,
        )
        serializer = TeacherDashboardSummarySerializer(payload)

        return Response(serializer.data)
