export type NotificationLevel = "info" | "success" | "warning" | "danger";

export type NotificationStatus = "unread" | "read" | "completed" | "archived";

export type NotificationCategory =
    | "daily_summary"
    | "assignments"
    | "tests"
    | "schedule"
    | "calendar"
    | "notes"
    | "birthday"
    | "education"
    | "feedback"
    | "moderation"
    | "security"
    | "system";

export type NotificationType =
    | "daily_summary"
    | "birthday"
    | "assignment_due_today"
    | "assignment_due_tomorrow"
    | "assignment_due_soon"
    | "assignment_overdue"
    | "test_today"
    | "test_tomorrow"
    | "exam_today"
    | "exam_tomorrow"
    | "calendar_event_today"
    | "note_reminder"
    | "schedule_changed"
    | "work_to_check"
    | "moderation_request"
    | "support_request"
    | "security"
    | "system";

export type NotificationSourceType =
    | "user"
    | "assignment"
    | "test"
    | "exam"
    | "lesson"
    | "course"
    | "schedule"
    | "calendar_event"
    | "note"
    | "support_request"
    | "moderation_request"
    | "security_event"
    | "system";

export type NotificationBootstrapReason =
    | "dashboard_login"
    | "manual_sync"
    | "celery_fallback";

export interface NotificationDto {
    id: number;
    title: string;
    message: string;
    notification_type: NotificationType;
    category: NotificationCategory;
    level: NotificationLevel;
    status: NotificationStatus;
    recipient_role: string;
    source_type: NotificationSourceType;
    source_id: string;
    action_label: string;
    action_url: string;
    has_action: boolean;
    is_unread: boolean;
    event_at: string | null;
    read_at: string | null;
    completed_at: string | null;
    expires_at: string | null;
    created_at: string;
}

export interface NotificationDetailDto extends NotificationDto {
    recipient: {
        id: number;
        email: string;
        full_name: string;
    };
    deduplication_key: string;
    delivery_channels: string[];
    delivery_statuses: Record<string, string>;
    payload: Record<string, unknown>;
    updated_at: string;
    is_read: boolean;
    is_completed: boolean;
    is_archived: boolean;
    is_expired: boolean;
}

export interface NotificationFeedDto {
    unread_count: number;
    items: NotificationDto[];
}

export interface NotificationUnreadCountDto {
    unread_count: number;
}

export interface NotificationBootstrapPayload {
    reason?: NotificationBootstrapReason;
    target_date?: string | null;
}

export interface NotificationBootstrapResponseDto {
    target_date: string;
    created_count: number;
    created_ids: number[];
    unread_count: number;
}

export interface NotificationActionResponseDto {
    detail: string;
    notification: NotificationDetailDto;
}

export interface NotificationBulkActionResponseDto {
    detail: string;
    updated_count: number;
    unread_count: number;
}

export interface NotificationDeleteResponseDto {
    detail: string;
}

export interface NotificationQueryParams {
    status?: NotificationStatus | "";
    level?: NotificationLevel | "";
    category?: NotificationCategory | "";
    notification_type?: NotificationType | "";
    source_type?: NotificationSourceType | "";
    source_id?: string;
    unread_only?: boolean;
}

export interface NotificationViewModel {
    id: number;
    title: string;
    message: string;
    type: NotificationType;
    category: NotificationCategory;
    categoryLabel: string;
    level: NotificationLevel;
    levelLabel: string;
    levelIcon: string;
    status: NotificationStatus;
    statusLabel: string;
    isUnread: boolean;
    hasAction: boolean;
    actionLabel: string;
    actionUrl: string;
    createdAt: string;
    createdAtLabel: string;
    eventAt: string | null;
    eventAtLabel: string;
}

export interface NotificationFeedViewModel {
    unreadCount: number;
    items: NotificationViewModel[];
}

export interface NotificationFilterOption {
    value: string;
    label: string;
    icon?: string;
}

export interface NotificationRealtimeMessage {
    type:
        | "notification.created"
        | "notification.read"
        | "notification.deleted"
        | "notification.count_changed";
    notification?: NotificationDto;
    notification_id?: number;
    unread_count?: number;
}