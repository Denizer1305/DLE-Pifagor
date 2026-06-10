from __future__ import annotations

from apps.course.models import CoursePlan
from apps.course.serializers.course.short import CourseShortSerializer
from rest_framework import serializers


class CoursePlanReadSerializer(serializers.ModelSerializer):
    """
    Read-сериализатор КТП курса.
    """

    course = CourseShortSerializer(read_only=True)
    imports_count = serializers.SerializerMethodField()

    class Meta:
        model = CoursePlan
        fields = (
            "id",
            "course",
            "discipline_name",
            "discipline_code",
            "specialty_code",
            "specialty_name",
            "teacher_name_snapshot",
            "organization_name_snapshot",
            "academic_year_label",
            "semester_number",
            "total_hours",
            "semester_hours",
            "theory_hours",
            "practice_hours",
            "lab_hours",
            "self_study_hours",
            "consultation_hours",
            "commission_name",
            "protocol_number",
            "protocol_date",
            "approved_order_number",
            "approved_order_date",
            "status",
            "is_active",
            "notes",
            "imports_count",
            "created_at",
            "updated_at",
        )

    def get_imports_count(self, obj: CoursePlan) -> int:
        """
        Возвращает количество импортов КТП.
        """

        return obj.imports.count()
