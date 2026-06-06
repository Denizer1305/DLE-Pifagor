import {
    createEmptyDashboardCalendarContent,
    mapRoleCodeToDashboardPageClass,
    mapRoleCodeToDashboardRole,
} from "@/components/dashboard/mappers/dashboard-shell.mapper";
import { dashboardCreateModalContent } from "@/components/dashboard/data/dashboard-create-modal.data";
import type {
    DashboardPageScaffoldModel,
    DashboardShellConfig,
    DashboardUserProfile,
} from "@/components/dashboard/types/dashboard.types";
import { createAdminNavigation } from "@/modules/admin/data/admin-navigation.data";
import { createTeacherNavigation } from "@/modules/teacher/data/teacher-navigation.data";

import logo from "@/assets/image/logo/logo.svg";
import anastasiaLogo from "@/assets/image/logo/Anastasia.svg";

export interface CalendarUserContext {
    fullName: string;
    roleCode: string;
    roleLabel: string;
    avatarUrl?: string;
}

export function createCalendarPageModel(
    context: CalendarUserContext,
): DashboardPageScaffoldModel {
    const shell = createCalendarShell(context);
    const user = shell.topbarUser;

    return {
        shell,
        calendarContent: {
            ...createEmptyDashboardCalendarContent(),
            title: "Календарь",
            fullCalendarLabel: "Открыть полный календарь",
            fullCalendarTo: {
                name: getCalendarRouteName(context.roleCode),
            },
        },
        calendarDays: [],
        notifications: {
            title: "Уведомления",
            items: [],
            countLabel: "новых",
            emptyText: "Уведомлений пока нет.",
            actionLabel: "Открыть уведомления",
            actionTo: {
                name: getNotificationsRouteName(context.roleCode),
            },
        },
        notes: {
            title: "Заметки",
            createLabel: "Создать заметку",
            removeLabel: "Удалить заметку",
            items: [],
            countLabel: "заметок",
            emptyText: "Заметок пока нет.",
            actionLabel: "Открыть все заметки",
            actionTo: {
                name: getNotesRouteName(context.roleCode),
            },
        },
        profilePanel: {
            user,
            title: "Профиль",
            subtitle: user.roleLabel,
            actions: [
                { label: "Мой профиль", icon: "fas fa-user", to: { name: getProfileRouteName(context.roleCode) } },
                { label: "Настройки", icon: "fas fa-gear", to: { name: getSettingsRouteName(context.roleCode) } },
                { label: "Выйти", icon: "fas fa-arrow-right-from-bracket", action: "logout" },
            ],
        },
        createModal: dashboardCreateModalContent,
    };
}

function createCalendarShell(context: CalendarUserContext): DashboardShellConfig {
    const role = mapRoleCodeToDashboardRole(context.roleCode);
    const user = createUser(context);

    return {
        pageClass: `${mapRoleCodeToDashboardPageClass(context.roleCode)} calendar-page`,
        role,
        brand: {
            logo,
            title: "ПИФАГОР",
            subtitle: getBrandSubtitle(context.roleCode),
        },
        profile: user,
        navigation: getNavigation(context.roleCode),
        sidebarExtra: {
            variant: "ai",
            title: "Анастасия",
            subtitle: "Помощник по планированию",
            text: "Поможет собрать рабочий день, не потерять важные события и держать план под рукой.",
            image: {
                src: anastasiaLogo,
                alt: "Анастасия",
            },
            action: {
                label: "На главную",
                icon: "fas fa-house",
                to: {
                    name: getDashboardRouteName(context.roleCode),
                },
            },
        },
        search: {
            placeholder: "Поиск по календарю, событиям, заметкам...",
            ariaLabel: "Поиск по календарю",
        },
        topbarLabels: {
            menu: "Открыть меню",
            calendar: "Открыть календарь",
            notifications: "Открыть уведомления",
            notes: "Открыть заметки",
            profile: "Открыть меню профиля",
            closePanel: "Закрыть панель",
        },
        topbarUser: user,
    };
}

function createUser(context: CalendarUserContext): DashboardUserProfile {
    return {
        fullName: context.fullName || "Пользователь",
        roleLabel: context.roleLabel || "Личный календарь",
        avatarUrl: context.avatarUrl || "",
        avatarAlt: "Профиль пользователя",
    };
}

function getNavigation(roleCode: string) {
    if (roleCode === "teacher" || roleCode === "curator" || roleCode === "methodist" || roleCode === "organizer" || roleCode === "mentor") {
        return createTeacherNavigation(null);
    }

    if (roleCode === "superadmin" || roleCode === "platform_admin" || roleCode === "admin" || roleCode === "director" || roleCode === "org_admin" || roleCode === "department_head") {
        return createAdminNavigation();
    }

    return [
        { key: "dashboard", label: "Главная", description: "Вернуться в личный кабинет", icon: "fas fa-house", to: { name: getDashboardRouteName(roleCode) }, exact: true },
        { key: "calendar", label: "Календарь", description: "План и события", icon: "fas fa-calendar-days", to: { name: getCalendarRouteName(roleCode) } },
        { key: "notes", label: "Заметки", description: "Личные заметки", icon: "fas fa-note-sticky", to: { name: getNotesRouteName(roleCode) } },
        { key: "notifications", label: "Уведомления", description: "События и напоминания", icon: "fas fa-bell", to: { name: getNotificationsRouteName(roleCode) } },
        { key: "settings", label: "Настройки", description: "Профиль и параметры", icon: "fas fa-gear", to: { name: getSettingsRouteName(roleCode) } },
    ];
}

function getBrandSubtitle(roleCode: string): string {
    const role = mapRoleCodeToDashboardRole(roleCode);

    return role === "admin"
        ? "Календарь администратора"
        : role === "teacher"
            ? "Календарь преподавателя"
            : role === "parent"
                ? "Календарь родителя"
                : "Календарь студента";
}

function getDashboardRouteName(roleCode: string): string {
    const role = mapRoleCodeToDashboardRole(roleCode);

    return role === "admin"
        ? "admin-dashboard"
        : role === "teacher"
            ? "teacher-dashboard"
            : role === "parent"
                ? "parent-dashboard"
                : "student-dashboard";
}

function getCalendarRouteName(roleCode: string): string {
    const role = mapRoleCodeToDashboardRole(roleCode);

    return `${role}-calendar`;
}

function getNotificationsRouteName(roleCode: string): string {
    const role = mapRoleCodeToDashboardRole(roleCode);

    return `${role}-notifications`;
}

function getNotesRouteName(roleCode: string): string {
    const role = mapRoleCodeToDashboardRole(roleCode);

    return `${role}-notes`;
}

function getProfileRouteName(roleCode: string): string {
    const role = mapRoleCodeToDashboardRole(roleCode);

    return `${role}-profile`;
}

function getSettingsRouteName(roleCode: string): string {
    const role = mapRoleCodeToDashboardRole(roleCode);

    return `${role}-settings`;
}
