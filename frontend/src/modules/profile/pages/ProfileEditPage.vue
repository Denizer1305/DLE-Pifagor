<script setup lang="ts">
import { computed } from "vue";
import { RouterLink, useRouter } from "vue-router";

import DashboardPageScaffold from "@/components/dashboard/layout/DashboardPageScaffold.vue";

import ProfileEditAvatarCard from "@/modules/profile/components/ProfileEditAvatarCard.vue";
import ProfileEditFormSection from "@/modules/profile/components/ProfileEditFormSection.vue";
import ProfileEditRoleFields from "@/modules/profile/components/ProfileEditRoleFields.vue";

import { useProfileEditForm } from "@/modules/profile/composables/useProfileEditForm";
import { redirectAfterLogout } from "@/modules/auth/utils/auth-redirect.utils";
import { useAuthStore } from "@/stores/auth.store";

const router = useRouter();
const authStore = useAuthStore();

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
        :error-message="errors.common"
        loading-text="Загружаем форму редактирования профиля..."
        @reload="loadProfileEdit"
        @logout="logout"
    >
        <section class="profile-edit-hero fade-in visible">
            <div
                class="profile-edit-hero-bg"
                aria-hidden="true"
            >
                <div class="profile-edit-hero-circle one"></div>
                <div class="profile-edit-hero-circle two"></div>
                <div class="profile-edit-hero-glow one"></div>
                <div class="profile-edit-hero-glow two"></div>
            </div>

            <div class="profile-edit-hero-layout">
                <div class="profile-edit-hero-copy">
                    <div class="profile-edit-hero-topline">
                        <i class="fas fa-pen"></i>
                        Редактирование профиля
                    </div>

                    <h1 class="profile-edit-hero-title">
                        Обновление личных и ролевых данных
                    </h1>

                    <p class="profile-edit-hero-text">
                        Здесь можно изменить основную информацию аккаунта, способы связи,
                        настройки отображения и профессиональные данные, связанные с ролью пользователя.
                    </p>

                    <div class="profile-edit-hero-badges">
                        <span class="profile-edit-hero-badge">
                            <i class="fas fa-user"></i>
                            Общие данные
                        </span>

                        <span class="profile-edit-hero-badge">
                            <i class="fas fa-id-badge"></i>
                            Ролевая информация
                        </span>

                        <span class="profile-edit-hero-badge">
                            <i class="fas fa-shield-check"></i>
                            Безопасное обновление
                        </span>
                    </div>
                </div>

                <div class="profile-edit-hero-actions">
                    <button
                        type="button"
                        class="profile-edit-main-btn"
                        :disabled="isSubmitting"
                        @click="submitForm"
                    >
                        <i class="fas fa-floppy-disk"></i>
                        {{ isSubmitting ? "Сохраняем..." : "Сохранить изменения" }}
                    </button>

                    <RouterLink
                        class="profile-edit-secondary-btn"
                        :to="{ name: 'profile' }"
                    >
                        <i class="fas fa-arrow-left"></i>
                        Вернуться в профиль
                    </RouterLink>
                </div>
            </div>
        </section>

        <div
            v-if="successMessage"
            class="dashboard-state-view is-empty"
        >
            <div class="dashboard-state-view__icon">
                <i class="fas fa-circle-check"></i>
            </div>

            <div class="dashboard-state-view__content">
                <strong>Изменения сохранены</strong>
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

            <section class="profile-edit-section fade-in visible">
                <div class="profile-edit-actions-card">
                    <div>
                        <strong>Готово к сохранению?</strong>
                        <span>
                            Проверьте данные перед отправкой. Часть изменений может пройти модерацию.
                        </span>
                    </div>

                    <div class="profile-edit-actions">
                        <RouterLink
                            class="profile-edit-secondary-btn"
                            :to="{ name: 'profile' }"
                        >
                            Отмена
                        </RouterLink>

                        <button
                            type="submit"
                            class="profile-edit-main-btn"
                            :disabled="isSubmitting"
                        >
                            <i class="fas fa-floppy-disk"></i>
                            {{ isSubmitting ? "Сохраняем..." : "Сохранить профиль" }}
                        </button>
                    </div>
                </div>
            </section>
        </form>
    </DashboardPageScaffold>

    <div
        v-else
        class="dashboard-loading-state"
    >
        <i class="fas fa-spinner"></i>
        <span>Загружаем форму редактирования профиля...</span>
    </div>
</template>
