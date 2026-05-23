<script setup lang="ts">
import { RouterLink } from "vue-router";

import PublicLanguageToggle from "@/modules/public/components/layout/PublicLanguageToggle.vue";
import PublicAccountMenu from "@/modules/public/components/layout/PublicAccountMenu.vue";
import { useI18n } from "@/composables/useI18n";
import { useThemedLogo } from "@/composables/useThemedLogo";
import type {
    PublicAccountMenuContent,
    PublicNavigationItem,
} from "@/modules/public/types/public.types";

interface Props {
    isOpen: boolean;
    navigation: PublicNavigationItem[];
    isDarkTheme: boolean;
    accountMenu?: PublicAccountMenuContent | null;
}

interface Emits {
    (event: "close"): void;
    (event: "toggle-theme"): void;
    (event: "logout"): void;
}

defineProps<Props>();
const emit = defineEmits<Emits>();
const { logoSrc } = useThemedLogo();
const { t } = useI18n();

function getItemIcon(item: PublicNavigationItem): string {
    return item.icon || "fa-solid fa-circle-dot";
}

function getItemDescription(item: PublicNavigationItem): string {
    return item.description || t("mobile.fallbackDescription");
}
</script>

<template>
    <Teleport to="body">
        <button
            class="mobile-overlay"
            :class="{ active: isOpen }"
            type="button"
            :aria-label="t('common.closeMobileMenu')"
            @click="emit('close')"
        ></button>

        <aside
            class="mobile-menu"
            :class="{ active: isOpen }"
            :aria-label="t('common.mobileMenu')"
        >
            <div
                class="mobile-menu-bg"
                aria-hidden="true"
            >
                <div class="mobile-menu-circle one"></div>
                <div class="mobile-menu-circle two"></div>
                <div class="mobile-menu-circle three"></div>
                <div class="mobile-menu-line one"></div>
                <div class="mobile-menu-line two"></div>
                <div class="mobile-menu-glow"></div>
            </div>

            <div class="mobile-menu-header">
                <RouterLink
                    class="mobile-logo"
                    :to="{ name: 'home' }"
                    @click="emit('close')"
                >
                    <img
                        :src="logoSrc"
                        :alt="t('footer.brandName')"
                    />

                    <span class="mobile-logo-text">
                        {{ t("footer.brandName") }}
                    </span>
                </RouterLink>

                <div class="mobile-header-actions">
                    <button
                        class="mobile-theme-toggle"
                        type="button"
                        :aria-label="t('common.switchTheme')"
                        @click="emit('toggle-theme')"
                    >
                        <i class="base-icon fa-solid fa-sun"></i>
                        <i class="base-icon fa-solid fa-moon"></i>
                    </button>

                    <PublicLanguageToggle />

                    <button
                        class="mobile-close-btn"
                        type="button"
                        :aria-label="t('common.closeMenu')"
                        @click="emit('close')"
                    >
                        <i class="fa-solid fa-xmark"></i>
                    </button>
                </div>
            </div>

            <div class="mobile-menu-body">
                <nav
                    class="mobile-nav-list"
                    :aria-label="t('common.mobileNavigation')"
                >
                    <RouterLink
                        v-for="item in navigation"
                        :key="item.routeName"
                        class="mobile-nav-link"
                        :to="{ name: item.routeName }"
                        @click="emit('close')"
                    >
                        <span class="mobile-nav-icon">
                            <i :class="getItemIcon(item)"></i>
                        </span>

                        <span class="mobile-nav-content">
                            <span class="mobile-nav-title">
                                {{ item.label }}
                            </span>

                            <span class="mobile-nav-desc">
                                {{ getItemDescription(item) }}
                            </span>
                        </span>

                        <span class="mobile-nav-arrow">
                            <i class="fa-solid fa-arrow-right"></i>
                        </span>
                    </RouterLink>
                </nav>

                <div class="mobile-quote">
                    <p class="mobile-quote-text">
                        {{ t("mobile.quote") }}
                    </p>

                    <p class="mobile-quote-author">
                        {{ t("footer.brandName") }}
                    </p>
                </div>

                <div class="mobile-auth">
                    <PublicAccountMenu
                        v-if="accountMenu"
                        :content="accountMenu"
                        mode="mobile"
                        @logout="emit('logout')"
                    />

                    <template v-else>
                        <RouterLink
                            class="mobile-login-btn"
                            :to="{ name: 'login' }"
                            @click="emit('close')"
                        >
                            <i class="fa-solid fa-right-to-bracket"></i>
                            {{ t("auth.login") }}
                        </RouterLink>

                        <RouterLink
                            class="mobile-login-btn mobile-register-btn"
                            :to="{ name: 'register' }"
                            @click="emit('close')"
                        >
                            <i class="fa-solid fa-user-plus"></i>
                            {{ t("auth.register") }}
                        </RouterLink>
                    </template>
                </div>
            </div>
        </aside>
    </Teleport>
</template>
