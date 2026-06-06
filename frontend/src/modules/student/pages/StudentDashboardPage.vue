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
import { useStudentDashboard } from "@/modules/student/composables/useStudentDashboard";
import { useStudentDashboardPresentation } from "@/modules/student/composables/useStudentDashboardPresentation";
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
} = useStudentDashboard(userFullName);

const {
    ui,
    scheduleContent,
    assignmentsContent,
    activityContent,
    goalsContent,
    gradeRows,
} = useStudentDashboardPresentation(model);

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
            section-class="student-dashboard-stats"
            :cards="model.stats"
        />

        <section class="dashboard-grid-2 student-dashboard-work-grid">
            <DashboardTimelineCard
                :content="scheduleContent"
                :empty-icon="model.scheduleSection.emptyIcon"
                :empty-title="ui.emptyTitle"
                @create="openDashboardCreateItem"
            />

            <DashboardActivityCard
                :content="assignmentsContent"
                :empty-icon="model.assignmentsSection.emptyIcon"
                :empty-title="ui.emptyTitle"
            />
        </section>

        <DashboardCoursesSection
            :content="model.coursesSection"
            :courses="model.courses"
            :empty-title="ui.emptyTitle"
            section-class="student-dashboard-courses-section"
        />

        <section class="dashboard-grid-3 student-dashboard-bottom-grid">
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

            <DashboardAttentionCard
                :content="goalsContent"
                :empty-icon="model.goalsSection.emptyIcon"
                :empty-title="ui.emptyTitle"
            />
        </section>
    </DashboardPageScaffold>
</template>
