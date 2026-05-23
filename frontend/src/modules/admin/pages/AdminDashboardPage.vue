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

import { useAdminDashboard } from "@/modules/admin/composables/useAdminDashboard";
import { adminDashboardPageUi } from "@/modules/admin/data/admin-dashboard-page.data";
import { redirectAfterLogout } from "@/modules/auth/utils/auth-redirect.utils";
import { useAuthStore } from "@/stores/auth.store";

const router = useRouter();
const authStore = useAuthStore();
const ui = adminDashboardPageUi;

const {
    errorMessage,
    isLoading,
    loadDashboard,
    pageModel,
    viewModel,
} = useAdminDashboard();

const featuredStatCard = computed<DashboardStatsCardContent>(() => {
    return {
        key: "featured",
        icon: pageModel.value.featuredStat.icon,
        title: pageModel.value.featuredStat.title,
        value: `${pageModel.value.featuredStat.value}%`,
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
        badge: pageModel.value.dayCard.title,
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

const criticalContent = computed<DashboardCardSectionContent>(() => {
    return {
        badge: ui.critical.badge,
        icon: ui.critical.icon,
        title: ui.critical.title,
        text: ui.critical.text,
        emptyText: ui.critical.emptyText,
        items: pageModel.value.criticalItems.map((item) => {
            return {
                id: item.title,
                icon: item.icon,
                title: item.title,
                text: item.text,
            };
        }),
    };
});

const participantCards = computed<DashboardCourseCardContent[]>(() => {
    return pageModel.value.participants.map((participant) => {
        return {
            id: participant.title,
            icon: participant.icon,
            status: participant.status,
            statusVariant: "active",
            title: participant.title,
            description: participant.text,
            meta: [
                {
                    value: participant.firstValue,
                    label: participant.firstLabel,
                },
                {
                    value: participant.secondValue,
                    label: participant.secondLabel,
                },
            ],
            progress: participant.progress,
            progressLabel: participant.progressLabel,
            actions: participant.actions.map((action, index) => {
                return {
                    label: action,
                    href: "#",
                    variant: index === 0 ? "primary" : "secondary",
                };
            }),
        };
    });
});

const recentEventsContent = computed<DashboardCardSectionContent>(() => {
    return {
        badge: ui.events.badge,
        icon: ui.events.icon,
        title: ui.events.title,
        text: ui.events.text,
        emptyText: ui.events.emptyText,
        items: pageModel.value.recentEvents.map((event) => {
            return {
                id: event.title,
                icon: event.icon,
                title: event.title,
                text: event.text,
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

        <section class="admin-dashboard-stat-grid">
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

        <DashboardTimelineCard
            :content="planContent"
            card-class="admin-dashboard-plan-card"
            :empty-icon="ui.plan.emptyIcon"
            :empty-title="ui.emptyTitle"
        />

        <DashboardAttentionCard
            :content="criticalContent"
            card-class="admin-dashboard-critical-card"
            :empty-icon="ui.critical.emptyIcon"
            :empty-title="ui.emptyTitle"
        />

        <section class="admin-dashboard-section">
            <DashboardSectionHead
                :badge="ui.participants.badge"
                :icon="ui.participants.icon"
                :title="ui.participants.title"
            />

            <div class="dashboard-courses-grid">
                <DashboardCourseCard
                    v-for="participant in participantCards"
                    :key="participant.id"
                    :course="participant"
                />
            </div>
        </section>

        <section class="dashboard-grid-3 admin-dashboard-bottom-grid">
            <DashboardActivityCard
                :content="recentEventsContent"
                :empty-icon="ui.events.emptyIcon"
                :empty-title="ui.emptyTitle"
            />

            <article class="dashboard-card">
                <div class="dashboard-card-inner">
                    <DashboardSectionHead
                        :badge="ui.overview.badge"
                        :icon="ui.overview.icon"
                        :title="ui.overview.title"
                        :text="ui.overview.text"
                    />

                    <div
                        v-if="pageModel.overviewRows.length"
                        class="dashboard-journal-table"
                    >
                        <div class="dashboard-journal-row head">
                            <span
                                v-for="header in ui.overview.headers"
                                :key="header"
                            >
                                {{ header }}
                            </span>
                        </div>

                        <div
                            v-for="row in pageModel.overviewRows"
                            :key="row.section"
                            class="dashboard-journal-row"
                        >
                            <span>{{ row.section }}</span>
                            <span>{{ row.state }}</span>
                            <span>{{ row.value }}</span>
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
                        :icon="ui.overview.emptyIcon"
                        :title="ui.emptyTitle"
                        :text="ui.overview.emptyText"
                    />

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
                </div>
            </article>

            <DashboardAiCard :content="pageModel.ai" />
        </section>
    </DashboardPageScaffold>
</template>
