from __future__ import annotations

from apps.testing.models import (
    TestAttempt,
    TestAttemptAnswer,
    TestQuestion,
    TestQuestionOption,
)
from rest_framework import serializers


class TestAttemptAnswerWriteSerializer(serializers.ModelSerializer):
    """
    Write-сериализатор ответа на вопрос теста.
    """

    attempt_id = serializers.PrimaryKeyRelatedField(
        queryset=TestAttempt.objects.all(),
        source="attempt",
    )
    question_id = serializers.PrimaryKeyRelatedField(
        queryset=TestQuestion.objects.all(),
        source="question",
    )
    selected_option_id = serializers.PrimaryKeyRelatedField(
        queryset=TestQuestionOption.objects.all(),
        source="selected_option",
        required=False,
        allow_null=True,
    )

    class Meta:
        model = TestAttemptAnswer
        fields = (
            "attempt_id",
            "question_id",
            "selected_option_id",
            "selected_options_data",
            "text_answer",
            "number_answer",
        )
        extra_kwargs = {
            "selected_options_data": {
                "required": False,
            },
            "text_answer": {
                "required": False,
                "allow_blank": True,
            },
            "number_answer": {
                "required": False,
                "allow_null": True,
            },
        }


class SaveAttemptAnswerSerializer(serializers.Serializer):
    """
    Action-сериализатор сохранения одного ответа.
    """

    question_id = serializers.IntegerField()
    selected_option_id = serializers.IntegerField(
        required=False,
        allow_null=True,
    )
    selected_options_data = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        default=list,
    )
    text_answer = serializers.CharField(
        required=False,
        allow_blank=True,
        default="",
    )
    number_answer = serializers.DecimalField(
        max_digits=12,
        decimal_places=4,
        required=False,
        allow_null=True,
    )


class SaveAttemptAnswersSerializer(serializers.Serializer):
    """
    Action-сериализатор сохранения набора ответов.
    """

    answers = SaveAttemptAnswerSerializer(
        many=True,
        allow_empty=False,
    )
