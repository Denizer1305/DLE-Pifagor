<script setup lang="ts">
import DashboardAttentionCard from "@/components/dashboard/cards/DashboardAttentionCard.vue";
import type { DashboardCardSectionContent } from "@/components/dashboard/types/dashboard.types";

interface Props {
    content: DashboardCardSectionContent;
}

defineProps<Props>();
</script>

<template>
    <DashboardAttentionCard :content="content" />
</template>
