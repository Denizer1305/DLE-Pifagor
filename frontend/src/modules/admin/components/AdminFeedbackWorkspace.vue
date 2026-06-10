<script setup lang="ts">
import { nextTick, ref, watch } from "vue";

import BaseSelect from "@/components/base/BaseSelect.vue";
import DashboardStateView from "@/components/dashboard/shared/DashboardStateView.vue";
import {
    adminFeedbackContent,
    adminFeedbackStatusOptions,
    adminFeedbackTopicOptions,
    getFeedbackStatusLabel,
    getFeedbackTopicLabel,
} from "@/modules/admin/data/admin-feedback.data";
import type {
    AdminFeedbackFilters,
    AdminFeedbackList,
    AdminFeedbackRequest,
    AdminFeedbackStatus,
} from "@/modules/admin/types/admin-feedback.types";

interface Props {
    feedback: AdminFeedbackList;
    filters: AdminFeedbackFilters;
    isLoading: boolean;
    updatingId: number | null;
    errorMessage: string;
    focusedRequestId?: number | null;
}

interface Emits {
    (event: "search"): void;
    (event: "set-filter", key: "status" | "topic", value: string): void;
    (event: "set-search", value: string): void;
    (event: "update-status", requestId: number, status: AdminFeedbackStatus): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();
const selectedRequest = ref<AdminFeedbackRequest | null>(null);

function formatCreatedAt(value: string): string {
    return new Intl.DateTimeFormat("ru-RU", {
        dateStyle: "medium",
        timeStyle: "short",
    }).format(new Date(value));
}

function openRequest(request: AdminFeedbackRequest): void {
    selectedRequest.value = request;
}

function closeRequest(): void {
    selectedRequest.value = null;
}

watch(
    () => [props.focusedRequestId, props.feedback.items, props.isLoading] as const,
    async ([requestId]) => {
        if (!requestId || props.isLoading) {
            return;
        }

        const request = props.feedback.items.find((item) => item.id === requestId);

        if (!request) {
            return;
        }

        await nextTick();
        selectedRequest.value = request;
    },
    { immediate: true },
);
</script>

<template>
    <section class="admin-feedback-page fade-in visible">
        <header class="admin-feedback-hero">
            <div class="dashboard-card-topline">
                <i class="fas fa-envelope-open-text"></i>
                {{ adminFeedbackContent.badge }}
            </div>
            <h1>{{ adminFeedbackContent.title }}</h1>
            <p>{{ adminFeedbackContent.text }}</p>
        </header>

        <div class="admin-feedback-summary">
            <article><strong>{{ feedback.summary.total }}</strong><span>Всего</span></article>
            <article><strong>{{ feedback.summary.new }}</strong><span>Новых</span></article>
            <article><strong>{{ feedback.summary.inProgress }}</strong><span>В работе</span></article>
            <article><strong>{{ feedback.summary.answered }}</strong><span>С ответом</span></article>
            <article><strong>{{ feedback.summary.closed }}</strong><span>Закрыто</span></article>
        </div>

        <form class="admin-feedback-filters" @submit.prevent="emit('search')">
            <label class="admin-feedback-search">
                <i class="fas fa-magnifying-glass"></i>
                <input
                    :value="filters.search"
                    type="search"
                    aria-label="Поиск обращений"
                    :placeholder="adminFeedbackContent.searchPlaceholder"
                    @input="emit('set-search', ($event.target as HTMLInputElement).value)"
                />
            </label>

            <BaseSelect
                :model-value="filters.status"
                :options="adminFeedbackStatusOptions"
                aria-label="Фильтр по статусу"
                mode="overlay"
                @update:model-value="emit('set-filter', 'status', $event)"
            />
            <BaseSelect
                :model-value="filters.topic"
                :options="adminFeedbackTopicOptions"
                aria-label="Фильтр по теме"
                mode="overlay"
                @update:model-value="emit('set-filter', 'topic', $event)"
            />
            <button type="submit" class="dashboard-course-btn primary">
                <i class="fas fa-filter"></i>
                Применить
            </button>
        </form>

        <p v-if="errorMessage" class="admin-feedback-error">{{ errorMessage }}</p>

        <DashboardStateView
            v-if="isLoading"
            variant="loading"
            :text="adminFeedbackContent.loadingText"
        />

        <div v-else-if="feedback.items.length" class="admin-feedback-list">
            <article
                v-for="request in feedback.items"
                :key="request.id"
                class="admin-feedback-card"
            >
                <div class="admin-feedback-card-head">
                    <div>
                        <span class="admin-feedback-topic">{{ getFeedbackTopicLabel(request.topic) }}</span>
                        <h2>{{ request.subject || request.fullName }}</h2>
                        <p>{{ request.fullName }} · {{ request.email }}</p>
                    </div>
                    <time>{{ formatCreatedAt(request.createdAt) }}</time>
                </div>

                <p class="admin-feedback-message">{{ request.message }}</p>

                <div
                    v-if="request.attachments.length"
                    class="admin-feedback-attachments"
                >
                    <strong>
                        <i class="fas fa-paperclip"></i>
                        Прикрепленные файлы
                    </strong>

                    <div class="admin-feedback-attachment-list">
                        <a
                            v-for="attachment in request.attachments"
                            :key="attachment.id"
                            :href="attachment.url"
                            class="admin-feedback-attachment"
                            target="_blank"
                            rel="noopener noreferrer"
                        >
                            <i class="fas fa-file-lines"></i>
                            <span>{{ attachment.name }}</span>
                            <small>{{ attachment.sizeLabel }}</small>
                        </a>
                    </div>
                </div>

                <footer class="admin-feedback-card-footer">
                    <div class="admin-feedback-meta">
                        <span v-if="request.organizationName">{{ request.organizationName }}</span>
                        <span v-if="request.phone">{{ request.phone }}</span>
                        <span v-if="request.attachmentCount">
                            <i class="fas fa-paperclip"></i>
                            {{ request.attachmentCount }}
                        </span>
                    </div>

                    <div class="admin-feedback-actions">
                        <button
                            type="button"
                            class="dashboard-course-btn"
                            @click="openRequest(request)"
                        >
                            <i class="fas fa-eye"></i>
                            Подробнее
                        </button>

                        <BaseSelect
                            class="admin-feedback-status"
                            :model-value="request.status"
                            :options="adminFeedbackStatusOptions.slice(1)"
                            :aria-label="`Статус: ${getFeedbackStatusLabel(request.status)}`"
                            :disabled="updatingId === request.id"
                            mode="overlay"
                            @update:model-value="emit('update-status', request.id, $event as AdminFeedbackStatus)"
                        />
                    </div>
                </footer>
            </article>
        </div>

        <div v-else class="admin-feedback-empty">
            <i class="fas fa-inbox"></i>
            <strong>{{ adminFeedbackContent.emptyTitle }}</strong>
            <p>{{ adminFeedbackContent.emptyText }}</p>
        </div>

        <Teleport to="body">
            <div
                v-if="selectedRequest"
                class="base-modal admin-feedback-detail is-open"
                role="dialog"
                aria-modal="true"
                aria-labelledby="admin-feedback-detail-title"
            >
                <button
                    type="button"
                    class="base-modal__overlay"
                    aria-label="Закрыть обращение"
                    @click="closeRequest"
                ></button>

                <article class="base-modal__dialog admin-feedback-detail__dialog">
                    <header class="base-modal__header">
                        <div>
                            <span class="admin-feedback-topic">
                                {{ getFeedbackTopicLabel(selectedRequest.topic) }}
                            </span>
                            <h2 id="admin-feedback-detail-title" class="base-modal__title">
                                {{ selectedRequest.subject || selectedRequest.fullName }}
                            </h2>
                            <p class="base-modal__description">
                                {{ selectedRequest.fullName }} · {{ selectedRequest.email }}
                            </p>
                        </div>

                        <button
                            type="button"
                            class="base-modal__close"
                            aria-label="Закрыть обращение"
                            @click="closeRequest"
                        >
                            <i class="fas fa-xmark"></i>
                        </button>
                    </header>

                    <div class="base-modal__body admin-feedback-detail__body">
                        <dl class="admin-feedback-detail__meta">
                            <div>
                                <dt>Дата</dt>
                                <dd>{{ formatCreatedAt(selectedRequest.createdAt) }}</dd>
                            </div>
                            <div>
                                <dt>Статус</dt>
                                <dd>{{ getFeedbackStatusLabel(selectedRequest.status) }}</dd>
                            </div>
                            <div v-if="selectedRequest.phone">
                                <dt>Телефон</dt>
                                <dd>{{ selectedRequest.phone }}</dd>
                            </div>
                            <div v-if="selectedRequest.organizationName">
                                <dt>Организация</dt>
                                <dd>{{ selectedRequest.organizationName }}</dd>
                            </div>
                        </dl>

                        <section class="admin-feedback-detail__message">
                            <h3>Сообщение</h3>
                            <p>{{ selectedRequest.message }}</p>
                        </section>

                        <section
                            v-if="selectedRequest.attachments.length"
                            class="admin-feedback-attachments"
                        >
                            <strong>
                                <i class="fas fa-paperclip"></i>
                                Прикрепленные файлы
                            </strong>

                            <div class="admin-feedback-attachment-list">
                                <a
                                    v-for="attachment in selectedRequest.attachments"
                                    :key="attachment.id"
                                    :href="attachment.url"
                                    class="admin-feedback-attachment"
                                    target="_blank"
                                    rel="noopener noreferrer"
                                >
                                    <i class="fas fa-file-lines"></i>
                                    <span>{{ attachment.name }}</span>
                                    <small>{{ attachment.sizeLabel }}</small>
                                </a>
                            </div>
                        </section>
                    </div>
                </article>
            </div>
        </Teleport>
    </section>
</template>
