<script setup lang="ts">
import type { DashboardStatsCardContent } from "@/components/dashboard/types/dashboard.types";

interface Props {
    card: DashboardStatsCardContent;
    isFeatured?: boolean;
    progressLabel?: string;
}

withDefaults(defineProps<Props>(), {
    isFeatured: false,
    progressLabel: "",
});

function getProgressValue(value?: number): number {
    if (typeof value !== "number") {
        return 0;
    }

    return Math.min(100, Math.max(0, value));
}
</script>

<template>
    <article
        class="dashboard-stat-card fade-in visible"
        :class="[
            card.tone ? `is-${card.tone}` : '',
            isFeatured ? 'is-featured featured' : '',
        ]"
    >
        <div class="dashboard-stat-card-top">
            <div class="dashboard-stat-card-icon">
                <i :class="card.icon"></i>
            </div>

            <span>{{ card.title }}</span>
        </div>

        <strong class="dashboard-stat-card-value">
            {{ card.value }}
        </strong>

        <p v-if="card.text">
            {{ card.text }}
        </p>

        <span
            v-if="card.caption"
            class="dashboard-stat-card-caption"
        >
            {{ card.caption }}
        </span>

        <div
            v-if="card.progress !== undefined"
            class="dashboard-progress"
        >
            <div class="dashboard-progress-head">
                <span class="dashboard-progress-label">{{ progressLabel }}</span>
                <span class="dashboard-progress-label">{{ getProgressValue(card.progress) }}%</span>
            </div>

            <div class="dashboard-progress-track">
                <div
                    class="dashboard-progress-bar"
                    :style="{ width: `${getProgressValue(card.progress)}%` }"
                ></div>
            </div>
        </div>
    </article>
</template>
