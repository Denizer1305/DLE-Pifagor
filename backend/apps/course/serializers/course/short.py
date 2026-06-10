from __future__ import annotations

from apps.course.models import Course
from rest_framework import serializers


class CourseShortSerializer(serializers.ModelSerializer):
    """
    Краткое представление курса.
    """

    class Meta:
        model = Course
        fields = (
            "id",
            "code",
            "slug",
            "title",
            "subtitle",
            "course_type",
            "origin",
            "status",
            "visibility",
            "level",
            "language",
            "is_template",
            "is_active",
        )
