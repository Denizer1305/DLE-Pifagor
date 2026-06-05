<script setup lang="ts">
import { onMounted } from "vue";

import DashboardPageScaffold from "@/components/dashboard/layout/DashboardPageScaffold.vue";
import { useDashboardLogout } from "@/composables/dashboard/useDashboardLogout";
import AdminUserDetailView from "@/modules/admin/components/users/AdminUserDetailView.vue";
import { useAdminDashboard } from "@/modules/admin/composables/useAdminDashboard";
import { useAdminUserDetail } from "@/modules/admin/composables/useAdminUserDetail";

const { logout } = useDashboardLogout();
const {
    errorMessage: shellError,
    isLoading: isShellLoading,
    loadDashboard,
    viewModel,
} = useAdminDashboard();
const detail = useAdminUserDetail();

onMounted(() => {
    void detail.loadUser();
});
</script>

<template>
    <DashboardPageScaffold
        :model="viewModel"
        :is-loading="isShellLoading"
        :error-message="shellError"
        loading-text="Загружаем кабинет администратора..."
        error-title="Не удалось загрузить кабинет"
        retry-label="Повторить"
        retry-icon="fas fa-rotate"
        @reload="loadDashboard"
        @logout="logout"
    >
        <AdminUserDetailView
            :user="detail.user.value"
            :is-loading="detail.isLoading.value"
            :updating-action="detail.updatingAction.value"
            :error-message="detail.errorMessage.value"
            @reload="detail.loadUser"
            @status-action="detail.runStatusAction"
        />
    </DashboardPageScaffold>
</template>
