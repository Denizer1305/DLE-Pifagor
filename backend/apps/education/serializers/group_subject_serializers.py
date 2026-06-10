from __future__ import annotations

from apps.education.models import (
    AcademicYear,
    CurriculumItem,
    EducationPeriod,
    GroupSubject,
)
from apps.education.services import create_group_subject, update_group_subject
from apps.organizations.models import StudyGroup, Subject
from rest_framework import serializers

from .common_serializers import (
    AcademicYearShortSerializer,
    CurriculumItemShortSerializer,
    EducationPeriodShortSerializer,
    StudyGroupShortSerializer,
    SubjectShortSerializer,
    run_education_service,
)


class GroupSubjectReadSerializer(serializers.ModelSerializer):
    """
    Сериализатор чтения предмета учебной группы.
    """

    group = StudyGroupShortSerializer(read_only=True)
    subject = SubjectShortSerializer(read_only=True)
    academic_year = AcademicYearShortSerializer(read_only=True)
    period = EducationPeriodShortSerializer(read_only=True)
    curriculum_item = CurriculumItemShortSerializer(read_only=True)
    teacher_assignments_count = serializers.SerializerMethodField()

    class Meta:
        model = GroupSubject
        fields = (
            "id",
            "group",
            "subject",
            "academic_year",
            "period",
            "curriculum_item",
            "planned_hours",
            "contact_hours",
            "independent_hours",
            "assessment_type",
            "is_required",
            "is_active",
            "teacher_assignments_count",
            "notes",
            "created_at",
            "updated_at",
        )

    def get_teacher_assignments_count(self, group_subject: GroupSubject) -> int:
        """
        Возвращает количество назначений преподавателей.
        """

        return group_subject.teacher_assignments.count()


class GroupSubjectWriteSerializer(serializers.ModelSerializer):
    """
    Сериализатор создания и обновления предмета учебной группы.
    """

    group_id = serializers.PrimaryKeyRelatedField(
        source="group",
        queryset=StudyGroup.objects.all(),
        write_only=True,
    )
    subject_id = serializers.PrimaryKeyRelatedField(
        source="subject",
        queryset=Subject.objects.all(),
        write_only=True,
        required=False,
    )
    academic_year_id = serializers.PrimaryKeyRelatedField(
        source="academic_year",
        queryset=AcademicYear.objects.all(),
        write_only=True,
        required=False,
    )
    period_id = serializers.PrimaryKeyRelatedField(
        source="period",
        queryset=EducationPeriod.objects.all(),
        write_only=True,
        required=False,
    )
    curriculum_item_id = serializers.PrimaryKeyRelatedField(
        source="curriculum_item",
        queryset=CurriculumItem.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = GroupSubject
        fields = (
            "group_id",
            "subject_id",
            "academic_year_id",
            "period_id",
            "curriculum_item_id",
            "planned_hours",
            "contact_hours",
            "independent_hours",
            "assessment_type",
            "is_required",
            "is_active",
            "notes",
        )

    def create(self, validated_data: dict) -> GroupSubject:
        """
        Создаёт предмет группы через сервис.
        """

        return run_education_service(
            create_group_subject,
            data=validated_data,
        )

    def update(
        self,
        instance: GroupSubject,
        validated_data: dict,
    ) -> GroupSubject:
        """
        Обновляет предмет группы через сервис.
        """

        return run_education_service(
            update_group_subject,
            group_subject=instance,
            data=validated_data,
        )
