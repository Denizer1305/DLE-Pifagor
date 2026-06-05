import { dashboardTopbarLabels } from "@/components/dashboard/mappers/dashboard-shell.mapper";
import type {
    DashboardProfilePanelContent,
    DashboardShellConfig,
} from "@/components/dashboard/types/dashboard.types";
import { createAdminNavigation } from "@/modules/admin/data/admin-navigation.data";
import type {
    AdminDashboardProfile,
    AdminDashboardStat,
} from "@/modules/admin/types/admin-dashboard.types";

import logo from "@/assets/image/logo/logo.svg";
import anastasiaLogo from "@/assets/image/logo/Anastasia.svg";
import fallbackAvatar from "@/assets/image/avatars/denizer1305.webp";

export const adminFallbackAvatar = fallbackAvatar;

export function createAdminShellConfig(
    profile: AdminDashboardProfile,
    stats: AdminDashboardStat[] = [],
): DashboardShellConfig {
    const fullName = profile.fullName || profile.email || "Администратор";
    const roleLabel = profile.roleLabel || "Полный доступ · Управление платформой";
    const avatarUrl = profile.avatarUrl || adminFallbackAvatar;

    return {
        pageClass: "admin-dashboard-page",
        role: "admin",
        brand: {
            logo,
            title: "ПИФАГОР",
            subtitle: "Личный кабинет администратора",
        },
        profile: {
            fullName,
            roleLabel,
            avatarUrl,
            avatarAlt: "Профиль администратора",
        },
        navigation: createAdminNavigation(stats),
        sidebarExtra: {
            variant: "ai",
            title: "Анастасия",
            subtitle: "ИИ-помощник администратора",
            text:
                "Поможет анализировать активность платформы, искать аномалии, готовить сводки и быстрее принимать управленческие решения.",
            image: {
                src: anastasiaLogo,
                alt: "Анастасия",
            },
            action: {
                label: "Открыть Анастасию",
                icon: "fas fa-sparkles",
                to: {
                    name: "admin-dashboard",
                },
            },
        },
        search: {
            placeholder: "Поиск по пользователям, курсам, обращениям...",
            ariaLabel: "Поиск",
        },
        topbarLabels: dashboardTopbarLabels,
        topbarUser: {
            fullName,
            roleLabel,
            avatarUrl,
            avatarAlt: "Профиль администратора",
        },
    };
}

export function createAdminProfilePanelContent(
    profile: AdminDashboardProfile,
): DashboardProfilePanelContent {
    const fullName = profile.fullName || profile.email || "Администратор";
    const roleLabel = profile.roleLabel || "Полный доступ · Управление платформой";

    return {
        user: {
            fullName,
            roleLabel,
            avatarUrl: profile.avatarUrl || adminFallbackAvatar,
            avatarAlt: "Профиль администратора",
        },
        title: "Профиль администратора",
        subtitle: "Управление аккаунтом и настройками платформы",
        actions: [
            {
                label: "Мой профиль",
                icon: "fas fa-user",
                to: {
                    name: "admin-profile",
                },
            },
            {
                label: "Настройки",
                icon: "fas fa-gear",
                to: {
                    name: "admin-settings",
                },
            },
            {
                label: "Выйти",
                icon: "fas fa-right-from-bracket",
                action: "logout",
            },
        ],
    };
}
