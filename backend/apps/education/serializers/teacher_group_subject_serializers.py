from __future__ import annotations

from apps.education.models import GroupSubject, TeacherGroupSubject
from apps.education.services import (
    create_teacher_group_subject,
    update_teacher_group_subject,
)
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .common_serializers import (
    GroupSubjectShortSerializer,
    UserShortSerializer,
    run_education_service,
)

User = get_user_model()


class TeacherGroupSubjectReadSerializer(serializers.ModelSerializer):
    """
    Сериализатор чтения назначения преподавателя на предмет группы.
    """

    teacher = UserShortSerializer(read_only=True)
    group_subject = GroupSubjectShortSerializer(read_only=True)

    class Meta:
        model = TeacherGroupSubject
        fields = (
            "id",
            "teacher",
            "group_subject",
            "role",
            "is_primary",
            "is_active",
            "planned_hours",
            "starts_at",
            "ends_at",
            "notes",
            "created_at",
            "updated_at",
        )


class TeacherGroupSubjectWriteSerializer(serializers.ModelSerializer):
    """
    Сериализатор создания и обновления назначения преподавателя.
    """

    teacher_id = serializers.PrimaryKeyRelatedField(
        source="teacher",
        queryset=User.objects.all(),
        write_only=True,
    )
    group_subject_id = serializers.PrimaryKeyRelatedField(
        source="group_subject",
        queryset=GroupSubject.objects.all(),
        write_only=True,
    )

    class Meta:
        model = TeacherGroupSubject
        fields = (
            "teacher_id",
            "group_subject_id",
            "role",
            "is_primary",
            "is_active",
            "planned_hours",
            "starts_at",
            "ends_at",
            "notes",
        )

    def create(self, validated_data: dict) -> TeacherGroupSubject:
        """
        Создаёт назначение преподавателя через сервис.
        """

        return run_education_service(
            create_teacher_group_subject,
            data=validated_data,
        )

    def update(
        self,
        instance: TeacherGroupSubject,
        validated_data: dict,
    ) -> TeacherGroupSubject:
        """
        Обновляет назначение преподавателя через сервис.
        """

        return run_education_service(
            update_teacher_group_subject,
            assignment=instance,
            data=validated_data,
        )
