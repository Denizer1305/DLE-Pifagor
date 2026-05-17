<script setup lang="ts">
import AuthDecor from "@/modules/auth/components/AuthDecor.vue";
import AuthPublicHeader from "@/modules/auth/components/AuthPublicHeader.vue";
import LogoutConfirmCard from "@/modules/auth/components/LogoutConfirmCard.vue";
import { useThemeStore } from "@/stores/theme.store";

const themeStore = useThemeStore();

function handleThemeToggle(): void {
    themeStore.toggleTheme();
}
</script>

<template>
    <div class="auth-page logout-page">
        <AuthPublicHeader
            :is-dark-theme="themeStore.isDark"
            @toggle-theme="handleThemeToggle"
        />

        <main class="auth-logout-section">
            <AuthDecor />

            <LogoutConfirmCard />
        </main>
    </div>
</template>