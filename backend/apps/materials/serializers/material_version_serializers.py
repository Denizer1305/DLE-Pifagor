from __future__ import annotations

from apps.materials.models import Material, MaterialVersion
from apps.materials.serializers.common_serializers import UserShortSerializer
from apps.materials.services import create_material_version, update_material_version
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class MaterialVersionShortSerializer(serializers.ModelSerializer):
    """
    Краткое представление версии материала.
    """

    class Meta:
        model = MaterialVersion
        fields = (
            "id",
            "version_number",
            "status",
            "is_current",
            "original_filename",
            "mime_type",
            "file_size_bytes",
            "external_url",
            "created_at",
        )


class MaterialVersionReadSerializer(serializers.ModelSerializer):
    """
    Read-сериализатор версии материала.
    """

    created_by = UserShortSerializer(read_only=True)
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = MaterialVersion
        fields = (
            "id",
            "material",
            "version_number",
            "status",
            "file",
            "file_url",
            "external_url",
            "content",
            "original_filename",
            "mime_type",
            "file_size_bytes",
            "checksum",
            "created_by",
            "change_log",
            "is_current",
            "created_at",
            "updated_at",
        )

    def get_file_url(self, obj: MaterialVersion) -> str:
        """
        Возвращает URL файла версии.
        """

        if not obj.file:
            return ""

        request = self.context.get("request")

        if request is None:
            return obj.file.url

        return request.build_absolute_uri(obj.file.url)


class MaterialVersionWriteSerializer(serializers.ModelSerializer):
    """
    Write-сериализатор версии материала.
    """

    material_id = serializers.PrimaryKeyRelatedField(
        source="material",
        queryset=Material.objects.all(),
    )
    created_by_id = serializers.PrimaryKeyRelatedField(
        source="created_by",
        queryset=User.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = MaterialVersion
        fields = (
            "material_id",
            "version_number",
            "status",
            "file",
            "external_url",
            "content",
            "original_filename",
            "mime_type",
            "file_size_bytes",
            "checksum",
            "created_by_id",
            "change_log",
            "is_current",
        )

    def validate(self, attrs: dict) -> dict:
        """
        Дополняет автора версии из request, если он не передан явно.
        """

        request = self.context.get("request")

        if request and request.user.is_authenticated:
            attrs.setdefault("created_by", request.user)

        return attrs

    def create(self, validated_data: dict) -> MaterialVersion:
        """
        Создаёт версию материала через сервисный слой.
        """

        return create_material_version(data=validated_data)

    def update(
        self,
        instance: MaterialVersion,
        validated_data: dict,
    ) -> MaterialVersion:
        """
        Обновляет версию материала через сервисный слой.
        """

        return update_material_version(
            version=instance,
            data=validated_data,
        )


class MaterialVersionSetCurrentSerializer(serializers.Serializer):
    """
    Action-сериализатор назначения текущей версии.
    """

    confirm = serializers.BooleanField(
        required=False,
        default=True,
    )
