from __future__ import annotations

from apps.testing.models import TestQuestion
from apps.testing.serializers.question.option import TestQuestionOptionReadSerializer
from rest_framework import serializers


class TestQuestionReadSerializer(serializers.ModelSerializer):
    """
    Read-сериализатор вопроса теста.
    """

    test_title = serializers.CharField(
        source="test.title",
        read_only=True,
    )
    options = TestQuestionOptionReadSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = TestQuestion
        fields = (
            "id",
            "test",
            "test_title",
            "question_type",
            "check_mode",
            "title",
            "text",
            "explanation",
            "expected_text_answer",
            "expected_number_answer",
            "case_sensitive",
            "order",
            "score",
            "is_required",
            "is_active",
            "options",
            "created_at",
            "updated_at",
        )
