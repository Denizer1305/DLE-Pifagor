from __future__ import annotations

from apps.education.models import AcademicYear
from apps.education.services import create_academic_year, update_academic_year
from rest_framework import serializers

from .common_serializers import run_education_service


class AcademicYearReadSerializer(serializers.ModelSerializer):
    """
    Сериализатор чтения учебного года.
    """

    periods_count = serializers.SerializerMethodField()
    curricula_count = serializers.SerializerMethodField()

    class Meta:
        model = AcademicYear
        fields = (
            "id",
            "name",
            "start_date",
            "end_date",
            "description",
            "is_current",
            "is_active",
            "periods_count",
            "curricula_count",
            "created_at",
            "updated_at",
        )

    def get_periods_count(self, academic_year: AcademicYear) -> int:
        """
        Возвращает количество периодов учебного года.
        """

        return academic_year.periods.count()

    def get_curricula_count(self, academic_year: AcademicYear) -> int:
        """
        Возвращает количество учебных планов учебного года.
        """

        return academic_year.curricula.count()


class AcademicYearWriteSerializer(serializers.ModelSerializer):
    """
    Сериализатор создания и обновления учебного года.
    """

    class Meta:
        model = AcademicYear
        fields = (
            "name",
            "start_date",
            "end_date",
            "description",
            "is_current",
            "is_active",
        )

    def create(self, validated_data: dict) -> AcademicYear:
        """
        Создаёт учебный год через сервис.
        """

        return run_education_service(
            create_academic_year,
            data=validated_data,
        )

    def update(
        self,
        instance: AcademicYear,
        validated_data: dict,
    ) -> AcademicYear:
        """
        Обновляет учебный год через сервис.
        """

        return run_education_service(
            update_academic_year,
            academic_year=instance,
            data=validated_data,
        )
