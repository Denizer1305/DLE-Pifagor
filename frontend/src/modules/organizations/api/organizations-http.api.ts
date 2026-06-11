import { httpClient } from "@/services/api/http.client";
import type { ApiListResponse } from "../types";

export async function getApiList<TItem, TQuery extends object = object>(
    url: string,
    query?: TQuery,
): Promise<ApiListResponse<TItem>> {
    const response = await httpClient.get<ApiListResponse<TItem>>(url, {
        params: query,
    });

    return response.data;
}

export async function getApiDetail<TData>(url: string): Promise<TData> {
    const response = await httpClient.get<TData>(url);

    return response.data;
}

export async function postApi<TData, TPayload = unknown>(
    url: string,
    payload?: TPayload,
): Promise<TData> {
    const response = await httpClient.post<TData>(url, payload);

    return response.data;
}

export async function patchApi<TData, TPayload = unknown>(
    url: string,
    payload: TPayload,
): Promise<TData> {
    const response = await httpClient.patch<TData>(url, payload);

    return response.data;
}

export async function deleteApi<TData>(url: string): Promise<TData> {
    const response = await httpClient.delete<TData>(url);

    return response.data;
}
