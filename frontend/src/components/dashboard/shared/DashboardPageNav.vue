<script setup lang="ts">
import { computed } from "vue";
import { RouterLink, useRoute, type RouteLocationRaw } from "vue-router";

interface DashboardPageNavItem {
    key: string;
    label: string;
    icon: string;
    to: RouteLocationRaw;
    badge?: string | number;
    exact?: boolean;
}

interface Props {
    items: DashboardPageNavItem[];
    actions?: DashboardPageNavItem[];
    ariaLabel?: string;
}

const props = withDefaults(defineProps<Props>(), {
    actions: () => [],
    ariaLabel: "Навигация страницы",
});

const route = useRoute();

const hasActions = computed(() => props.actions.length > 0);

function isActive(item: DashboardPageNavItem): boolean {
    if (typeof item.to === "object" && "name" in item.to) {
        return route.name === item.to.name;
    }

    if (typeof item.to === "string") {
        return item.exact ? route.path === item.to : route.path.startsWith(item.to);
    }

    return false;
}
</script>

<template>
    <nav
        class="dashboard-page-nav"
        :aria-label="ariaLabel"
    >
        <div class="dashboard-page-nav__links">
            <RouterLink
                v-for="item in items"
                :key="item.key"
                class="dashboard-page-nav__item"
                :class="{ 'is-active': isActive(item) }"
                :to="item.to"
            >
                <i :class="item.icon"></i>
                <span>{{ item.label }}</span>
                <mark v-if="item.badge !== undefined && item.badge !== null">
                    {{ item.badge }}
                </mark>
            </RouterLink>
        </div>

        <div
            v-if="hasActions"
            class="dashboard-page-nav__actions"
        >
            <RouterLink
                v-for="action in actions"
                :key="action.key"
                class="dashboard-page-nav__action"
                :to="action.to"
            >
                <i :class="action.icon"></i>
                <span>{{ action.label }}</span>
                <mark v-if="action.badge !== undefined && action.badge !== null">
                    {{ action.badge }}
                </mark>
            </RouterLink>
        </div>
    </nav>
</template>
