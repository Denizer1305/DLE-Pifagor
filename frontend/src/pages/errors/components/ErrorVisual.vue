<script setup lang="ts">
import { computed } from "vue";
import { RouterLink } from "vue-router";

import heroDarkLogo from "@/assets/brand/logo/themes/dark/hero-logo.svg";
import { useThemedLogo } from "@/composables/useThemedLogo";
import { useThemeStore } from "@/stores/theme.store";

defineProps<{
    visualIcon: string;
    orbitIcon: string;
}>();

const { heroLogoSrc } = useThemedLogo();
const themeStore = useThemeStore();

const currentHeroLogoSrc = computed(() => {
    return themeStore.isDark ? heroDarkLogo : heroLogoSrc.value;
});
</script>

<template>
    <aside class="error-visual" aria-label="ЦОС «Пифагор»">
        <RouterLink
            class="error-visual__logo"
            :to="{ name: 'home' }"
        >
            <img
                :src="currentHeroLogoSrc"
                alt="ЦОС «Пифагор»"
            />
        </RouterLink>

        <div class="error-visual__icon">
            <i :class="visualIcon"></i>
        </div>

        <div class="error-visual__orbit" aria-hidden="true">
            <i :class="orbitIcon"></i>
        </div>
    </aside>
</template>
