from __future__ import annotations

from apps.organizations.models import GroupCurator, StudyGroup
from apps.organizations.serializers.study_group_serializers import (
    StudyGroupShortSerializer,
)
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class GroupCuratorListSerializer(serializers.ModelSerializer):
    """
    Куратор группы для списка.
    """

    group = StudyGroupShortSerializer(read_only=True)
    teacher_full_name = serializers.CharField(
        source="teacher.get_full_name",
        read_only=True,
    )
    teacher_email = serializers.EmailField(
        source="teacher.email",
        read_only=True,
    )

    class Meta:
        model = GroupCurator
        fields = (
            "id",
            "group",
            "teacher",
            "teacher_full_name",
            "teacher_email",
            "is_primary",
            "is_active",
            "starts_at",
            "ends_at",
            "is_current",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields


class GroupCuratorDetailSerializer(GroupCuratorListSerializer):
    """
    Детальная карточка куратора группы.
    """

    class Meta(GroupCuratorListSerializer.Meta):
        fields = GroupCuratorListSerializer.Meta.fields + ("notes",)
        read_only_fields = fields


class GroupCuratorWriteSerializer(serializers.Serializer):
    """
    Сериализатор создания и редактирования куратора группы.
    """

    group_id = serializers.PrimaryKeyRelatedField(
        queryset=StudyGroup.objects.all(),
        source="group",
        required=False,
    )
    teacher_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="teacher",
        required=False,
    )
    is_primary = serializers.BooleanField(required=False)
    is_active = serializers.BooleanField(required=False)
    starts_at = serializers.DateField(required=False, allow_null=True)
    ends_at = serializers.DateField(required=False, allow_null=True)
    notes = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        """
        Проверяет данные куратора группы.
        """

        if self.context.get("is_create") and not attrs.get("group"):
            raise serializers.ValidationError(
                {
                    "group_id": "Необходимо указать учебную группу.",
                }
            )

        if self.context.get("is_create") and not attrs.get("teacher"):
            raise serializers.ValidationError(
                {
                    "teacher_id": "Необходимо указать куратора.",
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
