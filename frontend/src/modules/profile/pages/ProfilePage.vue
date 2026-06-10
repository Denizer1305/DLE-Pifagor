<script setup lang="ts">
import ProfilePageShell from "@/modules/profile/components/ProfilePageShell.vue";

import ProfileContactsCard from "@/modules/profile/components/ProfileContactsCard.vue";
import ProfileHeroSection from "@/modules/profile/components/ProfileHeroSection.vue";
import ProfileIdentityCard from "@/modules/profile/components/ProfileIdentityCard.vue";
import ProfileRoleSection from "@/modules/profile/components/ProfileRoleSection.vue";

import { useProfilePage } from "@/modules/profile/composables/useProfilePage";

const {
    pageModel,
    isLoading,
    errorMessage,
    loadProfile,
} = useProfilePage();

</script>

<template>
    <ProfilePageShell
        :model="pageModel?.scaffold"
        :is-loading="isLoading"
        :error-message="errorMessage"
        loading-text="Загружаем профиль пользователя..."
        @reload="loadProfile"
    >
        <template v-if="pageModel">
        <ProfileHeroSection :hero="pageModel.hero" />

        <ProfileIdentityCard :card="pageModel.identityCard" />

        <ProfileContactsCard :card="pageModel.contactsCard" />

        <ProfileRoleSection :section="pageModel.roleSection" />
        </template>
    </ProfilePageShell>
</template>
