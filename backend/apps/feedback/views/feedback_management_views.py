from __future__ import annotations

from apps.dashboard.permissions import IsPlatformAdmin
from apps.feedback.selectors import (
    get_feedback_requests_queryset,
    get_feedback_summary_payload,
)
from apps.feedback.serializers import (
    FeedbackAdminListResponseSerializer,
    FeedbackAdminRequestSerializer,
    FeedbackStatusUpdateSerializer,
)
from apps.feedback.services import update_feedback_status
from rest_framework.response import Response
from rest_framework.views import APIView


class FeedbackAdminListAPIView(APIView):
    permission_classes = (IsPlatformAdmin,)

    def get(self, request):
        queryset = get_feedback_requests_queryset(
            status=request.query_params.get("status", ""),
            topic=request.query_params.get("topic", ""),
            search=request.query_params.get("search", "").strip(),
        )[:100]
        payload = {
            "summary": get_feedback_summary_payload(),
            "items": queryset,
        }

        serializer = FeedbackAdminListResponseSerializer(
            payload,
            context={"request": request},
        )

        return Response(serializer.data)


class FeedbackAdminStatusAPIView(APIView):
    permission_classes = (IsPlatformAdmin,)

    def patch(self, request, request_id: int):
        serializer = FeedbackStatusUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        feedback_request = update_feedback_status(
            request_id=request_id,
            status=serializer.validated_data["status"],
        )
        feedback_request.attachment_count = feedback_request.attachments.count()

        serializer = FeedbackAdminRequestSerializer(
            feedback_request,
            context={"request": request},
        )

        return Response(serializer.data)
