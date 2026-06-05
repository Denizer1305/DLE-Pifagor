import type {
    DashboardNavigationItem,
    DashboardShellConfig,
    DashboardUserProfile,
} from "@/components/dashboard/types/dashboard.types";
import { dashboardTopbarLabels } from "@/components/dashboard/mappers/dashboard-shell.mapper";
import type { StudentDashboardSummary } from "@/modules/student/types/student-dashboard.types";

import logo from "@/assets/image/logo/logo.svg";
import fallbackAvatar from "@/assets/image/avatars/denizer1305.webp";

export function createStudentProfile(
    fullName: string,
    summary?: StudentDashboardSummary,
): DashboardUserProfile {
    const name = summary?.profile.fullName || fullName || "Студент";
    const roleLabel = summary?.profile.roleLabel || "Студент";
    const groupLabel = summary?.profile.groupLabel || "";

    return {
        fullName: name,
        roleLabel: groupLabel ? `${roleLabel} · ${groupLabel}` : roleLabel,
        avatarUrl: summary?.profile.avatarUrl || fallbackAvatar,
        avatarAlt: `Профиль студента ${name}`,
    };
}

export function createStudentShell(profile: DashboardUserProfile): DashboardShellConfig {
    return {
        pageClass: "student-dashboard-page",
        role: "student",
        brand: {
            logo,
            title: "ПИФАГОР",
            subtitle: "Личный кабинет студента",
        },
        profile: {
            ...profile,
            avatarAlt: profile.avatarAlt || "Профиль студента",
            roleLabel: profile.roleLabel || "Студент",
        },
        navigation: createStudentNavigation(),
        sidebarExtra: {
            variant: "student",
            icon: "fas fa-trophy",
            title: "Учебный прогресс",
            subtitle: "Появится после первых занятий",
            text: "Когда backend вернёт курсы, задания и оценки, здесь появится краткая сводка по прогрессу.",
            action: {
                label: "Смотреть прогресс",
                icon: "fas fa-chart-line",
                to: {
                    name: "student-progress",
                },
            },
        },
        search: {
            placeholder: "Поиск по курсам, урокам, заданиям...",
            ariaLabel: "Поиск",
        },
        topbarLabels: dashboardTopbarLabels,
        topbarUser: {
            ...profile,
            avatarAlt: profile.avatarAlt || "Профиль студента",
            roleLabel: profile.roleLabel || "Студент",
        },
    };
}

function createStudentNavigation(): DashboardNavigationItem[] {
    return [
        {
            key: "dashboard",
            label: "Главная",
            description: "Обзор дня и учебная активность",
            icon: "fas fa-house",
            to: { name: "student-dashboard" },
            exact: true,
        },
        {
            key: "courses",
            label: "Мои курсы",
            description: "Все подключённые дисциплины",
            icon: "fas fa-book-open",
            to: { name: "student-courses" },
        },
        {
            key: "lessons",
            label: "Уроки",
            description: "Занятия, материалы и темы",
            icon: "fas fa-chalkboard",
            to: { name: "student-lessons" },
        },
        {
            key: "assignments",
            label: "Задания",
            description: "Домашние, тесты и практика",
            icon: "fas fa-house-laptop",
            to: { name: "student-assignments" },
        },
        {
            key: "grades",
            label: "Успеваемость",
            description: "Оценки, статусы и результаты",
            icon: "fas fa-table-list",
            to: { name: "student-grades" },
        },
        {
            key: "progress",
            label: "Прогресс",
            description: "Личный рост и динамика",
            icon: "fas fa-chart-line",
            to: { name: "student-progress" },
        },
        {
            key: "calendar",
            label: "Календарь",
            description: "План, события и дедлайны",
            icon: "fas fa-calendar-days",
            to: { name: "student-calendar" },
        },
        {
            key: "feedback",
            label: "Обращения",
            description: "Вопросы и поддержка платформы",
            icon: "fas fa-envelope-open-text",
            to: { name: "student-feedback" },
        },
        {
            key: "notes",
            label: "Заметки",
            description: "Личные заметки и напоминания",
            icon: "fas fa-note-sticky",
            to: { name: "student-notes" },
        },
        {
            key: "settings",
            label: "Настройки",
            description: "Профиль и параметры кабинета",
            icon: "fas fa-gear",
            to: { name: "student-settings" },
        },
    ];
}
