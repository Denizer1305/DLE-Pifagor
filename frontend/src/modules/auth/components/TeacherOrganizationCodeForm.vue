<script setup lang="ts">
import { useI18n } from "@/composables/useI18n";
import AuthMessageModal from "@/modules/auth/components/AuthMessageModal.vue";
import AuthSubmitButton from "@/modules/auth/components/AuthSubmitButton.vue";
import { useTeacherOrganizationCodeForm } from "@/modules/auth/composables/useTeacherOrganizationCodeForm";

const { tr } = useI18n();

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
            {{ tr("Проверьте почту") }}
        </h3>

        <p class="auth-success-box__text">
            {{ tr("Мы отправили письмо для подтверждения email. После подтверждения заявка преподавателя будет рассмотрена организацией.") }}
        </p>

        <button
            class="auth-submit-btn"
            type="button"
            @click="goToLogin"
        >
            {{ tr("Перейти ко входу") }}
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
                {{ tr("Код образовательной организации") }}
            </label>

            <input
                id="inviteCode"
                v-model="form.inviteCode"
                class="form-input"
                :class="{ 'is-invalid': errors.inviteCode }"
                type="text"
                autocomplete="off"
                :placeholder="tr('Введите код, который выдала организация')"
            />

            <p
                v-if="errors.inviteCode"
                class="form-error"
            >
                {{ tr(errors.inviteCode) }}
            </p>

            <p class="form-hint">
                {{ tr("После проверки кода мы создадим аккаунт и отправим заявку администратору образовательной организации.") }}
            </p>
        </div>

        <div class="registration-actions">
            <button
                class="auth-step-button auth-step-button--ghost"
                type="button"
                @click="goBackToRegistration"
            >
                <i class="fa-solid fa-arrow-left"></i>
                {{ tr("Назад") }}
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
