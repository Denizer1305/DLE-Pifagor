import type {
    DashboardCalendarContent,
    DashboardRole,
    DashboardTopbarLabels,
} from "@/components/dashboard/types/dashboard.types";

const teacherRoleCodes = new Set([
    "teacher",
    "curator",
    "methodist",
    "organizer",
    "mentor",
]);

export const dashboardTopbarLabels: DashboardTopbarLabels = {
    menu: "Открыть меню",
    calendar: "Открыть календарь",
    notifications: "Открыть уведомления",
    notes: "Открыть заметки",
    profile: "Открыть меню профиля",
    closePanel: "Закрыть панель",
};

export function createEmptyDashboardCalendarContent(): DashboardCalendarContent {
    return {
        title: "Календарь",
        monthLabel: new Intl.DateTimeFormat("ru-RU", {
            month: "long",
            year: "numeric",
        }).format(new Date()),
        previousMonthLabel: "Предыдущий месяц",
        nextMonthLabel: "Следующий месяц",
        weekdays: [
            "Пн",
            "Вт",
            "Ср",
            "Чт",
            "Пт",
            "Сб",
            "Вс",
        ],
        noteBadge: "Событие",
        createLabel: "Создать событие",
        removeLabel: "Удалить событие",
    };
}

export function mapRoleCodeToDashboardRole(roleCode: string): DashboardRole {
    if (teacherRoleCodes.has(roleCode)) {
        return "teacher";
    }

    if (roleCode === "learner" || roleCode === "student") {
        return "student";
    }

    if (roleCode === "guardian") {
        return "parent";
    }

    return "admin";
}

export function mapRoleCodeToDashboardPageClass(roleCode: string): string {
    return `${mapRoleCodeToDashboardRole(roleCode)}-dashboard-page`;
}
