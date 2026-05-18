<script setup lang="ts">
import { RouterLink } from "vue-router";

import AuthMessageModal from "@/modules/auth/components/AuthMessageModal.vue";
import AuthSubmitButton from "@/modules/auth/components/AuthSubmitButton.vue";
import RegisterAgreement from "@/modules/auth/components/register/RegisterAgreement.vue";
import RegisterContactFields from "@/modules/auth/components/register/RegisterContactFields.vue";
import RegisterPasswordFields from "@/modules/auth/components/register/RegisterPasswordFields.vue";
import RegisterPersonalFields from "@/modules/auth/components/register/RegisterPersonalFields.vue";
import RegisterRoleSwitcher from "@/modules/auth/components/register/RegisterRoleSwitcher.vue";
import RegisterSuccessState from "@/modules/auth/components/register/RegisterSuccessState.vue";
import { useRegistrationForm } from "@/modules/auth/composables/useRegistrationForm";

const {
    form,
    errors,
    modal,
    selectedRole,
    currentStep,
    stepTitle,
    stepDescription,
    isSubmitting,
    isRegistered,

    closeModal,
    goNextStep,
    goPreviousStep,
    submitForm,
    goToLogin,
} = useRegistrationForm();
</script>

<template>
    <AuthMessageModal
        :is-open="modal.isOpen"
        :title="modal.title"
        :message="modal.message"
        :type="modal.type"
        @close="closeModal"
    />

    <RegisterSuccessState
        v-if="isRegistered"
        @go-login="goToLogin"
    />

    <form
        v-else
        class="registration-form registration-form--stepped"
        novalidate
        @submit.prevent="submitForm"
    >
        <input
            class="visually-hidden"
            type="text"
            name="username"
            autocomplete="username"
            :value="form.email"
            tabindex="-1"
            aria-hidden="true"
        />

        <div class="registration-progress">
            <div class="registration-progress__top">
                <span>Шаг {{ currentStep }} из 2</span>
                <strong>{{ stepTitle }}</strong>
            </div>

            <div class="registration-progress__bar">
                <span :style="{ width: currentStep === 1 ? '50%' : '100%' }"></span>
            </div>

            <p>{{ stepDescription }}</p>
        </div>

        <template v-if="currentStep === 1">
            <RegisterRoleSwitcher v-model="selectedRole" />

            <RegisterPersonalFields
                :form="form"
                :errors="errors"
                :role="selectedRole"
            />

            <RegisterContactFields
                :form="form"
                :errors="errors"
            />

            <div class="registration-actions">
                <RouterLink
                    class="auth-step-button auth-step-button--ghost"
                    :to="{ name: 'login' }"
                >
                    Уже есть аккаунт
                </RouterLink>

                <button
                    class="auth-step-button auth-step-button--primary"
                    type="button"
                    @click="goNextStep"
                >
                    Продолжить
                    <i class="fa-solid fa-arrow-right"></i>
                </button>
            </div>
        </template>

        <template v-else>
            <RegisterPasswordFields
                :form="form"
                :errors="errors"
            />

            <RegisterAgreement
                v-model="form.agreement"
                :error="errors.agreement"
            />

            <div class="registration-actions">
                <button
                    class="auth-step-button auth-step-button--ghost"
                    type="button"
                    @click="goPreviousStep"
                >
                    <i class="fa-solid fa-arrow-left"></i>
                    Назад
                </button>

                <AuthSubmitButton
                    :label="selectedRole === 'teacher' ? 'Перейти к коду организации' : 'Создать аккаунт'"
                    loading-label="Создаём аккаунт..."
                    icon="fa-solid fa-user-plus"
                    :is-loading="isSubmitting"
                    :disabled="isSubmitting"
                />
            </div>

            <p class="auth-form-bottom">
                Уже есть аккаунт?
                <RouterLink :to="{ name: 'login' }">
                    Войти
                </RouterLink>
            </p>
        </template>
    </form>
</template>
