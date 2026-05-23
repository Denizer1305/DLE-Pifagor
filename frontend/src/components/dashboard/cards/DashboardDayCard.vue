<script setup lang="ts">
import type { DashboardDayCardContent } from "@/components/dashboard/types/dashboard.types";

interface Props {
    content: DashboardDayCardContent;
}

defineProps<Props>();
</script>

<template>
    <div class="dashboard-day-card">
        <div class="dashboard-card-topline">
            <i :class="content.icon"></i>
            {{ content.badge }}
        </div>

        <h3 class="dashboard-day-title">
            {{ content.title }}
        </h3>

        <p class="dashboard-day-text">
            {{ content.text }}
        </p>

        <div class="dashboard-day-stats">
            <div
                v-for="stat in content.stats"
                :key="stat.label"
                class="dashboard-day-stat"
            >
                <strong>{{ stat.value }}</strong>
                <span>{{ stat.label }}</span>
            </div>
        </div>
    </div>
</template>
