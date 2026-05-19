from __future__ import annotations

from rest_framework import serializers

from apps.feedback.models import FeedbackRequest
from apps.feedback.validators import (
    validate_feedback_attachments_count,
    validate_feedback_message,
    validate_feedback_name,
    validate_feedback_topic_text,
)


class FeedbackRequestCreateSerializer(serializers.Serializer):
    topic = serializers.ChoiceField(
        choices=FeedbackRequest.TopicChoices.choices,
        default=FeedbackRequest.TopicChoices.QUESTION,
    )
    full_name = serializers.CharField(
        max_length=255,
    )
    email = serializers.EmailField()
    phone = serializers.CharField(
        max_length=32,
        required=False,
        allow_blank=True,
    )
    organization_name = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
    )
    subject = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
    )
    message = serializers.CharField()
    is_personal_data_consent = serializers.BooleanField()
    page_url = serializers.URLField(
        required=False,
        allow_blank=True,
    )
    frontend_route = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
    )
    attachments = serializers.ListField(
        child=serializers.FileField(),
        required=False,
        allow_empty=True,
        write_only=True,
    )

    def validate_full_name(self, value: str) -> str:
        return validate_feedback_name(value)

    def validate_subject(self, value: str) -> str:
        return validate_feedback_topic_text(value)

    def validate_organization_name(self, value: str) -> str:
        return validate_feedback_topic_text(value)

    def validate_message(self, value: str) -> str:
        return validate_feedback_message(value)

    def validate(self, attrs):
        if not attrs.get("is_personal_data_consent"):
            raise serializers.ValidationError(
                {
                    "is_personal_data_consent": (
                        "Необходимо согласие на обработку персональных данных."
                    )
                }
            )

        validate_feedback_attachments_count(attrs.get("attachments") or [])

        return attrs


class FeedbackRequestCreateResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    message = serializers.CharField()
    status = serializers.CharField()