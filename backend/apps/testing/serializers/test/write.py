from __future__ import annotations

from apps.course.models import Course, CourseLesson, CourseLessonBlock
from apps.organizations.models import Organization, Subject
from apps.testing.models import Test
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class TestWriteSerializer(serializers.ModelSerializer):
    """
    Write-сериализатор теста.
    """

    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(),
        source="course",
    )
    lesson_id = serializers.PrimaryKeyRelatedField(
        queryset=CourseLesson.objects.all(),
        source="lesson",
        required=False,
        allow_null=True,
    )
    lesson_block_id = serializers.PrimaryKeyRelatedField(
        queryset=CourseLessonBlock.objects.all(),
        source="lesson_block",
        required=False,
        allow_null=True,
    )
    organization_id = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all(),
        source="organization",
    )
    subject_id = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(),
        source="subject",
    )
    owner_teacher_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="owner_teacher",
    )

    class Meta:
        model = Test
        fields = (
            "title",
            "description",
            "instructions",
            "course_id",
            "lesson_id",
            "lesson_block_id",
            "organization_id",
            "subject_id",
            "owner_teacher_id",
            "status",
            "visibility",
            "max_attempts",
            "time_limit_minutes",
            "max_score",
            "passing_score",
            "shuffle_questions",
            "shuffle_options",
            "show_correct_answers_after_publish",
            "is_active",
        )
        extra_kwargs = {
            "description": {"required": False},
            "instructions": {"required": False},
            "status": {"required": False},
            "visibility": {"required": False},
            "max_attempts": {"required": False},
            "time_limit_minutes": {"required": False},
            "max_score": {"required": False},
            "passing_score": {"required": False},
            "shuffle_questions": {"required": False},
            "shuffle_options": {"required": False},
            "show_correct_answers_after_publish": {"required": False},
            "is_active": {"required": False},
        }
