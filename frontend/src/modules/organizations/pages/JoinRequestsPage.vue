<script setup lang="ts">
import { computed, onMounted, ref } from "vue";

import DashboardStateView from "@/components/dashboard/shared/DashboardStateView.vue";

import JoinRequestDetailsPanel from "../components/join-requests/JoinRequestDetailsPanel.vue";
import JoinRequestListTable from "../components/join-requests/JoinRequestListTable.vue";
import JoinRequestReviewModal from "../components/join-requests/JoinRequestReviewModal.vue";
import OrganizationDetailsModal from "../components/shared/OrganizationDetailsModal.vue";
import OrganizationWorkspace from "../components/shared/OrganizationWorkspace.vue";
import { useJoinRequests } from "../composables";
import type {
    JoinRequestId,
    JoinRequestListItemView,
    OrganizationTableActionKey,
} from "../types";

type ReviewMode = "approve" | "reject";

const {
    emptyState,
    errorMessage,
    fieldErrors,
    filters,
    hasItems,
    isDetailsLoading,
    isLoading,
    isReviewSubmitting,
    reviewForm,
    selectedDetails,
    tableConfig,
    viewItems,
    approveItem,
    clearSelection,
    loadItems,
    rejectItem,
    resetReviewForm,
    selectItem,
    setSearch,
    submitSearch,
} = useJoinRequests();

const reviewMode = ref<ReviewMode | null>(null);
const reviewRequestId = ref<JoinRequestId | null>(null);

const hasActiveFilters = computed(() => {
    return Boolean(filters.search);
});

const reviewTitle = computed(() => {
    return reviewMode.value === "reject"
        ? "Отклонить заявку"
        : "Принять заявку";
});

const reviewText = computed(() => {
    return reviewMode.value === "reject"
        ? "Добавьте комментарий, чтобы пользователь понял причину отклонения."
        : "При необходимости оставьте комментарий к принятому решению.";
});

function openReviewModal(mode: ReviewMode, id: JoinRequestId): void {
    reviewMode.value = mode;
    reviewRequestId.value = id;
    resetReviewForm();
}

function closeReviewModal(): void {
    reviewMode.value = null;
    reviewRequestId.value = null;
    resetReviewForm();
}

function handleTableAction(payload: {
    actionKey: OrganizationTableActionKey;
    item: JoinRequestListItemView;
}): void {
    if (payload.actionKey === "details") {
        selectItem(payload.item.id);
        return;
    }

    if (payload.actionKey === "approve") {
        openReviewModal("approve", payload.item.id);
        return;
    }

    if (payload.actionKey === "reject") {
        openReviewModal("reject", payload.item.id);
    }
}

async function submitReview(): Promise<void> {
    if (!reviewRequestId.value || !reviewMode.value) {
        return;
    }

    if (reviewMode.value === "approve") {
        await approveItem(reviewRequestId.value);
    } else {
        await rejectItem(reviewRequestId.value);
    }

    closeReviewModal();
}

onMounted(() => {
    void loadItems();
});
</script>

<template>
    <OrganizationWorkspace
        :search-value="filters.search"
        search-placeholder="Поиск по пользователю, организации или сообщению"
        :is-loading="isLoading"
        :is-action-loading="isReviewSubmitting"
        :has-active-filters="hasActiveFilters"
        :is-empty="!hasItems"
        :error-message="errorMessage"
        :empty-state="emptyState"
        filters-label="Найти"
        refresh-label="Обновить"
        @update:search-value="setSearch"
        @search="submitSearch"
        @refresh="loadItems"
    >
        <JoinRequestListTable
            :items="viewItems"
            :columns="tableConfig.columns"
            :actions="tableConfig.actions"
            @select="selectItem($event.id)"
            @action="handleTableAction"
        />

        <template #details>
            <OrganizationDetailsModal
                :is-open="Boolean(selectedDetails) || isDetailsLoading"
                title="Карточка заявки"
                @close="clearSelection"
            >
                <DashboardStateView
                    v-if="isDetailsLoading"
                    variant="loading"
                    text="Загружаем данные заявки..."
                />

                <JoinRequestDetailsPanel
                    v-else
                    :details="selectedDetails"
                    @close="clearSelection"
                />
            </OrganizationDetailsModal>

            <JoinRequestReviewModal
                :is-open="Boolean(reviewMode)"
                v-model="reviewForm"
                :title="reviewTitle"
                :text="reviewText"
                :tone="reviewMode === 'reject' ? 'danger' : 'success'"
                :submit-label="reviewMode === 'reject' ? 'Отклонить' : 'Принять'"
                cancel-label="Отмена"
                :is-submitting="isReviewSubmitting"
                :errors="fieldErrors"
                @submit="submitReview"
                @cancel="closeReviewModal"
                @close="closeReviewModal"
            />
        </template>
    </OrganizationWorkspace>
</template>
