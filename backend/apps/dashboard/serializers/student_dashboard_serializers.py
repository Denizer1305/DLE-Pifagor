from __future__ import annotations

from rest_framework import serializers


class StudentDashboardProfileSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    full_name = serializers.CharField(allow_blank=True)
    email = serializers.EmailField()
    avatar_url = serializers.CharField(allow_blank=True)
    role_label = serializers.CharField(allow_blank=True)
    group_label = serializers.CharField(allow_blank=True)


class StudentDashboardStatSerializer(serializers.Serializer):
    key = serializers.CharField()
    label = serializers.CharField()
    value = serializers.JSONField()
    caption = serializers.CharField(allow_blank=True)
    icon = serializers.CharField()
    progress = serializers.IntegerField(required=False)
    tone = serializers.CharField(required=False, allow_blank=True)


class StudentDashboardDayStatsSerializer(serializers.Serializer):
    lessons = serializers.IntegerField()
    assignments = serializers.IntegerField()
    notifications = serializers.IntegerField()


class StudentDashboardScheduleItemSerializer(serializers.Serializer):
    id = serializers.CharField()
    time = serializers.CharField()
    title = serializers.CharField()
    text = serializers.CharField(allow_blank=True)
    tone = serializers.CharField(required=False, allow_blank=True)


class StudentDashboardCalendarDaySerializer(serializers.Serializer):
    date = serializers.DateField()
    day = serializers.IntegerField()
    date_label = serializers.CharField(required=False, allow_blank=True)
    is_today = serializers.BooleanField()
    is_selected = serializers.BooleanField()
    is_muted = serializers.BooleanField()
    is_weekend = serializers.BooleanField()
    title = serializers.CharField(allow_blank=True)
    text = serializers.CharField(allow_blank=True)
    event_types = serializers.ListField(child=serializers.CharField())


class StudentDashboardCalendarSerializer(serializers.Serializer):
    month_label = serializers.CharField()
    selected_date = serializers.DateField()
    days = StudentDashboardCalendarDaySerializer(many=True)


class StudentDashboardCourseMetaSerializer(serializers.Serializer):
    value = serializers.JSONField()
    label = serializers.CharField()


class StudentDashboardCourseSerializer(serializers.Serializer):
    id = serializers.CharField()
    icon = serializers.CharField()
    status = serializers.CharField()
    status_variant = serializers.CharField(required=False, allow_blank=True)
    title = serializers.CharField()
    description = serializers.CharField(allow_blank=True)
    progress = serializers.IntegerField(required=False)
    meta = StudentDashboardCourseMetaSerializer(many=True)


class StudentDashboardListItemSerializer(serializers.Serializer):
    id = serializers.CharField()
    icon = serializers.CharField()
    title = serializers.CharField()
    text = serializers.CharField(allow_blank=True)
    meta = serializers.CharField(required=False, allow_blank=True)
    tone = serializers.CharField(required=False, allow_blank=True)


class StudentDashboardGradeRowSerializer(serializers.Serializer):
    id = serializers.CharField()
    subject = serializers.CharField()
    work = serializers.CharField()
    grade = serializers.CharField(allow_blank=True)
    status = serializers.CharField()
    warning = serializers.BooleanField(required=False)


class StudentDashboardNotificationSerializer(serializers.Serializer):
    id = serializers.CharField()
    icon = serializers.CharField()
    title = serializers.CharField()
    text = serializers.CharField(allow_blank=True)
    is_new = serializers.BooleanField(required=False)


class StudentDashboardNoteSerializer(serializers.Serializer):
    id = serializers.CharField()
    date = serializers.CharField()
    title = serializers.CharField()
    text = serializers.CharField(allow_blank=True)


class StudentDashboardSummarySerializer(serializers.Serializer):
    profile = StudentDashboardProfileSerializer()
    stats = StudentDashboardStatSerializer(many=True)
    day_stats = StudentDashboardDayStatsSerializer()
    schedule = StudentDashboardScheduleItemSerializer(many=True)
    calendar = StudentDashboardCalendarSerializer()
    courses = StudentDashboardCourseSerializer(many=True)
    assignments = StudentDashboardListItemSerializer(many=True)
    activity_items = StudentDashboardListItemSerializer(many=True)
    grade_rows = StudentDashboardGradeRowSerializer(many=True)
    goals = StudentDashboardListItemSerializer(many=True)
    notifications = StudentDashboardNotificationSerializer(many=True)
    notes = StudentDashboardNoteSerializer(many=True)
