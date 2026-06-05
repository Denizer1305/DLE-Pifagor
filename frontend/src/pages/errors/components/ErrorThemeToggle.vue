<script setup lang="ts">
import { computed } from "vue";

import { useI18n } from "@/composables/useI18n";
import { useThemeStore } from "@/stores/theme.store";

const themeStore = useThemeStore();
const { tr } = useI18n();

const iconClass = computed(() => {
    return themeStore.isDark ? "fa-solid fa-sun" : "fa-solid fa-moon";
});
</script>

<template>
    <button
        class="error-theme-toggle"
        type="button"
        :aria-label="tr('Переключить тему')"
        @click="themeStore.toggleTheme"
    >
        <i :class="iconClass"></i>
    </button>
</template>
