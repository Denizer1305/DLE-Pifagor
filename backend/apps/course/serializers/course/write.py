from __future__ import annotations

from apps.course.models import Course
from apps.course.services import create_course, update_course
from apps.education.models import AcademicYear, EducationPeriod
from apps.organizations.models import Organization, Subject
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class CourseWriteSerializer(serializers.ModelSerializer):
    """
    Write-сериализатор курса.
    """

    owner_teacher_id = serializers.IntegerField(
        required=False,
        allow_null=True,
    )
    organization_id = serializers.IntegerField(
        required=False,
        allow_null=True,
    )
    subject_id = serializers.IntegerField(
        required=False,
        allow_null=True,
    )
    academic_year_id = serializers.IntegerField(
        required=False,
        allow_null=True,
    )
    period_id = serializers.IntegerField(
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Course
        fields = (
            "code",
            "slug",
            "title",
            "subtitle",
            "description",
            "course_type",
            "origin",
            "status",
            "visibility",
            "level",
            "language",
            "owner_teacher_id",
            "organization_id",
            "subject_id",
            "academic_year_id",
            "period_id",
            "cover_image",
            "is_template",
            "is_active",
            "allow_self_enrollment",
            "enrollment_code",
            "starts_at",
            "ends_at",
        )
        extra_kwargs = {
            "subtitle": {
                "required": False,
                "allow_blank": True,
            },
            "description": {
                "required": False,
                "allow_blank": True,
            },
            "level": {
                "required": False,
                "allow_blank": True,
            },
            "language": {
                "required": False,
                "allow_blank": True,
            },
            "enrollment_code": {
                "required": False,
                "allow_blank": True,
            },
            "cover_image": {
                "required": False,
                "allow_null": True,
            },
            "is_template": {
                "required": False,
            },
            "is_active": {
                "required": False,
            },
            "allow_self_enrollment": {
                "required": False,
            },
            "starts_at": {
                "required": False,
                "allow_null": True,
            },
            "ends_at": {
                "required": False,
                "allow_null": True,
            },
        }

    def validate_owner_teacher_id(
        self,
        value: int | None,
    ) -> int | None:
        """
        Проверяет существование владельца курса.
        """

        if value is None:
            return value

        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("Преподаватель не найден.")

        return value

    def validate_organization_id(
        self,
        value: int | None,
    ) -> int | None:
        """
        Проверяет существование организации.
        """

        if value is None:
            return value

        if not Organization.objects.filter(id=value).exists():
            raise serializers.ValidationError("Организация не найдена.")

        return value

    def validate_subject_id(
        self,
        value: int | None,
    ) -> int | None:
        """
        Проверяет существование предмета.
        """

        if value is None:
            return value

        if not Subject.objects.filter(id=value).exists():
            raise serializers.ValidationError("Предмет не найден.")

        return value

    def validate_academic_year_id(
        self,
        value: int | None,
    ) -> int | None:
        """
        Проверяет существование учебного года.
        """

        if value is None:
            return value

        if not AcademicYear.objects.filter(id=value).exists():
            raise serializers.ValidationError("Учебный год не найден.")

        return value

    def validate_period_id(
        self,
        value: int | None,
    ) -> int | None:
        """
        Проверяет существование учебного периода.
        """

        if value is None:
            return value

        if not EducationPeriod.objects.filter(id=value).exists():
            raise serializers.ValidationError("Учебный период не найден.")

        return value

    def validate(self, attrs: dict) -> dict:
        """
        Дополняет владельца курса текущим пользователем, если он не передан.
        """

        request = self.context.get("request")

        if (
            request is not None
            and request.user.is_authenticated
            and not attrs.get("owner_teacher_id")
        ):
            attrs["owner_teacher_id"] = request.user.id

        return attrs

    def create(self, validated_data: dict) -> Course:
        """
        Создаёт курс через сервисный слой.
        """

        return create_course(data=validated_data)

    def update(
        self,
        instance: Course,
        validated_data: dict,
    ) -> Course:
        """
        Обновляет курс через сервисный слой.
        """

        return update_course(
            course=instance,
            data=validated_data,
        )
