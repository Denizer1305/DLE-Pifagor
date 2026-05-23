<script setup lang="ts">
import { onMounted } from "vue";

import AuthDecor from "@/modules/auth/components/AuthDecor.vue";
import AuthIntro from "@/modules/auth/components/AuthIntro.vue";
import AuthPublicHeader from "@/modules/auth/components/AuthPublicHeader.vue";
import { useAuthPageMotion } from "@/modules/auth/composables/useAuthPageMotion";
import { useThemeStore } from "@/stores/theme.store";
import type { AuthIntroConfig } from "@/modules/auth/types/auth-form.types";

interface Props {
    intro: AuthIntroConfig;
    pageClass?: string;
}

withDefaults(defineProps<Props>(), {
    pageClass: "",
});

const themeStore = useThemeStore();
const { revealPage } = useAuthPageMotion();

function handleThemeToggle(): void {
    themeStore.toggleTheme();
}

onMounted(() => {
    revealPage();
});
</script>

<template>
    <div :class="['auth-page', pageClass]">
        <AuthPublicHeader
            :is-dark-theme="themeStore.isDark"
            @toggle-theme="handleThemeToggle"
        />

        <main class="auth-section">
            <AuthDecor />

            <div class="container auth-container">
                <div class="auth-layout">
                    <AuthIntro :intro="intro" />

                    <section class="auth-form-shell fade-in">
                        <div class="auth-form-inner">
                            <slot />
                        </div>
                    </section>
                </div>
            </div>
        </main>
    </div>
</template>
