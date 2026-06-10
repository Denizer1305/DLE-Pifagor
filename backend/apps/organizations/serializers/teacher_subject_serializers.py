from __future__ import annotations

from apps.organizations.models import Subject, TeacherSubject
from apps.organizations.serializers.subject_serializers import SubjectShortSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class TeacherSubjectListSerializer(serializers.ModelSerializer):
    """
    Предмет преподавателя для административного списка.
    """

    subject = SubjectShortSerializer(read_only=True)
    teacher_full_name = serializers.CharField(
        source="teacher.get_full_name",
        read_only=True,
    )
    teacher_email = serializers.EmailField(
        source="teacher.email",
        read_only=True,
    )
    teacher_phone = serializers.CharField(
        source="teacher.phone",
        read_only=True,
    )

    class Meta:
        model = TeacherSubject
        fields = (
            "id",
            "teacher",
            "teacher_full_name",
            "teacher_email",
            "teacher_phone",
            "subject",
            "is_primary",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields


class TeacherSubjectDetailSerializer(serializers.ModelSerializer):
    """
    Детальная карточка предмета преподавателя.
    """

    subject = SubjectShortSerializer(read_only=True)
    teacher_full_name = serializers.CharField(
        source="teacher.get_full_name",
        read_only=True,
    )
    teacher_email = serializers.EmailField(
        source="teacher.email",
        read_only=True,
    )
    teacher_phone = serializers.CharField(
        source="teacher.phone",
        read_only=True,
    )

    class Meta:
        model = TeacherSubject
        fields = (
            "id",
            "teacher",
            "teacher_full_name",
            "teacher_email",
            "teacher_phone",
            "subject",
            "is_primary",
            "is_active",
            "notes",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields


class TeacherSubjectWriteSerializer(serializers.Serializer):
    """
    Сериализатор создания и редактирования предмета преподавателя.
    """

    teacher_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="teacher",
        required=False,
    )
    subject_id = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(),
        source="subject",
        required=False,
    )
    is_primary = serializers.BooleanField(required=False)
    is_active = serializers.BooleanField(required=False)
    notes = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    def validate(self, attrs):
        """
        Проверяет данные связи преподавателя с предметом.
        """

        if self.context.get("is_create") and not attrs.get("teacher"):
            raise serializers.ValidationError(
                {
                    "teacher_id": "Необходимо указать преподавателя.",
                }
            )

        if self.context.get("is_create") and not attrs.get("subject"):
            raise serializers.ValidationError(
                {
                    "subject_id": "Необходимо указать учебный предмет.",
                }
            )

        return attrs
