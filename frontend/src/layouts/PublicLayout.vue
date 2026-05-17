<script setup lang="ts">
import PublicFooter from "@/modules/public/components/layout/PublicFooter.vue";
import PublicHeader from "@/modules/public/components/layout/PublicHeader.vue";
import { useThemeStore } from "@/stores/theme.store";

const themeStore = useThemeStore();

function handleThemeToggle(): void {
    themeStore.toggleTheme();
}
</script>

<template>
    <div class="public-layout">
        <PublicHeader
            :is-dark-theme="themeStore.isDark"
            @toggle-theme="handleThemeToggle"
        />

        <main class="public-layout__main">
            <slot />
        </main>

        <PublicFooter />
    </div>
</template>
