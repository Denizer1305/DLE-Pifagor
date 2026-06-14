from __future__ import annotations

from rest_framework import serializers


class BackofficeUserStatusActionSerializer(serializers.Serializer):
    """
    Serializer действия над статусом пользователя.

    Используется для:
    - block;
    - unblock;
    - archive;
    - restore.
    """

    reason = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=500,
    )
    expected_updated_at = serializers.DateTimeField(
        required=False,
        write_only=True,
    )
