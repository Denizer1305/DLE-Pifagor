from __future__ import annotations

from apps.course.models import Course, CourseLesson, CourseSection
from apps.course.serializers.course.short import CourseShortSerializer
from apps.course.serializers.course_structure.sections import (
    CourseSectionReadSerializer,
)
from apps.course.services import create_course_lesson, update_course_lesson
from rest_framework import serializers


class CourseLessonReadSerializer(serializers.ModelSerializer):
    """
    Read-сериализатор урока курса.
    """

    course = CourseShortSerializer(read_only=True)
    section = CourseSectionReadSerializer(read_only=True)

    blocks_count = serializers.SerializerMethodField()
    material_links_count = serializers.SerializerMethodField()
    progresses_count = serializers.SerializerMethodField()

    class Meta:
        model = CourseLesson
        fields = (
            "id",
            "course",
            "section",
            "lesson_number",
            "lesson_type",
            "title",
            "short_content",
            "planned_hours",
            "theory_hours",
            "practice_hours",
            "lab_hours",
            "self_study_hours",
            "visual_aids",
            "literature",
            "independent_work",
            "notes",
            "order",
            "available_from",
            "is_required",
            "is_preview",
            "is_published",
            "is_active",
            "blocks_count",
            "material_links_count",
            "progresses_count",
            "created_at",
            "updated_at",
        )

    def get_blocks_count(self, obj: CourseLesson) -> int:
        """
        Возвращает количество блоков урока.
        """

        return obj.blocks.count()

    def get_material_links_count(self, obj: CourseLesson) -> int:
        """
        Возвращает количество материалов урока.
        """

        return obj.material_links.count()

    def get_progresses_count(self, obj: CourseLesson) -> int:
        """
        Возвращает количество записей прогресса урока.
        """

        return obj.progresses.count()


class CourseLessonWriteSerializer(serializers.ModelSerializer):
    """
    Write-сериализатор урока курса.
    """

    course_id = serializers.IntegerField()
    section_id = serializers.IntegerField(
        required=False,
        allow_null=True,
    )

    class Meta:
        model = CourseLesson
        fields = (
            "course_id",
            "section_id",
            "lesson_number",
            "lesson_type",
            "title",
            "short_content",
            "planned_hours",
            "theory_hours",
            "practice_hours",
            "lab_hours",
            "self_study_hours",
            "visual_aids",
            "literature",
            "independent_work",
            "notes",
            "order",
            "available_from",
            "is_required",
            "is_preview",
            "is_published",
            "is_active",
        )
        extra_kwargs = {
            "lesson_number": {
                "required": False,
                "allow_null": True,
            },
            "short_content": {
                "required": False,
                "allow_blank": True,
            },
            "visual_aids": {
                "required": False,
                "allow_blank": True,
            },
            "literature": {
                "required": False,
                "allow_blank": True,
            },
            "independent_work": {
                "required": False,
                "allow_blank": True,
            },
            "notes": {
                "required": False,
                "allow_blank": True,
            },
            "available_from": {
                "required": False,
                "allow_null": True,
            },
            "order": {
                "required": False,
            },
            "planned_hours": {
                "required": False,
            },
            "theory_hours": {
                "required": False,
            },
            "practice_hours": {
                "required": False,
            },
            "lab_hours": {
                "required": False,
            },
            "self_study_hours": {
                "required": False,
            },
            "is_required": {
                "required": False,
            },
            "is_preview": {
                "required": False,
            },
            "is_published": {
                "required": False,
            },
            "is_active": {
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

    def validate_section_id(
        self,
        value: int | None,
    ) -> int | None:
        """
        Проверяет существование раздела.
        """

        if value is None:
            return value

        if not CourseSection.objects.filter(id=value).exists():
            raise serializers.ValidationError("Раздел не найден.")

        return value

    def create(self, validated_data: dict) -> CourseLesson:
        """
        Создаёт урок через сервисный слой.
        """

        return create_course_lesson(data=validated_data)

    def update(
        self,
        instance: CourseLesson,
        validated_data: dict,
    ) -> CourseLesson:
        """
        Обновляет урок через сервисный слой.
        """

        return update_course_lesson(
            lesson=instance,
            data=validated_data,
        )


class CourseLessonStatusActionSerializer(serializers.Serializer):
    """
    Action-сериализатор публикации/архивации урока.
    """

    confirm = serializers.BooleanField(
        required=False,
        default=True,
    )
