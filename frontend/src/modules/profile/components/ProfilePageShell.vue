<script setup lang="ts">
import DashboardPageScaffold from "@/components/dashboard/layout/DashboardPageScaffold.vue";
import { useDashboardLogout } from "@/composables/dashboard/useDashboardLogout";

import type { DashboardPageScaffoldModel } from "@/components/dashboard/types/dashboard.types";

interface Props {
    model?: DashboardPageScaffoldModel | null;
    isLoading: boolean;
    errorMessage: string;
    loadingText: string;
}

interface Emits {
    (event: "reload"): void;
}

withDefaults(defineProps<Props>(), {
    model: null,
});

const emit = defineEmits<Emits>();
const { logout } = useDashboardLogout();
</script>

<template>
    <DashboardPageScaffold
        v-if="model"
        :model="model"
        :is-loading="isLoading"
        :error-message="errorMessage"
        :loading-text="loadingText"
        @reload="emit('reload')"
        @logout="logout"
    >
        <slot></slot>
    </DashboardPageScaffold>

    <div
        v-else
        class="dashboard-loading-state"
    >
        <i class="fas fa-spinner"></i>
        <span>{{ loadingText }}</span>
    </div>
</template>
