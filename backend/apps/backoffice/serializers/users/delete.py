from __future__ import annotations

from rest_framework import serializers


class BackofficeUserDeleteSerializer(serializers.Serializer):
    """
    Serializer планирования удаления пользователя.
    """

    reason = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=500,
    )
    scheduled_for_deletion_at = serializers.DateTimeField(
        required=False,
        allow_null=True,
    )
    expected_updated_at = serializers.DateTimeField(
        required=False,
        write_only=True,
    )
