<script setup lang="ts">
import type { EmptyStateView } from "../../types";

interface Props {
    isLoading?: boolean;
    isError?: boolean;
    errorMessage?: string;
    emptyState?: EmptyStateView | null;
    isEmpty?: boolean;
    retryLabel?: string;
}

interface Emits {
    (event: "retry"): void;
    (event: "empty-action"): void;
}

withDefaults(defineProps<Props>(), {
    isLoading: false,
    isError: false,
    errorMessage: "",
    emptyState: null,
    isEmpty: false,
    retryLabel: "",
});

defineEmits<Emits>();
</script>

<template>
    <div
        v-if="isLoading"
        class="org-table__loading"
    >
        <slot name="loading">
            <div class="org-table__skeleton">
                <div class="org-table__skeleton-row" />
                <div class="org-table__skeleton-row" />
                <div class="org-table__skeleton-row" />
            </div>
        </slot>
    </div>

    <div
        v-else-if="isError"
        class="org-empty org-empty--compact"
    >
        <div class="org-empty__content">
            <div class="org-empty__icon">
                <slot name="error-icon">
                    <i class="fas fa-triangle-exclamation"></i>
                </slot>
            </div>

            <h3 class="org-empty__title">
                {{ errorMessage }}
            </h3>

            <div
                v-if="retryLabel"
                class="org-empty__actions"
            >
                <button
                    class="org-empty__button org-empty__button--primary"
                    type="button"
                    @click="$emit('retry')"
                >
                    {{ retryLabel }}
                </button>
            </div>
        </div>
    </div>

    <div
        v-else-if="isEmpty && emptyState"
        class="org-empty"
    >
        <div class="org-empty__content">
            <div class="org-empty__icon">
                <slot
                    name="empty-icon"
                    :icon="emptyState.icon"
                >
                    <i class="fas fa-circle-info"></i>
                </slot>
            </div>

            <h3 class="org-empty__title">
                {{ emptyState.title }}
            </h3>

            <p class="org-empty__text">
                {{ emptyState.text }}
            </p>

            <div
                v-if="emptyState.actionLabel"
                class="org-empty__actions"
            >
                <button
                    class="org-empty__button org-empty__button--primary"
                    type="button"
                    @click="$emit('empty-action')"
                >
                    {{ emptyState.actionLabel }}
                </button>
            </div>
        </div>
    </div>

    <slot v-else />
</template>
