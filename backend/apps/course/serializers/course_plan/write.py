from __future__ import annotations

from apps.course.models import Course, CoursePlan
from apps.course.services import create_course_plan, update_course_plan
from rest_framework import serializers


class CoursePlanWriteSerializer(serializers.ModelSerializer):
    """
    Write-сериализатор КТП курса.
    """

    course_id = serializers.IntegerField()

    class Meta:
        model = CoursePlan
        fields = (
            "course_id",
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
        )
        extra_kwargs = {
            "discipline_code": {
                "required": False,
                "allow_blank": True,
            },
            "specialty_code": {
                "required": False,
                "allow_blank": True,
            },
            "specialty_name": {
                "required": False,
                "allow_blank": True,
            },
            "teacher_name_snapshot": {
                "required": False,
                "allow_blank": True,
            },
            "organization_name_snapshot": {
                "required": False,
                "allow_blank": True,
            },
            "academic_year_label": {
                "required": False,
                "allow_blank": True,
            },
            "commission_name": {
                "required": False,
                "allow_blank": True,
            },
            "protocol_number": {
                "required": False,
                "allow_blank": True,
            },
            "approved_order_number": {
                "required": False,
                "allow_blank": True,
            },
            "notes": {
                "required": False,
                "allow_blank": True,
            },
            "protocol_date": {
                "required": False,
                "allow_null": True,
            },
            "approved_order_date": {
                "required": False,
                "allow_null": True,
            },
            "is_active": {
                "required": False,
            },
        }

    def validate_course_id(
        self,
        value: int,
    ) -> int:
        """
        Проверяет существование курса.
        """

        if not Course.objects.filter(id=value).exists():
            raise serializers.ValidationError("Курс не найден.")

        return value

    def create(self, validated_data: dict) -> CoursePlan:
        """
        Создаёт КТП через сервисный слой.
        """

        return create_course_plan(data=validated_data)

    def update(
        self,
        instance: CoursePlan,
        validated_data: dict,
    ) -> CoursePlan:
        """
        Обновляет КТП через сервисный слой.
        """

        return update_course_plan(
            plan=instance,
            data=validated_data,
        )
