import type { DashboardNavigationItem } from "@/components/dashboard/types/dashboard.types";
import type { TeacherDashboardSummary } from "@/modules/teacher/types/teacher-dashboard.types";

function getStatValue(
    summary: TeacherDashboardSummary | null,
    key: string,
): string | number | undefined {
    return summary?.stats.find((stat) => stat.key === key)?.value;
}

function formatBadge(value: string | number | undefined): string | undefined {
    if (value === undefined || value === null || value === "") {
        return undefined;
    }

    if (typeof value === "number") {
        return new Intl.NumberFormat("ru-RU").format(value);
    }

    return value;
}

export function createTeacherNavigation(
    summary: TeacherDashboardSummary | null = null,
): DashboardNavigationItem[] {
    return [
        {
            key: "dashboard",
            label: "Главная",
            description: "Обзор дня и быстрые действия",
            icon: "fas fa-house",
            to: {
                name: "teacher-dashboard",
            },
            exact: true,
        },
        {
            key: "courses",
            label: "Мои курсы",
            description: "Все активные и черновые курсы",
            icon: "fas fa-book-open",
            to: {
                name: "teacher-courses",
            },
            badge: formatBadge(getStatValue(summary, "courses")),
        },
        {
            key: "lessons",
            label: "Уроки",
            description: "Планы занятий и материалы",
            icon: "fas fa-graduation-cap",
            to: {
                name: "teacher-lessons",
            },
        },
        {
            key: "tests",
            label: "Тесты",
            description: "Контроль знаний и проверки",
            icon: "fas fa-file-circle-check",
            to: {
                name: "teacher-tests",
            },
        },
        {
            key: "practice",
            label: "Практические",
            description: "Практика и задания",
            icon: "fas fa-pen-ruler",
            to: {
                name: "teacher-practice",
            },
        },
        {
            key: "homework",
            label: "Домашние задания",
            description: "Выдача и проверка работ",
            icon: "fas fa-house-laptop",
            to: {
                name: "teacher-homework",
            },
            badge: formatBadge(getStatValue(summary, "checking")),
        },
        {
            key: "journal",
            label: "Журнал",
            description: "Оценки, посещаемость, группы",
            icon: "fas fa-table-list",
            to: {
                name: "teacher-journal",
            },
        },
        {
            key: "analytics",
            label: "Аналитика",
            description: "Результаты и динамика обучения",
            icon: "fas fa-chart-line",
            to: {
                name: "teacher-analytics",
            },
        },
        {
            key: "calendar",
            label: "Календарь",
            description: "План, события и дедлайны",
            icon: "fas fa-calendar-days",
            to: {
                name: "teacher-calendar",
            },
        },
        {
            key: "feedback",
            label: "Обращения",
            description: "Вопросы и поддержка платформы",
            icon: "fas fa-envelope-open-text",
            to: {
                name: "teacher-feedback",
            },
        },
        {
            key: "notes",
            label: "Заметки",
            description: "Личные заметки и напоминания",
            icon: "fas fa-note-sticky",
            to: {
                name: "teacher-notes",
            },
        },
        {
            key: "notifications",
            label: "Уведомления",
            description: "Задания, проверки, события и напоминания",
            icon: "fas fa-bell",
            to: {
                name: "teacher-notifications",
            },
        },
        {
            key: "settings",
            label: "Настройки",
            description: "Профиль и параметры кабинета",
            icon: "fas fa-gear",
            to: {
                name: "teacher-settings",
            },
        },
    ];
}
