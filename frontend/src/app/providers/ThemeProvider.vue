<script setup lang="ts">
import { onMounted, watch } from "vue";

import { applyAppearanceSettings } from "@/modules/settings/composables/useAppearanceSettings";
import { getAppearanceSettings } from "@/modules/settings/services/settings.service";
import { useAuthStore } from "@/stores/auth.store";
import { useThemeStore } from "@/stores/theme.store";

const themeStore = useThemeStore();
const authStore = useAuthStore();

onMounted(() => {
    themeStore.initTheme();
});

watch(
    () => authStore.isAuthenticated,
    (isAuthenticated) => {
        if (isAuthenticated) {
            void syncUserAppearance();
        }
    },
    { immediate: true },
);

async function syncUserAppearance(): Promise<void> {
    try {
        applyAppearanceSettings(await getAppearanceSettings());
    } catch {
        // Local theme remains available if personal settings cannot be loaded.
    }
}
</script>

<template>
    <slot />
</template>
