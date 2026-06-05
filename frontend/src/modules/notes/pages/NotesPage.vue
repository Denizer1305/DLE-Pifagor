<script setup lang="ts">
import { RouterLink } from "vue-router";

import DashboardCreateItemModal from "@/components/dashboard/panels/DashboardCreateItemModal.vue";
import DashboardPageScaffold from "@/components/dashboard/layout/DashboardPageScaffold.vue";
import DashboardStateView from "@/components/dashboard/shared/DashboardStateView.vue";

import { useDashboardLogout } from "@/composables/dashboard/useDashboardLogout";
import { useNotesPage } from "@/modules/notes/composables/useNotesPage";

const { logout } = useDashboardLogout();

const {
    calendarRoute,
    content,
    errorMessage,
    isCreateModalOpen,
    isLoading,
    isSaving,
    model,
    notes,
    saveError,
    selectedNote,
    stats,
    closeCreateModal,
    closeNote,
    deleteNote,
    loadNotes,
    openCreateModal,
    openNote,
    submitCreateModal,
} = useNotesPage();
</script>

<template>
    <DashboardPageScaffold
        :model="model"
        :is-loading="false"
        error-message=""
        :loading-text="content.loadingText"
        @reload="loadNotes"
        @logout="logout"
    >
        <DashboardStateView
            v-if="isLoading"
            variant="loading"
            :text="content.loadingText"
        />

        <DashboardStateView
            v-else-if="errorMessage"
            variant="error"
            :title="content.errorTitle"
            :text="errorMessage"
            :action-label="content.retryLabel"
            :action-icon="content.retryIcon"
            @action="loadNotes"
        />

        <template v-else>
            <section class="notes-page-hero fade-in visible">
                <div>
                    <span class="dashboard-badge">
                        <i class="fas fa-note-sticky"></i>
                        {{ content.hero.badge }}
                    </span>

                    <h1>{{ content.hero.title }}</h1>
                    <p>{{ content.hero.text }}</p>
                </div>

                <div class="notes-page-actions">
                    <button
                        type="button"
                        class="dashboard-create-modal__primary"
                        @click="openCreateModal"
                    >
                        <i class="fas fa-plus"></i>
                        {{ content.actions.createLabel }}
                    </button>

                    <RouterLink
                        class="dashboard-create-modal__secondary"
                        :to="calendarRoute"
                    >
                        <i class="fas fa-calendar-days"></i>
                        {{ content.actions.openCalendarLabel }}
                    </RouterLink>
                </div>
            </section>

            <section class="notes-page-stats">
                <article class="notes-page-stat">
                    <span>{{ content.stats.totalLabel }}</span>
                    <strong>{{ stats.total }}</strong>
                </article>
                <article class="notes-page-stat">
                    <span>{{ content.stats.upcomingLabel }}</span>
                    <strong>{{ stats.upcoming }}</strong>
                </article>
                <article class="notes-page-stat">
                    <span>{{ content.stats.todayLabel }}</span>
                    <strong>{{ stats.today }}</strong>
                </article>
            </section>

            <section class="notes-page-card">
                <div class="notes-page-section-head">
                    <div>
                        <span class="dashboard-badge">
                            <i class="fas fa-list"></i>
                            {{ content.list.title }}
                        </span>
                        <p>{{ content.list.subtitle }}</p>
                    </div>
                </div>

                <div
                    v-if="notes.length"
                    class="notes-page-list"
                >
                    <article
                        v-for="note in notes"
                        :key="note.id"
                        class="notes-page-note"
                        :class="{ 'is-today': note.isToday, 'is-past': note.isPast }"
                    >
                        <div class="notes-page-note-date">
                            <span>{{ note.dateLabel }}</span>
                        </div>

                        <div class="notes-page-note-body">
                            <strong>{{ note.title }}</strong>
                            <p>{{ note.previewText }}</p>

                            <button
                                v-if="note.hasLongText"
                                type="button"
                                class="notes-page-read-btn"
                                @click="openNote(note)"
                            >
                                {{ content.actions.readLabel }}
                            </button>
                        </div>

                        <button
                            type="button"
                            class="dashboard-panel-remove-icon"
                            :aria-label="content.actions.deleteLabel"
                            @click="deleteNote(note.id)"
                        >
                            <i class="fas fa-trash"></i>
                        </button>
                    </article>
                </div>

                <div
                    v-else
                    class="dashboard-empty-state"
                >
                    <i class="fas fa-note-sticky"></i>
                    <div>
                        <strong>{{ content.list.emptyTitle }}</strong>
                        <p>{{ content.list.emptyText }}</p>
                    </div>
                </div>
            </section>
        </template>

        <DashboardCreateItemModal
            :is-open="isCreateModalOpen"
            kind="note"
            :content="content.modal"
            :is-submitting="isSaving"
            :error-message="saveError"
            @close="closeCreateModal"
            @submit="submitCreateModal"
        />

        <Teleport to="body">
            <div
                v-if="selectedNote"
                class="base-modal notes-page-reader is-open"
                role="dialog"
                aria-modal="true"
                aria-labelledby="notes-page-reader-title"
            >
                <button
                    type="button"
                    class="base-modal__overlay"
                    :aria-label="content.actions.closeLabel"
                    @click="closeNote"
                ></button>

                <article class="base-modal__dialog notes-page-reader__dialog">
                    <header class="base-modal__header">
                        <div>
                            <span class="dashboard-badge">
                                <i class="fas fa-note-sticky"></i>
                                {{ selectedNote.dateLabel }}
                            </span>

                            <h2
                                id="notes-page-reader-title"
                                class="base-modal__title"
                            >
                                {{ selectedNote.title }}
                            </h2>

                            <p class="base-modal__description">
                                {{ content.reader.title }}
                            </p>
                        </div>

                        <button
                            type="button"
                            class="base-modal__close"
                            :aria-label="content.actions.closeLabel"
                            @click="closeNote"
                        >
                            <i class="fas fa-xmark"></i>
                        </button>
                    </header>

                    <div class="base-modal__body notes-page-reader__body">
                        <p>{{ selectedNote.text }}</p>
                    </div>

                    <footer class="base-modal__footer">
                        <button
                            type="button"
                            class="dashboard-create-modal__secondary"
                            @click="closeNote"
                        >
                            {{ content.actions.closeLabel }}
                        </button>
                    </footer>
                </article>
            </div>
        </Teleport>
    </DashboardPageScaffold>
</template>
