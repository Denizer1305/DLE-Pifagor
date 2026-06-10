from __future__ import annotations

from apps.testing.models import TestQuestion, TestQuestionOption
from rest_framework import serializers


class TestQuestionOptionReadSerializer(serializers.ModelSerializer):
    """
    Read-сериализатор варианта ответа.
    """

    class Meta:
        model = TestQuestionOption
        fields = (
            "id",
            "question",
            "text",
            "order",
            "is_correct",
            "score",
            "feedback",
            "is_active",
            "created_at",
            "updated_at",
        )


class TestQuestionOptionWriteSerializer(serializers.ModelSerializer):
    """
    Write-сериализатор варианта ответа.
    """

    question_id = serializers.PrimaryKeyRelatedField(
        queryset=TestQuestion.objects.all(),
        source="question",
    )

    class Meta:
        model = TestQuestionOption
        fields = (
            "question_id",
            "text",
            "order",
            "is_correct",
            "score",
            "feedback",
            "is_active",
        )
        extra_kwargs = {
            "order": {"required": False},
            "is_correct": {"required": False},
            "score": {"required": False},
            "feedback": {"required": False},
            "is_active": {"required": False},
        }
