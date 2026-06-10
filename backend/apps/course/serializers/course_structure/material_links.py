from __future__ import annotations

from apps.course.models import Course, CourseLesson, CourseMaterialLink, CourseSection
from apps.course.serializers.course.short import CourseShortSerializer
from apps.course.serializers.course_structure.lessons import CourseLessonReadSerializer
from apps.course.serializers.course_structure.sections import (
    CourseSectionReadSerializer,
)
from apps.course.services import (
    create_course_material_link,
    update_course_material_link,
)
from apps.materials.models import Material
from apps.materials.serializers import MaterialShortSerializer
from rest_framework import serializers


class CourseMaterialLinkReadSerializer(serializers.ModelSerializer):
    """
    Read-сериализатор связи курса с материалом.
    """

    course = CourseShortSerializer(read_only=True)
    section = CourseSectionReadSerializer(read_only=True)
    lesson = CourseLessonReadSerializer(read_only=True)
    material = MaterialShortSerializer(read_only=True)

    class Meta:
        model = CourseMaterialLink
        fields = (
            "id",
            "course",
            "section",
            "lesson",
            "material",
            "placement",
            "order",
            "is_required",
            "is_visible",
            "notes",
            "created_at",
            "updated_at",
        )


class CourseMaterialLinkWriteSerializer(serializers.ModelSerializer):
    """
    Write-сериализатор связи курса с материалом.
    """

    course_id = serializers.IntegerField()
    section_id = serializers.IntegerField(
        required=False,
        allow_null=True,
    )
    lesson_id = serializers.IntegerField(
        required=False,
        allow_null=True,
    )
    material_id = serializers.IntegerField()

    class Meta:
        model = CourseMaterialLink
        fields = (
            "course_id",
            "section_id",
            "lesson_id",
            "material_id",
            "placement",
            "order",
            "is_required",
            "is_visible",
            "notes",
        )
        extra_kwargs = {
            "order": {
                "required": False,
            },
            "is_required": {
                "required": False,
            },
            "is_visible": {
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

    def validate_lesson_id(
        self,
        value: int | None,
    ) -> int | None:
        """
        Проверяет существование урока.
        """

        if value is None:
            return value

        if not CourseLesson.objects.filter(id=value).exists():
            raise serializers.ValidationError("Урок не найден.")

        return value

    def validate_material_id(self, value: int) -> int:
        """
        Проверяет существование материала.
        """

        if not Material.objects.filter(id=value).exists():
            raise serializers.ValidationError("Материал не найден.")

        return value

    def create(self, validated_data: dict) -> CourseMaterialLink:
        """
        Создаёт связь курса с материалом через сервисный слой.
        """

        return create_course_material_link(data=validated_data)

    def update(
        self,
        instance: CourseMaterialLink,
        validated_data: dict,
    ) -> CourseMaterialLink:
        """
        Обновляет связь курса с материалом через сервисный слой.
        """

        return update_course_material_link(
            link=instance,
            data=validated_data,
        )


class CourseMaterialLinkVisibilityActionSerializer(serializers.Serializer):
    """
    Action-сериализатор показа/скрытия материала курса.
    """

    confirm = serializers.BooleanField(
        required=False,
        default=True,
    )
