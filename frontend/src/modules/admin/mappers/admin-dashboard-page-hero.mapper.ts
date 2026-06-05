import { adminDashboardHero } from "@/modules/admin/data/admin-dashboard-page.data";
import {
    formatAdminCalendarDayLabel,
    getTodayDateKey,
} from "@/modules/admin/mappers/admin-dashboard-calendar.mapper";
import { getSummaryStatValue } from "@/modules/admin/mappers/admin-dashboard-page.utils";
import type { AdminDashboardSummary } from "@/modules/admin/types/admin-dashboard.types";
import type {
    AdminDashboardDayCardModel,
    AdminDashboardHeroModel,
    AdminDashboardTimelineItemModel,
} from "@/modules/admin/types/admin-dashboard-page.types";

export function mapAdminHero(summary: AdminDashboardSummary): AdminDashboardHeroModel {
    return {
        ...adminDashboardHero,
        badges: [
            ...adminDashboardHero.badges,
            {
                label: getActualDashboardDateLabel(summary),
                icon: "fas fa-calendar-day",
            },
        ],
        actions: summary.quickActions.length
            ? summary.quickActions.map((action) => ({
                label: action.label,
                icon: action.icon,
                routeName: action.routeName,
                variant: action.tone === "primary" ? "primary" : "secondary",
            }))
            : adminDashboardHero.actions,
    };
}

export function mapAdminDayCard(summary: AdminDashboardSummary): AdminDashboardDayCardModel {
    return {
        badge: "Сегодня",
        icon: "fas fa-calendar-day",
        title: getActualDashboardDateLabel(summary),
        text: getSelectedCalendarText(summary),
        stats: [
            { value: getSummaryStatValue(summary, "join_requests"), label: "новых заявок" },
            { value: summary.auditEvents.length, label: "событий" },
            { value: getSummaryStatValue(summary, "feedback"), label: "обращений" },
        ],
    };
}

export function mapCalendarToPlanItems(
    summary: AdminDashboardSummary,
): AdminDashboardTimelineItemModel[] {
    const selectedDate = summary.calendar.selectedDate || getTodayDateKey();

    return summary.calendar.days
        .filter((day) => !day.isMuted && day.date >= selectedDate && Boolean(day.title || day.text))
        .slice(0, 4)
        .map((day) => ({
            time: day.dateLabel || formatAdminCalendarDayLabel(day.date),
            title: day.title || "Административная задача",
            text: day.text || "Проверьте состояние платформы и новые события.",
        }));
}

function getActualDashboardDateLabel(summary: AdminDashboardSummary): string {
    return formatAdminCalendarDayLabel(summary.calendar.selectedDate || getTodayDateKey());
}

function getSelectedCalendarText(summary: AdminDashboardSummary): string {
    const selectedDate = summary.calendar.selectedDate || getTodayDateKey();
    const selectedDay = summary.calendar.days.find((day) => {
        return day.date === selectedDate || day.isSelected;
    });

    return selectedDay?.text
        || "Сегодня важно проверить обращения, просмотреть системные события, подтвердить новые заявки и обновить административную сводку.";
}
