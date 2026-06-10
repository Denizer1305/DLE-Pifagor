<script setup lang="ts">
import DashboardStateView from "@/components/dashboard/shared/DashboardStateView.vue";

import OrganizationToolbar from "./OrganizationToolbar.vue";
import type { EmptyStateView } from "../../types";

interface Props {
    searchValue: string;
    searchPlaceholder: string;
    isLoading: boolean;
    isActionLoading?: boolean;
    hasActiveFilters?: boolean;
    isEmpty: boolean;
    errorMessage?: string;
    emptyState: EmptyStateView;
    filtersLabel?: string;
    refreshLabel?: string;
    createLabel?: string;
    retryLabel?: string;
}

interface Emits {
    (event: "update:searchValue", value: string): void;
    (event: "search"): void;
    (event: "refresh"): void;
    (event: "create"): void;
}

withDefaults(defineProps<Props>(), {
    isActionLoading: false,
    hasActiveFilters: false,
    errorMessage: "",
    filtersLabel: "Фильтры",
    refreshLabel: "Обновить",
    createLabel: "",
    retryLabel: "Повторить",
});

defineEmits<Emits>();
</script>

<template>
    <div class="org-page__main org-page__main--wide">
        <OrganizationToolbar
            :search-value="searchValue"
            :search-placeholder="searchPlaceholder"
            :is-loading="isLoading || isActionLoading"
            :filters-label="filtersLabel"
            :refresh-label="refreshLabel"
            :create-label="createLabel"
            :has-active-filters="hasActiveFilters"
            @update:search-value="$emit('update:searchValue', $event)"
            @search="$emit('search')"
            @refresh="$emit('refresh')"
            @create="$emit('create')"
        >
            <template #filters>
                <slot name="filters" />
            </template>
        </OrganizationToolbar>

        <DashboardStateView
            v-if="isLoading"
            variant="loading"
            :text="emptyState.text"
        />

        <DashboardStateView
            v-else-if="errorMessage"
            variant="error"
            :title="errorMessage"
            :text="emptyState.text"
            :action-label="retryLabel"
            action-icon="fas fa-rotate-right"
            @action="$emit('refresh')"
        />

        <DashboardStateView
            v-else-if="isEmpty"
            variant="empty"
            :title="emptyState.title"
            :text="emptyState.text"
            :action-label="emptyState.actionLabel"
            action-icon="fas fa-plus"
            @action="$emit('create')"
        />

        <slot v-else />

        <slot name="details" />
    </div>
</template>
