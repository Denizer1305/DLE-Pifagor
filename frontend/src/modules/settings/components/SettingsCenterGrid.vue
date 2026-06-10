<script setup lang="ts">
import { RouterLink } from "vue-router";

import type { SettingsCenterCardModel } from "@/modules/settings/types/settings.types";

interface Props {
    cards: SettingsCenterCardModel[];
}

defineProps<Props>();
</script>

<template>
    <section class="settings-center-grid fade-in visible">
        <RouterLink
            v-for="card in cards"
            :key="card.key"
            class="settings-center-card"
            :to="{ name: card.routeName }"
        >
            <div class="settings-center-card-icon">
                <i :class="card.icon"></i>
            </div>

            <div class="settings-center-card-copy">
                <div class="settings-center-card-head">
                    <h2>{{ card.title }}</h2>

                    <span
                        v-if="card.badge"
                        class="settings-center-card-badge"
                    >
                        {{ card.badge }}
                    </span>
                </div>

                <p>{{ card.text }}</p>
            </div>

            <span class="settings-center-card-arrow">
                <i class="fas fa-arrow-right"></i>
            </span>
        </RouterLink>
    </section>
</template>
