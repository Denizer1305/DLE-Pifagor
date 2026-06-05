import type { DashboardDayCardContent } from "@/components/dashboard/types/dashboard.types";
import type { TeacherDashboardSummary } from "@/modules/teacher/types/teacher-dashboard.types";

export function createTeacherDayCard(
    summary: TeacherDashboardSummary,
): DashboardDayCardContent {
    return {
        badge: "Сегодня",
        icon: "fas fa-calendar-day",
        title: getActualDateLabel(summary.calendar.selectedDate),
        text:
            "Когда backend вернёт занятия, проверки и события на сегодня, они появятся в этой сводке.",
        stats: [
            {
                value: getStatValue(summary, "lessons_today"),
                label: "занятия",
            },
            {
                value: getStatValue(summary, "checking"),
                label: "работы",
            },
            {
                value: getStatValue(summary, "notifications"),
                label: "уведомлений",
            },
        ],
    };
}

function getStatValue(summary: TeacherDashboardSummary, key: string): string | number {
    return summary.stats.find((stat) => stat.key === key)?.value ?? 0;
}

function getActualDateLabel(value: string): string {
    const date = parseDateKey(value) || new Date();

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
