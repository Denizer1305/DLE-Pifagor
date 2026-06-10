from __future__ import annotations

from apps.testing.models import Test, TestQuestion
from rest_framework import serializers


class TestQuestionWriteSerializer(serializers.ModelSerializer):
    """
    Write-сериализатор вопроса теста.
    """

    test_id = serializers.PrimaryKeyRelatedField(
        queryset=Test.objects.all(),
        source="test",
    )

    class Meta:
        model = TestQuestion
        fields = (
            "test_id",
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
        )
        extra_kwargs = {
            "question_type": {"required": False},
            "check_mode": {"required": False},
            "title": {"required": False},
            "explanation": {"required": False},
            "expected_text_answer": {"required": False},
            "expected_number_answer": {"required": False},
            "case_sensitive": {"required": False},
            "order": {"required": False},
            "score": {"required": False},
            "is_required": {"required": False},
            "is_active": {"required": False},
        }


class QuestionReorderSerializer(serializers.Serializer):
    """
    Сериализатор переупорядочивания вопросов.
    """

    ordered_question_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False,
    )


class OptionReorderSerializer(serializers.Serializer):
    """
    Сериализатор переупорядочивания вариантов ответа.
    """

    ordered_option_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False,
    )
