import { computed, reactive, ref } from "vue";
import { useRoute } from "vue-router";

import { useI18n } from "@/composables/useI18n";
import { sendContactFeedback } from "@/modules/public/api/contact-feedback.api";
import {
    applyContactFeedbackBackendErrors,
    getContactFeedbackApiErrorMessage,
    getContactFeedbackResponseData,
    getContactFeedbackResponseStatus,
    isContactFeedbackProfanityMessage,
} from "@/modules/public/composables/contact-feedback-errors";
import {
    createInitialContactFeedbackErrors,
    createInitialContactFeedbackForm,
    normalizeContactFeedbackText,
} from "@/modules/public/composables/contact-feedback-form.state";
import {
    validateContactFeedbackFiles,
    validateContactFeedbackForm,
} from "@/modules/public/composables/contact-feedback-validation";
import type {
    ContactFeedbackFormErrors,
    ContactFeedbackFormState,
} from "@/modules/public/types/contact.types";

export function useContactFeedbackForm() {
    const route = useRoute();
    const { tr } = useI18n();
    const form = reactive<ContactFeedbackFormState>(createInitialContactFeedbackForm());
    const errors = reactive<ContactFeedbackFormErrors>(createInitialContactFeedbackErrors());
    const isSubmitting = ref(false);
    const isSubmitted = ref(false);
    const submitMessage = ref("");

    const selectedFilesText = computed(() => {
        return form.attachments.map((file) => file.name).join(", ");
    });
    const canSubmit = computed(() => {
        return Boolean(
            normalizeContactFeedbackText(form.fullName) &&
            normalizeContactFeedbackText(form.email) &&
            normalizeContactFeedbackText(form.message) &&
            form.isPersonalDataConsent &&
            !isSubmitting.value,
        );
    });

    function clearErrors(): void {
        Object.assign(errors, createInitialContactFeedbackErrors());
    }

    function clearSubmitState(): void {
        isSubmitted.value = false;
        submitMessage.value = "";
    }

    function validateForm(): boolean {
        clearErrors();
        return validateContactFeedbackForm(form, errors, tr);
    }

    function updateFiles(event: Event): void {
        clearSubmitState();
        const input = event.target as HTMLInputElement;
        form.attachments = Array.from(input.files || []);
        validateContactFeedbackFiles(form.attachments, errors, tr);
    }

    function removeFile(fileIndex: number): void {
        clearSubmitState();
        form.attachments = form.attachments.filter((_, index) => index !== fileIndex);
        validateContactFeedbackFiles(form.attachments, errors, tr);
    }

    function resetForm(): void {
        Object.assign(form, createInitialContactFeedbackForm());
        clearErrors();
        clearSubmitState();
    }

    async function submitForm(): Promise<void> {
        clearSubmitState();

        if (!validateForm()) {
            return;
        }

        isSubmitting.value = true;

        try {
            const response = await sendContactFeedback({
                topic: form.topic,
                fullName: normalizeContactFeedbackText(form.fullName),
                email: normalizeContactFeedbackText(form.email),
                phone: normalizeContactFeedbackText(form.phone),
                organizationName: normalizeContactFeedbackText(form.organizationName),
                subject: normalizeContactFeedbackText(form.subject),
                message: form.message.trim(),
                isPersonalDataConsent: form.isPersonalDataConsent,
                pageUrl: window.location.href,
                frontendRoute: route.fullPath,
                attachments: form.attachments,
            });

            isSubmitted.value = true;
            submitMessage.value = response.message || "Спасибо! Ваше сообщение отправлено.";
            Object.assign(form, createInitialContactFeedbackForm());
            clearErrors();
        } catch (error: unknown) {
            handleSubmitError(error);
        } finally {
            isSubmitting.value = false;
        }
    }

    function handleSubmitError(error: unknown): void {
        const status = getContactFeedbackResponseStatus(error);
        const responseData = getContactFeedbackResponseData(error);
        const apiErrorMessage = getContactFeedbackApiErrorMessage(error);

        console.error("Contact feedback error:", responseData || error);

        if (status === 429) {
            errors.common = tr("Вы отправляете сообщения слишком часто. Подождите несколько минут и попробуйте снова.");
            return;
        }

        if (responseData) {
            applyContactFeedbackBackendErrors(responseData, errors, tr);
            return;
        }

        if (isContactFeedbackProfanityMessage(apiErrorMessage)) {
            errors.message = tr(apiErrorMessage);
            errors.common = tr("Пожалуйста, переформулируйте текст обращения.");
            return;
        }

        errors.common = apiErrorMessage
            ? tr(apiErrorMessage)
            : tr("Не удалось отправить сообщение. Проверьте данные и попробуйте ещё раз.");
    }

    return {
        form,
        errors,
        isSubmitting,
        isSubmitted,
        submitMessage,
        selectedFilesText,
        canSubmit,
        submitForm,
        resetForm,
        updateFiles,
        removeFile,
        validateForm,
    };
}
