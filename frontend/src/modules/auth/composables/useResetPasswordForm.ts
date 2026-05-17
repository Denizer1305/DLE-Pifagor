import { computed, reactive, ref, toRef } from "vue";
import { useRoute } from "vue-router";

import { resetPassword } from "@/modules/auth/api/auth.api";
import { usePasswordStrength } from "@/modules/auth/composables/usePasswordStrength";
import { applyApiErrorsToForm } from "@/modules/auth/utils/form-errors.utils";

interface ResetPasswordFormState {
    password: string;
    passwordConfirm: string;
}

interface ResetPasswordFormErrors {
    common: string;
    password: string;
    passwordConfirm: string;
}

export function useResetPasswordForm() {
    const route = useRoute();

    const form = reactive<ResetPasswordFormState>({
        password: "",
        passwordConfirm: "",
    });

    const errors = reactive<ResetPasswordFormErrors>({
        common: "",
        password: "",
        passwordConfirm: "",
    });

    const isSubmitting = ref(false);
    const isCompleted = ref(false);
    const successMessage = ref("");

    const token = computed(() => {
        const value = route.query.token;

        return typeof value === "string" ? value : "";
    });

    const passwordRef = toRef(form, "password");

    const {
        checks: passwordChecks,
        label: passwordStrengthLabel,
        width: passwordStrengthWidth,
        isValid: isPasswordValid,
    } = usePasswordStrength(passwordRef);

    const passwordsMatch = computed(() => {
        return Boolean(form.password && form.passwordConfirm && form.password === form.passwordConfirm);
    });

    function clearErrors(): void {
        errors.common = "";
        errors.password = "";
        errors.passwordConfirm = "";
    }

    function validateForm(): boolean {
        clearErrors();

        if (!token.value) {
            errors.common = "В ссылке восстановления нет токена. Запросите письмо повторно.";
        }

        if (!isPasswordValid.value) {
            errors.password = "Пароль должен содержать минимум 8 символов, заглавную букву и цифру.";
        }

        if (!form.passwordConfirm) {
            errors.passwordConfirm = "Повторите пароль.";
        } else if (!passwordsMatch.value) {
            errors.passwordConfirm = "Пароли не совпадают.";
        }

        return !errors.common && !errors.password && !errors.passwordConfirm;
    }

    async function submitForm(): Promise<void> {
        if (!validateForm()) {
            return;
        }

        isSubmitting.value = true;

        try {
            const response = await resetPassword({
                token: token.value,
                password: form.password,
                password_confirm: form.passwordConfirm,
            });

            successMessage.value = response.message;
            isCompleted.value = true;
        } catch (error) {
            applyApiErrorsToForm(
                error,
                errors,
                {
                    token: "common",
                    password: "password",
                    password_confirm: "passwordConfirm",
                    non_field_errors: "common",
                    detail: "common",
                },
                "Не удалось обновить пароль. Попробуйте позже.",
            );
        } finally {
            isSubmitting.value = false;
        }
    }

    return {
        form,
        errors,
        isSubmitting,
        isCompleted,
        successMessage,
        passwordChecks,
        passwordStrengthLabel,
        passwordStrengthWidth,
        passwordsMatch,
        submitForm,
    };
}