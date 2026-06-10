from __future__ import annotations

from apps.organizations.models import Organization, Subject
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserShortSerializer(serializers.ModelSerializer):
    """
    Краткое представление пользователя.
    """

    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "full_name",
        )

    def get_full_name(self, obj: User) -> str:
        """
        Возвращает полное имя пользователя.
        """

        full_name = f"{obj.last_name} {obj.first_name}".strip()

        return full_name or obj.email


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
