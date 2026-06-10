export interface ParentDashboardProfileDto {
    id: number;
    full_name: string;
    email: string;
    avatar_url: string;
    role_label: string;
}

export interface ParentDashboardStatDto {
    key: string;
    label: string;
    value: string | number;
    caption: string;
    icon: string;
    progress?: number;
    tone?: string;
}

export interface ParentDashboardDayStatsDto {
    lessons: number;
    assignments: number;
    messages: number;
}

export interface ParentDashboardCalendarDayDto {
    date: string;
    day: number;
    date_label?: string;
    is_today: boolean;
    is_selected: boolean;
    is_muted: boolean;
    is_weekend: boolean;
    title: string;
    text: string;
    event_types: string[];
}

export interface ParentDashboardSummaryDto {
    profile: ParentDashboardProfileDto;
    stats: ParentDashboardStatDto[];
    day_stats: ParentDashboardDayStatsDto;
    schedule: {
        id: string | number;
        time: string;
        title: string;
        text: string;
        tone?: string;
    }[];
    calendar: {
        month_label: string;
        selected_date: string;
        days: ParentDashboardCalendarDayDto[];
    };
    courses: {
        id: string | number;
        icon: string;
        status: string;
        status_variant?: "active" | "draft" | "warning";
        title: string;
        description: string;
        progress?: number;
        meta: { value: string | number; label: string }[];
    }[];
    important_items: ParentDashboardListItemDto[];
    activity_items: ParentDashboardListItemDto[];
    grade_rows: {
        id: string | number;
        subject: string;
        work: string;
        grade: string;
        status: string;
        warning?: boolean;
    }[];
    messages: ParentDashboardListItemDto[];
    notifications: {
        id: string | number;
        icon: string;
        title: string;
        text: string;
        is_new?: boolean;
    }[];
    notes: { id: string | number; date: string; title: string; text: string }[];
}

export interface ParentDashboardListItemDto {
    id: string | number;
    icon: string;
    title: string;
    text: string;
    meta?: string;
    tone?: string;
}
