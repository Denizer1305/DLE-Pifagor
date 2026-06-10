from __future__ import annotations

from apps.course.models import (
    CourseEnrollment,
    CourseLesson,
    CourseProgress,
    LessonProgress,
)
from apps.course.serializers.course_access.enrollments import (
    CourseEnrollmentReadSerializer,
)
from apps.course.serializers.course_structure.lessons import CourseLessonReadSerializer
from rest_framework import serializers


class CourseProgressNestedShortSerializer(serializers.ModelSerializer):
    """
    Краткое вложенное представление прогресса курса.
    """

    class Meta:
        model = CourseProgress
        fields = (
            "id",
            "progress_percent",
            "total_lessons_count",
            "completed_lessons_count",
            "last_activity_at",
        )


class LessonProgressReadSerializer(serializers.ModelSerializer):
    """
    Read-сериализатор прогресса урока.
    """

    enrollment = CourseEnrollmentReadSerializer(read_only=True)
    course_progress = CourseProgressNestedShortSerializer(read_only=True)
    lesson = CourseLessonReadSerializer(read_only=True)

    progress_percent = serializers.SerializerMethodField()
    last_activity_at = serializers.SerializerMethodField()

    class Meta:
        model = LessonProgress
        fields = (
            "id",
            "enrollment",
            "course_progress",
            "lesson",
            "status",
            "progress_percent",
            "started_at",
            "completed_at",
            "last_activity_at",
            "created_at",
            "updated_at",
        )

    def get_progress_percent(self, obj: LessonProgress) -> int:
        """
        Возвращает вычисляемый процент прогресса урока.
        """

        completed_status = getattr(
            LessonProgress.StatusChoices,
            "COMPLETED",
            "completed",
        )
        in_progress_status = getattr(
            LessonProgress.StatusChoices,
            "IN_PROGRESS",
            "in_progress",
        )

        if obj.status == completed_status:
            return 100

        if obj.status == in_progress_status:
            return 50

        return 0

    def get_last_activity_at(self, obj: LessonProgress):
        """
        Возвращает ближайшую доступную дату активности.
        """

        return obj.completed_at or obj.started_at or obj.updated_at or obj.created_at


class LessonProgressWriteSerializer(serializers.ModelSerializer):
    """
    Write-сериализатор прогресса урока.

    Прогресс урока обычно меняется через actions:
    start / complete / reset / track-opened / track-completed.
    """

    enrollment_id = serializers.IntegerField()
    course_progress_id = serializers.IntegerField(
        required=False,
        allow_null=True,
    )
    lesson_id = serializers.IntegerField()

    class Meta:
        model = LessonProgress
        fields = (
            "enrollment_id",
            "course_progress_id",
            "lesson_id",
            "status",
            "started_at",
            "completed_at",
        )
        extra_kwargs = {
            "status": {
                "required": False,
            },
            "started_at": {
                "required": False,
                "allow_null": True,
            },
            "completed_at": {
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

    def validate_course_progress_id(
        self,
        value: int | None,
    ) -> int | None:
        """
        Проверяет существование прогресса курса.
        """

        if value is None:
            return value

        if not CourseProgress.objects.filter(id=value).exists():
            raise serializers.ValidationError("Прогресс курса не найден.")

        return value

    def validate_lesson_id(self, value: int) -> int:
        """
        Проверяет существование урока.
        """

        if not CourseLesson.objects.filter(id=value).exists():
            raise serializers.ValidationError("Урок не найден.")

        return value


class LessonProgressStatusActionSerializer(serializers.Serializer):
    """
    Action-сериализатор смены статуса прогресса урока.
    """

    confirm = serializers.BooleanField(
        required=False,
        default=True,
    )


class LessonProgressTrackActionSerializer(serializers.Serializer):
    """
    Action-сериализатор фиксации открытия/завершения урока.
    """

    enrollment_id = serializers.IntegerField()
    lesson_id = serializers.IntegerField()

    def validate_enrollment_id(self, value: int) -> int:
        """
        Проверяет существование записи на курс.
        """

        if not CourseEnrollment.objects.filter(id=value).exists():
            raise serializers.ValidationError("Запись на курс не найдена.")

        return value

    def validate_lesson_id(self, value: int) -> int:
        """
        Проверяет существование урока.
        """

        if not CourseLesson.objects.filter(id=value).exists():
            raise serializers.ValidationError("Урок не найден.")

        return value
