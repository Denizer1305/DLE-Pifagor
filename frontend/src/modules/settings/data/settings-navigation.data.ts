import type { DashboardNavigationItem } from "@/components/dashboard/types/dashboard.types";
import type { SettingsRoleCode } from "@/modules/settings/types/settings.types";

export function createSettingsNavigation(
    roleCode: SettingsRoleCode | string = "",
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
        },
        {
            key: "settings",
            label: "Настройки",
            description: "Центр параметров платформы",
            icon: "fas fa-gear",
            to: {
                name: "settings",
            },
            exact: true,
        },
        {
            key: "security",
            label: "Безопасность",
            description: "Пароль, сессии и защита",
            icon: "fas fa-shield-halved",
            to: {
                name: "settings-security",
            },
        },
        {
            key: "notifications",
            label: "Уведомления",
            description: "События и каналы связи",
            icon: "fas fa-bell",
            to: {
                name: "settings-notifications",
            },
        },
        {
            key: "appearance",
            label: "Внешний вид",
            description: "Тема, интерфейс и отображение",
            icon: "fas fa-palette",
            to: {
                name: "settings-appearance",
            },
        },
        {
            key: "roles",
            label: "Ролевые настройки",
            description: "Поведение кабинета по роли",
            icon: "fas fa-user-gear",
            to: {
                name: "settings-roles",
            },
        },
        {
            key: "privacy",
            label: "Приватность",
            description: "Видимость данных и доступ",
            icon: "fas fa-user-lock",
            to: {
                name: "settings-privacy",
            },
        },
    ];
}

function getDashboardRouteName(roleCode: SettingsRoleCode | string): string {
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
