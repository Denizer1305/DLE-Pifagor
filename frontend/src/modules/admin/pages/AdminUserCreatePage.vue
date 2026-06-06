<script setup lang="ts">
import DashboardPageScaffold from "@/components/dashboard/layout/DashboardPageScaffold.vue";
import { useDashboardLogout } from "@/composables/dashboard/useDashboardLogout";
import AdminUserCreateForm from "@/modules/admin/components/users/AdminUserCreateForm.vue";
import { useAdminDashboard } from "@/modules/admin/composables/useAdminDashboard";
import { useAdminUserCreate } from "@/modules/admin/composables/useAdminUserCreate";

const { logout } = useDashboardLogout();
const {
    errorMessage: shellError,
    isLoading: isShellLoading,
    loadDashboard,
    viewModel,
} = useAdminDashboard();
const create = useAdminUserCreate();
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
        <AdminUserCreateForm
            :form="create.form"
            :is-saving="create.isSaving.value"
            :error-message="create.errorMessage.value"
            :save-message="create.saveMessage.value"
            @submit="create.submit"
            @phone-input="create.handlePhoneInput"
        />
    </DashboardPageScaffold>
</template>
