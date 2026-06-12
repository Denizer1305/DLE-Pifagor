from __future__ import annotations

from apps.organizations.models import Organization, Subject
from apps.testing.models import QuestionBankItem
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class QuestionBankItemWriteSerializer(serializers.ModelSerializer):
    """
    Serializer создания и обновления шаблона вопроса банка.
    """

    organization_id = serializers.PrimaryKeyRelatedField(
        source="organization",
        queryset=Organization.objects.all(),
        write_only=True,
    )
    subject_id = serializers.PrimaryKeyRelatedField(
        source="subject",
        queryset=Subject.objects.all(),
        write_only=True,
    )
    owner_teacher_id = serializers.PrimaryKeyRelatedField(
        source="owner_teacher",
        queryset=User.objects.all(),
        write_only=True,
        required=False,
    )

    class Meta:
        model = QuestionBankItem
        fields = (
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
            "organization_id",
            "subject_id",
            "owner_teacher_id",
            "visibility",
            "is_active",
        )

    def validate(self, attrs):
        """
        Запускает model validation без сохранения.
        """

        attrs = dict(attrs)

        request = self.context.get("request")

        if "owner_teacher" not in attrs and request is not None:
            attrs["owner_teacher"] = request.user

        instance = QuestionBankItem(**attrs)
        instance.full_clean()

        return attrs
