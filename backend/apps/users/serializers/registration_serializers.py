from __future__ import annotations

from apps.users.validators.registration_validators import (
    validate_guardian_can_create_minor_learner,
    validate_learner_self_registration_age,
    validate_minor_learner_age,
    validate_registration_contacts,
)
from rest_framework import serializers


class BaseRegistrationSerializer(serializers.Serializer):
    """
    Базовый сериализатор регистрации пользователя.
    """

    email = serializers.EmailField()
    phone = serializers.CharField(max_length=32)
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        trim_whitespace=False,
    )
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    middle_name = serializers.CharField(
        max_length=150,
        required=False,
        allow_blank=True,
    )
    birth_date = serializers.DateField(required=False, allow_null=True)

    def validate(self, attrs):
        """
        Проверяет контакты пользователя.

        Args:
            attrs:
                Данные serializer.

        Returns:
            dict: Проверенные данные.
        """

        validate_registration_contacts(
            email=attrs.get("email"),
            phone=attrs.get("phone"),
        )

        return attrs


class TeacherRegistrationSerializer(BaseRegistrationSerializer):
    """
    Сериализатор регистрации преподавателя.
    """

    invite_code = serializers.CharField(max_length=128)
    position = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=255,
    )


class LearnerRegistrationSerializer(BaseRegistrationSerializer):
    """
    Сериализатор регистрации учащегося старше 14 лет.
    """

    def validate(self, attrs):
        """
        Проверяет контакты и возраст учащегося.

        Args:
            attrs:
                Данные serializer.

        Returns:
            dict: Проверенные данные.
        """

        attrs = super().validate(attrs)
        validate_learner_self_registration_age(attrs.get("birth_date"))

        return attrs


class GuardianRegistrationSerializer(BaseRegistrationSerializer):
    """
    Сериализатор регистрации родителя.
    """


class MinorLearnerRegistrationSerializer(BaseRegistrationSerializer):
    """
    Сериализатор регистрации ребёнка младше 14 лет родителем.
    """

    organization_id = serializers.IntegerField(required=False, allow_null=True)
    department_id = serializers.IntegerField(required=False, allow_null=True)
    group_id = serializers.IntegerField(required=False, allow_null=True)
    curator_id = serializers.IntegerField(required=False, allow_null=True)
    relation_type = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        """
        Проверяет контакты, возраст ребёнка и право родителя.

        Args:
            attrs:
                Данные serializer.

        Returns:
            dict: Проверенные данные.
        """

        attrs = super().validate(attrs)
        validate_minor_learner_age(attrs.get("birth_date"))

        request = self.context.get("request")

        if request is not None:
            validate_guardian_can_create_minor_learner(request.user)

        return attrs
