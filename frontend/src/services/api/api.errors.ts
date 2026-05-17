import type { AxiosError } from "axios";
import type { ApiErrorResponse } from "./api.types";

export class ApiError extends Error {
    public readonly status: number | null;
    public readonly payload: ApiErrorResponse | null;

    constructor(message: string, status: number | null = null, payload: ApiErrorResponse | null = null) {
        super(message);

        this.name = "ApiError";
        this.status = status;
        this.payload = payload;
    }
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

function getPayloadMessage(payload: ApiErrorResponse | null | undefined): string {
    if (!payload) {
        return "";
    }

    if (payload.error && typeof payload.error === "object" && "message" in payload.error) {
        return stringifyErrorValue((payload.error as Record<string, unknown>).message);
    }

    return (
        stringifyErrorValue(payload.detail) ||
        stringifyErrorValue(payload.message) ||
        stringifyErrorValue(payload.non_field_errors) ||
        stringifyErrorValue(payload.errors)
    );
}

export function normalizeApiError(error: unknown): ApiError {
    const axiosError = error as AxiosError<ApiErrorResponse>;

    if (axiosError.response) {
        const payload = axiosError.response.data;
        const message = getPayloadMessage(payload) || "Произошла ошибка при выполнении запроса.";

        return new ApiError(message, axiosError.response.status, payload);
    }

    if (axiosError.request) {
        return new ApiError("Сервер не отвечает. Проверьте подключение и попробуйте ещё раз.");
    }

    if (error instanceof Error) {
        return new ApiError(error.message);
    }

    return new ApiError("Произошла неизвестная ошибка.");
}
