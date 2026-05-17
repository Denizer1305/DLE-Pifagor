from __future__ import annotations

from apps.users.models import LearnerProfile
from apps.users.serializers.user_serializers import UserShortSerializer
from rest_framework import serializers


class LearnerProfileSerializer(serializers.ModelSerializer):
    """
    Сериализатор профиля учащегося.
    """

    user = UserShortSerializer(read_only=True)
    curator = UserShortSerializer(read_only=True)
    created_by_guardian = UserShortSerializer(read_only=True)
    verified_by = UserShortSerializer(read_only=True)

    class Meta:
        model = LearnerProfile
        fields = [
            "id",
            "user",
            "organization",
            "department",
            "group",
            "curator",
            "learner_code",
            "admission_year",
            "admission_date",
            "graduation_date",
            "status",
            "is_minor",
            "created_by_guardian",
            "notes",
            "verification_comment",
            "verified_by",
            "verified_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "user",
            "status",
            "is_minor",
            "created_by_guardian",
            "verification_comment",
            "verified_by",
            "verified_at",
            "created_at",
            "updated_at",
        ]


class LearnerProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор обновления профиля учащегося.
    """

    class Meta:
        model = LearnerProfile
        fields = [
            "organization",
            "department",
            "group",
            "curator",
            "learner_code",
            "admission_year",
            "admission_date",
            "graduation_date",
            "notes",
        ]


class SubmitLearnerGroupRequestSerializer(serializers.Serializer):
    """
    Сериализатор отправки заявки учащегося в группу.
    """

    organization_id = serializers.IntegerField()
    department_id = serializers.IntegerField(required=False, allow_null=True)
    group_id = serializers.IntegerField(required=False, allow_null=True)
    curator_id = serializers.IntegerField(required=False, allow_null=True)
