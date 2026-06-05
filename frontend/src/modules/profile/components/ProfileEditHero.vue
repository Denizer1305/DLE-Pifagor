<script setup lang="ts">
import { RouterLink } from "vue-router";

import type { ProfileEditHeroContent } from "@/modules/profile/types/profile-edit.types";

interface Props {
    content: ProfileEditHeroContent;
    isSubmitting: boolean;
}

interface Emits {
    (event: "submit"): void;
}

defineProps<Props>();
const emit = defineEmits<Emits>();
</script>

<template>
    <section class="profile-edit-hero fade-in visible">
        <div
            class="profile-edit-hero-bg"
            aria-hidden="true"
        >
            <div class="profile-edit-hero-circle one"></div>
            <div class="profile-edit-hero-circle two"></div>
            <div class="profile-edit-hero-glow one"></div>
            <div class="profile-edit-hero-glow two"></div>
        </div>

        <div class="profile-edit-hero-layout">
            <div class="profile-edit-hero-copy">
                <div class="profile-edit-hero-topline">
                    <i :class="content.icon"></i>
                    {{ content.topline }}
                </div>

                <h1 class="profile-edit-hero-title">
                    {{ content.title }}
                </h1>

                <p class="profile-edit-hero-text">
                    {{ content.text }}
                </p>

                <div class="profile-edit-hero-badges">
                    <span
                        v-for="badge in content.badges"
                        :key="badge.label"
                        class="profile-edit-hero-badge"
                    >
                        <i :class="badge.icon"></i>
                        {{ badge.label }}
                    </span>
                </div>
            </div>

            <div class="profile-edit-hero-actions">
                <button
                    type="button"
                    class="profile-edit-main-btn"
                    :disabled="isSubmitting"
                    @click="emit('submit')"
                >
                    <i :class="content.primaryAction.icon"></i>
                    {{ isSubmitting ? content.primaryAction.pendingLabel : content.primaryAction.label }}
                </button>

                <RouterLink
                    v-if="content.secondaryAction.to"
                    class="profile-edit-secondary-btn"
                    :to="content.secondaryAction.to"
                >
                    <i :class="content.secondaryAction.icon"></i>
                    {{ content.secondaryAction.label }}
                </RouterLink>
            </div>
        </div>
    </section>
</template>
