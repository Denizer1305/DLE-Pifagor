<script setup lang="ts">
import { computed } from "vue";
import { RouterLink, useRoute } from "vue-router";

import PublicMobileMenu from "@/modules/public/components/layout/PublicMobileMenu.vue";
import PublicLanguageToggle from "@/modules/public/components/layout/PublicLanguageToggle.vue";
import PublicThemeToggle from "@/modules/public/components/layout/PublicThemeToggle.vue";
import { useI18n } from "@/composables/useI18n";
import { useMobileMenu } from "@/modules/public/composables/useMobileMenu";
import { useScrollHeader } from "@/modules/public/composables/useScrollHeader";
import { publicNavigationItems } from "@/modules/public/data/public-navigation.data";
import { useThemedLogo } from "@/composables/useThemedLogo";

interface Props {
    isDarkTheme: boolean;
}

interface Emits {
    (event: "toggle-theme"): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

const route = useRoute();
const { localizePublicContent, t } = useI18n();

const {
    isMobileMenuOpen,
    mobileMenuLabel,
    closeMobileMenu,
    toggleMobileMenu,
} = useMobileMenu();

const { isScrolled } = useScrollHeader();
const { logoSrc } = useThemedLogo();

const navigationItems = computed(() => {
    return localizePublicContent(publicNavigationItems);
});

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
                        :aria-label="t('footer.brandName')"
                    >
                        <img
                            :src="logoSrc"
                            :alt="t('footer.brandName')"
                        />
                    </RouterLink>
                </div>

                <nav
                    class="header-nav"
                    :aria-label="t('common.navigation')"
                >
                    <ul class="nav-links">
                        <li
                            v-for="item in navigationItems"
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

                    <PublicLanguageToggle />

                    <RouterLink
                        class="header-login-link"
                        :to="{ name: 'login' }"
                    >
                        {{ t("auth.login") }}
                    </RouterLink>

                    <RouterLink
                        class="login-btn"
                        :to="{ name: 'register' }"
                    >
                        {{ t("auth.register") }}
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
            :navigation="navigationItems"
            :is-dark-theme="props.isDarkTheme"
            @close="closeMobileMenu"
            @toggle-theme="emit('toggle-theme')"
        />
    </header>
</template>
