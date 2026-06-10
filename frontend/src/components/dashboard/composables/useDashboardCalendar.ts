import { computed, ref, watch, type Ref } from "vue";

import type { DashboardCalendarDay } from "@/components/dashboard/types/dashboard.types";

export function useDashboardCalendar(days: Readonly<Ref<DashboardCalendarDay[]>>) {
    const selectedDate = ref("");
    const visibleMonthDate = ref(getInitialVisibleMonthDate(days.value));

    const sourceDaysByDate = computed(() => {
        return new Map(days.value.map((day) => [day.date, day]));
    });
    const displayedDays = computed(() => {
        return buildMonthDays(visibleMonthDate.value, sourceDaysByDate.value);
    });
    const displayedMonthLabel = computed(() => {
        return new Intl.DateTimeFormat("ru-RU", {
            month: "long",
            year: "numeric",
        }).format(visibleMonthDate.value);
    });
    const activeDay = computed(() => {
        if (selectedDate.value) {
            return displayedDays.value.find((day) => day.date === selectedDate.value) || null;
        }

        return (
            displayedDays.value.find((day) => day.isSelected) ||
            displayedDays.value.find((day) => day.isToday) ||
            displayedDays.value[0] ||
            null
        );
    });
    const hasActiveDayNote = computed(() => {
        return Boolean(activeDay.value?.title || activeDay.value?.text);
    });

    watch(
        days,
        (newDays) => {
            visibleMonthDate.value = getInitialVisibleMonthDate(newDays);
            selectedDate.value = "";
        },
        { deep: true },
    );

    function selectDay(day: DashboardCalendarDay): void {
        selectedDate.value = day.date;
    }

    function showPreviousMonth(): void {
        visibleMonthDate.value = addMonths(visibleMonthDate.value, -1);
        selectedDate.value = "";
    }

    function showNextMonth(): void {
        visibleMonthDate.value = addMonths(visibleMonthDate.value, 1);
        selectedDate.value = "";
    }

    return {
        activeDay,
        displayedDays,
        displayedMonthLabel,
        hasActiveDayNote,
        selectDay,
        showNextMonth,
        showPreviousMonth,
    };
}

export function getDashboardCalendarDateLabel(day: DashboardCalendarDay): string {
    return day.dateLabel || day.date;
}

function getInitialVisibleMonthDate(days: DashboardCalendarDay[]): Date {
    const sourceDay =
        days.find((day) => day.isSelected) ||
        days.find((day) => day.isToday) ||
        days[0];
    const sourceDate = parseDateKey(sourceDay?.date || "");

    if (sourceDate) {
        return new Date(sourceDate.getFullYear(), sourceDate.getMonth(), 1);
    }

    const today = new Date();

    return new Date(today.getFullYear(), today.getMonth(), 1);
}

function buildMonthDays(
    monthDate: Date,
    sourceDaysByDate: ReadonlyMap<string, DashboardCalendarDay>,
): DashboardCalendarDay[] {
    const year = monthDate.getFullYear();
    const month = monthDate.getMonth();
    const firstDay = new Date(year, month, 1);
    const startOffset = (firstDay.getDay() + 6) % 7;
    const startDate = new Date(year, month, 1 - startOffset);
    const todayKey = getDateKey(new Date());

    return Array.from({ length: 42 }, (_, index) => {
        const date = new Date(startDate);
        date.setDate(startDate.getDate() + index);

        const dateKey = getDateKey(date);
        const sourceDay = sourceDaysByDate.get(dateKey);

        return sourceDay || {
            date: dateKey,
            day: date.getDate(),
            dateLabel: formatDateLabel(date),
            isToday: dateKey === todayKey,
            isSelected: false,
            isMuted: date.getMonth() !== month,
            isWeekend: date.getDay() === 0 || date.getDay() === 6,
            title: "",
            text: "",
            events: [],
        };
    });
}

function addMonths(value: Date, count: number): Date {
    return new Date(value.getFullYear(), value.getMonth() + count, 1);
}

function getDateKey(value: Date): string {
    const year = value.getFullYear();
    const month = String(value.getMonth() + 1).padStart(2, "0");
    const day = String(value.getDate()).padStart(2, "0");

    return `${year}-${month}-${day}`;
}

function parseDateKey(value: string): Date | null {
    if (!value) {
        return null;
    }

    const [year, month, day] = value.split("-").map(Number);

    return year && month && day ? new Date(year, month - 1, day) : null;
}

function formatDateLabel(value: Date): string {
    return new Intl.DateTimeFormat("ru-RU", {
        day: "numeric",
        month: "long",
    }).format(value);
}
