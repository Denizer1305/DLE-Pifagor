<script setup lang="ts">
import { computed, ref } from "vue";

import DashboardActivityCard from "@/components/dashboard/cards/DashboardActivityCard.vue";
import DashboardAttentionCard from "@/components/dashboard/cards/DashboardAttentionCard.vue";
import DashboardOverviewCard from "@/components/dashboard/cards/DashboardOverviewCard.vue";
import DashboardTimelineCard from "@/components/dashboard/cards/DashboardTimelineCard.vue";
import DashboardPageScaffold from "@/components/dashboard/layout/DashboardPageScaffold.vue";
import DashboardCoursesSection from "@/components/dashboard/sections/DashboardCoursesSection.vue";
import DashboardHeroSection from "@/components/dashboard/sections/DashboardHeroSection.vue";
import DashboardStatsSection from "@/components/dashboard/sections/DashboardStatsSection.vue";

import { useDashboardLogout } from "@/composables/dashboard/useDashboardLogout";
import { useParentDashboard } from "@/modules/parent/composables/useParentDashboard";
import { useParentDashboardPresentation } from "@/modules/parent/composables/useParentDashboardPresentation";
import { useAuthStore } from "@/stores/auth.store";
import type { DashboardCreateItemKind } from "@/components/dashboard/types/dashboard.types";

const authStore = useAuthStore();
const userFullName = computed(() => authStore.userFullName);
const { logout } = useDashboardLogout();
const dashboardScaffold = ref<InstanceType<typeof DashboardPageScaffold> | null>(null);

const {
    model,
    errorMessage,
    isLoading,
    loadDashboard,
} = useParentDashboard(userFullName);

const {
    ui,
    scheduleContent,
    importantContent,
    activityContent,
    messagesContent,
    gradeRows,
} = useParentDashboardPresentation(model);

function reloadDashboard(): void {
    void loadDashboard();
}

function openDashboardCreateItem(kind: DashboardCreateItemKind): void {
    dashboardScaffold.value?.openCreateItem(kind);
}
</script>

<template>
    <DashboardPageScaffold
        ref="dashboardScaffold"
        :model="model"
        :is-loading="isLoading"
        :error-message="errorMessage"
        :loading-text="ui.loadingText"
        :error-title="ui.errorTitle"
        :retry-label="ui.retryLabel"
        :retry-icon="ui.retryIcon"
        @reload="reloadDashboard"
        @logout="logout"
    >
        <DashboardHeroSection :content="model.heroSection" />

        <DashboardStatsSection
            section-class="parent-dashboard-stats"
            :cards="model.stats"
        />

        <section class="dashboard-grid-2 parent-dashboard-work-grid">
            <DashboardTimelineCard
                :content="scheduleContent"
                :empty-icon="model.scheduleSection.emptyIcon"
                :empty-title="ui.emptyTitle"
                @create="openDashboardCreateItem"
            />

            <DashboardAttentionCard
                :content="importantContent"
                :empty-icon="model.notificationsSection.emptyIcon"
                :empty-title="ui.emptyTitle"
            />
        </section>

        <DashboardCoursesSection
            :content="model.coursesSection"
            :courses="model.courses"
            :empty-title="ui.emptyTitle"
            :filters="ui.courses.filters"
            section-class="parent-dashboard-courses-section"
        />

        <section class="dashboard-grid-3 parent-dashboard-bottom-grid">
            <DashboardActivityCard
                :content="activityContent"
                :empty-icon="model.activitySection.emptyIcon"
                :empty-title="ui.emptyTitle"
            />

            <DashboardOverviewCard
                :badge="model.gradesSection.badge"
                :icon="model.gradesSection.icon"
                :title="model.gradesSection.title"
                :text="model.gradesSection.text"
                :headers="ui.grades.headers"
                :rows="gradeRows"
                :empty-icon="model.gradesSection.emptyIcon"
                :empty-title="ui.emptyTitle"
                :empty-text="model.gradesSection.emptyText"
            />

            <DashboardActivityCard
                :content="messagesContent"
                :empty-icon="model.messagesSection.emptyIcon"
                :empty-title="ui.emptyTitle"
            />
        </section>
    </DashboardPageScaffold>
</template>
