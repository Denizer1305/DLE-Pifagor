import type {
    DashboardCalendarContent,
    DashboardCalendarDay,
    DashboardCreateItemModalContent,
    DashboardCourseCardContent,
    DashboardDayCardContent,
    DashboardHeroContent,
    DashboardHeroSectionContent,
    DashboardListItem,
    DashboardMiniPlanItem,
    DashboardNotesContent,
    DashboardNotificationsContent,
    DashboardProfilePanelContent,
    DashboardShellConfig,
    DashboardStatsCardContent,
    DashboardTimelineItem,
} from "@/components/dashboard/types/dashboard.types";

export interface StudentDashboardModel {
    shell: DashboardShellConfig;

    hero: StudentDashboardHeroContent;
    dayCard: DashboardDayCardContent;
    miniPlan: DashboardMiniPlanItem[];
    heroSection: DashboardHeroSectionContent;

    calendarContent: DashboardCalendarContent;
    calendarDays: DashboardCalendarDay[];
    notifications: DashboardNotificationsContent;
    notes: DashboardNotesContent;
    profilePanel: DashboardProfilePanelContent;
    createModal: DashboardCreateItemModalContent;

    stats: DashboardStatsCardContent[];

    scheduleSection: StudentDashboardSectionContent;
    schedule: DashboardTimelineItem[];

    assignmentsSection: StudentDashboardSectionContent;
    assignments: DashboardListItem[];

    coursesSection: StudentDashboardSectionContent;
    courses: DashboardCourseCardContent[];

    activitySection: StudentDashboardSectionContent;
    activityItems: DashboardListItem[];

    gradesSection: StudentDashboardSectionContent;
    gradeRows: StudentGradeRow[];

    goalsSection: StudentDashboardSectionContent;
    goals: DashboardListItem[];
}

export type StudentDashboardHeroContent = DashboardHeroContent;

export interface StudentDashboardSectionContent {
    badge: string;
    icon: string;
    title: string;
    text: string;
    emptyIcon: string;
    emptyText: string;
}

export interface StudentGradeRow {
    id: string | number;
    subject: string;
    work: string;
    grade: string;
    status: string;
    warning?: boolean;
}

export interface StudentDashboardProfile {
    id: number;
    fullName: string;
    email: string;
    avatarUrl: string;
    roleLabel: string;
    groupLabel: string;
}

export interface StudentDashboardCalendar {
    monthLabel: string;
    selectedDate: string;
    days: DashboardCalendarDay[];
}

export interface StudentDashboardDayStats {
    lessons: number;
    assignments: number;
    notifications: number;
}

export interface StudentDashboardSummary {
    profile: StudentDashboardProfile;
    stats: DashboardStatsCardContent[];
    dayStats: StudentDashboardDayStats;
    schedule: DashboardTimelineItem[];
    calendar: StudentDashboardCalendar;
    courses: DashboardCourseCardContent[];
    assignments: DashboardListItem[];
    activityItems: DashboardListItem[];
    gradeRows: StudentGradeRow[];
    goals: DashboardListItem[];
    notifications: DashboardNotificationsContent["items"];
    notes: DashboardNotesContent["items"];
}

export interface StudentDashboardProfileDto {
    id: number;
    full_name: string;
    email: string;
    avatar_url: string;
    role_label: string;
    group_label: string;
}

export interface StudentDashboardStatDto {
    key: string;
    label: string;
    value: string | number;
    caption: string;
    icon: string;
    progress?: number;
    tone?: string;
}

export interface StudentDashboardDayStatsDto {
    lessons: number;
    assignments: number;
    notifications: number;
}

export interface StudentDashboardScheduleItemDto {
    id: string | number;
    time: string;
    title: string;
    text: string;
    tone?: string;
}

export interface StudentDashboardCalendarDayDto {
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

export interface StudentDashboardCalendarDto {
    month_label: string;
    selected_date: string;
    days: StudentDashboardCalendarDayDto[];
}

export interface StudentDashboardCourseDto {
    id: string | number;
    icon: string;
    status: string;
    status_variant?: "active" | "draft" | "warning";
    title: string;
    description: string;
    progress?: number;
    meta: {
        value: string | number;
        label: string;
    }[];
}

export interface StudentDashboardListItemDto {
    id: string | number;
    icon: string;
    title: string;
    text: string;
    meta?: string;
    tone?: string;
}

export interface StudentGradeRowDto {
    id: string | number;
    subject: string;
    work: string;
    grade: string;
    status: string;
    warning?: boolean;
}

export interface StudentDashboardNotificationDto {
    id: string | number;
    icon: string;
    title: string;
    text: string;
    is_new?: boolean;
}

export interface StudentDashboardNoteDto {
    id: string | number;
    date: string;
    title: string;
    text: string;
}

export interface StudentDashboardSummaryDto {
    profile: StudentDashboardProfileDto;
    stats: StudentDashboardStatDto[];
    day_stats: StudentDashboardDayStatsDto;
    schedule: StudentDashboardScheduleItemDto[];
    calendar: StudentDashboardCalendarDto;
    courses: StudentDashboardCourseDto[];
    assignments: StudentDashboardListItemDto[];
    activity_items: StudentDashboardListItemDto[];
    grade_rows: StudentGradeRowDto[];
    goals: StudentDashboardListItemDto[];
    notifications: StudentDashboardNotificationDto[];
    notes: StudentDashboardNoteDto[];
}
