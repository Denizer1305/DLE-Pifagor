<script setup lang="ts">
import DashboardActivityCard from "@/components/dashboard/cards/DashboardActivityCard.vue";
import type { DashboardCardSectionContent } from "@/components/dashboard/types/dashboard.types";

interface Props {
    content: DashboardCardSectionContent;
}

defineProps<Props>();
</script>

<template>
    <DashboardActivityCard :content="content" />
</template>
