from __future__ import annotations

from apps.course.models import Course, CourseGroupAccess
from apps.course.serializers.course.short import CourseShortSerializer
from apps.course.services import create_course_group_access, update_course_group_access
from rest_framework import serializers


class CourseGroupAccessReadSerializer(serializers.ModelSerializer):
    """
    Read-сериализатор доступа группы к курсу.
    """

    course = CourseShortSerializer(read_only=True)
    group_title = serializers.SerializerMethodField()
    group_subject_title = serializers.SerializerMethodField()
    teacher_group_subject_title = serializers.SerializerMethodField()

    class Meta:
        model = CourseGroupAccess
        fields = (
            "id",
            "course",
            "group",
            "group_title",
            "group_subject",
            "group_subject_title",
            "teacher_group_subject",
            "teacher_group_subject_title",
            "visibility",
            "starts_at",
            "ends_at",
            "auto_enroll",
            "is_active",
            "notes",
            "created_at",
            "updated_at",
        )

    def get_group_title(self, obj: CourseGroupAccess) -> str:
        """
        Возвращает название группы.
        """

        if not obj.group_id:
            return ""

        return getattr(obj.group, "name", str(obj.group))

    def get_group_subject_title(self, obj: CourseGroupAccess) -> str:
        """
        Возвращает название предмета группы.
        """

        if not obj.group_subject_id:
            return ""

        return str(obj.group_subject)

    def get_teacher_group_subject_title(self, obj: CourseGroupAccess) -> str:
        """
        Возвращает название назначения преподавателя.
        """

        if not obj.teacher_group_subject_id:
            return ""

        return str(obj.teacher_group_subject)


class CourseGroupAccessWriteSerializer(serializers.ModelSerializer):
    """
    Write-сериализатор доступа группы к курсу.
    """

    course_id = serializers.IntegerField()
    group_id = serializers.IntegerField()
    group_subject_id = serializers.IntegerField(
        required=False,
        allow_null=True,
    )
    teacher_group_subject_id = serializers.IntegerField(
        required=False,
        allow_null=True,
    )

    class Meta:
        model = CourseGroupAccess
        fields = (
            "course_id",
            "group_id",
            "group_subject_id",
            "teacher_group_subject_id",
            "visibility",
            "starts_at",
            "ends_at",
            "auto_enroll",
            "is_active",
            "notes",
        )
        extra_kwargs = {
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

    def create(self, validated_data: dict) -> CourseGroupAccess:
        """
        Создаёт доступ группы через сервисный слой.
        """

        return create_course_group_access(data=validated_data)

    def update(
        self,
        instance: CourseGroupAccess,
        validated_data: dict,
    ) -> CourseGroupAccess:
        """
        Обновляет доступ группы через сервисный слой.
        """

        return update_course_group_access(
            group_access=instance,
            data=validated_data,
        )


class CourseGroupAccessVisibilityActionSerializer(serializers.Serializer):
    """
    Action-сериализатор изменения видимости курса для группы.
    """

    confirm = serializers.BooleanField(
        required=False,
        default=True,
    )
