<script setup lang="ts">
import { computed } from "vue";
import { RouterLink, useRoute } from "vue-router";

import PublicMobileMenu from "@/modules/public/components/layout/PublicMobileMenu.vue";
import PublicThemeToggle from "@/modules/public/components/layout/PublicThemeToggle.vue";
import { useMobileMenu } from "@/modules/public/composables/useMobileMenu";
import { useScrollHeader } from "@/modules/public/composables/useScrollHeader";
import { publicNavigationItems } from "@/modules/public/data/public-navigation.data";
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
    mobileMenuLabel,
    closeMobileMenu,
    toggleMobileMenu,
} = useMobileMenu();

const { isScrolled } = useScrollHeader();

const headerClasses = computed(() => {
    return {
        "is-scrolled": isScrolled.value,
    };
});

function isActiveRoute(routeName: string): boolean {
    return route.name === routeName;
}
</script>

<template>
    <header
        class="site-header"
        :class="headerClasses"
    >
        <div class="container">
            <div class="header-shell">
                <div class="logo-header">
                    <RouterLink
                        :to="{ name: 'home' }"
                        aria-label="Цифровая образовательная среда «Пифагор»"
                    >
                        <img
                            :src="logoSrc"
                            alt="ЦОС «Пифагор»"
                        />
                    </RouterLink>
                </div>

                <nav
                    class="header-nav"
                    aria-label="Основная навигация"
                >
                    <ul class="nav-links">
                        <li
                            v-for="item in publicNavigationItems"
                            :key="item.routeName"
                        >
                            <RouterLink
                                :to="{ name: item.routeName }"
                                :class="{ active: isActiveRoute(item.routeName) }"
                            >
                                {{ item.label }}
                            </RouterLink>
                        </li>
                    </ul>
                </nav>

                <div class="header-actions">
                    <PublicThemeToggle
                        :is-dark-theme="props.isDarkTheme"
                        @toggle="emit('toggle-theme')"
                    />

                    <RouterLink
                        class="header-login-link"
                        :to="{ name: 'login' }"
                    >
                        Войти
                    </RouterLink>

                    <RouterLink
                        class="login-btn"
                        :to="{ name: 'register' }"
                    >
                        Регистрация
                    </RouterLink>

                    <button
                        class="mobile-menu-toggle burger"
                        :class="{ active: isMobileMenuOpen }"
                        type="button"
                        :aria-label="mobileMenuLabel"
                        :aria-expanded="isMobileMenuOpen"
                        @click="toggleMobileMenu"
                    >
                        <span></span>
                        <span></span>
                        <span></span>
                    </button>
                </div>
            </div>
        </div>

        <PublicMobileMenu
            :is-open="isMobileMenuOpen"
            :navigation="publicNavigationItems"
            :is-dark-theme="props.isDarkTheme"
            @close="closeMobileMenu"
            @toggle-theme="emit('toggle-theme')"
        />
    </header>
</template>
