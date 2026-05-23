<script setup lang="ts">
import { computed } from "vue";
import { RouterLink, useRouter } from "vue-router";

import DashboardActivityCard from "@/components/dashboard/cards/DashboardActivityCard.vue";
import DashboardAiCard from "@/components/dashboard/cards/DashboardAiCard.vue";
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
    DashboardCourseCardContent,
    DashboardStatsCardContent,
    DashboardTimelineContent,
} from "@/components/dashboard/types/dashboard.types";

import { redirectAfterLogout } from "@/modules/auth/utils/auth-redirect.utils";
import { useTeacherDashboard } from "@/modules/teacher/composables/useTeacherDashboard";
import { teacherDashboardPageUi } from "@/modules/teacher/data/teacher-dashboard.data";
import { useAuthStore } from "@/stores/auth.store";

const router = useRouter();
const authStore = useAuthStore();
const ui = teacherDashboardPageUi;

const {
    errorMessage,
    isLoading,
    loadDashboard,
    pageModel,
    viewModel,
} = useTeacherDashboard();

const featuredStatCard = computed<DashboardStatsCardContent>(() => {
    return {
        key: "featured",
        icon: pageModel.value.featuredStat.icon,
        title: pageModel.value.featuredStat.title,
        value: pageModel.value.featuredStat.value,
        text: pageModel.value.featuredStat.label,
        progress: pageModel.value.featuredStat.progress,
    };
});

const compactStatCards = computed<DashboardStatsCardContent[]>(() => {
    return pageModel.value.compactStats.map((stat) => {
        return {
            key: stat.key,
            icon: stat.icon,
            title: stat.title,
            value: stat.value,
            text: stat.text,
        };
    });
});

const planContent = computed<DashboardTimelineContent>(() => {
    return {
        badge: ui.plan.badge,
        icon: ui.plan.icon,
        title: ui.plan.title,
        text: ui.plan.text,
        emptyText: ui.plan.emptyText,
        items: pageModel.value.planItems.map((item) => {
            return {
                id: `${item.time}-${item.title}`,
                time: item.time,
                title: item.title,
                text: item.text,
            };
        }),
    };
});

const attentionContent = computed<DashboardCardSectionContent>(() => {
    return {
        badge: ui.attention.badge,
        icon: ui.attention.icon,
        title: ui.attention.title,
        text: ui.attention.text,
        emptyText: ui.attention.emptyText,
        items: pageModel.value.attentionItems.map((item) => {
            return {
                id: item.id,
                icon: item.icon,
                title: item.title,
                text: item.text,
                tone: item.tone,
            };
        }),
    };
});

const courseCards = computed<DashboardCourseCardContent[]>(() => {
    return pageModel.value.courses.map((course) => {
        return {
            id: course.id,
            icon: course.icon,
            status: course.status,
            statusVariant: course.statusVariant,
            title: course.title,
            description: course.description,
            meta: [
                {
                    value: course.modulesCount,
                    label: ui.courses.meta.modules,
                },
                {
                    value: course.studentsCount,
                    label: ui.courses.meta.students,
                },
            ],
            progress: course.progress,
            progressLabel: ui.courses.progressLabel,
            actions: [
                {
                    label: ui.courses.actions.open,
                    to: {
                        name: "teacher-course-detail",
                        params: {
                            id: course.id,
                        },
                    },
                    variant: "primary",
                },
                {
                    label: ui.courses.actions.edit,
                    to: {
                        name: "teacher-course-edit",
                        params: {
                            id: course.id,
                        },
                    },
                },
                {
                    label: ui.courses.actions.analytics,
                    to: {
                        name: "teacher-course-analytics",
                        params: {
                            id: course.id,
                        },
                    },
                },
            ],
        };
    });
});

const activityContent = computed<DashboardCardSectionContent>(() => {
    return {
        badge: ui.activity.badge,
        icon: ui.activity.icon,
        title: ui.activity.title,
        text: ui.activity.text,
        emptyText: ui.activity.emptyText,
        items: pageModel.value.activityItems.map((item) => {
            return {
                id: item.id,
                icon: item.icon,
                title: item.title,
                text: item.text,
                tone: item.tone,
            };
        }),
    };
});

async function logout(): Promise<void> {
    await authStore.logout();
    await redirectAfterLogout(router);
}
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

        <section class="dashboard-stats-grid teacher-dashboard-stats fade-in visible">
            <DashboardStatsCard
                :card="featuredStatCard"
                is-featured
                :progress-label="ui.progressLabel"
            />

            <DashboardStatsCard
                v-for="card in compactStatCards"
                :key="card.key"
                :card="card"
            />
        </section>

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

        <section class="teacher-dashboard-courses-section fade-in visible">
            <DashboardSectionHead
                :badge="ui.courses.badge"
                :icon="ui.courses.icon"
                :title="ui.courses.title"
                :text="ui.courses.text"
            >
                <template #actions>
                    <div class="dashboard-inline-actions">
                        <button
                            v-for="(filter, index) in ui.courses.filters"
                            :key="filter"
                            class="dashboard-filter-chip"
                            :class="{ 'is-active': index === 0 }"
                            type="button"
                        >
                            {{ filter }}
                        </button>
                    </div>
                </template>
            </DashboardSectionHead>

            <div
                v-if="courseCards.length"
                class="dashboard-courses-grid"
            >
                <DashboardCourseCard
                    v-for="course in courseCards"
                    :key="course.id"
                    :course="course"
                />
            </div>

            <DashboardEmptyState
                v-else
                :icon="ui.courses.emptyIcon"
                :title="ui.emptyTitle"
                :text="ui.courses.emptyText"
            />
        </section>

        <section class="dashboard-grid-3 teacher-dashboard-bottom-grid">
            <DashboardActivityCard
                :content="activityContent"
                :empty-icon="ui.activity.emptyIcon"
                :empty-title="ui.emptyTitle"
            />

            <article class="dashboard-card fade-in visible">
                <div class="dashboard-card-inner">
                    <DashboardSectionHead
                        :badge="ui.journal.badge"
                        :icon="ui.journal.icon"
                        :title="ui.journal.title"
                        :text="ui.journal.text"
                    />

                    <div
                        v-if="pageModel.journalRows.length"
                        class="dashboard-journal-table"
                    >
                        <div class="dashboard-journal-row head">
                            <span
                                v-for="header in ui.journal.headers"
                                :key="header"
                            >
                                {{ header }}
                            </span>
                        </div>

                        <div
                            v-for="row in pageModel.journalRows"
                            :key="row.id"
                            class="dashboard-journal-row"
                        >
                            <span>{{ row.student }}</span>
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
                        :icon="ui.journal.emptyIcon"
                        :title="ui.emptyTitle"
                        :text="ui.journal.emptyText"
                    />

                    <div
                        v-if="pageModel.journalRows.length"
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
                </div>
            </article>

            <DashboardAiCard :content="pageModel.ai" />
        </section>
    </DashboardPageScaffold>
</template>
