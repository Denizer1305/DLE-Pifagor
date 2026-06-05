import type {
    DashboardCalendarContent,
    DashboardNotesContent,
    DashboardNotificationsContent,
} from "@/components/dashboard/types/dashboard.types";
import type { TeacherDashboardSummary } from "@/modules/teacher/types/teacher-dashboard.types";

export function createTeacherCalendarContent(monthLabel: string): DashboardCalendarContent {
    return {
        title: "Календарь преподавателя",
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
        legend: [
            {
                key: "lesson",
                label: "Урок",
            },
            {
                key: "checking",
                label: "Проверка",
            },
            {
                key: "deadline",
                label: "Дедлайн",
            },
        ],
        noteBadge: "Событие дня",
        createLabel: "Создать событие",
        removeLabel: "Удалить событие",
        fullCalendarLabel: "Открыть полный календарь",
        fullCalendarTo: {
            name: "teacher-calendar",
        },
    };
}

export function createTeacherNotificationsContent(
    summary: TeacherDashboardSummary,
): DashboardNotificationsContent {
    return {
        title: "Уведомления",
        items: summary.notifications.map((item) => {
            return {
                id: item.id,
                icon: item.icon,
                title: item.title,
                text: item.text,
                isNew: item.is_new,
            };
        }),
        emptyText: "Уведомлений пока нет.",
        actionLabel: "Посмотреть все уведомления",
        actionTo: {
            name: "teacher-notifications",
        },
    };
}

export function createTeacherNotesContent(
    summary: TeacherDashboardSummary,
): DashboardNotesContent {
    return {
        title: "Ближайшие заметки",
        createLabel: "Создать заметку",
        removeLabel: "Удалить заметку",
        items: summary.notes.map((note) => {
            return {
                id: note.id,
                date: note.date,
                title: note.title,
                text: note.text,
            };
        }),
        emptyText: "Заметок пока нет.",
        actionLabel: "Открыть все заметки",
        actionTo: {
            name: "teacher-notes",
        },
    };
}
