import type {
    DashboardCalendarContent,
    DashboardCalendarDay,
    DashboardDayCardContent,
    DashboardMiniPlanItem,
} from "@/components/dashboard/types/dashboard.types";
import type { ParentDashboardSummary } from "@/modules/parent/types/parent-dashboard.types";

export function createParentDayCard(
    summary?: ParentDashboardSummary,
): DashboardDayCardContent {
    return {
        badge: "Сегодня",
        icon: "fas fa-calendar-day",
        title: getDateLabel(summary?.calendar.selectedDate),
        text: getSelectedCalendarText(summary),
        stats: [
            { value: summary?.dayStats.lessons ?? 0, label: "занятий" },
            { value: summary?.dayStats.assignments ?? 0, label: "заданий" },
            { value: summary?.dayStats.messages ?? 0, label: "сообщений" },
        ],
    };
}

export function createParentMiniPlan(
    summary?: ParentDashboardSummary,
): DashboardMiniPlanItem[] {
    return (summary?.schedule ?? []).slice(0, 3).map(({ time, title, text }) => ({
        time,
        title,
        text,
    }));
}

export function createParentCalendarContent(
    summary?: ParentDashboardSummary,
): DashboardCalendarContent {
    return {
        title: "Календарь ребенка",
        monthLabel: summary?.calendar.monthLabel || getMonthLabel(new Date()),
        previousMonthLabel: "Предыдущий месяц",
        nextMonthLabel: "Следующий месяц",
        weekdays: ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"],
        legend: [
            { key: "lesson", label: "Урок" },
            { key: "checking", label: "Проверка" },
            { key: "deadline", label: "Дедлайн" },
        ],
        noteBadge: "Событие дня",
        createLabel: "Добавить событие",
        removeLabel: "Удалить событие",
        fullCalendarLabel: "Открыть полный календарь",
        fullCalendarTo: { name: "parent-calendar" },
    };
}

export function createEmptyParentCalendarDays(): DashboardCalendarDay[] {
    const today = new Date();
    const year = today.getFullYear();
    const month = today.getMonth();
    const firstDay = new Date(year, month, 1);
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    const mondayOffset = (firstDay.getDay() + 6) % 7;
    const days: DashboardCalendarDay[] = [];

    for (let index = 0; index < mondayOffset; index += 1) {
        days.push(createCalendarDay(new Date(year, month, index - mondayOffset + 1), true));
    }

    for (let day = 1; day <= daysInMonth; day += 1) {
        days.push(createCalendarDay(new Date(year, month, day), false));
    }

    while (days.length % 7 !== 0) {
        const lastDate = parseDateKey(days[days.length - 1]?.date) || today;
        const date = new Date(lastDate);
        date.setDate(lastDate.getDate() + 1);
        days.push(createCalendarDay(date, true));
    }

    return days;
}

function createCalendarDay(date: Date, isMuted: boolean): DashboardCalendarDay {
    const dateKey = formatDateKey(date);
    const isToday = dateKey === formatDateKey(new Date());

    return {
        date: dateKey,
        day: date.getDate(),
        dateLabel: getDateLabel(dateKey),
        isToday,
        isSelected: isToday,
        isMuted,
        isWeekend: date.getDay() === 0 || date.getDay() === 6,
        title: isToday ? "Сегодня" : "Событий нет",
        text: "Данные пока не добавлены.",
        events: [],
    };
}

function getDateLabel(value?: string): string {
    const date = parseDateKey(value) || new Date();
    return new Intl.DateTimeFormat("ru-RU", { day: "numeric", month: "long" }).format(date);
}

function getSelectedCalendarText(summary?: ParentDashboardSummary): string {
    if (!summary?.calendar.selectedDate) {
        return "После привязки учебного профиля здесь появятся события на выбранный день.";
    }

    const selectedDay = summary.calendar.days.find((day) => {
        return day.date === summary.calendar.selectedDate || day.isSelected;
    });
    return selectedDay?.text || "На выбранный день данных пока нет.";
}

function getMonthLabel(date: Date): string {
    return new Intl.DateTimeFormat("ru-RU", { month: "long", year: "numeric" }).format(date);
}

function parseDateKey(value?: string): Date | null {
    if (!value) {
        return null;
    }

    const [year, month, day] = value.split("-").map(Number);
    return year && month && day ? new Date(year, month - 1, day) : null;
}

function formatDateKey(date: Date): string {
    return [
        date.getFullYear(),
        String(date.getMonth() + 1).padStart(2, "0"),
        String(date.getDate()).padStart(2, "0"),
    ].join("-");
}
