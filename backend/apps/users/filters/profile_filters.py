from __future__ import annotations

import django_filters
from apps.users.constants.lifecycle import GuardianLearnerStatus, ProfileStatus
from apps.users.constants.moderation import ModerationStatus
from apps.users.models import (
    GuardianLearner,
    GuardianProfile,
    LearnerProfile,
    Profile,
    TeacherProfile,
)


class ProfileFilter(django_filters.FilterSet):
    """
    Фильтр базовых профилей пользователей.
    """

    gender = django_filters.CharFilter(
        field_name="gender",
        label="Пол",
    )
    city = django_filters.CharFilter(
        field_name="city",
        lookup_expr="icontains",
        label="Город",
    )
    avatar_moderation_status = django_filters.ChoiceFilter(
        field_name="avatar_moderation_status",
        choices=ModerationStatus.choices,
        label="Статус модерации аватара",
    )
    profile_moderation_status = django_filters.ChoiceFilter(
        field_name="profile_moderation_status",
        choices=ModerationStatus.choices,
        label="Статус модерации профиля",
    )

    class Meta:
        model = Profile
        fields = [
            "gender",
            "city",
            "avatar_moderation_status",
            "profile_moderation_status",
        ]


class LearnerProfileFilter(django_filters.FilterSet):
    """
    Фильтр профилей учащихся.
    """

    status = django_filters.ChoiceFilter(
        field_name="status",
        choices=ProfileStatus.choices,
        label="Статус профиля",
    )
    organization = django_filters.NumberFilter(
        field_name="organization_id",
        label="ID организации",
    )
    department = django_filters.NumberFilter(
        field_name="department_id",
        label="ID отделения",
    )
    group = django_filters.NumberFilter(
        field_name="group_id",
        label="ID группы",
    )
    curator = django_filters.NumberFilter(
        field_name="curator_id",
        label="ID куратора",
    )
    is_minor = django_filters.BooleanFilter(
        field_name="is_minor",
        label="Младше 14 лет",
    )
    admission_year = django_filters.NumberFilter(
        field_name="admission_year",
        label="Год поступления",
    )
    created_by_guardian = django_filters.NumberFilter(
        field_name="created_by_guardian_id",
        label="ID родителя, создавшего профиль",
    )

    class Meta:
        model = LearnerProfile
        fields = [
            "status",
            "organization",
            "department",
            "group",
            "curator",
            "is_minor",
            "admission_year",
            "created_by_guardian",
        ]


class GuardianProfileFilter(django_filters.FilterSet):
    """
    Фильтр профилей родителей и законных представителей.
    """

    status = django_filters.ChoiceFilter(
        field_name="status",
        choices=ProfileStatus.choices,
        label="Статус профиля",
    )
    occupation = django_filters.CharFilter(
        field_name="occupation",
        lookup_expr="icontains",
        label="Род деятельности",
    )
    work_place = django_filters.CharFilter(
        field_name="work_place",
        lookup_expr="icontains",
        label="Место работы",
    )

    class Meta:
        model = GuardianProfile
        fields = [
            "status",
            "occupation",
            "work_place",
        ]


class TeacherProfileFilter(django_filters.FilterSet):
    """
    Фильтр профилей преподавателей.
    """

    status = django_filters.ChoiceFilter(
        field_name="status",
        choices=ProfileStatus.choices,
        label="Статус профиля",
    )
    organization = django_filters.NumberFilter(
        field_name="organization_id",
        label="ID организации",
    )
    department = django_filters.NumberFilter(
        field_name="department_id",
        label="ID отделения",
    )
    is_public = django_filters.BooleanFilter(
        field_name="is_public",
        label="Публичный профиль",
    )
    show_on_teachers_page = django_filters.BooleanFilter(
        field_name="show_on_teachers_page",
        label="Показывать на странице преподавателей",
    )
    experience_years_min = django_filters.NumberFilter(
        field_name="experience_years",
        lookup_expr="gte",
        label="Минимальный стаж",
    )
    experience_years_max = django_filters.NumberFilter(
        field_name="experience_years",
        lookup_expr="lte",
        label="Максимальный стаж",
    )

    class Meta:
        model = TeacherProfile
        fields = [
            "status",
            "organization",
            "department",
            "is_public",
            "show_on_teachers_page",
        ]


class GuardianLearnerFilter(django_filters.FilterSet):
    """
    Фильтр связей родителей и учащихся.
    """

    guardian = django_filters.NumberFilter(
        field_name="guardian_id",
        label="ID родителя",
    )
    learner = django_filters.NumberFilter(
        field_name="learner_id",
        label="ID учащегося",
    )
    status = django_filters.ChoiceFilter(
        field_name="status",
        choices=GuardianLearnerStatus.choices,
        label="Статус связи",
    )
    relation_type = django_filters.CharFilter(
        field_name="relation_type",
        label="Тип связи",
    )
    is_primary = django_filters.BooleanFilter(
        field_name="is_primary",
        label="Основной представитель",
    )
    is_learner_consent_required = django_filters.BooleanFilter(
        field_name="is_learner_consent_required",
        label="Требуется согласие учащегося",
    )

    class Meta:
        model = GuardianLearner
        fields = [
            "guardian",
            "learner",
            "status",
            "relation_type",
            "is_primary",
            "is_learner_consent_required",
        ]
