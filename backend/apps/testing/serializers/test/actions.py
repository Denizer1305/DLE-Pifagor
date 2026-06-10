from __future__ import annotations

from rest_framework import serializers


class TestStatusActionSerializer(serializers.Serializer):
    """
    Action-сериализатор смены статуса теста.
    """

    confirm = serializers.BooleanField(
        required=False,
        default=True,
    )
