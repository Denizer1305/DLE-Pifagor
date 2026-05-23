from __future__ import annotations

from apps.dashboard.permissions import IsPlatformAdmin
from apps.dashboard.selectors import get_admin_dashboard_summary
from apps.dashboard.serializers import AdminDashboardSummarySerializer
from rest_framework.response import Response
from rest_framework.views import APIView


class AdminDashboardSummaryAPIView(APIView):
    """
    Агрегированная сводка главной страницы администратора.
    """

    permission_classes = (IsPlatformAdmin,)

    def get(self, request):
        payload = get_admin_dashboard_summary(
            user=request.user,
            request=request,
        )

        serializer = AdminDashboardSummarySerializer(payload)

        return Response(serializer.data)
