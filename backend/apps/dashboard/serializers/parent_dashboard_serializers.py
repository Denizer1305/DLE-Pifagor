from __future__ import annotations

from apps.dashboard.serializers.student_dashboard_serializers import (
    StudentDashboardCalendarSerializer,
    StudentDashboardCourseSerializer,
    StudentDashboardGradeRowSerializer,
    StudentDashboardListItemSerializer,
    StudentDashboardNoteSerializer,
    StudentDashboardNotificationSerializer,
    StudentDashboardScheduleItemSerializer,
)
from rest_framework import serializers


class ParentDashboardProfileSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    full_name = serializers.CharField(allow_blank=True)
    email = serializers.EmailField()
    avatar_url = serializers.CharField(allow_blank=True)
    role_label = serializers.CharField(allow_blank=True)


class ParentDashboardStatSerializer(serializers.Serializer):
    key = serializers.CharField()
    label = serializers.CharField()
    value = serializers.JSONField()
    caption = serializers.CharField(allow_blank=True)
    icon = serializers.CharField()
    progress = serializers.IntegerField(required=False)
    tone = serializers.CharField(required=False, allow_blank=True)


class ParentDashboardDayStatsSerializer(serializers.Serializer):
    lessons = serializers.IntegerField()
    assignments = serializers.IntegerField()
    messages = serializers.IntegerField()


class ParentDashboardSummarySerializer(serializers.Serializer):
    profile = ParentDashboardProfileSerializer()
    stats = ParentDashboardStatSerializer(many=True)
    day_stats = ParentDashboardDayStatsSerializer()
    schedule = StudentDashboardScheduleItemSerializer(many=True)
    calendar = StudentDashboardCalendarSerializer()
    courses = StudentDashboardCourseSerializer(many=True)
    important_items = StudentDashboardListItemSerializer(many=True)
    activity_items = StudentDashboardListItemSerializer(many=True)
    grade_rows = StudentDashboardGradeRowSerializer(many=True)
    messages = StudentDashboardListItemSerializer(many=True)
    notifications = StudentDashboardNotificationSerializer(many=True)
    notes = StudentDashboardNoteSerializer(many=True)
