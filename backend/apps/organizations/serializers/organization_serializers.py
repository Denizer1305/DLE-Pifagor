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


class OrganizationShortSerializer(serializers.ModelSerializer):
    """
    Короткое представление образовательной организации.
    """

    class Meta:
        model = Organization
        fields = (
            "id",
            "name",
            "short_name",
            "slug",
            "code",
            "city",
        )
        read_only_fields = fields


class OrganizationListSerializer(serializers.ModelSerializer):
    """
    Организация для административного списка.
    """

    has_active_teacher_registration_code = serializers.BooleanField(
        read_only=True,
    )

    class Meta:
        model = Organization
        fields = (
            "id",
            "name",
            "short_name",
            "slug",
            "code",
            "city",
            "is_active",
            "is_public",
            "is_default_public",
            "has_active_teacher_registration_code",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields


class OrganizationDetailSerializer(serializers.ModelSerializer):
    """
    Детальная карточка организации для административного раздела.
    """

    logo_url = serializers.SerializerMethodField()
    has_active_teacher_registration_code = serializers.BooleanField(
        read_only=True,
    )

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
            "logo",
            "logo_url",
            "is_active",
            "is_public",
            "is_default_public",
            "teacher_registration_code_is_active",
            "teacher_registration_code_expires_at",
            "has_active_teacher_registration_code",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "logo_url",
            "teacher_registration_code_is_active",
            "teacher_registration_code_expires_at",
            "has_active_teacher_registration_code",
            "created_at",
            "updated_at",
        )

    def get_logo_url(self, obj: Organization) -> str:
        """
        Возвращает абсолютный URL логотипа.
        """

        if not obj.logo:
            return ""

        request = self.context.get("request")

        if request:
            return request.build_absolute_uri(obj.logo.url)

        return obj.logo.url


class OrganizationWriteSerializer(serializers.Serializer):
    """
    Сериализатор создания и редактирования организации.

    Код регистрации преподавателя здесь не меняется.
    """

    name = serializers.CharField(
        required=False,
        max_length=255,
    )
    short_name = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=120,
    )
    slug = serializers.SlugField(
        required=False,
        allow_blank=True,
        max_length=160,
    )
    code = serializers.CharField(
        required=False,
        max_length=64,
    )
    description = serializers.CharField(
        required=False,
        allow_blank=True,
    )
    city = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=150,
    )
    address = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=255,
    )
    phone = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=32,
    )
    email = serializers.EmailField(
        required=False,
        allow_blank=True,
    )
    website = serializers.URLField(
        required=False,
        allow_blank=True,
    )
    logo = serializers.ImageField(
        required=False,
        allow_null=True,
    )
    is_public = serializers.BooleanField(required=False)
    is_default_public = serializers.BooleanField(required=False)

    def validate(self, attrs):
        """
        Проверяет обязательные поля при создании.
        """

        if self.context.get("is_create") and not attrs.get("name"):
            raise serializers.ValidationError(
                {
                    "name": "Название организации обязательно.",
                }
            )

        if self.context.get("is_create") and not attrs.get("code"):
            raise serializers.ValidationError(
                {
                    "code": "Код организации обязателен.",
                }
            )

        return attrs


class TeacherRegistrationCodeSetSerializer(serializers.Serializer):
    """
    Сериализатор установки кода регистрации преподавателя.
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


class TeacherRegistrationCodeOutputSerializer(serializers.Serializer):
    """
    Результат установки кода регистрации преподавателя.

    raw_code возвращается только один раз.
    """

    organization = OrganizationDetailSerializer()
    raw_code = serializers.CharField()
