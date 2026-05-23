<script setup lang="ts">
import type { DashboardCalendarLegendItem } from "@/components/dashboard/types/dashboard.types";

interface Props {
    items: DashboardCalendarLegendItem[];
}

defineProps<Props>();
</script>

<template>
    <div
        v-if="items.length"
        class="dashboard-calendar-legend"
    >
        <span
            v-for="item in items"
            :key="item.key"
            class="dashboard-calendar-legend-item"
            :class="`is-${item.key}`"
        >
            <i></i>
            {{ item.label }}
        </span>
    </div>
</template>
