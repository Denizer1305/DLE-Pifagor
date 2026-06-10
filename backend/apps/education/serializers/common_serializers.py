from __future__ import annotations

from typing import Any, Callable

from apps.education.models import (
    AcademicYear,
    Curriculum,
    CurriculumItem,
    EducationPeriod,
    GroupSubject,
)
from apps.organizations.models import Department, Organization, StudyGroup, Subject
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

User = get_user_model()


def raise_drf_validation_error(error: DjangoValidationError) -> None:
    """
    Преобразует Django ValidationError в DRF ValidationError.
    """

    try:
        detail = error.message_dict
    except AttributeError:
        detail = getattr(error, "messages", str(error))

    raise serializers.ValidationError(detail)


def run_education_service(
    service: Callable[..., Any],
    **kwargs: Any,
) -> Any:
    """
    Запускает сервис и преобразует ошибки в формат DRF.
    """

    try:
        return service(**kwargs)
    except DjangoValidationError as error:
        raise_drf_validation_error(error)


class UserShortSerializer(serializers.Serializer):
    """
    Краткое представление пользователя.
    """

    id = serializers.IntegerField(read_only=True)
    email = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()

    def get_email(self, user: User) -> str:
        """
        Возвращает email пользователя.
        """

        return getattr(user, "email", "") or ""

    def get_phone(self, user: User) -> str:
        """
        Возвращает телефон пользователя.
        """

        return getattr(user, "phone", "") or ""

    def get_full_name(self, user: User) -> str:
        """
        Возвращает отображаемое имя пользователя.
        """

        full_name = getattr(user, "full_name", "")

        if full_name:
            return str(full_name)

        get_full_name = getattr(user, "get_full_name", None)

        if callable(get_full_name):
            resolved_full_name = get_full_name()

            if resolved_full_name:
                return str(resolved_full_name)

        parts = [
            getattr(user, "last_name", ""),
            getattr(user, "first_name", ""),
            getattr(user, "middle_name", ""),
        ]

        resolved_name = " ".join(part for part in parts if part).strip()

        return resolved_name or self.get_email(user) or f"Пользователь #{user.id}"


class OrganizationShortSerializer(serializers.ModelSerializer):
    """
    Краткое представление организации.
    """

    class Meta:
        model = Organization
        fields = (
            "id",
            "name",
            "short_name",
            "code",
        )


class DepartmentShortSerializer(serializers.ModelSerializer):
    """
    Краткое представление отделения.
    """

    organization = OrganizationShortSerializer(read_only=True)

    class Meta:
        model = Department
        fields = (
            "id",
            "name",
            "short_name",
            "code",
            "organization",
        )


class StudyGroupShortSerializer(serializers.ModelSerializer):
    """
    Краткое представление учебной группы.
    """

    organization = OrganizationShortSerializer(read_only=True)
    department = DepartmentShortSerializer(read_only=True)

    class Meta:
        model = StudyGroup
        fields = (
            "id",
            "name",
            "code",
            "organization",
            "department",
        )


class SubjectShortSerializer(serializers.ModelSerializer):
    """
    Краткое представление предмета.
    """

    class Meta:
        model = Subject
        fields = (
            "id",
            "name",
            "short_name",
            "code",
        )


class AcademicYearShortSerializer(serializers.ModelSerializer):
    """
    Краткое представление учебного года.
    """

    class Meta:
        model = AcademicYear
        fields = (
            "id",
            "name",
            "start_date",
            "end_date",
            "is_current",
            "is_active",
        )


class EducationPeriodShortSerializer(serializers.ModelSerializer):
    """
    Краткое представление учебного периода.
    """

    academic_year = AcademicYearShortSerializer(read_only=True)

    class Meta:
        model = EducationPeriod
        fields = (
            "id",
            "name",
            "code",
            "period_type",
            "sequence",
            "start_date",
            "end_date",
            "is_current",
            "is_active",
            "academic_year",
        )


class CurriculumShortSerializer(serializers.ModelSerializer):
    """
    Краткое представление учебного плана.
    """

    organization = OrganizationShortSerializer(read_only=True)
    department = DepartmentShortSerializer(read_only=True)
    academic_year = AcademicYearShortSerializer(read_only=True)

    class Meta:
        model = Curriculum
        fields = (
            "id",
            "code",
            "name",
            "status",
            "is_active",
            "organization",
            "department",
            "academic_year",
        )


class CurriculumItemShortSerializer(serializers.ModelSerializer):
    """
    Краткое представление элемента учебного плана.
    """

    curriculum = CurriculumShortSerializer(read_only=True)
    period = EducationPeriodShortSerializer(read_only=True)
    subject = SubjectShortSerializer(read_only=True)

    class Meta:
        model = CurriculumItem
        fields = (
            "id",
            "curriculum",
            "period",
            "subject",
            "sequence",
            "planned_hours",
            "contact_hours",
            "independent_hours",
            "assessment_type",
            "is_required",
            "is_active",
        )


class GroupSubjectShortSerializer(serializers.ModelSerializer):
    """
    Краткое представление предмета группы.
    """

    group = StudyGroupShortSerializer(read_only=True)
    subject = SubjectShortSerializer(read_only=True)
    academic_year = AcademicYearShortSerializer(read_only=True)
    period = EducationPeriodShortSerializer(read_only=True)

    class Meta:
        model = GroupSubject
        fields = (
            "id",
            "group",
            "subject",
            "academic_year",
            "period",
            "planned_hours",
            "contact_hours",
            "independent_hours",
            "assessment_type",
            "is_required",
            "is_active",
        )
