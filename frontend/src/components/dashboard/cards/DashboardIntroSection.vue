<script setup lang="ts">
import { RouterLink } from "vue-router";

import type {
    DashboardDayCardContent,
    DashboardIntroContent,
} from "@/components/dashboard/types/dashboard.types";

interface Props {
    content: DashboardIntroContent;
    dayCard?: DashboardDayCardContent;
}

defineProps<Props>();

function getActionClass(variant?: string): string[] {
    return [
        "dashboard-quick-btn",
        variant === "primary" ? "primary" : "",
    ].filter(Boolean);
}
</script>

<template>
    <section class="dashboard-intro fade-in visible">
        <div class="dashboard-intro-grid">
            <div class="dashboard-intro-content">
                <div class="dashboard-intro-badges">
                    <span
                        v-for="badge in content.badges"
                        :key="badge.label"
                        class="dashboard-intro-badge"
                    >
                        <i :class="badge.icon"></i>
                        {{ badge.label }}
                    </span>
                </div>

                <h1 class="dashboard-intro-title">
                    {{ content.title }}
                </h1>

                <p class="dashboard-intro-text">
                    {{ content.text }}
                </p>

                <div
                    v-if="content.actions.length"
                    class="dashboard-quick-actions"
                >
                    <template
                        v-for="action in content.actions"
                        :key="action.label"
                    >
                        <RouterLink
                            v-if="action.to"
                            :to="action.to"
                            :class="getActionClass(action.variant)"
                        >
                            <i
                                v-if="action.icon"
                                :class="action.icon"
                            ></i>
                            {{ action.label }}
                        </RouterLink>

                        <a
                            v-else
                            :href="action.href || '#'"
                            :class="getActionClass(action.variant)"
                        >
                            <i
                                v-if="action.icon"
                                :class="action.icon"
                            ></i>
                            {{ action.label }}
                        </a>
                    </template>
                </div>
            </div>

            <div
                v-if="dayCard"
                class="dashboard-intro-side"
            >
                <div class="dashboard-day-card">
                    <div class="dashboard-card-topline">
                        <i :class="dayCard.icon"></i>
                        {{ dayCard.badge }}
                    </div>

                    <h3 class="dashboard-day-title">
                        {{ dayCard.title }}
                    </h3>

                    <p class="dashboard-day-text">
                        {{ dayCard.text }}
                    </p>

                    <div class="dashboard-day-stats">
                        <div
                            v-for="stat in dayCard.stats"
                            :key="stat.label"
                            class="dashboard-day-stat"
                        >
                            <strong>{{ stat.value }}</strong>
                            <span>{{ stat.label }}</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>