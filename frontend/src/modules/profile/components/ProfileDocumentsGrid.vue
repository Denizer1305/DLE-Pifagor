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
                <i class="fas fa-certificate"></i>
                Коллекция документов
            </div>

            <h2 class="achievements-card-title">
                Все сертификаты и награды
            </h2>

            <p class="achievements-card-text">
                Основной каталог документов, который можно просматривать, фильтровать и открывать в полном виде.
            </p>

            <div class="achievements-documents-grid">
                <article
                    v-for="document in documents"
                    :key="document.id"
                    class="achievement-document-card"
                >
                    <div class="achievement-document-preview">
                        <i :class="document.icon"></i>
                    </div>

                    <div class="achievement-document-content">
                        <strong>{{ document.title }}</strong>
                        <span>{{ document.subtitle }}</span>
                    </div>

                    <div class="achievement-document-actions">
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