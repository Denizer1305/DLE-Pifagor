<script setup lang="ts">
import { RouterLink } from "vue-router";

import type { DashboardProfilePanelContent } from "@/components/dashboard/types/dashboard.types";

interface Props {
    content: DashboardProfilePanelContent;
}

interface Emits {
    (event: "logout"): void;
}

defineProps<Props>();
defineEmits<Emits>();
</script>

<template>
    <div class="dashboard-panel-content">
        <div class="dashboard-profile-panel-head">
            <div class="dashboard-profile-panel-avatar">
                <img
                    v-if="content.user.avatarUrl"
                    :src="content.user.avatarUrl"
                    :alt="content.user.avatarAlt"
                />

                <span v-else>
                    {{ content.user.fullName.slice(0, 1).toUpperCase() }}
                </span>
            </div>

            <div>
                <strong>{{ content.user.fullName }}</strong>
                <span>{{ content.user.roleLabel }}</span>
            </div>
        </div>

        <div class="dashboard-profile-panel-info">
            <strong>{{ content.title }}</strong>
            <span>{{ content.subtitle }}</span>
        </div>

        <div class="dashboard-profile-panel-actions">
            <template
                v-for="action in content.actions"
                :key="action.label"
            >
                <button
                    v-if="action.action === 'logout'"
                    type="button"
                    class="dashboard-profile-action"
                    @click="$emit('logout')"
                >
                    <i :class="action.icon"></i>
                    {{ action.label }}
                </button>

                <RouterLink
                    v-else-if="action.to"
                    class="dashboard-profile-action"
                    :to="action.to"
                >
                    <i :class="action.icon"></i>
                    {{ action.label }}
                </RouterLink>
            </template>
        </div>
    </div>
</template>