<script setup lang="ts">
import { toRef } from "vue";
import { RouterLink } from "vue-router";

import DashboardCalendarDayButton from "@/components/dashboard/calendar/DashboardCalendarDay.vue";
import DashboardCalendarLegend from "@/components/dashboard/calendar/DashboardCalendarLegend.vue";
import {
    getDashboardCalendarDateLabel,
    useDashboardCalendar,
} from "@/components/dashboard/composables/useDashboardCalendar";
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
    (event: "remove", itemId: number): void;
}>();

const {
    activeDay,
    displayedDays,
    displayedMonthLabel,
    hasActiveDayNote,
    selectDay,
    showNextMonth,
    showPreviousMonth,
} = useDashboardCalendar(toRef(props, "days"));
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

        <DashboardCalendarLegend
            v-if="content.legend"
            :items="content.legend"
        />

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
            <DashboardCalendarDayButton
                v-for="day in displayedDays"
                :key="day.date"
                :day="day"
                :is-active="activeDay?.date === day.date"
                @select="selectDay"
            />
        </div>

        <div
            v-if="activeDay && hasActiveDayNote"
            class="dashboard-calendar-note"
        >
            <div class="dashboard-calendar-note-top">
                <span class="dashboard-calendar-note-date">
                    {{ getDashboardCalendarDateLabel(activeDay) }}
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

            <button
                v-if="activeDay.itemId && content.removeLabel"
                type="button"
                class="dashboard-panel-remove-btn"
                @click="emit('remove', activeDay.itemId)"
            >
                <i class="fas fa-trash"></i>
                {{ content.removeLabel }}
            </button>
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
