from __future__ import annotations

from apps.testing.models import Test, TestAttempt
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class TestAttemptWriteSerializer(serializers.ModelSerializer):
    """
    Write-сериализатор попытки теста.
    """

    test_id = serializers.PrimaryKeyRelatedField(
        queryset=Test.objects.all(),
        source="test",
    )
    learner_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="learner",
    )
    reviewer_teacher_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="reviewer_teacher",
        required=False,
        allow_null=True,
    )

    class Meta:
        model = TestAttempt
        fields = (
            "test_id",
            "learner_id",
            "attempt_number",
            "status",
            "check_status",
            "started_at",
            "submitted_at",
            "auto_checked_at",
            "reviewed_at",
            "confirmed_at",
            "published_at",
            "auto_score",
            "teacher_score",
            "final_score",
            "auto_grade",
            "teacher_grade",
            "final_grade",
            "requires_manual_review",
            "is_confirmed_by_teacher",
            "is_visible_to_learner",
            "is_visible_to_guardian",
            "reviewer_teacher_id",
            "teacher_comment",
        )
        extra_kwargs = {
            "attempt_number": {"required": False},
            "status": {"required": False},
            "check_status": {"required": False},
            "started_at": {"required": False, "allow_null": True},
            "submitted_at": {"required": False, "allow_null": True},
            "auto_checked_at": {"required": False, "allow_null": True},
            "reviewed_at": {"required": False, "allow_null": True},
            "confirmed_at": {"required": False, "allow_null": True},
            "published_at": {"required": False, "allow_null": True},
            "auto_score": {"required": False},
            "teacher_score": {"required": False, "allow_null": True},
            "final_score": {"required": False, "allow_null": True},
            "auto_grade": {"required": False, "allow_null": True},
            "teacher_grade": {"required": False, "allow_null": True},
            "final_grade": {"required": False, "allow_null": True},
            "requires_manual_review": {"required": False},
            "is_confirmed_by_teacher": {"required": False},
            "is_visible_to_learner": {"required": False},
            "is_visible_to_guardian": {"required": False},
            "teacher_comment": {"required": False},
        }
