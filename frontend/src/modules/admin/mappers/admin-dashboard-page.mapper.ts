import { adminDashboardHero } from "@/modules/admin/data/admin-dashboard-page.data";
import { adminAiCardContent } from "@/modules/admin/data/admin-dashboard.data";
import type { AdminDashboardSummary } from "@/modules/admin/types/admin-dashboard.types";
import type {
    AdminDashboardPageModel,
    AdminDashboardParticipantCardModel,
    AdminDashboardTimelineItemModel,
} from "@/modules/admin/types/admin-dashboard-page.types";

export function mapAdminSummaryToPageModel(
    summary: AdminDashboardSummary,
): AdminDashboardPageModel {
    const auditCount = summary.auditEvents.length;
    const planItems = mapCalendarToPlanItems(summary);
    const systemScore = getSystemHealthScore(summary.systemHealth.status);
    const heroActions = getHeroActions(summary);
    const currentDateLabel = getActualDashboardDateLabel(summary);

    const hero = {
        ...adminDashboardHero,
        badges: [
            ...adminDashboardHero.badges,
            {
                label: currentDateLabel,
                icon: "fas fa-calendar-day",
            },
        ],
        actions: heroActions,
    };

    const dayCard = {
        badge: "Сегодня",
        icon: "fas fa-calendar-day",
        title: currentDateLabel,
        text: getSelectedCalendarText(summary),
        stats: [
            {
                value: getSummaryStatValue(summary, "join_requests"),
                label: "новых заявок",
            },
            {
                value: auditCount,
                label: "событий",
            },
            {
                value: getSummaryStatValue(summary, "feedback"),
                label: "обращений",
            },
        ],
    };

    const miniPlan = planItems.slice(0, 3);

    return {
        hero,
        dayCard,
        miniPlan,
        heroSection: {
            hero,
            dayCard,
            miniPlan,
            miniPlanTitle: "Ближайший план",
            miniPlanIcon: "fas fa-clock",
        },
        featuredStat: {
            icon: "fas fa-chart-line",
            title: "Состояние платформы",
            value: systemScore,
            label: getSystemHealthText(summary.systemHealth.status),
            progress: systemScore,
        },
        compactStats: [
            {
                key: "users",
                icon: "fas fa-users",
                title: "Пользователи",
                value: formatNumber(getSummaryStatValue(summary, "users")),
                text: getStatCaption(
                    summary,
                    "users",
                    "Зарегистрированные участники платформы",
                ),
            },
            {
                key: "courses",
                icon: "fas fa-book",
                title: "Курсы",
                value: formatNumber(getSummaryStatValue(summary, "courses")),
                text: getStatCaption(
                    summary,
                    "courses",
                    "Активные учебные и рабочие курсы",
                ),
            },
            {
                key: "feedback",
                icon: "fas fa-envelope-open-text",
                title: "Обращения",
                value: formatNumber(getSummaryStatValue(summary, "feedback")),
                text: getStatCaption(
                    summary,
                    "feedback",
                    "Новые и ожидающие обработки заявки",
                ),
            },
            {
                key: "teachers",
                icon: "fas fa-chalkboard-user",
                title: "Преподаватели",
                value: formatNumber(getSummaryStatValue(summary, "teachers")),
                text: getStatCaption(
                    summary,
                    "teachers",
                    "Активные аккаунты и новые модерации",
                ),
            },
            {
                key: "system",
                icon: "fas fa-server",
                title: "Системные события",
                value: formatNumber(auditCount),
                text: "Новые записи системного и пользовательского аудита",
            },
        ],
        planItems,
        criticalItems: [
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
        ],
        participants: mapAdminParticipants(summary),
        recentEvents: mapAdminRecentEvents(summary),
        overviewRows: [
            {
                section: "Пользователи",
                state: "Активность",
                value: formatNumber(getSummaryStatValue(summary, "users")),
                status: "Стабильно",
                warning: false,
            },
            {
                section: "Курсы",
                state: "Активные",
                value: formatNumber(getSummaryStatValue(summary, "courses")),
                status: "Норма",
                warning: false,
            },
            {
                section: "Обращения",
                state: "Новые",
                value: formatNumber(getSummaryStatValue(summary, "feedback")),
                status: getSummaryStatValue(summary, "feedback") > 0
                    ? "Нужно внимание"
                    : "Чисто",
                warning: getSummaryStatValue(summary, "feedback") > 0,
            },
            {
                section: "Система",
                state: summary.systemHealth.status,
                value: formatNumber(auditCount),
                status: summary.systemHealth.status === "ok"
                    ? "Норма"
                    : "Проверить",
                warning: summary.systemHealth.status !== "ok",
            },
        ],
        ai: adminAiCardContent,
    };
}

function getHeroActions(summary: AdminDashboardSummary) {
    if (!summary.quickActions.length) {
        return adminDashboardHero.actions;
    }

    return summary.quickActions.map((action) => {
        return {
            label: action.label,
            icon: action.icon,
            routeName: action.routeName,
            variant: action.tone === "primary"
                ? "primary" as const
                : "secondary" as const,
        };
    });
}

function mapCalendarToPlanItems(
    summary: AdminDashboardSummary,
): AdminDashboardTimelineItemModel[] {
    const selectedDate = summary.calendar.selectedDate || getTodayDateKey();

    const sourceDays = summary.calendar.days
        .filter((day) => {
            return (
                !day.isMuted &&
                day.date >= selectedDate &&
                Boolean(day.title || day.text)
            );
        })
        .slice(0, 4);

    return sourceDays.map((day) => {
        return {
            time: day.dateLabel || formatCalendarDayLabel(day.date),
            title: day.title || "Административная задача",
            text: day.text || "Проверьте состояние платформы и новые события.",
        };
    });
}

function mapAdminParticipants(
    summary: AdminDashboardSummary,
): AdminDashboardParticipantCardModel[] {
    return [
        {
            icon: "fas fa-chalkboard-user",
            title: "Преподаватели",
            status: "Активны",
            text: getStatCaption(summary, "teachers", "Активные преподавательские роли"),
            firstValue: formatNumber(getSummaryStatValue(summary, "teachers")),
            firstLabel: "аккаунтов",
            secondValue: formatNumber(getSummaryStatValue(summary, "join_requests")),
            secondLabel: "заявок на проверке",
            progressLabel: "Доля преподавателей",
            progress: getSharePercent(
                getSummaryStatValue(summary, "teachers"),
                getSummaryStatValue(summary, "users"),
            ),
            actions: [
                "Открыть",
                "Модерация",
                "Экспорт",
            ],
        },
        {
            icon: "fas fa-user-graduate",
            title: "Студенты",
            status: "Активны",
            text: getStatCaption(summary, "learners", "Активные учащиеся"),
            firstValue: formatNumber(getSummaryStatValue(summary, "learners")),
            firstLabel: "студентов",
            secondValue: formatNumber(getSummaryStatValue(summary, "courses")),
            secondLabel: "курсов",
            progressLabel: "Доля студентов",
            progress: getSharePercent(
                getSummaryStatValue(summary, "learners"),
                getSummaryStatValue(summary, "users"),
            ),
            actions: [
                "Открыть",
                "Группы",
                "Аналитика",
            ],
        },
        {
            icon: "fas fa-people-roof",
            title: "Родители",
            status: "Стабильно",
            text: getStatCaption(summary, "guardians", "Активные родительские аккаунты"),
            firstValue: formatNumber(getSummaryStatValue(summary, "guardians")),
            firstLabel: "аккаунтов",
            secondValue: formatNumber(getSummaryStatValue(summary, "learners")),
            secondLabel: "связанных студентов",
            progressLabel: "Доля родителей",
            progress: getSharePercent(
                getSummaryStatValue(summary, "guardians"),
                getSummaryStatValue(summary, "users"),
            ),
            actions: [
                "Открыть",
                "Связи",
                "Экспорт",
            ],
        },
    ];
}

function mapAdminRecentEvents(summary: AdminDashboardSummary) {
    if (summary.auditEvents.length) {
        return summary.auditEvents.slice(0, 4).map((event) => {
            return {
                icon: "fas fa-wave-square",
                title: event.action,
                text: event.message || event.actor?.fullName || "Системное событие",
            };
        });
    }

    if (summary.recentUsers.length) {
        return summary.recentUsers.slice(0, 4).map((user) => {
            return {
                icon: "fas fa-user-plus",
                title: user.fullName || user.email,
                text: `${user.status} · ${formatDateTime(user.createdAt)}`,
            };
        });
    }

    return [
        {
            icon: "fas fa-circle-info",
            title: "Событий пока нет",
            text: "Backend не вернул записи аудита или новых пользователей.",
        },
    ];
}

function getActualDashboardDateLabel(summary: AdminDashboardSummary): string {
    const selectedDate = summary.calendar.selectedDate;

    if (selectedDate) {
        return formatCalendarDayLabel(selectedDate);
    }

    return formatCalendarDayLabel(getTodayDateKey());
}

function getSelectedCalendarText(summary: AdminDashboardSummary): string {
    const selectedDate = summary.calendar.selectedDate || getTodayDateKey();

    const selectedDay = summary.calendar.days.find((day) => {
        return day.date === selectedDate || day.isSelected;
    });

    if (selectedDay?.text) {
        return selectedDay.text;
    }

    return "Сегодня важно проверить обращения, просмотреть системные события, подтвердить новые заявки и обновить административную сводку.";
}

function getSummaryStatValue(
    summary: AdminDashboardSummary,
    key: string,
): number {
    return summary.stats.find((stat) => stat.key === key)?.value ?? 0;
}

function getStatCaption(
    summary: AdminDashboardSummary,
    key: string,
    fallback: string,
): string {
    return summary.stats.find((stat) => stat.key === key)?.caption || fallback;
}

function getSharePercent(value: number, total: number): number {
    if (total <= 0 || value <= 0) {
        return 0;
    }

    return Math.min(100, Math.round((value / total) * 100));
}

function getSystemHealthScore(status: string): number {
    if (status === "critical") {
        return 40;
    }

    if (status === "warning") {
        return 70;
    }

    return 100;
}

function getSystemHealthText(status: string): string {
    if (status === "critical") {
        return "Backend сообщает о критическом состоянии системы.";
    }

    if (status === "warning") {
        return "Backend сообщает, что системе требуется внимание.";
    }

    return "Backend сообщает, что система работает стабильно.";
}

function formatNumber(value: number): string {
    return new Intl.NumberFormat("ru-RU").format(value);
}

function formatCalendarDayLabel(value: string): string {
    if (!value) {
        return "";
    }

    return new Intl.DateTimeFormat("ru-RU", {
        day: "numeric",
        month: "long",
    }).format(parseDateKey(value));
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

function getTodayDateKey(): string {
    const today = new Date();

    return [
        today.getFullYear(),
        String(today.getMonth() + 1).padStart(2, "0"),
        String(today.getDate()).padStart(2, "0"),
    ].join("-");
}

function parseDateKey(value: string): Date {
    const [year, month, day] = value.split("-").map(Number);

    if (!year || !month || !day) {
        return new Date();
    }

    return new Date(year, month - 1, day);
}