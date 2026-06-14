from __future__ import annotations

from apps.backoffice.selectors.users import (
    get_recent_backoffice_user_audit_logs_for_target,
)
from apps.backoffice.serializers.users.audit import BackofficeUserAuditLogListSerializer
from apps.backoffice.serializers.users.related import BackofficeUserRoleSerializer
from apps.users.models import User
from apps.users.serializers.profile_serializers import ProfileSerializer
from apps.users.serializers.user_serializers import UserShortSerializer
from rest_framework import serializers


class BackofficeUserDetailSerializer(serializers.ModelSerializer):
    """
    Детальная read-карточка пользователя для backoffice.
    """

    full_name = serializers.CharField(
        source="get_full_name",
        read_only=True,
    )
    account_managed_by = UserShortSerializer(read_only=True)
    profile = ProfileSerializer(read_only=True)
    user_roles = BackofficeUserRoleSerializer(many=True, read_only=True)
    audit_logs = serializers.SerializerMethodField()

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
            "profile",
            "user_roles",
            "audit_logs",
        ]
        read_only_fields = fields

    def get_audit_logs(self, obj) -> list[dict]:
        """
        Возвращает последние записи аудита пользователя.
        """

        audit_logs = get_recent_backoffice_user_audit_logs_for_target(
            target_user=obj,
        )

        return BackofficeUserAuditLogListSerializer(
            audit_logs,
            many=True,
            context=self.context,
        ).data
