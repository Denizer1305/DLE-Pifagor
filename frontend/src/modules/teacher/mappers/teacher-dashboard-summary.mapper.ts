import type { DashboardCalendarDay } from "@/components/dashboard/types/dashboard.types";
import type {
    TeacherDashboardActivityItem,
    TeacherDashboardActivityItemDto,
    TeacherDashboardAttentionItem,
    TeacherDashboardAttentionItemDto,
    TeacherDashboardCalendarDayDto,
    TeacherDashboardCourse,
    TeacherDashboardCourseDto,
    TeacherDashboardJournalRow,
    TeacherDashboardJournalRowDto,
    TeacherDashboardProfile,
    TeacherDashboardProfileDto,
    TeacherDashboardScheduleItem,
    TeacherDashboardScheduleItemDto,
    TeacherDashboardStat,
    TeacherDashboardStatDto,
    TeacherDashboardSummary,
    TeacherDashboardSummaryDto,
} from "@/modules/teacher/types/teacher-dashboard.types";
import { resolveBackendAssetUrl } from "@/utils/backend-asset-url.utils";

export function mapTeacherDashboardSummary(
    dto: TeacherDashboardSummaryDto,
): TeacherDashboardSummary {
    return {
        profile: mapProfile(dto.profile),
        stats: dto.stats.map(mapStat),
        schedule: dto.schedule.map(mapScheduleItem),
        calendar: {
            monthLabel: dto.calendar.month_label,
            selectedDate: dto.calendar.selected_date,
            days: dto.calendar.days.map(mapCalendarDay),
        },
        courses: dto.courses.map(mapCourse),
        attentionItems: dto.attention_items.map(mapAttentionItem),
        activityItems: dto.activity_items.map(mapActivityItem),
        journalRows: dto.journal_rows.map(mapJournalRow),
        notifications: dto.notifications,
        notes: dto.notes,
    };
}

function mapProfile(dto: TeacherDashboardProfileDto): TeacherDashboardProfile {
    return {
        id: dto.id,
        fullName: dto.full_name,
        email: dto.email,
        avatarUrl: resolveBackendAssetUrl(dto.avatar_url),
        roleLabel: dto.role_label,
        subjectLabel: dto.subject_label,
    };
}

function mapStat(dto: TeacherDashboardStatDto): TeacherDashboardStat {
    return {
        key: dto.key,
        label: dto.label,
        value: dto.value,
        caption: dto.caption,
        icon: dto.icon,
        progress: dto.progress,
        tone: dto.tone || "primary",
    };
}

function mapScheduleItem(dto: TeacherDashboardScheduleItemDto): TeacherDashboardScheduleItem {
    return {
        id: dto.id,
        time: dto.time,
        title: dto.title,
        text: dto.text,
        icon: dto.icon || "fas fa-calendar-check",
    };
}

function mapCalendarDay(dto: TeacherDashboardCalendarDayDto): DashboardCalendarDay {
    return {
        date: dto.date,
        day: dto.day,
        dateLabel: dto.date_label || formatCalendarDateLabel(dto.date),
        isToday: dto.is_today,
        isSelected: dto.is_selected,
        isMuted: dto.is_muted,
        isWeekend: dto.is_weekend,
        title: dto.title,
        text: dto.text,
        events: dto.event_types.map((type) => {
            return {
                type: normalizeCalendarEventType(type),
            };
        }),
    };
}

function mapCourse(dto: TeacherDashboardCourseDto): TeacherDashboardCourse {
    return {
        id: dto.id,
        title: dto.title,
        description: dto.description,
        icon: dto.icon,
        status: dto.status,
        statusLabel: dto.status_label,
        modulesCount: dto.modules_count,
        studentsCount: dto.students_count,
        progress: dto.progress,
    };
}

function mapAttentionItem(dto: TeacherDashboardAttentionItemDto): TeacherDashboardAttentionItem {
    return {
        id: dto.id,
        icon: dto.icon,
        title: dto.title,
        text: dto.text,
        tone: dto.tone || "warning",
    };
}

function mapActivityItem(dto: TeacherDashboardActivityItemDto): TeacherDashboardActivityItem {
    return {
        id: dto.id,
        icon: dto.icon,
        title: dto.title,
        text: dto.text,
        tone: dto.tone || "primary",
    };
}

function mapJournalRow(dto: TeacherDashboardJournalRowDto): TeacherDashboardJournalRow {
    return {
        id: dto.id,
        studentName: dto.student_name,
        workTitle: dto.work_title,
        grade: dto.grade,
        status: dto.status,
        isWarning: dto.is_warning,
    };
}

function normalizeCalendarEventType(type: string) {
    if (type === "lesson" || type === "checking" || type === "deadline") {
        return type;
    }

    return "neutral";
}

function formatCalendarDateLabel(value: string): string {
    const date = parseDateKey(value);

    if (!date) {
        return "";
    }

    return new Intl.DateTimeFormat("ru-RU", {
        day: "numeric",
        month: "long",
    }).format(date);
}

function parseDateKey(value: string): Date | null {
    if (!value) {
        return null;
    }

    const [year, month, day] = value.split("-").map(Number);

    if (!year || !month || !day) {
        return null;
    }

    return new Date(year, month - 1, day);
}
