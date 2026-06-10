from __future__ import annotations

from rest_framework import serializers


class StartTestAttemptSerializer(serializers.Serializer):
    """
    Action-сериализатор старта попытки.
    """

    test_id = serializers.IntegerField()


class SubmitTestAttemptSerializer(serializers.Serializer):
    """
    Action-сериализатор отправки попытки.
    """

    confirm = serializers.BooleanField(
        required=False,
        default=True,
    )


class ConfirmAttemptResultSerializer(serializers.Serializer):
    """
    Action-сериализатор подтверждения оценки преподавателем.
    """

    final_score = serializers.DecimalField(
        max_digits=8,
        decimal_places=2,
    )
    final_grade = serializers.IntegerField(
        min_value=2,
        max_value=5,
    )
    teacher_comment = serializers.CharField(
        required=False,
        allow_blank=True,
        default="",
    )


class ReviewAttemptAnswerSerializer(serializers.Serializer):
    """
    Action-сериализатор ручной проверки ответа.
    """

    teacher_score = serializers.DecimalField(
        max_digits=8,
        decimal_places=2,
    )
    teacher_comment = serializers.CharField(
        required=False,
        allow_blank=True,
        default="",
    )
