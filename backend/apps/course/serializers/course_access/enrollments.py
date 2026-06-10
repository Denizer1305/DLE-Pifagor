from __future__ import annotations

from apps.course.models import Course, CourseEnrollment
from apps.course.serializers.common_serializers import UserShortSerializer
from apps.course.serializers.course.short import CourseShortSerializer
from apps.course.services import create_course_enrollment, update_course_enrollment
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class CourseEnrollmentReadSerializer(serializers.ModelSerializer):
    """
    Read-сериализатор записи обучающегося на курс.
    """

    course = CourseShortSerializer(read_only=True)
    learner = UserShortSerializer(read_only=True)
    group_access_title = serializers.SerializerMethodField()
    access_rule_title = serializers.SerializerMethodField()

    class Meta:
        model = CourseEnrollment
        fields = (
            "id",
            "course",
            "learner",
            "group_access",
            "group_access_title",
            "access_rule",
            "access_rule_title",
            "status",
            "enrolled_at",
            "started_at",
            "completed_at",
            "last_activity_at",
            "progress_percent",
            "created_at",
            "updated_at",
        )

    def get_group_access_title(self, obj: CourseEnrollment) -> str:
        """
        Возвращает краткое название группового доступа.
        """

        if not obj.group_access_id:
            return ""

        return str(obj.group_access)

    def get_access_rule_title(self, obj: CourseEnrollment) -> str:
        """
        Возвращает краткое название правила доступа.
        """

        if not obj.access_rule_id:
            return ""

        return str(obj.access_rule)


class CourseEnrollmentWriteSerializer(serializers.ModelSerializer):
    """
    Write-сериализатор записи на курс.
    """

    course_id = serializers.IntegerField()
    learner_id = serializers.IntegerField()
    group_access_id = serializers.IntegerField(
        required=False,
        allow_null=True,
    )
    access_rule_id = serializers.IntegerField(
        required=False,
        allow_null=True,
    )

    class Meta:
        model = CourseEnrollment
        fields = (
            "course_id",
            "learner_id",
            "group_access_id",
            "access_rule_id",
            "status",
            "enrolled_at",
            "started_at",
            "completed_at",
            "last_activity_at",
            "progress_percent",
        )
        extra_kwargs = {
            "enrolled_at": {
                "required": False,
                "allow_null": True,
            },
            "started_at": {
                "required": False,
                "allow_null": True,
            },
            "completed_at": {
                "required": False,
                "allow_null": True,
            },
            "last_activity_at": {
                "required": False,
                "allow_null": True,
            },
            "progress_percent": {
                "required": False,
            },
        }

    def validate_course_id(self, value: int) -> int:
        """
        Проверяет существование курса.
        """

        if not Course.objects.filter(id=value).exists():
            raise serializers.ValidationError("Курс не найден.")

        return value

    def validate_learner_id(self, value: int) -> int:
        """
        Проверяет существование обучающегося.
        """

        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("Пользователь не найден.")

        return value

    def create(self, validated_data: dict) -> CourseEnrollment:
        """
        Создаёт запись на курс через сервисный слой.
        """

        return create_course_enrollment(data=validated_data)

    def update(
        self,
        instance: CourseEnrollment,
        validated_data: dict,
    ) -> CourseEnrollment:
        """
        Обновляет запись на курс через сервисный слой.
        """

        return update_course_enrollment(
            enrollment=instance,
            data=validated_data,
        )


class CourseEnrollmentStatusActionSerializer(serializers.Serializer):
    """
    Action-сериализатор смены статуса записи на курс.
    """

    confirm = serializers.BooleanField(
        required=False,
        default=True,
    )
