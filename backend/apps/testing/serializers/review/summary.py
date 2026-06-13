from __future__ import annotations

from rest_framework import serializers


class TestReviewSummarySerializer(serializers.Serializer):
    """
    Serializer сводки по конкретному тесту.
    """

    attempts_count = serializers.IntegerField(read_only=True)
    started_count = serializers.IntegerField(read_only=True)
    submitted_count = serializers.IntegerField(read_only=True)
    needs_review_count = serializers.IntegerField(read_only=True)
    confirmed_count = serializers.IntegerField(read_only=True)
    published_count = serializers.IntegerField(read_only=True)
    expired_count = serializers.IntegerField(read_only=True)
    cancelled_count = serializers.IntegerField(read_only=True)

    learners_count = serializers.IntegerField(read_only=True)
    passed_count = serializers.IntegerField(read_only=True)
    failed_count = serializers.IntegerField(read_only=True)
    blocked_count = serializers.IntegerField(read_only=True)
    visible_results_count = serializers.IntegerField(read_only=True)

    average_final_score = serializers.DecimalField(
        max_digits=8,
        decimal_places=2,
        read_only=True,
    )
    average_final_grade = serializers.DecimalField(
        max_digits=4,
        decimal_places=2,
        read_only=True,
    )
    average_score = serializers.DecimalField(
        max_digits=8,
        decimal_places=2,
        read_only=True,
    )
    average_grade = serializers.DecimalField(
        max_digits=4,
        decimal_places=2,
        read_only=True,
    )


class TeacherTestingSummarySerializer(serializers.Serializer):
    """
    Serializer общей сводки преподавателя по тестированию.
    """

    attempts_count = serializers.IntegerField(read_only=True)
    needs_review_count = serializers.IntegerField(read_only=True)
    confirmed_count = serializers.IntegerField(read_only=True)
    published_count = serializers.IntegerField(read_only=True)
    learners_count = serializers.IntegerField(read_only=True)
    blocked_count = serializers.IntegerField(read_only=True)

    average_final_grade = serializers.DecimalField(
        max_digits=4,
        decimal_places=2,
        read_only=True,
    )
    average_grade = serializers.DecimalField(
        max_digits=4,
        decimal_places=2,
        read_only=True,
    )
