from __future__ import annotations

from apps.dashboard.permissions import IsParentDashboardUser
from apps.dashboard.selectors.parent_dashboard_selectors import (
    get_parent_dashboard_summary,
)
from apps.dashboard.serializers import ParentDashboardSummarySerializer
from rest_framework.response import Response
from rest_framework.views import APIView


class ParentDashboardSummaryAPIView(APIView):
    permission_classes = (IsParentDashboardUser,)

    def get(self, request):
        payload = get_parent_dashboard_summary(
            user=request.user,
            request=request,
        )
        serializer = ParentDashboardSummarySerializer(payload)

        return Response(serializer.data)
