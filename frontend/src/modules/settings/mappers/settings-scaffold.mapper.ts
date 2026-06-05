import {
    createEmptyDashboardCalendarContent,
    dashboardTopbarLabels,
    mapRoleCodeToDashboardPageClass,
    mapRoleCodeToDashboardRole,
} from "@/components/dashboard/mappers/dashboard-shell.mapper";
import type {
    DashboardPageScaffoldModel,
    DashboardShellConfig,
} from "@/components/dashboard/types/dashboard.types";
import { dashboardCreateModalContent } from "@/components/dashboard/data/dashboard-create-modal.data";
import { createSettingsNavigation } from "@/modules/settings/data/settings-navigation.data";
import { localizeSettingsContent } from "@/modules/settings/data/settings-translations.data";
import type { LocaleCode } from "@/stores/locale.store";

import logo from "@/assets/image/logo/logo.svg";
import anastasiaLogo from "@/assets/image/logo/Anastasia.svg";
import fallbackAvatar from "@/assets/image/avatars/denizer1305.webp";

export interface SettingsUserContext {
    fullName: string;
    roleLabel: string;
    roleCode: string;
    avatarUrl?: string;
}

export function createSettingsScaffold(
    context: SettingsUserContext,
    pageClass: string,
    locale: LocaleCode = "ru",
): DashboardPageScaffoldModel {
    const scaffold: DashboardPageScaffoldModel = {
        shell: createSettingsShell(context, pageClass),
        calendarContent: createEmptyDashboardCalendarContent(),
        calendarDays: [],
        createModal: dashboardCreateModalContent,
        notifications: {
            title: "Уведомления",
            items: [],
            actionLabel: "Открыть уведомления",
            actionTo: { name: "settings-notifications" },
        },
        notes: {
            title: "Заметки",
            createLabel: "Создать заметку",
            removeLabel: "Удалить заметку",
            items: [],
            actionLabel: "Открыть все заметки",
            actionTo: { name: "profile" },
        },
        profilePanel: {
            user: {
                fullName: context.fullName || "Пользователь",
                roleLabel: context.roleLabel || "Пользователь",
                avatarUrl: context.avatarUrl || fallbackAvatar,
                avatarAlt: "Профиль пользователя",
            },
            title: "Профиль",
            subtitle: context.roleLabel || "Пользователь",
            actions: [
                { label: "Мой профиль", icon: "fas fa-user", to: { name: "profile" } },
                { label: "Настройки", icon: "fas fa-gear", to: { name: "settings" } },
                { label: "Внешний вид", icon: "fas fa-palette", to: { name: "settings-appearance" } },
                { label: "Выйти", icon: "fas fa-arrow-right-from-bracket", action: "logout" },
            ],
        },
    };

    return localizeSettingsContent(scaffold, locale);
}

function createSettingsShell(
    context: SettingsUserContext,
    pageClass: string,
): DashboardShellConfig {
    const user = {
        fullName: context.fullName || "Пользователь",
        roleLabel: context.roleLabel || "Пользователь",
        avatarUrl: context.avatarUrl || fallbackAvatar,
        avatarAlt: "Профиль пользователя",
    };

    return {
        pageClass: `${mapRoleCodeToDashboardPageClass(context.roleCode)} ${pageClass}`,
        role: mapRoleCodeToDashboardRole(context.roleCode),
        brand: {
            logo,
            title: "ПИФАГОР",
            subtitle: "Настройки платформы",
        },
        profile: user,
        navigation: createSettingsNavigation(context.roleCode),
        sidebarExtra: {
            variant: "ai",
            title: "Анастасия",
            subtitle: "Помощник по настройкам",
            text: "Поможет разобраться с настройками, подобрать комфортный интерфейс и включить важные параметры безопасности.",
            image: { src: anastasiaLogo, alt: "Анастасия" },
            action: {
                label: "Открыть Анастасию",
                icon: "fas fa-sparkles",
                to: { name: "settings" },
            },
        },
        search: {
            placeholder: "Поиск по настройкам, безопасности, уведомлениям...",
            ariaLabel: "Поиск по настройкам",
        },
        topbarLabels: dashboardTopbarLabels,
        topbarUser: {
            ...user,
            roleLabel: context.roleLabel || "Настройки аккаунта",
        },
    };
}
