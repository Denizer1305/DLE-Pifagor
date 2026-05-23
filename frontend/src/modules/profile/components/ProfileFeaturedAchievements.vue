<script setup lang="ts">
import type { ProfileAchievementDocumentModel } from "@/modules/profile/types/profile.types";

interface Props {
    documents: ProfileAchievementDocumentModel[];
}

interface Emits {
    (event: "preview", document: ProfileAchievementDocumentModel): void;
}

defineProps<Props>();
const emit = defineEmits<Emits>();
</script>

<template>
    <section class="achievements-grid fade-in visible">
        <article class="achievements-card achievements-card-wide">
            <div class="achievements-card-topline">
                <i class="fas fa-star"></i>
                Избранное
            </div>

            <h2 class="achievements-card-title">
                Ключевые достижения
            </h2>

            <p class="achievements-card-text">
                Самые значимые материалы, которые формируют ядро вашего профессионального портфолио.
            </p>

            <div class="achievements-featured-grid">
                <article
                    v-for="document in documents"
                    :key="document.id"
                    class="achievement-featured-card"
                >
                    <div class="achievement-featured-preview">
                        <i :class="document.icon"></i>
                    </div>

                    <div class="achievement-featured-body">
                        <div class="achievement-featured-tags">
                            <span>{{ document.sourceLabel }}</span>
                            <span>{{ document.categoryLabel }}</span>
                        </div>

                        <h3>{{ document.title }}</h3>
                        <p>{{ document.subtitle }}</p>
                    </div>

                    <div class="achievement-featured-footer">
                        <button
                            type="button"
                            class="achievement-document-btn"
                            @click="emit('preview', document)"
                        >
                            {{ document.previewLabel }}
                        </button>

                        <button
                            type="button"
                            class="achievement-document-btn"
                        >
                            {{ document.downloadLabel }}
                        </button>
                    </div>
                </article>
            </div>
        </article>
    </section>
</template>