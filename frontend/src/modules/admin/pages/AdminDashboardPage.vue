<script setup lang="ts">
import { RouterLink } from "vue-router";
import { ref } from "vue";

import DashboardActivityCard from "@/components/dashboard/cards/DashboardActivityCard.vue";
import DashboardAiCard from "@/components/dashboard/cards/DashboardAiCard.vue";
import DashboardAttentionCard from "@/components/dashboard/cards/DashboardAttentionCard.vue";
import DashboardOverviewCard from "@/components/dashboard/cards/DashboardOverviewCard.vue";
import DashboardTimelineCard from "@/components/dashboard/cards/DashboardTimelineCard.vue";
import DashboardPageScaffold from "@/components/dashboard/layout/DashboardPageScaffold.vue";
import DashboardCoursesSection from "@/components/dashboard/sections/DashboardCoursesSection.vue";
import DashboardHeroSection from "@/components/dashboard/sections/DashboardHeroSection.vue";
import DashboardStatsSection from "@/components/dashboard/sections/DashboardStatsSection.vue";

import { useDashboardLogout } from "@/composables/dashboard/useDashboardLogout";
import { useAdminDashboard } from "@/modules/admin/composables/useAdminDashboard";
import { useAdminDashboardPresentation } from "@/modules/admin/composables/useAdminDashboardPresentation";
import type { DashboardCreateItemKind } from "@/components/dashboard/types/dashboard.types";

const { logout } = useDashboardLogout();
const dashboardScaffold = ref<InstanceType<typeof DashboardPageScaffold> | null>(null);

const {
    errorMessage,
    isLoading,
    loadDashboard,
    pageModel,
    viewModel,
} = useAdminDashboard();

const {
    ui,
    featuredStatCard,
    compactStatCards,
    planContent,
    criticalContent,
    participantCards,
    recentEventsContent,
    overviewRows,
} = useAdminDashboardPresentation(pageModel);

function openDashboardCreateItem(kind: DashboardCreateItemKind): void {
    dashboardScaffold.value?.openCreateItem(kind);
}
</script>

<template>
    <DashboardPageScaffold
        ref="dashboardScaffold"
        :model="viewModel"
        :is-loading="isLoading"
        :error-message="errorMessage"
        :loading-text="ui.loadingText"
        :error-title="ui.errorTitle"
        :retry-label="ui.retryLabel"
        :retry-icon="ui.retryIcon"
        @reload="loadDashboard"
        @logout="logout"
    >
        <DashboardHeroSection :content="pageModel.heroSection" />

        <DashboardStatsSection
            section-class="admin-dashboard-stat-grid"
            :featured-card="featuredStatCard"
            :cards="compactStatCards"
            :progress-label="ui.progressLabel"
        />

        <DashboardTimelineCard
            :content="planContent"
            card-class="admin-dashboard-plan-card"
            :empty-icon="ui.plan.emptyIcon"
            :empty-title="ui.emptyTitle"
            @create="openDashboardCreateItem"
        />

        <DashboardAttentionCard
            :content="criticalContent"
            card-class="admin-dashboard-critical-card"
            :empty-icon="ui.critical.emptyIcon"
            :empty-title="ui.emptyTitle"
        />

        <DashboardCoursesSection
            :content="ui.participants"
            :courses="participantCards"
            :empty-title="ui.emptyTitle"
            section-class="admin-dashboard-section"
        />

        <section class="dashboard-grid-3 admin-dashboard-bottom-grid">
            <DashboardActivityCard
                :content="recentEventsContent"
                :empty-icon="ui.events.emptyIcon"
                :empty-title="ui.emptyTitle"
            />

            <DashboardOverviewCard
                :badge="ui.overview.badge"
                :icon="ui.overview.icon"
                :title="ui.overview.title"
                :text="ui.overview.text"
                :headers="ui.overview.headers"
                :rows="overviewRows"
                :empty-icon="ui.overview.emptyIcon"
                :empty-title="ui.emptyTitle"
                :empty-text="ui.overview.emptyText"
            >
                <template #actions>
                    <div class="dashboard-course-actions admin-dashboard-table-actions">
                        <RouterLink
                            class="dashboard-course-btn primary"
                            :to="{ name: 'admin-analytics' }"
                        >
                            {{ ui.overview.analyticsLabel }}
                        </RouterLink>

                        <a
                            class="dashboard-course-btn"
                            href="#"
                        >
                            {{ ui.overview.reportLabel }}
                        </a>
                    </div>
                </template>
            </DashboardOverviewCard>

            <DashboardAiCard :content="pageModel.ai" />
        </section>
    </DashboardPageScaffold>
</template>
