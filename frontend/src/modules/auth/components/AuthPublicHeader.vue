<script setup lang="ts">
import { computed } from "vue";
import { RouterLink } from "vue-router";

import logoPrimary from "@/assets/image/logo/logo.svg";

interface Props {
    logoSrc?: string;
    logoAlt?: string;
    homeRouteName?: string;
    isDarkTheme?: boolean;
}

interface Emits {
    (event: "toggle-theme"): void;
}

const props = withDefaults(defineProps<Props>(), {
    logoSrc: logoPrimary,
    logoAlt: "ЦОС «Пифагор»",
    homeRouteName: "home",
    isDarkTheme: false,
});

const emit = defineEmits<Emits>();

const themeIconClass = computed(() => {
    return props.isDarkTheme ? "fa-solid fa-sun" : "fa-solid fa-moon";
});

function handleThemeToggle(): void {
    emit("toggle-theme");
}
</script>

<template>
    <header class="auth-public-header">
        <div class="auth-public-header__shell">
            <RouterLink
                class="auth-public-header__brand"
                :to="{ name: homeRouteName }"
                :aria-label="logoAlt"
            >
                <img
                    class="auth-public-header__logo"
                    :src="logoSrc"
                    :alt="logoAlt"
                />
            </RouterLink>

            <button
                class="auth-public-header__theme-button"
                type="button"
                aria-label="Переключить тему"
                @click="handleThemeToggle"
            >
                <i :class="themeIconClass"></i>
            </button>
        </div>
    </header>
</template>