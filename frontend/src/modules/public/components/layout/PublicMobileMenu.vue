<script setup lang="ts">
import { RouterLink } from "vue-router";

import type { PublicNavigationItem } from "@/modules/public/types/public.types";

interface Props {
    isOpen: boolean;
    navigation: PublicNavigationItem[];
}

interface Emits {
    (event: "close"): void;
}

defineProps<Props>();
const emit = defineEmits<Emits>();
</script>

<template>
    <Transition name="public-mobile-menu">
        <div
            v-if="isOpen"
            class="public-mobile-menu"
        >
            <button
                class="public-mobile-menu__backdrop"
                type="button"
                aria-label="Закрыть меню"
                @click="emit('close')"
            ></button>

            <aside class="public-mobile-menu__panel">
                <div class="public-mobile-menu__top">
                    <span>Меню</span>

                    <button
                        class="public-mobile-menu__close"
                        type="button"
                        aria-label="Закрыть меню"
                        @click="emit('close')"
                    >
                        <i class="fa-solid fa-xmark"></i>
                    </button>
                </div>

                <nav class="public-mobile-menu__nav">
                    <RouterLink
                        v-for="item in navigation"
                        :key="item.routeName"
                        class="public-mobile-menu__link"
                        :to="{ name: item.routeName }"
                        @click="emit('close')"
                    >
                        {{ item.label }}
                    </RouterLink>
                </nav>

                <div class="public-mobile-menu__actions">
                    <RouterLink
                        class="public-mobile-menu__action public-mobile-menu__action--ghost"
                        :to="{ name: 'login' }"
                        @click="emit('close')"
                    >
                        Войти
                    </RouterLink>

                    <RouterLink
                        class="public-mobile-menu__action public-mobile-menu__action--primary"
                        :to="{ name: 'register' }"
                        @click="emit('close')"
                    >
                        Регистрация
                    </RouterLink>
                </div>
            </aside>
        </div>
    </Transition>
</template>