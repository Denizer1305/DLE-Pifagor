<script setup lang="ts">
import { RouterLink } from "vue-router";

import { useI18n } from "@/composables/useI18n";
import AuthPasswordField from "@/modules/auth/components/AuthPasswordField.vue";
import AuthSubmitButton from "@/modules/auth/components/AuthSubmitButton.vue";
import { useResetPasswordForm } from "@/modules/auth/composables/useResetPasswordForm";

const {
    form,
    errors,
    isSubmitting,
    isCompleted,
    passwordChecks,
    passwordStrengthLabel,
    passwordStrengthWidth,
    submitForm,
    successMessage,
} = useResetPasswordForm();

const { tr } = useI18n();
</script>

<template>
    <div
        v-if="isCompleted"
        class="auth-success-box"
    >
        <div class="auth-success-box__icon">
            <i class="fa-solid fa-circle-check"></i>
        </div>

        <h3 class="auth-success-box__title">
            {{ tr("Пароль обновлён") }}
        </h3>

        <p class="auth-success-box__text">
            {{ tr(successMessage || "Теперь можно войти в аккаунт с новым паролем.") }}
        </p>

        <RouterLink
            class="auth-submit-btn"
            :to="{ name: 'login' }"
        >
            {{ tr("Перейти ко входу") }}
            <i class="fa-solid fa-right-to-bracket"></i>
        </RouterLink>
    </div>

    <form
        v-else
        class="reset-password-form"
        @submit.prevent="submitForm"
    >
        <div
            v-if="errors.common"
            class="form-alert form-alert--error"
        >
            <i class="fa-solid fa-circle-exclamation"></i>
            {{ tr(errors.common) }}
        </div>

        <AuthPasswordField
            id="newPassword"
            v-model="form.password"
            label="Новый пароль"
            placeholder="Введите новый пароль"
            autocomplete="new-password"
            :error="errors.password"
        />

        <div class="password-strength">
            <div class="password-strength__top">
                <span>{{ tr("Надёжность пароля") }}</span>
                <strong>{{ tr(passwordStrengthLabel) }}</strong>
            </div>

            <div class="password-strength__track">
                <div
                    class="password-strength__fill"
                    :style="{ width: passwordStrengthWidth }"
                ></div>
            </div>
        </div>

        <ul class="password-rules">
            <li :class="{ valid: passwordChecks.length }">
                <i :class="passwordChecks.length ? 'fa-solid fa-check-circle' : 'fa-regular fa-circle'"></i>
                {{ tr("Минимум 8 символов") }}
            </li>

            <li :class="{ valid: passwordChecks.upper }">
                <i :class="passwordChecks.upper ? 'fa-solid fa-check-circle' : 'fa-regular fa-circle'"></i>
                {{ tr("Заглавная буква") }}
            </li>

            <li :class="{ valid: passwordChecks.digit }">
                <i :class="passwordChecks.digit ? 'fa-solid fa-check-circle' : 'fa-regular fa-circle'"></i>
                {{ tr("Минимум одна цифра") }}
            </li>
        </ul>

        <AuthPasswordField
            id="confirmPassword"
            v-model="form.passwordConfirm"
            label="Повторите пароль"
            placeholder="Повторите новый пароль"
            autocomplete="new-password"
            :error="errors.passwordConfirm"
        />

        <AuthSubmitButton
            label="Обновить пароль"
            loading-label="Обновляем..."
            icon="fa-solid fa-check"
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
