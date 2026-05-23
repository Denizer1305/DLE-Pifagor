from __future__ import annotations

from apps.users.models import User
from apps.users.selectors.role_selectors import get_user_active_role_codes
from rest_framework import serializers


class UserShortSerializer(serializers.ModelSerializer):
    """
    Краткий сериализатор пользователя.

    Используется во вложенных объектах:
        - роли;
        - профили;
        - заявки;
        - аудит.
    """

    full_name = serializers.CharField(
        source="get_full_name",
        read_only=True,
    )

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "phone",
            "first_name",
            "last_name",
            "middle_name",
            "full_name",
        ]
        read_only_fields = fields


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Детальный сериализатор пользователя.

    Используется для просмотра собственного профиля пользователя
    и административного просмотра.
    """

    full_name = serializers.CharField(
        source="get_full_name",
        read_only=True,
    )
    active_roles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "backup_email",
            "phone",
            "first_name",
            "last_name",
            "middle_name",
            "full_name",
            "birth_date",
            "status",
            "is_active",
            "is_staff",
            "is_superuser",
            "is_email_verified",
            "email_verified_at",
            "is_phone_verified",
            "phone_verified_at",
            "is_login_allowed",
            "account_managed_by",
            "login_available_from",
            "login_activation_requested_at",
            "login_activated_at",
            "scheduled_for_deletion_at",
            "anonymized_at",
            "created_at",
            "updated_at",
            "active_roles",
        ]
        read_only_fields = [
            "id",
            "status",
            "is_active",
            "is_staff",
            "is_superuser",
            "is_email_verified",
            "email_verified_at",
            "is_phone_verified",
            "phone_verified_at",
            "is_login_allowed",
            "account_managed_by",
            "login_available_from",
            "login_activation_requested_at",
            "login_activated_at",
            "scheduled_for_deletion_at",
            "anonymized_at",
            "created_at",
            "updated_at",
            "active_roles",
        ]

    def get_active_roles(self, obj):
        return sorted(get_user_active_role_codes(obj))


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор обновления базовых данных пользователя.

    Не управляет ролями, статусом, подтверждением email/phone
    и жизненным циклом аккаунта.
    """

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "middle_name",
            "birth_date",
        ]

    def validate(self, attrs):
        """
        Проверяет данные пользователя перед обновлением.

        Args:
            attrs:
                Данные serializer.

        Returns:
            dict: Проверенные данные.
        """

        return attrs
