<script setup lang="ts">
import DashboardPageScaffold from "@/components/dashboard/layout/DashboardPageScaffold.vue";
import SettingsHeroSection from "@/modules/settings/components/SettingsHeroSection.vue";

import { useDashboardLogout } from "@/composables/dashboard/useDashboardLogout";

import type { DashboardPageScaffoldModel } from "@/components/dashboard/types/dashboard.types";
import type { SettingsHeroModel } from "@/modules/settings/types/settings.types";

interface Props {
    model?: DashboardPageScaffoldModel | null;
    hero?: SettingsHeroModel | null;
    isReady?: boolean;
    isLoading: boolean;
    errorMessage: string;
    loadingText: string;
}

interface Emits {
    (event: "reload"): void;
}

const props = withDefaults(defineProps<Props>(), {
    model: null,
    hero: null,
    isReady: true,
});

const emit = defineEmits<Emits>();
const { logout } = useDashboardLogout();
</script>

<template>
    <DashboardPageScaffold
        v-if="isReady && model && hero"
        :model="model"
        :is-loading="isLoading"
        :error-message="errorMessage"
        :loading-text="loadingText"
        @reload="emit('reload')"
        @logout="logout"
    >
        <SettingsHeroSection :hero="hero" />
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
