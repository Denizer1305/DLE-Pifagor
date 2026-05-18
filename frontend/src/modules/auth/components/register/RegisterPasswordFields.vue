<script setup lang="ts">
import AuthPasswordField from "@/modules/auth/components/AuthPasswordField.vue";
import PasswordRequirementsHint from "@/modules/auth/components/PasswordRequirementsHint.vue";
import type {
    RegisterFormErrors,
    RegisterFormState,
} from "@/modules/auth/types/auth-form.types";

interface Props {
    form: RegisterFormState;
    errors: RegisterFormErrors;
}

defineProps<Props>();
</script>

<template>
    <div class="form-grid">
        <AuthPasswordField
            id="registerPassword"
            v-model="form.password"
            label="Пароль"
            placeholder="Минимум 8 символов"
            autocomplete="new-password"
            :error="errors.password"
        />

        <AuthPasswordField
            id="registerPasswordConfirm"
            v-model="form.passwordConfirm"
            label="Повторите пароль"
            placeholder="Повторите пароль"
            autocomplete="new-password"
            :error="errors.passwordConfirm"
        />
    </div>

    <PasswordRequirementsHint
        :password="form.password"
        :password-confirm="form.passwordConfirm"
        show-match-rule
    />
</template>
