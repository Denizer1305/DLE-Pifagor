<script setup lang="ts">
import DashboardEmptyState from "@/components/dashboard/shared/DashboardEmptyState.vue";
import type {
    ProfileAchievementDocumentModel,
    ProfileAchievementsCollectionContent,
} from "@/modules/profile/types/profile.types";

interface Props {
    documents: ProfileAchievementDocumentModel[];
    content: ProfileAchievementsCollectionContent;
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
                <i :class="content.icon"></i>
                {{ content.topline }}
            </div>

            <h2 class="achievements-card-title">
                {{ content.title }}
            </h2>

            <p class="achievements-card-text">
                {{ content.text }}
            </p>

            <div
                v-if="documents.length"
                class="achievements-documents-grid"
            >
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

            <DashboardEmptyState
                v-else
                :icon="content.emptyIcon"
                :title="content.emptyTitle"
                :text="content.emptyText"
            />
        </article>
    </section>
</template>
