from __future__ import annotations

from apps.testing.models import TestLearnerResult
from rest_framework import serializers


class TestLearnerResultReadSerializer(serializers.ModelSerializer):
    """
    Read-сериализатор итогового результата обучающегося по тесту.
    """

    test_title = serializers.CharField(
        source="test.title",
        read_only=True,
    )
    learner_name = serializers.SerializerMethodField()

    class Meta:
        model = TestLearnerResult
        fields = (
            "id",
            "test",
            "test_title",
            "learner",
            "learner_name",
            "status",
            "grade_source",
            "confirmed_attempts_count",
            "attempts_count",
            "average_score",
            "average_grade",
            "best_score",
            "best_grade",
            "last_attempt",
            "is_passed",
            "is_blocked",
            "is_visible_to_learner",
            "is_visible_to_guardian",
            "created_at",
            "updated_at",
        )

    def get_learner_name(self, obj: TestLearnerResult) -> str:
        """
        Возвращает имя обучающегося.
        """

        if hasattr(obj.learner, "get_full_name"):
            full_name = obj.learner.get_full_name()

            if full_name:
                return full_name

        return getattr(obj.learner, "email", str(obj.learner))
