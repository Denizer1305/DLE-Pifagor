<script setup lang="ts">
import type { ProfileAchievementsStatModel } from "@/modules/profile/types/profile.types";

interface Props {
    stats: ProfileAchievementsStatModel[];
}

defineProps<Props>();
</script>

<template>
    <section class="achievements-stats-strip fade-in visible">
        <div class="achievements-stats-grid">
            <article
                v-for="stat in stats"
                :key="stat.key"
                class="achievements-stat-card"
            >
                <div class="achievements-stat-icon">
                    <i :class="stat.icon"></i>
                </div>

                <div class="achievements-stat-copy">
                    <strong>{{ stat.value }}</strong>
                    <span>{{ stat.label }}</span>
                </div>
            </article>
        </div>
    </section>
</template>