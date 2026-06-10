<script setup lang="ts">
import { onMounted } from "vue";

import DashboardPageScaffold from "@/components/dashboard/layout/DashboardPageScaffold.vue";
import { useDashboardLogout } from "@/composables/dashboard/useDashboardLogout";
import AdminUsersWorkspace from "@/modules/admin/components/users/AdminUsersWorkspace.vue";
import { useAdminDashboard } from "@/modules/admin/composables/useAdminDashboard";
import { useAdminUsers } from "@/modules/admin/composables/useAdminUsers";

const { logout } = useDashboardLogout();
const {
    errorMessage: shellError,
    isLoading: isShellLoading,
    loadDashboard,
    viewModel,
} = useAdminDashboard();
const users = useAdminUsers();

onMounted(() => {
    void users.loadUsers();
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
        <AdminUsersWorkspace
            :model="users.model.value"
            :filters="users.filters"
            :is-loading="users.isLoading.value"
            :error-message="users.errorMessage.value"
            :can-go-previous="users.canGoPrevious.value"
            :can-go-next="users.canGoNext.value"
            @reload="users.loadUsers"
            @search="users.submitSearch"
            @reset="users.resetFilters"
            @set-search="users.setSearch"
            @set-filter="users.setFilter"
            @previous="users.goPrevious"
            @next="users.goNext"
        />
    </DashboardPageScaffold>
</template>
