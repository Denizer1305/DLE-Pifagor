import type {
    DashboardCalendarContent,
    DashboardNotesContent,
    DashboardNotificationsContent,
} from "@/components/dashboard/types/dashboard.types";

export function createAdminCalendarContent(monthLabel: string): DashboardCalendarContent {
    return {
        title: "Календарь администратора",
        monthLabel,
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
        noteBadge: "Заметка дня",
        createLabel: "Создать событие",
        removeLabel: "Удалить событие",
        fullCalendarLabel: "Открыть полный календарь",
        fullCalendarTo: {
            name: "admin-calendar",
        },
    };
}

export function createAdminNotificationsContent(): DashboardNotificationsContent {
    return {
        title: "Уведомления",
        items: [],
        countLabel: "новых",
        emptyText: "Уведомлений пока нет.",
    };
}

export function createAdminNotesContent(): DashboardNotesContent {
    return {
        title: "Важные заметки",
        createLabel: "Создать заметку",
        removeLabel: "Удалить заметку",
        items: [],
        countLabel: "заметок",
        emptyText: "Заметок пока нет.",
        actionLabel: "Открыть все заметки",
        actionTo: {
            name: "admin-notes",
        },
    };
}
