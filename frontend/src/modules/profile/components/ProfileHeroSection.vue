<script setup lang="ts">
import type { ProfileHeroModel } from "@/modules/profile/types/profile.types";

interface Props {
    hero: ProfileHeroModel;
}

defineProps<Props>();
</script>

<template>
    <section class="profile-hero-card fade-in visible">
        <div
            class="profile-hero-card-bg"
            aria-hidden="true"
        >
            <div class="profile-hero-circle one"></div>
            <div class="profile-hero-circle two"></div>
            <div class="profile-hero-glow one"></div>
            <div class="profile-hero-glow two"></div>
        </div>

        <div class="profile-hero-layout">
            <div class="profile-hero-copy">
                <div class="profile-hero-topline">
                    <i :class="hero.icon"></i>
                    {{ hero.topline }}
                </div>

                <h1 class="profile-hero-title">
                    {{ hero.title }}
                </h1>

                <p class="profile-hero-subtitle">
                    {{ hero.text }}
                </p>

                <div
                    v-if="hero.badges.length"
                    class="profile-hero-badges"
                >
                    <span
                        v-for="badge in hero.badges"
                        :key="badge.label"
                        class="profile-hero-badge"
                    >
                        <i :class="badge.icon"></i>
                        {{ badge.label }}
                    </span>
                </div>
            </div>

            <div class="profile-hero-side">
                <div class="profile-hero-avatar-card">
                    <div class="profile-hero-avatar">
                        <img
                            :src="hero.avatarUrl"
                            :alt="hero.avatarAlt"
                        />
                    </div>

                    <div class="profile-hero-meta">
                        <strong>{{ hero.roleLabel }}</strong>
                        <span>{{ hero.subtitle }}</span>
                    </div>

                    <div
                        v-if="hero.stats.length"
                        class="profile-hero-stats"
                    >
                        <div
                            v-for="stat in hero.stats"
                            :key="stat.label"
                            class="profile-hero-stat"
                        >
                            <strong>{{ stat.value }}</strong>
                            <span>{{ stat.label }}</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>
