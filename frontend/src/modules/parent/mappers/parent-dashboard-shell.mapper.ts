import type {
    DashboardNavigationItem,
    DashboardShellConfig,
    DashboardUserProfile,
} from "@/components/dashboard/types/dashboard.types";
import { dashboardTopbarLabels } from "@/components/dashboard/mappers/dashboard-shell.mapper";
import type { ParentDashboardSummary } from "@/modules/parent/types/parent-dashboard.types";

import logo from "@/assets/image/logo/logo.svg";
import fallbackAvatar from "@/assets/image/avatars/anastasia_qe.webp";

export function createParentProfile(
    fullName: string,
    summary?: ParentDashboardSummary,
): DashboardUserProfile {
    const name = summary?.profile.fullName || fullName || "Родитель";
    const roleLabel = summary?.profile.roleLabel || "Родитель";

    return {
        fullName: name,
        roleLabel,
        avatarUrl: summary?.profile.avatarUrl || fallbackAvatar,
        avatarAlt: `Профиль родителя ${name}`,
    };
}

export function createParentShell(profile: DashboardUserProfile): DashboardShellConfig {
    return {
        pageClass: "parent-dashboard-page",
        role: "parent",
        brand: {
            logo,
            title: "ПИФАГОР",
            subtitle: "Личный кабинет родителя",
        },
        profile,
        navigation: createParentNavigation(),
        sidebarExtra: {
            variant: "student",
            icon: "fas fa-child",
            title: "Аккаунт ребенка",
            subtitle: "Быстрый переход к учебному профилю",
            text: "После привязки ребенка здесь появится быстрый доступ к его успеваемости, посещаемости и домашним заданиям.",
            action: {
                label: "Открыть профиль ребенка",
                icon: "fas fa-arrow-right",
                to: { name: "parent-child" },
            },
        },
        search: {
            placeholder: "Поиск по оценкам, предметам, сообщениям...",
            ariaLabel: "Поиск",
        },
        topbarLabels: dashboardTopbarLabels,
        topbarUser: profile,
    };
}

function createParentNavigation(): DashboardNavigationItem[] {
    return [
        {
            key: "dashboard",
            label: "Главная",
            description: "Сводка по ребенку и важные события",
            icon: "fas fa-house",
            to: { name: "parent-dashboard" },
            exact: true,
        },
        {
            key: "child",
            label: "Мой ребенок",
            description: "Профиль, группа и основная информация",
            icon: "fas fa-user-graduate",
            to: { name: "parent-child" },
        },
        {
            key: "grades",
            label: "Успеваемость",
            description: "Оценки, динамика и результаты",
            icon: "fas fa-book-open",
            to: { name: "parent-grades" },
        },
        {
            key: "attendance",
            label: "Посещаемость",
            description: "Пропуски, присутствие и причины",
            icon: "fas fa-calendar-check",
            to: { name: "parent-attendance" },
        },
        {
            key: "assignments",
            label: "Домашние задания",
            description: "Что задано и что уже выполнено",
            icon: "fas fa-house-laptop",
            to: { name: "parent-assignments" },
        },
        {
            key: "schedule",
            label: "Расписание",
            description: "Уроки, занятия и ближайшие события",
            icon: "fas fa-clock",
            to: { name: "parent-schedule" },
        },
        {
            key: "calendar",
            label: "Календарь",
            description: "План, события и дедлайны",
            icon: "fas fa-calendar-days",
            to: { name: "parent-calendar" },
        },
        {
            key: "notes",
            label: "Заметки",
            description: "Личные заметки и напоминания",
            icon: "fas fa-note-sticky",
            to: { name: "parent-notes" },
        },
        {
            key: "messages",
            label: "Сообщения",
            description: "Диалог с преподавателями и школой",
            icon: "fas fa-envelope-open-text",
            to: { name: "parent-messages" },
        },
        {
            key: "feedback",
            label: "Обращения",
            description: "Вопросы и поддержка платформы",
            icon: "fas fa-headset",
            to: { name: "parent-feedback" },
        },
        {
            key: "settings",
            label: "Настройки",
            description: "Профиль и параметры кабинета",
            icon: "fas fa-gear",
            to: { name: "parent-settings" },
        },
    ];
}
