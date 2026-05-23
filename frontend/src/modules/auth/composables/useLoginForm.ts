import { computed, reactive, ref } from "vue";
import { useRoute, useRouter } from "vue-router";

import { useAuthStore } from "@/stores/auth.store";
import { isEmpty, normalizeEmail } from "@/modules/auth/utils/validation.utils";
import { redirectAfterLogin } from "@/modules/auth/utils/auth-redirect.utils";
import { applyApiErrorsToForm } from "@/modules/auth/utils/form-errors.utils";

interface LoginFormState {
    email: string;
    password: string;
}

interface LoginFormErrors {
    email: string;
    password: string;
    common: string;
}

export function useLoginForm() {
    const route = useRoute();
    const router = useRouter();
    const authStore = useAuthStore();

    const form = reactive<LoginFormState>({
        email: "",
        password: "",
    });

    const errors = reactive<LoginFormErrors>({
        email: "",
        password: "",
        common: "",
    });

    const isSubmitting = ref(false);

    const canSubmit = computed(() => {
        return Boolean(form.email.trim() && form.password.trim() && !isSubmitting.value);
    });

    function clearErrors(): void {
        errors.email = "";
        errors.password = "";
        errors.common = "";
    }

    function validateForm(): boolean {
        clearErrors();

        if (isEmpty(form.email)) {
            errors.email = "Укажите email.";
        }

        if (isEmpty(form.password)) {
            errors.password = "Укажите пароль.";
        }

        return !errors.email && !errors.password;
    }

    async function submitForm(): Promise<void> {
        if (!validateForm()) {
            return;
        }

        isSubmitting.value = true;

        try {
            await authStore.login({
                email: normalizeEmail(form.email),
                password: form.password,
            });

            await redirectAfterLogin(
                router,
                route,
                authStore.activeRole,
                authStore.isSuperuser,
            );
        } catch (error) {
            applyApiErrorsToForm(
                error,
                errors,
                {
                    email: "email",
                    password: "password",
                },
                "Не удалось войти. Проверьте email и пароль.",
            );
        } finally {
            isSubmitting.value = false;
        }
    }

    return {
        form,
        errors,
        isSubmitting,
        canSubmit,
        submitForm,
    };
}
