<script setup lang="ts">
import { computed } from "vue";

import DashboardPageNav from "@/components/dashboard/shared/DashboardPageNav.vue";
import type {
    OrganizationNavigationItem,
    OrganizationPageHeaderView,
    OrganizationSummaryCardView,
} from "../../types";

interface Props {
    header: OrganizationPageHeaderView;
    navigation: OrganizationNavigationItem[];
    summary: OrganizationSummaryCardView[];
}

const props = defineProps<Props>();

const iconClassMap: Record<string, string> = {
    "book-open": "fas fa-book-open",
    "building-2": "fas fa-building",
    "graduation-cap": "fas fa-user-graduate",
    inbox: "fas fa-inbox",
    "layers-3": "fas fa-layer-group",
    "library-big": "fas fa-book",
    "user-check": "fas fa-user-check",
    "users-round": "fas fa-users",
};

const primaryNavigationKeys = new Set([
    "organizations",
    "departments",
    "studyGroups",
    "subjects",
]);

const navItems = computed(() => {
    return props.navigation
        .filter((item) => primaryNavigationKeys.has(item.key))
        .map((item) => ({
            key: item.key,
            label: item.label,
            icon: iconClassMap[item.icon] ?? "fas fa-circle",
            to: {
                name: item.routeName,
            },
            badge: item.badge,
        }));
});

const navActions = computed(() => {
    return props.navigation
        .filter((item) => !primaryNavigationKeys.has(item.key))
        .map((item) => ({
        key: item.key,
        label: item.label,
        icon: iconClassMap[item.icon] ?? "fas fa-circle",
        to: {
            name: item.routeName,
        },
        badge: item.badge,
        }));
});

const visibleSummary = computed(() => {
    return props.summary.filter((item) => item.value !== "—");
});

function getSummaryIcon(icon: string): string {
    return iconClassMap[icon] ?? "fas fa-chart-simple";
}
</script>

<template>
    <section class="org-dashboard-page fade-in visible">
        <header class="admin-users-hero org-dashboard-hero">
            <span class="dashboard-badge">
                <i class="fas fa-building-columns"></i>
                {{ header.eyebrow }}
            </span>

            <h1>{{ header.title }}</h1>
            <p>{{ header.description }}</p>
        </header>

        <DashboardPageNav
            v-if="navItems.length > 1 || navActions.length"
            :items="navItems"
            :actions="navActions"
            aria-label="Навигация по образовательным организациям"
        />

        <div
            v-if="visibleSummary.length"
            class="admin-users-summary org-dashboard-summary"
        >
            <article
                v-for="item in visibleSummary"
                :key="item.key"
                :class="`is-${item.tone}`"
            >
                <i :class="getSummaryIcon(item.icon)"></i>
                <span>{{ item.label }}</span>
                <strong>{{ item.value }}</strong>
                <small>{{ item.meta }}</small>
            </article>
        </div>

        <RouterView />
    </section>
</template>
