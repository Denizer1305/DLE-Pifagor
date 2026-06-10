from __future__ import annotations

from apps.testing.models import Test
from rest_framework import serializers


class TestReadSerializer(serializers.ModelSerializer):
    """
    Read-сериализатор теста.
    """

    course_title = serializers.CharField(
        source="course.title",
        read_only=True,
    )
    lesson_title = serializers.CharField(
        source="lesson.title",
        read_only=True,
        allow_null=True,
    )
    organization_name = serializers.CharField(
        source="organization.name",
        read_only=True,
    )
    subject_name = serializers.CharField(
        source="subject.name",
        read_only=True,
    )
    owner_teacher_name = serializers.SerializerMethodField()
    questions_count = serializers.IntegerField(
        source="questions.count",
        read_only=True,
    )

    class Meta:
        model = Test
        fields = (
            "id",
            "title",
            "description",
            "instructions",
            "course",
            "course_title",
            "lesson",
            "lesson_title",
            "lesson_block",
            "organization",
            "organization_name",
            "subject",
            "subject_name",
            "owner_teacher",
            "owner_teacher_name",
            "status",
            "visibility",
            "max_attempts",
            "time_limit_minutes",
            "max_score",
            "passing_score",
            "shuffle_questions",
            "shuffle_options",
            "show_correct_answers_after_publish",
            "questions_count",
            "is_active",
            "published_at",
            "archived_at",
            "created_at",
            "updated_at",
        )

    def get_owner_teacher_name(self, obj: Test) -> str:
        """
        Возвращает имя преподавателя-владельца.
        """

        if hasattr(obj.owner_teacher, "get_full_name"):
            full_name = obj.owner_teacher.get_full_name()

            if full_name:
                return full_name

        return getattr(obj.owner_teacher, "email", str(obj.owner_teacher))
