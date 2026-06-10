from __future__ import annotations

from apps.education.models import AcademicYear, LearnerGroupEnrollment
from apps.education.services import (
    create_learner_group_enrollment,
    update_learner_group_enrollment,
)
from apps.organizations.models import StudyGroup
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .common_serializers import (
    AcademicYearShortSerializer,
    StudyGroupShortSerializer,
    UserShortSerializer,
    run_education_service,
)

User = get_user_model()


class LearnerGroupEnrollmentReadSerializer(serializers.ModelSerializer):
    """
    Сериализатор чтения академического зачисления обучающегося.
    """

    learner = UserShortSerializer(read_only=True)
    group = StudyGroupShortSerializer(read_only=True)
    academic_year = AcademicYearShortSerializer(read_only=True)

    class Meta:
        model = LearnerGroupEnrollment
        fields = (
            "id",
            "learner",
            "group",
            "academic_year",
            "enrollment_date",
            "completion_date",
            "status",
            "is_primary",
            "journal_number",
            "notes",
            "created_at",
            "updated_at",
        )


class LearnerGroupEnrollmentWriteSerializer(serializers.ModelSerializer):
    """
    Сериализатор создания и обновления академического зачисления.
    """

    learner_id = serializers.PrimaryKeyRelatedField(
        source="learner",
        queryset=User.objects.all(),
        write_only=True,
    )
    group_id = serializers.PrimaryKeyRelatedField(
        source="group",
        queryset=StudyGroup.objects.all(),
        write_only=True,
    )
    academic_year_id = serializers.PrimaryKeyRelatedField(
        source="academic_year",
        queryset=AcademicYear.objects.all(),
        write_only=True,
    )

    class Meta:
        model = LearnerGroupEnrollment
        fields = (
            "learner_id",
            "group_id",
            "academic_year_id",
            "enrollment_date",
            "completion_date",
            "status",
            "is_primary",
            "journal_number",
            "notes",
        )

    def create(self, validated_data: dict) -> LearnerGroupEnrollment:
        """
        Создаёт академическое зачисление через сервис.
        """

        return run_education_service(
            create_learner_group_enrollment,
            data=validated_data,
        )

    def update(
        self,
        instance: LearnerGroupEnrollment,
        validated_data: dict,
    ) -> LearnerGroupEnrollment:
        """
        Обновляет академическое зачисление через сервис.
        """

        return run_education_service(
            update_learner_group_enrollment,
            enrollment=instance,
            data=validated_data,
        )


class LearnerGroupEnrollmentCompleteSerializer(serializers.Serializer):
    """
    Сериализатор завершения академического зачисления.
    """

    completion_date = serializers.DateField()
    status = serializers.ChoiceField(
        choices=(
            LearnerGroupEnrollment.StatusChoices.TRANSFERRED,
            LearnerGroupEnrollment.StatusChoices.GRADUATED,
            LearnerGroupEnrollment.StatusChoices.EXPELLED,
            LearnerGroupEnrollment.StatusChoices.ARCHIVED,
        ),
        default=LearnerGroupEnrollment.StatusChoices.GRADUATED,
    )
