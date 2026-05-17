import { reactive, ref } from "vue";
import { useRouter } from "vue-router";

import { useAuthStore } from "@/stores/auth.store";
import { applyApiErrorsToForm } from "@/modules/auth/utils/form-errors.utils";
import {
    clearTeacherRegistrationDraft,
    getTeacherRegistrationDraft,
} from "@/modules/auth/utils/teacher-registration-draft.utils";

interface TeacherOrganizationCodeFormState {
    inviteCode: string;
}

interface TeacherOrganizationCodeFormErrors {
    common: string;
    inviteCode: string;
}

export function useTeacherOrganizationCodeForm() {
    const router = useRouter();
    const authStore = useAuthStore();

    const form = reactive<TeacherOrganizationCodeFormState>({
        inviteCode: "",
    });

    const errors = reactive<TeacherOrganizationCodeFormErrors>({
        common: "",
        inviteCode: "",
    });

    const modal = reactive({
        isOpen: false,
        title: "",
        message: "",
        type: "error" as "error" | "success" | "warning" | "info",
    });

    const isSubmitting = ref(false);
    const isCompleted = ref(false);

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
        errors.common = "";
        errors.inviteCode = "";
    }

    function validateForm(): boolean {
        clearErrors();

        if (!form.inviteCode.trim()) {
            errors.inviteCode = "Введите код образовательной организации.";
            openModal("Введите код", "Без кода организации преподаватель не может отправить заявку.", "warning");

            return false;
        }

        return true;
    }

    async function submitForm(): Promise<void> {
        if (!validateForm()) {
            return;
        }

        const draft = getTeacherRegistrationDraft();

        if (!draft) {
            openModal(
                "Данные регистрации не найдены",
                "Вернитесь на страницу регистрации и заполните данные преподавателя заново.",
                "warning",
            );

            return;
        }

        isSubmitting.value = true;

        try {
            await authStore.registerTeacher({
                ...draft,
                invite_code: form.inviteCode.trim(),
            });

            clearTeacherRegistrationDraft();
            isCompleted.value = true;

            openModal(
                "Заявка отправлена",
                "Мы отправили письмо для подтверждения email. После подтверждения заявка уйдёт администратору организации.",
                "success",
            );
        } catch (error) {
            const message = applyApiErrorsToForm(
                error,
                errors,
                {
                    invite_code: "inviteCode",
                    code: "inviteCode",
                    non_field_errors: "common",
                    detail: "common",
                },
            );

            openModal("Код не принят", message, "error");
        } finally {
            isSubmitting.value = false;
        }
    }

    async function goBackToRegistration(): Promise<void> {
        await router.push({ name: "register" });
    }

    async function goToLogin(): Promise<void> {
        await router.push({ name: "login" });
    }

    return {
        form,
        errors,
        modal,
        isSubmitting,
        isCompleted,

        closeModal,
        submitForm,
        goBackToRegistration,
        goToLogin,
    };
}