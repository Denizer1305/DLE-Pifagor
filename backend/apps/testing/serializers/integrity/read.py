from __future__ import annotations

from apps.testing.models import TestAttemptIntegrityReport
from rest_framework import serializers


class TestAttemptIntegrityReportReadSerializer(serializers.ModelSerializer):
    """
    Serializer чтения сохранённого отчёта добросовестности попытки.
    """

    attempt_id = serializers.IntegerField(read_only=True)
    test_id = serializers.IntegerField(
        source="attempt.test_id",
        read_only=True,
    )
    learner_id = serializers.IntegerField(
        source="attempt.learner_id",
        read_only=True,
    )
    test_title = serializers.CharField(
        source="attempt.test.title",
        read_only=True,
    )
    learner_email = serializers.EmailField(
        source="attempt.learner.email",
        read_only=True,
    )

    class Meta:
        model = TestAttemptIntegrityReport
        fields = (
            "id",
            "attempt_id",
            "test_id",
            "learner_id",
            "test_title",
            "learner_email",
            "score",
            "risk_level",
            "flags_data",
            "checked_at",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields
