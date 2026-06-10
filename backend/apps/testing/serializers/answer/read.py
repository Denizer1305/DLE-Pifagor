from __future__ import annotations

from apps.testing.models import TestAttemptAnswer
from rest_framework import serializers


class TestAttemptAnswerReadSerializer(serializers.ModelSerializer):
    """
    Read-сериализатор ответа на вопрос теста.
    """

    question_text = serializers.CharField(
        source="question.text",
        read_only=True,
    )
    question_type = serializers.CharField(
        source="question.question_type",
        read_only=True,
    )
    selected_option_text = serializers.CharField(
        source="selected_option.text",
        read_only=True,
        allow_null=True,
    )

    class Meta:
        model = TestAttemptAnswer
        fields = (
            "id",
            "attempt",
            "question",
            "question_text",
            "question_type",
            "selected_option",
            "selected_option_text",
            "selected_options_data",
            "text_answer",
            "number_answer",
            "is_correct",
            "auto_score",
            "teacher_score",
            "final_score",
            "requires_manual_review",
            "teacher_comment",
            "created_at",
            "updated_at",
        )
