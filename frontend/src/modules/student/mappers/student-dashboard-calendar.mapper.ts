import type {
    DashboardCalendarContent,
    DashboardDayCardContent,
    DashboardMiniPlanItem,
} from "@/components/dashboard/types/dashboard.types";
import type { StudentDashboardSummary } from "@/modules/student/types/student-dashboard.types";

export function createStudentDayCard(
    summary?: StudentDashboardSummary,
): DashboardDayCardContent {
    return {
        badge: "Сегодня",
        icon: "fas fa-calendar-day",
        title: getDateLabel(summary?.calendar.selectedDate),
        text: getSelectedCalendarText(summary),
        stats: [
            { value: summary?.dayStats.lessons ?? 0, label: "занятий" },
            { value: summary?.dayStats.assignments ?? 0, label: "заданий" },
            { value: summary?.dayStats.notifications ?? 0, label: "уведомлений" },
        ],
    };
}

export function createStudentMiniPlan(
    summary?: StudentDashboardSummary,
): DashboardMiniPlanItem[] {
    return (summary?.schedule ?? []).slice(0, 3).map(({ time, title, text }) => ({
        time,
        title,
        text,
    }));
}

export function createStudentCalendarContent(
    summary?: StudentDashboardSummary,
): DashboardCalendarContent {
    return {
        title: "Календарь студента",
        monthLabel: summary?.calendar.monthLabel || getMonthLabel(new Date()),
        previousMonthLabel: "Предыдущий месяц",
        nextMonthLabel: "Следующий месяц",
        weekdays: ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"],
        legend: [
            { key: "lesson", label: "Занятие" },
            { key: "checking", label: "Сдача" },
            { key: "deadline", label: "Дедлайн" },
        ],
        noteBadge: "Событие дня",
        createLabel: "Добавить событие",
        removeLabel: "Удалить событие",
        fullCalendarLabel: "Открыть полный календарь",
        fullCalendarTo: {
            name: "student-calendar",
        },
    };
}

function getDateLabel(value?: string): string {
    const date = parseDateKey(value) || new Date();

    return new Intl.DateTimeFormat("ru-RU", {
        day: "numeric",
        month: "long",
    }).format(date);
}

function getSelectedCalendarText(summary?: StudentDashboardSummary): string {
    if (!summary?.calendar.selectedDate) {
        return "Когда появятся занятия, задания или события на сегодня, они отобразятся здесь.";
    }

    const selectedDay = summary.calendar.days.find((day) => {
        return day.date === summary.calendar.selectedDate || day.isSelected;
    });

    return selectedDay?.text
        || "Когда появятся занятия, задания или события на выбранный день, они отобразятся здесь.";
}

function getMonthLabel(date: Date): string {
    return new Intl.DateTimeFormat("ru-RU", {
        month: "long",
        year: "numeric",
    }).format(date);
}

function parseDateKey(value?: string): Date | null {
    if (!value) {
        return null;
    }

    const [year, month, day] = value.split("-").map(Number);
    return year && month && day ? new Date(year, month - 1, day) : null;
}
