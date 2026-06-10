from __future__ import annotations

from apps.education.models import AcademicYear, Curriculum
from apps.education.services import create_curriculum, update_curriculum
from apps.organizations.models import Department, Organization
from rest_framework import serializers

from .common_serializers import (
    AcademicYearShortSerializer,
    DepartmentShortSerializer,
    OrganizationShortSerializer,
    run_education_service,
)


class CurriculumReadSerializer(serializers.ModelSerializer):
    """
    Сериализатор чтения учебного плана.
    """

    organization = OrganizationShortSerializer(read_only=True)
    department = DepartmentShortSerializer(read_only=True)
    academic_year = AcademicYearShortSerializer(read_only=True)
    calculated_total_hours = serializers.IntegerField(read_only=True)
    items_count = serializers.SerializerMethodField()

    class Meta:
        model = Curriculum
        fields = (
            "id",
            "organization",
            "department",
            "academic_year",
            "code",
            "name",
            "description",
            "total_hours",
            "calculated_total_hours",
            "items_count",
            "status",
            "is_active",
            "created_at",
            "updated_at",
        )

    def get_items_count(self, curriculum: Curriculum) -> int:
        """
        Возвращает количество элементов учебного плана.
        """

        return curriculum.items.count()


class CurriculumWriteSerializer(serializers.ModelSerializer):
    """
    Сериализатор создания и обновления учебного плана.
    """

    organization_id = serializers.PrimaryKeyRelatedField(
        source="organization",
        queryset=Organization.objects.all(),
        write_only=True,
    )
    department_id = serializers.PrimaryKeyRelatedField(
        source="department",
        queryset=Department.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
    )
    academic_year_id = serializers.PrimaryKeyRelatedField(
        source="academic_year",
        queryset=AcademicYear.objects.all(),
        write_only=True,
    )

    class Meta:
        model = Curriculum
        fields = (
            "organization_id",
            "department_id",
            "academic_year_id",
            "code",
            "name",
            "description",
            "total_hours",
            "status",
            "is_active",
        )

    def create(self, validated_data: dict) -> Curriculum:
        """
        Создаёт учебный план через сервис.
        """

        return run_education_service(
            create_curriculum,
            data=validated_data,
        )

    def update(
        self,
        instance: Curriculum,
        validated_data: dict,
    ) -> Curriculum:
        """
        Обновляет учебный план через сервис.
        """

        return run_education_service(
            update_curriculum,
            curriculum=instance,
            data=validated_data,
        )
