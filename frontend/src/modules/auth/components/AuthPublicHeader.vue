<script setup lang="ts">
import { computed } from "vue";
import { RouterLink } from "vue-router";

import logoPrimary from "@/assets/brand/logo/themes/light/logo.svg";
import { useI18n } from "@/composables/useI18n";
import { useThemedLogo } from "@/composables/useThemedLogo";
import PublicLanguageToggle from "@/modules/public/components/layout/PublicLanguageToggle.vue";

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
const { t } = useI18n();
const { getThemedLogoSrc } = useThemedLogo();

const themeIconClass = computed(() => {
    return props.isDarkTheme ? "fa-solid fa-sun" : "fa-solid fa-moon";
});

const currentLogoSrc = computed(() => getThemedLogoSrc(props.logoSrc));

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
                    :src="currentLogoSrc"
                    :alt="logoAlt"
                />
            </RouterLink>

            <div class="auth-public-header__actions">
                <button
                    class="auth-public-header__theme-button"
                    type="button"
                    :aria-label="t('common.switchTheme')"
                    @click="handleThemeToggle"
                >
                    <i :class="themeIconClass"></i>
                </button>

                <PublicLanguageToggle />
            </div>
        </div>
    </header>
</template>
