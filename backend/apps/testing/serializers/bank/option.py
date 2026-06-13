from __future__ import annotations

from apps.testing.models import QuestionBankOption
from rest_framework import serializers


class QuestionBankOptionReadSerializer(serializers.ModelSerializer):
    """
    Serializer чтения варианта ответа шаблона вопроса.
    """

    class Meta:
        model = QuestionBankOption
        fields = (
            "id",
            "bank_item",
            "text",
            "order",
            "is_correct",
            "score",
            "feedback",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields


class QuestionBankOptionWriteSerializer(serializers.ModelSerializer):
    """
    Serializer создания и обновления варианта ответа шаблона вопроса.
    """

    bank_item_id = serializers.PrimaryKeyRelatedField(
        source="bank_item",
        queryset=QuestionBankOption._meta.get_field(
            "bank_item",
        ).remote_field.model.objects.all(),
        write_only=True,
    )

    class Meta:
        model = QuestionBankOption
        fields = (
            "bank_item_id",
            "text",
            "order",
            "is_correct",
            "score",
            "feedback",
            "is_active",
        )

    def validate(self, attrs):
        """
        Запускает model validation без сохранения.
        """

        instance = QuestionBankOption(**attrs)
        instance.full_clean()

        return attrs
