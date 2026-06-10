from __future__ import annotations

from apps.course.models import Course, CourseSection
from apps.course.serializers.course.short import CourseShortSerializer
from apps.course.services import create_course_section, update_course_section
from rest_framework import serializers


class CourseSectionReadSerializer(serializers.ModelSerializer):
    """
    Read-сериализатор раздела курса.
    """

    course = CourseShortSerializer(read_only=True)
    lessons_count = serializers.SerializerMethodField()
    material_links_count = serializers.SerializerMethodField()

    class Meta:
        model = CourseSection
        fields = (
            "id",
            "course",
            "title",
            "description",
            "section_number",
            "order",
            "planned_hours",
            "is_required",
            "is_published",
            "is_active",
            "lessons_count",
            "material_links_count",
            "created_at",
            "updated_at",
        )

    def get_lessons_count(self, obj: CourseSection) -> int:
        """
        Возвращает количество уроков раздела.
        """

        return obj.lessons.count()

    def get_material_links_count(self, obj: CourseSection) -> int:
        """
        Возвращает количество материалов раздела.
        """

        return obj.material_links.count()


class CourseSectionWriteSerializer(serializers.ModelSerializer):
    """
    Write-сериализатор раздела курса.
    """

    course_id = serializers.IntegerField()

    class Meta:
        model = CourseSection
        fields = (
            "course_id",
            "title",
            "description",
            "section_number",
            "order",
            "planned_hours",
            "is_required",
            "is_published",
            "is_active",
        )
        extra_kwargs = {
            "description": {
                "required": False,
                "allow_blank": True,
            },
            "section_number": {
                "required": False,
                "allow_null": True,
            },
            "order": {
                "required": False,
            },
            "planned_hours": {
                "required": False,
            },
            "is_required": {
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

    def create(self, validated_data: dict) -> CourseSection:
        """
        Создаёт раздел через сервисный слой.
        """

        return create_course_section(data=validated_data)

    def update(
        self,
        instance: CourseSection,
        validated_data: dict,
    ) -> CourseSection:
        """
        Обновляет раздел через сервисный слой.
        """

        return update_course_section(
            section=instance,
            data=validated_data,
        )


class CourseSectionStatusActionSerializer(serializers.Serializer):
    """
    Action-сериализатор публикации/архивации раздела.
    """

    confirm = serializers.BooleanField(
        required=False,
        default=True,
    )
