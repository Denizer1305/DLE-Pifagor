from __future__ import annotations

from apps.organizations.models import Department, Organization
from apps.organizations.serializers.organization_serializers import (
    OrganizationShortSerializer,
)
from rest_framework import serializers


class DepartmentShortSerializer(serializers.ModelSerializer):
    """
    Короткое представление отделения.
    """

    class Meta:
        model = Department
        fields = (
            "id",
            "name",
            "short_name",
            "code",
        )
        read_only_fields = fields


class DepartmentListSerializer(serializers.ModelSerializer):
    """
    Отделение для административного списка.
    """

    organization = OrganizationShortSerializer(read_only=True)

    class Meta:
        model = Department
        fields = (
            "id",
            "organization",
            "name",
            "short_name",
            "code",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields


class DepartmentDetailSerializer(serializers.ModelSerializer):
    """
    Детальная карточка отделения.
    """

    organization = OrganizationShortSerializer(read_only=True)

    class Meta:
        model = Department
        fields = (
            "id",
            "organization",
            "name",
            "short_name",
            "code",
            "description",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields


class DepartmentWriteSerializer(serializers.Serializer):
    """
    Сериализатор создания и редактирования отделения.
    """

    organization_id = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all(),
        source="organization",
        required=False,
    )
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
        allow_blank=True,
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

        if self.context.get("is_create") and not attrs.get("organization"):
            raise serializers.ValidationError(
                {
                    "organization_id": "Необходимо указать организацию.",
                }
            )

        if self.context.get("is_create") and not attrs.get("name"):
            raise serializers.ValidationError(
                {
                    "name": "Название отделения обязательно.",
                }
            )

        return attrs
