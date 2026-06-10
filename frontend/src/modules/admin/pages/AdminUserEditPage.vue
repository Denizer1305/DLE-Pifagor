<script setup lang="ts">
import { onMounted } from "vue";

import DashboardPageScaffold from "@/components/dashboard/layout/DashboardPageScaffold.vue";
import { useDashboardLogout } from "@/composables/dashboard/useDashboardLogout";
import AdminUserEditForm from "@/modules/admin/components/users/AdminUserEditForm.vue";
import { useAdminDashboard } from "@/modules/admin/composables/useAdminDashboard";
import { useAdminUserEdit } from "@/modules/admin/composables/useAdminUserEdit";

const { logout } = useDashboardLogout();
const {
    errorMessage: shellError,
    isLoading: isShellLoading,
    loadDashboard,
    viewModel,
} = useAdminDashboard();
const edit = useAdminUserEdit();

onMounted(() => {
    void edit.loadUser();
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
        <AdminUserEditForm
            :user="edit.user.value"
            :form="edit.form"
            :is-loading="edit.isLoading.value"
            :is-saving="edit.isSaving.value"
            :error-message="edit.errorMessage.value"
            :save-message="edit.saveMessage.value"
            @reload="edit.loadUser"
            @submit="edit.submit"
        />
    </DashboardPageScaffold>
</template>
