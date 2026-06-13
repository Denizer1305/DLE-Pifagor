from __future__ import annotations

from apps.testing.models import Test
from rest_framework import serializers


class CopyBankItemToTestSerializer(serializers.Serializer):
    """
    Serializer действия копирования шаблона вопроса в тест.
    """

    test_id = serializers.PrimaryKeyRelatedField(
        source="test",
        queryset=Test.objects.all(),
    )
    order = serializers.IntegerField(
        min_value=1,
        required=False,
        allow_null=True,
    )


class DuplicateBankItemSerializer(serializers.Serializer):
    """
    Serializer действия дублирования шаблона вопроса.
    """

    title = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
    )


class BankItemStatusActionSerializer(serializers.Serializer):
    """
    Serializer действий публикации, архивации и восстановления шаблона.
    """

    comment = serializers.CharField(
        required=False,
        allow_blank=True,
    )
