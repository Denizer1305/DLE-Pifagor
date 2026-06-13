from __future__ import annotations

from apps.testing.models import QuestionBankItem
from rest_framework import serializers

from .option import QuestionBankOptionReadSerializer


class QuestionBankItemReadSerializer(serializers.ModelSerializer):
    """
    Serializer чтения шаблона вопроса банка тестовых заданий.
    """

    organization_title = serializers.CharField(
        source="organization.title",
        read_only=True,
    )
    subject_title = serializers.CharField(
        source="subject.title",
        read_only=True,
    )
    owner_teacher_email = serializers.EmailField(
        source="owner_teacher.email",
        read_only=True,
    )
    options = QuestionBankOptionReadSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = QuestionBankItem
        fields = (
            "id",
            "title",
            "text",
            "explanation",
            "question_type",
            "check_mode",
            "expected_text_answer",
            "expected_number_answer",
            "case_sensitive",
            "score",
            "difficulty",
            "tags_data",
            "organization",
            "organization_title",
            "subject",
            "subject_title",
            "owner_teacher",
            "owner_teacher_email",
            "visibility",
            "status",
            "is_active",
            "published_at",
            "archived_at",
            "created_at",
            "updated_at",
            "options",
        )
        read_only_fields = fields
