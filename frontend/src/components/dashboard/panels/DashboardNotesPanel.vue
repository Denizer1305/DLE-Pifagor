<script setup lang="ts">
import { computed, ref } from "vue";
import { RouterLink } from "vue-router";

import type {
    DashboardNoteItem,
    DashboardNotesContent,
} from "@/components/dashboard/types/dashboard.types";

interface Props {
    content: DashboardNotesContent;
}

const props = defineProps<Props>();
const emit = defineEmits<{
    (event: "create"): void;
    (event: "remove", itemId: number): void;
}>();

const selectedNote = ref<DashboardNoteItem | null>(null);

const readLabel = computed(() => props.content.readLabel || "Прочитать");
const closeLabel = computed(() => props.content.closeLabel || "Закрыть");
const modalTitle = computed(() => props.content.modalTitle || "Полный текст заметки");

function getPreviewText(text: string): string {
    const normalizedText = text.trim();

    if (normalizedText.length <= 120) {
        return normalizedText;
    }

    return `${normalizedText.slice(0, 120).trim()}...`;
}

function hasLongText(text: string): boolean {
    return text.trim().length > 120;
}

function openNote(item: DashboardNoteItem): void {
    selectedNote.value = item;
}

function closeNote(): void {
    selectedNote.value = null;
}

function removeNote(itemId: number): void {
    if (selectedNote.value?.itemId === itemId) {
        closeNote();
    }

    emit("remove", itemId);
}
</script>

<template>
    <div class="dashboard-panel-content">
        <div class="dashboard-floating-panel-head">
            <strong>{{ content.title }}</strong>
            <span
                v-if="content.count"
                class="dashboard-panel-count"
            >
                <b>{{ content.count }}</b>
                {{ content.countLabel }}
            </span>
        </div>

        <button
            type="button"
            class="dashboard-panel-create-btn"
            @click="emit('create')"
        >
            <i class="fas fa-plus"></i>
            {{ content.createLabel }}
        </button>

        <div
            v-if="content.items.length"
            class="dashboard-notes-list"
        >
            <div
                v-for="item in content.items"
                :key="item.id"
                class="dashboard-note-item"
            >
                <div class="dashboard-note-date">
                    {{ item.date }}
                </div>

                <div class="dashboard-note-body">
                    <strong>{{ item.title }}</strong>
                    <span>{{ getPreviewText(item.text) }}</span>

                    <button
                        v-if="hasLongText(item.text)"
                        type="button"
                        class="dashboard-note-read-btn"
                        @click="openNote(item)"
                    >
                        {{ readLabel }}
                    </button>
                </div>

                <button
                    v-if="item.itemId && content.removeLabel"
                    type="button"
                    class="dashboard-panel-remove-icon"
                    :aria-label="content.removeLabel"
                    @click="removeNote(item.itemId)"
                >
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </div>

        <div
            v-else
            class="dashboard-panel-empty"
        >
            {{ content.emptyText }}
        </div>

        <RouterLink
            v-if="content.actionTo"
            class="dashboard-panel-link"
            :to="content.actionTo"
        >
            {{ content.actionLabel }}
        </RouterLink>

        <a
            v-else-if="content.actionLabel"
            href="#"
            class="dashboard-panel-link"
        >
            {{ content.actionLabel }}
        </a>

        <Teleport to="body">
            <div
                v-if="selectedNote"
                class="base-modal dashboard-note-reader is-open"
                role="dialog"
                aria-modal="true"
                aria-labelledby="dashboard-note-reader-title"
            >
                <button
                    type="button"
                    class="base-modal__overlay"
                    :aria-label="closeLabel"
                    @click="closeNote"
                ></button>

                <article class="base-modal__dialog dashboard-note-reader__dialog">
                    <header class="base-modal__header">
                        <div>
                            <span class="dashboard-badge">
                                <i class="fas fa-note-sticky"></i>
                                {{ selectedNote.date }}
                            </span>

                            <h2
                                id="dashboard-note-reader-title"
                                class="base-modal__title"
                            >
                                {{ selectedNote.title }}
                            </h2>

                            <p class="base-modal__description">
                                {{ modalTitle }}
                            </p>
                        </div>

                        <button
                            type="button"
                            class="base-modal__close"
                            :aria-label="closeLabel"
                            @click="closeNote"
                        >
                            <i class="fas fa-xmark"></i>
                        </button>
                    </header>

                    <div class="base-modal__body dashboard-note-reader__body">
                        <p>{{ selectedNote.text }}</p>
                    </div>

                    <footer class="base-modal__footer">
                        <button
                            type="button"
                            class="dashboard-create-modal__secondary"
                            @click="closeNote"
                        >
                            {{ closeLabel }}
                        </button>
                    </footer>
                </article>
            </div>
        </Teleport>
    </div>
</template>
