import { computed, reactive, ref } from "vue";

import { ROLE_LABELS } from "@/app/constants/roles.constants";
import { formatRussianPhone } from "@/modules/auth/composables/usePhoneMask";
import { useAuthStore } from "@/stores/auth.store";
import {
    createInitialContactFeedbackErrors,
    createInitialContactFeedbackForm,
    normalizeContactFeedbackText,
} from "@/modules/public/composables/contact-feedback-form.state";
import {
    applyContactFeedbackBackendErrors,
    getContactFeedbackApiErrorMessage,
    getContactFeedbackResponseData,
} from "@/modules/public/composables/contact-feedback-errors";
import { validateContactFeedbackForm } from "@/modules/public/composables/contact-feedback-validation";
import { createFeedbackRequest } from "@/modules/feedback/services/feedback.service";
import { feedbackPageContent } from "@/modules/feedback/data/feedback-page.data";
import { createFeedbackPageModel } from "@/modules/feedback/mappers/feedback-page.mapper";
import type { FeedbackTopic } from "@/modules/feedback/types/feedback.types";

export function useFeedbackPage() {
    const authStore = useAuthStore();
    const form = reactive(createInitialContactFeedbackForm());
    const errors = reactive(createInitialContactFeedbackErrors());
    const isSubmitting = ref(false);
    const isSubmitted = ref(false);
    const submitMessage = ref("");

    const model = computed(() => {
        return createFeedbackPageModel({
            fullName: authStore.userFullName || authStore.user?.email || "",
            roleCode: authStore.activeRole || "",
            roleLabel: authStore.activeRole
                ? ROLE_LABELS[authStore.activeRole]
                : "Пользователь",
            avatarUrl: authStore.avatarUrl || "",
        });
    });

    function fillUserFields(): void {
        form.fullName = authStore.userFullName || "";
        form.email = authStore.user?.email || "";
        form.phone = formatRussianPhone(authStore.user?.phone || "");
        form.organizationName = authStore.organizationName || "";
        form.isPersonalDataConsent = true;
    }

    function resetErrors(): void {
        Object.assign(errors, createInitialContactFeedbackErrors());
    }

    function resetForm(): void {
        Object.assign(form, createInitialContactFeedbackForm());
        fillUserFields();
        resetErrors();
        isSubmitted.value = false;
        submitMessage.value = "";
    }

    function selectTopic(value: string): void {
        if (feedbackPageContent.topics.some((topic) => topic.value === value)) {
            form.topic = value as FeedbackTopic;
        }
    }

    function updateFiles(files: FileList | null): void {
        form.attachments = files ? Array.from(files) : [];
        errors.attachments = "";
    }

    function removeFile(index: number): void {
        form.attachments = form.attachments.filter((_, fileIndex) => fileIndex !== index);
        errors.attachments = "";
    }

    function updatePhone(value: string): void {
        form.phone = formatRussianPhone(value);
        errors.phone = "";
    }

    async function submitForm(): Promise<void> {
        resetErrors();

        if (!validateContactFeedbackForm(form, errors, (value) => value)) {
            return;
        }

        isSubmitting.value = true;
        isSubmitted.value = false;
        submitMessage.value = "";

        try {
            const response = await createFeedbackRequest({
                topic: form.topic,
                fullName: normalizeContactFeedbackText(form.fullName),
                email: normalizeContactFeedbackText(form.email),
                phone: normalizeContactFeedbackText(form.phone),
                organizationName: normalizeContactFeedbackText(form.organizationName),
                subject: normalizeContactFeedbackText(form.subject),
                message: form.message.trim(),
                isPersonalDataConsent: form.isPersonalDataConsent,
                pageUrl: window.location.href,
                frontendRoute: window.location.pathname,
                attachments: form.attachments,
            });

            isSubmitted.value = true;
            submitMessage.value = response.message || feedbackPageContent.form.successText;
        } catch (error) {
            const responseData = getContactFeedbackResponseData(error);

            if (responseData) {
                applyContactFeedbackBackendErrors(responseData, errors, (value) => value);
            } else {
                errors.common =
                    getContactFeedbackApiErrorMessage(error) ||
                    "Не удалось отправить обращение. Проверьте данные и попробуйте еще раз.";
            }
        } finally {
            isSubmitting.value = false;
        }
    }

    fillUserFields();

    return {
        content: feedbackPageContent,
        errors,
        form,
        isSubmitted,
        isSubmitting,
        model,
        submitMessage,
        resetForm,
        removeFile,
        selectTopic,
        submitForm,
        updateFiles,
        updatePhone,
    };
}
