<script setup lang="ts">
import { RouterLink } from "vue-router";

import type { PublicNavigationItem } from "@/modules/public/types/public.types";
import logoSrc from "@/assets/image/logo/logo.svg";

interface Props {
    isOpen: boolean;
    navigation: PublicNavigationItem[];
    isDarkTheme: boolean;
}

interface Emits {
    (event: "close"): void;
    (event: "toggle-theme"): void;
}

defineProps<Props>();
const emit = defineEmits<Emits>();

function getItemIcon(item: PublicNavigationItem): string {
    return item.icon || "fa-solid fa-circle-dot";
}

function getItemDescription(item: PublicNavigationItem): string {
    return item.description || "Перейти в раздел";
}
</script>

<template>
    <Teleport to="body">
        <button
            class="mobile-overlay"
            :class="{ active: isOpen }"
            type="button"
            aria-label="Закрыть мобильное меню"
            @click="emit('close')"
        ></button>

        <aside
            class="mobile-menu"
            :class="{ active: isOpen }"
            aria-label="Мобильное меню"
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
                        alt="ЦОС «Пифагор»"
                    />

                    <span class="mobile-logo-text">
                        Пифагор
                    </span>
                </RouterLink>

                <div class="mobile-header-actions">
                    <button
                        class="mobile-theme-toggle"
                        type="button"
                        aria-label="Переключить тему"
                        @click="emit('toggle-theme')"
                    >
                        <i class="base-icon fa-solid fa-sun"></i>
                        <i class="base-icon fa-solid fa-moon"></i>
                    </button>

                    <button
                        class="mobile-close-btn"
                        type="button"
                        aria-label="Закрыть меню"
                        @click="emit('close')"
                    >
                        <i class="fa-solid fa-xmark"></i>
                    </button>
                </div>
            </div>

            <div class="mobile-menu-body">
                <nav
                    class="mobile-nav-list"
                    aria-label="Мобильная навигация"
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
                        Цифровая образовательная среда для спокойного обучения,
                        развития и наставничества.
                    </p>

                    <p class="mobile-quote-author">
                        ЦОС «Пифагор»
                    </p>
                </div>

                <div class="mobile-auth">
                    <RouterLink
                        class="mobile-login-btn"
                        :to="{ name: 'login' }"
                        @click="emit('close')"
                    >
                        <i class="fa-solid fa-right-to-bracket"></i>
                        Войти
                    </RouterLink>

                    <RouterLink
                        class="mobile-login-btn mobile-register-btn"
                        :to="{ name: 'register' }"
                        @click="emit('close')"
                    >
                        <i class="fa-solid fa-user-plus"></i>
                        Регистрация
                    </RouterLink>
                </div>
            </div>
        </aside>
    </Teleport>
</template>
