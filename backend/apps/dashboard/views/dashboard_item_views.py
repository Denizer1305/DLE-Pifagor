from __future__ import annotations

from apps.dashboard.selectors.dashboard_item_selectors import (
    get_dashboard_item_for_user,
    get_dashboard_items_for_user,
)
from apps.dashboard.serializers.dashboard_item_serializers import (
    DashboardItemCreateSerializer,
    DashboardItemSerializer,
)
from apps.dashboard.services.dashboard_item_services import (
    create_dashboard_item,
    delete_dashboard_item,
)
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class DashboardItemListCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        items = get_dashboard_items_for_user(user=request.user)

        return Response(DashboardItemSerializer(items, many=True).data)

    def post(self, request):
        serializer = DashboardItemCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item = create_dashboard_item(
            user=request.user,
            validated_data=serializer.validated_data,
        )

        return Response(
            DashboardItemSerializer(item).data,
            status=status.HTTP_201_CREATED,
        )


class DashboardItemDetailAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, item_id):
        item = get_dashboard_item_for_user(user=request.user, item_id=item_id)

        if not item:
            return Response(status=status.HTTP_404_NOT_FOUND)

        delete_dashboard_item(item=item)

        return Response(status=status.HTTP_204_NO_CONTENT)
