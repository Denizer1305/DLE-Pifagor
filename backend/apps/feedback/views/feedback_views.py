from __future__ import annotations

from apps.feedback.models import FeedbackRequest
from apps.feedback.serializers import FeedbackRequestCreateSerializer
from apps.feedback.services import create_feedback_request
from apps.feedback.throttles import ContactFeedbackThrottle
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import status
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


def get_request_files_list(request, field_name: str = "attachments") -> list:
    if hasattr(request, "FILES") and hasattr(request.FILES, "getlist"):
        return request.FILES.getlist(field_name)

    return []


def build_serializer_input_data(request, field_name: str = "attachments"):
    data = request.data.copy()
    files = get_request_files_list(request, field_name=field_name)

    if hasattr(data, "setlist"):
        data.setlist(field_name, files)
    else:
        data[field_name] = files

    return data


class ContactFeedbackCreateAPIView(APIView):
    permission_classes = (AllowAny,)
    throttle_classes = (ContactFeedbackThrottle,)
    throttle_scope = "contact_feedback"
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def post(self, request):
        serializer = FeedbackRequestCreateSerializer(
            data=build_serializer_input_data(request),
            context={
                "request": request,
            },
        )
        serializer.is_valid(raise_exception=True)

        try:
            feedback_request = create_feedback_request(
                request=request,
                topic=serializer.validated_data.get(
                    "topic",
                    FeedbackRequest.TopicChoices.QUESTION,
                ),
                full_name=serializer.validated_data["full_name"],
                email=serializer.validated_data["email"],
                phone=serializer.validated_data.get("phone", ""),
                organization_name=serializer.validated_data.get(
                    "organization_name",
                    "",
                ),
                subject=serializer.validated_data.get("subject", ""),
                message=serializer.validated_data["message"],
                is_personal_data_consent=serializer.validated_data[
                    "is_personal_data_consent"
                ],
                source=FeedbackRequest.SourceChoices.CONTACTS_PAGE,
                page_url=serializer.validated_data.get("page_url", ""),
                frontend_route=serializer.validated_data.get("frontend_route", ""),
                files=serializer.validated_data.get("attachments", []),
            )
        except DjangoValidationError as error:
            payload = (
                error.message_dict
                if hasattr(error, "message_dict")
                else {
                    "detail": error.messages,
                }
            )
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {
                "id": feedback_request.id,
                "status": feedback_request.status,
                "message": "Спасибо! Ваше сообщение отправлено.",
            },
            status=status.HTTP_201_CREATED,
        )
