import type {
    ApiErrorResponse,
    ApiFieldErrors,
    ApiListResponse,
    PaginatedApiResponse,
    UserShortDto,
} from "../types";

export interface NormalizedList<TItem> {
    items: TItem[];
    totalCount: number;
    hasNext: boolean;
    hasPrevious: boolean;
}

export function mapApiListResponse<TItem>(
    response: ApiListResponse<TItem>,
): NormalizedList<TItem> {
    if (Array.isArray(response)) {
        return {
            items: response,
            totalCount: response.length,
            hasNext: false,
            hasPrevious: false,
        };
    }

    const paginatedResponse = response as PaginatedApiResponse<TItem>;

    return {
        items: paginatedResponse.results,
        totalCount: paginatedResponse.count,
        hasNext: Boolean(paginatedResponse.next),
        hasPrevious: Boolean(paginatedResponse.previous),
    };
}

export function formatBoolean(value: boolean): string {
    return value ? "Да" : "Нет";
}

export function formatOptional(value: string | number | null | undefined): string {
    if (value === null || value === undefined || value === "") {
        return "Не указано";
    }

    return String(value);
}

export function formatYear(value: number | null | undefined): string {
    if (!value) {
        return "—";
    }

    return String(value);
}

export function formatDateTime(value: string | null | undefined): string {
    if (!value) {
        return "—";
    }

    const date = new Date(value);

    if (Number.isNaN(date.getTime())) {
        return value;
    }

    return new Intl.DateTimeFormat("ru-RU", {
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
    }).format(date);
}

export function formatDate(value: string | null | undefined): string {
    if (!value) {
        return "—";
    }

    const date = new Date(value);

    if (Number.isNaN(date.getTime())) {
        return value;
    }

    return new Intl.DateTimeFormat("ru-RU", {
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
    }).format(date);
}

export function getUserDisplayName(user: UserShortDto | null | undefined): string {
    if (!user) {
        return "Пользователь не указан";
    }

    if (user.full_name) {
        return user.full_name;
    }

    const fullName = [
        user.last_name,
        user.first_name,
        user.middle_name,
    ]
        .filter(Boolean)
        .join(" ")
        .trim();

    return fullName || user.email || user.phone || `Пользователь #${user.id}`;
}

export function getUserContacts(user: UserShortDto | null | undefined): string {
    if (!user) {
        return "Контакты не указаны";
    }

    return [user.email, user.phone].filter(Boolean).join(" · ") || "Контакты не указаны";
}

export function getInitials(value: string): string {
    const parts = value
        .trim()
        .split(/\s+/)
        .filter(Boolean);

    const firstPart = parts[0];
    const secondPart = parts[1];

    if (!firstPart) {
        return "—";
    }

    if (!secondPart) {
        return firstPart.slice(0, 2).toUpperCase();
    }

    return `${firstPart[0] ?? ""}${secondPart[0] ?? ""}`.toUpperCase();
}

export function getApiErrorMessage(error: unknown): string {
    const apiError = error as ApiErrorResponse;

    if (typeof apiError?.detail === "string") {
        return apiError.detail;
    }

    if (typeof apiError?.error?.message === "string") {
        return apiError.error.message;
    }

    return "Не удалось выполнить действие. Попробуйте ещё раз.";
}

export function mapApiFieldErrors(error: unknown): Record<string, string> {
    const apiError = error as ApiErrorResponse;
    const fields = apiError?.error?.fields;

    if (!fields) {
        return {};
    }

    return mapFieldErrors(fields);
}

function mapFieldErrors(fields: ApiFieldErrors): Record<string, string> {
    return Object.entries(fields).reduce<Record<string, string>>(
        (accumulator, [field, value]) => {
            if (Array.isArray(value)) {
                accumulator[field] = value.join(" ");
                return accumulator;
            }

            accumulator[field] = value;
            return accumulator;
        },
        {},
    );
}
