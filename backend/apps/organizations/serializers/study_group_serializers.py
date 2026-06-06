from __future__ import annotations

from apps.organizations.constants import StudyForm, StudyGroupStatus
from apps.organizations.models import Department, Organization, StudyGroup
from apps.organizations.serializers.department_serializers import (
    DepartmentShortSerializer,
)
from apps.organizations.serializers.organization_serializers import (
    OrganizationShortSerializer,
)
from rest_framework import serializers


class StudyGroupShortSerializer(serializers.ModelSerializer):
    """
    Короткое представление учебной группы.
    """

    class Meta:
        model = StudyGroup
        fields = (
            "id",
            "name",
            "code",
            "course_number",
            "status",
        )
        read_only_fields = fields


class StudyGroupListSerializer(serializers.ModelSerializer):
    """
    Учебная группа для административного списка.
    """

    organization = OrganizationShortSerializer(read_only=True)
    department = DepartmentShortSerializer(read_only=True)
    has_active_join_code = serializers.BooleanField(read_only=True)

    class Meta:
        model = StudyGroup
        fields = (
            "id",
            "organization",
            "department",
            "name",
            "code",
            "admission_year",
            "graduation_year",
            "course_number",
            "study_form",
            "status",
            "is_active",
            "is_archived",
            "has_active_join_code",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields


class StudyGroupDetailSerializer(serializers.ModelSerializer):
    """
    Детальная карточка учебной группы.
    """

    organization = OrganizationShortSerializer(read_only=True)
    department = DepartmentShortSerializer(read_only=True)
    has_active_join_code = serializers.BooleanField(read_only=True)

    class Meta:
        model = StudyGroup
        fields = (
            "id",
            "organization",
            "department",
            "name",
            "code",
            "description",
            "admission_year",
            "graduation_year",
            "course_number",
            "study_form",
            "status",
            "is_active",
            "is_archived",
            "join_code_is_active",
            "join_code_expires_at",
            "has_active_join_code",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields


class StudyGroupWriteSerializer(serializers.Serializer):
    """
    Сериализатор создания и редактирования учебной группы.
    """

    organization_id = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all(),
        source="organization",
        required=False,
    )
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(),
        source="department",
        required=False,
        allow_null=True,
    )
    name = serializers.CharField(
        required=False,
        max_length=120,
    )
    code = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=64,
    )
    admission_year = serializers.IntegerField(
        required=False,
        allow_null=True,
        min_value=1900,
        max_value=2200,
    )
    graduation_year = serializers.IntegerField(
        required=False,
        allow_null=True,
        min_value=1900,
        max_value=2200,
    )
    course_number = serializers.IntegerField(
        required=False,
        allow_null=True,
        min_value=1,
        max_value=6,
    )
    study_form = serializers.ChoiceField(
        required=False,
        choices=StudyForm.choices,
    )
    status = serializers.ChoiceField(
        required=False,
        choices=StudyGroupStatus.choices,
    )
    description = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    def validate(self, attrs):
        """
        Проверяет данные учебной группы.
        """

        if self.context.get("is_create") and not attrs.get("organization"):
            raise serializers.ValidationError(
                {
                    "organization_id": "Необходимо указать организацию.",
                }
            )

        if self.context.get("is_create") and not attrs.get("name"):
            raise serializers.ValidationError(
                {
                    "name": "Название группы обязательно.",
                }
            )

        organization = attrs.get("organization")
        department = attrs.get("department")

        if organization and department:
            if department.organization_id != organization.id:
                raise serializers.ValidationError(
                    {
                        "department_id": (
                            "Отделение должно принадлежать выбранной организации."
                        )
                    }
                )

        admission_year = attrs.get("admission_year")
        graduation_year = attrs.get("graduation_year")

        if (
            admission_year
            and graduation_year
            and graduation_year < admission_year
        ):
            raise serializers.ValidationError(
                {
                    "graduation_year": (
                        "Год выпуска не может быть раньше года поступления."
                    )
                }
            )

        return attrs


class GroupJoinCodeSetSerializer(serializers.Serializer):
    """
    Сериализатор установки кода вступления в группу.
    """

    raw_code = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=64,
    )
    expires_at = serializers.DateTimeField(
        required=False,
        allow_null=True,
    )


class GroupJoinCodeOutputSerializer(serializers.Serializer):
    """
    Результат установки кода вступления в группу.

    raw_code возвращается только один раз.
    """

    group = StudyGroupDetailSerializer()
    raw_code = serializers.CharField()