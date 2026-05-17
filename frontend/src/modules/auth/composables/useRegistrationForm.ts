import { computed, reactive, ref } from "vue";
import { useRouter } from "vue-router";

import { useAuthStore } from "@/stores/auth.store";
import { useToastStore } from "@/stores/toast.store";
import { evaluatePasswordStrength } from "@/modules/auth/composables/usePasswordStrength";
import { applyApiErrorsToForm } from "@/modules/auth/utils/form-errors.utils";
import {
    isEmpty,
    isValidEmail,
    isValidRussianPhone,
    normalizeEmail,
    normalizePhone,
    normalizeText,
} from "@/modules/auth/utils/validation.utils";
import type {
    RegisterFormErrors,
    RegisterFormState,
    RegistrationRole,
    RegistrationStep,
} from "@/modules/auth/types/auth-form.types";

export function useRegistrationForm() {
    const router = useRouter();
    const authStore = useAuthStore();
    const toastStore = useToastStore();

    const selectedRole = ref<RegistrationRole>("learner");
    const currentStep = ref<RegistrationStep>(1);
    const isSubmitting = ref(false);
    const isRegistered = ref(false);

    const modal = reactive({
        isOpen: false,
        title: "",
        message: "",
        type: "error" as "error" | "success" | "warning" | "info",
    });

    const form = reactive<RegisterFormState>({
        lastName: "",
        firstName: "",
        middleName: "",
        birthDate: "",
        email: "",
        phone: "",
        password: "",
        passwordConfirm: "",
        agreement: false,
    });

    const errors = reactive<RegisterFormErrors>({
        common: "",
        lastName: "",
        firstName: "",
        middleName: "",
        birthDate: "",
        email: "",
        phone: "",
        password: "",
        passwordConfirm: "",
        agreement: "",
    });

    const stepTitle = computed(() => {
        return currentStep.value === 1
            ? "Основные данные"
            : "Безопасность аккаунта";
    });

    const stepDescription = computed(() => {
        return currentStep.value === 1
            ? "Выберите роль и укажите личные данные."
            : "Создайте пароль и подтвердите согласие на обработку данных.";
    });

    function openModal(
        title: string,
        message: string,
        type: "error" | "success" | "warning" | "info" = "error",
    ): void {
        modal.title = title;
        modal.message = message;
        modal.type = type;
        modal.isOpen = true;
    }

    function closeModal(): void {
        modal.isOpen = false;
    }

    function clearErrors(): void {
        Object.keys(errors).forEach((key) => {
            errors[key as keyof RegisterFormErrors] = "";
        });
    }

    function validateStepOne(): boolean {
        clearErrors();

        if (isEmpty(form.lastName)) {
            errors.lastName = "Укажите фамилию.";
        }

        if (isEmpty(form.firstName)) {
            errors.firstName = "Укажите имя.";
        }

        if (selectedRole.value === "learner" && isEmpty(form.birthDate)) {
            errors.birthDate = "Укажите дату рождения учащегося.";
        }

        if (isEmpty(form.email)) {
            errors.email = "Укажите email.";
        } else if (!isValidEmail(form.email)) {
            errors.email = "Введите email полностью.";
        }

        if (isEmpty(form.phone)) {
            errors.phone = "Укажите телефон.";
        } else if (!isValidRussianPhone(form.phone)) {
            errors.phone = "Введите телефон в формате +7 999 999-99-99.";
        }

        const firstError =
            errors.lastName ||
            errors.firstName ||
            errors.birthDate ||
            errors.email ||
            errors.phone;

        if (firstError) {
            toastStore.warning(firstError);
            return false;
        }

        return true;
    }

    function validateStepTwo(): boolean {
        clearErrors();

        const passwordStrength = evaluatePasswordStrength(form.password);

        if (!passwordStrength.isValid) {
            errors.password = "Пароль должен содержать минимум 8 символов, заглавную букву и цифру.";
        }

        if (!form.passwordConfirm) {
            errors.passwordConfirm = "Повторите пароль.";
        } else if (form.password !== form.passwordConfirm) {
            errors.passwordConfirm = "Пароли не совпадают.";
        }

        if (!form.agreement) {
            errors.agreement = "Необходимо принять условия использования.";
        }

        const firstError =
            errors.password ||
            errors.passwordConfirm ||
            errors.agreement;

        if (firstError) {
            toastStore.warning(firstError);
            return false;
        }

        return true;
    }

    function goNextStep(): void {
        if (!validateStepOne()) {
            return;
        }

        currentStep.value = 2;
    }

    function goPreviousStep(): void {
        currentStep.value = 1;
    }

    function getBasePayload() {
        return {
            email: normalizeEmail(form.email),
            phone: normalizePhone(form.phone),
            password: form.password,
            first_name: normalizeText(form.firstName),
            last_name: normalizeText(form.lastName),
            middle_name: normalizeText(form.middleName),
            birth_date: form.birthDate || null,
        };
    }

    async function submitRegistration(): Promise<void> {
        const payload = getBasePayload();

        if (selectedRole.value === "teacher") {
            sessionStorage.setItem(
                "pifagor.teacher.registration.draft",
                JSON.stringify(payload),
            );

            await router.push({ name: "teacher-organization-code" });
            return;
        }

        if (selectedRole.value === "guardian") {
            await authStore.registerGuardian(payload);
            return;
        }

        await authStore.registerLearner(payload);
    }

    async function submitForm(): Promise<void> {
        if (!validateStepTwo()) {
            return;
        }

        isSubmitting.value = true;

        try {
            await submitRegistration();

            if (selectedRole.value !== "teacher") {
                isRegistered.value = true;

                openModal(
                    "Проверьте почту",
                    "Мы отправили письмо для подтверждения email. После подтверждения можно будет войти в аккаунт.",
                    "success",
                );
            }
        } catch (error) {
            const message = applyApiErrorsToForm(
                error,
                errors,
                {
                    first_name: "firstName",
                    last_name: "lastName",
                    middle_name: "middleName",
                    birth_date: "birthDate",
                    email: "email",
                    phone: "phone",
                    password: "password",
                    password_confirm: "passwordConfirm",
                    non_field_errors: "common",
                    detail: "common",
                },
            );

            openModal("Не удалось создать аккаунт", message, "error");
        } finally {
            isSubmitting.value = false;
        }
    }

    async function goToLogin(): Promise<void> {
        await router.push({ name: "login" });
    }

    return {
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
    };
}