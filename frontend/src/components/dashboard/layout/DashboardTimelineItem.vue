<script setup lang="ts">
import type { DashboardTimelineItem } from "@/components/dashboard/types/dashboard.types";

interface Props {
    item: DashboardTimelineItem;
}

defineProps<Props>();
</script>

<template>
    <article
        class="dashboard-timeline-item"
        :class="item.tone ? `is-${item.tone}` : ''"
    >
        <div class="dashboard-timeline-time">
            {{ item.time }}
        </div>

        <div class="dashboard-timeline-line">
            <span class="dashboard-timeline-dot"></span>
        </div>

        <div class="dashboard-timeline-card">
            <strong>{{ item.title }}</strong>
            <span>{{ item.text }}</span>
        </div>
    </article>
</template>
