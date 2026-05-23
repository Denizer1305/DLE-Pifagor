<script setup lang="ts">
import { RouterLink } from "vue-router";

import { useI18n } from "@/composables/useI18n";
import AuthSubmitButton from "@/modules/auth/components/AuthSubmitButton.vue";
import { useForgotPasswordForm } from "@/modules/auth/composables/useForgotPasswordForm";

const {
    form,
    errors,
    isSubmitting,
    isSent,
    submitForm,
    successMessage,
} = useForgotPasswordForm();

const { tr } = useI18n();
</script>

<template>
    <div
        v-if="isSent"
        class="auth-success-box"
    >
        <div class="auth-success-box__icon">
            <i class="fa-solid fa-envelope-circle-check"></i>
        </div>

        <h3 class="auth-success-box__title">
            {{ tr("Письмо отправлено") }}
        </h3>

        <p class="auth-success-box__text">
            {{ tr(successMessage || "Если аккаунт с таким email существует, мы отправили инструкцию для восстановления доступа.") }}
        </p>

        <RouterLink
            class="auth-submit-btn"
            :to="{ name: 'login' }"
        >
            {{ tr("Вернуться ко входу") }}
            <i class="fa-solid fa-right-to-bracket"></i>
        </RouterLink>
    </div>

    <form
        v-else
        class="forgot-password-form"
        @submit.prevent="submitForm"
    >
        <div
            v-if="errors.common"
            class="form-alert form-alert--error"
        >
            <i class="fa-solid fa-circle-exclamation"></i>
            {{ tr(errors.common) }}
        </div>

        <div class="form-group full">
            <label
                class="form-label"
                for="forgotEmail"
            >
                Email
            </label>

            <input
                id="forgotEmail"
                v-model="form.email"
                class="form-input"
                :class="{ 'is-invalid': errors.email }"
                type="email"
                placeholder="name@example.com"
                autocomplete="email"
            />

            <p
                v-if="errors.email"
                class="form-error"
            >
                {{ tr(errors.email) }}
            </p>
        </div>

        <AuthSubmitButton
            label="Отправить инструкцию"
            loading-label="Отправляем..."
            icon="fa-solid fa-paper-plane"
            :is-loading="isSubmitting"
        />

        <p class="auth-form-bottom">
            {{ tr("Вспомнили пароль?") }}
            <RouterLink :to="{ name: 'login' }">
                {{ tr("Вернуться ко входу") }}
            </RouterLink>
        </p>
    </form>
</template>
