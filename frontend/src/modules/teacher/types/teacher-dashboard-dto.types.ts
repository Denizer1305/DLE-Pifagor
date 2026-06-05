import type {
    TeacherCourseStatus,
    TeacherDashboardTone,
} from "@/modules/teacher/types/teacher-dashboard-common.types";

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
