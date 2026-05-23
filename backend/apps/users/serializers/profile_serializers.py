from __future__ import annotations

from apps.users.models import Profile
from apps.users.serializers.user_serializers import UserShortSerializer
from rest_framework import serializers


class ProfileSerializer(serializers.ModelSerializer):
    """
    Сериализатор базового профиля пользователя.
    """

    user = UserShortSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = [
            "id",
            "user",
            "gender",
            "avatar",
            "about",
            "city",
            "timezone",
            "preferred_contact_method",
            "show_email",
            "show_phone",
            "email_notifications",
            "push_notifications",
            "social_link_max",
            "social_link_vk",
            "avatar_moderation_status",
            "profile_moderation_status",
            "moderation_comment",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "user",
            "avatar_moderation_status",
            "profile_moderation_status",
            "moderation_comment",
            "created_at",
            "updated_at",
        ]


class ProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор обновления базового профиля.
    """

    class Meta:
        model = Profile
        fields = [
            "gender",
            "avatar",
            "about",
            "city",
            "timezone",
            "preferred_contact_method",
            "show_email",
            "show_phone",
            "email_notifications",
            "push_notifications",
            "social_link_max",
            "social_link_vk",
        ]


class AvatarModerationSerializer(serializers.Serializer):
    """
    Сериализатор модерации аватара.
    """

    is_approved = serializers.BooleanField()
    comment = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=1000,
    )
