from __future__ import annotations

from apps.education.models import Curriculum, CurriculumItem, EducationPeriod
from apps.education.services import create_curriculum_item, update_curriculum_item
from apps.organizations.models import Subject
from rest_framework import serializers

from .common_serializers import (
    CurriculumShortSerializer,
    EducationPeriodShortSerializer,
    SubjectShortSerializer,
    run_education_service,
)


class CurriculumItemReadSerializer(serializers.ModelSerializer):
    """
    Сериализатор чтения элемента учебного плана.
    """

    curriculum = CurriculumShortSerializer(read_only=True)
    period = EducationPeriodShortSerializer(read_only=True)
    subject = SubjectShortSerializer(read_only=True)

    class Meta:
        model = CurriculumItem
        fields = (
            "id",
            "curriculum",
            "period",
            "subject",
            "sequence",
            "planned_hours",
            "contact_hours",
            "independent_hours",
            "assessment_type",
            "is_required",
            "is_active",
            "notes",
            "created_at",
            "updated_at",
        )


class CurriculumItemWriteSerializer(serializers.ModelSerializer):
    """
    Сериализатор создания и обновления элемента учебного плана.
    """

    curriculum_id = serializers.PrimaryKeyRelatedField(
        source="curriculum",
        queryset=Curriculum.objects.all(),
        write_only=True,
    )
    period_id = serializers.PrimaryKeyRelatedField(
        source="period",
        queryset=EducationPeriod.objects.all(),
        write_only=True,
    )
    subject_id = serializers.PrimaryKeyRelatedField(
        source="subject",
        queryset=Subject.objects.all(),
        write_only=True,
    )

    class Meta:
        model = CurriculumItem
        fields = (
            "curriculum_id",
            "period_id",
            "subject_id",
            "sequence",
            "planned_hours",
            "contact_hours",
            "independent_hours",
            "assessment_type",
            "is_required",
            "is_active",
            "notes",
        )

    def create(self, validated_data: dict) -> CurriculumItem:
        """
        Создаёт элемент учебного плана через сервис.
        """

        return run_education_service(
            create_curriculum_item,
            data=validated_data,
        )

    def update(
        self,
        instance: CurriculumItem,
        validated_data: dict,
    ) -> CurriculumItem:
        """
        Обновляет элемент учебного плана через сервис.
        """

        return run_education_service(
            update_curriculum_item,
            curriculum_item=instance,
            data=validated_data,
        )
