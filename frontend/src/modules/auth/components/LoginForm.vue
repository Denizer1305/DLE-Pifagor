<script setup lang="ts">
import { RouterLink } from "vue-router";

import { useI18n } from "@/composables/useI18n";
import AuthPasswordField from "@/modules/auth/components/AuthPasswordField.vue";
import AuthSubmitButton from "@/modules/auth/components/AuthSubmitButton.vue";
import { useLoginForm } from "@/modules/auth/composables/useLoginForm";

const {
    form,
    errors,
    isSubmitting,
    canSubmit,
    submitForm,
} = useLoginForm();

const { tr } = useI18n();
</script>

<template>
    <form
        class="login-form"
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
                for="loginEmail"
            >
                Email
            </label>

            <input
                id="loginEmail"
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

        <AuthPasswordField
            id="loginPassword"
            v-model="form.password"
            label="Пароль"
            placeholder="Введите пароль"
            autocomplete="current-password"
            :error="errors.password"
        />

        <div class="auth-form-row">
            <label class="auth-checkbox">
                <input type="checkbox" />
                <span>{{ tr("Запомнить устройство") }}</span>
            </label>

            <RouterLink
                class="auth-form-link"
                :to="{ name: 'forgot-password' }"
            >
                {{ tr("Забыли пароль?") }}
            </RouterLink>
        </div>

        <AuthSubmitButton
            label="Войти в кабинет"
            loading-label="Входим..."
            icon="fa-solid fa-right-to-bracket"
            :is-loading="isSubmitting"
            :disabled="!canSubmit"
        />

        <p class="auth-form-bottom">
            {{ tr("Нет аккаунта?") }}
            <RouterLink :to="{ name: 'register' }">
                {{ tr("Создать аккаунт") }}
            </RouterLink>
        </p>
    </form>
</template>
