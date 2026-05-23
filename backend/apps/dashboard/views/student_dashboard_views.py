from __future__ import annotations

from apps.dashboard.permissions import IsStudentDashboardUser
from apps.dashboard.selectors.student_dashboard_selectors import (
    get_student_dashboard_summary,
)
from apps.dashboard.serializers import StudentDashboardSummarySerializer
from rest_framework.response import Response
from rest_framework.views import APIView


class StudentDashboardSummaryAPIView(APIView):
    permission_classes = (IsStudentDashboardUser,)

    def get(self, request):
        payload = get_student_dashboard_summary(
            user=request.user,
            request=request,
        )
        serializer = StudentDashboardSummarySerializer(payload)

        return Response(serializer.data)
