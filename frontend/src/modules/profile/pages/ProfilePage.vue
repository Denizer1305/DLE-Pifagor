<script setup lang="ts">
import { useRouter } from "vue-router";

import DashboardPageScaffold from "@/components/dashboard/layout/DashboardPageScaffold.vue";

import ProfileContactsCard from "@/modules/profile/components/ProfileContactsCard.vue";
import ProfileHeroSection from "@/modules/profile/components/ProfileHeroSection.vue";
import ProfileIdentityCard from "@/modules/profile/components/ProfileIdentityCard.vue";
import ProfileRoleSection from "@/modules/profile/components/ProfileRoleSection.vue";

import { useProfilePage } from "@/modules/profile/composables/useProfilePage";
import { redirectAfterLogout } from "@/modules/auth/utils/auth-redirect.utils";
import { useAuthStore } from "@/stores/auth.store";

const router = useRouter();
const authStore = useAuthStore();

const {
    pageModel,
    isLoading,
    errorMessage,
    loadProfile,
} = useProfilePage();

async function logout(): Promise<void> {
    await authStore.logout();
    await redirectAfterLogout(router);
}
</script>

<template>
    <DashboardPageScaffold
        v-if="pageModel"
        :model="pageModel.scaffold"
        :is-loading="isLoading"
        :error-message="errorMessage"
        loading-text="Загружаем профиль пользователя..."
        @reload="loadProfile"
        @logout="logout"
    >
        <ProfileHeroSection :hero="pageModel.hero" />

        <ProfileIdentityCard :card="pageModel.identityCard" />

        <ProfileContactsCard :card="pageModel.contactsCard" />

        <ProfileRoleSection :section="pageModel.roleSection" />
    </DashboardPageScaffold>

    <div
        v-else
        class="dashboard-loading-state"
    >
        <i class="fas fa-spinner"></i>
        <span>Загружаем профиль пользователя...</span>
    </div>
</template>