from __future__ import annotations

from rest_framework import serializers


class TestTakingOptionSerializer(serializers.Serializer):
    """
    Безопасный serializer варианта ответа для прохождения теста.

    Не отдаёт:
    - is_correct;
    - score;
    - feedback.
    """

    id = serializers.IntegerField(read_only=True)
    text = serializers.CharField(read_only=True)
    order = serializers.IntegerField(read_only=True)
