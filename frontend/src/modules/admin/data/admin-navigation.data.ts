import type { DashboardNavigationItem } from "@/components/dashboard/types/dashboard.types";
import type { AdminDashboardStat } from "@/modules/admin/types/admin-dashboard.types";

function getStatValue(
    stats: AdminDashboardStat[],
    key: string,
): number | undefined {
    return stats.find((stat) => stat.key === key)?.value;
}

function formatBadge(value: number | undefined): string | undefined {
    if (value === undefined) {
        return undefined;
    }

    return new Intl.NumberFormat("ru-RU").format(value);
}

export function createAdminNavigation(
    stats: AdminDashboardStat[] = [],
): DashboardNavigationItem[] {
    return [
        {
            key: "dashboard",
            label: "Главная",
            description: "Обзор системы и ключевые показатели",
            icon: "fas fa-house",
            to: {
                name: "admin-dashboard",
            },
            exact: true,
        },
        {
            key: "users",
            label: "Пользователи",
            description: "Все аккаунты платформы",
            icon: "fas fa-users",
            to: {
                name: "admin-users",
            },
            badge: formatBadge(getStatValue(stats, "users")),
        },
        {
            key: "teachers",
            label: "Преподаватели",
            description: "Состав, статусы и активность",
            icon: "fas fa-chalkboard-user",
            to: {
                name: "admin-users",
                query: {
                    role: "teacher",
                },
            },
            badge: formatBadge(getStatValue(stats, "teachers")),
        },
        {
            key: "learners",
            label: "Студенты",
            description: "Обучающиеся и группы",
            icon: "fas fa-user-graduate",
            to: {
                name: "admin-users",
                query: {
                    role: "learner",
                },
            },
            badge: formatBadge(getStatValue(stats, "learners")),
        },
        {
            key: "guardians",
            label: "Родители",
            description: "Связанные родительские аккаунты",
            icon: "fas fa-people-roof",
            to: {
                name: "admin-users",
                query: {
                    role: "guardian",
                },
            },
            badge: formatBadge(getStatValue(stats, "guardians")),
        },
        {
            key: "courses",
            label: "Курсы",
            description: "Активные, черновики, архив",
            icon: "fas fa-book-open",
            to: {
                name: "admin-courses",
            },
            badge: formatBadge(getStatValue(stats, "courses")),
        },
        {
            key: "structure",
            label: "Структура",
            description: "Группы, классы, роли и связи",
            icon: "fas fa-layer-group",
            to: {
                name: "admin-structure",
            },
        },
        {
            key: "feedback",
            label: "Обращения",
            description: "Запросы, жалобы и обратная связь",
            icon: "fas fa-envelope-open-text",
            to: {
                name: "admin-feedback",
            },
            badge: formatBadge(getStatValue(stats, "feedback")),
        },
        {
            key: "analytics",
            label: "Аналитика",
            description: "Посещаемость, активность, рост",
            icon: "fas fa-chart-line",
            to: {
                name: "admin-analytics",
            },
        },
        {
            key: "system",
            label: "Система",
            description: "Логи, состояние, события",
            icon: "fas fa-server",
            to: {
                name: "admin-system",
            },
        },
        {
            key: "settings",
            label: "Настройки",
            description: "Параметры платформы и доступы",
            icon: "fas fa-gear",
            to: {
                name: "admin-settings",
            },
        },
    ];
}
