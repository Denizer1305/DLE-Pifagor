from __future__ import annotations

from apps.course.models import Course, CourseAccessRule
from apps.course.serializers.common_serializers import (
    OrganizationShortSerializer,
    UserShortSerializer,
)
from apps.course.serializers.course.short import CourseShortSerializer
from apps.course.services import create_course_access_rule, update_course_access_rule
from apps.organizations.models import Organization
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class CourseAccessRuleReadSerializer(serializers.ModelSerializer):
    """
    Read-сериализатор правила доступа к курсу.
    """

    course = CourseShortSerializer(read_only=True)
    learner = UserShortSerializer(read_only=True)
    organization = OrganizationShortSerializer(read_only=True)

    enrollments_count = serializers.SerializerMethodField()

    class Meta:
        model = CourseAccessRule
        fields = (
            "id",
            "course",
            "access_type",
            "learner",
            "organization",
            "access_code",
            "starts_at",
            "ends_at",
            "auto_enroll",
            "is_active",
            "notes",
            "enrollments_count",
            "created_at",
            "updated_at",
        )

    def get_enrollments_count(self, obj: CourseAccessRule) -> int:
        """
        Возвращает количество записей, созданных через правило доступа.
        """

        return obj.enrollments.count()


class CourseAccessRuleWriteSerializer(serializers.ModelSerializer):
    """
    Write-сериализатор правила доступа к курсу.
    """

    course_id = serializers.IntegerField()
    learner_id = serializers.IntegerField(
        required=False,
        allow_null=True,
    )
    organization_id = serializers.IntegerField(
        required=False,
        allow_null=True,
    )

    class Meta:
        model = CourseAccessRule
        fields = (
            "course_id",
            "access_type",
            "learner_id",
            "organization_id",
            "access_code",
            "starts_at",
            "ends_at",
            "auto_enroll",
            "is_active",
            "notes",
        )
        extra_kwargs = {
            "access_code": {
                "required": False,
                "allow_blank": True,
            },
            "starts_at": {
                "required": False,
                "allow_null": True,
            },
            "ends_at": {
                "required": False,
                "allow_null": True,
            },
            "auto_enroll": {
                "required": False,
            },
            "is_active": {
                "required": False,
            },
            "notes": {
                "required": False,
                "allow_blank": True,
            },
        }

    def validate_course_id(self, value: int) -> int:
        """
        Проверяет существование курса.
        """

        if not Course.objects.filter(id=value).exists():
            raise serializers.ValidationError("Курс не найден.")

        return value

    def validate_learner_id(
        self,
        value: int | None,
    ) -> int | None:
        """
        Проверяет существование обучающегося.
        """

        if value is None:
            return value

        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("Пользователь не найден.")

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

    def create(self, validated_data: dict) -> CourseAccessRule:
        """
        Создаёт правило доступа через сервисный слой.
        """

        return create_course_access_rule(data=validated_data)

    def update(
        self,
        instance: CourseAccessRule,
        validated_data: dict,
    ) -> CourseAccessRule:
        """
        Обновляет правило доступа через сервисный слой.
        """

        return update_course_access_rule(
            access_rule=instance,
            data=validated_data,
        )


class CourseAccessRuleStatusActionSerializer(serializers.Serializer):
    """
    Action-сериализатор включения/выключения правила доступа.
    """

    confirm = serializers.BooleanField(
        required=False,
        default=True,
    )
