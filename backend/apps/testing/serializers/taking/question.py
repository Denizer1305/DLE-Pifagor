from __future__ import annotations

from rest_framework import serializers

from .option import TestTakingOptionSerializer


class TestTakingQuestionSerializer(serializers.Serializer):
    """
    Безопасный serializer вопроса для прохождения теста.

    Не отдаёт:
    - expected_text_answer;
    - expected_number_answer;
    - source_bank_item;
    - правильные варианты.
    """

    id = serializers.IntegerField(read_only=True)
    question_type = serializers.CharField(read_only=True)
    check_mode = serializers.CharField(read_only=True)
    title = serializers.CharField(read_only=True, allow_blank=True)
    text = serializers.CharField(read_only=True)
    order = serializers.IntegerField(read_only=True)
    score = serializers.IntegerField(read_only=True)
    is_required = serializers.BooleanField(read_only=True)
    options = TestTakingOptionSerializer(
        many=True,
        read_only=True,
    )
