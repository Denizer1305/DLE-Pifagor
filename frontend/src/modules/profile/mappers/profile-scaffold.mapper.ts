import {
    createEmptyDashboardCalendarContent,
    dashboardTopbarLabels,
    mapRoleCodeToDashboardPageClass,
    mapRoleCodeToDashboardRole,
} from "@/components/dashboard/mappers/dashboard-shell.mapper";
import { dashboardCreateModalContent } from "@/components/dashboard/data/dashboard-create-modal.data";
import type {
    DashboardPageScaffoldModel,
    DashboardShellConfig,
} from "@/components/dashboard/types/dashboard.types";
import { createProfileNavigation } from "@/modules/profile/data/profile-navigation.data";
import type {
    CurrentProfileDto,
    ProfileRoleCode,
} from "@/modules/profile/types/profile.types";
import { resolveBackendAssetUrl } from "@/utils/backend-asset-url.utils";

import logo from "@/assets/image/logo/logo.svg";
import anastasiaLogo from "@/assets/image/logo/Anastasia.svg";
import fallbackAvatar from "@/assets/image/avatars/denizer1305.webp";

export function mapCurrentProfileToScaffoldModel(
    dto: CurrentProfileDto,
): DashboardPageScaffoldModel {
    const avatarUrl = resolveBackendAssetUrl(dto.identity.avatar_url) || fallbackAvatar;

    return {
        shell: createProfileShell(dto, avatarUrl),
        calendarContent: createEmptyDashboardCalendarContent(),
        calendarDays: [],
        createModal: dashboardCreateModalContent,
        notifications: {
            title: "Уведомления",
            items: [],
            countLabel: "новых",
            actionLabel: "Открыть уведомления",
            actionTo: { name: getPanelRouteName(dto.active_role.code, "notifications") },
        },
        notes: {
            title: "Заметки",
            createLabel: "Создать заметку",
            removeLabel: "Удалить заметку",
            items: [],
            countLabel: "заметок",
            actionLabel: "Открыть все заметки",
            actionTo: { name: getPanelRouteName(dto.active_role.code, "notes") },
        },
        profilePanel: {
            user: {
                fullName: dto.identity.full_name || "Пользователь",
                roleLabel: dto.active_role.label,
                avatarUrl,
                avatarAlt: "Профиль пользователя",
            },
            title: "Профиль",
            subtitle: dto.active_role.label,
            actions: [
                { label: "Мой профиль", icon: "fas fa-user", to: { name: "profile" } },
                { label: "Редактировать профиль", icon: "fas fa-pen-to-square", to: { name: "profile-edit" } },
                { label: "Достижения и награды", icon: "fas fa-award", to: { name: "profile-achievements" } },
                { label: "Выйти", icon: "fas fa-arrow-right-from-bracket", action: "logout" },
            ],
        },
    };
}

function createProfileShell(
    dto: CurrentProfileDto,
    avatarUrl: string,
): DashboardShellConfig {
    const user = {
        fullName: dto.identity.full_name || "Пользователь",
        roleLabel: dto.active_role.label,
        avatarUrl,
        avatarAlt: "Профиль пользователя",
    };

    return {
        pageClass: `${mapRoleCodeToDashboardPageClass(dto.active_role.code)} profile-page`,
        role: mapRoleCodeToDashboardRole(dto.active_role.code),
        brand: { logo, title: "ПИФАГОР", subtitle: "Профиль пользователя" },
        profile: user,
        navigation: createProfileNavigation(dto.active_role.code),
        sidebarExtra: {
            variant: "ai",
            title: "Анастасия",
            subtitle: "Помощник профиля",
            text: "Поможет оформить профиль, систематизировать достижения и аккуратно представить данные внутри платформы.",
            image: { src: anastasiaLogo, alt: "Анастасия" },
            action: {
                label: "Открыть Анастасию",
                icon: "fas fa-sparkles",
                to: { name: "profile" },
            },
        },
        search: {
            placeholder: "Поиск по профилю, данным и документам...",
            ariaLabel: "Поиск по профилю",
        },
        topbarLabels: dashboardTopbarLabels,
        topbarUser: user,
    };
}

function getPanelRouteName(
    roleCode: ProfileRoleCode,
    panel: "notifications" | "notes",
): string {
    if (["teacher", "curator", "methodist", "organizer", "mentor"].includes(roleCode)) {
        return `teacher-${panel}`;
    }

    if (roleCode === "learner" || roleCode === "student") {
        return `student-${panel}`;
    }

    if (roleCode === "guardian") {
        return `parent-${panel}`;
    }

    return "admin-dashboard";
}
