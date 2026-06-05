<script setup lang="ts">
import type { DashboardCalendarDay } from "@/components/dashboard/types/dashboard.types";

interface Props {
    day: DashboardCalendarDay;
    isActive?: boolean;
}

interface Emits {
    (event: "select", day: DashboardCalendarDay): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

function getDayClasses(): string[] {
    return [
        "dashboard-calendar-day",
        props.day.isMuted ? "is-muted" : "",
        props.day.isWeekend ? "is-weekend" : "",
        props.day.isToday ? "is-today" : "",
        props.isActive ? "is-selected" : "",
        props.day.events?.length ? "has-events" : "",
    ].filter(Boolean);
}
</script>

<template>
    <button
        type="button"
        :class="getDayClasses()"
        :data-date-label="day.dateLabel || day.date"
        :data-note-title="day.title"
        :data-note-text="day.text"
        @click="emit('select', day)"
    >
        <span class="dashboard-calendar-day-number">
            {{ day.day }}
        </span>

        <span
            v-if="day.events?.length"
            class="dashboard-calendar-day-dots"
        >
            <i
                v-for="(event, index) in day.events"
                :key="`${day.date}-${event.type}-${index}`"
                class="dashboard-event-dot"
                :class="`is-${event.type}`"
            ></i>
        </span>
    </button>
</template>
