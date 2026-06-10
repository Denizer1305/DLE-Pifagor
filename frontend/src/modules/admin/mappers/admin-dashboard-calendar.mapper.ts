import type { DashboardCalendarDay } from "@/components/dashboard/types/dashboard.types";
import type {
    AdminDashboardCalendar,
    AdminDashboardCalendarDayDto,
    AdminDashboardCalendarDto,
} from "@/modules/admin/types/admin-dashboard.types";

export function mapAdminCalendar(dto: AdminDashboardCalendarDto): AdminDashboardCalendar {
    const days = dto.days.map(mapCalendarDay);
    const selectedDate = dto.selected_date || getLocalDateKey(new Date());

    return {
        monthLabel: dto.month_label || formatCalendarMonthLabel(selectedDate),
        selectedDate,
        days: days.length >= 28 ? days : buildCalendarMonthDays(selectedDate),
    };
}

export function formatAdminDate(value: string): string {
    if (!value) {
        return "—";
    }

    return new Intl.DateTimeFormat("ru-RU", {
        day: "2-digit",
        month: "short",
        year: "numeric",
    }).format(new Date(value));
}

export function formatAdminDateTime(value: string): string {
    if (!value) {
        return "—";
    }

    return new Intl.DateTimeFormat("ru-RU", {
        day: "2-digit",
        month: "short",
        hour: "2-digit",
        minute: "2-digit",
    }).format(new Date(value));
}

export function formatAdminTime(value: string): string {
    if (!value) {
        return "—";
    }

    return new Intl.DateTimeFormat("ru-RU", {
        hour: "2-digit",
        minute: "2-digit",
    }).format(new Date(value));
}

export function formatAdminCalendarDayLabel(value: string): string {
    if (!value) {
        return "";
    }

    return new Intl.DateTimeFormat("ru-RU", {
        day: "numeric",
        month: "long",
    }).format(parseDateKey(value) || new Date());
}

export function getTodayDateKey(): string {
    return getLocalDateKey(new Date());
}

function mapCalendarDay(dto: AdminDashboardCalendarDayDto): DashboardCalendarDay {
    return {
        date: dto.date,
        day: dto.day,
        dateLabel: formatAdminCalendarDayLabel(dto.date),
        isToday: dto.is_today,
        isSelected: dto.is_selected,
        isMuted: dto.is_muted,
        isWeekend: dto.is_weekend,
        title: "",
        text: "",
        events: [],
    };
}

function formatCalendarMonthLabel(value: string): string {
    return value
        ? new Intl.DateTimeFormat("ru-RU", { month: "long", year: "numeric" }).format(new Date(value))
        : "";
}

function buildCalendarMonthDays(selectedDate: string): DashboardCalendarDay[] {
    const selected = parseDateKey(selectedDate) || new Date();
    const year = selected.getFullYear();
    const month = selected.getMonth();
    const firstDay = new Date(year, month, 1);
    const startOffset = (firstDay.getDay() + 6) % 7;
    const startDate = new Date(year, month, 1 - startOffset);
    const todayKey = getLocalDateKey(new Date());
    const selectedKey = getLocalDateKey(selected);

    return Array.from({ length: 42 }, (_, index) => {
        const date = new Date(startDate);
        date.setDate(startDate.getDate() + index);
        const dateKey = getLocalDateKey(date);

        return {
            date: dateKey,
            day: date.getDate(),
            dateLabel: formatAdminCalendarDayLabel(dateKey),
            isToday: dateKey === todayKey,
            isSelected: dateKey === selectedKey,
            isMuted: date.getMonth() !== month,
            isWeekend: date.getDay() === 0 || date.getDay() === 6,
            title: "",
            text: "",
            events: [],
        };
    });
}

function parseDateKey(value: string): Date | null {
    if (!value) {
        return null;
    }

    const [year, month, day] = value.split("-").map(Number);
    return year && month && day ? new Date(year, month - 1, day) : null;
}

function getLocalDateKey(date: Date): string {
    return [
        date.getFullYear(),
        String(date.getMonth() + 1).padStart(2, "0"),
        String(date.getDate()).padStart(2, "0"),
    ].join("-");
}
