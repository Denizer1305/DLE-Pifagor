from __future__ import annotations

from apps.materials.models import Material, MaterialCategory, MaterialVersion
from apps.materials.serializers.common_serializers import (
    OrganizationShortSerializer,
    SubjectShortSerializer,
    UserShortSerializer,
)
from apps.materials.serializers.material_category_serializers import (
    MaterialCategoryShortSerializer,
)
from apps.materials.serializers.material_version_serializers import (
    MaterialVersionShortSerializer,
)
from apps.materials.services import create_material, update_material
from apps.organizations.models import Organization, Subject
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class MaterialShortSerializer(serializers.ModelSerializer):
    """
    Краткое представление учебного материала.
    """

    current_version = MaterialVersionShortSerializer(read_only=True)

    class Meta:
        model = Material
        fields = (
            "id",
            "uid",
            "title",
            "slug",
            "material_type",
            "status",
            "visibility",
            "source",
            "is_active",
            "current_version",
        )


class MaterialReadSerializer(serializers.ModelSerializer):
    """
    Read-сериализатор учебного материала.
    """

    organization = OrganizationShortSerializer(read_only=True)
    subject = SubjectShortSerializer(read_only=True)
    category = MaterialCategoryShortSerializer(read_only=True)
    owner = UserShortSerializer(read_only=True)
    current_version = MaterialVersionShortSerializer(read_only=True)

    versions_count = serializers.SerializerMethodField()
    usage_logs_count = serializers.SerializerMethodField()
    preview_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Material
        fields = (
            "id",
            "uid",
            "title",
            "slug",
            "short_description",
            "description",
            "material_type",
            "status",
            "visibility",
            "source",
            "organization",
            "subject",
            "category",
            "owner",
            "current_version",
            "tags",
            "preview_image",
            "preview_image_url",
            "is_active",
            "published_at",
            "archived_at",
            "versions_count",
            "usage_logs_count",
            "created_at",
            "updated_at",
        )

    def get_versions_count(self, obj: Material) -> int:
        """
        Возвращает количество версий материала.
        """

        return obj.versions.count()

    def get_usage_logs_count(self, obj: Material) -> int:
        """
        Возвращает количество событий использования материала.
        """

        return obj.usage_logs.count()

    def get_preview_image_url(self, obj: Material) -> str:
        """
        Возвращает URL изображения предпросмотра.
        """

        if not obj.preview_image:
            return ""

        request = self.context.get("request")

        if request is None:
            return obj.preview_image.url

        return request.build_absolute_uri(obj.preview_image.url)


class MaterialWriteSerializer(serializers.ModelSerializer):
    """
    Write-сериализатор учебного материала.
    """

    organization_id = serializers.PrimaryKeyRelatedField(
        source="organization",
        queryset=Organization.objects.all(),
        required=False,
        allow_null=True,
    )
    subject_id = serializers.PrimaryKeyRelatedField(
        source="subject",
        queryset=Subject.objects.all(),
        required=False,
        allow_null=True,
    )
    category_id = serializers.PrimaryKeyRelatedField(
        source="category",
        queryset=MaterialCategory.objects.all(),
        required=False,
        allow_null=True,
    )
    owner_id = serializers.PrimaryKeyRelatedField(
        source="owner",
        queryset=User.objects.all(),
        required=False,
        allow_null=True,
    )
    current_version_id = serializers.PrimaryKeyRelatedField(
        source="current_version",
        queryset=MaterialVersion.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Material
        fields = (
            "title",
            "slug",
            "short_description",
            "description",
            "material_type",
            "status",
            "visibility",
            "source",
            "organization_id",
            "subject_id",
            "category_id",
            "owner_id",
            "current_version_id",
            "tags",
            "preview_image",
            "is_active",
        )

    def validate(self, attrs: dict) -> dict:
        """
        Дополняет владельца из request, если он не передан явно.
        """

        request = self.context.get("request")

        if request and request.user.is_authenticated:
            attrs.setdefault("owner", request.user)

        return attrs

    def create(self, validated_data: dict) -> Material:
        """
        Создаёт материал через сервисный слой.
        """

        return create_material(data=validated_data)

    def update(
        self,
        instance: Material,
        validated_data: dict,
    ) -> Material:
        """
        Обновляет материал через сервисный слой.
        """

        return update_material(
            material=instance,
            data=validated_data,
        )


class MaterialStatusActionSerializer(serializers.Serializer):
    """
    Action-сериализатор изменения статуса материала.
    """

    confirm = serializers.BooleanField(
        required=False,
        default=True,
    )


class MaterialCreateWithVersionSerializer(serializers.Serializer):
    """
    Сериализатор создания материала вместе с первой версией.
    """

    title = serializers.CharField(max_length=255)
    slug = serializers.SlugField(max_length=120)
    short_description = serializers.CharField(
        max_length=500,
        required=False,
        allow_blank=True,
    )
    description = serializers.CharField(
        required=False,
        allow_blank=True,
    )
    material_type = serializers.ChoiceField(
        choices=Material.MaterialTypeChoices.choices,
    )
    visibility = serializers.ChoiceField(
        choices=Material.VisibilityChoices.choices,
        default=Material.VisibilityChoices.PRIVATE,
    )
    source = serializers.ChoiceField(
        choices=Material.SourceChoices.choices,
        default=Material.SourceChoices.MANUAL,
    )

    organization_id = serializers.PrimaryKeyRelatedField(
        source="organization",
        queryset=Organization.objects.all(),
        required=False,
        allow_null=True,
    )
    subject_id = serializers.PrimaryKeyRelatedField(
        source="subject",
        queryset=Subject.objects.all(),
        required=False,
        allow_null=True,
    )
    category_id = serializers.PrimaryKeyRelatedField(
        source="category",
        queryset=MaterialCategory.objects.all(),
        required=False,
        allow_null=True,
    )

    tags = serializers.ListField(
        child=serializers.CharField(max_length=64),
        required=False,
        default=list,
    )
    preview_image = serializers.FileField(
        required=False,
        allow_null=True,
    )

    file = serializers.FileField(
        required=False,
        allow_null=True,
    )
    external_url = serializers.URLField(
        required=False,
        allow_blank=True,
    )
    content = serializers.CharField(
        required=False,
        allow_blank=True,
    )
    change_log = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=1000,
    )
