from __future__ import annotations

from apps.users.models import GuardianLearner, GuardianProfile
from apps.users.serializers.user_serializers import UserShortSerializer
from rest_framework import serializers


class GuardianProfileSerializer(serializers.ModelSerializer):
    """
    Сериализатор профиля родителя или законного представителя.
    """

    user = UserShortSerializer(read_only=True)

    class Meta:
        model = GuardianProfile
        fields = [
            "id",
            "user",
            "status",
            "occupation",
            "work_place",
            "emergency_contact_phone",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "user",
            "status",
            "created_at",
            "updated_at",
        ]


class GuardianProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор обновления профиля родителя.
    """

    class Meta:
        model = GuardianProfile
        fields = [
            "occupation",
            "work_place",
            "emergency_contact_phone",
            "notes",
        ]


class GuardianLearnerSerializer(serializers.ModelSerializer):
    """
    Сериализатор связи родителя и учащегося.
    """

    guardian = UserShortSerializer(read_only=True)
    learner = UserShortSerializer(read_only=True)
    requested_by = UserShortSerializer(read_only=True)
    approved_by = UserShortSerializer(read_only=True)

    class Meta:
        model = GuardianLearner
        fields = [
            "id",
            "guardian",
            "learner",
            "relation_type",
            "status",
            "is_primary",
            "is_learner_consent_required",
            "curator_code_verified_at",
            "learner_code_verified_at",
            "requested_by",
            "approved_by",
            "approved_at",
            "comment",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "guardian",
            "learner",
            "status",
            "curator_code_verified_at",
            "learner_code_verified_at",
            "requested_by",
            "approved_by",
            "approved_at",
            "created_at",
            "updated_at",
        ]


class GuardianLearnerCreateSerializer(serializers.Serializer):
    """
    Сериализатор создания связи родителя и учащегося.
    """

    learner_id = serializers.IntegerField()
    relation_type = serializers.CharField(required=False, allow_blank=True)
    is_primary = serializers.BooleanField(default=False)
    curator_code = serializers.CharField(required=False, allow_blank=True)
    learner_code = serializers.CharField(required=False, allow_blank=True)
