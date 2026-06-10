from __future__ import annotations

from apps.materials.models import MaterialCategory
from apps.materials.serializers.common_serializers import OrganizationShortSerializer
from apps.materials.services import create_material_category, update_material_category
from apps.organizations.models import Organization
from rest_framework import serializers


class MaterialCategoryShortSerializer(serializers.ModelSerializer):
    """
    Краткое представление категории материала.
    """

    class Meta:
        model = MaterialCategory
        fields = (
            "id",
            "name",
            "slug",
            "is_active",
        )


class MaterialCategoryReadSerializer(serializers.ModelSerializer):
    """
    Read-сериализатор категории материалов.
    """

    organization = OrganizationShortSerializer(read_only=True)
    parent = MaterialCategoryShortSerializer(read_only=True)

    materials_count = serializers.SerializerMethodField()
    children_count = serializers.SerializerMethodField()

    class Meta:
        model = MaterialCategory
        fields = (
            "id",
            "organization",
            "parent",
            "name",
            "slug",
            "description",
            "is_active",
            "materials_count",
            "children_count",
            "created_at",
            "updated_at",
        )

    def get_materials_count(self, obj: MaterialCategory) -> int:
        """
        Возвращает количество материалов категории.
        """

        return obj.materials.count()

    def get_children_count(self, obj: MaterialCategory) -> int:
        """
        Возвращает количество дочерних категорий.
        """

        return obj.children.count()


class MaterialCategoryWriteSerializer(serializers.ModelSerializer):
    """
    Write-сериализатор категории материалов.

    organization_id и parent_id объявлены как IntegerField, а не как
    PrimaryKeyRelatedField, чтобы глобальные категории можно было создавать
    без organization_id.
    """

    organization_id = serializers.IntegerField(
        required=False,
        allow_null=True,
    )
    parent_id = serializers.IntegerField(
        required=False,
        allow_null=True,
    )

    class Meta:
        model = MaterialCategory
        fields = (
            "organization_id",
            "parent_id",
            "name",
            "slug",
            "description",
            "is_active",
        )
        extra_kwargs = {
            "description": {
                "required": False,
                "allow_blank": True,
            },
            "is_active": {
                "required": False,
            },
        }

    def validate_organization_id(
        self,
        value: int | None,
    ) -> int | None:
        """
        Проверяет существование организации, если она передана.
        """

        if value is None:
            return value

        if not Organization.objects.filter(id=value).exists():
            raise serializers.ValidationError("Организация не найдена.")

        return value

    def validate_parent_id(
        self,
        value: int | None,
    ) -> int | None:
        """
        Проверяет существование родительской категории, если она передана.
        """

        if value is None:
            return value

        if not MaterialCategory.objects.filter(id=value).exists():
            raise serializers.ValidationError("Родительская категория не найдена.")

        return value

    def validate(self, attrs: dict) -> dict:
        """
        Проверяет согласованность организации и родительской категории.
        """

        organization_id = attrs.get("organization_id")
        parent_id = attrs.get("parent_id")

        if parent_id is None:
            return attrs

        parent = MaterialCategory.objects.get(id=parent_id)

        if organization_id is None and parent.organization_id is not None:
            raise serializers.ValidationError(
                {
                    "parent_id": (
                        "Глобальная категория не может иметь родителя "
                        "из конкретной организации."
                    )
                }
            )

        if (
            organization_id is not None
            and parent.organization_id is not None
            and parent.organization_id != organization_id
        ):
            raise serializers.ValidationError(
                {
                    "parent_id": (
                        "Родительская категория должна относиться "
                        "к той же организации."
                    )
                }
            )

        return attrs

    def create(self, validated_data: dict) -> MaterialCategory:
        """
        Создаёт категорию через сервисный слой.
        """

        return create_material_category(data=validated_data)

    def update(
        self,
        instance: MaterialCategory,
        validated_data: dict,
    ) -> MaterialCategory:
        """
        Обновляет категорию через сервисный слой.
        """

        return update_material_category(
            category=instance,
            data=validated_data,
        )
