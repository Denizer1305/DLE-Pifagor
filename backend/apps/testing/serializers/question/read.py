from __future__ import annotations

from apps.testing.models import TestQuestion
from apps.testing.serializers.question.option import TestQuestionOptionReadSerializer
from rest_framework import serializers


class TestQuestionReadSerializer(serializers.ModelSerializer):
    """
    Read-сериализатор вопроса теста.
    """

    source_bank_item_title = serializers.CharField(
        source="source_bank_item.title",
        read_only=True,
        allow_null=True,
    )
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
            "source_bank_item",
            "source_bank_item_title",
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
            "difficulty",
            "tags_data",
            "is_reusable",
            "is_required",
            "is_active",
            "created_at",
            "updated_at",
            "options",
        )
        read_only_fields = fields
