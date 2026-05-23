<script setup lang="ts">
import { ref } from "vue";
import { RouterLink } from "vue-router";

import type { PublicAccountMenuContent } from "@/modules/public/types/public.types";

interface Props {
    content: PublicAccountMenuContent;
    mode?: "desktop" | "mobile";
}

interface Emits {
    (event: "logout"): void;
}

const props = withDefaults(defineProps<Props>(), {
    mode: "desktop",
});
const emit = defineEmits<Emits>();
const isOpen = ref(false);

function close(): void {
    isOpen.value = false;
}

function logout(): void {
    close();
    emit("logout");
}
</script>

<template>
    <div
        class="public-account"
        :class="{ 'is-mobile': props.mode === 'mobile' }"
    >
        <button
            v-if="props.mode === 'desktop'"
            type="button"
            class="public-account__trigger"
            :aria-label="content.openLabel"
            :aria-expanded="isOpen"
            @click="isOpen = !isOpen"
        >
            <span class="public-account__avatar">
                <img
                    :src="content.user.avatarUrl"
                    :alt="content.user.avatarAlt"
                />
            </span>

            <span class="public-account__meta">
                <strong>{{ content.user.fullName }}</strong>
                <span>{{ content.user.roleLabel }}</span>
            </span>

            <i class="fa-solid fa-chevron-down"></i>
        </button>

        <div
            v-if="props.mode === 'mobile' || isOpen"
            class="public-account__panel"
        >
            <div class="public-account__head">
                <span class="public-account__avatar">
                    <img
                        :src="content.user.avatarUrl"
                        :alt="content.user.avatarAlt"
                    />
                </span>

                <span class="public-account__meta">
                    <strong>{{ content.user.fullName }}</strong>
                    <span>{{ content.user.roleLabel }}</span>
                </span>
            </div>

            <div class="public-account__info">
                <strong>{{ content.title }}</strong>
                <span>{{ content.subtitle }}</span>
            </div>

            <div class="public-account__actions">
                <template
                    v-for="action in content.actions"
                    :key="action.label"
                >
                    <button
                        v-if="action.action === 'logout'"
                        type="button"
                        class="public-account__action"
                        @click="logout"
                    >
                        <i :class="action.icon"></i>
                        {{ action.label }}
                    </button>

                    <RouterLink
                        v-else-if="action.routeName"
                        class="public-account__action"
                        :to="{ name: action.routeName }"
                        @click="close"
                    >
                        <i :class="action.icon"></i>
                        {{ action.label }}
                    </RouterLink>
                </template>
            </div>
        </div>

        <button
            v-if="props.mode === 'desktop' && isOpen"
            type="button"
            class="public-account__backdrop"
            :aria-label="content.closeLabel"
            @click="close"
        ></button>
    </div>
</template>
