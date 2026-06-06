<script setup lang="ts">
import { RouterLink } from "vue-router";

import type { DashboardHeroSectionContent } from "@/components/dashboard/types/dashboard.types";

interface Props {
    content: DashboardHeroSectionContent;
}

defineProps<Props>();

function getActionClass(variant?: string): string[] {
    return [
        "dashboard-quick-btn",
        variant === "secondary" || variant === "light" ? "light" : "",
    ].filter(Boolean);
}

function toRoute(routeName: string) {
    return {
        name: routeName,
    };
}
</script>

<template>
    <section class="dashboard-intro fade-in visible">
        <div class="dashboard-intro-grid">
            <div class="dashboard-intro-copy">
                <div
                    v-if="content.hero.badges.length"
                    class="dashboard-intro-badges"
                >
                    <span
                        v-for="badge in content.hero.badges"
                        :key="badge.label"
                        class="dashboard-intro-badge"
                    >
                        <i :class="badge.icon"></i>
                        {{ badge.label }}
                    </span>
                </div>

                <h1 class="dashboard-intro-title">
                    {{ content.hero.title }}
                </h1>

                <p class="dashboard-intro-text">
                    {{ content.hero.text }}
                </p>

                <div
                    v-if="content.hero.actions.length"
                    class="dashboard-quick-actions"
                >
                    <RouterLink
                        v-for="action in content.hero.actions"
                        :key="action.label"
                        :to="toRoute(action.routeName)"
                        :class="getActionClass(action.variant)"
                    >
                        <i :class="action.icon"></i>
                        {{ action.label }}
                    </RouterLink>
                </div>
            </div>

            <div class="dashboard-intro-side">
                <div class="dashboard-day-card">
                    <div class="dashboard-card-topline">
                        <i :class="content.dayCard.icon"></i>
                        {{ content.dayCard.badge }}
                    </div>

                    <h3 class="dashboard-day-title">
                        {{ content.dayCard.title }}
                    </h3>

                    <p class="dashboard-day-text">
                        {{ content.dayCard.text }}
                    </p>

                    <div
                        v-if="content.dayCard.stats.length"
                        class="dashboard-day-stats"
                    >
                        <div
                            v-for="stat in content.dayCard.stats"
                            :key="stat.label"
                            class="dashboard-day-stat"
                        >
                            <strong>{{ stat.value }}</strong>
                            <span>{{ stat.label }}</span>
                        </div>
                    </div>
                </div>

                <div
                    v-if="Array.isArray(content.miniPlan)"
                    class="dashboard-schedule-card"
                >
                    <div class="dashboard-card-topline">
                        <i :class="content.miniPlanIcon || 'fas fa-clock'"></i>
                        {{ content.miniPlanTitle }}
                    </div>

                    <div
                        v-if="content.miniPlan.length"
                        class="dashboard-schedule-list"
                    >
                        <div
                            v-for="item in content.miniPlan"
                            :key="`${item.time}-${item.title}`"
                            class="dashboard-schedule-item"
                        >
                            <div class="dashboard-schedule-time">
                                {{ item.time }}
                            </div>

                            <div class="dashboard-schedule-copy">
                                <strong>{{ item.title }}</strong>
                                <span>{{ item.text }}</span>
                            </div>
                        </div>
                    </div>

                    <div
                        v-else
                        class="dashboard-panel-empty"
                    >
                        {{ content.miniPlanEmptyText || "План пока не заполнен. Добавьте событие или заметку." }}
                    </div>
                </div>

                <slot name="side-extra"></slot>
            </div>
        </div>
    </section>
</template>
