from __future__ import annotations

from apps.organizations.models import Subject
from rest_framework import serializers


class SubjectShortSerializer(serializers.ModelSerializer):
    """
    Короткое представление учебного предмета.
    """

    class Meta:
        model = Subject
        fields = (
            "id",
            "name",
            "short_name",
            "code",
        )
        read_only_fields = fields


class SubjectListSerializer(serializers.ModelSerializer):
    """
    Учебный предмет для административного списка.
    """

    class Meta:
        model = Subject
        fields = (
            "id",
            "name",
            "short_name",
            "code",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields


class SubjectDetailSerializer(serializers.ModelSerializer):
    """
    Детальная карточка учебного предмета.
    """

    class Meta:
        model = Subject
        fields = (
            "id",
            "name",
            "short_name",
            "code",
            "description",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields


class SubjectWriteSerializer(serializers.Serializer):
    """
    Сериализатор создания и редактирования учебного предмета.
    """

    name = serializers.CharField(
        required=False,
        max_length=255,
    )
    short_name = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=120,
    )
    code = serializers.CharField(
        required=False,
        max_length=64,
    )
    description = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    def validate(self, attrs):
        """
        Проверяет обязательные поля при создании.
        """

        if self.context.get("is_create") and not attrs.get("name"):
            raise serializers.ValidationError(
                {
                    "name": "Название учебного предмета обязательно.",
                }
            )

        if self.context.get("is_create") and not attrs.get("code"):
            raise serializers.ValidationError(
                {
                    "code": "Код учебного предмета обязателен.",
                }
            )

        return attrs