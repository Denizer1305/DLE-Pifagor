from __future__ import annotations

from apps.users.models import Profile
from rest_framework import serializers


class CurrentProfileRoleSerializer(serializers.Serializer):
    """
    Сериализатор активной роли пользователя.
    """

    code = serializers.CharField()
    label = serializers.CharField()


class CurrentProfileIdentitySerializer(serializers.Serializer):
    """
    Сериализатор основных персональных данных профиля.
    """

    id = serializers.IntegerField()
    email = serializers.EmailField()
    phone = serializers.CharField(allow_blank=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    middle_name = serializers.CharField(allow_blank=True)
    full_name = serializers.CharField()
    birth_date = serializers.DateField(allow_null=True)
    gender = serializers.CharField()
    city = serializers.CharField(allow_blank=True)
    about = serializers.CharField(allow_blank=True)
    avatar_url = serializers.CharField(allow_blank=True)
    timezone = serializers.CharField(allow_blank=True)


class CurrentProfileContactsSerializer(serializers.Serializer):
    """
    Сериализатор контактных данных профиля.
    """

    email = serializers.EmailField()
    backup_email = serializers.EmailField(allow_blank=True)
    phone = serializers.CharField(allow_blank=True)
    vk_url = serializers.CharField(allow_blank=True)
    max_url = serializers.CharField(allow_blank=True)
    preferred_contact_method = serializers.CharField()
    is_email_verified = serializers.BooleanField()
    is_phone_verified = serializers.BooleanField()
    show_email = serializers.BooleanField()
    show_phone = serializers.BooleanField()


class CurrentProfileDisplaySettingsSerializer(serializers.Serializer):
    """
    Сериализатор настроек отображения профиля.
    """

    show_email = serializers.BooleanField()
    show_phone = serializers.BooleanField()
    email_notifications = serializers.BooleanField()
    push_notifications = serializers.BooleanField()


class CurrentProfileSerializer(serializers.Serializer):
    """
    Сериализатор страницы «Мой профиль».
    """

    identity = CurrentProfileIdentitySerializer()
    contacts = CurrentProfileContactsSerializer()
    display_settings = CurrentProfileDisplaySettingsSerializer()
    active_role = CurrentProfileRoleSerializer()
    role_profile = serializers.DictField()
    available_roles = serializers.ListField(child=serializers.CharField())


class CurrentProfileUpdateSerializer(serializers.Serializer):
    """
    Сериализатор формы редактирования текущего профиля.
    """

    first_name = serializers.CharField(
        max_length=150,
        required=False,
    )
    last_name = serializers.CharField(
        max_length=150,
        required=False,
    )
    middle_name = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=150,
    )
    birth_date = serializers.DateField(
        required=False,
        allow_null=True,
    )

    gender = serializers.ChoiceField(
        choices=Profile.GenderChoices.choices,
        required=False,
    )
    city = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=150,
    )
    about = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    phone = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=32,
    )
    backup_email = serializers.EmailField(
        required=False,
        allow_blank=True,
    )
    vk_url = serializers.URLField(
        required=False,
        allow_blank=True,
    )
    max_url = serializers.URLField(
        required=False,
        allow_blank=True,
    )

    preferred_contact_method = serializers.ChoiceField(
        choices=[
            "email",
            "phone",
            "vk",
            "max",
        ],
        required=False,
    )

    show_email = serializers.BooleanField(required=False)
    show_phone = serializers.BooleanField(required=False)
    email_notifications = serializers.BooleanField(required=False)
    push_notifications = serializers.BooleanField(required=False)

    role_profile = serializers.DictField(required=False)

    def validate(self, attrs):
        """
        Нормализует входные данные формы профиля.
        """

        for field in [
            "first_name",
            "last_name",
            "middle_name",
            "city",
            "about",
            "phone",
        ]:
            if field in attrs and isinstance(attrs[field], str):
                attrs[field] = attrs[field].strip()

        if (
            attrs.get("backup_email")
            and self.context.get("primary_email")
            and attrs["backup_email"].lower() == self.context["primary_email"].lower()
        ):
            raise serializers.ValidationError(
                {"backup_email": "Резервный email должен отличаться от основного."}
            )

        return attrs


class CurrentProfileAvatarSerializer(serializers.Serializer):
    """
    Сериализатор загрузки аватара текущего пользователя.
    """

    avatar = serializers.ImageField()
