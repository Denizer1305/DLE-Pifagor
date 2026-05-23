import type {
    DashboardCalendarDay,
    DashboardCalendarEventType,
    DashboardTone,
} from "@/components/dashboard/types/dashboard.types";
import type {
    StudentDashboardListItemDto,
    StudentDashboardSummary,
    StudentDashboardSummaryDto,
} from "@/modules/student/types/student-dashboard.types";
import { resolveBackendAssetUrl } from "@/utils/backend-asset-url.utils";

export function mapStudentDashboardSummary(
    dto: StudentDashboardSummaryDto,
): StudentDashboardSummary {
    return {
        profile: {
            id: dto.profile.id,
            fullName: dto.profile.full_name,
            email: dto.profile.email,
            avatarUrl: resolveBackendAssetUrl(dto.profile.avatar_url),
            roleLabel: dto.profile.role_label,
            groupLabel: dto.profile.group_label,
        },
        stats: dto.stats.map((stat) => {
            return {
                key: stat.key,
                title: stat.label,
                value: stat.value,
                text: stat.caption,
                icon: stat.icon,
                progress: stat.progress ?? 0,
                tone: normalizeTone(stat.tone),
            };
        }),
        dayStats: {
            lessons: dto.day_stats.lessons,
            assignments: dto.day_stats.assignments,
            notifications: dto.day_stats.notifications,
        },
        schedule: dto.schedule.map((item) => {
            return {
                id: item.id,
                time: item.time,
                title: item.title,
                text: item.text,
                tone: normalizeTone(item.tone),
            };
        }),
        calendar: {
            monthLabel: dto.calendar.month_label,
            selectedDate: dto.calendar.selected_date,
            days: dto.calendar.days.map(mapCalendarDay),
        },
        courses: dto.courses.map((course) => {
            return {
                id: course.id,
                icon: course.icon,
                status: course.status,
                statusVariant: course.status_variant,
                title: course.title,
                description: course.description,
                progress: course.progress ?? 0,
                meta: course.meta,
            };
        }),
        assignments: dto.assignments.map(mapListItem),
        activityItems: dto.activity_items.map(mapListItem),
        gradeRows: dto.grade_rows.map((row) => {
            return {
                id: row.id,
                subject: row.subject,
                work: row.work,
                grade: row.grade,
                status: row.status,
                warning: row.warning,
            };
        }),
        goals: dto.goals.map(mapListItem),
        notifications: dto.notifications.map((notification) => {
            return {
                id: notification.id,
                icon: notification.icon,
                title: notification.title,
                text: notification.text,
                isNew: notification.is_new,
            };
        }),
        notes: dto.notes,
    };
}

function mapListItem(item: StudentDashboardListItemDto) {
    return {
        id: item.id,
        icon: item.icon,
        title: item.title,
        text: item.text,
        meta: item.meta,
        tone: normalizeTone(item.tone),
    };
}

function mapCalendarDay(
    day: StudentDashboardSummaryDto["calendar"]["days"][number],
): DashboardCalendarDay {
    return {
        date: day.date,
        day: day.day,
        dateLabel: day.date_label,
        isToday: day.is_today,
        isSelected: day.is_selected,
        isMuted: day.is_muted,
        isWeekend: day.is_weekend,
        title: day.title,
        text: day.text,
        events: day.event_types.map((type) => {
            return {
                type: normalizeCalendarEventType(type),
            };
        }),
    };
}

function normalizeTone(tone?: string): DashboardTone | undefined {
    if (
        tone === "primary"
        || tone === "success"
        || tone === "warning"
        || tone === "danger"
        || tone === "violet"
        || tone === "neutral"
    ) {
        return tone;
    }

    return undefined;
}

function normalizeCalendarEventType(type: string): DashboardCalendarEventType {
    if (
        type === "lesson"
        || type === "checking"
        || type === "deadline"
        || type === "system"
        || type === "neutral"
    ) {
        return type;
    }

    return "neutral";
}
