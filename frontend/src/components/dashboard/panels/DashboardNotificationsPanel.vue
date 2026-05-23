<script setup lang="ts">
import { RouterLink } from "vue-router";

import type { DashboardNotificationsContent } from "@/components/dashboard/types/dashboard.types";

interface Props {
    content: DashboardNotificationsContent;
}

defineProps<Props>();
const emit = defineEmits<{
    (event: "create"): void;
}>();
</script>

<template>
    <div class="dashboard-panel-content">
        <div class="dashboard-floating-panel-head">
            <strong>{{ content.title }}</strong>
        </div>

        <div
            v-if="content.items.length"
            class="dashboard-notifications-list"
        >
            <div
                v-for="item in content.items"
                :key="item.id"
                class="dashboard-notification-item"
                :class="{ 'is-new': item.isNew }"
            >
                <i :class="item.icon"></i>

                <div>
                    <strong>{{ item.title }}</strong>
                    <span>{{ item.text }}</span>
                </div>
            </div>
        </div>

        <div
            v-else
            class="dashboard-panel-empty"
        >
            {{ content.emptyText }}
        </div>

        <RouterLink
            v-if="content.actionTo"
            class="dashboard-panel-link"
            :to="content.actionTo"
        >
            {{ content.actionLabel }}
        </RouterLink>

        <a
            v-else-if="content.actionLabel"
            href="#"
            class="dashboard-panel-link"
        >
            {{ content.actionLabel }}
        </a>
    </div>
</template>
