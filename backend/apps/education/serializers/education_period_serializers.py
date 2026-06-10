from __future__ import annotations

from apps.education.models import AcademicYear, EducationPeriod
from apps.education.services import create_education_period, update_education_period
from rest_framework import serializers

from .common_serializers import AcademicYearShortSerializer, run_education_service


class EducationPeriodReadSerializer(serializers.ModelSerializer):
    """
    Сериализатор чтения учебного периода.
    """

    academic_year = AcademicYearShortSerializer(read_only=True)

    class Meta:
        model = EducationPeriod
        fields = (
            "id",
            "academic_year",
            "name",
            "code",
            "period_type",
            "sequence",
            "start_date",
            "end_date",
            "description",
            "is_current",
            "is_active",
            "created_at",
            "updated_at",
        )


class EducationPeriodWriteSerializer(serializers.ModelSerializer):
    """
    Сериализатор создания и обновления учебного периода.
    """

    academic_year_id = serializers.PrimaryKeyRelatedField(
        source="academic_year",
        queryset=AcademicYear.objects.all(),
        write_only=True,
    )

    class Meta:
        model = EducationPeriod
        fields = (
            "academic_year_id",
            "name",
            "code",
            "period_type",
            "sequence",
            "start_date",
            "end_date",
            "description",
            "is_current",
            "is_active",
        )

    def create(self, validated_data: dict) -> EducationPeriod:
        """
        Создаёт учебный период через сервис.
        """

        return run_education_service(
            create_education_period,
            data=validated_data,
        )

    def update(
        self,
        instance: EducationPeriod,
        validated_data: dict,
    ) -> EducationPeriod:
        """
        Обновляет учебный период через сервис.
        """

        return run_education_service(
            update_education_period,
            period=instance,
            data=validated_data,
        )
