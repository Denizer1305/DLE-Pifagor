<script setup lang="ts">
import type { ProfileAchievementsPageModel } from "@/modules/profile/types/profile.types";

interface Props {
    filters: ProfileAchievementsPageModel["filters"];
    activeSource: string;
    activeCategory: string;
}

interface Emits {
    (event: "update:activeSource", value: string): void;
    (event: "update:activeCategory", value: string): void;
    (event: "upload"): void;
}

defineProps<Props>();
const emit = defineEmits<Emits>();
</script>

<template>
    <section class="achievements-management-section fade-in visible">
        <div class="achievements-management-card">
            <div class="achievements-management-head">
                <div>
                    <div class="achievements-card-topline">
                        <i :class="filters.icon"></i>
                        {{ filters.topline }}
                    </div>

                    <h2 class="achievements-card-title">
                        {{ filters.title }}
                    </h2>

                    <p class="achievements-card-text">
                        {{ filters.text }}
                    </p>
                </div>

                <div class="achievements-management-actions">
                    <button
                        type="button"
                        class="achievements-main-btn primary"
                        :disabled="!filters.isUploadEnabled"
                        @click="emit('upload')"
                    >
                        <i :class="filters.uploadIcon"></i>
                        {{ filters.uploadLabel }}
                    </button>
                </div>
            </div>

            <div
                class="achievements-source-switch"
                role="tablist"
                :aria-label="filters.sourceAriaLabel"
            >
                <button
                    v-for="source in filters.sources"
                    :key="source.key"
                    type="button"
                    class="achievements-source-btn"
                    :class="{ 'is-active': source.key === activeSource }"
                    @click="emit('update:activeSource', source.key)"
                >
                    {{ source.label }}
                </button>
            </div>

            <div class="achievements-filter-chips">
                <button
                    v-for="category in filters.categories"
                    :key="category.key"
                    type="button"
                    class="achievements-filter-chip"
                    :class="{ 'is-active': category.key === activeCategory }"
                    @click="emit('update:activeCategory', category.key)"
                >
                    {{ category.label }}
                </button>
            </div>
        </div>
    </section>
</template>
