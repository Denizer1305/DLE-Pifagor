from __future__ import annotations

from rest_framework import serializers


class AdminDashboardProfileSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    full_name = serializers.CharField()
    email = serializers.EmailField()
    avatar_url = serializers.CharField(allow_blank=True)
    role_label = serializers.CharField()


class AdminDashboardStatSerializer(serializers.Serializer):
    key = serializers.CharField()
    label = serializers.CharField()
    value = serializers.IntegerField()
    caption = serializers.CharField()
    icon = serializers.CharField()
    tone = serializers.CharField()


class AdminDashboardCalendarDaySerializer(serializers.Serializer):
    date = serializers.DateField()
    day = serializers.IntegerField()
    is_today = serializers.BooleanField()
    is_selected = serializers.BooleanField()
    is_muted = serializers.BooleanField()
    is_weekend = serializers.BooleanField()
    title = serializers.CharField()
    text = serializers.CharField()


class AdminDashboardCalendarSerializer(serializers.Serializer):
    month_label = serializers.CharField()
    selected_date = serializers.DateField()
    days = AdminDashboardCalendarDaySerializer(many=True)


class AdminDashboardUserShortSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    full_name = serializers.CharField()
    email = serializers.EmailField()
    status = serializers.CharField()
    created_at = serializers.DateTimeField()


class AdminDashboardOrganizationShortSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class AdminDashboardDepartmentShortSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class AdminDashboardGroupShortSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class AdminDashboardJoinRequestSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    request_type = serializers.CharField()
    status = serializers.CharField()
    user = AdminDashboardUserShortSerializer()
    organization = AdminDashboardOrganizationShortSerializer(
        allow_null=True,
        required=False,
    )
    department = AdminDashboardDepartmentShortSerializer(
        allow_null=True,
        required=False,
    )
    group = AdminDashboardGroupShortSerializer(
        allow_null=True,
        required=False,
    )
    message = serializers.CharField(allow_blank=True)
    created_at = serializers.DateTimeField()


class AdminDashboardFeedbackRequestSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    full_name = serializers.CharField()
    email = serializers.EmailField()
    topic = serializers.CharField()
    status = serializers.CharField()
    message = serializers.CharField()
    created_at = serializers.DateTimeField()


class AdminDashboardAuditActorSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    full_name = serializers.CharField(allow_blank=True)
    email = serializers.EmailField(allow_blank=True)


class AdminDashboardAuditEventSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    message = serializers.CharField(allow_blank=True)
    actor = AdminDashboardAuditActorSerializer(
        allow_null=True,
        required=False,
    )
    target_user = AdminDashboardAuditActorSerializer(
        allow_null=True,
        required=False,
    )
    created_at = serializers.DateTimeField()


class AdminDashboardSystemCheckSerializer(serializers.Serializer):
    key = serializers.CharField()
    label = serializers.CharField()
    status = serializers.CharField()
    text = serializers.CharField()
    icon = serializers.CharField()


class AdminDashboardSystemHealthSerializer(serializers.Serializer):
    status = serializers.CharField()
    checks = AdminDashboardSystemCheckSerializer(many=True)


class AdminDashboardQuickActionSerializer(serializers.Serializer):
    key = serializers.CharField()
    label = serializers.CharField()
    description = serializers.CharField()
    icon = serializers.CharField()
    route_name = serializers.CharField()
    tone = serializers.CharField()


class AdminDashboardSummarySerializer(serializers.Serializer):
    profile = AdminDashboardProfileSerializer()
    stats = AdminDashboardStatSerializer(many=True)
    calendar = AdminDashboardCalendarSerializer()
    recent_users = AdminDashboardUserShortSerializer(many=True)
    join_requests = AdminDashboardJoinRequestSerializer(many=True)
    feedback_requests = AdminDashboardFeedbackRequestSerializer(many=True)
    audit_events = AdminDashboardAuditEventSerializer(many=True)
    system_health = AdminDashboardSystemHealthSerializer()
    quick_actions = AdminDashboardQuickActionSerializer(many=True)
