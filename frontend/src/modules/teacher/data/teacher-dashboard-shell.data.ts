import { dashboardTopbarLabels } from "@/components/dashboard/mappers/dashboard-shell.mapper";
import type {
    DashboardProfilePanelContent,
    DashboardShellConfig,
} from "@/components/dashboard/types/dashboard.types";
import { createTeacherNavigation } from "@/modules/teacher/data/teacher-navigation.data";
import type {
    TeacherDashboardProfile,
    TeacherDashboardSummary,
} from "@/modules/teacher/types/teacher-dashboard.types";

import logo from "@/assets/image/logo/logo.svg";
import anastasiaLogo from "@/assets/image/logo/Anastasia.svg";
import teacherAvatar from "@/assets/image/avatars/foto_teachers.webp";

export const teacherFallbackAvatar = teacherAvatar;

export function createTeacherShellConfig(
    profile: TeacherDashboardProfile,
    summary: TeacherDashboardSummary | null,
): DashboardShellConfig {
    const fullName = profile.fullName || "Преподаватель";
    const roleLabel = profile.roleLabel || "Преподаватель";
    const subjectLabel = profile.subjectLabel || "Учебные дисциплины";
    const avatarUrl = profile.avatarUrl || teacherFallbackAvatar;

    return {
        pageClass: "teacher-dashboard-page",
        role: "teacher",
        brand: {
            logo,
            title: "ПИФАГОР",
            subtitle: "Личный кабинет преподавателя",
        },
        profile: {
            fullName,
            roleLabel: `${roleLabel} · ${subjectLabel}`,
            avatarUrl,
            avatarAlt: "Профиль преподавателя",
        },
        navigation: createTeacherNavigation(summary),
        sidebarExtra: {
            variant: "ai",
            title: "Анастасия",
            subtitle: "Помощник преподавателя",
            text:
                "Подскажет, как составить урок, сделать тест, выдать домашнее задание и быстрее проверить работы.",
            image: {
                src: anastasiaLogo,
                alt: "Анастасия",
            },
            action: {
                label: "Открыть Анастасию",
                icon: "fas fa-sparkles",
                to: {
                    name: "teacher-dashboard",
                },
            },
        },
        search: {
            placeholder: "Поиск по курсам, урокам, заданиям...",
            ariaLabel: "Поиск",
        },
        topbarLabels: dashboardTopbarLabels,
        topbarUser: {
            fullName,
            roleLabel: createTeacherTopbarCaption(summary),
            avatarUrl,
            avatarAlt: "Профиль преподавателя",
        },
    };
}

export function createTeacherProfilePanelContent(
    profile: TeacherDashboardProfile,
): DashboardProfilePanelContent {
    const fullName = profile.fullName || "Преподаватель";
    const roleLabel = profile.roleLabel || "Преподаватель";

    return {
        user: {
            fullName,
            roleLabel,
            avatarUrl: profile.avatarUrl || teacherFallbackAvatar,
            avatarAlt: "Профиль преподавателя",
        },
        title: "Профиль преподавателя",
        subtitle: profile.subjectLabel || "Учебные дисциплины и настройки",
        actions: [
            {
                label: "Мой профиль",
                icon: "fas fa-user",
                to: {
                    name: "teacher-profile",
                },
            },
            {
                label: "Настройки",
                icon: "fas fa-gear",
                to: {
                    name: "teacher-settings",
                },
            },
            {
                label: "Безопасность",
                icon: "fas fa-shield-alt",
                to: {
                    name: "teacher-security",
                },
            },
            {
                label: "Выйти",
                icon: "fas fa-arrow-right-from-bracket",
                action: "logout",
            },
        ],
    };
}

function createTeacherTopbarCaption(summary: TeacherDashboardSummary | null): string {
    if (!summary) {
        return "Рабочее пространство преподавателя";
    }

    return `${getStatValue(summary, "lessons_today")} пары · ${getStatValue(summary, "checking")} работ на проверке`;
}

function getStatValue(summary: TeacherDashboardSummary, key: string): string | number {
    return summary.stats.find((stat) => stat.key === key)?.value ?? 0;
}
