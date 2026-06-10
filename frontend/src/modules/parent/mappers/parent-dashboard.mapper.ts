import type {
    DashboardCalendarDay,
    DashboardCalendarEventType,
    DashboardTone,
} from "@/components/dashboard/types/dashboard.types";
import type { ParentDashboardSummaryDto } from "@/modules/parent/types/parent-dashboard-dto.types";
import type { ParentDashboardSummary } from "@/modules/parent/types/parent-dashboard.types";
import { resolveBackendAssetUrl } from "@/utils/backend-asset-url.utils";

export function mapParentDashboardSummary(
    dto: ParentDashboardSummaryDto,
): ParentDashboardSummary {
    return {
        profile: {
            id: dto.profile.id,
            fullName: dto.profile.full_name,
            email: dto.profile.email,
            avatarUrl: resolveBackendAssetUrl(dto.profile.avatar_url),
            roleLabel: dto.profile.role_label,
        },
        stats: dto.stats.map((stat) => ({
            key: stat.key,
            title: stat.label,
            value: stat.value,
            text: stat.caption,
            icon: stat.icon,
            progress: stat.progress ?? 0,
            tone: normalizeTone(stat.tone),
        })),
        dayStats: dto.day_stats,
        schedule: dto.schedule.map((item) => ({
            ...item,
            tone: normalizeTone(item.tone),
        })),
        calendar: {
            monthLabel: dto.calendar.month_label,
            selectedDate: dto.calendar.selected_date,
            days: dto.calendar.days.map(mapCalendarDay),
        },
        courses: dto.courses,
        importantItems: dto.important_items.map(mapListItem),
        activityItems: dto.activity_items.map(mapListItem),
        gradeRows: dto.grade_rows,
        messages: dto.messages.map(mapListItem),
        notifications: dto.notifications.map((item) => ({
            id: item.id,
            icon: item.icon,
            title: item.title,
            text: item.text,
            isNew: item.is_new,
        })),
        notes: dto.notes,
    };
}

function mapListItem(item: ParentDashboardSummaryDto["important_items"][number]) {
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
    day: ParentDashboardSummaryDto["calendar"]["days"][number],
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
        events: day.event_types.map((type) => ({
            type: normalizeCalendarEventType(type),
        })),
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
