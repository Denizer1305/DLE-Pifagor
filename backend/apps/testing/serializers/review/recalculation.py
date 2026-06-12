from __future__ import annotations

from rest_framework import serializers


class RecalculateAttemptScoreSerializer(serializers.Serializer):
    """
    Serializer действия пересчёта баллов попытки по ответам.
    """

    confirm = serializers.BooleanField(default=True)


class ReviewQueueFilterSerializer(serializers.Serializer):
    """
    Serializer параметров очереди проверки.
    """

    test_id = serializers.IntegerField(
        required=False,
        allow_null=True,
    )
