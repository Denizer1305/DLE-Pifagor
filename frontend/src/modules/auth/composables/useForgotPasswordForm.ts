import { reactive, ref } from "vue";

import { forgotPassword } from "@/modules/auth/api/auth.api";
import { applyApiErrorsToForm } from "@/modules/auth/utils/form-errors.utils";
import { isEmpty, isValidEmail, normalizeEmail } from "@/modules/auth/utils/validation.utils";

interface ForgotPasswordFormState {
    email: string;
}

interface ForgotPasswordFormErrors {
    email: string;
    common: string;
}

export function useForgotPasswordForm() {
    const form = reactive<ForgotPasswordFormState>({
        email: "",
    });

    const errors = reactive<ForgotPasswordFormErrors>({
        email: "",
        common: "",
    });

    const isSubmitting = ref(false);
    const isSent = ref(false);
    const successMessage = ref("");

    function clearErrors(): void {
        errors.email = "";
        errors.common = "";
    }

    function validateForm(): boolean {
        clearErrors();

        if (isEmpty(form.email)) {
            errors.email = "Укажите email для восстановления доступа.";
            return false;
        }

        if (!isValidEmail(form.email)) {
            errors.email = "Введите корректный email в формате name@example.com.";
            return false;
        }

        return true;
    }

    async function submitForm(): Promise<void> {
        if (!validateForm()) {
            return;
        }

        isSubmitting.value = true;

        try {
            const response = await forgotPassword({
                email: normalizeEmail(form.email),
            });

            successMessage.value = response.message;
            isSent.value = true;
        } catch (error) {
            applyApiErrorsToForm(
                error,
                errors,
                {
                    email: "email",
                    non_field_errors: "common",
                    detail: "common",
                },
                "Не удалось отправить письмо. Попробуйте позже.",
            );
        } finally {
            isSubmitting.value = false;
        }
    }

    return {
        form,
        errors,
        isSubmitting,
        isSent,
        successMessage,
        submitForm,
    };
}
