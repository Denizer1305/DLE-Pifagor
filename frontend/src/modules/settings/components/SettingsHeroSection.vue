<script setup lang="ts">
import type { SettingsHeroModel } from "@/modules/settings/types/settings.types";

interface Props {
    hero: SettingsHeroModel;
    pageClass?: string;
}

defineProps<Props>();
</script>

<template>
    <section
        class="settings-hero-card fade-in visible"
        :class="pageClass"
    >
        <div
            class="settings-hero-bg"
            aria-hidden="true"
        >
            <div class="settings-hero-circle one"></div>
            <div class="settings-hero-circle two"></div>
            <div class="settings-hero-glow one"></div>
            <div class="settings-hero-glow two"></div>
        </div>

        <div class="settings-hero-layout">
            <div class="settings-hero-copy">
                <div class="settings-hero-topline">
                    <i :class="hero.icon"></i>
                    {{ hero.topline }}
                </div>

                <h1 class="settings-hero-title">
                    {{ hero.title }}
                </h1>

                <p class="settings-hero-text">
                    {{ hero.text }}
                </p>

                <div
                    v-if="hero.badges.length"
                    class="settings-hero-badges"
                >
                    <span
                        v-for="badge in hero.badges"
                        :key="badge.label"
                        class="settings-hero-badge"
                    >
                        <i :class="badge.icon"></i>
                        {{ badge.label }}
                    </span>
                </div>
            </div>

            <div class="settings-hero-side">
                <div class="settings-hero-summary">
                    <div class="settings-hero-summary-head">
                        <strong>Текущая сводка</strong>
                        <span>Активные параметры</span>
                    </div>

                    <div class="settings-hero-summary-list">
                        <div
                            v-for="row in hero.summaryRows"
                            :key="row.label"
                            class="settings-hero-summary-row"
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