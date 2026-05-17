export interface ApiPaginatedResponse<T> {
    count: number;
    next: string | null;
    previous: string | null;
    results: T[];
}

export interface ApiErrorDetail {
    field?: string;
    code?: string;
    message: string;
}

export interface ApiErrorResponse {
    detail?: unknown;
    message?: unknown;
    errors?: Record<string, unknown>;
    non_field_errors?: unknown;
    error?: unknown;
    [key: string]: unknown;
}
