from __future__ import annotations

COURSE_GROUP_ACCESS_MUTABLE_FIELDS = {
    "course",
    "course_id",
    "group",
    "group_id",
    "group_subject",
    "group_subject_id",
    "teacher_group_subject",
    "teacher_group_subject_id",
    "visibility",
    "starts_at",
    "ends_at",
    "auto_enroll",
    "is_active",
    "notes",
}

COURSE_ACCESS_RULE_MUTABLE_FIELDS = {
    "course",
    "course_id",
    "access_type",
    "learner",
    "learner_id",
    "organization",
    "organization_id",
    "access_code",
    "starts_at",
    "ends_at",
    "auto_enroll",
    "is_active",
    "notes",
}

COURSE_ENROLLMENT_MUTABLE_FIELDS = {
    "course",
    "course_id",
    "learner",
    "learner_id",
    "group_access",
    "group_access_id",
    "access_rule",
    "access_rule_id",
    "status",
    "enrolled_at",
    "started_at",
    "completed_at",
    "last_activity_at",
    "progress_percent",
}
