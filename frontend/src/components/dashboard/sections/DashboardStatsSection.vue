<script setup lang="ts">
import DashboardStatsCard from "@/components/dashboard/cards/DashboardStatsCard.vue";
import type { DashboardStatsCardContent } from "@/components/dashboard/types/dashboard.types";

interface Props {
    cards: DashboardStatsCardContent[];
    featuredCard?: DashboardStatsCardContent | null;
    progressLabel?: string;
    sectionClass?: string;
}

withDefaults(defineProps<Props>(), {
    featuredCard: null,
    progressLabel: "",
    sectionClass: "",
});
</script>

<template>
    <section
        class="dashboard-stats-grid fade-in visible"
        :class="sectionClass"
    >
        <DashboardStatsCard
            v-if="featuredCard"
            :card="featuredCard"
            is-featured
            :progress-label="progressLabel"
        />

        <DashboardStatsCard
            v-for="card in cards"
            :key="card.key"
            :card="card"
        />
    </section>
</template>
