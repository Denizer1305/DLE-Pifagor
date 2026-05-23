<script setup lang="ts">
import { computed } from "vue";
import { useRouter } from "vue-router";

import DashboardActivityCard from "@/components/dashboard/cards/DashboardActivityCard.vue";
import DashboardAttentionCard from "@/components/dashboard/cards/DashboardAttentionCard.vue";
import DashboardCourseCard from "@/components/dashboard/cards/DashboardCourseCard.vue";
import DashboardStatsCard from "@/components/dashboard/cards/DashboardStatsCard.vue";
import DashboardTimelineCard from "@/components/dashboard/cards/DashboardTimelineCard.vue";
import DashboardPageScaffold from "@/components/dashboard/layout/DashboardPageScaffold.vue";
import DashboardHeroSection from "@/components/dashboard/sections/DashboardHeroSection.vue";
import DashboardEmptyState from "@/components/dashboard/shared/DashboardEmptyState.vue";
import DashboardSectionHead from "@/components/dashboard/shared/DashboardSectionHead.vue";
import type {
    DashboardCardSectionContent,
    DashboardTimelineContent,
} from "@/components/dashboard/types/dashboard.types";

import { useStudentDashboard } from "@/modules/student/composables/useStudentDashboard";
import { studentDashboardPageUi } from "@/modules/student/data/student-dashboard.data";
import { redirectAfterLogout } from "@/modules/auth/utils/auth-redirect.utils";
import { useAuthStore } from "@/stores/auth.store";

const router = useRouter();
const authStore = useAuthStore();
const userFullName = computed(() => authStore.userFullName);
const ui = studentDashboardPageUi;

const {
    model,
    errorMessage,
    isLoading,
    loadDashboard,
} = useStudentDashboard(userFullName);

const scheduleContent = computed<DashboardTimelineContent>(() => {
    return {
        badge: model.value.scheduleSection.badge,
        icon: model.value.scheduleSection.icon,
        title: model.value.scheduleSection.title,
        text: model.value.scheduleSection.text,
        emptyText: model.value.scheduleSection.emptyText,
        items: model.value.schedule,
    };
});

const assignmentsContent = computed<DashboardCardSectionContent>(() => {
    return createCardSection(
        model.value.assignmentsSection,
        model.value.assignments,
    );
});

const activityContent = computed<DashboardCardSectionContent>(() => {
    return createCardSection(
        model.value.activitySection,
        model.value.activityItems,
    );
});

const goalsContent = computed<DashboardCardSectionContent>(() => {
    return createCardSection(
        model.value.goalsSection,
        model.value.goals,
    );
});

function createCardSection(
    section: typeof model.value.assignmentsSection,
    items: DashboardCardSectionContent["items"],
): DashboardCardSectionContent {
    return {
        badge: section.badge,
        icon: section.icon,
        title: section.title,
        text: section.text,
        emptyText: section.emptyText,
        items,
    };
}

function reloadDashboard(): void {
    void loadDashboard();
}

async function logout(): Promise<void> {
    await authStore.logout();
    await redirectAfterLogout(router);
}
</script>

<template>
    <DashboardPageScaffold
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

        <section class="dashboard-stats-grid student-dashboard-stats fade-in visible">
            <DashboardStatsCard
                v-for="stat in model.stats"
                :key="stat.key"
                :card="stat"
            />
        </section>

        <section class="dashboard-grid-2 student-dashboard-work-grid">
            <DashboardTimelineCard
                :content="scheduleContent"
                :empty-icon="model.scheduleSection.emptyIcon"
                :empty-title="ui.emptyTitle"
            />

            <DashboardActivityCard
                :content="assignmentsContent"
                :empty-icon="model.assignmentsSection.emptyIcon"
                :empty-title="ui.emptyTitle"
            />
        </section>

        <section class="student-dashboard-courses-section fade-in visible">
            <DashboardSectionHead
                :badge="model.coursesSection.badge"
                :icon="model.coursesSection.icon"
                :title="model.coursesSection.title"
                :text="model.coursesSection.text"
            />

            <div
                v-if="model.courses.length"
                class="dashboard-courses-grid"
            >
                <DashboardCourseCard
                    v-for="course in model.courses"
                    :key="course.id"
                    :course="course"
                />
            </div>

            <DashboardEmptyState
                v-else
                :icon="model.coursesSection.emptyIcon"
                :title="ui.emptyTitle"
                :text="model.coursesSection.emptyText"
            />
        </section>

        <section class="dashboard-grid-3 student-dashboard-bottom-grid">
            <DashboardActivityCard
                :content="activityContent"
                :empty-icon="model.activitySection.emptyIcon"
                :empty-title="ui.emptyTitle"
            />

            <article class="dashboard-card fade-in visible">
                <div class="dashboard-card-inner">
                    <DashboardSectionHead
                        :badge="model.gradesSection.badge"
                        :icon="model.gradesSection.icon"
                        :title="model.gradesSection.title"
                        :text="model.gradesSection.text"
                    />

                    <div
                        v-if="model.gradeRows.length"
                        class="dashboard-journal-table"
                    >
                        <div class="dashboard-journal-row head">
                            <span
                                v-for="header in ui.grades.headers"
                                :key="header"
                            >
                                {{ header }}
                            </span>
                        </div>

                        <div
                            v-for="row in model.gradeRows"
                            :key="row.id"
                            class="dashboard-journal-row"
                        >
                            <span>{{ row.subject }}</span>
                            <span>{{ row.work }}</span>
                            <span>{{ row.grade }}</span>
                            <span
                                class="dashboard-journal-status"
                                :class="{ warn: row.warning }"
                            >
                                {{ row.status }}
                            </span>
                        </div>
                    </div>

                    <DashboardEmptyState
                        v-else
                        :icon="model.gradesSection.emptyIcon"
                        :title="ui.emptyTitle"
                        :text="model.gradesSection.emptyText"
                    />
                </div>
            </article>

            <DashboardAttentionCard
                :content="goalsContent"
                :empty-icon="model.goalsSection.emptyIcon"
                :empty-title="ui.emptyTitle"
            />
        </section>
    </DashboardPageScaffold>
</template>
