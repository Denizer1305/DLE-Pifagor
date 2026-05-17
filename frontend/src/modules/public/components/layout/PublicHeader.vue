<script setup lang="ts">
import { computed } from "vue";
import { RouterLink, useRoute } from "vue-router";

import PublicMobileMenu from "@/modules/public/components/layout/PublicMobileMenu.vue";
import PublicThemeToggle from "@/modules/public/components/layout/PublicThemeToggle.vue";
import { publicNavigationItems } from "@/modules/public/data/public-navigation.data";
import { useMobileMenu } from "@/modules/public/composables/useMobileMenu";
import { useScrollHeader } from "@/modules/public/composables/useScrollHeader";
import logoSrc from "@/assets/image/logo/logo.svg";

interface Props {
    isDarkTheme: boolean;
}

interface Emits {
    (event: "toggle-theme"): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

const route = useRoute();

const {
    isMobileMenuOpen,
    mobileMenuIcon,
    mobileMenuLabel,
    closeMobileMenu,
    toggleMobileMenu,
} = useMobileMenu();

const { isScrolled } = useScrollHeader();

const headerClasses = computed(() => {
    return {
        "public-header--scrolled": isScrolled.value,
    };
});

function isActiveRoute(routeName: string): boolean {
    return route.name === routeName;
}
</script>

<template>
    <header
        class="public-header"
        :class="headerClasses"
    >
        <div class="container public-header__container">
            <RouterLink
                class="public-header__brand"
                :to="{ name: 'home' }"
                aria-label="Цифровая образовательная среда «Пифагор»"
            >
                <img
                    class="public-header__logo"
                    :src="logoSrc"
                    alt="ЦОС «Пифагор»"
                />

                <span class="public-header__brand-text">
                    <strong>Пифагор</strong>
                    <small>цифровая образовательная среда</small>
                </span>
            </RouterLink>

            <nav
                class="public-header__nav"
                aria-label="Основная навигация"
            >
                <RouterLink
                    v-for="item in publicNavigationItems"
                    :key="item.routeName"
                    class="public-header__nav-link"
                    :class="{ 'is-active': isActiveRoute(item.routeName) }"
                    :to="{ name: item.routeName }"
                >
                    {{ item.label }}
                </RouterLink>
            </nav>

            <div class="public-header__actions">
                <PublicThemeToggle
                    :is-dark-theme="props.isDarkTheme"
                    @toggle="emit('toggle-theme')"
                />

                <RouterLink
                    class="public-header__login"
                    :to="{ name: 'login' }"
                >
                    Войти
                </RouterLink>

                <RouterLink
                    class="public-header__register"
                    :to="{ name: 'register' }"
                >
                    Регистрация
                </RouterLink>

                <button
                    class="public-header__burger"
                    type="button"
                    :aria-label="mobileMenuLabel"
                    @click="toggleMobileMenu"
                >
                    <i :class="mobileMenuIcon"></i>
                </button>
            </div>
        </div>

        <PublicMobileMenu
            :is-open="isMobileMenuOpen"
            :navigation="publicNavigationItems"
            @close="closeMobileMenu"
        />
    </header>
</template>