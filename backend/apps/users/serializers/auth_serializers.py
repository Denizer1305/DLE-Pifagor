from __future__ import annotations

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    """
    Сериализатор входа пользователя.
    """

    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
    )


class TokenPairSerializer(serializers.Serializer):
    """
    Сериализатор пары JWT-токенов.
    """

    access = serializers.CharField()
    refresh = serializers.CharField(write_only=True)


class RefreshTokenSerializer(serializers.Serializer):
    """
    Сериализатор обновления access token.

    Refresh token может прийти:
        - из httpOnly cookie;
        - из тела запроса, если это нужно для тестирования или fallback-сценария.
    """

    refresh = serializers.CharField(
        required=False,
        allow_blank=True,
    )


class AccessTokenSerializer(serializers.Serializer):
    """
    Сериализатор ответа с новым access token.
    """

    access = serializers.CharField()


class EmailVerificationSerializer(serializers.Serializer):
    """
    Сериализатор подтверждения email.
    """

    token = serializers.CharField()


class ResendEmailVerificationSerializer(serializers.Serializer):
    """
    Сериализатор повторной отправки подтверждения email.
    """

    email = serializers.EmailField()


class ForgotPasswordSerializer(serializers.Serializer):
    """
    Сериализатор запроса восстановления пароля.
    """

    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    """
    Сериализатор установки нового пароля по токену.
    """

    token = serializers.CharField()
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        trim_whitespace=False,
    )
    password_confirm = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
    )

    def validate_password(self, value):
        """
        Проверяет сложность пароля.
        """

        validate_password(value)

        if not any(char.isupper() for char in value):
            raise serializers.ValidationError(
                "Пароль должен содержать хотя бы одну заглавную букву."
            )

        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError(
                "Пароль должен содержать хотя бы одну цифру."
            )

        return value

    def validate(self, attrs):
        """
        Проверяет совпадение паролей.
        """

        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError(
                {
                    "password_confirm": "Пароли не совпадают.",
                }
            )

        return attrs
