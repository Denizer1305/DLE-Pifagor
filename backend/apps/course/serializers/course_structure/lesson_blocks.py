from __future__ import annotations

from apps.course.models import CourseLesson, CourseLessonBlock
from apps.course.serializers.course_structure.lessons import CourseLessonReadSerializer
from apps.course.services import create_course_lesson_block, update_course_lesson_block
from apps.materials.models import Material
from apps.materials.serializers import MaterialShortSerializer
from rest_framework import serializers


class CourseLessonBlockReadSerializer(serializers.ModelSerializer):
    """
    Read-сериализатор блока урока.
    """

    lesson = CourseLessonReadSerializer(read_only=True)
    material = MaterialShortSerializer(read_only=True)

    class Meta:
        model = CourseLessonBlock
        fields = (
            "id",
            "lesson",
            "block_type",
            "title",
            "content",
            "external_url",
            "material",
            "order",
            "is_visible",
            "created_at",
            "updated_at",
        )


class CourseLessonBlockWriteSerializer(serializers.ModelSerializer):
    """
    Write-сериализатор блока урока.
    """

    lesson_id = serializers.IntegerField()
    material_id = serializers.IntegerField(
        required=False,
        allow_null=True,
    )

    class Meta:
        model = CourseLessonBlock
        fields = (
            "lesson_id",
            "block_type",
            "title",
            "content",
            "external_url",
            "material_id",
            "order",
            "is_visible",
        )
        extra_kwargs = {
            "title": {
                "required": False,
                "allow_blank": True,
            },
            "content": {
                "required": False,
                "allow_blank": True,
            },
            "external_url": {
                "required": False,
                "allow_blank": True,
            },
            "order": {
                "required": False,
            },
            "is_visible": {
                "required": False,
            },
        }

    def validate_lesson_id(self, value: int) -> int:
        """
        Проверяет существование урока.
        """

        if not CourseLesson.objects.filter(id=value).exists():
            raise serializers.ValidationError("Урок не найден.")

        return value

    def validate_material_id(
        self,
        value: int | None,
    ) -> int | None:
        """
        Проверяет существование материала.
        """

        if value is None:
            return value

        if not Material.objects.filter(id=value).exists():
            raise serializers.ValidationError("Материал не найден.")

        return value

    def create(self, validated_data: dict) -> CourseLessonBlock:
        """
        Создаёт блок урока через сервисный слой.
        """

        return create_course_lesson_block(data=validated_data)

    def update(
        self,
        instance: CourseLessonBlock,
        validated_data: dict,
    ) -> CourseLessonBlock:
        """
        Обновляет блок урока через сервисный слой.
        """

        return update_course_lesson_block(
            block=instance,
            data=validated_data,
        )


class CourseLessonBlockVisibilityActionSerializer(serializers.Serializer):
    """
    Action-сериализатор показа/скрытия блока урока.
    """

    confirm = serializers.BooleanField(
        required=False,
        default=True,
    )
