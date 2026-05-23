import type {
    DashboardCardSectionContent,
    DashboardCalendarDay,
    DashboardListItem,
    DashboardStatsCardContent,
    DashboardTimelineContent,
    DashboardTimelineItem,
} from "@/components/dashboard/types/dashboard.types";
import type {
    AdminDashboardAuditActor,
    AdminDashboardAuditActorDto,
    AdminDashboardAuditEvent,
    AdminDashboardAuditEventDto,
    AdminDashboardCalendar,
    AdminDashboardCalendarDayDto,
    AdminDashboardCalendarDto,
    AdminDashboardFeedbackRequest,
    AdminDashboardFeedbackRequestDto,
    AdminDashboardJoinRequest,
    AdminDashboardJoinRequestDto,
    AdminDashboardProfile,
    AdminDashboardProfileDto,
    AdminDashboardQuickAction,
    AdminDashboardQuickActionDto,
    AdminDashboardStat,
    AdminDashboardStatDto,
    AdminDashboardSummary,
    AdminDashboardSummaryDto,
    AdminDashboardSystemCheck,
    AdminDashboardSystemCheckDto,
    AdminDashboardSystemHealth,
    AdminDashboardSystemHealthDto,
    AdminDashboardUserShort,
    AdminDashboardUserShortDto,
} from "@/modules/admin/types/admin-dashboard.types";
import { resolveBackendAssetUrl } from "@/utils/backend-asset-url.utils";

function mapProfile(dto: AdminDashboardProfileDto): AdminDashboardProfile {
    return {
        id: dto.id,
        fullName: dto.full_name,
        email: dto.email,
        avatarUrl: resolveBackendAssetUrl(dto.avatar_url),
        roleLabel: dto.role_label,
    };
}

function mapStat(dto: AdminDashboardStatDto): AdminDashboardStat {
    return {
        key: dto.key,
        label: dto.label,
        value: dto.value,
        caption: dto.caption,
        icon: dto.icon,
        tone: dto.tone,
    };
}

function mapCalendarDay(dto: AdminDashboardCalendarDayDto): DashboardCalendarDay {
    return {
        date: dto.date,
        day: dto.day,
        dateLabel: formatCalendarDateLabel(dto.date),
        isToday: dto.is_today,
        isSelected: dto.is_selected,
        isMuted: dto.is_muted,
        isWeekend: dto.is_weekend,
        title: "",
        text: "",
        events: [],
    };
}

function mapCalendar(dto: AdminDashboardCalendarDto): AdminDashboardCalendar {
    const days = dto.days.map(mapCalendarDay);
    const selectedDate = dto.selected_date || getLocalDateKey(new Date());

    return {
        monthLabel: dto.month_label || formatCalendarMonthLabel(selectedDate),
        selectedDate,
        days: days.length >= 28 ? days : buildCalendarMonthDays(selectedDate),
    };
}

function mapUserShort(dto: AdminDashboardUserShortDto): AdminDashboardUserShort {
    return {
        id: dto.id,
        fullName: dto.full_name,
        email: dto.email,
        status: dto.status,
        createdAt: dto.created_at,
    };
}

function mapJoinRequest(dto: AdminDashboardJoinRequestDto): AdminDashboardJoinRequest {
    return {
        id: dto.id,
        requestType: dto.request_type,
        status: dto.status,
        user: mapUserShort(dto.user),
        organization: dto.organization,
        department: dto.department,
        group: dto.group,
        message: dto.message,
        createdAt: dto.created_at,
    };
}

function mapFeedbackRequest(dto: AdminDashboardFeedbackRequestDto): AdminDashboardFeedbackRequest {
    return {
        id: dto.id,
        fullName: dto.full_name,
        email: dto.email,
        topic: dto.topic,
        status: dto.status,
        message: dto.message,
        createdAt: dto.created_at,
    };
}

function mapAuditActor(
    dto: AdminDashboardAuditActorDto | null,
): AdminDashboardAuditActor | null {
    if (!dto) {
        return null;
    }

    return {
        id: dto.id,
        fullName: dto.full_name,
        email: dto.email,
    };
}

function mapAuditEvent(dto: AdminDashboardAuditEventDto): AdminDashboardAuditEvent {
    return {
        id: dto.id,
        action: dto.action,
        message: dto.message,
        actor: mapAuditActor(dto.actor),
        targetUser: mapAuditActor(dto.target_user),
        createdAt: dto.created_at,
    };
}

function mapSystemCheck(dto: AdminDashboardSystemCheckDto): AdminDashboardSystemCheck {
    return {
        key: dto.key,
        label: dto.label,
        status: dto.status,
        text: dto.text,
        icon: dto.icon,
    };
}

function mapSystemHealth(dto: AdminDashboardSystemHealthDto): AdminDashboardSystemHealth {
    return {
        status: dto.status,
        checks: dto.checks.map(mapSystemCheck),
    };
}

function mapQuickAction(dto: AdminDashboardQuickActionDto): AdminDashboardQuickAction {
    return {
        key: dto.key,
        label: dto.label,
        description: dto.description,
        icon: dto.icon,
        routeName: dto.route_name,
        tone: dto.tone,
    };
}

export function mapAdminDashboardSummary(
    dto: AdminDashboardSummaryDto,
): AdminDashboardSummary {
    return {
        profile: mapProfile(dto.profile),
        stats: dto.stats.map(mapStat),
        calendar: mapCalendar(dto.calendar),
        recentUsers: dto.recent_users.map(mapUserShort),
        joinRequests: dto.join_requests.map(mapJoinRequest),
        feedbackRequests: dto.feedback_requests.map(mapFeedbackRequest),
        auditEvents: dto.audit_events.map(mapAuditEvent),
        systemHealth: mapSystemHealth(dto.system_health),
        quickActions: dto.quick_actions.map(mapQuickAction),
    };
}

export function mapAdminStatsToDashboardCards(
    stats: AdminDashboardStat[],
): DashboardStatsCardContent[] {
    return stats.map((stat) => {
        return {
            key: stat.key,
            title: stat.label,
            text: stat.caption,
            icon: stat.icon,
            value: stat.value,
            caption: getStatCaption(stat.key),
            progress: getStatProgress(stat.value),
            tone: stat.tone,
        };
    });
}

export function mapAdminQuickActionsToListItems(
    actions: AdminDashboardQuickAction[],
): DashboardListItem[] {
    return actions.map((action) => {
        return {
            id: action.key,
            icon: action.icon,
            title: action.label,
            text: action.description,
            tone: action.tone,
        };
    });
}

export function mapRecentUsersToSection(
    users: AdminDashboardUserShort[],
): DashboardCardSectionContent {
    return {
        badge: "Пользователи",
        icon: "fas fa-users",
        title: "Новые пользователи",
        text: "Последние созданные аккаунты платформы.",
        action: {
            label: "Все пользователи",
            icon: "fas fa-arrow-right",
            to: {
                name: "admin-users",
            },
        },
        items: users.map((user) => {
            return {
                id: user.id,
                icon: "fas fa-user",
                title: user.fullName || user.email,
                text: user.email,
                meta: `${user.status} · ${formatDate(user.createdAt)}`,
                tone: "primary",
            };
        }),
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
        action: {
            label: "Открыть заявки",
            icon: "fas fa-arrow-right",
            to: {
                name: "admin-join-requests",
            },
        },
        items: requests.map((request) => {
            return {
                id: request.id,
                icon: "fas fa-user-clock",
                title: request.user.fullName || request.user.email,
                text: getJoinRequestText(request),
                meta: `${request.status} · ${formatDateTime(request.createdAt)}`,
                tone: "warning",
            };
        }),
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
        action: {
            label: "Все обращения",
            icon: "fas fa-arrow-right",
            to: {
                name: "admin-feedback",
            },
        },
        items: requests.map((request) => {
            return {
                id: request.id,
                icon: "fas fa-message",
                title: request.fullName,
                text: `${request.topic} · ${request.email}`,
                meta: formatDateTime(request.createdAt),
                tone: "warning",
            };
        }),
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
        items: health.checks.map((check) => {
            return {
                id: check.key,
                icon: check.icon,
                title: check.label,
                text: check.text,
                tone: check.status === "ok" ? "success" : "warning",
            };
        }),
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
        action: {
            label: "Логи",
            icon: "fas fa-arrow-right",
            to: {
                name: "admin-system",
            },
        },
        items: events.map(mapAuditEventToTimelineItem),
        emptyText: "Событий аудита пока нет.",
    };
}

function mapAuditEventToTimelineItem(
    event: AdminDashboardAuditEvent,
): DashboardTimelineItem {
    const actorLabel = event.actor?.fullName || event.actor?.email || "Система";

    return {
        id: event.id,
        time: formatTime(event.createdAt),
        title: event.action,
        text: event.message || actorLabel,
        tone: "neutral",
    };
}

function getJoinRequestText(request: AdminDashboardJoinRequest): string {
    if (request.organization?.name) {
        return request.organization.name;
    }

    if (request.department?.name) {
        return request.department.name;
    }

    if (request.group?.name) {
        return request.group.name;
    }

    return "Организация не указана";
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
    if (value <= 0) {
        return 8;
    }

    if (value >= 100) {
        return 100;
    }

    return Math.max(12, value);
}

function formatDate(value: string): string {
    if (!value) {
        return "—";
    }

    return new Intl.DateTimeFormat("ru-RU", {
        day: "2-digit",
        month: "short",
        year: "numeric",
    }).format(new Date(value));
}

function formatDateTime(value: string): string {
    if (!value) {
        return "—";
    }

    return new Intl.DateTimeFormat("ru-RU", {
        day: "2-digit",
        month: "short",
        hour: "2-digit",
        minute: "2-digit",
    }).format(new Date(value));
}

function formatTime(value: string): string {
    if (!value) {
        return "—";
    }

    return new Intl.DateTimeFormat("ru-RU", {
        hour: "2-digit",
        minute: "2-digit",
    }).format(new Date(value));
}

function formatCalendarDateLabel(value: string): string {
    if (!value) {
        return "";
    }

    return new Intl.DateTimeFormat("ru-RU", {
        day: "numeric",
        month: "long",
    }).format(new Date(value));
}

function formatCalendarMonthLabel(value: string): string {
    if (!value) {
        return "";
    }

    return new Intl.DateTimeFormat("ru-RU", {
        month: "long",
        year: "numeric",
    }).format(new Date(value));
}

function buildCalendarMonthDays(selectedDate: string): DashboardCalendarDay[] {
    const selected = parseDateKey(selectedDate) || new Date();
    const year = selected.getFullYear();
    const month = selected.getMonth();
    const firstDay = new Date(year, month, 1);
    const startOffset = (firstDay.getDay() + 6) % 7;
    const startDate = new Date(year, month, 1 - startOffset);
    const todayKey = getLocalDateKey(new Date());
    const selectedKey = getLocalDateKey(selected);

    return Array.from({ length: 42 }, (_, index) => {
        const date = new Date(startDate);
        date.setDate(startDate.getDate() + index);
        const dateKey = getLocalDateKey(date);

        return {
            date: dateKey,
            day: date.getDate(),
            dateLabel: formatCalendarDateLabel(dateKey),
            isToday: dateKey === todayKey,
            isSelected: dateKey === selectedKey,
            isMuted: date.getMonth() !== month,
            isWeekend: date.getDay() === 0 || date.getDay() === 6,
            title: "",
            text: "",
            events: [],
        };
    });
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

function getLocalDateKey(date: Date): string {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const day = String(date.getDate()).padStart(2, "0");

    return `${year}-${month}-${day}`;
}
