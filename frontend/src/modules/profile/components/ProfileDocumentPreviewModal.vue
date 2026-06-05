<script setup lang="ts">
import type { ProfileAchievementDocumentModel } from "@/modules/profile/types/profile.types";

interface Props {
    isOpen: boolean;
    document: ProfileAchievementDocumentModel | null;
}

interface Emits {
    (event: "close"): void;
}

defineProps<Props>();
const emit = defineEmits<Emits>();
</script>

<template>
    <Teleport to="body">
        <div
            v-if="isOpen && document"
            class="base-modal achievement-preview-modal is-open"
            role="dialog"
            aria-modal="true"
        >
            <button
                type="button"
                class="base-modal__overlay"
                aria-label="Закрыть окно"
                @click="emit('close')"
            ></button>

            <div class="base-modal__dialog achievement-preview-modal__dialog">
                <header class="base-modal__header">
                    <div>
                        <h2 class="base-modal__title">
                            {{ document.title }}
                        </h2>

                        <p class="base-modal__description">
                            {{ document.subtitle }}
                        </p>
                    </div>

                    <button
                        type="button"
                        class="base-modal__close"
                        aria-label="Закрыть"
                        @click="emit('close')"
                    >
                        <i class="fas fa-xmark"></i>
                    </button>
                </header>

                <div class="base-modal__body">
                    <div class="achievement-featured-preview">
                        <i :class="document.icon"></i>
                    </div>

                    <div class="achievement-featured-tags">
                        <span>{{ document.sourceLabel }}</span>
                        <span>{{ document.categoryLabel }}</span>
                    </div>
                </div>

                <footer class="base-modal__footer">
                    <button
                        type="button"
                        class="achievement-document-btn"
                        @click="emit('close')"
                    >
                        Закрыть
                    </button>

                    <button
                        type="button"
                        class="achievement-document-btn"
                    >
                        {{ document.downloadLabel }}
                    </button>
                </footer>
            </div>
        </div>
    </Teleport>
</template>
