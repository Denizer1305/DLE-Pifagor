from __future__ import annotations

from rest_framework import serializers


class TestTakingAnswerSerializer(serializers.Serializer):
    """
    Serializer одного ответа обучающегося при прохождении теста.
    """

    question_id = serializers.IntegerField()
    selected_option_id = serializers.IntegerField(
        required=False,
        allow_null=True,
    )
    selected_options_data = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        allow_empty=True,
    )
    text_answer = serializers.CharField(
        required=False,
        allow_blank=True,
    )
    number_answer = serializers.DecimalField(
        max_digits=12,
        decimal_places=4,
        required=False,
        allow_null=True,
    )


class TestTakingSaveAnswersSerializer(serializers.Serializer):
    """
    Serializer сохранения набора ответов обучающегося.
    """

    attempt_id = serializers.IntegerField()
    answers = TestTakingAnswerSerializer(many=True)


class TestTakingSubmitSerializer(serializers.Serializer):
    """
    Serializer отправки попытки.
    """

    confirm = serializers.BooleanField(default=True)
