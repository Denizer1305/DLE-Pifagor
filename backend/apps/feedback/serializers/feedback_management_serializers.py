from __future__ import annotations

from apps.feedback.models import FeedbackAttachment, FeedbackRequest
from rest_framework import serializers


class FeedbackAdminAttachmentSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = FeedbackAttachment
        fields = (
            "id",
            "original_name",
            "mime_type",
            "file_size",
            "kind",
            "url",
        )

    def get_url(self, obj: FeedbackAttachment) -> str:
        if not obj.file:
            return ""

        request = self.context.get("request")
        url = obj.file.url

        return request.build_absolute_uri(url) if request else url


class FeedbackAdminRequestSerializer(serializers.ModelSerializer):
    attachment_count = serializers.IntegerField(read_only=True)
    attachments = FeedbackAdminAttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = FeedbackRequest
        fields = (
            "id",
            "topic",
            "source",
            "status",
            "full_name",
            "email",
            "phone",
            "organization_name",
            "subject",
            "message",
            "page_url",
            "attachment_count",
            "attachments",
            "created_at",
            "updated_at",
        )


class FeedbackAdminSummarySerializer(serializers.Serializer):
    total = serializers.IntegerField()
    new = serializers.IntegerField()
    in_progress = serializers.IntegerField()
    answered = serializers.IntegerField()
    closed = serializers.IntegerField()


class FeedbackAdminListResponseSerializer(serializers.Serializer):
    summary = FeedbackAdminSummarySerializer()
    items = FeedbackAdminRequestSerializer(many=True)


class FeedbackStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=FeedbackRequest.StatusChoices.choices)
