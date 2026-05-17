from __future__ import annotations

from apps.users.models import UserJoinRequest
from apps.users.serializers.user_serializers import UserShortSerializer
from rest_framework import serializers


class UserJoinRequestSerializer(serializers.ModelSerializer):
    """
    Сериализатор заявки пользователя.
    """

    user = UserShortSerializer(read_only=True)
    target_user = UserShortSerializer(read_only=True)
    reviewed_by = UserShortSerializer(read_only=True)

    class Meta:
        model = UserJoinRequest
        fields = [
            "id",
            "request_type",
            "user",
            "target_user",
            "organization",
            "department",
            "group",
            "status",
            "message",
            "review_comment",
            "reviewed_by",
            "reviewed_at",
            "expires_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "request_type",
            "user",
            "target_user",
            "organization",
            "department",
            "group",
            "status",
            "review_comment",
            "reviewed_by",
            "reviewed_at",
            "created_at",
            "updated_at",
        ]


class JoinRequestReviewSerializer(serializers.Serializer):
    """
    Сериализатор подтверждения или отклонения заявки.
    """

    comment = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=1000,
    )
