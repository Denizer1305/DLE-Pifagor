from __future__ import annotations

from rest_framework import serializers


class TeacherDashboardProfileSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    full_name = serializers.CharField(allow_blank=True)
    email = serializers.EmailField()
    avatar_url = serializers.CharField(allow_blank=True)
    role_label = serializers.CharField(allow_blank=True)
    subject_label = serializers.CharField(allow_blank=True)


class TeacherDashboardStatSerializer(serializers.Serializer):
    key = serializers.CharField()
    label = serializers.CharField()
    value = serializers.JSONField()
    caption = serializers.CharField(allow_blank=True)
    icon = serializers.CharField()
    progress = serializers.IntegerField(required=False)
    tone = serializers.CharField(required=False, allow_blank=True)


class TeacherDashboardScheduleItemSerializer(serializers.Serializer):
    id = serializers.CharField()
    time = serializers.CharField()
    title = serializers.CharField()
    text = serializers.CharField(allow_blank=True)
    icon = serializers.CharField(required=False, allow_blank=True)


class TeacherDashboardCalendarDaySerializer(serializers.Serializer):
    date = serializers.DateField()
    day = serializers.IntegerField()
    date_label = serializers.CharField(required=False, allow_blank=True)
    is_today = serializers.BooleanField()
    is_selected = serializers.BooleanField()
    is_muted = serializers.BooleanField()
    is_weekend = serializers.BooleanField()
    title = serializers.CharField(allow_blank=True)
    text = serializers.CharField(allow_blank=True)
    event_types = serializers.ListField(
        child=serializers.CharField(),
    )


class TeacherDashboardCalendarSerializer(serializers.Serializer):
    month_label = serializers.CharField()
    selected_date = serializers.DateField()
    days = TeacherDashboardCalendarDaySerializer(many=True)


class TeacherDashboardCourseSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField(allow_blank=True)
    icon = serializers.CharField()
    status = serializers.CharField()
    status_label = serializers.CharField()
    modules_count = serializers.IntegerField()
    students_count = serializers.IntegerField()
    progress = serializers.IntegerField()


class TeacherDashboardAttentionItemSerializer(serializers.Serializer):
    id = serializers.CharField()
    icon = serializers.CharField()
    title = serializers.CharField()
    text = serializers.CharField(allow_blank=True)
    tone = serializers.CharField(required=False, allow_blank=True)


class TeacherDashboardActivityItemSerializer(serializers.Serializer):
    id = serializers.CharField()
    icon = serializers.CharField()
    title = serializers.CharField()
    text = serializers.CharField(allow_blank=True)
    tone = serializers.CharField(required=False, allow_blank=True)


class TeacherDashboardJournalRowSerializer(serializers.Serializer):
    id = serializers.CharField()
    student_name = serializers.CharField()
    work_title = serializers.CharField()
    grade = serializers.CharField(allow_blank=True)
    status = serializers.CharField()
    is_warning = serializers.BooleanField()


class TeacherDashboardNotificationSerializer(serializers.Serializer):
    id = serializers.CharField()
    icon = serializers.CharField()
    title = serializers.CharField()
    text = serializers.CharField(allow_blank=True)
    is_new = serializers.BooleanField()


class TeacherDashboardNoteSerializer(serializers.Serializer):
    id = serializers.CharField()
    date = serializers.CharField()
    title = serializers.CharField()
    text = serializers.CharField(allow_blank=True)


class TeacherDashboardSummarySerializer(serializers.Serializer):
    profile = TeacherDashboardProfileSerializer()
    stats = TeacherDashboardStatSerializer(many=True)
    schedule = TeacherDashboardScheduleItemSerializer(many=True)
    calendar = TeacherDashboardCalendarSerializer()
    courses = TeacherDashboardCourseSerializer(many=True)
    attention_items = TeacherDashboardAttentionItemSerializer(many=True)
    activity_items = TeacherDashboardActivityItemSerializer(many=True)
    journal_rows = TeacherDashboardJournalRowSerializer(many=True)
    notifications = TeacherDashboardNotificationSerializer(many=True)
    notes = TeacherDashboardNoteSerializer(many=True)
