import { computed, reactive, ref } from "vue";
import { useRoute } from "vue-router";

import { sendContactFeedback } from "@/modules/public/api/contact-feedback.api";
import type {
    ContactFeedbackFormErrors,
    ContactFeedbackFormState,
    ContactFeedbackTopic,
} from "@/modules/public/types/contact.types";

import { useI18n } from "@/composables/useI18n";

const MAX_FILES_COUNT = 5;
const MAX_FILE_SIZE = 5 * 1024 * 1024;

const ALLOWED_FILE_EXTENSIONS = [
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".pdf",
    ".doc",
    ".docx",
];

const ALLOWED_FILE_TYPES = [
    "image/jpeg",
    "image/png",
    "image/webp",
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
];

const DEFAULT_TOPIC: ContactFeedbackTopic = "question";

function createInitialForm(): ContactFeedbackFormState {
    return {
        topic: DEFAULT_TOPIC,
        fullName: "",
        email: "",
        phone: "",
        organizationName: "",
        subject: "",
        message: "",
        isPersonalDataConsent: false,
        attachments: [],
    };
}

function createInitialErrors(): ContactFeedbackFormErrors {
    return {
        topic: "",
        fullName: "",
        email: "",
        phone: "",
        organizationName: "",
        subject: "",
        message: "",
        isPersonalDataConsent: "",
        attachments: "",
        common: "",
    };
}

function normalizeText(value: string): string {
    return value.trim().replace(/\s+/g, " ");
}

function isEmailValid(email: string): boolean {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim());
}

function getFileExtension(fileName: string): string {
    const dotIndex = fileName.lastIndexOf(".");

    if (dotIndex === -1) {
        return "";
    }

    return fileName.slice(dotIndex).toLowerCase();
}

function getErrorMessage(value: unknown): string {
    if (!value) {
        return "";
    }

    if (typeof value === "string") {
        return value;
    }

    if (Array.isArray(value)) {
        return value
            .map((item) => getErrorMessage(item))
            .filter(Boolean)
            .join(" ");
    }

    if (typeof value === "object") {
        return Object.values(value)
            .map((item) => getErrorMessage(item))
            .filter(Boolean)
            .join(" ");
    }

    return "";
}

function isObject(value: unknown): value is Record<string, unknown> {
    return Boolean(value && typeof value === "object" && !Array.isArray(value));
}

function getResponseStatus(error: unknown): number | null {
    if (!isObject(error)) {
        return null;
    }

    const response = error.response;

    if (!isObject(response)) {
        return null;
    }

    const status = response.status;

    return typeof status === "number" ? status : null;
}

function getResponseData(error: unknown): Record<string, unknown> | null {
    if (!isObject(error)) {
        return null;
    }

    const response = error.response;

    if (!isObject(response)) {
        return null;
    }

    const data = response.data;

    return isObject(data) ? data : null;
}

export function useContactFeedbackForm() {
    const route = useRoute();

    const form = reactive<ContactFeedbackFormState>(createInitialForm());
    const errors = reactive<ContactFeedbackFormErrors>(createInitialErrors());

    const isSubmitting = ref(false);
    const isSubmitted = ref(false);
    const submitMessage = ref("");
    const { tr } = useI18n();

    const selectedFilesText = computed(() => {
        if (!form.attachments.length) {
            return "";
        }

        return form.attachments
            .map((file) => file.name)
            .join(", ");
    });

    const canSubmit = computed(() => {
        return Boolean(
            normalizeText(form.fullName) &&
            normalizeText(form.email) &&
            normalizeText(form.message) &&
            form.isPersonalDataConsent &&
            !isSubmitting.value,
        );
    });

    function clearErrors(): void {
        Object.assign(errors, createInitialErrors());
    }

    function clearSubmitState(): void {
        isSubmitted.value = false;
        submitMessage.value = "";
    }

    function validateFiles(files: File[]): boolean {
        errors.attachments = "";

        if (!files.length) {
            return true;
        }

        if (files.length > MAX_FILES_COUNT) {
            errors.attachments = tr(`Можно прикрепить не более ${MAX_FILES_COUNT} файлов.`);
            return false;
        }

        const invalidExtensionFile = files.find((file) => {
            const extension = getFileExtension(file.name);

            return !ALLOWED_FILE_EXTENSIONS.includes(extension);
        });

        if (invalidExtensionFile) {
            errors.attachments = tr(`Файл «${invalidExtensionFile.name}» имеет неподдерживаемый формат. Поддерживаются изображения, PDF, DOC и DOCX.`);
            return false;
        }

        const invalidTypeFile = files.find((file) => {
            return file.type && !ALLOWED_FILE_TYPES.includes(file.type);
        });

        if (invalidTypeFile) {
            errors.attachments = tr(`Файл «${invalidTypeFile.name}» имеет неподдерживаемый тип.`);
            return false;
        }

        const oversizedFile = files.find((file) => {
            return file.size > MAX_FILE_SIZE;
        });

        if (oversizedFile) {
            errors.attachments = tr(`Файл «${oversizedFile.name}» больше 5 МБ.`);
            return false;
        }

        return true;
    }

    function validateForm(): boolean {
        clearErrors();

        const fullName = normalizeText(form.fullName);
        const email = normalizeText(form.email);
        const message = form.message.trim();

        if (!fullName) {
            errors.fullName = tr("Укажите имя.");
        } else if (fullName.length < 2) {
            errors.fullName = tr("Имя должно содержать не менее 2 символов.");
        }

        if (!email) {
            errors.email = tr("Укажите email.");
        } else if (!isEmailValid(email)) {
            errors.email = tr("Введите корректный email.");
        }

        if (!message) {
            errors.message = tr("Введите сообщение.");
        } else if (message.length < 10) {
            errors.message = tr("Сообщение должно содержать не менее 10 символов.");
        } else if (message.length > 5000) {
            errors.message = tr("Сообщение не должно превышать 5000 символов.");
        }

        if (!form.isPersonalDataConsent) {
            errors.isPersonalDataConsent =
                tr("Необходимо согласие на обработку персональных данных.");
        }

        validateFiles(form.attachments);

        return !Object.values(errors).some(Boolean);
    }

    function updateFiles(event: Event): void {
        clearSubmitState();

        const input = event.target as HTMLInputElement;
        const files = Array.from(input.files || []);

        form.attachments = files;
        validateFiles(files);
    }

    function removeFile(fileIndex: number): void {
        clearSubmitState();

        form.attachments = form.attachments.filter((_, index) => {
            return index !== fileIndex;
        });

        validateFiles(form.attachments);
    }

    function resetForm(): void {
        Object.assign(form, createInitialForm());
        clearErrors();
        clearSubmitState();
    }

    function applyBackendErrors(responseData: Record<string, unknown>): void {
        errors.topic = getErrorMessage(responseData.topic);
        errors.fullName = getErrorMessage(
            responseData.full_name || responseData.fullName,
        );
        errors.email = getErrorMessage(responseData.email);
        errors.phone = getErrorMessage(responseData.phone);
        errors.organizationName = getErrorMessage(
            responseData.organization_name || responseData.organizationName,
        );
        errors.subject = getErrorMessage(responseData.subject);
        errors.message = getErrorMessage(responseData.message);
        errors.isPersonalDataConsent = getErrorMessage(
            responseData.is_personal_data_consent ||
                responseData.isPersonalDataConsent ||
                responseData.consent,
        );
        errors.attachments = getErrorMessage(responseData.attachments);

        errors.common =
            getErrorMessage(responseData.detail) ||
            getErrorMessage(responseData.non_field_errors) ||
            getErrorMessage(responseData.error) ||
            "";

        const hasFieldErrors = Object.entries(errors).some(([key, value]) => {
            return key !== "common" && Boolean(value);
        });

        if (!errors.common && !hasFieldErrors) {
            errors.common =
                tr("Не удалось отправить сообщение. Проверьте данные и попробуйте ещё раз.");
        }
    }

    function getApiErrorMessage(error: unknown): string {
        if (!error) {
            return "";
        }

        if (error instanceof Error && error.message) {
            return error.message;
        }

        if (isObject(error)) {
            return (
                getErrorMessage(error.message) ||
                getErrorMessage(error.detail) ||
                getErrorMessage(error.error)
            );
        }

        return "";
    }

    function isProfanityMessage(message: string): boolean {
        const normalizedMessage = message.toLowerCase();

        return (
            normalizedMessage.includes("недопустимые выражения") ||
            normalizedMessage.includes("переформулируйте сообщение") ||
            normalizedMessage.includes("нецензур")
        );
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
                fullName: normalizeText(form.fullName),
                email: normalizeText(form.email),
                phone: normalizeText(form.phone),
                organizationName: normalizeText(form.organizationName),
                subject: normalizeText(form.subject),
                message: form.message.trim(),
                isPersonalDataConsent: form.isPersonalDataConsent,
                pageUrl: window.location.href,
                frontendRoute: route.fullPath,
                attachments: form.attachments,
            });

            isSubmitted.value = true;
            submitMessage.value =
                response.message || "Спасибо! Ваше сообщение отправлено.";

            Object.assign(form, createInitialForm());
            clearErrors();
        } catch (error: unknown) {
            const status = getResponseStatus(error);
            const responseData = getResponseData(error);
            const apiErrorMessage = getApiErrorMessage(error);

            console.error("Contact feedback error:", responseData || error);

            if (status === 429) {
                errors.common =
                    tr("Вы отправляете сообщения слишком часто. Подождите несколько минут и попробуйте снова.");
                return;
            }

            if (responseData) {
                applyBackendErrors(responseData);

                if (!Object.values(errors).some(Boolean) && apiErrorMessage) {
                    errors.common = tr(apiErrorMessage);
                }

                return;
            }

            if (apiErrorMessage) {
                if (isProfanityMessage(apiErrorMessage)) {
                    errors.message = tr(apiErrorMessage);
                    errors.common = tr("Пожалуйста, переформулируйте текст обращения.");
                    return;
                }

                errors.common = tr(apiErrorMessage);
                return;
            }

            errors.common =
                tr("Не удалось отправить сообщение. Проверьте данные и попробуйте ещё раз.");
        }finally {
            isSubmitting.value = false;
        }
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