from __future__ import annotations

from apps.users.models import TeacherProfile
from apps.users.serializers.user_serializers import UserShortSerializer
from rest_framework import serializers


class TeacherProfileSerializer(serializers.ModelSerializer):
    """
    Сериализатор профиля преподавателя.
    """

    user = UserShortSerializer(read_only=True)
    verified_by = UserShortSerializer(read_only=True)

    class Meta:
        model = TeacherProfile
        fields = [
            "id",
            "user",
            "organization",
            "department",
            "position",
            "public_title",
            "short_bio",
            "bio",
            "education",
            "experience_years",
            "achievements",
            "cover_image",
            "is_public",
            "show_on_teachers_page",
            "status",
            "code_verified_at",
            "verified_by",
            "verified_at",
            "verification_comment",
            "hired_at",
            "dismissed_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "user",
            "status",
            "code_verified_at",
            "verified_by",
            "verified_at",
            "verification_comment",
            "created_at",
            "updated_at",
        ]


class TeacherProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор обновления профиля преподавателя.
    """

    class Meta:
        model = TeacherProfile
        fields = [
            "position",
            "public_title",
            "short_bio",
            "bio",
            "education",
            "experience_years",
            "achievements",
            "cover_image",
            "is_public",
            "show_on_teachers_page",
            "hired_at",
            "dismissed_at",
        ]


class PublicTeacherProfileSerializer(serializers.ModelSerializer):
    """
    Публичный сериализатор преподавателя.

    Используется для страницы преподавателей.
    """

    user = UserShortSerializer(read_only=True)

    class Meta:
        model = TeacherProfile
        fields = [
            "id",
            "user",
            "organization",
            "department",
            "position",
            "public_title",
            "short_bio",
            "bio",
            "education",
            "experience_years",
            "achievements",
            "cover_image",
        ]
        read_only_fields = fields
