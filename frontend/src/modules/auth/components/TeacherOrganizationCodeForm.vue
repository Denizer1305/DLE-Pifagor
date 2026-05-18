<script setup lang="ts">
import AuthMessageModal from "@/modules/auth/components/AuthMessageModal.vue";
import AuthSubmitButton from "@/modules/auth/components/AuthSubmitButton.vue";
import { useTeacherOrganizationCodeForm } from "@/modules/auth/composables/useTeacherOrganizationCodeForm";

const {
    form,
    errors,
    modal,
    isSubmitting,
    isCompleted,

    closeModal,
    submitForm,
    goBackToRegistration,
    goToLogin,
} = useTeacherOrganizationCodeForm();
</script>

<template>
    <AuthMessageModal
        :is-open="modal.isOpen"
        :title="modal.title"
        :message="modal.message"
        :type="modal.type"
        @close="closeModal"
    />

    <div
        v-if="isCompleted"
        class="auth-success-box"
    >
        <div class="auth-success-box__icon">
            <i class="fa-solid fa-envelope-circle-check"></i>
        </div>

        <h3 class="auth-success-box__title">
            Проверьте почту
        </h3>

        <p class="auth-success-box__text">
            Мы отправили письмо для подтверждения email. После подтверждения заявка преподавателя будет рассмотрена организацией.
        </p>

        <button
            class="auth-submit-btn"
            type="button"
            @click="goToLogin"
        >
            Перейти ко входу
            <i class="fa-solid fa-right-to-bracket"></i>
        </button>
    </div>

    <form
        v-else
        class="teacher-code-form"
        novalidate
        @submit.prevent="submitForm"
    >
        <div class="form-group full">
            <label
                class="form-label"
                for="inviteCode"
            >
                Код образовательной организации
            </label>

            <input
                id="inviteCode"
                v-model="form.inviteCode"
                class="form-input"
                :class="{ 'is-invalid': errors.inviteCode }"
                type="text"
                autocomplete="off"
                placeholder="Введите код, который выдала организация"
            />

            <p
                v-if="errors.inviteCode"
                class="form-error"
            >
                {{ errors.inviteCode }}
            </p>

            <p class="form-hint">
                После проверки кода мы создадим аккаунт и отправим заявку администратору образовательной организации.
            </p>
        </div>

        <div class="registration-actions">
            <button
                class="auth-step-button auth-step-button--ghost"
                type="button"
                @click="goBackToRegistration"
            >
                <i class="fa-solid fa-arrow-left"></i>
                Назад
            </button>

            <AuthSubmitButton
                label="Отправить заявку"
                loading-label="Проверяем код..."
                icon="fa-solid fa-paper-plane"
                :is-loading="isSubmitting"
                :disabled="isSubmitting"
            />
        </div>
    </form>
</template>
