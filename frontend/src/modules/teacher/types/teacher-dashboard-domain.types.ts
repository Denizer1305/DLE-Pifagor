import type { DashboardCalendarDay } from "@/components/dashboard/types/dashboard.types";
import type {
    TeacherCourseStatus,
    TeacherDashboardTone,
} from "@/modules/teacher/types/teacher-dashboard-common.types";
import type {
    TeacherDashboardNoteDto,
    TeacherDashboardNotificationDto,
} from "@/modules/teacher/types/teacher-dashboard-dto.types";

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
