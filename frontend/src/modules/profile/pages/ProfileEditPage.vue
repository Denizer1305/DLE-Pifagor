<script setup lang="ts">
import { computed } from "vue";

import ProfileEditAvatarCard from "@/modules/profile/components/ProfileEditAvatarCard.vue";
import ProfileEditFormSection from "@/modules/profile/components/ProfileEditFormSection.vue";
import ProfileEditHero from "@/modules/profile/components/ProfileEditHero.vue";
import ProfileEditRoleFields from "@/modules/profile/components/ProfileEditRoleFields.vue";
import ProfileEditSubmitActions from "@/modules/profile/components/ProfileEditSubmitActions.vue";
import ProfilePageShell from "@/modules/profile/components/ProfilePageShell.vue";

import { useProfileEditForm } from "@/modules/profile/composables/useProfileEditForm";
import { profileEditPageContent } from "@/modules/profile/data/profile-edit.data";

const {
    source,
    pageModel,
    form,
    errors,
    isLoading,
    isSubmitting,
    isAvatarSubmitting,
    successMessage,
    citySuggestions,
    isCitySuggestionsLoading,
    loadProfileEdit,
    submitForm,
    uploadAvatar,
    deleteAvatar,
    searchCities,
    selectCity,
} = useProfileEditForm();

const avatarUrl = computed(() => {
    return pageModel.value?.hero.avatarUrl || "";
});

const avatarAlt = computed(() => {
    return pageModel.value?.hero.avatarAlt || "Профиль пользователя";
});

const roleCode = computed(() => {
    return source.value?.active_role.code || "";
});

</script>

<template>
    <ProfilePageShell
        :model="pageModel?.scaffold"
        :is-loading="isLoading"
        :error-message="errors.common"
        loading-text="Загружаем форму редактирования профиля..."
        @reload="loadProfileEdit"
    >
        <template v-if="pageModel">
        <ProfileEditHero
            :content="profileEditPageContent.hero"
            :is-submitting="isSubmitting"
            @submit="submitForm"
        />

        <div
            v-if="successMessage"
            class="dashboard-state-view is-empty"
        >
            <div class="dashboard-state-view__icon">
                <i :class="profileEditPageContent.successIcon"></i>
            </div>

            <div class="dashboard-state-view__content">
                <strong>{{ profileEditPageContent.successTitle }}</strong>
                <p>{{ successMessage }}</p>
            </div>
        </div>

        <form
            id="profileEditForm"
            class="profile-edit-form"
            @submit.prevent="submitForm"
        >
            <ProfileEditAvatarCard
                :avatar-url="avatarUrl"
                :avatar-alt="avatarAlt"
                :is-submitting="isAvatarSubmitting"
                @upload="uploadAvatar"
                @delete="deleteAvatar"
            />

            <ProfileEditFormSection
                :form="form"
                :errors="errors"
                :city-suggestions="citySuggestions"
                :is-city-suggestions-loading="isCitySuggestionsLoading"
                @search-city="searchCities"
                @select-city="selectCity"
            />

            <ProfileEditRoleFields
                :role-code="roleCode"
                :form="form"
            />

            <ProfileEditSubmitActions
                :content="profileEditPageContent.submit"
                :is-submitting="isSubmitting"
            />
        </form>
        </template>
    </ProfilePageShell>
</template>
