from __future__ import annotations

from apps.course.models import CourseEnrollment, CourseLesson, CourseProgress
from apps.course.serializers.course_access.enrollments import (
    CourseEnrollmentReadSerializer,
)
from apps.course.serializers.course_structure.lessons import CourseLessonReadSerializer
from rest_framework import serializers


class CourseProgressReadSerializer(serializers.ModelSerializer):
    """
    Read-сериализатор общего прогресса по курсу.
    """

    enrollment = CourseEnrollmentReadSerializer(read_only=True)
    last_lesson = CourseLessonReadSerializer(read_only=True)

    lesson_progresses_count = serializers.SerializerMethodField()

    class Meta:
        model = CourseProgress
        fields = (
            "id",
            "enrollment",
            "progress_percent",
            "total_lessons_count",
            "completed_lessons_count",
            "last_lesson",
            "last_activity_at",
            "lesson_progresses_count",
            "created_at",
            "updated_at",
        )

    def get_lesson_progresses_count(self, obj: CourseProgress) -> int:
        """
        Возвращает количество записей прогресса уроков.
        """

        return obj.lesson_progresses.count()


class CourseProgressWriteSerializer(serializers.ModelSerializer):
    """
    Write-сериализатор общего прогресса по курсу.

    Обычно прогресс пересчитывается сервисами, но serializer оставлен
    для административных сценариев и тестов.
    """

    enrollment_id = serializers.IntegerField()
    last_lesson_id = serializers.IntegerField(
        required=False,
        allow_null=True,
    )

    class Meta:
        model = CourseProgress
        fields = (
            "enrollment_id",
            "progress_percent",
            "total_lessons_count",
            "completed_lessons_count",
            "last_lesson_id",
            "last_activity_at",
        )
        extra_kwargs = {
            "progress_percent": {
                "required": False,
            },
            "total_lessons_count": {
                "required": False,
            },
            "completed_lessons_count": {
                "required": False,
            },
            "last_activity_at": {
                "required": False,
                "allow_null": True,
            },
        }

    def validate_enrollment_id(self, value: int) -> int:
        """
        Проверяет существование записи на курс.
        """

        if not CourseEnrollment.objects.filter(id=value).exists():
            raise serializers.ValidationError("Запись на курс не найдена.")

        return value

    def validate_last_lesson_id(
        self,
        value: int | None,
    ) -> int | None:
        """
        Проверяет существование последнего урока.
        """

        if value is None:
            return value

        if not CourseLesson.objects.filter(id=value).exists():
            raise serializers.ValidationError("Урок не найден.")

        return value


class CourseProgressRecalculateActionSerializer(serializers.Serializer):
    """
    Action-сериализатор пересчёта прогресса курса.
    """

    confirm = serializers.BooleanField(
        required=False,
        default=True,
    )


class CourseProgressEnsureActionSerializer(serializers.Serializer):
    """
    Action-сериализатор создания недостающего прогресса курса.
    """

    confirm = serializers.BooleanField(
        required=False,
        default=True,
    )
