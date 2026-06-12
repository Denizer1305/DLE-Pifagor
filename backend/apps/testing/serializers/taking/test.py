from __future__ import annotations

from rest_framework import serializers

from .question import TestTakingQuestionSerializer


class TestTakingInfoSerializer(serializers.Serializer):
    """
    Serializer общей информации о тесте для прохождения.
    """

    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True, allow_blank=True)
    instructions = serializers.CharField(read_only=True, allow_blank=True)
    time_limit_minutes = serializers.IntegerField(
        read_only=True,
        allow_null=True,
    )
    shuffle_questions = serializers.BooleanField(read_only=True)
    shuffle_options = serializers.BooleanField(read_only=True)


class TestTakingAttemptSerializer(serializers.Serializer):
    """
    Serializer попытки в payload прохождения теста.
    """

    id = serializers.IntegerField(read_only=True)
    attempt_number = serializers.IntegerField(read_only=True)
    status = serializers.CharField(read_only=True)
    started_at = serializers.DateTimeField(read_only=True)
    expires_at = serializers.DateTimeField(
        read_only=True,
        allow_null=True,
    )


class TestTakingPayloadSerializer(serializers.Serializer):
    """
    Serializer полного payload прохождения теста.
    """

    test = TestTakingInfoSerializer(read_only=True)
    attempt = TestTakingAttemptSerializer(read_only=True)
    questions = TestTakingQuestionSerializer(
        many=True,
        read_only=True,
    )
