<script setup lang="ts">
import { RouterLink } from "vue-router";

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
import { useTeacherDashboard } from "@/modules/teacher/composables/useTeacherDashboard";
import { useTeacherDashboardPresentation } from "@/modules/teacher/composables/useTeacherDashboardPresentation";

const { logout } = useDashboardLogout();

const {
    errorMessage,
    isLoading,
    loadDashboard,
    pageModel,
    viewModel,
} = useTeacherDashboard();

const {
    ui,
    featuredStatCard,
    compactStatCards,
    planContent,
    attentionContent,
    courseCards,
    activityContent,
    journalRows,
} = useTeacherDashboardPresentation(pageModel);
</script>

<template>
    <DashboardPageScaffold
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
            section-class="teacher-dashboard-stats"
            :featured-card="featuredStatCard"
            :cards="compactStatCards"
            :progress-label="ui.progressLabel"
        />

        <section class="dashboard-grid-2">
            <DashboardTimelineCard
                :content="planContent"
                card-class="teacher-dashboard-plan-card"
                :empty-icon="ui.plan.emptyIcon"
                :empty-title="ui.emptyTitle"
            />

            <DashboardAttentionCard
                :content="attentionContent"
                card-class="teacher-dashboard-attention-card"
                :empty-icon="ui.attention.emptyIcon"
                :empty-title="ui.emptyTitle"
            />
        </section>

        <DashboardCoursesSection
            :content="ui.courses"
            :courses="courseCards"
            :empty-title="ui.emptyTitle"
            :filters="ui.courses.filters"
            section-class="teacher-dashboard-courses-section"
        />

        <section class="dashboard-grid-3 teacher-dashboard-bottom-grid">
            <DashboardActivityCard
                :content="activityContent"
                :empty-icon="ui.activity.emptyIcon"
                :empty-title="ui.emptyTitle"
            />

            <DashboardOverviewCard
                :badge="ui.journal.badge"
                :icon="ui.journal.icon"
                :title="ui.journal.title"
                :text="ui.journal.text"
                :headers="ui.journal.headers"
                :rows="journalRows"
                :empty-icon="ui.journal.emptyIcon"
                :empty-title="ui.emptyTitle"
                :empty-text="ui.journal.emptyText"
            >
                <template #actions>
                    <div
                        v-if="journalRows.length"
                        class="dashboard-course-actions dashboard-journal-actions"
                    >
                        <RouterLink
                            class="dashboard-course-btn primary"
                            :to="{ name: 'teacher-journal' }"
                        >
                            {{ ui.journal.openLabel }}
                        </RouterLink>

                        <RouterLink
                            class="dashboard-course-btn"
                            :to="{ name: 'teacher-analytics' }"
                        >
                            {{ ui.journal.analyticsLabel }}
                        </RouterLink>
                    </div>
                </template>
            </DashboardOverviewCard>

            <DashboardAiCard :content="pageModel.ai" />
        </section>
    </DashboardPageScaffold>
</template>
