import { formatAdminDateTime } from "@/modules/admin/mappers/admin-dashboard-calendar.mapper";
import {
    formatAdminNumber,
    getSharePercent,
    getSummaryStatCaption,
    getSummaryStatValue,
} from "@/modules/admin/mappers/admin-dashboard-page.utils";
import type { AdminDashboardSummary } from "@/modules/admin/types/admin-dashboard.types";
import type {
    AdminDashboardEventModel,
    AdminDashboardParticipantCardModel,
} from "@/modules/admin/types/admin-dashboard-page.types";

export function mapAdminParticipants(
    summary: AdminDashboardSummary,
): AdminDashboardParticipantCardModel[] {
    const users = getSummaryStatValue(summary, "users");

    return [
        createParticipant(
            "fas fa-chalkboard-user",
            "Преподаватели",
            "Активны",
            getSummaryStatCaption(summary, "teachers", "Активные преподавательские роли"),
            getSummaryStatValue(summary, "teachers"),
            "аккаунтов",
            getSummaryStatValue(summary, "join_requests"),
            "заявок на проверке",
            "Доля преподавателей",
            users,
            ["Открыть", "Модерация", "Экспорт"],
        ),
        createParticipant(
            "fas fa-user-graduate",
            "Студенты",
            "Активны",
            getSummaryStatCaption(summary, "learners", "Активные учащиеся"),
            getSummaryStatValue(summary, "learners"),
            "студентов",
            getSummaryStatValue(summary, "courses"),
            "курсов",
            "Доля студентов",
            users,
            ["Открыть", "Группы", "Аналитика"],
        ),
        createParticipant(
            "fas fa-people-roof",
            "Родители",
            "Стабильно",
            getSummaryStatCaption(summary, "guardians", "Активные родительские аккаунты"),
            getSummaryStatValue(summary, "guardians"),
            "аккаунтов",
            getSummaryStatValue(summary, "learners"),
            "связанных студентов",
            "Доля родителей",
            users,
            ["Открыть", "Связи", "Экспорт"],
        ),
    ];
}

export function mapAdminRecentEvents(summary: AdminDashboardSummary): AdminDashboardEventModel[] {
    if (summary.auditEvents.length) {
        return summary.auditEvents.slice(0, 4).map((event) => ({
            icon: "fas fa-wave-square",
            title: event.action,
            text: event.message || event.actor?.fullName || "Системное событие",
        }));
    }

    if (summary.recentUsers.length) {
        return summary.recentUsers.slice(0, 4).map((user) => ({
            icon: "fas fa-user-plus",
            title: user.fullName || user.email,
            text: `${user.status} · ${formatAdminDateTime(user.createdAt)}`,
        }));
    }

    return [{
        icon: "fas fa-circle-info",
        title: "Событий пока нет",
        text: "Backend не вернул записи аудита или новых пользователей.",
    }];
}

function createParticipant(
    icon: string,
    title: string,
    status: string,
    text: string,
    firstValue: number,
    firstLabel: string,
    secondValue: number,
    secondLabel: string,
    progressLabel: string,
    totalUsers: number,
    actions: string[],
): AdminDashboardParticipantCardModel {
    return {
        icon,
        title,
        status,
        text,
        firstValue: formatAdminNumber(firstValue),
        firstLabel,
        secondValue: formatAdminNumber(secondValue),
        secondLabel,
        progressLabel,
        progress: getSharePercent(firstValue, totalUsers),
        actions,
    };
}
