import {
    formatAdminNumber,
    getSummaryStatCaption,
    getSummaryStatValue,
    getSystemHealthScore,
    getSystemHealthText,
} from "@/modules/admin/mappers/admin-dashboard-page.utils";
import type { AdminDashboardSummary } from "@/modules/admin/types/admin-dashboard.types";
import type {
    AdminDashboardAttentionItemModel,
    AdminDashboardCompactStatModel,
    AdminDashboardFeaturedStatModel,
    AdminDashboardOverviewRowModel,
} from "@/modules/admin/types/admin-dashboard-page.types";

export function mapAdminFeaturedStat(
    summary: AdminDashboardSummary,
): AdminDashboardFeaturedStatModel {
    const score = getSystemHealthScore(summary.systemHealth.status);

    return {
        icon: "fas fa-chart-line",
        title: "Состояние платформы",
        value: score,
        label: getSystemHealthText(summary.systemHealth.status),
        progress: score,
    };
}

export function mapAdminCompactStats(
    summary: AdminDashboardSummary,
): AdminDashboardCompactStatModel[] {
    return [
        createCompactStat(summary, "users", "fas fa-users", "Пользователи", "Зарегистрированные участники платформы"),
        createCompactStat(summary, "courses", "fas fa-book", "Курсы", "Активные учебные и рабочие курсы"),
        createCompactStat(summary, "feedback", "fas fa-envelope-open-text", "Обращения", "Новые и ожидающие обработки заявки"),
        createCompactStat(summary, "teachers", "fas fa-chalkboard-user", "Преподаватели", "Активные аккаунты и новые модерации"),
        {
            key: "system",
            icon: "fas fa-server",
            title: "Системные события",
            value: formatAdminNumber(summary.auditEvents.length),
            text: "Новые записи системного и пользовательского аудита",
        },
    ];
}

export function mapAdminCriticalItems(
    summary: AdminDashboardSummary,
): AdminDashboardAttentionItemModel[] {
    return [
        {
            icon: "fas fa-clipboard-check",
            title: `${getSummaryStatValue(summary, "join_requests")} заявок требуют обработки`,
            text: "Запросы ожидают проверки и привязки к организации.",
        },
        {
            icon: "fas fa-envelope-open-text",
            title: `${getSummaryStatValue(summary, "feedback")} новых обращений`,
            text: "Входящие сообщения поддержки требуют ответа.",
        },
        {
            icon: "fas fa-server",
            title: `${summary.systemHealth.checks.length} системных проверок`,
            text: getSystemHealthText(summary.systemHealth.status),
        },
        {
            icon: "fas fa-user-plus",
            title: `${summary.recentUsers.length} новых пользователей`,
            text: "Последние созданные аккаунты платформы.",
        },
    ];
}

export function mapAdminOverviewRows(
    summary: AdminDashboardSummary,
): AdminDashboardOverviewRowModel[] {
    const feedback = getSummaryStatValue(summary, "feedback");
    const isSystemHealthy = summary.systemHealth.status === "ok";

    return [
        {
            section: "Пользователи",
            state: "Активность",
            value: formatAdminNumber(getSummaryStatValue(summary, "users")),
            status: "Стабильно",
            warning: false,
        },
        {
            section: "Курсы",
            state: "Активные",
            value: formatAdminNumber(getSummaryStatValue(summary, "courses")),
            status: "Норма",
            warning: false,
        },
        {
            section: "Обращения",
            state: "Новые",
            value: formatAdminNumber(feedback),
            status: feedback > 0 ? "Нужно внимание" : "Чисто",
            warning: feedback > 0,
        },
        {
            section: "Система",
            state: summary.systemHealth.status,
            value: formatAdminNumber(summary.auditEvents.length),
            status: isSystemHealthy ? "Норма" : "Проверить",
            warning: !isSystemHealthy,
        },
    ];
}

function createCompactStat(
    summary: AdminDashboardSummary,
    key: string,
    icon: string,
    title: string,
    fallback: string,
): AdminDashboardCompactStatModel {
    return {
        key,
        icon,
        title,
        value: formatAdminNumber(getSummaryStatValue(summary, key)),
        text: getSummaryStatCaption(summary, key, fallback),
    };
}
