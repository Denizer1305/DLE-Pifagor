<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { RouterLink } from "vue-router";

import type {
    DashboardCalendarContent,
    DashboardCalendarDay,
} from "@/components/dashboard/types/dashboard.types";

interface Props {
    content: DashboardCalendarContent;
    days: DashboardCalendarDay[];
}

const props = defineProps<Props>();
const emit = defineEmits<{
    (event: "create"): void;
}>();

const selectedDate = ref<string>("");
const visibleMonthDate = ref(getInitialVisibleMonthDate());

const visibleMonthKey = computed(() => {
    return getMonthKey(visibleMonthDate.value);
});

const sourceDaysByDate = computed(() => {
    return new Map(props.days.map((day) => {
        return [
            day.date,
            day,
        ];
    }));
});

const displayedDays = computed(() => {
    return buildMonthDays(visibleMonthDate.value);
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

watch(
    () => props.days,
    () => {
        visibleMonthDate.value = getInitialVisibleMonthDate();
        selectedDate.value = "";
    },
    {
        deep: true,
    },
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

function getDayClasses(day: DashboardCalendarDay): string[] {
    return [
        "dashboard-calendar-day",
        day.isMuted ? "is-muted" : "",
        day.isWeekend ? "is-weekend" : "",
        day.isToday ? "is-today" : "",
        activeDay.value?.date === day.date ? "is-selected" : "",
    ].filter(Boolean);
}

function getEventDotClass(type: string): string[] {
    return [
        "dashboard-event-dot",
        `is-${type}`,
    ];
}

function getDateLabel(day: DashboardCalendarDay): string {
    if (day.dateLabel) {
        return day.dateLabel;
    }

    return day.date;
}

const hasActiveDayNote = computed(() => {
    return Boolean(activeDay.value?.title || activeDay.value?.text);
});

function getInitialVisibleMonthDate(): Date {
    const sourceDay =
        props.days.find((day) => day.isSelected) ||
        props.days.find((day) => day.isToday) ||
        props.days[0];
    const sourceDate = parseDateKey(sourceDay?.date || "");

    if (sourceDate) {
        return new Date(sourceDate.getFullYear(), sourceDate.getMonth(), 1);
    }

    const today = new Date();

    return new Date(today.getFullYear(), today.getMonth(), 1);
}

function buildMonthDays(monthDate: Date): DashboardCalendarDay[] {
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
        const sourceDay = sourceDaysByDate.value.get(dateKey);

        if (sourceDay) {
            return sourceDay;
        }

        return {
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

function getMonthKey(value: Date): string {
    return `${value.getFullYear()}-${String(value.getMonth() + 1).padStart(2, "0")}`;
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

    if (!year || !month || !day) {
        return null;
    }

    return new Date(year, month - 1, day);
}

function formatDateLabel(value: Date): string {
    return new Intl.DateTimeFormat("ru-RU", {
        day: "numeric",
        month: "long",
    }).format(value);
}
</script>

<template>
    <div class="dashboard-calendar-content">
        <div class="dashboard-floating-panel-head dashboard-calendar-head">
            <div>
                <strong>{{ content.title }}</strong>
            </div>

            <div class="dashboard-calendar-month-switch">
                <button
                    type="button"
                    class="dashboard-calendar-nav"
                    :aria-label="content.previousMonthLabel"
                    @click="showPreviousMonth"
                >
                    <i class="fas fa-chevron-left"></i>
                </button>

                <div class="dashboard-calendar-month-label">
                    {{ displayedMonthLabel || content.monthLabel }}
                </div>

                <button
                    type="button"
                    class="dashboard-calendar-nav"
                    :aria-label="content.nextMonthLabel"
                    @click="showNextMonth"
                >
                    <i class="fas fa-chevron-right"></i>
                </button>
            </div>
        </div>

        <div
            v-if="content.legend?.length"
            class="dashboard-calendar-legend"
        >
            <span
                v-for="item in content.legend"
                :key="item.key"
                class="dashboard-calendar-legend-item"
                :class="`is-${item.key}`"
            >
                <i></i>
                {{ item.label }}
            </span>
        </div>

        <button
            type="button"
            class="dashboard-panel-create-btn"
            @click="emit('create')"
        >
            <i class="fas fa-plus"></i>
            {{ content.createLabel }}
        </button>

        <div class="dashboard-calendar-weekdays">
            <span
                v-for="weekday in content.weekdays"
                :key="weekday"
            >
                {{ weekday }}
            </span>
        </div>

        <div class="dashboard-mini-calendar">
            <button
                v-for="day in displayedDays"
                :key="day.date"
                type="button"
                :class="getDayClasses(day)"
                @click="selectDay(day)"
            >
                <span class="dashboard-calendar-day-number">
                    {{ day.day }}
                </span>

                <span
                    v-if="day.events?.length"
                    class="dashboard-calendar-day-dots"
                >
                    <i
                        v-for="event in day.events"
                        :key="`${day.date}-${event.type}`"
                        :class="getEventDotClass(event.type)"
                    ></i>
                </span>
            </button>
        </div>

        <div
            v-if="activeDay && hasActiveDayNote"
            class="dashboard-calendar-note"
        >
            <div class="dashboard-calendar-note-top">
                <span class="dashboard-calendar-note-date">
                    {{ getDateLabel(activeDay) }}
                </span>

                <span class="dashboard-calendar-note-badge">
                    {{ content.noteBadge }}
                </span>
            </div>

            <strong class="dashboard-calendar-note-title">
                {{ activeDay.title }}
            </strong>

            <p class="dashboard-calendar-note-text">
                {{ activeDay.text }}
            </p>
        </div>

        <RouterLink
            v-if="content.fullCalendarTo"
            class="dashboard-panel-link"
            :to="content.fullCalendarTo"
        >
            {{ content.fullCalendarLabel }}
        </RouterLink>

        <a
            v-else-if="content.fullCalendarLabel"
            href="#"
            class="dashboard-panel-link"
        >
            {{ content.fullCalendarLabel }}
        </a>
    </div>
</template>
