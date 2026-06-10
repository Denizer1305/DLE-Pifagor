from __future__ import annotations

from apps.materials.models import Material, MaterialUsageLog
from apps.materials.serializers.common_serializers import UserShortSerializer
from apps.materials.serializers.material_serializers import MaterialShortSerializer
from apps.materials.services import log_material_usage
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class MaterialUsageLogReadSerializer(serializers.ModelSerializer):
    """
    Read-сериализатор журнала использования материала.
    """

    material = MaterialShortSerializer(read_only=True)
    user = UserShortSerializer(read_only=True)

    class Meta:
        model = MaterialUsageLog
        fields = (
            "id",
            "material",
            "user",
            "action",
            "context",
            "context_object_id",
            "ip_address",
            "user_agent",
            "metadata",
            "created_at",
        )


class MaterialUsageLogWriteSerializer(serializers.ModelSerializer):
    """
    Write-сериализатор журнала использования материала.
    """

    material_id = serializers.PrimaryKeyRelatedField(
        source="material",
        queryset=Material.objects.all(),
    )
    user_id = serializers.PrimaryKeyRelatedField(
        source="user",
        queryset=User.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = MaterialUsageLog
        fields = (
            "material_id",
            "user_id",
            "action",
            "context",
            "context_object_id",
            "ip_address",
            "user_agent",
            "metadata",
        )

    def create(self, validated_data: dict) -> MaterialUsageLog:
        """
        Создаёт событие использования через сервисный слой.
        """

        request = self.context.get("request")

        return log_material_usage(
            material=validated_data["material"],
            action=validated_data["action"],
            context=validated_data.get(
                "context",
                MaterialUsageLog.ContextChoices.LIBRARY,
            ),
            user=validated_data.get("user"),
            context_object_id=validated_data.get("context_object_id"),
            request=request,
            metadata=validated_data.get("metadata"),
        )


class MaterialUsageLogCreateSerializer(serializers.Serializer):
    """
    Action-сериализатор логирования использования материала.
    """

    action = serializers.ChoiceField(
        choices=MaterialUsageLog.ActionChoices.choices,
    )
    context = serializers.ChoiceField(
        choices=MaterialUsageLog.ContextChoices.choices,
        default=MaterialUsageLog.ContextChoices.LIBRARY,
        required=False,
    )
    context_object_id = serializers.IntegerField(
        required=False,
        allow_null=True,
        min_value=1,
    )
    metadata = serializers.JSONField(
        required=False,
        default=dict,
    )
