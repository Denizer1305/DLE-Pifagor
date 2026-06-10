import type { ContactFeedbackFormErrors } from "@/modules/public/types/contact.types";
import { ApiError } from "@/services/api/api.errors";

type Translator = (value: string) => string;

export function getContactFeedbackResponseStatus(error: unknown): number | null {
    if (error instanceof ApiError) {
        return error.status;
    }

    const response = getErrorResponse(error);

    return typeof response?.status === "number" ? response.status : null;
}

export function getContactFeedbackResponseData(
    error: unknown,
): Record<string, unknown> | null {
    if (error instanceof ApiError && isObject(error.payload)) {
        return error.payload as Record<string, unknown>;
    }

    const data = getErrorResponse(error)?.data;

    return isObject(data) ? data : null;
}

export function applyContactFeedbackBackendErrors(
    responseData: Record<string, unknown>,
    errors: ContactFeedbackFormErrors,
    tr: Translator,
): void {
    errors.topic = getErrorMessage(responseData.topic);
    errors.fullName = getErrorMessage(responseData.full_name || responseData.fullName);
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
        getErrorMessage(responseData.error);

    const hasFieldErrors = Object.entries(errors).some(([key, value]) => {
        return key !== "common" && Boolean(value);
    });

    if (!errors.common && !hasFieldErrors) {
        errors.common = tr("Не удалось отправить сообщение. Проверьте данные и попробуйте ещё раз.");
    }
}

export function getContactFeedbackApiErrorMessage(error: unknown): string {
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

export function isContactFeedbackProfanityMessage(message: string): boolean {
    const normalizedMessage = message.toLowerCase();

    return (
        normalizedMessage.includes("недопустимые выражения") ||
        normalizedMessage.includes("переформулируйте сообщение") ||
        normalizedMessage.includes("нецензур")
    );
}

function getErrorMessage(value: unknown): string {
    if (typeof value === "string") {
        return value;
    }

    if (Array.isArray(value)) {
        return value.map(getErrorMessage).filter(Boolean).join(" ");
    }

    if (isObject(value)) {
        return Object.values(value).map(getErrorMessage).filter(Boolean).join(" ");
    }

    return "";
}

function getErrorResponse(error: unknown): Record<string, unknown> | null {
    if (!isObject(error)) {
        return null;
    }

    return isObject(error.response) ? error.response : null;
}

function isObject(value: unknown): value is Record<string, unknown> {
    return Boolean(value && typeof value === "object" && !Array.isArray(value));
}
