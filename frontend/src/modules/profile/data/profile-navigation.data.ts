import type { DashboardNavigationItem } from "@/components/dashboard/types/dashboard.types";
import type { ProfileRoleCode } from "@/modules/profile/types/profile.types";

export function createProfileNavigation(
    roleCode: ProfileRoleCode = "",
): DashboardNavigationItem[] {
    return [
        {
            key: "dashboard",
            label: "Главная",
            description: "Вернуться в личный кабинет",
            icon: "fas fa-house",
            to: {
                name: getDashboardRouteName(roleCode),
            },
        },
        {
            key: "profile",
            label: "Мой профиль",
            description: "Личные и ролевые данные",
            icon: "fas fa-user",
            to: {
                name: "profile",
            },
            exact: true,
        },
        {
            key: "profile-edit",
            label: "Редактирование профиля",
            description: "Изменение данных и настроек",
            icon: "fas fa-pen-to-square",
            to: {
                name: "profile-edit",
            },
        },
        {
            key: "achievements",
            label: "Достижения и награды",
            description: "Сертификаты и документы",
            icon: "fas fa-award",
            to: {
                name: "profile-achievements",
            },
        },
        {
            key: "settings",
            label: "Настройки",
            description: "Параметры кабинета",
            icon: "fas fa-gear",
            to: {
                name: getSettingsRouteName(roleCode),
            },
        },
    ];
}

function getDashboardRouteName(roleCode: ProfileRoleCode): string {
    if (
        roleCode === "teacher" ||
        roleCode === "curator" ||
        roleCode === "methodist" ||
        roleCode === "organizer" ||
        roleCode === "mentor"
    ) {
        return "teacher-dashboard";
    }

    if (roleCode === "learner" || roleCode === "student") {
        return "student-dashboard";
    }

    if (roleCode === "guardian") {
        return "parent-dashboard";
    }

    return "admin-dashboard";
}

function getSettingsRouteName(roleCode: ProfileRoleCode): string {
    if (
        roleCode === "teacher" ||
        roleCode === "curator" ||
        roleCode === "methodist" ||
        roleCode === "organizer" ||
        roleCode === "mentor"
    ) {
        return "teacher-settings";
    }

    if (roleCode === "learner" || roleCode === "student") {
        return "student-settings";
    }

    if (roleCode === "guardian") {
        return "parent-settings";
    }

    return "admin-settings";
}