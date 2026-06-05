<script setup lang="ts">
import { onMounted } from "vue";
import { useRoute } from "vue-router";

import DashboardPageScaffold from "@/components/dashboard/layout/DashboardPageScaffold.vue";
import { useDashboardLogout } from "@/composables/dashboard/useDashboardLogout";
import AdminFeedbackWorkspace from "@/modules/admin/components/AdminFeedbackWorkspace.vue";
import { useAdminDashboard } from "@/modules/admin/composables/useAdminDashboard";
import { useAdminFeedback } from "@/modules/admin/composables/useAdminFeedback";
import type {
    AdminFeedbackStatus,
    AdminFeedbackTopic,
} from "@/modules/admin/types/admin-feedback.types";

const { logout } = useDashboardLogout();
const route = useRoute();
const {
    errorMessage: shellError,
    isLoading: isShellLoading,
    loadDashboard,
    viewModel,
} = useAdminDashboard();
const {
    filters,
    feedback,
    isLoading,
    updatingId,
    errorMessage,
    loadFeedback,
    updateStatus,
} = useAdminFeedback();

function setFilter(key: "status" | "topic", value: string): void {
    if (key === "status") {
        filters.status = value as AdminFeedbackStatus | "";
    } else {
        filters.topic = value as AdminFeedbackTopic | "";
    }

    void loadFeedback();
}

function setSearch(value: string): void {
    filters.search = value;
}

async function handleStatusUpdate(requestId: number, status: AdminFeedbackStatus): Promise<void> {
    await updateStatus(requestId, status);
    await loadDashboard();
}

onMounted(() => {
    void loadFeedback();
});
</script>

<template>
    <DashboardPageScaffold
        :model="viewModel"
        :is-loading="isShellLoading"
        :error-message="shellError"
        loading-text="Загружаем кабинет администратора..."
        error-title="Не удалось загрузить кабинет"
        retry-label="Попробовать снова"
        retry-icon="fas fa-rotate"
        @reload="loadDashboard"
        @logout="logout"
    >
        <AdminFeedbackWorkspace
            :feedback="feedback"
            :filters="filters"
            :is-loading="isLoading"
            :updating-id="updatingId"
            :error-message="errorMessage"
            :focused-request-id="Number(route.query.request) || null"
            @search="loadFeedback"
            @set-filter="setFilter"
            @set-search="setSearch"
            @update-status="handleStatusUpdate"
        />
    </DashboardPageScaffold>
</template>
