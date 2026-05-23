import type {
    DashboardAiCardContent,
    DashboardCalendarContent,
    DashboardCalendarDay,
    DashboardCreateItemModalContent,
    DashboardDayCardContent,
    DashboardHeroContent,
    DashboardHeroSectionContent,
    DashboardMiniPlanItem,
    DashboardNotesContent,
    DashboardNotificationsContent,
    DashboardProfilePanelContent,
    DashboardShellConfig,
} from "@/components/dashboard/types/dashboard.types";

export type TeacherDashboardTone =
    | "primary"
    | "success"
    | "warning"
    | "danger"
    | "neutral";

export type TeacherCourseStatus =
    | "active"
    | "draft"
    | "archived";

export interface TeacherDashboardProfileDto {
    id: number;
    full_name: string;
    email: string;
    avatar_url: string;
    role_label: string;
    subject_label: string;
}

export interface TeacherDashboardStatDto {
    key: string;
    label: string;
    value: string | number;
    caption: string;
    icon: string;
    progress?: number;
    tone?: TeacherDashboardTone;
}

export interface TeacherDashboardScheduleItemDto {
    id: number | string;
    time: string;
    title: string;
    text: string;
    icon?: string;
}

export interface TeacherDashboardCalendarDayDto {
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

export interface TeacherDashboardCalendarDto {
    month_label: string;
    selected_date: string;
    days: TeacherDashboardCalendarDayDto[];
}

export interface TeacherDashboardCourseDto {
    id: number | string;
    title: string;
    description: string;
    icon: string;
    status: TeacherCourseStatus;
    status_label: string;
    modules_count: number;
    students_count: number;
    progress: number;
}

export interface TeacherDashboardAttentionItemDto {
    id: number | string;
    icon: string;
    title: string;
    text: string;
    tone?: TeacherDashboardTone;
}

export interface TeacherDashboardActivityItemDto {
    id: number | string;
    icon: string;
    title: string;
    text: string;
    tone?: TeacherDashboardTone;
}

export interface TeacherDashboardJournalRowDto {
    id: number | string;
    student_name: string;
    work_title: string;
    grade: string;
    status: string;
    is_warning: boolean;
}

export interface TeacherDashboardNotificationDto {
    id: number | string;
    icon: string;
    title: string;
    text: string;
    is_new: boolean;
}

export interface TeacherDashboardNoteDto {
    id: number | string;
    date: string;
    title: string;
    text: string;
}

export interface TeacherDashboardSummaryDto {
    profile: TeacherDashboardProfileDto;
    stats: TeacherDashboardStatDto[];
    schedule: TeacherDashboardScheduleItemDto[];
    calendar: TeacherDashboardCalendarDto;
    courses: TeacherDashboardCourseDto[];
    attention_items: TeacherDashboardAttentionItemDto[];
    activity_items: TeacherDashboardActivityItemDto[];
    journal_rows: TeacherDashboardJournalRowDto[];
    notifications: TeacherDashboardNotificationDto[];
    notes: TeacherDashboardNoteDto[];
}

export interface TeacherDashboardProfile {
    id: number;
    fullName: string;
    email: string;
    avatarUrl: string;
    roleLabel: string;
    subjectLabel: string;
}

export interface TeacherDashboardStat {
    key: string;
    label: string;
    value: string | number;
    caption: string;
    icon: string;
    progress?: number;
    tone?: TeacherDashboardTone;
}

export interface TeacherDashboardScheduleItem {
    id: number | string;
    time: string;
    title: string;
    text: string;
    icon: string;
}

export interface TeacherDashboardCourse {
    id: number | string;
    title: string;
    description: string;
    icon: string;
    status: TeacherCourseStatus;
    statusLabel: string;
    modulesCount: number;
    studentsCount: number;
    progress: number;
}

export interface TeacherDashboardAttentionItem {
    id: number | string;
    icon: string;
    title: string;
    text: string;
    tone: TeacherDashboardTone;
}

export interface TeacherDashboardActivityItem {
    id: number | string;
    icon: string;
    title: string;
    text: string;
    tone: TeacherDashboardTone;
}

export interface TeacherDashboardJournalRow {
    id: number | string;
    studentName: string;
    workTitle: string;
    grade: string;
    status: string;
    isWarning: boolean;
}

export interface TeacherDashboardSummary {
    profile: TeacherDashboardProfile;
    stats: TeacherDashboardStat[];
    schedule: TeacherDashboardScheduleItem[];
    calendar: {
        monthLabel: string;
        selectedDate: string;
        days: DashboardCalendarDay[];
    };
    courses: TeacherDashboardCourse[];
    attentionItems: TeacherDashboardAttentionItem[];
    activityItems: TeacherDashboardActivityItem[];
    journalRows: TeacherDashboardJournalRow[];
    notifications: TeacherDashboardNotificationDto[];
    notes: TeacherDashboardNoteDto[];
}

export type TeacherDashboardHeroActionModel = DashboardHeroContent["actions"][number];

export type TeacherDashboardHeroModel = DashboardHeroContent;

export interface TeacherDashboardFeaturedStatModel {
    icon: string;
    title: string;
    value: string | number;
    label: string;
    progress: number;
}

export interface TeacherDashboardCompactStatModel {
    key: string;
    icon: string;
    title: string;
    value: string | number;
    text: string;
}

export type TeacherDashboardTimelineItemModel = DashboardMiniPlanItem;

export interface TeacherDashboardCourseCardModel {
    id: number | string;
    icon: string;
    title: string;
    description: string;
    status: string;
    statusVariant: "active" | "draft" | "warning";
    modulesCount: number;
    studentsCount: number;
    progress: number;
}

export interface TeacherDashboardJournalRowModel {
    id: number | string;
    student: string;
    work: string;
    grade: string;
    status: string;
    warning: boolean;
}

export interface TeacherDashboardPageModel {
    hero: TeacherDashboardHeroModel;
    dayCard: DashboardDayCardContent;
    miniPlan: TeacherDashboardTimelineItemModel[];
    heroSection: DashboardHeroSectionContent;

    featuredStat: TeacherDashboardFeaturedStatModel;
    compactStats: TeacherDashboardCompactStatModel[];

    planItems: TeacherDashboardTimelineItemModel[];
    attentionItems: TeacherDashboardAttentionItem[];
    courses: TeacherDashboardCourseCardModel[];
    activityItems: TeacherDashboardActivityItem[];
    journalRows: TeacherDashboardJournalRowModel[];
    ai: DashboardAiCardContent;
}

export interface TeacherDashboardViewModel {
    shell: DashboardShellConfig;
    calendarContent: DashboardCalendarContent;
    calendarDays: DashboardCalendarDay[];
    notifications: DashboardNotificationsContent;
    notes: DashboardNotesContent;
    profilePanel: DashboardProfilePanelContent;
    createModal: DashboardCreateItemModalContent;
}
