import type {
    DashboardCardSectionContent,
    DashboardListItem,
    DashboardStatsCardContent,
    DashboardTimelineContent,
    DashboardTimelineItem,
} from "@/components/dashboard/types/dashboard.types";
import {
    formatAdminDate,
    formatAdminDateTime,
    formatAdminTime,
} from "@/modules/admin/mappers/admin-dashboard-calendar.mapper";
import type {
    AdminDashboardAuditEvent,
    AdminDashboardFeedbackRequest,
    AdminDashboardJoinRequest,
    AdminDashboardQuickAction,
    AdminDashboardStat,
    AdminDashboardSystemHealth,
    AdminDashboardUserShort,
} from "@/modules/admin/types/admin-dashboard.types";

export function mapAdminStatsToDashboardCards(
    stats: AdminDashboardStat[],
): DashboardStatsCardContent[] {
    return stats.map((stat) => ({
        key: stat.key,
        title: stat.label,
        text: stat.caption,
        icon: stat.icon,
        value: stat.value,
        caption: getStatCaption(stat.key),
        progress: getStatProgress(stat.value),
        tone: stat.tone,
    }));
}

export function mapAdminQuickActionsToListItems(
    actions: AdminDashboardQuickAction[],
): DashboardListItem[] {
    return actions.map((action) => ({
        id: action.key,
        icon: action.icon,
        title: action.label,
        text: action.description,
        tone: action.tone,
    }));
}

export function mapRecentUsersToSection(
    users: AdminDashboardUserShort[],
): DashboardCardSectionContent {
    return {
        badge: "Пользователи",
        icon: "fas fa-users",
        title: "Новые пользователи",
        text: "Последние созданные аккаунты платформы.",
        action: { label: "Все пользователи", icon: "fas fa-arrow-right", to: { name: "admin-users" } },
        items: users.map((user) => ({
            id: user.id,
            icon: "fas fa-user",
            title: user.fullName || user.email,
            text: user.email,
            meta: `${user.status} · ${formatAdminDate(user.createdAt)}`,
            tone: "primary",
        })),
        emptyText: "Новых пользователей пока нет.",
    };
}

export function mapJoinRequestsToSection(
    requests: AdminDashboardJoinRequest[],
): DashboardCardSectionContent {
    return {
        badge: "Модерация",
        icon: "fas fa-user-check",
        title: "Заявки на присоединение",
        text: "Пользователи, ожидающие проверки и привязки к организации.",
        action: { label: "Открыть заявки", icon: "fas fa-arrow-right", to: { name: "admin-join-requests" } },
        items: requests.map((request) => ({
            id: request.id,
            icon: "fas fa-user-clock",
            title: request.user.fullName || request.user.email,
            text: getJoinRequestText(request),
            meta: `${request.status} · ${formatAdminDateTime(request.createdAt)}`,
            tone: "warning",
        })),
        emptyText: "Нет заявок, ожидающих рассмотрения.",
    };
}

export function mapFeedbackRequestsToSection(
    requests: AdminDashboardFeedbackRequest[],
): DashboardCardSectionContent {
    return {
        badge: "Поддержка",
        icon: "fas fa-envelope-open-text",
        title: "Обращения пользователей",
        text: "Новые сообщения от пользователей, организаций и партнёров.",
        action: { label: "Все обращения", icon: "fas fa-arrow-right", to: { name: "admin-feedback" } },
        items: requests.map((request) => ({
            id: request.id,
            icon: "fas fa-message",
            title: request.fullName,
            text: `${request.topic} · ${request.email}`,
            meta: formatAdminDateTime(request.createdAt),
            tone: "warning",
        })),
        emptyText: "Новых обращений пока нет.",
    };
}

export function mapSystemHealthToSection(
    health: AdminDashboardSystemHealth,
): DashboardCardSectionContent {
    return {
        badge: health.status,
        icon: "fas fa-server",
        title: "Состояние системы",
        text: "Базовая проверка состояния платформы.",
        items: health.checks.map((check) => ({
            id: check.key,
            icon: check.icon,
            title: check.label,
            text: check.text,
            tone: check.status === "ok" ? "success" : "warning",
        })),
        emptyText: "Системных проверок пока нет.",
    };
}

export function mapAuditEventsToTimeline(
    events: AdminDashboardAuditEvent[],
): DashboardTimelineContent {
    return {
        badge: "Аудит",
        icon: "fas fa-clock-rotate-left",
        title: "Последние действия",
        text: "Последние события пользовательского аудита.",
        action: { label: "Логи", icon: "fas fa-arrow-right", to: { name: "admin-system" } },
        items: events.map(mapAuditEventToTimelineItem),
        emptyText: "Событий аудита пока нет.",
    };
}

function mapAuditEventToTimelineItem(event: AdminDashboardAuditEvent): DashboardTimelineItem {
    const actorLabel = event.actor?.fullName || event.actor?.email || "Система";
    return {
        id: event.id,
        time: formatAdminTime(event.createdAt),
        title: event.action,
        text: event.message || actorLabel,
        tone: "neutral",
    };
}

function getJoinRequestText(request: AdminDashboardJoinRequest): string {
    return request.organization?.name
        || request.department?.name
        || request.group?.name
        || "Организация не указана";
}

function getStatCaption(key: string): string {
    const captions: Record<string, string> = {
        users: "аккаунты",
        teachers: "преподаватели",
        learners: "студенты",
        guardians: "родители",
        join_requests: "ожидают",
        feedback: "новые",
        organizations: "организации",
        courses: "курсы",
    };
    return captions[key] || "показатель";
}

function getStatProgress(value: number): number {
    return value <= 0 ? 8 : Math.min(100, Math.max(12, value));
}
