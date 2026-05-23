<script setup lang="ts">
import { RouterLink } from "vue-router";

import type { DashboardAction } from "@/components/dashboard/types/dashboard.types";

interface Props {
    action: DashboardAction;
    mode?: "button" | "card";
}

defineProps<Props>();

function getClass(mode?: string, variant?: string): string[] {
    if (mode === "card") {
        return [
            "dashboard-quick-action",
            variant === "primary" ? "primary" : "",
        ].filter(Boolean);
    }

    return [
        "dashboard-quick-btn",
        variant === "primary" ? "primary" : "",
    ].filter(Boolean);
}
</script>

<template>
    <RouterLink
        v-if="action.to"
        :to="action.to"
        :class="getClass(mode, action.variant)"
    >
        <template v-if="mode === 'card'">
            <span class="dashboard-quick-action-icon">
                <i
                    v-if="action.icon"
                    :class="action.icon"
                ></i>
            </span>

            <span class="dashboard-quick-action-copy">
                <strong>{{ action.label }}</strong>
                <span v-if="action.description">{{ action.description }}</span>
            </span>
        </template>

        <template v-else>
            <i
                v-if="action.icon"
                :class="action.icon"
            ></i>
            {{ action.label }}
        </template>
    </RouterLink>

    <a
        v-else
        :href="action.href || '#'"
        :class="getClass(mode, action.variant)"
    >
        <template v-if="mode === 'card'">
            <span class="dashboard-quick-action-icon">
                <i
                    v-if="action.icon"
                    :class="action.icon"
                ></i>
            </span>

            <span class="dashboard-quick-action-copy">
                <strong>{{ action.label }}</strong>
                <span v-if="action.description">{{ action.description }}</span>
            </span>
        </template>

        <template v-else>
            <i
                v-if="action.icon"
                :class="action.icon"
            ></i>
            {{ action.label }}
        </template>
    </a>
</template>
