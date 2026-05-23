import { ApiError } from "@/services/api/api.errors";

export type FormErrors = Record<string, string>;
export type ApiFieldMap = Record<string, string>;

const DEFAULT_FORM_ERROR_MESSAGE = "Проверьте данные и попробуйте ещё раз.";

interface ParsedApiError {
    fieldErrors: Record<string, string>;
    message: string;
}

function stringifyErrorValue(value: unknown): string {
    if (typeof value === "string") {
        return value;
    }

    if (Array.isArray(value)) {
        return value.map(stringifyErrorValue).filter(Boolean).join(" ");
    }

    if (value && typeof value === "object") {
        return Object.values(value).map(stringifyErrorValue).filter(Boolean).join(" ");
    }

    return "";
}

function isRecord(value: unknown): value is Record<string, unknown> {
    return Boolean(value) && typeof value === "object" && !Array.isArray(value);
}

export function parseApiFormError(error: unknown): ParsedApiError {
    const result: ParsedApiError = {
        fieldErrors: {},
        message: "",
    };

    if (!(error instanceof ApiError) || !error.payload) {
        result.message = error instanceof Error
            ? error.message
            : "Произошла ошибка при выполнении запроса.";

        return result;
    }

    const payload = error.payload;

    if (isRecord(payload.error)) {
        const wrappedError = payload.error;

        result.message =
            stringifyErrorValue(wrappedError.message) ||
            stringifyErrorValue(wrappedError.detail) ||
            stringifyErrorValue(payload.message) ||
            stringifyErrorValue(payload.detail);

        if (isRecord(wrappedError.details)) {
            Object.entries(wrappedError.details).forEach(([field, value]) => {
                result.fieldErrors[field] = stringifyErrorValue(value);
            });
        }

        return result;
    }

    result.message =
        stringifyErrorValue(payload.message) ||
        stringifyErrorValue(payload.detail) ||
        stringifyErrorValue(payload.non_field_errors);

    if (isRecord(payload.errors)) {
        Object.entries(payload.errors).forEach(([field, value]) => {
            result.fieldErrors[field] = stringifyErrorValue(value);
        });
    }

    Object.entries(payload).forEach(([field, value]) => {
        if (
            field === "message" ||
            field === "detail" ||
            field === "errors" ||
            field === "error"
        ) {
            return;
        }

        result.fieldErrors[field] = stringifyErrorValue(value);
    });

    return result;
}

export function applyApiErrorsToForm(
    error: unknown,
    errors: FormErrors,
    fieldMap: ApiFieldMap = {},
    fallbackMessage = DEFAULT_FORM_ERROR_MESSAGE,
): string {
    const parsedError = parseApiFormError(error);

    Object.entries(parsedError.fieldErrors).forEach(([apiField, message]) => {
        const formField = fieldMap[apiField] || apiField;

        if (formField in errors) {
            errors[formField] = message;
        }
    });

    const message = parsedError.message || fallbackMessage;

    if ("common" in errors && !errors.common) {
        errors.common = message;
    }

    return message;
}
