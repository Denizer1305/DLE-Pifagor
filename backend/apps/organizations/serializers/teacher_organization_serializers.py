from __future__ import annotations

from apps.organizations.constants import TeacherEmploymentType
from apps.organizations.models import Organization, TeacherOrganization
from apps.organizations.serializers.organization_serializers import (
    OrganizationShortSerializer,
)
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class TeacherOrganizationListSerializer(serializers.ModelSerializer):
    """
    Связь преподавателя с организацией для списка.
    """

    organization = OrganizationShortSerializer(read_only=True)
    teacher_full_name = serializers.CharField(
        source="teacher.get_full_name",
        read_only=True,
    )
    teacher_email = serializers.EmailField(
        source="teacher.email",
        read_only=True,
    )

    class Meta:
        model = TeacherOrganization
        fields = (
            "id",
            "teacher",
            "teacher_full_name",
            "teacher_email",
            "organization",
            "position",
            "employment_type",
            "is_primary",
            "is_active",
            "starts_at",
            "ends_at",
            "is_current",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields


class TeacherOrganizationDetailSerializer(TeacherOrganizationListSerializer):
    """
    Детальная карточка связи преподавателя с организацией.
    """

    class Meta(TeacherOrganizationListSerializer.Meta):
        fields = TeacherOrganizationListSerializer.Meta.fields + (
            "notes",
        )
        read_only_fields = fields


class TeacherOrganizationWriteSerializer(serializers.Serializer):
    """
    Сериализатор создания и редактирования связи преподавателя с организацией.
    """

    teacher_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="teacher",
        required=False,
    )
    organization_id = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all(),
        source="organization",
        required=False,
    )
    position = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=150,
    )
    employment_type = serializers.ChoiceField(
        required=False,
        choices=TeacherEmploymentType.choices,
    )
    is_primary = serializers.BooleanField(required=False)
    is_active = serializers.BooleanField(required=False)
    starts_at = serializers.DateField(required=False, allow_null=True)
    ends_at = serializers.DateField(required=False, allow_null=True)
    notes = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        """
        Проверяет данные связи преподавателя с организацией.
        """

        if self.context.get("is_create") and not attrs.get("teacher"):
            raise serializers.ValidationError(
                {
                    "teacher_id": "Необходимо указать преподавателя.",
                }
            )

        if self.context.get("is_create") and not attrs.get("organization"):
            raise serializers.ValidationError(
                {
                    "organization_id": "Необходимо указать организацию.",
                }
            )

        starts_at = attrs.get("starts_at")
        ends_at = attrs.get("ends_at")

        if starts_at and ends_at and ends_at < starts_at:
            raise serializers.ValidationError(
                {
                    "ends_at": "Дата окончания не может быть раньше даты начала.",
                }
            )

        return attrs