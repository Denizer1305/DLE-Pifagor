<script setup lang="ts">
import type { ProfileAchievementsPageModel } from "@/modules/profile/types/profile.types";

interface Props {
    hero: ProfileAchievementsPageModel["hero"];
}

defineProps<Props>();
</script>

<template>
    <section class="achievements-hero fade-in visible">
        <div
            class="achievements-hero-bg"
            aria-hidden="true"
        >
            <div class="achievements-hero-circle one"></div>
            <div class="achievements-hero-circle two"></div>
            <div class="achievements-hero-glow one"></div>
            <div class="achievements-hero-glow two"></div>
        </div>

        <div class="achievements-hero-layout">
            <div class="achievements-hero-copy">
                <div class="achievements-hero-topline">
                    <i :class="hero.icon"></i>
                    {{ hero.topline }}
                </div>

                <h1 class="achievements-hero-title">
                    {{ hero.title }}
                </h1>

                <p class="achievements-hero-text">
                    {{ hero.text }}
                </p>

                <div
                    v-if="hero.badges.length"
                    class="achievements-hero-badges"
                >
                    <span
                        v-for="badge in hero.badges"
                        :key="badge.label"
                        class="achievements-hero-badge"
                    >
                        <i :class="badge.icon"></i>
                        {{ badge.label }}
                    </span>
                </div>
            </div>

            <div class="achievements-hero-side">
                <div class="achievements-status-card">
                    <div class="achievements-status-head">
                        <strong>{{ hero.summaryTitle }}</strong>
                        <span>{{ hero.summarySubtitle }}</span>
                    </div>

                    <div class="achievements-status-list">
                        <div
                            v-for="row in hero.statusRows"
                            :key="row.label"
                            class="achievements-status-row"
                        >
                            <span>{{ row.label }}</span>
                            <strong>{{ row.value }}</strong>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>
