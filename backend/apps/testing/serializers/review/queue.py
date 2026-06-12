from __future__ import annotations

from apps.testing.models import TestAttempt
from rest_framework import serializers


class TestAttemptReviewQueueSerializer(serializers.ModelSerializer):
    """
    Serializer очереди проверки попыток для преподавателя.
    """

    test_title = serializers.CharField(
        source="test.title",
        read_only=True,
    )
    course_title = serializers.CharField(
        source="test.course.title",
        read_only=True,
    )
    learner_email = serializers.EmailField(
        source="learner.email",
        read_only=True,
    )
    reviewer_teacher_email = serializers.EmailField(
        source="reviewer_teacher.email",
        read_only=True,
        allow_null=True,
    )
    manual_answers_count = serializers.IntegerField(read_only=True)

    integrity_risk_level = serializers.CharField(
        source="integrity_report.risk_level",
        read_only=True,
        allow_null=True,
    )
    integrity_score = serializers.IntegerField(
        source="integrity_report.score",
        read_only=True,
        allow_null=True,
    )

    class Meta:
        model = TestAttempt
        fields = (
            "id",
            "test",
            "test_title",
            "course_title",
            "learner",
            "learner_email",
            "attempt_number",
            "status",
            "check_status",
            "requires_manual_review",
            "manual_answers_count",
            "auto_score",
            "teacher_score",
            "final_score",
            "auto_grade",
            "teacher_grade",
            "final_grade",
            "reviewer_teacher",
            "reviewer_teacher_email",
            "integrity_risk_level",
            "integrity_score",
            "started_at",
            "submitted_at",
            "reviewed_at",
            "updated_at",
        )
        read_only_fields = fields
