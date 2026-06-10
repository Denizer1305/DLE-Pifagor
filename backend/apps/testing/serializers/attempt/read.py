from __future__ import annotations

from apps.testing.models import TestAttempt
from rest_framework import serializers


class TestAttemptReadSerializer(serializers.ModelSerializer):
    """
    Read-сериализатор попытки теста.
    """

    test_title = serializers.CharField(
        source="test.title",
        read_only=True,
    )
    learner_name = serializers.SerializerMethodField()
    reviewer_teacher_name = serializers.SerializerMethodField()

    class Meta:
        model = TestAttempt
        fields = (
            "id",
            "test",
            "test_title",
            "learner",
            "learner_name",
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
            "reviewer_teacher",
            "reviewer_teacher_name",
            "teacher_comment",
            "created_at",
            "updated_at",
        )

    def get_learner_name(self, obj: TestAttempt) -> str:
        """
        Возвращает имя обучающегося.
        """

        return _get_user_display_name(user=obj.learner)

    def get_reviewer_teacher_name(self, obj: TestAttempt) -> str | None:
        """
        Возвращает имя проверяющего преподавателя.
        """

        if obj.reviewer_teacher is None:
            return None

        return _get_user_display_name(user=obj.reviewer_teacher)


def _get_user_display_name(*, user) -> str:
    """
    Возвращает отображаемое имя пользователя.
    """

    if hasattr(user, "get_full_name"):
        full_name = user.get_full_name()

        if full_name:
            return full_name

    return getattr(user, "email", str(user))
