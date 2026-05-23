<script setup lang="ts">
import { RouterLink, useRoute } from "vue-router";

import type { DashboardNavigationItem } from "@/components/dashboard/types/dashboard.types";

interface Props {
    navigation: DashboardNavigationItem[];
}

const props = defineProps<Props>();
const route = useRoute();

function isActive(item: DashboardNavigationItem): boolean {
    if (typeof item.to === "string") {
        return item.exact
            ? route.path === item.to
            : route.path.startsWith(item.to);
    }

    if ("name" in item.to && item.to.name) {
        return route.name === item.to.name;
    }

    if ("path" in item.to && item.to.path) {
        return item.exact
            ? route.path === item.to.path
            : route.path.startsWith(item.to.path);
    }

    return false;
}
</script>

<template>
    <nav class="sidebar-nav">
        <RouterLink
            v-for="item in props.navigation"
            :key="item.key"
            class="sidebar-nav-link"
            :class="{ 'is-active': isActive(item) }"
            :to="item.to"
        >
            <span class="sidebar-nav-icon">
                <i :class="item.icon"></i>
            </span>

            <span class="sidebar-nav-copy">
                <strong>{{ item.label }}</strong>
                <span>{{ item.description }}</span>
            </span>

            <span
                v-if="item.badge !== undefined && item.badge !== null"
                class="sidebar-nav-badge"
            >
                {{ item.badge }}
            </span>
        </RouterLink>
    </nav>
</template>
