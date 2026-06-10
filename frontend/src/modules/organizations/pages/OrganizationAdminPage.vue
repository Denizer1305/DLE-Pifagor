<script setup lang="ts">
import DashboardPageScaffold from "@/components/dashboard/layout/DashboardPageScaffold.vue";
import { useDashboardLogout } from "@/composables/dashboard/useDashboardLogout";
import { useAdminDashboard } from "@/modules/admin/composables/useAdminDashboard";

import OrganizationDashboardWorkspace from "../components/shared/OrganizationDashboardWorkspace.vue";
import { useOrganizationAdminPage } from "../composables";

const { logout } = useDashboardLogout();
const {
    errorMessage: shellError,
    isLoading: isShellLoading,
    loadDashboard,
    viewModel,
} = useAdminDashboard();

const {
    navigation,
    rootHeader,
    summary,
} = useOrganizationAdminPage();
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
        <OrganizationDashboardWorkspace
            :header="rootHeader"
            :navigation="navigation"
            :summary="summary"
        />
    </DashboardPageScaffold>
</template>
