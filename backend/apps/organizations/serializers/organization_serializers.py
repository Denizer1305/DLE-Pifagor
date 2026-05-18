from __future__ import annotations

from apps.organizations.models import Organization, Subject
from rest_framework import serializers


class PublicOrganizationSerializer(serializers.ModelSerializer):
    """
    Публичная информация об образовательной организации.
    """

    logo_url = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = (
            "id",
            "name",
            "short_name",
            "slug",
            "code",
            "description",
            "city",
            "address",
            "phone",
            "email",
            "website",
            "logo_url",
            "is_default_public",
        )

    def get_logo_url(self, obj: Organization) -> str:
        """
        Возвращает абсолютный URL логотипа.

        Args:
            obj:
                Организация.

        Returns:
            str: URL логотипа.
        """

        if not obj.logo:
            return ""

        request = self.context.get("request")

        if request:
            return request.build_absolute_uri(obj.logo.url)

        return obj.logo.url


class PublicSubjectSerializer(serializers.ModelSerializer):
    """
    Публичный учебный предмет для фильтрации преподавателей.
    """

    class Meta:
        model = Subject
        fields = (
            "id",
            "name",
            "short_name",
            "code",
        )
